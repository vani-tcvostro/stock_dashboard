import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Stock Market Analytics Dashboard")

#Sidebar (User Inputs)
#user selects which stocks they want to study
#^NSEI is NIFTY 50 is used as overall market comparison
stocks=st.multiselect(
    "Select Stocks / Index",
    ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","^NSEI"],
    default=["RELIANCE.NS","TCS.NS","HDFCBANK.NS","^NSEI"]
)

#User selects the date range of analysis
#auto fills with a meaningful period
start_date=st.date_input("Start Date",pd.to_datetime("2020-01-01"))
end_date=st.date_input("End Date",pd.to_datetime("2024-12-31"))

#fetching data
#auto_adjust=True means prices are adjusted for splits and dividends automatically
#We only take 'Close' prices since they represent final market trading value of the day
data=yf.download(stocks,start=start_date,end=end_date,auto_adjust=True)['Close']

#displaying first few rows so user sees data is correctly loaded
st.subheader("First 5 Rows of Data")
st.write(data.head())

#PRICE TREND PLOT
#Shows how stock values moved over time. it helps identify growth, crashes, patterns
st.subheader("Price Trend Over Time")
fig1,ax1=plt.subplots()
for s in stocks:
    ax1.plot(data[s],label=s)   # Plot each selected stock/index
ax1.set_xlabel("Date")
ax1.set_ylabel("Price (INR)")
ax1.legend()
st.pyplot(fig1)

#DAILY RETURNS 
#Returns is % change day to day , helps measure gain and loss behavior
returns=data.pct_change()

# VOLATILITY ANALYSIS
#Volatility=rolling standard deviation , shows how risky the stock is
#Using 30 day window to smooth short term fluctuations
st.subheader("Rolling Volatility (30 Days)")
fig2,ax2=plt.subplots()
for s in stocks:
    ax2.plot(returns[s].rolling(30).std(),label=s)
ax2.set_xlabel("Date")
ax2.set_ylabel("Volatility (Std Dev)")
ax2.legend()
st.pyplot(fig2)

#CORRELATION HEATMAP 
#Shows how similarly stocks move relative to each other
#Helps understand diversification and portfolio risk
st.subheader(" Correlation Between Selected Stocks")
fig3,ax3=plt.subplots()
sns.heatmap(returns.corr(),annot=True,cmap="coolwarm",ax=ax3)
st.pyplot(fig3)


