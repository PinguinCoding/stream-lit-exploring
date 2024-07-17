import streamlit as st
import sqlite3


# Função para criar a conexão e tabela no banco de dados
def create_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# Função para registrar um novo usuário
def register_user(username, password, selected_role):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, selected_role))
    conn.commit()
    conn.close()


# Função para verificar as credenciais do usuário
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user_role = c.fetchone()
    conn.close()
    if user_role:
        return user_role[0]
    return None


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Responder", "Admin"]

create_connection()


# Página de registro
def register():
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    selected_role = st.selectbox("Role", ROLES[1:])

    if st.button("Register"):
        if username and password and selected_role:
            try:
                register_user(username, password, selected_role)
                st.success("User registered successfully!")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose another one.")
        else:
            st.error("Please fill out all fields.")


# Página de login
def login():
    st.header("Log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        user_role = verify_user(username, password)
        if user_role:
            st.session_state.role = user_role
            st.success(f"Logged in as {user_role}")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")


# Página de logout
def logout():
    st.session_state.role = None
    st.experimental_rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out",
                      icon=":material/logout:")

settings = st.Page("settings.py",
                   title="Settings",
                   icon=":material/settings:")

request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)

request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)

respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)

respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)

admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)

admin_2 = st.Page("admin/admin_2.py",
                  title="Admin 2",
                  icon=":material/security:")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Request manager")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login), st.Page(register)])

pg.run()
