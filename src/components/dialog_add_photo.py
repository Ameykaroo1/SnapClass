import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time
from PIL import Image

@st.dialog("Capture or upload photos")
def add_photos_dialog():
  st.write('Add classroom photos to scan for attendance')

  if 'photo_tab' not in st.session_state:
    st.session_state.photo_tab = 'camera'

  t1,t2 = st.columns(2)

  with t1:
    type_camera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
    if st.button("Camera",type=type_camera, width='stretch'):
      st.session_state.photo_tab='camera'

  with t2:
    type_upload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
    if st.button("Upload photos",type=type_upload, width='stretch'):
      st.session_state.photo_tab='upload'

  if st.session_state.photo_tab == 'camera':
    cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
    if cam_photo and cam_photo.file_id != st.session_state.get('last_cam_id'):
        st.session_state.attendance_images.append(Image.open(cam_photo))
        st.session_state.last_cam_id = cam_photo.file_id
        st.toast("Photo Captured")
        st.rerun()

  if st.session_state.photo_tab == 'upload':
    uploaded_files = st.file_uploader('Choose image files', type=['jpg','png','jpeg'], accept_multiple_files=True, key='dialog_upload')

    if uploaded_files:
        new_ids = [f.file_id for f in uploaded_files]
        if new_ids != st.session_state.get('last_upload_ids'):
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            st.session_state.last_upload_ids = new_ids
            st.toast('Photo Uploaded Successfully')
            st.rerun()

    if not uploaded_files:
        st.session_state.files_processed = False

  st.divider()
  if st.button('Done', type='primary', width='stretch'):
    st.session_state.show_add_photo = False
    st.rerun()