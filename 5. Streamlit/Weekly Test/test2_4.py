import streamlit as st
import pandas as pd
import numpy as np

st.title("4.Create a Streamlit app that displays a line chart of random data. Allow the user to select the number of data points they want in the chart using a slider.")
x=st.slider('x')


data=pd.DataFrame(np.random.randn(x,3), columns=['2017','2018',"2019"])

st.line_chart(data)