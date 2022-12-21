import pandas as pd
import yfinance as yf
import streamlit as st
from PIL import Image
import datetime
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt
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
    st.sidebar.write('### Data Set')
    price_volume = st.sidebar.radio("Select Price-Volume-Both",["Price", "Volume", "Both"])

    st.sidebar.write('### Period')
    sliderperiod=range(1,366)
    slider=st.sidebar.select_slider("Filter Time Period", options=sliderperiod, value=180)

    today=datetime.today()
    period=timedelta(days=slider)

    start=st.sidebar.date_input("Start Date", value=today-period)
    end=st.sidebar.date_input("End Date", value=today)

    st.sidebar.write('### Securities for Chart')
    security = st.sidebar.radio("Filter Security Group for Chart", ["Indicies", "Stocks"])

    #DIVIDE GRAPHS AND PRICE TABLE INTO COLUMNS
    c3, c4 = st.columns((3, 1))
    with c3:
        st.header("Security Chart")
        st.markdown("<h5>This chart displays the securities traded at BIST</h5>", unsafe_allow_html=True)

        #Charts
        if security=="Indicies":
            indicies=["XU030.IS", "XU100.IS", "XBANK.IS","XUSIN.IS"]
            selectindex=st.sidebar.selectbox("Filter Index", indicies)
            symbol=selectindex
            st.sidebar.write('### Securities for Table')
            price_table = st.sidebar.multiselect("Select Indicies for Table", indicies, default=["XU030.IS", "XU100.IS", "XBANK.IS","XUSIN.IS"])
        else:
            stocks=["AKBNK.IS","AKSEN.IS","ARCLK.IS","ASELS.IS","BIMAS.IS","EKGYO.IS","EREGL.IS","FROTO.IS","GARAN.IS","GUBRF.IS","HEKTS.IS","ISCTR.IS","KCHOL.IS","KOZAA.IS","KOZAL.IS","KRDMD.IS","PETKM.IS","PGSUS.IS","SAHOL.IS","SASA.IS","SISE.IS","TAVHL.IS","TCELL.IS","THYAO.IS","TKFEN.IS","TOASO.IS","TTKOM.IS","TUPRS.IS","VESTL.IS","YKBNK.IS"]
            selectstock = st.sidebar.selectbox("Filter Stock", stocks)
            symbol=selectstock
            st.sidebar.write('### Securities for Table')
            price_table = st.sidebar.multiselect("Select Stocks for Table", stocks, default=["AKBNK.IS","AKSEN.IS","ARCLK.IS","ASELS.IS","BIMAS.IS","EKGYO.IS","EREGL.IS","FROTO.IS","GARAN.IS"])

        st.sidebar.write('### ML Prediction')
        prediction = st.sidebar.checkbox("Add Prediction")
        if prediction:
            predictionperiod = range(1, 366)
            prediction_period = st.sidebar.select_slider("Filter Prediction Period", options=predictionperiod, value=30)
            components = st.sidebar.checkbox("Display Prediction Components")
            crossValidation = st.sidebar.checkbox("Cross Validation")
        def graph(symbol, start, end):
            if price_volume=="Price":
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
                    # CROSS VALIDATION
                    if crossValidation:
                        st.sidebar.write("Select a cross validation metric")
                        metrics=st.sidebar.radio("Metric", ["rmse", "mse", "mape", "mdape"])

                        st.sidebar.write("Select a parameters")
                        initial_range=range(1, 1441)
                        initial_period=st.sidebar.select_slider("Initial Period", options=initial_range, value=120)
                        cv_range=range(1, 1441)
                        cv_period=st.sidebar.select_slider("CV period", options=cv_range, value=30)
                        hor_range = range(1, 1441)
                        hor_period = st.sidebar.select_slider("Horizon period", options=hor_range, value=60)
                        def cv_graph(model, initial, period, horizon, metric):
                            initial=str(initial)+" days"
                            period = str(period) + " days"
                            horizon = str(horizon) + " days"
                            cv = cross_validation(model, initial=initial, period=period, horizon=horizon)
                            crossvalidation_graph= plot_cross_validation_metric(cv, metric=metric)
                            st.write(crossvalidation_graph)

                        cv_graph(model, initial_period, cv_period, hor_period, metrics )


                        #df_pm=performance_metrics(cv)

                else:
                    pass

            elif price_volume=="Volume":
                data = yf.Ticker(symbol)
                df = data.history(period='1d', start=start, end=end)
                st.bar_chart(df.Volume)
                # PREDICTION USING ML ALGORITHMS
                if prediction:
                    df = df.reset_index()
                    df=df[['Date', 'Volume']]
                    df.columns = ['ds', 'y']
                    model = Prophet()
                    model.fit(df)
                    future = model.make_future_dataframe(periods=prediction_period)
                    predict = model.predict(future)
                    st.pyplot(model.plot_components(predict))
                    st.pyplot(model.plot(predict))
                    if components:
                        st.pyplot(model.plot_components(predict))
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
        global df1
        df1=closes['Close'].iloc[-1]
        st.dataframe(closes['Close'].iloc[-1], use_container_width=1)

    # DOWNLOADING THE CONTENTS OF THE CHART AND TABLE
    c5, c6 = st.columns((3, 1))
    with c5:
        def download_csv(df):
            csv=df.to_csv()
            b64=base64.b64encode(csv.encode()).decode()
            href=f'<a href="data:file/csv;base64,{b64}">Download Chart into CSV</a>'
            return href

        st.markdown(download_csv(df), unsafe_allow_html=True)

    with c6:
        def download_csv1(df1):
            csv1 = df1.to_csv()
            datatable = base64.b64encode(csv1.encode()).decode()
            href1 = f'<a href="data:file/csv;base64,{datatable}">Download Table into CSV</a>'
            return href1

        st.markdown(download_csv1(df1), unsafe_allow_html=True)

    # SETTING TECHNICAL INDICATORS
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

        #if sma:
            #sma=SMA(df)
            #sma = sma.reset_index()
            #sma = sma.rename(columns={'Close': 'SMA'})

            #st.line_chart(sma, x='Date', y=['SMA'])
            #sma = SMA(df)
            #st.line_chart(sma[:])
            #ema = EMA(df) #Burada ayrıca fonksiyonlardaki return data değerini pd.Dataframe ile dönüştümek gerekiyor.
            #sma["EMA"]=ema['Close']
            #sma=sma.reset_index()
            #st.line_chart(sma, x='Date', y=['Close', 'EMA'])
            #print(sma.head)
        #if ema:
            #ema=EMA(df)
            #ema = ema.reset_index()
            #ema = ema.rename(columns={'Close': 'EMA'})
            #st.line_chart(ema, x='Date', y=["EMA"])
        #if macd:
            #macd = MACD(df)
            #fig, ax = plt.subplots(figsize=(10, 5))
            #ax2 = ax.twinx()
            #ax.plot(macd.index.date, macd['Close'], color='orange', label='Close')
            #ax2.plot(macd.index.date, macd['MACD'], color='cyan', label='MACD')
            #ax.set_xticklabels(macd.index.date)
            #ax.legend(loc='best')
            #ax2.legend(loc='right')
            #st.pyplot(fig)
        #if rsi:
            #rsi=RSI(df)
            #macd = MACD(df)
            #fig, ax = plt.subplots(figsize=(10, 5))
            #ax2 = ax.twinx()
            #ax2.plot(macd.index.date, macd['Close'], color='cyan', label='Close')

            #ax.plot(macd.index.date, macd['MACD'], color='red', label='MACD')
            #ax.set_ylabel("RSI-MACD")
            #ax.set_xlabel("Date")
            #ax.set_title("RSI-MACD")
            #ax.legend(loc='best')
            #ax2.legend(loc='best')
            #plt.grid(axis='y')
            #st.pyplot(fig)



            #st.line_chart(rsi, x='Date', y=["RSI"])



















