import pandas as pd
import yfinance as yf
import streamlit as st
from PIL import Image
import datetime
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt
import matplotlib
import prophet
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
import seaborn as sns
import base64
import altair
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

from Home_Page import authentication_status

# WİDE PAGE LAYOUT
st.set_page_config(layout="wide")

#USER AUTHENTICATION
names = ["root admin", "Mustafa Yıldız"]
usernames = ["radmin", "myildiz"]
file_path = Path(__file__).parent.parent /  "hashed_pw.pk1"
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
    st.title("ML Prediction")

    #SIDEBAR
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title("Filters for Stocks")

    today=datetime.today()
    period=timedelta(days=365)
    start=st.sidebar.date_input("Start Date", value=today-period)
    end=st.sidebar.date_input("End Date", value=today)

    stocks=["AKBNK.IS","AKSEN.IS","ARCLK.IS","ASELS.IS","BIMAS.IS","EKGYO.IS","EREGL.IS","FROTO.IS","GARAN.IS","GUBRF.IS","HEKTS.IS","ISCTR.IS","KCHOL.IS","KOZAA.IS","KOZAL.IS","KRDMD.IS","PETKM.IS","PGSUS.IS","SAHOL.IS","SASA.IS","SISE.IS","TAVHL.IS","TCELL.IS","THYAO.IS","TKFEN.IS","TOASO.IS","TTKOM.IS","TUPRS.IS","VESTL.IS","YKBNK.IS"]
    selectstock = st.sidebar.selectbox("Filter Stock", stocks)
    symbol=selectstock

    st.sidebar.write('### ML Prediction')
    prediction = st.sidebar.checkbox("Add Prediction")
    if prediction:
        predictionperiod = range(1, 366)
        prediction_period = st.sidebar.select_slider("Filter Prediction Period", options=predictionperiod, value=30)
        components = st.sidebar.checkbox("Display Prediction Components")

    def graph(symbol, start, end):
        data = yf.Ticker(symbol)
        global df
        df = data.history(period='1d', start=start, end=end)
        st.line_chart(df.Close)
        # PREDICTION USING ML ALGORITHMS
        if prediction:
            df = df.reset_index()
            df=df[['Date', 'Close']]
            df.columns = ['ds', 'y']
            global model
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=prediction_period)
            predict = model.predict(future)
            st.pyplot(model.plot(predict))
            if components:
                st.pyplot(model.plot_components(predict))

    graph(symbol, start, end)

















