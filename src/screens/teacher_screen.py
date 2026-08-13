import streamlit as st
import time

from src.ui.base_layout import style_backgroud_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
)
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np
from src.database.config import supabase
from datetime import datetime
from src.components.dialog_voice_attendance import voice_attendance_dialog
import pandas as pd

# NOTE: import your voice attendance dialog here once it exists, then
# flip the disabled=True flag below to False, e.g.:
# from src.components.dialog_voice_attendance import voice_attendance_dialog


# ===========================
# MAIN SCREEN
# ===========================

def teacher_screen():

    style_backgroud_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    else:
        teacher_screen_register()


# ===========================
# LOGIN
# ===========================

def login_teacher(username, password):

    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:

        st.session_state.teacher_data = teacher
        st.session_state.user_role = "teacher"
        st.session_state.is_logged_in = True

        return True

    return False


def teacher_screen_login():

    c1, c2 = st.columns(2)

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            key="teacher_back_login",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Teacher Login")

    teacher_username = st.text_input(
        "Username",
        placeholder="ananyaroy",
    )

    teacher_password = st.text_input(
        "Password",
        type="password",
    )

    st.divider()

    b1, b2 = st.columns(2)

    with b1:

        if st.button(
            "Login",
            use_container_width=True,
        ):

            if login_teacher(
                teacher_username,
                teacher_password,
            ):
                st.toast("Welcome back! 🎉")
                time.sleep(1)
                st.rerun()

            else:
                st.error("Invalid username or password")

    with b2:

        if st.button(
            "Register Instead",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# ===========================
# REGISTER
# ===========================

def register_teacher(
    username,
    name,
    password,
    confirm_password,
):

    if not username or not name or not password:
        return False, "All fields are required."

    if password != confirm_password:
        return False, "Passwords do not match."

    if check_teacher_exists(username):
        return False, "Username already exists."

    try:

        create_teacher(
            username,
            password,
            name,
        )

        return True, "Registration successful."

    except Exception as e:
        return False, str(e)


def teacher_screen_register():

    c1, c2 = st.columns(2)

    with c1:
        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            key="teacher_back_register",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Teacher Registration")

    username = st.text_input(
        "Username",
        placeholder="ananyaroy",
    )

    name = st.text_input(
        "Name",
        placeholder="Ananya Roy",
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password",
    )

    st.divider()

    b1, b2 = st.columns(2)

    with b1:

        if st.button(
            "Register",
            use_container_width=True,
        ):

            success, message = register_teacher(
                username,
                name,
                password,
                confirm,
            )

            if success:

                st.success(message)
                time.sleep(1)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    with b2:

        if st.button(
            "Login Instead",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()


# ===========================
# DASHBOARD
# ===========================

def teacher_dashboard():

    teacher = st.session_state["teacher_data"]

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    c1, c2 = st.columns([3, 1], vertical_alignment='bottom')

    with c1:
        header_dashboard()

    with c2:

        st.write(f"### Welcome, {teacher['name']}")

        if st.button("Logout"):

            del st.session_state["teacher_data"]

            st.session_state.teacher_login_type = "login"

            st.rerun()

    st.divider()

    t1, t2, t3 = st.columns(3)

    with t1:

        if st.button(
            "Take Attendance",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "take_attendance"
                else "secondary"
            ),
            use_container_width=True,
        ):

            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with t2:

        if st.button(
            "Manage Subjects",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "manage_subjects"
                else "secondary"
            ),
            use_container_width=True,
        ):

            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with t3:

        if st.button(
            "Attendance Records",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "attendance_records"
                else "secondary"
            ),
            use_container_width=True,
        ):

            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


# ===========================
# TABS
# ===========================

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("📸 Take AI Attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'show_add_photo' not in st.session_state:
        st.session_state.show_add_photo = False

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button("Add Photos"):
            st.session_state.show_add_photo = True

    if st.session_state.show_add_photo:
        add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    st.subheader("Added Photos")
    if st.session_state.attendance_images:
        cols = st.columns(4)
        for i, img in enumerate(st.session_state.attendance_images):
            with cols[i % 4]:
                st.image(img, width='stretch', use_container_width=True, caption=f'photo {i+1}')
    else:
        st.caption("No photos added yet")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Clear all photos", width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            all_detected_id = {}
            for i, img in enumerate(st.session_state.attendance_images):
                img_np = np.array(img.convert('RGB'))

                detected, _, _ = predict_attendance(img_np)

                if detected:
                    for sid in detected.keys():
                        student_id = int(sid)
                        all_detected_id.setdefault(student_id, []).append(f"photo {i+1}")

            enrolled_res = supabase.table('subject_students').select("*,students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled in this course')
            else:
                results, attendance_to_log = [], []
                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                for node in enrolled_students:
                    student = node['students']
                    sources = all_detected_id.get(int(student['student_id']), [])
                    is_present = len(sources) > 0

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Source": ", ".join(sources) if is_present else "-",
                        "Status": "Present" if is_present else "Absent"
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present)
                    })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        # Voice attendance disabled until dialog_voice_attendance is created/imported.
        # Once ready: remove disabled=True and uncomment the call below.
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            pass
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("📚 Manage Subjects", width='stretch')
    with col2:
        if st.button("Create New Subject", width='content'):
            create_subject_dialog(teacher_id)

    # List of subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['subject_code']}", key=f"share_{sub['subject_id']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                # NOTE: confirm your Supabase column name — likely 'section', not 'selection'
                section=sub['selection'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.warning("NO Subjects Found! Please create a new subject.", icon="⚠️")


def teacher_tab_attendance_records():

    st.header("📋 Attendance Records")

    st.info("Attendance records will appear here.")