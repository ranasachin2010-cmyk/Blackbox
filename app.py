import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="My Blackbox NIFTY500", page_icon="📦", layout="wide")

# --- PASSWORD LOCK ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.title("📦 Blackbox PRO - Locked")
    pwd = st.text_input("Password", type="password")
    if st.button("Unlock"):
        if pwd == "rana123":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Galat password")
    st.stop()

@st.cache_data(ttl=86400)
def get_nifty500():
    try:
        df = pd.read_html("https://en.wikipedia.org/wiki/NIFTY_500")[2]
        symbols = df['Symbol'].tolist()
        return [s.strip()+".NS" for s in symbols]
    except:
        return [
            "RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","BHARTIARTL.NS","SBIN.NS","BAJFINANCE.NS","LT.NS",
            "SUNPHARMA.NS","TITAN.NS","ITC.NS","ONGC.NS","NTPC.NS","AXISBANK.NS","HCLTECH.NS","MARUTI.NS","WIPRO.NS","POWERGRID.NS",
            "DIVISLAB.NS","WELCORP.NS","HUDCO.NS","IRFC.NS","BEL.NS","SUZLON.NS","BHEL.NS","VEDL.NS","TATAMOTORS.NS","ZOMATO.NS",
            "HAL.NS","RVNL.NS","PFC.NS","RECLTD.NS","TATAPOWER.NS","DLF.NS","INDIGO.NS","BANKBARODA.NS","PNB.NS","IDFCFIRSTB.NS"
        ]

if "all_stocks" not in st.session_state:
    st.session_state.all_stocks = get_nifty500()

st.title("📦 Blackbox PRO - Only BUY Scanner")
st.success(f"✅ NIFTY 500 Loaded: {len(st.session_state.all_stocks)} Stocks")

c1,c2 = st.columns([3,1])
with c1:
    new_stock = st.text_input("Naya stock", placeholder="SUZLON.NS", label_visibility="collapsed").upper().strip()
with c2:
    if st.button("Add Stock"):
        if new_stock:
            if not new_stock.endswith(".NS"): new_stock += ".NS"
            if new_stock not in st.session_state.all_stocks:
                st.session_state.all_stocks.insert(0, new_stock)
                st.toast(f"{new_stock} added!")

def get_close(df):
    c = df['Close']
    if isinstance(c, pd.DataFrame): c = c.iloc[:,0]
    return c

search = st.text_input("🔍 Search", placeholder="TATA, BANK, SUZLON")
filtered = st.session_state.all_stocks
if search:
    filtered = [s for s in st.session_state.all_stocks if search in s]

stocks = st.multiselect(f"Chuno ({len(filtered)} stocks)", filtered, default=filtered[:10])

if st.button(f"Scan {len(stocks)} Stocks 🔍", type="primary"):
    buy_count = 0
    buy_list = []
    prog = st.progress(0)
    status = st.empty()

    for i,s in enumerate(stocks):
        status.text(f"Scanning {s}... {i+1}/{len(stocks)}")
        try:
            df = yf.download(s, period="60d", interval="1d", progress=False, auto_adjust=True)
            if len(df) < 30:
                prog.progress((i+1)/len(stocks))
                continue
            close = get_close(df)
            e9 = close.ewm(span=9).mean()
            e26 = close.ewm(span=26).mean()
            macd = close.ewm(span=12).mean() - close.ewm(span=26).mean()
            sig = macd.ewm(span=9).mean()
            lc = float(close.iloc[-1]); le9 = float(e9.iloc[-1]); le26 = float(e26.iloc[-1]); lm = float(macd.iloc[-1]); ls = float(sig.iloc[-1])

            # SIRF BUY CONDITION
            if le9 > le26 and lm > ls:
                buy_count += 1
                buy_list.append(s)
                sl = lc*0.98; tgt = lc*1.04
                st.success(f"✅ BUY: {s} @ {lc:.2f} | SL: {sl:.2f} | Target: {tgt:.2f}")
                chart_df = pd.DataFrame({"Close":close.tail(40),"E9":e9.tail(40),"E26":e26.tail(40)})
                st.line_chart(chart_df)
                st.divider()
        except:
            pass
        prog.progress((i+1)/len(stocks))

    status.empty()
    prog.empty()

    if buy_count > 0:
        st.balloons()
        st.success(f"🎯 Total {buy_count} BUY Signals: {', '.join(buy_list)}")
    else:
        st.warning("😔 Aaj koi BUY nahi hai is list me - Market weak hai")
