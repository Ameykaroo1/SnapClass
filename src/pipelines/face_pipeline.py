import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_five_point_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get("face_embedding")

        if embedding is not None and len(embedding) > 0:
            X.append(np.array(embedding))
            y.append(student["student_id"])

    if len(X) == 0:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(X, y)
    except ValueError:
        return None

    return {
        "clf": clf,
        "X": X,
        "y": y
    }


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return model_data is not None


def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if model_data is None:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    X = model_data["X"]
    y = model_data["y"]

    all_students = sorted(list(set(y)))

    for encoding in encodings:

        # Predict student
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = all_students[0]

        # Get stored embedding
        try:
            student_embedding = X[y.index(predicted_id)]
        except ValueError:
            continue

        # Euclidean distance
        distance = np.linalg.norm(student_embedding - encoding)

        threshold = 0.6

        if distance <= threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)