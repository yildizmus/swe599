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
    st.title("Cross Validation")

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

    st.sidebar.write('### Cross Validation')
    crossValidation = st.sidebar.checkbox("Cross Validation")


    data = yf.Ticker(symbol)
    global df
    df = data.history(period='1d', start=start, end=end)
    st.line_chart(df.Close)
    df = df.reset_index()
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']
    global model
    model = Prophet()
    model.fit(df)


    def cv_graph(model, initial, period, horizon, metric):
        initial=str(initial)+" days"
        period = str(period) + " days"
        horizon = str(horizon) + " days"
        cv = cross_validation(model, initial=initial, period=period, horizon=horizon)
        crossvalidation_graph= plot_cross_validation_metric(cv, metric=metric)
        st.write(crossvalidation_graph)

    if crossValidation:
        st.sidebar.write("Select a parameters")
        initial_range = range(1, 1441)
        initial_period = st.sidebar.select_slider("Initial Period", options=initial_range, value=120)
        cv_range = range(1, 1441)
        cv_period = st.sidebar.select_slider("CV period", options=cv_range, value=30)
        hor_range = range(1, 1441)
        hor_period = st.sidebar.select_slider("Horizon period", options=hor_range, value=60)
        st.sidebar.write("Select a cross validation metric")
        metrics=st.sidebar.radio("Metric", ["rmse", "mse", "mape", "mdape"])
        cv_graph(model, initial_period, cv_period, hor_period, metrics)

    else:
        pass




















