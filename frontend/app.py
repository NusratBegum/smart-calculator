import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(page_title="Smart Calculator", page_icon="🧮")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def safe_request(method, url, **kwargs):
    try:
        return requests.request(method, url, timeout=10, **kwargs)
    except requests.exceptions.RequestException:
        st.error("Could not reach the backend. Is it running?")
        return None


def show_auth():
    st.title("Smart Calculator")
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

        if submitted:
            resp = safe_request(
                "POST",
                f"{API_BASE_URL}/login",
                json={"username": username, "password": password},
            )
            if resp is not None:
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error(resp.json().get("detail", "Login failed"))

    with register_tab:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username", key="register_username")
            new_password = st.text_input("Choose a password", type="password", key="register_password")
            submitted = st.form_submit_button("Register")

        if submitted:
            resp = safe_request(
                "POST",
                f"{API_BASE_URL}/register",
                json={"username": new_username, "password": new_password},
            )
            if resp is not None:
                if resp.status_code == 201:
                    st.success("Account created. Switch to the Login tab to sign in.")
                else:
                    st.error(resp.json().get("detail", "Registration failed"))


def show_app():
    st.title("Smart Calculator")
    st.write(f"Logged in as **{st.session_state.username}**")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    st.header("Calculate")
    expression = st.text_input("Expression", placeholder="e.g. 5 + 10 * 2")
    if st.button("Calculate"):
        resp = safe_request(
            "POST",
            f"{API_BASE_URL}/calculate",
            json={"expression": expression},
            headers=headers,
        )
        if resp is not None:
            if resp.status_code == 200:
                st.success(f"Result: {resp.json()['result']}")
            else:
                st.error(resp.json().get("detail", "Calculation failed"))

    st.header("History")
    resp = safe_request("GET", f"{API_BASE_URL}/history", headers=headers)
    if resp is not None:
        if resp.status_code == 200:
            history = resp.json()
            if history:
                st.dataframe(
                    [
                        {
                            "expression": row["expression"],
                            "result": row["result"],
                            "created_at": row["created_at"],
                        }
                        for row in history
                    ]
                )
            else:
                st.write("No calculations yet.")
        else:
            st.error("Could not load history.")


if st.session_state.token is None:
    show_auth()
else:
    show_app()
