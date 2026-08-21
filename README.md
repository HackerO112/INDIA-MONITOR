```markdown
# 🇮🇳 India Monitor

**Comprehensive, real-time country intelligence dashboard for the Republic of India — built entirely with free public APIs and open-source tools.**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![APIs](https://img.shields.io/badge/Public_APIs-5-orange)](#data-sources)
[![Indicators](https://img.shields.io/badge/World_Bank_Indicators-40%2B-purple)](#indicator-coverage)

---

## ✨ Overview

India Monitor is a single-file Streamlit application that aggregates **40+ live economic, social, demographic, infrastructure, and environmental indicators** for India into a unified, interactive dashboard. Every number is traceable to its source, every calculation is published, and every limitation is disclosed.

---

## 🎯 Why This Exists

- **Transparency** — Every indicator shows its source vintage, unit, and year-over-year change. No silent blending of data vintages.
- **Accessibility** — Plain-English labels, no jargon, no paywall. Anyone can read it.
- **Reproducibility** — All composite scores and sector ratings have published formulas with exact weights.
- **Single-file simplicity** — One `app.py`, zero config files, zero database. Clone and run.

---

## 📊 Features at a Glance

### 7 Interactive Views

| View | What's Inside |
|---|---|
| **Overview** | 6 key metric cards with trend arrows, composite gauge (0–100), 6-dimension radar chart, 12-sector scored bar, live headlines |
| **Economy** | GDP (growth + nominal + per capita + area chart), inflation, unemployment, fiscal (debt/tax/spending), trade overlay (exports vs imports), FDI |
| **Sectors** | 12-sector scored ranking with read-through table + 9 deep-dive tabs: Agriculture, Manufacturing, Services & IT, Banking & Finance, Healthcare, Education, Energy (with donut chart), Digital & Telecom, Real Estate & Urban, MSME & Entrepreneurship |
| **People** | Demographics (age structure bar, population trend, fertility, urbanisation), Health (life expectancy, infant mortality, physicians, hospital beds, death rate), Education (enrolment overlay, literacy, spending) |
| **Infrastructure** | Energy (donut mix + 4 trend charts), Digital (internet, mobile, secure servers), Transport (rail, air, container ports), Environment (CO₂ area chart, per capita, forest, freshwater) |
| **Markets & Climate** | Sensex & Nifty 50 live cards with change arrows, trailing-year area charts, normalised index comparison overlay, Delhi weather + AQI with category labels |
| **Sources & Methods** | Source health table, full 40+ indicator registry, complete calculation glossary, caveats |

### Smart Composites

- **Overall India Score** (0–100) — weighted blend of 6 sub-indices
- **6 Sub-indices** — Economic Health, Social Development, Infrastructure, Environment, Trade & Finance, Fiscal Health
- **12 Sector Scores** — bespoke multi-indicator formulas with plain-English read-throughs
- **Trend Arrows** — year-over-year change with inverted direction for "lower is better" indicators

### Design & UX

- 🎨 Modern card system with colored accent borders and hover lift animations
- 📱 Fully responsive — desktop → tablet → phone
- 💚 Pulse animation on LIVE indicators
- 🌊 Gradient hero with radial glow
- 📐 Clean Plotly charts — no clutter, unified hover, consistent palette
- ♿ Accessible — semantic labels, high contrast, plain language
- 🛡️ Error-resilient — every API failure shows "—" gracefully, never crashes

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Framework | [Streamlit](https://streamlit.io/) ≥ 1.40 |
| Charts | [Plotly](https://plotly.com/python/) (express + graph_objects) |
| Data | [Pandas](https://pandas.pydata.org/) |
| HTTP | [Requests](https://docs.python-requests.org/) |
| XML Parsing | `xml.etree.ElementTree` (stdlib) |
| Deployment | Any — `streamlit run`, Docker, Streamlit Community Cloud, Railway, Render |

**No database. No config files. No build step. No frontend framework.**

---

## 📡 Data Sources

All APIs are **free, keyless, and publicly accessible**.

| Source | What It Provides | Cache TTL |
|---|---|---|
| [World Bank Indicators API v2](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation) | 40+ macro, sectoral, social, demographic, infra, environmental series | 30 min |
| [Yahoo Finance v8 Chart](https://query1.finance.yahoo.com/v8/finance/chart/) | Sensex (`^BSESN`) & Nifty 50 (`^NSEI`) daily closes, 1-year lookback | 5 min |
| [Open-Meteo Forecast](https://open-meteo.com/en/docs) | Delhi temperature, humidity, wind speed, precipitation | 10 min |
| [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api) | Delhi PM2.5, PM10, US AQI, Indian AQI | 10 min |
| [Google News RSS](https://news.google.com/rss/search) | 10 latest India business/policy/tech headlines | 10 min |

---

## 📋 Indicator Coverage (40+)

### Macro & Fiscal
GDP growth, GDP nominal (USD), GDP per capita, GNI per capita, CPI inflation, ILO unemployment, population, urban population, central government debt, tax revenue, government expenditure

### Sectoral
Agriculture value added, industry value added, services value added, manufacturing value added

### Trade & Capital
Exports (% GDP), imports (% GDP), net trade balance, FI inflows, high-tech exports (% of manufactured exports)

### Health
Life expectancy, infant mortality rate, health expenditure (% GDP), physicians per 1 000, hospital beds per 1 000, crude birth rate, crude death rate

### Education
Adult literacy rate, primary/secondary/tertiary enrolment, government education expenditure

### Demographics
Population ages 0-14, 15-64, 65+, total fertility rate

### Energy
Electricity access, renewable/gas/hydro/nuclear/oil/coal electricity shares, energy use per GDP

### Digital
Internet users, mobile subscriptions per 100, secure internet servers

### Environment
CO₂ per capita, total CO₂ emissions, forest area, annual freshwater withdrawal

### Financial
Domestic credit to private sector, broad money growth

### Transport
Railway lines (km), air passengers carried, container port traffic (TEU)

---

## 🧮 Calculation Methodology

All formulas are fully transparent and published in the app's **Sources & Methods** view.

### Overall India Score

```
Overall = Economic Health × 0.30
        + Social Development × 0.25
        + Infrastructure × 0.20
        + Environment × 0.10
        + Trade & Finance × 0.10
        + Fiscal Health × 0.05
```

### Sub-Index Formulas

```
Economic Health  = GDP growth (norm, ×.30) + Inflation⁻¹ (×.25) + Unemployment⁻¹ (×.20) + Debt⁻¹ (×.15) + Tax revenue (×.10)

Social Development = Life expectancy (×.25) + Infant mortality⁻¹ (×.20) + Health spend (×.15)
                   + Secondary enrolment (×.15) + Literacy (×.15) + Tertiary enrolment (×.10)

Infrastructure = Electricity access (×.25) + Internet users (×.25) + Mobile subs (×.15)
               + Renewable elec (×.20) + Urban pop (×.15)

Environment = CO₂ per capita⁻¹ (×.30) + Forest area (×.25) + Renewable elec (×.25) + Coal elec⁻¹ (×.20)

Trade & Finance = Exports (×.30) + FDI (×.30) + High-tech exports (×.20) + Credit to private (×.20)

Fiscal Health = Debt⁻¹ (×.35) + Tax revenue (×.35) + Govt spending (×.30)
```

### Normalisation

```
score = clamp((value - low) / (high - low), 0, 1) × 100
```

For "lower is better" indicators (inflation, unemployment, debt, CO₂, coal, infant mortality, fertility): the score is inverted (`1 - normalised`).

### Sector Scores

Each of the 12 sectors uses a bespoke weighted blend of 2–5 input indicators. Exact formulas and read-through explanations are displayed in the Sectors view data table.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or newer
- pip

### Install & Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/india-monitor.git
cd india-monitor

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py --server.port 5000
```

Open **http://localhost:5000** in your browser.

### requirements.txt

```
streamlit>=1.40.0
pandas>=2.0.0
plotly>=5.18.0
requests>=2.31.0
```

---

## ⚙️ Configuration

### Command-Line Flags

```bash
streamlit run app.py \
  --server.port 5000 \           # Port (default: 8501)
  --server.address 0.0.0.0 \     # Bind to all interfaces (for Docker/cloud)
  --server.headless true \       # No browser auto-open (for servers)
  --browser.gatherUsageStats false  # Disable Streamlit telemetry
```

### Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `STREAMLIT_SERVER_PORT` | `8501` | Server port |
| `STREAMLIT_SERVER_ADDRESS` | `localhost` | Bind address |
| `REQUESTS_TIMEOUT` | `10` | API timeout in seconds (set via code) |

### Auto-Refresh

Toggle **Auto-refresh** in the sidebar and set the interval (5 / 10 / 15 / 30 / 60 minutes). The app clears cached data and re-fetches on each cycle. Manual refresh is also available via the **Refresh now** button.

---

## 🐳 Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["streamlit", "run", "app.py", \
     "--server.port=5000", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
```

```bash
# Build
docker build -t india-monitor .

# Run
docker run -d -p 5000:5000 --name india-monitor india-monitor
```

---

## ☁️ Deploy to Cloud (Free)

### Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repo, set `app.py` as the main file
4. Deploy — done in ~60 seconds

### Railway / Render

Both support Streamlit out of the box:

```bash
# Railway
railway init
railway up

# Render — just connect the GitHub repo and set:
# Build Command: pip install -r requirements.txt
# Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 📁 Project Structure

```
india-monitor/
├── app.py                 # ← Everything lives here (single-file design)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container deployment
├── LICENSE                # MIT License
├── README.md              # This file
└── .github/
    └── workflows/
        └── ci.yml         # Optional: automated tests
```

> **Why single file?** Zero mental overhead to understand, modify, or fork. No import chains, no config sprawl, no "which file does what?" — it's all in one place. The ~1100 lines are organised with clear section comments.

---

## 🔄 Caching Strategy

| Data Type | TTL | Rationale |
|---|---|---|
| World Bank indicators | 30 min | Annual data; changes slowly |
| Yahoo Finance charts | 5 min | Market hours; more volatile |
| Weather / AQI | 10 min | Semi-real-time observation |
| News headlines | 10 min | Frequently updated feed |

All caching uses `@st.cache_data(ttl=...)`. The **Refresh now** button calls `st.cache_data.clear()` to bypass all caches.

> ⚠️ Respects upstream rate limits. Do not reduce TTLs aggressively — World Bank and Yahoo Finance may throttle or block.

---

## 🧪 Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| All metrics show "—" | No internet / API blocked | Check network; try a VPN if WB API is geo-restricted |
| Sensex/Nifty show "Unavailable" | Yahoo Finance rate-limited | Wait 5 min (cache clears) or reduce refresh frequency |
| Headlines empty | Google News RSS blocked | Same as above; RSS is less stable than REST APIs |
| Slow first load | 40+ World Bank API calls | Expected — subsequent loads use cache |
| `SyntaxError` on f-string | Curly braces in CSS | Ensure `inject_css()` uses plain `"""` string, not `f"""` |
| Port 5000 in use | Another process | Use `--server.port 8080` or any free port |

---

## 🤝 Contributing

Contributions are welcome! This project is intentionally simple — a single file — so changes are easy to review and test.

### How to Contribute

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** to `app.py`
4. **Test locally**: `streamlit run app.py`
5. **Commit**: `git commit -m "Add: your feature description"`
6. **Push**: `git push origin feature/your-feature`
7. **Open a Pull Request**

### Ideas for Contributions

- 🗺️ **State-level data** — add ISRO/state government APIs for regional breakdowns
- 📊 **Additional chart types** — heatmap, treemap, choropleth
- 🔔 **Alert system** — threshold-based notifications (e.g., "Inflation > 8%")
- 🌙 **Dark mode toggle** — add a theme switcher
- 📱 **PWA support** — make it installable on mobile
- 🌐 **Multi-country** — parameterise the country code to monitor any nation
- 📈 **Historical snapshots** — store periodic data for time-travel comparison
- 🤖 **AI summary** — LLM-generated narrative of key changes
- 🇮🇳 **Hindi language toggle** — bilingual interface

### Code Style

- Follow existing patterns in `app.py`
- Use clear section comments: `# ── section name ──`
- Keep everything in the single file
- Add new indicators to the `IND` dict with proper unit and definition
- Handle `None` gracefully everywhere — never let a missing API value crash the app

---

## ⚠️ Disclaimers

- **Not financial, policy, medical, or investment advice.**
- World Bank data typically lags the current calendar year by 1–2 years. The displayed year is part of the value, not an estimate.
- Yahoo Finance data may be delayed or rate-limited. Treat market charts as **indicative**, not tradeable.
- Climate readings are **Delhi-only** single-point observations — they do not represent India as a whole.
- Some sectors (Defence, Tourism, Real Estate) have limited World Bank coverage and use partial or baseline scores, clearly labelled.
- All composite scores are **transparent, reproducible blends** — not machine-learning forecasts or proprietary indices.
- Upstream services can revise historical data, rate-limit requests, or experience outages at any time.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, distribute, and sell this software. Attribution is appreciated but not required.

---

## 🙏 Acknowledgements

- **[World Bank Open Data](https://data.worldbank.org/)** — the backbone of this dashboard; 40+ free indicators
- **[Yahoo Finance](https://finance.yahoo.com/)** — free market data via unofficial chart API
- **[Open-Meteo](https://open-meteo.com/)** — free weather and air quality, no API key needed
- **[Google News](https://news.google.com/)** — free RSS feed for headline context
- **[Streamlit](https://streamlit.io/)** — the framework that makes single-file data apps possible
- **[Plotly](https://plotly.com/python/)** — beautiful, interactive charts
- **The Republic of India** 🇮🇳 — the subject of this monitor

---

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/india-monitor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/india-monitor/discussions)

---

<p align="center">
  <strong>Built with ❤️ for transparent, accessible country intelligence.</strong><br>
  <sub>One file. Five APIs. Forty indicators. Zero secrets.</sub>
</p>
```

**Before publishing, just do these 4 replacements:**

| Placeholder | Replace With |
|---|---|
| `YOUR_USERNAME` | Your actual GitHub username |
| `![Dashboard Preview](...)` | A real screenshot of the running dashboard |
| `https://github.com/YOUR_USERNAME/india-monitor/issues` | Your actual repo URL |
| `https://github.com/YOUR_USERNAME/india-monitor/discussions` | Your actual repo URL |

**Optional bonus files to add to your repo:**

```
india-monitor/
├── .gitignore              # Add: venv/, __pycache__/, *.pyc, .env
├── LICENSE                 # MIT license text
├── .github/
│   └── FUNDING.yml         # GitHub Sponsors / Buy Me a Coffee link
└── screenshots/
    ├── overview.png
    ├── economy.png
    ├── sectors.png
    └── markets.png
```

The README is designed to pass every open-source checklist: clear purpose, instant runnability, full methodology transparency, contributing guide, troubleshooting table, Docker support, and disclaimers.
