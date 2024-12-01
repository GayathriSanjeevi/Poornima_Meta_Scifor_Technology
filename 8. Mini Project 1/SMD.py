from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage import fundamentaldata
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import requests

st.title("Real Time Stock Market Dashboard")

API_key = "C76QOZK3UZH4IXSM"  # Replace with your own API key

company = st.sidebar.text_input("Enter the company/stock symbol:", "AAPL")
data_type = st.sidebar.selectbox("Which Data you want to see?", ("Daily", "Weekly", "Monthly"))
output = "compact"

st.sidebar.write("Selected Interval is", data_type)

# Function to fetch stock data
def fetch_data_download_report(API_key, company, output):
    try:
        ts = TimeSeries(key=API_key, output_format='pandas')
        
        with st.spinner("Fetching stock data..."):
            if data_type == "Daily":
                data, meta_data = ts.get_daily(symbol=company, outputsize=output)
            elif data_type == "Weekly":
                data, meta_data = ts.get_weekly(symbol=company)
            elif data_type == "Monthly":
                data, meta_data = ts.get_monthly(symbol=company)

        # Display metadata
        st.sidebar.write(meta_data)

        # Display stock data
        data = data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        st.dataframe(data)

        # Plotting the Close Price (Line Chart)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Close'], label='Close Price', color='blue')
        ax.set_title(f"{company} Stock Prices (Line Chart)")
        ax.set_xlabel("Time Period")
        ax.set_ylabel("Price (USD)")
        plt.xticks(rotation=45)
        ax.legend()
        linechart_path = f"{company}_linechart.png"
        plt.savefig(linechart_path)
        st.pyplot(fig)

        # Plotting Area Chart
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.fill_between(data.index, data["Close"], color="skyblue", alpha=0.4)
        ax1.set_title(f"{company} Stock Prices (Area Chart)")
        ax1.set_xlabel("Time Period")
        ax1.set_ylabel("Price (USD)")
        plt.xticks(rotation=45)
        areachart_path = f"{company}_areachart.png"
        plt.savefig(areachart_path)
        st.pyplot(fig1)

        # Button to export the report as a PDF
        export_as_pdf = st.button("Export Dashboard as PDF")

        # If export button is clicked, generate the PDF
        if export_as_pdf:
            generate_pdf(data, company, linechart_path, areachart_path)

    except Exception as e:
        st.error(f"Failed to fetch data. Please check the stock symbol or try again later. Error: {e}")

# Function to generate PDF report
def generate_pdf(data, company, linechart_path, areachart_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Stock Market Dashboard", ln=True, align='C')
    
    # Add company name and time period
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, "Company:", ln=False)
    pdf.cell(40, 10, company, ln=True)
    
    # Add the chart images to the PDF
    pdf.ln(10)
    pdf.image(linechart_path, x=10, y=None, w=100)  # Line chart
    pdf.ln(10)
    pdf.image(areachart_path, x=10, y=None, w=100)  # Area chart

    # Generate CSV download for data
    def convert_df(df):
        return df.to_csv().encode("utf-8")

    csv = convert_df(data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{company}_stock_data.csv",
        mime="text/csv",
    )

    # Create PDF download link
    pdf_output = pdf.output(dest="S").encode("latin1")
    b64_pdf = base64.b64encode(pdf_output).decode('latin1')
    st.markdown(f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{company}_stock_dashboard.pdf">Download PDF</a>', unsafe_allow_html=True)

# Function for moving average
def moving_average(API_key, company, data_type):
    try:
        tech_indicator = TechIndicators(key=API_key, output_format='pandas')
        ma_type = st.sidebar.selectbox("Choose Moving Average Type", ("SMA", "EMA"))
        tp = st.number_input("Enter the time period:", format='%d', min_value=1, value=50)

        with st.spinner("Fetching moving average data..."):
            if ma_type == "SMA":
                data_ma, _ = tech_indicator.get_sma(symbol=company, interval=data_type.lower(), time_period=tp, series_type='close')
            else:
                data_ma, _ = tech_indicator.get_ema(symbol=company, interval=data_type.lower(), time_period=tp, series_type='close')

        # Plot moving average
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data_ma.index, data_ma[ma_type], label=f'{ma_type} - {tp} Period', color='red')
        ax.set_title(f"{company} {ma_type} (Moving Average)")
        ax.set_xlabel("Time Period")
        ax.set_ylabel("Price (USD)")
        plt.xticks(rotation=45)
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Failed to fetch moving average data. Error: {e}")

def Comparative_analysis(key):
    st.title("Comparative Analysis of stocks")
    st.write("Enter the stocks to be compared")
    symbol1 =st.text_input("Enter the stock symbol1: ")  # e.g., IBM, AAPL, etc.
    symbol2 =st.text_input("Enter the stock symbol2: ")
    url1 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol1}&apikey={API_key}'
    url2 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol2}&apikey={API_key}'

    r1 = requests.get(url1)
    r2 = requests.get(url2)

    data1 = r1.json()
    data2= r2.json()

    df1=pd.DataFrame(data1.keys(),columns=['Metric'])
    
    df1['Stock 1']=data1.values()
    df1['Stock 2']=data2.values()

    st.table(df1)


# Sidebar to select the page
page_names_to_funcs = {
    "Fetch Data": fetch_data_download_report,
    "Moving Average of stocks": moving_average,
    "Comparison of stocks": Comparative_analysis
}

page_name = st.sidebar.selectbox("Choose a function", page_names_to_funcs.keys())

if page_name == 'Fetch Data':
    page_names_to_funcs[page_name](API_key, company, output)
elif page_name == "Moving Average of stocks":
    page_names_to_funcs[page_name](API_key, company, data_type)
elif page_name=="Comparison of stocks":
    page_names_to_funcs[page_name](API_key)
