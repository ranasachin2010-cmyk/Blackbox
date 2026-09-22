import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Blackbox PRO - Only BUY", page_icon="📦", layout="wide")

# --- 1. PASSWORD LOCK ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if not st.session_state.auth:
    st.title("📦 Blackbox PRO - Locked")
    pwd = st.text_input("Password daalo", type="password")
    if st.button("Unlock"):
        if pwd == "rana123": # apna password
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Galat password")
    st.stop()

# --- 2. NIFTY 500 FULL LIST ---
@st.cache_data
def get_nifty500():
    # Ye Nifty 500 ki full list hai (Wikipedia se li hui)
    return [
        "360ONE.NS","3MINDIA.NS","ABB.NS","ACC.NS","AIAENG.NS","APLAPOLLO.NS","AUBANK.NS","AARTIIND.NS","AAVAS.NS","ABBOTINDIA.NS",
        "ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS","ATGL.NS","AWL.NS","ABCAPITAL.NS","ABFRL.NS","AEGISLOG.NS","AETHER.NS",
        "AFFLE.NS","AJANTPHARM.NS","APLLTD.NS","ALKEM.NS","ALKYLAMINE.NS","ALOKINDS.NS","ARE&M.NS","AMBER.NS","AMBUJACEM.NS","ANANDRATHI.NS",
        "ANGELONE.NS","APARINDS.NS","APOLLOTYRE.NS","APOLLOHOSP.NS","ASAHIINDIA.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTERDM.NS","ASTRAL.NS",
        "ATUL.NS","AUROPHARMA.NS","DMART.NS","AXISBANK.NS","BSE.NS","BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BAJAJHLDNG.NS","BALAMINES.NS",
        "BALKRISIND.NS","BANDHANBNK.NS","BANKBARODA.NS","BANKINDIA.NS","BATAINDIA.NS","BAYERCROP.NS","BERGEPAINT.NS","BDL.NS","BEL.NS","BHARATFORG.NS",
        "BHEL.NS","BPCL.NS","BHARTIARTL.NS","BIKAJI.NS","BIOCON.NS","BIRLACORPN.NS","BSOFT.NS","BLUEDART.NS","BLUESTARCO.NS","BBTC.NS",
        "BOSCHLTD.NS","BRITANNIA.NS","CESC.NS","CAMSLTD.NS","CANBK.NS","CAPLIPOINT.NS","CGCL.NS","CARBORUNIV.NS","CASTROLIND.NS","CEATLTD.NS",
        "CENTRALBK.NS","CDSL.NS","CENTURYPLY.NS","CERA.NS","CHALET.NS","CHAMBLFERT.NS","CHOLAFIN.NS","CHOLAHLDNG.NS","CIPLA.NS","CUB.NS",
        "COALINDIA.NS","COFORGE.NS","COLPAL.NS","CAMS.NS","CONCOR.NS","COROMANDEL.NS","CRAFTSMAN.NS","CREDITACC.NS","CROMPTON.NS","CUMMINSIND.NS",
        "DCMSHRIRAM.NS","DLF.NS","DABUR.NS","DALBHARAT.NS","DATAPATTNS.NS","DEEPAKFERT.NS","DEEPAKNTR.NS","DELHIVERY.NS","DEVYANI.NS","DIVISLAB.NS",
        "DIXON.NS","LALPATHLAB.NS","DRREDDY.NS","EIDPARRY.NS","EIHOTEL.NS","EPL.NS","EASEMYTRIP.NS","EICHERMOT.NS","ELGIEQUIP.NS","EMAMILTD.NS",
        "ENDURANCE.NS","ENGINERSIN.NS","ESCORTS.NS","EXIDEIND.NS","FDC.NS","FEDERALBNK.NS","FINEORG.NS","FINCABLES.NS","FINPIPE.NS","FSL.NS",
        "FORTIS.NS","GAIL.NS","GMRINFRA.NS","GALAXYSURF.NS","GRSE.NS","GARFIBRES.NS","GICRE.NS","GILLETTE.NS","GLAND.NS","GLAXO.NS",
        "GLENMARK.NS","MEDANTA.NS","GODFRYPHLP.NS","GODREJCP.NS","GODREJIND.NS","GODREJPROP.NS","GRANULES.NS","GRAPHITE.NS","GRASIM.NS","GESHIP.NS",
        "GRINDWELL.NS","GAEL.NS","GODREJAGRO.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HFCL.NS","HAPPSTMNDS.NS","HAPPYFORGE.NS",
        "HAVELLS.NS","HEROMOTOCO.NS","HINDALCO.NS","HAL.NS","HINDPETRO.NS","HINDUNILVR.NS","HINDZINC.NS","POWERINDIA.NS","HOMEFIRST.NS","HONASA.NS",
        "HONAUT.NS","HUDCO.NS","HYUNDAI.NS","ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS","IDBI.NS","IDFCFIRSTB.NS","IDFC.NS","IIFL.NS",
        "IRB.NS","IRCON.NS","ITC.NS","ITI.NS","INDIACEM.NS","INDIAMART.NS","INDIANB.NS","IEX.NS","INDHOTEL.NS","IOC.NS",
        "IRCTC.NS","IRFC.NS","INDUSINDBK.NS","NAUKRI.NS","INFY.NS","INDIGO.NS","IPCALAB.NS","JBCHEPHARM.NS","JKCEMENT.NS","JKTYRE.NS",
        "JMFINANCIL.NS","JSWENERGY.NS","JSWSTEEL.NS","JAMNAAUTO.NS","JINDALSTEL.NS","JIOFIN.NS","JUBLFOOD.NS","JUSTDIAL.NS","JYOTHYLAB.NS","KPRMILL.NS",
        "KEI.NS","KNRCON.NS","KPITTECH.NS","KRBL.NS","KAJARIACER.NS","KPIL.NS","KALYANKJIL.NS","KANSAINER.NS","KARURVYSYA.NS","KEC.NS",
        "KALYAN.NS","KOTAKBANK.NS","KIMS.NS","LTF.NS","LTTS.NS","LICHSGFIN.NS","LTIM.NS","LT.NS","LATENTVIEW.NS","LAURUSLABS.NS",
        "LEMONTREE.NS","LICI.NS","LINDEINDIA.NS","LLOYDSME.NS","LUPIN.NS","MMTC.NS","MRF.NS","MTARTECH.NS","LODHA.NS","M&M.NS",
        "M&MFIN.NS","MANKIND.NS","MARICO.NS","MARUTI.NS","MASTEK.NS","MFSL.NS","MAXHEALTH.NS","MAZDOCK.NS","MEDPLUS.NS","MOTHERSON.NS",
        "METROPOLIS.NS","MINDACORP.NS","MSUMI.NS","MIDHANI.NS","MPHASIS.NS","MCX.NS","MUTHOOTFIN.NS","NATCOPHARM.NS","NBCC.NS","NCC.NS",
        "NHPC.NS","NLCINDIA.NS","NMDC.NS","NSLNISP.NS","NTPC.NS","NH.NS","NATIONALUM.NS","NFL.NS","NAVINFLUOR.NS","NESTLEIND.NS",
        "NAM-INDIA.NS","OBEROIRLTY.NS","ONGC.NS","OIL.NS","OLECTRA.NS","PAYTM.NS","OFSS.NS","POLICYBZR.NS","PCBL.NS","PIIND.NS",
        "PAGEIND.NS","PATANJALI.NS","PERSISTENT.NS","PETRONET.NS","PFIZER.NS","PHOENIXLTD.NS","PIDILITIND.NS","PEL.NS","PPLPHARMA.NS","POLYMED.NS",
        "POLYCAB.NS","POONAWALLA.NS","PFC.NS","POWERGRID.NS","PRESTIGE.NS","RBLBANK.NS","RECLTD.NS","RHIM.NS","RITES.NS","RADICO.NS",
        "RVNL.NS","RAILTEL.NS","RAJESHEXPO.NS","RALLIS.NS","RAMCOCEM.NS","RELIANCE.NS","RELIGARE.NS","RPOWER.NS","SBICARD.NS","SBILIFE.NS",
        "SJVN.NS","SKFINDIA.NS","SRF.NS","SAIL.NS","SANOFI.NS","SAPPHIRE.NS","SAREGAMA.NS","SCHAEFFLER.NS","SEQUENT.NS","SHREECEM.NS",
        "SHRIRAMFIN.NS","SHYAMMETL.NS","SIEMENS.NS","SIGNATURE.NS","SBIN.NS","SWSOLAR.NS","SONACOMS.NS","SONATSOFTW.NS","STARHEALTH.NS","SBFC.NS",
        "SUNPHARMA.NS","SUNTV.NS","SUNDARMFIN.NS","SUNDRMFAST.NS","SUPREMEIND.NS","SUZLON.NS","SWANENERGY.NS","SYNGENE.NS","SYRMA.NS","TTKPRESTIG.NS",
        "TVSMOTOR.NS","TATACHEM.NS","TATACOMM.NS","TCS.NS","TATACONSUM.NS","TATAELXSI.NS","TATAMOTORS.NS","TATAPOWER.NS","TATASTEEL.NS","TATATECH.NS",
        "TTML.NS","TECHM.NS","TEJASNET.NS","NIACL.NS","RAMCOIND.NS","THOMASCOOK.NS","THYROCARE.NS","TITAN.NS","TMB.NS","TORNTPHARM.NS",
        "TORNTPOWER.NS","TRENT.NS","TRIDENT.NS","TRIVENI.NS","TRITURBINE.NS","TIINDIA.NS","UCOBANK.NS","UNOMINDA.NS","UPL.NS","UTIAMC.NS",
        "ULTRACEMCO.NS","UNIONBANK.NS","UBL.NS","MCDOWELL-N.NS","VGUARD.NS","VARROC.NS","VBL.NS","MANYAVAR.NS","VEDL.NS","VOLTAS.NS",
        "WELCORP.NS","WELSPUNLIV.NS","WESTLIFE.NS","WHIRLPOOL.NS","WIPRO.NS","YESBANK.NS","ZFCVINDIA.NS","ZEEL.NS","ZENSARTECH.NS","ZOMATO.NS","ZYDUSLIFE.NS"
    ]

if "all_stocks" not in st.session_state:
    st.session_state.all_stocks = get_nifty500()

st.title("📦 Blackbox PRO - Only BUY Scanner")
st.success(f"✅ NIFTY 500 Loaded: {len(st.session_state.all_stocks)} Stocks")

# Add new stock
c1,c2 = st.columns([4,1])
with c1:
    new_stock = st.text_input("Naya stock add karo", placeholder="jaise SUZLON.NS", label_visibility="collapsed").upper().strip()
with c2:
    if st.button("Add Stock"):
        if new_stock:
            if not new_stock.endswith(".NS"): new_stock += ".NS"
            if new_stock not in st.session_state.all_stocks:
                st.session_state.all_stocks.insert(0, new_stock)
                st.toast(f"{new_stock} add ho gaya!")

def get_close(df):
    c = df['Close']
    if isinstance(c, pd.DataFrame): c = c.iloc[:,0]
    return c

search = st.text_input("🔍 Search", placeholder="TATA, BANK, SUZLON")
filtered = st.session_state.all_stocks
if search:
    filtered = [s for s in st.session_state.all_stocks if search.upper() in s]

stocks = st.multiselect(f"Stocks chuno ({len(filtered)} me se)", filtered, default=filtered[:5])

if st.button(f"Scan {len(stocks)} Stocks 🔍", type="primary"):
    buy_list = []
    prog = st.progress(0)
    status = st.empty()

    for i,s in enumerate(stocks):
        status.text(f"Scanning {s}... {i+1}/{len(stocks)}")
        try:
            df = yf.download(s, period="6mo", interval="1d", progress=False, auto_adjust=True)
            if len(df) < 30:
                prog.progress((i+1)/len(stocks))
                continue
            close = get_close(df)
            e9 = close.ewm(span=9).mean()
            e26 = close.ewm(span=26).mean()
            macd = close.ewm(span=12).mean() - close.ewm(span=26).mean()
            sig = macd.ewm(span=9).mean()
            lc = float(close.iloc[-1])
            le9 = float(e9.iloc[-1])
            le26 = float(e26.iloc[-1])
            lm = float(macd.iloc[-1])
            ls = float(sig.iloc[-1])

            # ONLY BUY CONDITION
            if le9 > le26 and lm > ls:
                sl = lc * 0.98
                tgt = lc * 1.04
                st.success(f"✅ BUY: {s} @ {lc:.2f} | SL: {sl:.2f} | Target: {tgt:.2f}")
                buy_list.append(s)
                st.line_chart(pd.DataFrame({"Close":close.tail(40),"E9":e9.tail(40),"E26":e26.tail(40)}))
                st.divider()
        except:
            pass
        prog.progress((i+1)/len(stocks))

    status.empty()
    prog.empty()

    if buy_list:
        st.balloons()
        st.success(f"🎯 Total {len(buy_list)} BUY Found: {', '.join(buy_list)}")
    else:
        st.warning("Aaj koi BUY nahi hai - Market weak hai")
