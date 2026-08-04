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
from src.components.dialog_create_subject import create_subject_dialog


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

    c1, c2 = st.columns([3, 1])

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
    st.header("📸 Take AI Attendance")

def teacher_tab_manage_subjects():
    teacher_id  = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("📚 Manage Subjects",width='stretch')
    with col2:
        if st.button("Create New Subject",width='content'):
            create_subject_dialog(teacher_id)

    #List of subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes']),
            ]
        def share_btn():
            if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon="::material/share"):
                share_subject_dialog(sub['name'],sub['subject_code'])
            st.write()

        subject_card(
            name = sub['subject_name'],
            code = sub['subject_code'],
            section = sub['subject_section'],
            stats = stats,
            footer_callback = share_btn
        )
    else:
        st.warning("NO Subjects Found! Please create a new subject.",icon="⚠️")

def teacher_tab_attendance_records():

    st.header("📋 Attendance Records")

    st.info("Attendance records will appear here.")