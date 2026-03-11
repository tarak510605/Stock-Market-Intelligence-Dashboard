# Quick Start Guide
## Stock Market Intelligence Dashboard

**Get up and running in 5 minutes!**

---

## 🚀 Fast Setup

### 1. Install Dependencies (1 minute)

```bash
# Navigate to project folder
cd Stock-Market-Intelligence-Dashboard

# Install packages
pip install -r requirements.txt
```

---

### 2. Collect Data (2 minutes)

```bash
# Run data collection
cd etl
python fetch_stock_data.py
```

**What happens**: Downloads ~3 years of stock data for AAPL, MSFT, TSLA, NVDA

---

### 3. Clean Data (1 minute)

```bash
# Still in etl folder
python clean_stock_data.py
```

**What happens**: Cleans data and creates moving averages, returns, volatility

---

### 4. Analyze Data (5-10 minutes)

```bash
# Go to analysis folder
cd ../analysis

# Launch Jupyter
jupyter notebook
```

**Open and run these notebooks in order**:

1. `exploratory_analysis.ipynb` — Price trends, correlations, returns
2. `technical_indicators.ipynb` — RSI, MACD, signals
3. `portfolio_analysis.ipynb` — Portfolio performance, risk metrics

---

### 5. Create Tableau Dashboard (Optional, 10 minutes)

```bash
# Prepare Tableau data
cd ../dashboard
python prepare_tableau_data.py
```

**Then**:
- Open Tableau Desktop
- Connect to `tableau_dataset.csv`
- Follow `TABLEAU_GUIDE.md` instructions

---

## 📊 What You'll Get

### Analysis Results

✅ **Price Trends** — Visualize stock performance over time  
✅ **Return Statistics** — Mean, median, volatility for each stock  
✅ **Correlation Matrix** — See how stocks move together  
✅ **Technical Signals** — Buy/sell recommendations based on indicators  
✅ **Portfolio Performance** — Track $10,000 investment growth  
✅ **Risk Metrics** — Sharpe ratio, max drawdown, VaR  

### Files Generated

- `data/raw/stock_prices.csv` — Raw downloaded data
- `data/cleaned/stock_data_cleaned.csv` — Processed data
- `data/processed/*.png` — Charts and visualizations
- `data/processed/*.csv` — Analysis results
- `dashboard/tableau_dataset.csv` — Tableau-ready data

---

## 🎯 Key Outputs

### Exploratory Analysis
- Stock comparison charts
- Volume analysis
- Return distributions
- Yearly performance tables

### Technical Indicators
- RSI signals (overbought/oversold)
- MACD crossovers (buy/sell)
- Bollinger Bands (volatility)
- Moving average trends

### Portfolio Analysis
- Portfolio value growth chart
- Individual stock contributions
- Risk-adjusted returns
- Drawdown analysis
- Correlation heatmap

---

## 💡 Quick Tips

### Running All Steps in One Go

```bash
# From project root
cd etl
python fetch_stock_data.py
python clean_stock_data.py

cd ../dashboard
python prepare_tableau_data.py

cd ../analysis
jupyter notebook
```

### Troubleshooting

**Problem**: Module not found error  
**Solution**: Make sure you installed requirements.txt

**Problem**: No data file found  
**Solution**: Run fetch_stock_data.py first

**Problem**: Charts not displaying  
**Solution**: Run `%matplotlib inline` in Jupyter

**Problem**: Python version error  
**Solution**: Use Python 3.8 or higher

---

## 📈 Next Steps After Initial Run

1. **Customize Analysis**
   - Change stock symbols in `fetch_stock_data.py`
   - Modify date ranges
   - Adjust portfolio weights

2. **Explore Data**
   - Read through notebook markdown cells
   - Try different time periods
   - Add new stocks

3. **Build Dashboard**
   - Follow TABLEAU_GUIDE.md
   - Create interactive visualizations
   - Share insights

4. **Extend Project**
   - Add more technical indicators
   - Try different portfolio allocations
   - Implement backtesting

---

## 🎓 Understanding the Results

### Sample Insights You'll Find

**Example findings** (will vary with actual data):

```
Stock Performance:
  NVDA: +150% (Best performer)
  AAPL: +75%
  MSFT: +60%
  TSLA: +45%

Portfolio Metrics:
  Total Return: +85%
  Sharpe Ratio: 1.45
  Max Drawdown: -22%
  Volatility: 28%

Current Signals:
  AAPL: BUY (RSI oversold)
  MSFT: HOLD (neutral signals)
  NVDA: SELL (RSI overbought)
  TSLA: BUY (MACD bullish)
```

---

## ⏱️ Time Estimates

- **Setup**: 1 minute
- **Data Collection**: 2 minutes
- **Data Cleaning**: 1 minute
- **Run Notebooks**: 10 minutes
- **Review Results**: 15 minutes
- **Create Tableau Dashboard**: 30 minutes

**Total**: ~1 hour for complete analysis

---

## 📚 File Navigation

```
Stock-Market-Intelligence-Dashboard/
│
├── etl/                    ← START HERE
│   ├── fetch_stock_data.py
│   └── clean_stock_data.py
│
├── analysis/               ← THEN RUN THESE
│   ├── exploratory_analysis.ipynb
│   ├── technical_indicators.ipynb
│   └── portfolio_analysis.ipynb
│
└── dashboard/              ← FINALLY CREATE DASHBOARD
    ├── prepare_tableau_data.py
    └── TABLEAU_GUIDE.md
```

---

## 🔍 What Each Script Does

### fetch_stock_data.py
- Downloads stock data from Yahoo Finance
- Saves to `data/raw/stock_prices.csv`
- Shows download progress

### clean_stock_data.py
- Removes duplicates and missing values
- Calculates daily returns
- Adds moving averages
- Computes volatility
- Saves to `data/cleaned/stock_data_cleaned.csv`

### exploratory_analysis.ipynb
- Visualizes price trends
- Analyzes trading volume
- Creates correlation heatmap
- Generates summary statistics

### technical_indicators.ipynb
- Calculates RSI, MACD, Bollinger Bands
- Generates buy/sell signals
- Plots technical charts
- Exports indicator data

### portfolio_analysis.ipynb
- Simulates $10,000 investment
- Tracks portfolio value
- Calculates risk metrics
- Shows individual stock contributions

### prepare_tableau_data.py
- Creates Tableau-friendly dataset
- Adds date dimensions
- Formats columns
- Exports to CSV

---

## ✅ Success Checklist

After running all scripts, you should have:

- [ ] Raw data in `data/raw/`
- [ ] Cleaned data in `data/cleaned/`
- [ ] Charts in `data/processed/`
- [ ] Tableau dataset in `dashboard/`
- [ ] Analysis results in notebooks
- [ ] Summary statistics exported

---

## 🎯 Common Use Cases

### For Portfolio Review
1. Run all scripts to get latest data
2. Open `portfolio_analysis.ipynb`
3. Review performance metrics
4. Check rebalancing needs

### For Trading Signals
1. Update data (run fetch and clean)
2. Open `technical_indicators.ipynb`
3. Check RSI and MACD signals
4. Review moving average crossovers

### For Presentations
1. Generate all visualizations
2. Create Tableau dashboard
3. Export key charts
4. Use summary statistics

---

## 📞 Need Help?

1. **Check README.md** — Comprehensive documentation
2. **Read code comments** — Inline explanations
3. **Review notebooks** — Step-by-step analysis
4. **Check TABLEAU_GUIDE.md** — Dashboard instructions

---

## 🎓 Learning Path

**Beginner**:
1. Run scripts as-is
2. Read through notebooks
3. Understand outputs

**Intermediate**:
1. Modify stock symbols
2. Change analysis periods
3. Adjust portfolio weights

**Advanced**:
1. Add new indicators
2. Create custom metrics
3. Build predictive models

---

**Happy Analyzing! 📊**

---

Last Updated: March 2026
