import streamlit as st

st.header("Respond 2")
st.write("You are logged in as *{}*.".format(st.session_state.role))
