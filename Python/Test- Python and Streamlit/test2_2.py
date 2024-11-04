import streamlit as st
st.title('2.Write a simple Streamlit app that takes a user’s name as input and displays a personalized greeting message.')

user=st.text_input("Enter the user name")

st.write("Hi", user,"Welcome to Streamlit app")