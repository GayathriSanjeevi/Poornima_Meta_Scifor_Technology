from alpha_vantage.timeseries import TimeSeries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.title("Real Time Stock Market Dashboard")

API_key="JJ9RDA2FQ9V4HJ54"

company=st.sidebar.text_input("Enter the company/stock name:")
type=st.sidebar.selectbox("Which Data you want to see?",
                          ("Daily", "Weekly", "Monthly"),placeholder="Select any one time period")
output="compact"

st.sidebar.write("Selected Interval is ", type)

def fetch_data_download_report(API_key,company,output):

    ts=TimeSeries(key=API_key,output_format='pandas') #output in pandas dataframe format

    if type=="Daily":
        data,meta_data=ts.get_daily(symbol=company, outputsize=output)
    elif type=="Weekly":
        data, meta_data=ts.get_weekly(symbol=company)
    elif type=="Monthly":
        data,meta_data=ts.get_monthly(symbol=company)

    st.sidebar.write(meta_data)

    st.dataframe(data)

    data = data.rename(columns={
        '1. open': 'Open', 
        '2. high': 'High', 
        '3. low': 'Low', 
        '4. close': 'Close', 
        '5. volume': 'Volume'
    })

    #Line chart showing stock prices

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label='Close Price')
    ax.set_title(f"{company} Stock Prices")
    ax.set_xlabel("Time Period")
    ax.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    #Area Chart
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.fill_between(data.index, data["Close"], color="skyblue", alpha=0.4)
    ax1.set_title(f"{company} Stock Prices (Area Chart)")
    ax1.set_xlabel("Time Period")
    ax1.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

def moving_average(API_key,company,type):
    from alpha_vantage.techindicators import TechIndicators

    tech_indicator=TechIndicators(key=API_key,output_format='pandas')

    tp=st.number_input("Enter the time period: ", format='%d', min_value=0)
    
    data_sma, meta_data_sma=tech_indicator.get_sma(company,interval=type.lower(), time_period=tp, series_type='close')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data_sma.index, data_sma['SMA'], label='Close Price')
    ax.set_title(f"{company} Stock Prices Simple Moving Average")
    ax.set_xlabel("Time Period")
    ax.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

def Comparative_analysis():
    st.write("Comparative Analysis Page")

def interactive_filtering():
    st.write("Filtering of Stocks Page")

page_names_to_funcs = {
  "Fetch Data": fetch_data_download_report,
  "Moving Average of stocks": moving_average,
  #"Comparison of stocks": Comparative_analysis,
   # "Filtering of stocks": interactive_filtering
}

page_name = st.sidebar.selectbox("Choose a function", page_names_to_funcs.keys())
if page_name=='Fetch Data':
    page_names_to_funcs[page_name](API_key, company, output)

elif page_name=="Moving Average of stocks":
    page_names_to_funcs[page_name](API_key, company, type)

