import streamlit as st

st.header("Settings")
st.write("You are logged in as *{}*.".format(st.session_state.role))
