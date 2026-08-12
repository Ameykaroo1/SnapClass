import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image
import time
from src.database.db import create_attendance

@st.dialog("Capture or upload photos")
def attendance_result_dialog(df, logs):
  st.write('please review attendance before confirming')
  st.dataframe(df, hide_index=True, width='stretch')

  col1,col2 = st.columns(2)
  with col1:
    if st.button('Discard',width='stretch'):
      st.rerun()

  with col2:
    if st.button('Confirm & save', width='stretch',type='primary'):
      try:
        create_attendance(logs)
        st.toast('Attendance taken')
        st.session_state.attendance_images=[]
        st.rerun()
      except Exception as e:
         st.error('Sync failed')