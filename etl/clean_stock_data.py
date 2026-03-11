"""
Stock Data Cleaning Module
===========================
Cleans raw stock data and creates calculated financial features.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


# File paths
RAW_DATA_PATH = '../data/raw/stock_prices.csv'
CLEANED_DATA_PATH = '../data/cleaned/stock_data_cleaned.csv'


def load_raw_data(file_path=RAW_DATA_PATH):
    """
    Load raw stock data from CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to raw data file
    
    Returns:
    --------
    pd.DataFrame
        Loaded stock data
    """
    print(f"Loading raw data from: {file_path}")
    try:
        data = pd.read_csv(file_path)
        print(f"✓ Loaded {len(data)} records")
        return data
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        print("  Please run fetch_stock_data.py first!")
        return None
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        return None


def clean_data(data):
    """
    Clean the stock data: handle missing values, convert types, remove duplicates.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Raw stock data
    
    Returns:
    --------
    pd.DataFrame
        Cleaned stock data
    """
    print("\n" + "="*60)
    print("CLEANING DATA")
    print("="*60)
    
    df = data.copy()
    
    # 1. Convert date column to datetime
    print("\n1. Converting date to datetime format...")
    df['Date'] = pd.to_datetime(df['Date'])
    print(f"   ✓ Date column converted to datetime")
    
    # 2. Normalize column names
    print("\n2. Normalizing column names...")
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print(f"   ✓ Column names normalized")
    
    # 3. Remove duplicate records
    print("\n3. Removing duplicate records...")
    before_duplicates = len(df)
    df = df.drop_duplicates(subset=['date', 'symbol'], keep='first')
    after_duplicates = len(df)
    duplicates_removed = before_duplicates - after_duplicates
    print(f"   ✓ Removed {duplicates_removed} duplicate records")
    
    # 4. Handle missing values
    print("\n4. Handling missing values...")
    missing_before = df.isnull().sum().sum()
    print(f"   Missing values before: {missing_before}")
    
    # For price columns, forward fill then backward fill
    price_columns = ['open', 'high', 'low', 'close', 'adj_close']
    for col in price_columns:
        if col in df.columns:
            df[col] = df.groupby('symbol')[col].ffill().bfill()
    
    # For volume, fill with 0
    if 'volume' in df.columns:
        df['volume'] = df['volume'].fillna(0)
    
    missing_after = df.isnull().sum().sum()
    print(f"   Missing values after: {missing_after}")
    print(f"   ✓ Handled {missing_before - missing_after} missing values")
    
    # 5. Sort by symbol and date
    print("\n5. Sorting data by symbol and date...")
    df = df.sort_values(['symbol', 'date']).reset_index(drop=True)
    print(f"   ✓ Data sorted")
    
    print("\n" + "="*60)
    print(f"CLEANED DATA SHAPE: {df.shape}")
    print("="*60)
    
    return df


def create_features(data):
    """
    Create calculated financial features.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Cleaned stock data
    
    Returns:
    --------
    pd.DataFrame
        Data with new features
    """
    print("\n" + "="*60)
    print("CREATING CALCULATED FEATURES")
    print("="*60)
    
    df = data.copy()
    
    # Group by symbol for calculations
    for symbol in df['symbol'].unique():
        mask = df['symbol'] == symbol
        symbol_df = df[mask].copy()
        
        print(f"\nProcessing {symbol}...")
        
        # 1. Daily Return (percentage change)
        print("  • Calculating daily returns...")
        symbol_df['daily_return'] = symbol_df['close'].pct_change() * 100
        
        # 2. 20-day Moving Average
        print("  • Calculating 20-day moving average...")
        symbol_df['ma_20'] = symbol_df['close'].rolling(window=20, min_periods=1).mean()
        
        # 3. 50-day Moving Average
        print("  • Calculating 50-day moving average...")
        symbol_df['ma_50'] = symbol_df['close'].rolling(window=50, min_periods=1).mean()
        
        # 4. Volatility (20-day rolling standard deviation)
        print("  • Calculating volatility...")
        symbol_df['volatility'] = symbol_df['daily_return'].rolling(window=20, min_periods=1).std()
        
        # 5. Price Range (High - Low)
        print("  • Calculating price range...")
        symbol_df['price_range'] = symbol_df['high'] - symbol_df['low']
        
        # 6. Volume Moving Average (20-day)
        print("  • Calculating volume moving average...")
        symbol_df['volume_ma_20'] = symbol_df['volume'].rolling(window=20, min_periods=1).mean()
        
        # 7. Cumulative Return
        print("  • Calculating cumulative returns...")
        symbol_df['cumulative_return'] = (1 + symbol_df['daily_return']/100).cumprod() - 1
        
        # Update the main dataframe
        df.loc[mask, symbol_df.columns] = symbol_df
    
    # Fill NaN values in calculated features
    feature_columns = ['daily_return', 'ma_20', 'ma_50', 'volatility', 
                       'price_range', 'volume_ma_20', 'cumulative_return']
    for col in feature_columns:
        df[col] = df[col].fillna(0)
    
    print("\n" + "="*60)
    print(f"FEATURES CREATED: {len(feature_columns)}")
    print("="*60)
    
    return df


def save_cleaned_data(data, file_path=CLEANED_DATA_PATH):
    """
    Save cleaned data to CSV file.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Cleaned stock data
    file_path : str
        Path where CSV will be saved
    """
    if data is not None:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to CSV
        data.to_csv(file_path, index=False)
        print(f"\n✓ Cleaned data saved to: {file_path}")
        print(f"  File size: {os.path.getsize(file_path) / 1024:.2f} KB")
        print(f"  Columns: {', '.join(data.columns.tolist())}")
    else:
        print("No data to save!")


def display_data_summary(data):
    """
    Display summary of cleaned data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Cleaned stock data
    """
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    
    print(f"\nShape: {data.shape}")
    print(f"Date range: {data['date'].min()} to {data['date'].max()}")
    print(f"Symbols: {', '.join(data['symbol'].unique())}")
    
    print("\n" + "-"*60)
    print("STATISTICS BY SYMBOL")
    print("-"*60)
    
    for symbol in data['symbol'].unique():
        symbol_data = data[data['symbol'] == symbol]
        print(f"\n{symbol}:")
        print(f"  Records: {len(symbol_data)}")
        print(f"  Avg Close Price: ${symbol_data['close'].mean():.2f}")
        print(f"  Std Deviation: ${symbol_data['close'].std():.2f}")
        print(f"  Avg Daily Return: {symbol_data['daily_return'].mean():.2f}%")
        print(f"  Avg Volatility: {symbol_data['volatility'].mean():.2f}%")
        print(f"  Total Return: {symbol_data['cumulative_return'].iloc[-1]*100:.2f}%")


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("STOCK DATA CLEANING & FEATURE ENGINEERING")
    print("Stock Market Intelligence Dashboard")
    print("="*60 + "\n")
    
    # Load raw data
    raw_data = load_raw_data()
    
    if raw_data is not None:
        # Clean data
        cleaned_data = clean_data(raw_data)
        
        # Create features
        final_data = create_features(cleaned_data)
        
        # Display summary
        display_data_summary(final_data)
        
        # Save cleaned data
        save_cleaned_data(final_data)
        
        print("\n" + "="*60)
        print("Data cleaning completed successfully!")
        print("="*60 + "\n")
    else:
        print("\nData cleaning failed!")


if __name__ == "__main__":
    main()
