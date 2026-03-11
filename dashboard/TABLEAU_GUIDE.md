# Tableau Dashboard Guide
## Stock Market Intelligence Dashboard

This guide will help you create an interactive Tableau dashboard using the prepared dataset.

---

## Dataset Information

**File**: `tableau_dataset.csv`  
**Location**: `/dashboard/tableau_dataset.csv`

**Key Columns**:
- **Date Dimensions**: Date, Year, Quarter, Month, Week, Day
- **Stock Information**: Stock_Symbol
- **Price Data**: Opening_Price, High_Price, Low_Price, Closing_Price
- **Volume**: Trading_Volume, Volume_Category
- **Returns**: Daily_Return_Pct, Cumulative_Return
- **Technical Indicators**: Moving_Avg_20Day, Moving_Avg_50Day, Volatility_Pct
- **Signals**: MA_Signal, Return_Category

---

## Dashboard Components

### 1. **Stock Price Trends**
**Chart Type**: Line Chart  
**Configuration**:
- Columns: Date (continuous)
- Rows: Closing_Price
- Color: Stock_Symbol
- Show: Moving averages as reference lines

**Purpose**: Visualize price trends over time for all stocks

---

### 2. **Moving Average Signals**
**Chart Type**: Dual-Axis Line Chart  
**Configuration**:
- Columns: Date
- Rows: Closing_Price, Moving_Avg_20Day, Moving_Avg_50Day
- Color: MA_Signal (Bullish = Green, Bearish = Red)
- Filters: Stock_Symbol

**Purpose**: Identify buy/sell signals based on moving average crossovers

---

### 3. **Volatility Chart**
**Chart Type**: Area Chart  
**Configuration**:
- Columns: Date
- Rows: Volatility_Pct
- Color: Stock_Symbol
- Add reference line for average volatility

**Purpose**: Compare volatility levels across stocks

---

### 4. **Correlation Heatmap**
**Chart Type**: Heatmap  
**Data Source**: Use correlation_matrix.csv
**Configuration**:
- Columns: Symbol 1
- Rows: Symbol 2
- Color: Correlation Value
- Color scale: Red (-1) → White (0) → Blue (+1)

**Purpose**: Show relationship between stock movements

---

### 5. **Portfolio Performance**
**Chart Type**: Stacked Area Chart  
**Data Source**: Use portfolio_timeseries.csv
**Configuration**:
- Columns: Date
- Rows: Individual stock values (AAPL, MSFT, NVDA, TSLA)
- Color: Stock_Symbol
- Show total portfolio value as line overlay

**Purpose**: Track portfolio value composition over time

---

### 6. **Volume Analysis**
**Chart Type**: Bar Chart + Line Chart (Dual Axis)  
**Configuration**:
- Columns: Date
- Rows (Primary): Trading_Volume (Bar)
- Rows (Secondary): Closing_Price (Line)
- Color: Volume_Category
- Filters: Stock_Symbol

**Purpose**: Correlate volume with price movements

---

### 7. **Return Distribution**
**Chart Type**: Histogram  
**Configuration**:
- Columns: Daily_Return_Pct (bins)
- Rows: Count of records
- Color: Return_Category
- Filters: Stock_Symbol

**Purpose**: Understand return distribution patterns

---

### 8. **Performance Summary Table**
**Chart Type**: Data Table  
**Data Source**: Use stock_summary_stats.csv
**Configuration**:
- Rows: Stock_Symbol
- Columns: Total_Return_Pct, Avg_Daily_Return_Pct, Volatility_Pct, 
  Avg_Volume, Start_Price, End_Price
- Color formatting: Green for positive returns, Red for negative

**Purpose**: Quick overview of key metrics

---

## Dashboard Layout

Recommended layout (4x2 grid):

```
┌─────────────────────┬─────────────────────┐
│  Stock Price Trends │  Volume Analysis    │
│  (Full Width)       │                     │
├─────────────────────┼─────────────────────┤
│  Moving Averages    │  Volatility Chart   │
│                     │                     │
├─────────────────────┼─────────────────────┤
│  Portfolio          │  Correlation        │
│  Performance        │  Heatmap            │
├─────────────────────┼─────────────────────┤
│  Return Distribution│  Performance Table  │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

---

## Step-by-Step Instructions

### Step 1: Import Data
1. Open Tableau Desktop
2. Click "Connect to Data" > "Text File"
3. Navigate to `dashboard/tableau_dataset.csv`
4. Click "Sheet 1" to start creating visualizations

### Step 2: Create Price Trends Chart
1. Drag "Date" to Columns (change to continuous)
2. Drag "Closing_Price" to Rows
3. Drag "Stock_Symbol" to Color
4. Right-click Y-axis → "Add Reference Line" for moving averages
5. Format: Add title, labels, grid lines

### Step 3: Add Filters
1. Drag "Stock_Symbol" to Filters shelf
2. Right-click filter → "Show Filter"
3. Select "Multiple Values (dropdown)"
4. Drag "Date" to Filters for date range selector

### Step 4: Create Dashboard
1. Click "Dashboard" → "New Dashboard"
2. Set size to "Automatic" or "Desktop (1366 x 768)"
3. Drag sheets onto dashboard canvas
4. Arrange according to layout above

### Step 5: Add Interactivity
1. Select each sheet on dashboard
2. Click filter icon → "Use as Filter"
3. Now clicking on elements will filter other views
4. Add global filters for Date and Stock_Symbol

### Step 6: Format Dashboard
1. Add title: "Stock Market Intelligence Dashboard"
2. Add subtitle with date range
3. Format colors consistently
4. Add tooltips with additional information
5. Add annotations for key insights

### Step 7: Create Actions
1. Dashboard → Actions → Add Action → "Filter"
2. Configure hover or click actions
3. Test interactivity

---

## Color Scheme

Use consistent colors across all visualizations:

- **AAPL**: #2E86AB (Blue)
- **MSFT**: #A23B72 (Purple)
- **NVDA**: #F18F01 (Orange)
- **TSLA**: #C73E1D (Red)

**Signal Colors**:
- Bullish/Gains: Green (#28A745)
- Bearish/Losses: Red (#DC3545)
- Neutral: Gray (#6C757D)

---

## Calculated Fields

Create these calculated fields in Tableau:

### 1. Price Change Color
```
IF [Daily_Return_Pct] > 0 THEN "Positive"
ELSEIF [Daily_Return_Pct] < 0 THEN "Negative"
ELSE "Unchanged"
END
```

### 2. Performance Label
```
IF [Total_Return_Pct] > 10 THEN "Strong"
ELSEIF [Total_Return_Pct] > 0 THEN "Moderate"
ELSE "Negative"
END
```

### 3. Volatility Level
```
IF [Volatility_Pct] > 3 THEN "High"
ELSEIF [Volatility_Pct] > 1 THEN "Medium"
ELSE "Low"
END
```

---

## Tips for Better Visualizations

1. **Use Tooltips**: Add calculated fields and descriptions
2. **Reference Lines**: Show averages, targets, benchmarks
3. **Trend Lines**: Add trend lines to show direction
4. **Annotations**: Highlight important events or patterns
5. **Consistent Formatting**: Use same colors, fonts, sizes
6. **Performance**: Use extracts for large datasets
7. **Mobile**: Design with mobile viewing in mind

---

## Publishing

### To Tableau Public:
1. File → Save to Tableau Public
2. Sign in with Tableau Public account
3. Your dashboard will be published online
4. Get shareable link

### To Tableau Server:
1. Server → Publish Workbook
2. Select project location
3. Set permissions
4. Configure refresh schedule for data

---

## Example Dashboard Insights

Your dashboard should answer these questions:

1. **Which stock had the best performance?**
2. **What are the current moving average signals?**
3. **Which stocks are most correlated?**
4. **What is the portfolio's current value?**
5. **When were the most volatile periods?**
6. **What is the average daily trading volume?**
7. **How are returns distributed?**
8. **What is the Sharpe ratio for each stock?**

---

## Advanced Features

Consider adding these advanced features:

1. **Parameter Controls**: Let users change time periods, thresholds
2. **Set Actions**: Allow users to create custom stock groups
3. **Forecasting**: Use Tableau's built-in forecasting
4. **Clustering**: Group similar trading days
5. **What-If Analysis**: Show different portfolio allocations
6. **Mobile Layout**: Create optimized mobile dashboard

---

## Troubleshooting

**Problem**: Charts not showing data  
**Solution**: Check data types, ensure fields are measures/dimensions

**Problem**: Filters not working  
**Solution**: Verify action filters are configured correctly

**Problem**: Dates showing as text  
**Solution**: Change data type to Date in Data Source tab

**Problem**: Performance is slow  
**Solution**: Create extract instead of live connection

---

## Resources

- **Tableau Public Gallery**: https://public.tableau.com/app/discover
- **Tableau Training**: https://www.tableau.com/learn/training
- **Community Forums**: https://community.tableau.com/

---

**Created for**: Stock Market Intelligence Dashboard  
**Last Updated**: March 2026
