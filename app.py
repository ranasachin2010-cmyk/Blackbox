import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Blackbox", page_icon="📦", layout="centered")

# --- 1. PASSWORD LOCK (Blackbox ka logic chhupane ke liye) ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("📦 My Blackbox - Locked")
    pwd = st.text_input("Password daalo", type="password")
    if st.button("Unlock"):
        if pwd == "rana123": # <-- apna password yaha change karo
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Galat password")
    st.stop()

# --- 2. MAIN APP ---
st.title("📦 My Blackbox - Swing Scanner")
st.caption("Logic Hidden | Signal Only")

stocks = st.multiselect("Stocks chuno", 
 ["DIVISLAB.NS","WELCORP.NS","HUDCO.NS","NTPC.NS","ONGC.NS","VEDL.NS","POWERGRID.NS","RELIANCE.NS","TCS.NS"],
 default=["HUDCO.NS","DIVISLAB.NS","WELCORP.NS"])

def get_close(df):
    c = df['Close']
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:,0]
    return c

if st.button("Scan Now 🔍"):
    for s in stocks:
        df = yf.download(s, period="60d", interval="1d", progress=False, auto_adjust=True)
        if len(df) < 30:
            st.warning(f"{s} me data kam hai")
            continue
        
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

        buy_cond = last_e9 > last_e26 and last_macd > last_sig

        if buy_cond:
            sl = last_close * 0.98
            target = last_close * 1.04
            st.success(f"✅ BUY: {s} @ {last_close:.2f}\n\nSL: {sl:.2f} | Target: {target:.2f}")
        else:
            st.error(f"❌ NO TRADE: {s} @ {last_close:.2f}")

        chart_df = pd.DataFrame({
            "Close": close.tail(40),
            "E9": e9.tail(40),
            "E26": e26.tail(40)
        })
        st.line_chart(chart_df)
        st.divider()
    st.balloons()
