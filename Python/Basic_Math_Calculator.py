import streamlit as st

st.title("Basic Math Operations")

x=int(st.text_input("Enter the first number:"))
y=int(st.text_input("Enter the second number:"))

st.write("x is", x)
st.write("y is", y)

option=st.selectbox("Enter the operation need to be done 1. Addition, 2. Subtraction, 3. Multiplication,  Division",
                    ("1", "2", "3", "4"))

if option=="1":
    st.write("Result is", x+y)
elif option=="2":
    st.write("Result is", x-y)
elif option=="3":
    st.write("Result is", x*y)
elif option=="4":
    st.write("Result is", x/y)