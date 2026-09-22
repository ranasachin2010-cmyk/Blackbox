import streamlit as st
import yfinance as yf

st.set_page_config(page_title="My Blackbox", page_icon="📦")
st.title("📦 My Blackbox - Swing Scanner")

stocks = st.multiselect("Stocks chuno", 
 ["DIVISLAB.NS","WELCORP.NS","NTPC.NS","ONGC.NS","VEDL.NS","HUDCO.NS","POWERGRID.NS"],
 default=["DIVISLAB.NS","WELCORP.NS"])

def get_close(df):
    # naya yfinance fix
    c = df['Close']
    if hasattr(c, 'iloc') and c.ndim > 1:
        c = c.iloc[:,0]
    return c

if st.button("Scan Now 🔍"):
 for s in stocks:
  df = yf.download(s, period="60d", interval="1d", progress=False, auto_adjust=False)
  close = get_close(df)
  
  e9 = close.ewm(span=9).mean()
  e26 = close.ewm(span=26).mean()
  macd = close.ewm(span=12).mean() - close.ewm(span=26).mean()
  sig = macd.ewm(span=9).mean()

  last_close = float(close.iloc[-1])
  last_e9 = float(e9.iloc[-1])
  last_e26 = float(e26.iloc[-1])
  last_macd = float(macd.iloc[-1])
  last_sig = float(sig.iloc[-1])

  if last_e9 > last_e26 and last_macd > last_sig:
   st.success(f"✅ BUY: {s} @ {last_close:.2f} | SL {last_close*0.98:.2f}")
  else:
   st.error(f"❌ NO TRADE: {s} @ {last_close:.2f}")

  chart_df = {"Close": close.tail(40), "E9": e9.tail(40), "E26": e26.tail(40)}
  st.line_chart(chart_df)
  st.divider()
