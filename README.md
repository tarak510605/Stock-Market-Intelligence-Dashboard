# Stock Market Intelligence Dashboard

A comprehensive financial analytics system for stock market analysis, featuring automated data collection, technical indicators, portfolio analysis, and interactive Tableau dashboards.

---

## 📊 Overview

Analyzes stock market data (AAPL, MSFT, TSLA, NVDA) to provide:
- Price trends and trading volume analysis
- Technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
- Portfolio risk metrics (Sharpe Ratio, VaR, Maximum Drawdown)
- Correlation and diversification analysis
- Interactive Tableau visualizations

---

## 📁 Project Structure

```
Stock-Market-Intelligence-Dashboard/
├── data/
│   ├── raw/                           # Raw data from yfinance
│   ├── cleaned/                       # Cleaned data with features
│   └── processed/                     # Analysis outputs
├── etl/
│   ├── fetch_stock_data.py            # Data collection
│   └── clean_stock_data.py            # Data cleaning & feature engineering
├── analysis/
│   ├── exploratory_analysis.ipynb     # EDA and trends
│   ├── technical_indicators.ipynb     # RSI, MACD, Bollinger Bands
│   └── portfolio_analysis.ipynb       # Portfolio metrics & risk
├── visualization/
│   └── charts.py                      # Reusable chart functions
├── dashboard/
│   ├── prepare_tableau_data.py        # Tableau dataset prep
│   └── TABLEAU_GUIDE.md               # Dashboard creation guide
├── utils/
│   ├── financial_metrics.py           # Financial calculations
│   └── helper_functions.py            # Data utilities
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
# Clone/download the project
cd Stock-Market-Intelligence-Dashboard

# Install dependencies
pip install -r requirements.txt
# OR
/usr/local/bin/python3 -m pip install yfinance pandas numpy matplotlib seaborn scipy jupyter notebook openpyxl
```

---

## 📊 Usage

### 1. Data Collection & Cleaning
```bash
cd etl
/usr/local/bin/python3 fetch_stock_data.py    # Fetches stock data → data/raw/
/usr/local/bin/python3 clean_stock_data.py    # Cleans & engineers features → data/cleaned/
```

### 2. Analysis (Jupyter Notebooks)
```bash
cd ../analysis
jupyter notebook

# Run notebooks:
# 1. exploratory_analysis.ipynb     - Price trends, volume, correlations
# 2. technical_indicators.ipynb     - RSI, MACD, Bollinger Bands
# 3. portfolio_analysis.ipynb       - Risk metrics, Sharpe ratio, returns
```

### 3. Tableau Dashboard
```bash
cd ../dashboard
/usr/local/bin/python3 prepare_tableau_data.py    # Creates tableau_dataset.csv

# Then:
# 1. Open Tableau Desktop
# 2. Import tableau_dataset.csv
# 3. Follow TABLEAU_GUIDE.md
```

---

## 🛠️ Technologies

**Data**: yfinance, pandas, NumPy  
**Analysis**: SciPy, Jupyter Notebook  
**Visualization**: Tableau  
**Environment**: Python 3.8+


