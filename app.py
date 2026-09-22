import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Blackbox", page_icon="📦")
st.title("📦 My Blackbox - Swing Scanner")
st.caption("Logic hidden | Signal only")

stocks = st.multiselect("Stocks chuno", 
 ["DIVISLAB.NS","WELCORP.NS","NTPC.NS","ONGC.NS","VEDL.NS","HUDCO.NS","POWERGRID.NS"],
 default=["DIVISLAB.NS","WELCORP.NS"])

if st.button("Scan Now 🔍"):
 for s in stocks:
  df = yf.download(s, period="30d", interval="1d", progress=False)
  df['E9'] = df['Close'].ewm(9).mean()
  df['E26'] = df['Close'].ewm(26).mean()
  df['MACD'] = df['Close'].ewm(12).mean() - df['Close'].ewm(26).mean()
  df['SIG'] = df['MACD'].ewm(9).mean()
  
  last = df.iloc[-1]
  buy = last['E9'] > last['E26'] and last['MACD'] > last['SIG']
  
  col1, col2 = st.columns(2)
  with col1:
   st.write(f"**{s}** - {round(last['Close'],2)}")
  with col2:
   if buy:
    st.success("✅ BUY SIGNAL")
   else:
    st.error("❌ NO TRADE")
  st.line_chart(df[['Close','E9','E26']].tail(30))
  st.divider()

st.info("Ye Blackbox hai - andar ka formula user ko nahi dikhega, sirf signal dikhega.")
