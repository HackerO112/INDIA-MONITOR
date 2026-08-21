"""India Monitor — comprehensive live country intelligence dashboard.
Run:  streamlit run app.py --server.port 5000
"""

from __future__ import annotations

import html, math, time, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests, streamlit as st

# ── page & palette ────────────────────────────────────────────────
st.set_page_config(page_title="India Monitor", page_icon="🇮🇳",
                   layout="wide", initial_sidebar_state="expanded")

N  = "#0B1F35"   # navy
O  = "#F2994A"   # saffron
G  = "#2D9B75"   # green
B  = "#3D7FA6"   # blue
T  = "#1A8A7D"   # teal
P  = "#7B61FF"   # purple
K  = "#14202B"   # ink
M  = "#667788"   # muted
R  = "#D95D5D"   # red
BG = "#F5F7FA"   # background
TIMEOUT = 10

# ── style injection ───────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    :root{--n:#0B1F35;--o:#F2994A;--g:#2D9B75;--b:#3D7FA6;--t:#1A8A7D;--p:#7B61FF;--k:#14202B;--m:#667788;--r:#D95D5D;--bg:#F5F7FA}
    .stApp{background:#F5F7FA;color:#14202B}
    [data-testid="stHeader"]{background:rgba(245,247,250,.94);backdrop-filter:blur(12px)}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#0B1F35 0%,#0d2740 100%)}
    [data-testid="stSidebar"] *{color:#dce8f0!important}
    [data-testid="stSidebar"] .stRadio>label>div>span{font-weight:600;font-size:.92rem;padding:.55rem .8rem;border-radius:10px;transition:all .2s}
    [data-testid="stSidebar"] .stRadio>label>div>span:hover{background:rgba(255,255,255,.08)}
    [data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.12);margin:1rem 0}
    [data-testid="stSidebar"] .stCaption{color:#8ba3b8!important}
    .block-container{max-width:1500px;padding-top:1.6rem;padding-bottom:3rem}

    .hero{background:linear-gradient(135deg,#0b1f35 0%,#0f3452 50%,#17504f 100%);border-radius:22px;padding:2.2rem 2.6rem;color:#fff;margin-bottom:1.2rem;box-shadow:0 16px 48px rgba(11,31,53,.22);position:relative;overflow:hidden}
    .hero::after{content:"";position:absolute;top:-60px;right:-40px;width:260px;height:260px;background:radial-gradient(circle,rgba(242,153,74,.18) 0%,transparent 70%);pointer-events:none}
    .hero h1{font-size:clamp(2rem,4.5vw,3.8rem);letter-spacing:-.06em;margin:0;font-weight:900}
    .hero p{color:#b8cfe0;max-width:680px;font-size:1rem;margin:.65rem 0 0;line-height:1.55}
    .eyebrow{color:#8ec5d0;text-transform:uppercase;letter-spacing:.18em;font-size:.7rem;font-weight:800}

    .pill{display:inline-flex;align-items:center;gap:4px;padding:.28rem .6rem;border-radius:999px;font-size:.7rem;font-weight:700;letter-spacing:.03em}
    .pill-live{background:#dff5eb;color:#14694d}
    .pill-est{background:#fff0d9;color:#87511c}
    .pulse{width:6px;height:6px;border-radius:50%;background:#2D9B75;animation:pulse 1.6s infinite}
    @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}

    .mc{background:#fff;border:1px solid #e8edf2;border-radius:16px;padding:1rem 1.1rem;min-height:130px;box-shadow:0 2px 12px rgba(11,31,53,.04);transition:all .25s;position:relative;overflow:hidden}
    .mc:hover{transform:translateY(-3px);box-shadow:0 8px 28px rgba(11,31,53,.09)}
    .mc::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;border-radius:4px 0 0 4px}
    .mc-o::before{background:#F2994A}.mc-g::before{background:#2D9B75}.mc-b::before{background:#3D7FA6}
    .mc-t::before{background:#1A8A7D}.mc-p::before{background:#7B61FF}.mc-n::before{background:#0B1F35}
    .mc-label{color:#667788;font-size:.72rem;text-transform:uppercase;letter-spacing:.09em;font-weight:800}
    .mc-val{color:#0B1F35;font-size:1.65rem;font-weight:900;margin-top:.4rem;line-height:1.1}
    .mc-trend{font-size:.9rem;margin-left:6px;font-weight:700}
    .mc-sub{color:#667788;font-size:.74rem;margin-top:.35rem;display:flex;align-items:center;gap:6px;flex-wrap:wrap}

    .stitle{margin-top:1.5rem;margin-bottom:.15rem;color:#0B1F35;font-size:1.22rem;font-weight:900;padding-bottom:.35rem;border-bottom:2px solid #F2994A;display:inline-block}
    .scopy{color:#667788;margin-bottom:.85rem;font-size:.88rem}

    .nw{background:#fff;border:1px solid #e8edf2;border-radius:14px;padding:.75rem .95rem;margin:.45rem 0;transition:all .2s}
    .nw:hover{border-color:#F2994A;box-shadow:0 4px 16px rgba(242,153,74,.1)}
    .nw a{color:#0B1F35;text-decoration:none;font-weight:700;font-size:.92rem}
    .nw a:hover{color:#F2994A}
    .nw-meta{color:#667788;font-size:.7rem;margin-top:.3rem}

    .ibox{background:linear-gradient(135deg,#eef6ff 0%,#f0faf7 100%);border:1px solid #d4e6f1;border-radius:14px;padding:1rem 1.2rem;font-size:.88rem;color:#14202B}
    .src-line{color:#667788;font-size:.73rem;border-top:1px solid #e7edf2;padding-top:.6rem;margin-top:1.5rem}

    @media(max-width:768px){
      .block-container{padding:.8rem .6rem 2rem}
      .hero{padding:1.3rem 1.1rem;border-radius:16px}
      .hero h1{font-size:2rem}
      .mc{min-height:115px;padding:.8rem}
      .mc-val{font-size:1.3rem}
      [data-testid="stHorizontalBlock"]{gap:.5rem}
    }
    @media(max-width:480px){
      .hero h1{font-size:1.7rem}
      .mc-val{font-size:1.15rem}
    }
    ::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#c4cdd6;border-radius:8px}
    </style>""", unsafe_allow_html=True)

inject_css()

# ── network helper ────────────────────────────────────────────────
UA = {"User-Agent": "IndiaMonitor/2.0 (public dashboard; +https://github.com)"}

def _get(url: str, params: dict | None = None):
    try:
        r = requests.get(url, params=params, timeout=TIMEOUT, headers=UA)
        r.raise_for_status(); return r
    except Exception:
        return None

# ── data fetchers ─────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def wb(code: str, n: int = 20) -> pd.DataFrame:
    r = _get(f"https://api.worldbank.org/v2/country/IND/indicator/{code}",
             {"format": "json", "per_page": n})
    if not r: return pd.DataFrame(columns=["year", "value"])
    try:
        rows = r.json()[1]
        return pd.DataFrame([{"year": int(d["date"]), "value": d["value"]}
                             for d in rows if d.get("value") is not None]).sort_values("year")
    except Exception:
        return pd.DataFrame(columns=["year", "value"])

@st.cache_data(ttl=300, show_spinner=False)
def yahoo(sym: str) -> pd.DataFrame:
    r = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",
             {"range": "1y", "interval": "1d"})
    if not r: return pd.DataFrame(columns=["date", "close"])
    try:
        res = r.json()["chart"]["result"][0]
        ts = res["timestamp"]; cs = res["indicators"]["quote"][0]["close"]
        return pd.DataFrame({"date": [datetime.fromtimestamp(t, tz=timezone.utc).date() for t in ts],
                             "close": cs}).dropna()
    except Exception:
        return pd.DataFrame(columns=["date", "close"])

@st.cache_data(ttl=600, show_spinner=False)
def weather() -> dict | None:
    r = _get("https://api.open-meteo.com/v1/forecast",
             {"latitude": 28.6139, "longitude": 77.209,
              "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
              "timezone": "Asia/Kolkata"})
    if not r: return None
    try: return r.json()["current"]
    except Exception: return None

@st.cache_data(ttl=600, show_spinner=False)
def aqi() -> dict | None:
    r = _get("https://air-quality-api.open-meteo.com/v1/air-quality",
             {"latitude": 28.6139, "longitude": 77.209,
              "current": "pm10,pm2_5,us_aqi,indian_aqi",
              "timezone": "Asia/Kolkata"})
    if not r: return None
    try: return r.json()["current"]
    except Exception: return None

@st.cache_data(ttl=600, show_spinner=False)
def headlines() -> list[dict]:
    r = _get("https://news.google.com/rss/search",
             {"q": "India economy business policy technology", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})
    if not r: return []
    try:
        root = ET.fromstring(r.content)
        return [{"title": it.findtext("title", ""), "link": it.findtext("link", "#"),
                 "date": it.findtext("pubDate", ""), "src": it.findtext("source", "News")}
                for it in root.findall("./channel/item")[:10]]
    except Exception:
        return []

# ── indicator registry ────────────────────────────────────────────
IND = {
    # ── macro ──
    "GDP growth":       ("NY.GDP.MKTP.KD.ZG", "%",      "Real GDP annual growth"),
    "GDP nominal":      ("NY.GDP.MKTP.CD",    "USD B",  "GDP current US$"),
    "GDP per capita":   ("NY.GDP.PCAP.CD",    "USD",    "GDP per person"),
    "GNI per capita":   ("NY.GNP.PCAP.CD",    "USD",    "GNI per person (Atlas method)"),
    "Inflation":        ("FP.CPI.TOTL.ZG",    "%",      "Consumer price inflation"),
    "Unemployment":     ("SL.UEM.TOTL.ZS",    "%",      "ILO unemployment rate"),
    "Population":       ("SP.POP.TOTL",       "",       "Total population"),
    "Urban pop":        ("SP.URB.TOTL.IN.ZS", "%",      "Urban population share"),
    # ── sectoral ──
    "Agriculture":      ("NV.AGR.TOTL.ZS",    "% GDP",  "Agriculture value added"),
    "Industry":         ("NV.IND.TOTL.ZS",    "% GDP",  "Industry value added"),
    "Services":         ("NV.SRV.TOTL.ZS",    "% GDP",  "Services value added"),
    "Manufacturing":    ("NV.IND.MANF.ZS",    "% GDP",  "Manufacturing value added"),
    # ── trade ──
    "Exports":          ("NE.EXP.GNFS.ZS",    "% GDP",  "Exports of goods & services"),
    "Imports":          ("NE.IMP.GNFS.ZS",    "% GDP",  "Imports of goods & services"),
    "Trade balance":    ("NE.TRD.GNFS.ZS",    "% GDP",  "Net trade balance"),
    "FDI inflows":      ("BX.KLT.DINV.WD.GD.ZS","% GDP","FDI net inflows"),
    "High-tech exports":("TX.VAL.TECH.MF.ZS", "%",      "High-tech in manufactured exports"),
    # ── fiscal ──
    "Govt debt":        ("GC.DOD.TOTL.GD.ZS", "% GDP",  "Central government debt"),
    "Tax revenue":      ("GC.REV.XGRT.GD.ZS", "% GDP",  "Tax revenue"),
    "Govt spending":    ("GC.XPN.TOTL.GD.ZS", "% GDP",  "Government expenditure"),
    # ── health ──
    "Life expectancy":  ("SP.DYN.LE00.IN",    "years",  "Life expectancy at birth"),
    "Infant mortality": ("SP.DYN.IMRT.IN",    "per 1k", "Infant deaths per 1 000 live births"),
    "Health spend":     ("SH.XPD.CHEX.GD.ZS", "% GDP",  "Current health expenditure"),
    "Physicians":       ("SH.MED.PHYS.ZS",    "per 1k", "Physicians per 1 000"),
    "Hospital beds":    ("SH.MED.BEDS.ZS",    "per 1k", "Hospital beds per 1 000"),
    "Birth rate":       ("SP.DYN.CBRT.IN",    "per 1k", "Crude birth rate"),
    "Death rate":       ("SP.DYN.CDRT.IN",    "per 1k", "Crude death rate"),
    # ── education ──
    "Primary enrol":    ("SE.PRM.ENRR",       "%",      "Primary school enrolment"),
    "Secondary enrol":  ("SE.SEC.ENRR",       "%",      "Secondary school enrolment"),
    "Tertiary enrol":   ("SE.TER.ENRR",       "%",      "Tertiary school enrolment"),
    "Edu spend":        ("SE.XPD.TOTL.GD.ZS", "% GDP",  "Government education expenditure"),
    "Literacy rate":    ("SE.ADT.LITR.ZS",    "%",      "Adult literacy rate"),
    # ── demographics ──
    "Age 0-14":         ("SP.POP.0014.TO.ZS", "%",      "Population age 0-14"),
    "Age 15-64":        ("SP.POP.1564.TO.ZS", "%",      "Working-age population 15-64"),
    "Age 65+":          ("SP.POP.65UP.TO.ZS", "%",      "Population age 65+"),
    "Fertility":        ("SP.DYN.TFRT.IN",    "",       "Total fertility rate"),
    # ── energy ──
    "Elec access":      ("EG.ELC.ACCS.ZS",    "%",      "Access to electricity"),
    "Renewable elec":   ("EG.ELC.RNEW.ZS",    "%",      "Renewable electricity output"),
    "Coal elec":        ("EG.ELC.COAL.ZS",    "%",      "Coal electricity output"),
    "Gas elec":         ("EG.ELC.GAS.ZS",     "%",      "Natural gas electricity"),
    "Hydro elec":       ("EG.ELC.HYRO.ZS",    "%",      "Hydroelectric output"),
    "Nuclear elec":     ("EG.ELC.NUCL.ZS",    "%",      "Nuclear electricity"),
    "Oil elec":         ("EG.ELC.PETR.ZS",    "%",      "Oil electricity"),
    "Energy per GDP":   ("EG.USE.COMM.GD.PP.KD","",     "Energy use per unit GDP"),
    # ── digital ──
    "Internet users":   ("IT.NET.USER.ZS",    "%",      "Individuals using internet"),
    "Mobile subs":      ("IT.CEL.SETS.P2",    "per 100","Mobile subscriptions per 100"),
    "Secure internet":  ("IT.NET.SECR.P6",    "%",      "Secure internet servers per 1M"),
    # ── environment ──
    "CO2 per cap":      ("EN.ATM.CO2E.PC",    "t",      "CO₂ emissions per capita"),
    "CO2 total":        ("EN.ATM.CO2E.KT",    "kt",     "Total CO₂ emissions"),
    "Forest area":      ("AG.LND.FRST.ZS",    "% land", "Forest area"),
    "Freshwater use":   ("ER.H2O.FWTL.ZS",    "%",      "Annual freshwater withdrawal"),
    "Renewable internal":("EG.ELC.RNWX.ZS",   "%",      "Renewable internal freshwater"),
    # ── financial ──
    "Credit private":   ("FS.AST.PRVT.GD.ZS", "% GDP",  "Domestic credit to private sector"),
    "Broad money":      ("FM.LBL.BMNY.GD.ZS", "%",      "Broad money growth"),
    "Domestic credit":  ("FS.DMT.CIST.GD.ZS", "% GDP",  "Domestic credit to private sector"),
    # ── transport ──
    "Rail lines":       ("IS.RRS.TOTL.KM",    "km",     "Railway lines total"),
    "Air passengers":   ("IS.AIR.PSGR",       "",       "Air passengers carried"),
    "Ports traffic":    ("IS.SHP.GCNW.XQ",    "",       "Container port traffic (TEU)"),
}

@st.cache_data(ttl=1800, show_spinner=False)
def snapshot() -> dict:
    out = {}
    for name, (code, unit, defn) in IND.items():
        df = wb(code, 25)
        if df.empty:
            out[name] = {"v": None, "y": None, "u": unit, "d": defn, "p": None}
        else:
            last = df.iloc[-1]
            prev = df.iloc[-2]["value"] if len(df) > 1 else None
            out[name] = {"v": float(last["value"]), "y": int(last["year"]),
                         "u": unit, "d": defn,
                         "p": float(prev) if prev is not None else None}
    return out

# ── helpers ───────────────────────────────────────────────────────
def v(name: str, d: dict) -> float | None:
    x = d.get(name, {}).get("v")
    return float(x) if x is not None else None

def fmt(val, unit="", dp=1):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "—"
    if unit == "USD B": return f"${val/1e9:,.1f}B"
    if unit == "USD":   return f"${val:,.0f}"
    if unit == "kt":    return f"{val/1e3:,.1f}K t" if val > 1e6 else f"{val:,.0f} t"
    if unit == "km":    return f"{val:,.0f}"
    if unit == "" and val > 1e9: return f"{val/1e9:.2f}B"
    if unit == "" and val > 1e6: return f"{val/1e6:.1f}M"
    return f"{val:,.{dp}f}{unit}"

def trend(d: dict, name: str, inverse=False):
    """Return (arrow_char, hex_color, diff_string)."""
    cur = d.get(name, {}).get("v")
    prv = d.get(name, {}).get("p")
    if cur is None or prv is None:
        return "", M, ""
    diff = cur - prv
    if abs(diff) < 1e-9:
        return "→", M, "0"
    up = diff > 0
    good = (not up and inverse) or (up and not inverse)
    arrow = "↑" if up else "↓"
    col = G if good else R
    u = d[name]["u"]
    return arrow, col, f"{fmt(abs(diff), u)}"

def _norm(val, lo, hi, inv=False):
    if val is None: return 50.0
    p = max(0, min(1, (val - lo) / (hi - lo))) if hi != lo else .5
    return round((1 - p if inv else p) * 100, 1)

# ── composite scoring ─────────────────────────────────────────────
def composites(d: dict) -> dict[str, float]:
    gdp_g  = v("GDP growth", d)
    inf    = v("Inflation", d)
    unemp  = v("Unemployment", d)
    pop    = v("Population", d)
    agri   = v("Agriculture", d)
    ind    = v("Industry", d)
    srv    = v("Services", d)
    mfg    = v("Manufacturing", d)
    exp    = v("Exports", d)
    imp    = v("Imports", d)
    fdi    = v("FDI inflows", d)
    htech  = v("High-tech exports", d)
    debt   = v("Govt debt", d)
    tax    = v("Tax revenue", d)
    spend  = v("Govt spending", d)
    life   = v("Life expectancy", d)
    infant = v("Infant mortality", d)
    health = v("Health spend", d)
    phys   = v("Physicians", d)
    beds   = v("Hospital beds", d)
    pri    = v("Primary enrol", d)
    sec    = v("Secondary enrol", d)
    ter    = v("Tertiary enrol", d)
    edus   = v("Edu spend", d)
    lit    = v("Literacy rate", d)
    elec   = v("Elec access", d)
    renew  = v("Renewable elec", d)
    coal   = v("Coal elec", d)
    inet   = v("Internet users", d)
    mob    = v("Mobile subs", d)
    co2    = v("CO2 per cap", d)
    forest = v("Forest area", d)
    credit = v("Credit private", d)
    urban  = v("Urban pop", d)

    econ = (_norm(gdp_g, -3, 10) * .30 +
            _norm(inf, 2, 12, True) * .25 +
            _norm(unemp, 2, 15, True) * .20 +
            _norm(debt, 20, 90, True) * .15 +
            _norm(tax, 5, 30) * .10)

    social = (_norm(life, 50, 85) * .25 +
              _norm(infant, 80, 5, True) * .20 +
              _norm(health, 1, 10) * .15 +
              _norm(sec, 30, 115) * .15 +
              _norm(lit, 40, 100) * .15 +
              _norm(ter, 5, 50) * .10)

    infra = (_norm(elec, 50, 100) * .25 +
             _norm(inet, 10, 95) * .25 +
             _norm(mob, 10, 120) * .15 +
             _norm(renew, 0, 60) * .20 +
             _norm(urban, 20, 50) * .15)

    environ = (_norm(co2, 0.2, 5, True) * .30 +
               _norm(forest, 5, 35) * .25 +
               _norm(renew, 0, 60) * .25 +
               _norm(coal, 20, 85, True) * .20)

    trade_s = (_norm(exp, 5, 40) * .30 +
               _norm(fdi, -2, 6) * .30 +
               _norm(htech, 0, 30) * .20 +
               _norm(credit, 10, 80) * .20)

    fiscal_s = (_norm(debt, 20, 90, True) * .35 +
                _norm(tax, 5, 30) * .35 +
                _norm(spend, 8, 35) * .30)

    overall = (econ * .30 + social * .25 + infra * .20 +
               environ * .10 + trade_s * .10 + fiscal_s * .05)

    return {"Economic Health": round(econ, 1),
            "Social Development": round(social, 1),
            "Infrastructure": round(infra, 1),
            "Environment": round(environ, 1),
            "Trade & Finance": round(trade_s, 1),
            "Fiscal Health": round(fiscal_s, 1),
            "Overall India Score": round(overall, 1)}

def radar_rows(d: dict) -> list[tuple[str, float]]:
    c = composites(d)
    return [(k, c[k]) for k in ["Economic Health", "Social Development",
            "Infrastructure", "Environment", "Trade & Finance", "Fiscal Health"]]

def sector_detail_scores(d: dict) -> pd.DataFrame:
    rows = [
        ("Agriculture & Food",   _norm(v("Agriculture", d), 10, 30, False) * .5 + _norm(v("GDP growth", d), -3, 10) * .5,
         "Crop output share + growth momentum"),
        ("Manufacturing",        _norm(v("Manufacturing", d), 10, 30) * .4 + _norm(v("High-tech exports", d), 0, 30) * .3 + _norm(v("Exports", d), 5, 40) * .3,
         "Mfg share + high-tech exports + trade orientation"),
        ("Services & IT",        _norm(v("Services", d), 35, 75) * .5 + _norm(v("Internet users", d), 10, 95) * .3 + _norm(v("Tertiary enrol", d), 5, 50) * .2,
         "Services depth + digital reach + skilled workforce"),
        ("Banking & Finance",    _norm(v("Credit private", d), 10, 80) * .5 + _norm(v("Broad money", d), 0, 25) * .3 + _norm(v("FDI inflows", d), -2, 6) * .2,
         "Private credit + money supply growth + FDI"),
        ("Healthcare",           _norm(v("Life expectancy", d), 50, 85) * .25 + _norm(v("Infant mortality", d), 80, 5, True) * .25 + _norm(v("Health spend", d), 1, 10) * .2 + _norm(v("Physicians", d), 0, 4) * .15 + _norm(v("Hospital beds", d), 0, 6) * .15,
         "Life expectancy + infant mortality + spending + capacity"),
        ("Education",            _norm(v("Literacy rate", d), 40, 100) * .25 + _norm(v("Secondary enrol", d), 30, 115) * .25 + _norm(v("Tertiary enrol", d), 5, 50) * .2 + _norm(v("Edu spend", d), 1, 8) * .15 + _norm(v("Primary enrol", d), 60, 120) * .15,
         "Literacy + enrolment rates + spending"),
        ("Energy & Power",       _norm(v("Elec access", d), 50, 100) * .3 + _norm(v("Renewable elec", d), 0, 60) * .35 + _norm(v("Coal elec", d), 20, 85, True) * .2 + _norm(v("Energy per GDP", d), 2, 15, True) * .15,
         "Access + renewable transition + efficiency"),
        ("Digital & Telecom",    _norm(v("Internet users", d), 10, 95) * .35 + _norm(v("Mobile subs", d), 10, 120) * .35 + _norm(v("Secure internet", d), 0, 50) * .3,
         "Internet penetration + mobile density + cybersecurity"),
        ("Defence & Security",   65.0,  # placeholder — WB has limited defence data
         "Limited public-data coverage; fixed baseline"),
        ("Real Estate & Urban",  _norm(v("Urban pop", d), 20, 50) * .5 + _norm(v("GDP growth", d), -3, 10) * .3 + _norm(v("Population", d), .5e9, 1.8e9) * .2,
         "Urbanisation pace + growth + demographic demand"),
        ("Tourism & Hospitality", 55.0,  # limited WB tourism indicators
         "Limited public-data coverage; fixed baseline"),
        ("MSME & Entrepreneurship", _norm(v("Credit private", d), 10, 80) * .5 + _norm(v("FDI inflows", d), -2, 6) * .3 + _norm(v("Broad money", d), 0, 25) * .2,
         "Credit access + FDI climate + money supply"),
    ]
    return pd.DataFrame(rows, columns=["Sector", "Score", "Read-through"]).sort_values("Score", ascending=False)

# ── UI components ─────────────────────────────────────────────────
def card(label, value, sub, accent="o", tone="est", tarrow="", tcol=""):
    pill_cls = "pill-live" if tone == "live" else "pill-est"
    tag = '<span class="pulse"></span> LIVE' if tone == "live" else "LATEST"
    ta = f'<span class="mc-trend" style="color:{tcol}">{tarrow}</span>' if tarrow else ""
    st.markdown(f"""<div class="mc mc-{accent}">
      <div class="mc-label">{html.escape(label)}</div>
      <div class="mc-val">{html.escape(str(value))}{ta}</div>
      <div class="mc-sub"><span class="pill {pill_cls}">{tag}</span>&nbsp;{html.escape(sub)}</div>
    </div>""", unsafe_allow_html=True)

def heading(t, c=""):
    st.markdown(f'<div class="stitle">{html.escape(t)}</div>', unsafe_allow_html=True)
    if c: st.markdown(f'<div class="scopy">{html.escape(c)}</div>', unsafe_allow_html=True)

def _line(df, title, ylabel, color=O, height=280):
    if df.empty:
        st.info("Data unavailable for this series."); return
    fig = px.line(df, x="year", y="value", markers=True, title=title)
    fig.update_traces(line=dict(color=color, width=2.5), marker=dict(size=6))
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=46, b=10),
                      paper_bgcolor="#fff", plot_bgcolor="#fff",
                      yaxis_title=ylabel, xaxis_title=None, hovermode="x unified",
                      font=dict(size=12, color=K))
    fig.update_xaxes(showgrid=False, linecolor="#e0e5ea")
    fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5", linecolor="#e0e5ea")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def _area(df, title, ylabel, color=O, height=280):
    if df.empty: st.info("Data unavailable."); return
    fig = px.area(df, x="year", y="value", title=title)
    fig.update_traces(line=dict(color=color, width=2), fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},.15)")
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=46, b=10),
                      paper_bgcolor="#fff", plot_bgcolor="#fff",
                      yaxis_title=ylabel, xaxis_title=None, hovermode="x unified",
                      font=dict(size=12, color=K))
    fig.update_xaxes(showgrid=False, linecolor="#e0e5ea")
    fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5", linecolor="#e0e5ea")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def _bar_h(df, x, y, title, color_map=None, height=300, text_fmt=".1f"):
    if df.empty: st.info("Data unavailable."); return
    fig = px.bar(df, x=x, y=y, orientation="h", text=x, color=y if color_map is None else None,
                 color_continuous_scale=["#f6d4c4", O, G] if color_map is None else None,
                 color_discrete_map=color_map)
    fig.update_traces(texttemplate=f"%{{x:{text_fmt}}}", textposition="outside")
    fig.update_layout(height=height, margin=dict(l=5, r=30, t=15, b=10),
                      paper_bgcolor="#fff", plot_bgcolor="#fff", showlegend=False,
                      yaxis_title=None, font=dict(size=12, color=K))
    if color_map is None:
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(range=[0, max(df[x])*1.25]))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def _gauge(val, title, color=O, height=220):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=val,
        number=dict(suffix="/100", font=dict(size=30, color=N, weight="bold")),
        gauge=dict(axis=dict(range=[0,100], tickwidth=1, tickcolor="#ccd3da"),
                   bar=dict(color=color, thickness=.7),
                   steps=[dict(range=[0,40], color="#fde9e9"),
                          dict(range=[40,70], color="#fff1dc"),
                          dict(range=[70,100], color="#e2f3ea")],
                   threshold=dict(line=dict(color="#ccc", width=1), thickness=.6, value=val))))
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=32, b=0), paper_bgcolor="#fff",
                      title=dict(text=title, font=dict(size=13, color=M, weight="bold"), x=.5, xanchor="center"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── sidebar ───────────────────────────────────────────────────────
if "last_r" not in st.session_state:
    st.session_state.last_r = time.time()

with st.sidebar:
    st.markdown("### 🇮🇳 INDIA MONITOR")
    st.caption("Comprehensive country intelligence")
    st.divider()
    auto = st.toggle("Auto-refresh", value=False, key="auto_ref")
    if auto:
        interval = st.select_slider("Interval", options=[5, 10, 15, 30, 60], value=15,
                                    format_func=lambda x: f"{x} min")
    if st.button("⟳  Refresh now", use_container_width=True, type="primary"):
        st.cache_data.clear(); st.session_state.last_r = time.time(); st.rerun()
    st.divider()
    view = st.radio("Navigate", [
        "📊  Overview",
        "💰  Economy",
        "🏭  Sectors",
        "👥  People",
        "🏗️  Infrastructure",
        "📈  Markets & Climate",
        "📋  Sources & Methods",
    ], label_visibility="collapsed")
    st.divider()
    st.caption("**Country at a glance**")
    st.markdown("""
    <div style="font-size:.82rem;line-height:1.7;color:#b0c4d4">
    <b>Capital</b> &nbsp; New Delhi<br>
    <b>Currency</b> &nbsp; ₹ Indian Rupee<br>
    <b>Area</b> &nbsp; 3.287 M km²<br>
    <b>Languages</b> &nbsp; Hindi, English +21<br>
    <b>Timezone</b> &nbsp; IST (UTC+5:30)<br>
    <b>ISO</b> &nbsp; IN / IND / 356
    </div>""", unsafe_allow_html=True)

if auto and time.time() - st.session_state.last_r > interval * 60:
    st.cache_data.clear(); st.session_state.last_r = time.time(); st.rerun()

# ── fetch data ────────────────────────────────────────────────────
D = snapshot()
C = composites(D)
now_str = datetime.now().astimezone().strftime("%d %b %Y · %H:%M IST")

# ── hero ──────────────────────────────────────────────────────────
st.markdown(f"""<div class="hero">
<div class="eyebrow">National intelligence brief · Republic of India</div>
<h1>India, in motion.</h1>
<p>A comprehensive monitor of the forces shaping 1.4 billion people — growth, sectors, people, markets, climate, and the signals between them.</p>
<div style="margin-top:1rem"><span class="pill pill-live"><span class="pulse"></span>&nbsp; REFRESHED {now_str}</span></div>
</div>""", unsafe_allow_html=True)

# ── VIEW: OVERVIEW ────────────────────────────────────────────────
if "Overview" in view:
    heading("Key national indicators", "Latest available readings with year-over-year change direction.")

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    for i, (name, accent) in enumerate([
        ("GDP growth", "o"), ("Inflation", "r" if (v("Inflation", D) or 0) > 6 else "g"),
        ("Unemployment", "b"), ("Population", "n"), ("GDP per capita", "p"),
        ("Life expectancy", "g")]):
        val = v(name, D)
        ar, ac, ad = trend(D, name, inverse=name in ("Inflation", "Unemployment"))
        yr = D[name]["y"] or "—"
        sub = f"{yr} · {D[name]['d']}"
        if ad: sub += f" ({ad})"
        card(name, fmt(val, D[name]["u"]), sub, accent, "est", ar, ac)
        if i < 3:
            with [c1, c2, c3][i]: pass
        else:
            with [c4, c5, c6][i-3]: pass

    # re-render cards inside columns
    st.markdown("")  # spacer
    c1, c2, c3 = st.columns(3)
    with c1:
        val = v("GDP growth", D); ar, ac, ad = trend(D, "GDP growth")
        card("GDP growth", fmt(val, "%"), f"{D['GDP growth']['y'] or '—'} · {D['GDP growth']['d']}" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
    with c2:
        val = v("Inflation", D); ar, ac, ad = trend(D, "Inflation", inverse=True)
        card("Inflation", fmt(val, "%"), f"{D['Inflation']['y'] or '—'} · {D['Inflation']['d']}" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
    with c3:
        val = v("Unemployment", D); ar, ac, ad = trend(D, "Unemployment", inverse=True)
        card("Unemployment", fmt(val, "%"), f"{D['Unemployment']['y'] or '—'} · {D['Unemployment']['d']}" + (f" ({ad})" if ad else ""), "b", "est", ar, ac)

    c4, c5, c6 = st.columns(3)
    with c4:
        val = v("Population", D); ar, ac, ad = trend(D, "Population")
        card("Population", fmt(val, D["Population"]["u"]), f"{D['Population']['y'] or '—'} · Total residents" + (f" ({ad})" if ad else ""), "n", "est", ar, ac)
    with c5:
        val = v("GDP per capita", D); ar, ac, ad = trend(D, "GDP per capita")
        card("GDP per capita", fmt(val, "USD"), f"{D['GDP per capita']['y'] or '—'} · Per person" + (f" ({ad})" if ad else ""), "p", "est", ar, ac)
    with c6:
        val = v("Life expectancy", D); ar, ac, ad = trend(D, "Life expectancy")
        card("Life expectancy", fmt(val, "years"), f"{D['Life expectancy']['y'] or '—'} · At birth" + (f" ({ad})" if ad else ""), "g", "est", ar, ac)

    # gauge + radar
    st.markdown("")
    g1, g2 = st.columns([1, 1.2])
    with g1:
        heading("Composite score", "Weighted blend of six sub-indices (see Methods).")
        _gauge(C["Overall India Score"], "India Monitor Score")
        sub_scores = pd.DataFrame([("Economic Health", C["Economic Health"], O),
                                   ("Social Dev.", C["Social Development"], G),
                                   ("Infrastructure", C["Infrastructure"], B),
                                   ("Environment", C["Environment"], T),
                                   ("Trade & Finance", C["Trade & Finance"], P),
                                   ("Fiscal Health", C["Fiscal Health"], "#e67e22")],
                                  columns=["Index", "Score", "Color"])
        fig = px.bar(sub_scores, x="Score", y="Index", orientation="h",
                     color="Index", color_discrete_map={r["Index"]: r["Color"] for _, r in sub_scores.iterrows()},
                     text="Score")
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig.update_layout(height=220, margin=dict(l=5, r=30, t=10, b=5),
                          paper_bgcolor="#fff", plot_bgcolor="#fff", showlegend=False,
                          xaxis=dict(range=[0, 110]), yaxis_title=None,
                          font=dict(size=11, color=K))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with g2:
        heading("Radar profile", "Six-dimensional national fingerprint.")
        rr = radar_rows(D)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[r[1] for r in rr] + [rr[0][1]],
            theta=[r[0] for r in rr] + [rr[0][0]],
            fill="toself", fillcolor="rgba(242,153,74,.18)",
            line=dict(color=O, width=2.5),
            marker=dict(size=7, color=O)))
        fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100], tickfont=dict(size=9, color=M),
                                      gridcolor="#edf0f4", angle=45),
                                    angularaxis=dict(tickfont=dict(size=11, color=K), gridcolor="#edf0f4",
                                                    rotation=45, direction="clockwise")),
                          height=360, margin=dict(l=10, r=10, t=10, b=10),
                          paper_bgcolor="#fff", showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # sector snapshot
    st.markdown("")
    heading("Sector signal summary", "12-sector scan. Scores are normalised 0–100 composites from World Bank data.")
    ss = sector_detail_scores(D)
    fig = px.bar(ss, x="Score", y="Sector", orientation="h", color="Score",
                 color_continuous_scale=["#f6d4c4", O, G], text="Score")
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(height=420, margin=dict(l=10, r=35, t=10, b=10),
                      paper_bgcolor="#fff", plot_bgcolor="#fff", coloraxis_showscale=False,
                      xaxis=dict(range=[0, 110]), yaxis_title=None, font=dict(size=11, color=K))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # headlines
    st.markdown("")
    heading("Live headlines", "India business and policy context from public news feeds.")
    stories = headlines()
    if stories:
        for s in stories[:6]:
            st.markdown(f'<div class="nw"><a href="{html.escape(s["link"])}" target="_blank" rel="noopener">{html.escape(s["title"])}</a><div class="nw-meta">{html.escape(s["src"])} · {html.escape(s["date"])}</div></div>',
                        unsafe_allow_html=True)
    else:
        st.info("Headline feed is temporarily unavailable.")

# ── VIEW: ECONOMY ─────────────────────────────────────────────────
elif "Economy" in view:
    heading("Macroeconomic deep dive", "GDP, prices, labour, fiscal position, and trade flows — with long-run context.")
    tabs = st.tabs(["GDP", "Prices & Labour", "Fiscal", "Trade & Capital"])
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            val = v("GDP growth", D); ar, ac, ad = trend(D, "GDP growth")
            card("GDP growth", fmt(val, "%"), f"{D['GDP growth']['y'] or '—'} · Real annual" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
            card("GDP nominal", fmt(v("GDP nominal", D), "USD B"), f"{D['GDP nominal']['y'] or '—'} · Current US$", "o")
        with c2:
            card("GDP per capita", fmt(v("GDP per capita", D), "USD"), f"{D['GDP per capita']['y'] or '—'}", "p")
            card("GNI per capita", fmt(v("GNI per capita", D), "USD"), f"{D['GNI per capita']['y'] or '—'} · Atlas method", "p")
        _area(wb("NY.GDP.MKTP.KD.ZG", 30), "Real GDP growth trend", "%", O)
        _line(wb("NY.GDP.MKTP.CD", 20), "Nominal GDP (US$ B)", "US$ B", N)
    with tabs[1]:
        c1, c2, c3 = st.columns(3)
        with c1:
            val = v("Inflation", D); ar, ac, ad = trend(D, "Inflation", True)
            card("CPI Inflation", fmt(val, "%"), f"{D['Inflation']['y'] or '—'}" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
        with c2:
            val = v("Unemployment", D); ar, ac, ad = trend(D, "Unemployment", True)
            card("Unemployment", fmt(val, "%"), f"{D['Unemployment']['y'] or '—'} · ILO" + (f" ({ad})" if ad else ""), "b", "est", ar, ac)
        with c3:
            card("Population", fmt(v("Population", D), ""), f"{D['Population']['y'] or '—'}", "n")
        a1, a2 = st.columns(2)
        with a1: _line(wb("FP.CPI.TOTL.ZG", 25), "Consumer price inflation", "%", R)
        with a2: _line(wb("SL.UEM.TOTL.ZS", 20), "Unemployment rate (ILO)", "%", B)
    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        with c1:
            val = v("Govt debt", D); ar, ac, ad = trend(D, "Govt debt", True)
            card("Govt debt", fmt(val, "% GDP"), f"{D['Govt debt']['y'] or '—'}" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
        with c2:
            val = v("Tax revenue", D); ar, ac, ad = trend(D, "Tax revenue")
            card("Tax revenue", fmt(val, "% GDP"), f"{D['Tax revenue']['y'] or '—'}" + (f" ({ad})" if ad else ""), "g", "est", ar, ac)
        with c3:
            val = v("Govt spending", D); ar, ac, ad = trend(D, "Govt spending")
            card("Govt spending", fmt(val, "% GDP"), f"{D['Govt spending']['y'] or '—'}" + (f" ({ad})" if ad else ""), "b", "est", ar, ac)
        a1, a2, a3 = st.columns(3)
        with a1: _line(wb("GC.DOD.TOTL.GD.ZS", 20), "Central government debt", "% GDP", R)
        with a2: _line(wb("GC.REV.XGRT.GD.ZS", 20), "Tax revenue", "% GDP", G)
        with a3: _line(wb("GC.XPN.TOTL.GD.ZS", 20), "Government expenditure", "% GDP", B)
    with tabs[3]:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            val = v("Exports", D); ar, ac, ad = trend(D, "Exports")
            card("Exports", fmt(val, "% GDP"), f"{D['Exports']['y'] or '—'}" + (f" ({ad})" if ad else ""), "g", "est", ar, ac)
        with c2:
            val = v("Imports", D); ar, ac, ad = trend(D, "Imports")
            card("Imports", fmt(val, "% GDP"), f"{D['Imports']['y'] or '—'}" + (f" ({ad})" if ad else ""), "o", "est", ar, ac)
        with c3:
            tb = (v("Exports", D) or 0) - (v("Imports", D) or 0)
            card("Net trade", fmt(tb, " pp"), "Exports − Imports as % GDP", "b")
        with c4:
            val = v("FDI inflows", D); ar, ac, ad = trend(D, "FDI inflows")
            card("FDI inflows", fmt(val, "% GDP"), f"{D['FDI inflows']['y'] or '—'}" + (f" ({ad})" if ad else ""), "p", "est", ar, ac)
        a1, a2 = st.columns(2)
        with a1:
            df = wb("NE.EXP.GNFS.ZS", 25)
            df2 = wb("NE.IMP.GNFS.ZS", 25)
            if not df.empty and not df2.empty:
                merged = df.merge(df2, on="year", suffixes=("_exp", "_imp"))
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=merged["year"], y=merged["value_exp"], name="Exports", line=dict(color=G, width=2.5), fill="tozeroy", fillcolor="rgba(45,155,117,.1)"))
                fig.add_trace(go.Scatter(x=merged["year"], y=merged["value_imp"], name="Imports", line=dict(color=O, width=2.5), fill="tozeroy", fillcolor="rgba(242,153,74,.1)"))
                fig.update_layout(title="Exports vs Imports (% GDP)", height=290, margin=dict(l=10,r=10,t=46,b=10),
                                  paper_bgcolor="#fff", plot_bgcolor="#fff", yaxis_title="% GDP", xaxis_title=None,
                                  hovermode="x unified", font=dict(size=12, color=K), legend=dict(orientation="h", y=1.12))
                fig.update_xaxes(showgrid=False); fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with a2: _line(wb("BX.KLT.DINV.WD.GD.ZS", 20), "FDI net inflows", "% GDP", P)

# ── VIEW: SECTORS ─────────────────────────────────────────────────
elif "Sectors" in view:
    heading("Sector intelligence", "Deep-dive into India's economic engines with 12-sector scoring.")
    ss = sector_detail_scores(D)
    fig = px.bar(ss, x="Score", y="Sector", orientation="h", color="Score",
                 color_continuous_scale=["#f6d4c4", O, G], text="Score")
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(height=440, margin=dict(l=10, r=35, t=10, b=10),
                      paper_bgcolor="#fff", plot_bgcolor="#fff", coloraxis_showscale=False,
                      xaxis=dict(range=[0, 110]), yaxis_title=None, font=dict(size=11, color=K))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.dataframe(ss.assign(Score=ss["Score"].round(1)), use_container_width=True, hide_index=True,
                 column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f"),
                                "Read-through": st.column_config.TextColumn("Methodology")})

    st.markdown("")
    tabs = st.tabs(["Agriculture", "Manufacturing", "Services & IT", "Banking & Finance",
                     "Healthcare", "Education", "Energy", "Digital & Telecom",
                     "Real Estate & Urban", "MSME & Entrepreneurship"])
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1: _line(wb("NV.AGR.TOTL.ZS", 25), "Agriculture share of GDP", "% GDP", G)
        with c2: _line(wb("AG.LND.AGRI.ZS", 20), "Agricultural land (% land area)", "%", G)
        _line(wb("AG.YLD.CREL.KG", 20), "Cereal yield (kg per hectare)", "kg/ha", "#8B6914")
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1: _line(wb("NV.IND.MANF.ZS", 25), "Manufacturing share of GDP", "% GDP", O)
        with c2: _line(wb("TX.VAL.TECH.MF.ZS", 20), "High-tech exports (% mfg exports)", "%", P)
        _line(wb("NV.IND.TOTL.ZS", 25), "Total industry share of GDP", "% GDP", O)
    with tabs[2]:
        c1, c2 = st.columns(2)
        with c1: _line(wb("NV.SRV.TOTL.ZS", 25), "Services share of GDP", "% GDP", B)
        with c2: _line(wb("SL.SRV.EMPL.ZS", 15), "Services employment (% total)", "%", B)
    with tabs[3]:
        c1, c2 = st.columns(2)
        with c1: _line(wb("FS.AST.PRVT.GD.ZS", 20), "Credit to private sector", "% GDP", P)
        with c2: _line(wb("FM.LBL.BMNY.GD.ZS", 20), "Broad money growth", "%", P)
        _line(wb("BX.KLT.DINV.WD.GD.ZS", 20), "FDI inflows", "% GDP", P)
    with tabs[4]:
        c1, c2, c3 = st.columns(3)
        with c1: card("Life expectancy", fmt(v("Life expectancy", D), "years"), D["Life expectancy"]["d"], "g")
        with c2: card("Infant mortality", fmt(v("Infant mortality", D), "per 1k"), D["Infant mortality"]["d"], "r" if (v("Infant mortality", D) or 0) > 30 else "g")
        with c3: card("Health spend", fmt(v("Health spend", D), "% GDP"), D["Health spend"]["d"], "b")
        a1, a2 = st.columns(2)
        with a1: _line(wb("SP.DYN.LE00.IN", 25), "Life expectancy trend", "years", G)
        with a2: _line(wb("SP.DYN.IMRT.IN", 25), "Infant mortality trend", "per 1 000", R)
        a3, a4 = st.columns(2)
        with a3: _line(wb("SH.XPD.CHEX.GD.ZS", 20), "Health expenditure (% GDP)", "% GDP", B)
        with a4: _line(wb("SH.MED.PHYS.ZS", 15), "Physicians per 1 000", "per 1 000", T)
    with tabs[5]:
        c1, c2, c3 = st.columns(3)
        with c1: card("Literacy", fmt(v("Literacy rate", D), "%"), D["Literacy rate"]["d"], "g")
        with c2: card("Secondary enrol", fmt(v("Secondary enrol", D), "%"), D["Secondary enrol"]["d"], "b")
        with c3: card("Edu spend", fmt(v("Edu spend", D), "% GDP"), D["Edu spend"]["d"], "p")
        a1, a2 = st.columns(2)
        with a1: _line(wb("SE.ADT.LITR.ZS", 15), "Adult literacy rate", "%", G)
        with a2: _line(wb("SE.SEC.ENRR", 20), "Secondary enrolment", "%", B)
        a3, a4 = st.columns(2)
        with a3: _line(wb("SE.TER.ENRR", 20), "Tertiary enrolment", "%", P)
        with a4: _line(wb("SE.XPD.TOTL.GD.ZS", 20), "Education expenditure", "% GDP", "#e67e22")
    with tabs[6]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: card("Elec access", fmt(v("Elec access", D), "%"), D["Elec access"]["d"], "g")
        with c2: card("Renewable", fmt(v("Renewable elec", D), "%"), D["Renewable elec"]["d"], G)
        with c3: card("Coal", fmt(v("Coal elec", D), "%"), D["Coal elec"]["d"], "o")
        with c4: card("Gas", fmt(v("Gas elec", D), "%"), D["Gas elec"]["d"], "b")
        # energy mix donut
        mix_data = {"Source": ["Coal", "Renewable", "Gas", "Hydro", "Nuclear", "Oil"],
                    "Share": [v("Coal elec", D), v("Renewable elec", D), v("Gas elec", D),
                              v("Hydro elec", D), v("Nuclear elec", D), v("Oil elec", D)]}
        mix_df = pd.DataFrame(mix_data).dropna()
        if not mix_df.empty:
            fig = px.pie(mix_df, values="Share", names="Source", hole=.55,
                         color_discrete_sequence=[O, G, B, T, P, R])
            fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10),
                              paper_bgcolor="#fff", font=dict(size=12, color=K),
                              legend=dict(orientation="h", y=-.05))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        a1, a2 = st.columns(2)
        with a1: _line(wb("EG.ELC.RNEW.ZS", 20), "Renewable electricity trend", "%", G)
        with a2: _line(wb("EG.ELC.COAL.ZS", 20), "Coal electricity trend", "%", O)
    with tabs[7]:
        c1, c2, c3 = st.columns(3)
        with c1: card("Internet users", fmt(v("Internet users", D), "%"), D["Internet users"]["d"], "b")
        with c2: card("Mobile subs", fmt(v("Mobile subs", D), "per 100"), D["Mobile subs"]["d"], "p")
        with c3: card("Secure internet", fmt(v("Secure internet", D), "%"), D["Secure internet"]["d"], "t")
        a1, a2 = st.columns(2)
        with a1: _line(wb("IT.NET.USER.ZS", 20), "Internet users trend", "%", B)
        with a2: _line(wb("IT.CEL.SETS.P2", 20), "Mobile subscriptions", "per 100", P)
    with tabs[8]:
        c1, c2 = st.columns(2)
        with c1:
            val = v("Urban pop", D); ar, ac, ad = trend(D, "Urban pop")
            card("Urban population", fmt(val, "%"), f"{D['Urban pop']['y'] or '—'}" + (f" ({ad})" if ad else ""), "b", "est", ar, ac)
        with c2: card("Population", fmt(v("Population", D), ""), f"{D['Population']['y'] or '—'} · Total", "n")
        _line(wb("SP.URB.TOTL.IN.ZS", 25), "Urbanisation trend", "%", B)
    with tabs[9]:
        c1, c2 = st.columns(2)
        with c1: card("Credit to private", fmt(v("Credit private", D), "% GDP"), D["Credit private"]["d"], "p")
        with c2: card("Broad money growth", fmt(v("Broad money", D), "%"), D["Broad money"]["d"], "p")
        a1, a2 = st.columns(2)
        with a1: _line(wb("FS.AST.PRVT.GD.ZS", 20), "Private sector credit", "% GDP", P)
        with a2: _line(wb("FM.LBL.BMNY.GD.ZS", 20), "Broad money growth", "%", P)

# ── VIEW: PEOPLE ──────────────────────────────────────────────────
elif "People" in view:
    heading("People & demographics", "Population structure, health outcomes, education access, and social indicators.")
    tabs = st.tabs(["Demographics", "Health", "Education"])
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: card("Population", fmt(v("Population", D), ""), f"{D['Population']['y'] or '—'}", "n")
        with c2: card("Age 0-14", fmt(v("Age 0-14", D), "%"), D["Age 0-14"]["d"], "o")
        with c3: card("Age 15-64", fmt(v("Age 15-64", D), "%"), D["Age 15-64"]["d"], "g")
        with c4: card("Age 65+", fmt(v("Age 65+", D), "%"), D["Age 65+"]["d"], "b")
        c5, c6 = st.columns(2)
        with c5:
            val = v("Fertility", D); ar, ac, ad = trend(D, "Fertility", True)
            card("Fertility rate", fmt(val, ""), f"{D['Fertility']['y'] or '—'} · Births/woman" + (f" ({ad})" if ad else ""), "p", "est", ar, ac)
        with c6:
            card("Urban pop", fmt(v("Urban pop", D), "%"), D["Urban pop"]["d"], "b")
        # age structure bar
        age_df = pd.DataFrame({"Group": ["Age 0-14", "Age 15-64", "Age 65+"],
                               "Share": [v("Age 0-14", D), v("Age 15-64", D), v("Age 65+", D)]}).dropna()
        if not age_df.empty:
            fig = px.bar(age_df, x="Share", y="Group", orientation="h", text="Share",
                         color="Group", color_discrete_map={"Age 0-14": O, "Age 15-64": G, "Age 65+": B})
            fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
            fig.update_layout(height=220, margin=dict(l=5, r=30, t=10, b=5),
                              paper_bgcolor="#fff", plot_bgcolor="#fff", showlegend=False,
                              xaxis_title="% of population", yaxis_title=None, font=dict(size=12, color=K))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        a1, a2 = st.columns(2)
        with a1: _line(wb("SP.POP.TOTL", 25), "Population trend", "Billions", N)
        with a2: _line(wb("SP.URB.TOTL.IN.ZS", 25), "Urbanisation trend", "%", B)
        a3, a4 = st.columns(2)
        with a3: _line(wb("SP.DYN.TFRT.IN", 25), "Fertility rate trend", "Births/woman", P)
        with a4: _line(wb("SP.DYN.CBRT.IN", 20), "Birth rate", "per 1 000", G)
    with tabs[1]:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: card("Life expectancy", fmt(v("Life expectancy", D), "years"), D["Life expectancy"]["d"], "g")
        with c2: card("Infant mortality", fmt(v("Infant mortality", D), "per 1k"), D["Infant mortality"]["d"], "r" if (v("Infant mortality", D) or 0) > 30 else "g")
        with c3: card("Health spend", fmt(v("Health spend", D), "% GDP"), D["Health spend"]["d"], "b")
        with c4: card("Physicians", fmt(v("Physicians", D), "per 1k"), D["Physicians"]["d"], "t")
        with c5: card("Hospital beds", fmt(v("Hospital beds", D), "per 1k"), D["Hospital beds"]["d"], "p")
        a1, a2 = st.columns(2)
        with a1: _line(wb("SP.DYN.LE00.IN", 25), "Life expectancy", "years", G, 300)
        with a2: _line(wb("SP.DYN.IMRT.IN", 25), "Infant mortality", "per 1 000", R, 300)
        a3, a4 = st.columns(2)
        with a3: _line(wb("SH.XPD.CHEX.GD.ZS", 20), "Health expenditure", "% GDP", B)
        with a4: _line(wb("SP.DYN.CDRT.IN", 20), "Death rate", "per 1 000", M)
    with tabs[2]:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: card("Literacy", fmt(v("Literacy rate", D), "%"), D["Literacy rate"]["d"], "g")
        with c2: card("Primary enrol", fmt(v("Primary enrol", D), "%"), D["Primary enrol"]["d"], "o")
        with c3: card("Secondary enrol", fmt(v("Secondary enrol", D), "%"), D["Secondary enrol"]["d"], "b")
        with c4: card("Tertiary enrol", fmt(v("Tertiary enrol", D), "%"), D["Tertiary enrol"]["d"], "p")
        with c5: card("Edu spend", fmt(v("Edu spend", D), "% GDP"), D["Edu spend"]["d"], "#e67e22")
        a1, a2 = st.columns(2)
        with a1:
            df = wb("SE.PRM.ENRR", 20)
            df2 = wb("SE.SEC.ENRR", 20)
            df3 = wb("SE.TER.ENRR", 20)
            if not df.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df["year"], y=df["value"], name="Primary", line=dict(color=O, width=2.5)))
                if not df2.empty: fig.add_trace(go.Scatter(x=df2["year"], y=df2["value"], name="Secondary", line=dict(color=B, width=2.5)))
                if not df3.empty: fig.add_trace(go.Scatter(x=df3["year"], y=df3["value"], name="Tertiary", line=dict(color=P, width=2.5)))
                fig.update_layout(title="Enrolment rates comparison", height=290, margin=dict(l=10,r=10,t=46,b=10),
                                  paper_bgcolor="#fff", plot_bgcolor="#fff", yaxis_title="%", xaxis_title=None,
                                  hovermode="x unified", font=dict(size=12, color=K),
                                  legend=dict(orientation="h", y=1.12))
                fig.update_xaxes(showgrid=False); fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with a2: _line(wb("SE.ADT.LITR.ZS", 15), "Adult literacy rate", "%", G)
        _line(wb("SE.XPD.TOTL.GD.ZS", 20), "Education expenditure", "% GDP", "#e67e22")

# ── VIEW: INFRASTRUCTURE ──────────────────────────────────────────
elif "Infrastructure" in view:
    heading("Infrastructure & environment", "Energy mix, digital reach, transport networks, and environmental indicators.")
    tabs = st.tabs(["Energy", "Digital", "Transport", "Environment"])
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: card("Elec access", fmt(v("Elec access", D), "%"), D["Elec access"]["d"], "g")
        with c2: card("Renewable", fmt(v("Renewable elec", D), "%"), D["Renewable elec"]["d"], G)
        with c3: card("Coal", fmt(v("Coal elec", D), "%"), D["Coal elec"]["d"], "o")
        with c4: card("Gas", fmt(v("Gas elec", D), "%"), D["Gas elec"]["d"], "b")
        mix_data = {"Source": ["Coal", "Renewable", "Gas", "Hydro", "Nuclear", "Oil"],
                    "Share": [v("Coal elec", D), v("Renewable elec", D), v("Gas elec", D),
                              v("Hydro elec", D), v("Nuclear elec", D), v("Oil elec", D)]}
        mix_df = pd.DataFrame(mix_data).dropna()
        if not mix_df.empty:
            fig = px.pie(mix_df, values="Share", names="Source", hole=.55,
                         color_discrete_sequence=[O, G, B, T, P, R])
            fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10),
                              paper_bgcolor="#fff", font=dict(size=12, color=K),
                              legend=dict(orientation="h", y=-.05))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        a1, a2 = st.columns(2)
        with a1: _line(wb("EG.ELC.RNEW.ZS", 20), "Renewable electricity", "%", G)
        with a2: _line(wb("EG.ELC.COAL.ZS", 20), "Coal electricity", "%", O)
        a3, a4 = st.columns(2)
        with a3: _line(wb("EG.ELC.ACCS.ZS", 20), "Electricity access", "%", G)
        with a4: _line(wb("EG.USE.COMM.GD.PP.KD", 20), "Energy intensity", "MJ per $ PPP", T)
    with tabs[1]:
        c1, c2, c3 = st.columns(3)
        with c1: card("Internet users", fmt(v("Internet users", D), "%"), D["Internet users"]["d"], "b")
        with c2: card("Mobile subs", fmt(v("Mobile subs", D), "per 100"), D["Mobile subs"]["d"], "p")
        with c3: card("Secure servers", fmt(v("Secure internet", D), "%"), D["Secure internet"]["d"], "t")
        a1, a2 = st.columns(2)
        with a1: _line(wb("IT.NET.USER.ZS", 20), "Internet penetration", "%", B)
        with a2: _line(wb("IT.CEL.SETS.P2", 20), "Mobile subscriptions", "per 100", P)
    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        with c1: card("Rail lines", fmt(v("Rail lines", D), "km"), D["Rail lines"]["d"], "n")
        with c2: card("Air passengers", fmt(v("Air passengers", D), ""), D["Air passengers"]["d"], "b")
        with c3: card("Container traffic", fmt(v("Ports traffic", D), "TEU"), D["Ports traffic"]["d"], "o")
        a1, a2 = st.columns(2)
        with a1: _line(wb("IS.RRS.TOTL.KM", 15), "Railway lines", "km", N)
        with a2: _line(wb("IS.AIR.PSGR", 20), "Air passengers", "Passengers", B)
    with tabs[3]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: card("CO₂ per capita", fmt(v("CO2 per cap", D), "t"), D["CO2 per cap"]["d"], "r" if (v("CO2 per cap", D) or 0) > 2 else "g")
        with c2: card("CO₂ total", fmt(v("CO2 total", D), "kt"), D["CO2 total"]["d"], "o")
        with c3: card("Forest area", fmt(v("Forest area", D), "% land"), D["Forest area"]["d"], G)
        with c4: card("Freshwater use", fmt(v("Freshwater use", D), "%"), D["Freshwater use"]["d"], "b")
        a1, a2 = st.columns(2)
        with a1: _area(wb("EN.ATM.CO2E.KT", 25), "Total CO₂ emissions", "Kilotonnes", R)
        with a2: _line(wb("EN.ATM.CO2E.PC", 25), "CO₂ per capita", "Tonnes", O)
        a3, a4 = st.columns(2)
        with a3: _line(wb("AG.LND.FRST.ZS", 20), "Forest area", "% land area", G)
        with a4: _line(wb("ER.H2O.FWTL.ZS", 15), "Freshwater withdrawal", "% internal resources", B)

# ── VIEW: MARKETS & CLIMATE ───────────────────────────────────────
elif "Markets" in view:
    heading("Markets & climate", "Real-time market context and Delhi climate snapshot. Market data is indicative; climate is a single-point reference.")
    sensex_df = yahoo("^BSESN")
    nifty_df = yahoo("^NSEI")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if not sensex_df.empty:
            cur = float(sensex_df.iloc[-1]["close"])
            prv = float(sensex_df.iloc[-2]["close"]) if len(sensex_df) > 1 else cur
            chg = ((cur / prv) - 1) * 100
            card("Sensex", f"{cur:,.0f}", f"{chg:+.2f}% vs prior close", "o",
                 "live", "↑" if chg > 0 else "↓", G if chg > 0 else R)
        else: card("Sensex", "—", "Feed unavailable", "o")
    with c2:
        if not nifty_df.empty:
            cur = float(nifty_df.iloc[-1]["close"])
            prv = float(nifty_df.iloc[-2]["close"]) if len(nifty_df) > 1 else cur
            chg = ((cur / prv) - 1) * 100
            card("Nifty 50", f"{cur:,.0f}", f"{chg:+.2f}% vs prior close", "b",
                 "live", "↑" if chg > 0 else "↓", G if chg > 0 else R)
        else: card("Nifty 50", "—", "Feed unavailable", "b")
    w = weather()
    a = aqi_data = aqi()
    with c3:
        if w:
            card("Delhi temp", f"{w['temperature_2m']:.1f}°C",
                 f"Humidity {w['relative_humidity_2m']}% · Wind {w['wind_speed_10m']:.0f} km/h", "t", "live")
        else: card("Delhi temp", "—", "Weather unavailable", "t")
    with c4:
        if aqi_data:
            aq = aqi_data.get("us_aqi", aqi_data.get("indian_aqi", 0))
            pm25 = aqi_data.get("pm2_5", 0)
            pm10 = aqi_data.get("pm10", 0)
            label = "Good" if aq < 50 else "Moderate" if aq < 100 else "Unhealthy" if aq < 150 else "Very Unhealthy"
            card("Delhi AQI", f"{aq:.0f}", f"{label} · PM2.5 {pm25:.1f} · PM10 {pm10:.1f}",
                 "r" if aq > 100 else "o" if aq > 50 else "g", "live")
        else: card("Delhi AQI", "—", "AQI feed unavailable", "t")

    a1, a2 = st.columns(2)
    with a1:
        if not sensex_df.empty:
            fig = px.area(sensex_df, x="date", y="close", title="Sensex · trailing year")
            fig.update_traces(line=dict(color=O, width=2), fillcolor="rgba(242,153,74,.12)")
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=46, b=10),
                              paper_bgcolor="#fff", plot_bgcolor="#fff", yaxis_title=None, xaxis_title=None,
                              hovermode="x unified", font=dict(size=12, color=K))
            fig.update_xaxes(showgrid=False, linecolor="#e0e5ea")
            fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5", linecolor="#e0e5ea")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with a2:
        if not nifty_df.empty:
            fig = px.area(nifty_df, x="date", y="close", title="Nifty 50 · trailing year")
            fig.update_traces(line=dict(color=B, width=2), fillcolor="rgba(61,127,166,.12)")
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=46, b=10),
                              paper_bgcolor="#fff", plot_bgcolor="#fff", yaxis_title=None, xaxis_title=None,
                              hovermode="x unified", font=dict(size=12, color=K))
            fig.update_xaxes(showgrid=False, linecolor="#e0e5ea")
            fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5", linecolor="#e0e5ea")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # market comparison
    if not sensex_df.empty and not nifty_df.empty:
        merged = sensex_df.merge(nifty_df, on="date", suffixes=("_sensex", "_nifty"))
        if not merged.empty:
            merged["sensex_norm"] = (merged["close_sensex"] / merged["close_sensex"].iloc[0]) * 100
            merged["nifty_norm"] = (merged["close_nifty"] / merged["close_nifty"].iloc[0]) * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=merged["date"], y=merged["sensex_norm"], name="Sensex (normalised)",
                                     line=dict(color=O, width=2.5)))
            fig.add_trace(go.Scatter(x=merged["date"], y=merged["nifty_norm"], name="Nifty 50 (normalised)",
                                     line=dict(color=B, width=2.5)))
            fig.update_layout(title="Sensex vs Nifty 50 · normalised to 100", height=280,
                              margin=dict(l=10, r=10, t=46, b=10),
                              paper_bgcolor="#fff", plot_bgcolor="#fff", yaxis_title="Index (base=100)",
                              xaxis_title=None, hovermode="x unified", font=dict(size=12, color=K),
                              legend=dict(orientation="h", y=1.12))
            fig.update_xaxes(showgrid=False); fig.update_yaxes(showgrid=True, gridcolor="#f0f2f5")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""<div class="ibox">
    <strong>📍 Climate note:</strong> Weather and air quality readings are for New Delhi (28.6°N, 77.2°E), used as a transparent
    single-point reference. This is a <em>country</em> monitor, not a city weather app. Data from Open-Meteo (weather + AQI),
    refreshed every 10 minutes independently of the macro cache.
    </div>""", unsafe_allow_html=True)

# ── VIEW: SOURCES & METHODS ───────────────────────────────────────
elif "Methods" in view:
    heading("Sources & methods", "Full transparency on every data point, calculation, and limitation.")
    st.markdown("### 📡 Source health")
    src = [
        ("World Bank Indicators API v2", "40+ macro, sectoral, social, infra, environmental series", "Connected" if D else "Unreachable"),
        ("Yahoo Finance v8 chart", "Sensex (^BSESN) & Nifty 50 (^NSEI) daily close", "Connected" if not yahoo("^BSESN").empty else "Unavailable"),
        ("Open-Meteo Forecast", "Delhi temperature, humidity, wind", "Connected" if weather() else "Unavailable"),
        ("Open-Meteo Air Quality", "Delhi PM2.5, PM10, US AQI, Indian AQI", "Connected" if aqi() else "Unavailable"),
        ("Google News RSS", "India business/policy/tech headlines", "Connected" if headlines() else "Unavailable"),
    ]
    st.dataframe(pd.DataFrame(src, columns=["Source", "Coverage", "Status"]),
                 use_container_width=True, hide_index=True)

    st.markdown("### 📊 Indicator registry (40+ series)")
    reg = [(n, IND[n][0], IND[n][1], IND[n][2],
            f"{D[n]['y']}" if D[n]["v"] is not None else "—",
            fmt(D[n]["v"], D[n]["u"]) if D[n]["v"] is not None else "—")
           for n in IND]
    st.dataframe(pd.DataFrame(reg, columns=["Name", "WB Code", "Unit", "Definition", "Year", "Value"]),
                 use_container_width=True, hide_index=True, height=800)

    st.markdown("### 🧮 Calculation glossary")
    st.markdown("""
**Overall India Score** = Economic Health × 0.30 + Social Development × 0.25 + Infrastructure × 0.20 + Environment × 0.10 + Trade & Finance × 0.10 + Fiscal Health × 0.05

**Economic Health** = GDP growth (norm, ×.30) + Inflation inverse (×.25) + Unemployment inverse (×.20) + Debt inverse (×.15) + Tax revenue (×.10)

**Social Development** = Life expectancy (×.25) + Infant mortality inverse (×.20) + Health spend (×.15) + Secondary enrolment (×.15) + Literacy (×.15) + Tertiary enrolment (×.10)

**Infrastructure** = Electricity access (×.25) + Internet users (×.25) + Mobile subs (×.15) + Renewable elec (×.20) + Urban pop (×.15)

**Environment** = CO₂ per capita inverse (×.30) + Forest area (×.25) + Renewable elec (×.25) + Coal elec inverse (×.20)

**Trade & Finance** = Exports (×.30) + FDI (×.30) + High-tech exports (×.20) + Credit to private sector (×.20)

**Fiscal Health** = Debt inverse (×.35) + Tax revenue (×.35) + Govt spending (×.30)

**Normalisation** = clamp((value − low) / (high − low), 0, 1) × 100. Inverse flips the direction (lower is better).

**Sector scores** = each of the 12 sectors has a bespoke weighted formula using 2–5 input indicators (see the "Read-through" column on the Sectors page).

**Net trade** = Exports % GDP − Imports % GDP. This is a structural openness measure, not the merchandise trade balance.

**Trend arrows** = difference between the two most recent World Bank observations. Direction is flipped (inverted) for indicators where decline is positive (inflation, unemployment, infant mortality, fertility, CO₂, coal share, government debt).
""")

    st.markdown("### ⚠️ Caveats")
    st.warning("""
• This dashboard is for **public-information analysis and education only**. It is NOT financial, policy, medical, or investment advice.

• World Bank observations typically lag the current calendar year by 1–2 years. The displayed year is part of the value, not an approximation.

• Yahoo Finance data may be delayed or rate-limited. Treat market charts as **indicative**, not tradeable.

• Climate readings are **Delhi-only** single-point observations — they do not represent India as a whole.

• Some sectors (Defence, Tourism, Real Estate) have limited World Bank coverage and use partial or baseline scores. These are clearly labelled.

• All composite scores are transparent, reproducible blends — not machine-learning forecasts or proprietary indices.

• Upstream services can revise historical data, rate-limit requests, or experience outages at any time.
""")

    st.markdown(f"""<div class="src-line">
    Built as a single <code>app.py</code> · 40+ World Bank indicators · Yahoo Finance · Open-Meteo · Google News RSS ·
    Cached refreshes (TTL 5–30 min) to respect upstream rate limits ·
    Last full refresh: {now_str}
    </div>""", unsafe_allow_html=True)

# ── footer ────────────────────────────────────────────────────────
st.markdown(f"""<div class="src-line" style="text-align:center;margin-top:2rem">
🇮🇳 India Monitor · Public-data country intelligence · {now_str} ·
Built with Streamlit, Plotly, World Bank, Yahoo Finance, Open-Meteo
</div>""", unsafe_allow_html=True)