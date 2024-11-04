import streamlit as st

st.title("5.How does Streamlit handle real-time data updates with st.button or st.checkbox? Explain a scenario where this can be useful.")

st.write('st.button or checkbox can be used --> to do a specific function only when they are pressed/checked -- here st.button is illustrated. when the button is pressed, checks for if condition and the corresponding messge is displayed else the other message')

st.button("To illustrate Button Function - Reset", type="primary")
if st.button("Say hello"):
    st.write("Hi Welcome")
else:
    st.write("Goodbye")
