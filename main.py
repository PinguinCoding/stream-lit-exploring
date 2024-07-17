import sqlite3
import threading
import streamlit as st

st.set_page_config(page_title="Streamlit Build Test")

ROLES = [None, "Requester", "Responder", "Admin"]

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "init"

db_lock = threading.Lock()


def create_db():
    with db_lock:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        secret_key TEXT NOT NULL,
        role TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()


create_db()

secret_key = st.secrets["database"]["secret_key"]


@st.cache_resource
def get_db_connection():
    with db_lock:
        conn = sqlite3.connect("users.db")
        return conn


@st.cache_data
def check_credentials(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    st.write("Teste")
    conn.close()
    return user


def add_user(username, password, user_role):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role, secret_key) VALUES (?, ?, ?, ?)",
                (username, password, user_role, secret_key))
    conn.commit()
    conn.close()


def login():
    st.header("Log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Enter"):
        user = check_credentials(username, password)
        if user:
            st.success("Login Successful!")
            st.write("Welcome back, {}!".format(username))
            st.session_state.role = user[-1]
            st.experimental_rerun()
        else:
            st.error("Username or password incorrect")


def register():
    st.header("Register new user")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    selected_role = st.selectbox("Choose your role", ROLES)

    if st.button("Register"):
        add_user(new_username, new_password, selected_role)
        st.success("User registered successfully!")
        st.session_state.page = "login"
        st.experimental_rerun()


def init():
    st.header("Welcome!")
    st.write("Do you want to login or register?")

    if st.button("Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

    if st.button("Register"):
        st.session_state.page = "register"
        st.experimental_rerun()


def logout():
    if st.button("Confirm exit"):
        st.session_state.role = None
        st.session_state.page = "init"
        st.experimental_rerun()


role = st.session_state.role
page = st.session_state.page

init_page = st.Page(init,
                    title="Enter page")

login_page = st.Page(login,
                     title="Login",
                     icon=":material/login:")

register_page = st.Page(register,
                        title="Register")

logout_page = st.Page(logout,
                      title="Log out",
                      icon=":material/logout:")

settings = st.Page("settings.py",
                   title="Settings",
                   icon=":material/settings:")

request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester")
)

request_2 = st.Page(
    "request/request_2.py",
    title="Request 2",
    icon=":material/bug_report:"
)

respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder")
)

respond_2 = st.Page(
    "respond/respond_2.py",
    title="Respond 2",
    icon=":material/handyman:"
)

admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin")
)

admin_2 = st.Page(
    "admin/admin_2.py",
    title="Admin 2",
    icon=":material/security:"
)

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Request manager")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

if role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if role == "Admin":
    page_dict["Admin"] = admin_pages

pg = None

if page == "init":
    pg = st.navigation([init_page])
elif page == "login":
    pg = st.navigation([login_page])
elif page == "register":
    pg = st.navigation([register_page])

pg.run()
