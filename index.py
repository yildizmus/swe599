import pandas as pd
import yfinance as yf
import streamlit as st
from PIL import Image
import datetime
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt
import prophet
from prophet import Prophet
import seaborn as sns
import base64

import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# WİDE PAGE LAYOUT
st.set_page_config(layout="wide")


#USER AUTHENTICATION

names = ["root admin", "Mustafa Yıldız"]
usernames = ["radmin", "myildiz"]
file_path = Path(__file__).parent / "hashed_pw.pk1"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names,usernames,hashed_passwords, "index", "index")
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:


    #GENERAL TITLE
    st.title("Financial Price Prediction Platform")

    #DIVIDE LOGOS AND LINKS INTO COLUMNS
    c1, c2 = st.columns((3, 1))
    with c1:
        #LOGO1
        logo=Image.open("bist_logo.png")
        st.image(logo, width= 100)
        st.markdown('<a href= "https://borsaistanbul.com/en/sayfa/2726/equity-market-data-analytics"> BIST Data Analytics </a>',
                    unsafe_allow_html=True)
    with c2:
        #LOGO2
        logo=Image.open("yahoo_finance.jpeg")
        st.image(logo, width= 100)
        st.markdown('<a href= "https://finance.yahoo.com/"> Yahoo Finance </a>',
                    unsafe_allow_html=True)

    #SIDEBAR
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title("Filters")
    security=st.sidebar.radio("Select Security", ["Indicies", "Stocks"])

    st.sidebar.write('### Period Selection')
    sliderperiod=range(1,366)
    slider=st.sidebar.select_slider("Select Time Period", options=sliderperiod, value=30)

    today=datetime.today()
    period=timedelta(days=slider)

    start=st.sidebar.date_input("Start Date", value=today-period)
    end=st.sidebar.date_input("End Date", value=today)

    st.sidebar.write('### Select Data Set')
    price_volume = st.sidebar.radio("Select Data Set", ["Price", "Volume", "Both"])

    st.sidebar.write('### ML Prediction')
    prediction=st.sidebar.checkbox("Add Prediction")
    if prediction:
        predictionperiod = range(1, 366)
        prediction_period = st.sidebar.select_slider("Select Prediction Period", options=predictionperiod, value=30)

    #DIVIDE GRAPHS AND PRICE TABLE INTO COLUMNS
    c3, c4 = st.columns((3, 1))
    with c3:
        st.header("Security Chart")
        st.markdown("<h5>This chart displays the securities traded at BIST</h5>", unsafe_allow_html=True)

        #Charts
        if security=="Indicies":
            indicies=["XU030.IS", "XU100.IS", "XBANK.IS","XUSIN.IS"]
            selectindex=st.sidebar.selectbox("Index Name", indicies)
            symbol=selectindex
            st.sidebar.write('### Select Securities')
            price_table = st.sidebar.multiselect("Select Securities", indicies, default=["XU030.IS", "XU100.IS", "XBANK.IS","XUSIN.IS"])
        else:
            stocks=["AKBNK.IS","AKSEN.IS","ARCLK.IS","ASELS.IS","BIMAS.IS","EKGYO.IS","EREGL.IS","FROTO.IS","GARAN.IS","GUBRF.IS","HEKTS.IS","ISCTR.IS","KCHOL.IS","KOZAA.IS","KOZAL.IS","KRDMD.IS","PETKM.IS","PGSUS.IS","SAHOL.IS","SASA.IS","SISE.IS","TAVHL.IS","TCELL.IS","THYAO.IS","TKFEN.IS","TOASO.IS","TTKOM.IS","TUPRS.IS","VESTL.IS","YKBNK.IS"]
            selectstock = st.sidebar.selectbox("Stocks Name", stocks)
            symbol=selectstock
            st.sidebar.write('### Select Securities')
            price_table = st.sidebar.multiselect("Select Securities", stocks, default=["AKBNK.IS","AKSEN.IS","ARCLK.IS","ASELS.IS","BIMAS.IS","EKGYO.IS","EREGL.IS","FROTO.IS","GARAN.IS"])

        def graph(symbol, start, end):
            if price_volume=="Price":
                data = yf.Ticker(symbol)
                global df
                df = data.history(period='1d', start=start, end=end)
                st.line_chart(df.Close)
                if prediction:
                    df = df.reset_index()
                    df=df[['Date', 'Close']]
                    df.columns = ['ds', 'y']
                    model = Prophet()
                    model.fit(df)
                    future = model.make_future_dataframe(periods=prediction_period)
                    predict = model.predict(future)
                    st.pyplot(model.plot(predict))
                else:
                    pass

            elif price_volume=="Volume":
                data = yf.Ticker(symbol)
                df = data.history(period='1d', start=start, end=end)
                st.bar_chart(df.Volume)
                if prediction:
                    df = df.reset_index()
                    df=df[['Date', 'Volume']]
                    df.columns = ['ds', 'y']
                    model = Prophet()
                    model.fit(df)
                    future = model.make_future_dataframe(periods=prediction_period)
                    predict = model.predict(future)
                    st.pyplot(model.plot(predict))
                else:
                    pass
            elif price_volume == "Both":
                data = yf.Ticker(symbol)
                df = data.history(period='1d', start=start, end=end)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax2 = ax.twinx()
                ax.bar(df.index.date, df['Volume']/1000, color='grey', label='Volume (K)')
                ax2.plot(df.index.date, df['Close'], color='cyan', label='Price')
                ax.set_xticklabels(df.index.date)
                ax.legend(loc='best')
                ax2.legend(loc='best')
                st.pyplot(fig)

        graph(symbol, start, end)

    with c4:
        st.header("Price Table")
        st.write("<h5>This table displays the selected end date closing values of the securities</h5>", unsafe_allow_html=True)
        closes=yf.Tickers(price_table).history(period='1d', start=start, end=end)
        st.dataframe(closes['Close'].iloc[-1], use_container_width=1)

    #PREDICTION USING ML ALGORITHMS

    def download_csv(df):
        csv=df.to_csv()
        b64=base64.b64encode(csv.encode()).decode()
        href=f'<a href="data:file/csv;base64,{b64}">download CSV</a>'
        return href

    st.markdown(download_csv(df), unsafe_allow_html=True)







