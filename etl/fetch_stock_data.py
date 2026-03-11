"""
Stock Data Fetching Module
===========================
Fetches historical stock data for specified tickers using yfinance library.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Constants
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'TSLA', 'NVDA']
START_DATE = '2021-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')
RAW_DATA_PATH = '../data/raw/stock_prices.csv'


def fetch_stock_data(symbols=STOCK_SYMBOLS, start_date=START_DATE, end_date=END_DATE):
    """
    Fetch historical stock data for multiple symbols.
    
    Parameters:
    -----------
    symbols : list
        List of stock ticker symbols
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing stock data for all symbols
    """
    print(f"Fetching stock data from {start_date} to {end_date}...")
    print(f"Symbols: {', '.join(symbols)}")
    
    all_data = []
    
    for symbol in symbols:
        try:
            print(f"\nDownloading {symbol}...")
            # Download stock data
            stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            # Flatten MultiIndex columns if present
            if isinstance(stock_data.columns, pd.MultiIndex):
                stock_data.columns = stock_data.columns.get_level_values(0)
            
            # Add symbol column
            stock_data['Symbol'] = symbol
            
            # Reset index to make Date a column
            stock_data.reset_index(inplace=True)
            
            # Append to list
            all_data.append(stock_data)
            
            print(f"✓ Successfully downloaded {len(stock_data)} records for {symbol}")
            
        except Exception as e:
            print(f"✗ Error downloading {symbol}: {str(e)}")
            continue
    
    # Combine all data into single DataFrame
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        print(f"\n{'='*60}")
        print(f"Total records fetched: {len(combined_data)}")
        print(f"Date range: {combined_data['Date'].min()} to {combined_data['Date'].max()}")
        print(f"{'='*60}")
        return combined_data
    else:
        print("No data was fetched!")
        return None


def save_stock_data(data, file_path=RAW_DATA_PATH):
    """
    Save stock data to CSV file.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data to save
    file_path : str
        Path where CSV will be saved
    """
    if data is not None:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to CSV
        data.to_csv(file_path, index=False)
        print(f"\n✓ Data saved successfully to: {file_path}")
        print(f"  File size: {os.path.getsize(file_path) / 1024:.2f} KB")
    else:
        print("No data to save!")


def get_stock_info(symbol):
    """
    Get detailed information about a stock.
    
    Parameters:
    -----------
    symbol : str
        Stock ticker symbol
    
    Returns:
    --------
    dict
        Dictionary containing stock information
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Extract key information
        stock_info = {
            'symbol': symbol,
            'company_name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'current_price': info.get('currentPrice', 'N/A'),
            'currency': info.get('currency', 'N/A')
        }
        
        return stock_info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {str(e)}")
        return None


def display_stock_summary(data):
    """
    Display summary statistics of fetched stock data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    """
    if data is not None:
        print("\n" + "="*60)
        print("STOCK DATA SUMMARY")
        print("="*60)
        
        for symbol in data['Symbol'].unique():
            symbol_data = data[data['Symbol'] == symbol]
            print(f"\n{symbol}:")
            print(f"  Records: {len(symbol_data)}")
            print(f"  Price Range: ${symbol_data['Close'].min():.2f} - ${symbol_data['Close'].max():.2f}")
            print(f"  Average Volume: {symbol_data['Volume'].mean():,.0f}")
            print(f"  Latest Close: ${symbol_data['Close'].iloc[-1]:.2f}")


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("STOCK MARKET DATA COLLECTION")
    print("Stock Market Intelligence Dashboard")
    print("="*60 + "\n")
    
    # Fetch stock data
    stock_data = fetch_stock_data()
    
    # Display summary
    if stock_data is not None:
        display_stock_summary(stock_data)
        
        # Save data
        save_stock_data(stock_data)
        
        print("\n" + "="*60)
        print("Data collection completed successfully!")
        print("="*60 + "\n")
    else:
        print("\nData collection failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
