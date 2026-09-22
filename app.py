import streamlit as st
import yfinance as yf

st.set_page_config(page_title="My Blackbox", page_icon="📦")
st.title("📦 My Blackbox - Swing Scanner")

stocks = st.multiselect("Stocks chuno", 
 ["DIVISLAB.NS","WELCORP.NS","NTPC.NS","ONGC.NS","VEDL.NS","HUDCO.NS","POWERGRID.NS"],
 default=["DIVISLAB.NS","WELCORP.NS"])

if st.button("Scan Now 🔍"):
 for s in stocks:
  try:
   df = yf.download(s, period="60d", interval="1d", progress=False)
   if len(df) < 30:
    st.warning(f"{s} me data kam hai")
    continue
   
   df['E9'] = df['Close'].ewm(span=9).mean()
   df['E26'] = df['Close'].ewm(span=26).mean()
   df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
   df['SIG'] = df['MACD'].ewm(span=9).mean()
   df = df.dropna()
   
   last = df.iloc[-1]
   buy = float(last['E9']) > float(last['E26']) and float(last['MACD']) > float(last['SIG'])

   if buy:
    st.success(f"✅ BUY: {s} @ {float(last['Close']):.2f} | SL {float(last['Close'])*0.98:.2f}")
   else:
    st.error(f"❌ NO TRADE: {s} @ {float(last['Close']):.2f}")
   
   st.line_chart(df[['Close','E9','E26']].tail(40))
   st.divider()
  except Exception as e:
   st.error(f"{s} error: {e}")
