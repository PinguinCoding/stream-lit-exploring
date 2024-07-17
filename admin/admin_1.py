import streamlit as st

st.header("Admin 1")
st.write("You are logged in as *{}*.".format(st.session_state.role))
