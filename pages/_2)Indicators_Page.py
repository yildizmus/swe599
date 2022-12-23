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
    st.title("Indicators")

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

    data = yf.Ticker(symbol)
    global df
    df = data.history(period='1d', start=start, end=end)
    st.line_chart(df.Close)

    def SMA(data, period=30, column='Close'):
        return data[column].rolling(window=period).mean()

    def EMA(data, period=21, column='Close'):
        return data[column].ewm(span=period, adjust=False).mean()

    def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
        shortEMA=EMA(data, period_short, column=column)
        longEMA = EMA(data, period_long, column=column)
        data['MACD']=shortEMA-longEMA
        data["Signal_Line"]=EMA(data, period_signal, column='MACD')
        return data

    def RSI(data, period=14, column='Close'):
        delta=data[column].diff(1)
        delta=delta[1:]
        up=delta.copy()
        down=delta.copy()
        up[up<0]=0
        down[down>0]=0
        data['up']=up
        data['down']=down
        AVG_Gain=SMA(data, period, column='up')
        AVG_Loss = SMA(data, period, column='down')
        RS=AVG_Gain/AVG_Loss
        RSI=100.0-(100.0/(1.0+RS))
        data['RSI']=RSI
        return data

    st.sidebar.write('### Technical Indicators')
    indicators = st.sidebar.checkbox("Add Indicators")

    if indicators:
        sma=st.sidebar.checkbox('SMA')
        ema = st.sidebar.checkbox('EMA')
        macd = st.sidebar.checkbox('MACD')
        rsi = st.sidebar.checkbox('RSI')
        fig, ax = plt.subplots(figsize=(10, 5))
        ax2 = ax.twinx()
        df = df.reset_index()
        ax.plot(df["Date"], df['Close'], color='cyan', label='Close')

        if sma:
            sma = SMA(df)
            ax.plot(df["Date"], sma[:], color='lightblue', label='SMA', linewidth=1, linestyle='--')
        if ema:
            ema = EMA(df)
            ax.plot(df["Date"], ema[:], color='blue', label='EMA', linewidth=1, linestyle='--')
        if macd:
            macd = MACD(df)
            ax2.plot(df["Date"], macd["MACD"], color='green', label='MACD', linewidth=1, linestyle='--')
        if rsi:
            rsi=RSI(df)
            ax2.plot(df["Date"], rsi["RSI"], color='darkblue', label='RSI', linewidth=1, linestyle='--')


        ax.legend(loc='best')
        ax2.legend(loc='right')
        st.pyplot(fig)