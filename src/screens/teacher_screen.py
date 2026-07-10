import streamlit as st
import time
from src.ui.base_layout import style_backgroud_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login


def teacher_screen():

  style_backgroud_dashboard()
  style_base_layout()

  # If already authenticated, skip straight to the dashboard
  if st.session_state.get('teacher'):
    teacher_dashboard()
    return

  if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
    teacher_screen_login()
  elif st.session_state.teacher_login_type == 'register':
    teacher_screen_register()


def teacher_screen_login():
  c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with c1:
    header_dashboard()
  with c2:
    if st.button("Go back to Home", type='secondary', key='login_back_btn', shortcut="control+backspace"):
      st.session_state['login_type'] = None
      st.rerun()

  st.header("Login using password",text_alignment='center')
  st.write("")
  st.write("")
  teacher_username = st.text_input("Enter Username", placeholder='ananyaroy')

  teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter Password")
  st.divider()

  btnc1, btnc2 = st.columns(2)
  with btnc1:
    if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='login_submit_btn'):
      if not teacher_username or not teacher_pass:
        st.error("Please enter both username and password")
      else:
        teacher = teacher_login(teacher_username, teacher_pass)
        if teacher:
          st.session_state['teacher'] = teacher
          st.toast("Welcome back!", icon="🎉")
          time.sleep(1)
          st.rerun()
        else:
          st.error("Invalid username or password")

  with btnc2:
    if st.button('Register Instead', type='primary', icon=':material/passkey:', width='stretch', key='goto_register_btn'):
      st.session_state.teacher_login_type = 'register'
      st.rerun()

  footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
  if not teacher_username or not teacher_name or not teacher_pass:
    return False, "All fields are required!"
  if check_teacher_exists(teacher_username):
    return False, "Username already taken"
  if teacher_pass != teacher_pass_confirm:
    return False, "Passwords don't match"

  try:
    create_teacher(teacher_username, teacher_pass, teacher_name)
    return True, "Successfully created! Login now"
  except Exception:
    return False, "Unexpected error occurred. Please try again."


def teacher_screen_register():
  c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with c1:
    header_dashboard()
  with c2:
    if st.button("Go back to Home", type='secondary', key='register_back_btn', shortcut="control+backspace"):
      st.session_state['login_type'] = None
      st.rerun()

  st.header("Register your teacher profile")
  st.write("")
  st.write("")
  teacher_username = st.text_input("Enter Username", placeholder='ananyaroy')

  teacher_name = st.text_input("Enter name", placeholder='Ananya Roy')

  teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter Password")

  teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter Password", key='confirm_pass')

  st.divider()

  btnc1, btnc2 = st.columns(2)
  with btnc1:
    if st.button('Register Now', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='register_submit_btn'):
      success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
      if success:
        st.success(message)
        time.sleep(2)
        st.session_state.teacher_login_type = 'login'
        st.rerun()
      else:
        st.error(message)
  with btnc2:
    if st.button('Login Instead', type='primary', icon=':material/passkey:', width='stretch', key='goto_login_btn'):
      st.session_state.teacher_login_type = 'login'
      st.rerun()

  footer_dashboard()


def teacher_dashboard():
  c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
  with c1:
    header_dashboard()
  with c2:
    if st.button("Logout", type='secondary', key='teacher_logout_btn'):
      del st.session_state['teacher']
      st.session_state['login_type'] = None
      st.rerun()

  teacher = st.session_state['teacher']

  st.markdown(f"""
    <div style="margin: 2rem 0;">
      <h1 style="color:#5865F2; font-size: 2.5rem; margin-bottom: 0.2rem;">
        Welcome, {teacher.get('name', 'Teacher')}
      </h1>
      <p style="color:#666; font-size: 1.1rem;">
        @{teacher.get('username', '')}
      </p>
    </div>
  """, unsafe_allow_html=True)

  st.divider()
  st.write("Your teacher dashboard content goes here.")

  footer_dashboard()