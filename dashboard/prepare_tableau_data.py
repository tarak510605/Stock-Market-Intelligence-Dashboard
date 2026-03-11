"""
Tableau Dataset Preparation Script
====================================
Prepares aggregated dataset for Tableau visualization.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys
sys.path.append('../')

from utils.helper_functions import load_data


def prepare_tableau_dataset():
    """
    Prepare comprehensive dataset for Tableau dashboard.
    
    This creates a flattened, aggregated dataset suitable for
    importing into Tableau for visualization.
    """
    print("="*80)
    print("TABLEAU DATASET PREPARATION")
    print("Stock Market Intelligence Dashboard")
    print("="*80)
    
    # Load cleaned data
    print("\n1. Loading data...")
    data = load_data('../data/cleaned/stock_data_cleaned.csv')
    
    if data is None:
        print("✗ Failed to load data!")
        return None
    
    print(f"✓ Loaded {len(data)} records")
    
    # Select and rename columns for Tableau
    print("\n2. Selecting and formatting columns...")
    
    tableau_data = data.copy()
    
    # Ensure all required columns exist
    required_cols = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume',
                    'daily_return', 'ma_20', 'ma_50', 'volatility']
    
    missing_cols = [col for col in required_cols if col not in tableau_data.columns]
    if missing_cols:
        print(f"⚠️ Warning: Missing columns: {missing_cols}")
    
    # Rename columns for better readability in Tableau
    column_mapping = {
        'date': 'Date',
        'symbol': 'Stock_Symbol',
        'open': 'Opening_Price',
        'high': 'High_Price',
        'low': 'Low_Price',
        'close': 'Closing_Price',
        'adj_close': 'Adjusted_Close',
        'volume': 'Trading_Volume',
        'daily_return': 'Daily_Return_Pct',
        'ma_20': 'Moving_Avg_20Day',
        'ma_50': 'Moving_Avg_50Day',
        'volatility': 'Volatility_Pct',
        'price_range': 'Daily_Price_Range',
        'volume_ma_20': 'Volume_MA_20Day',
        'cumulative_return': 'Cumulative_Return'
    }
    
    tableau_data = tableau_data.rename(columns=column_mapping)
    
    # Convert date to proper format
    tableau_data['Date'] = pd.to_datetime(tableau_data['Date'])
    
    # Add additional date dimensions for Tableau
    print("\n3. Adding date dimensions...")
    tableau_data['Year'] = tableau_data['Date'].dt.year
    tableau_data['Quarter'] = tableau_data['Date'].dt.quarter
    tableau_data['Month'] = tableau_data['Date'].dt.month
    tableau_data['Month_Name'] = tableau_data['Date'].dt.strftime('%B')
    tableau_data['Week'] = tableau_data['Date'].dt.isocalendar().week
    tableau_data['Day_of_Week'] = tableau_data['Date'].dt.dayofweek
    tableau_data['Day_Name'] = tableau_data['Date'].dt.strftime('%A')
    
    # Add calculated fields
    print("\n4. Adding calculated fields...")
    
    # Price change from previous day
    for symbol in tableau_data['Stock_Symbol'].unique():
        mask = tableau_data['Stock_Symbol'] == symbol
        tableau_data.loc[mask, 'Price_Change'] = tableau_data.loc[mask, 'Closing_Price'].diff()
    
    # Percentage of 52-week high
    for symbol in tableau_data['Stock_Symbol'].unique():
        mask = tableau_data['Stock_Symbol'] == symbol
        rolling_max = tableau_data.loc[mask, 'Closing_Price'].rolling(window=252, min_periods=1).max()
        tableau_data.loc[mask, 'Pct_of_52Week_High'] = (
            tableau_data.loc[mask, 'Closing_Price'] / rolling_max * 100
        )
    
    # Trading volume categories
    tableau_data['Volume_Category'] = pd.cut(
        tableau_data['Trading_Volume'], 
        bins=[0, 50_000_000, 100_000_000, float('inf')], 
        labels=['Low', 'Medium', 'High']
    )
    
    # Return categories
    tableau_data['Return_Category'] = pd.cut(
        tableau_data['Daily_Return_Pct'],
        bins=[-float('inf'), -2, -0.5, 0.5, 2, float('inf')],
        labels=['Large Loss', 'Small Loss', 'Flat', 'Small Gain', 'Large Gain']
    )
    
    # MA signal (20-day vs 50-day)
    tableau_data['MA_Signal'] = 'Neutral'
    tableau_data.loc[tableau_data['Moving_Avg_20Day'] > tableau_data['Moving_Avg_50Day'], 'MA_Signal'] = 'Bullish'
    tableau_data.loc[tableau_data['Moving_Avg_20Day'] < tableau_data['Moving_Avg_50Day'], 'MA_Signal'] = 'Bearish'
    
    # Fill missing values
    print("\n5. Handling missing values...")
    tableau_data = tableau_data.fillna(0)
    
    # Select final columns
    print("\n6. Selecting final columns...")
    final_columns = [
        'Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Week', 
        'Day_of_Week', 'Day_Name',
        'Stock_Symbol', 
        'Opening_Price', 'High_Price', 'Low_Price', 'Closing_Price',
        'Trading_Volume', 'Volume_Category',
        'Daily_Return_Pct', 'Return_Category', 'Price_Change',
        'Moving_Avg_20Day', 'Moving_Avg_50Day', 'MA_Signal',
        'Volatility_Pct', 'Daily_Price_Range',
        'Cumulative_Return', 'Pct_of_52Week_High'
    ]
    
    # Only include columns that exist
    final_columns = [col for col in final_columns if col in tableau_data.columns]
    tableau_data = tableau_data[final_columns]
    
    # Sort by symbol and date
    tableau_data = tableau_data.sort_values(['Stock_Symbol', 'Date'])
    
    # Display summary
    print("\n" + "="*80)
    print("DATASET SUMMARY")
    print("="*80)
    print(f"Total Records: {len(tableau_data):,}")
    print(f"Date Range: {tableau_data['Date'].min()} to {tableau_data['Date'].max()}")
    print(f"Stocks: {', '.join(tableau_data['Stock_Symbol'].unique())}")
    print(f"Columns: {len(tableau_data.columns)}")
    print(f"\nColumn List:")
    for col in tableau_data.columns:
        print(f"  • {col}")
    
    return tableau_data


def save_tableau_dataset(data, file_path='../dashboard/tableau_dataset.csv'):
    """
    Save Tableau dataset to CSV.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Tableau dataset
    file_path : str
        Output file path
    """
    if data is not None:
        data.to_csv(file_path, index=False)
        print(f"\n✓ Tableau dataset saved to: {file_path}")
        print(f"  File size: {os.path.getsize(file_path) / 1024:.2f} KB")
        print(f"  Ready to import into Tableau!")
    else:
        print("No data to save!")


def create_summary_stats():
    """
    Create summary statistics table for Tableau.
    """
    print("\n" + "="*80)
    print("CREATING SUMMARY STATISTICS TABLE")
    print("="*80)
    
    data = load_data('../data/cleaned/stock_data_cleaned.csv')
    
    if data is None:
        return None
    
    summary_list = []
    
    for symbol in data['symbol'].unique():
        symbol_data = data[data['symbol'] == symbol]
        
        summary_list.append({
            'Stock_Symbol': symbol,
            'Start_Date': symbol_data['date'].min(),
            'End_Date': symbol_data['date'].max(),
            'Trading_Days': len(symbol_data),
            'Start_Price': symbol_data['close'].iloc[0],
            'End_Price': symbol_data['close'].iloc[-1],
            'Min_Price': symbol_data['close'].min(),
            'Max_Price': symbol_data['close'].max(),
            'Avg_Price': symbol_data['close'].mean(),
            'Total_Return_Pct': ((symbol_data['close'].iloc[-1] / symbol_data['close'].iloc[0]) - 1) * 100,
            'Avg_Daily_Return_Pct': symbol_data['daily_return'].mean(),
            'Volatility_Pct': symbol_data['daily_return'].std(),
            'Avg_Volume': symbol_data['volume'].mean(),
            'Total_Volume': symbol_data['volume'].sum()
        })
    
    summary_df = pd.DataFrame(summary_list)
    summary_df.to_csv('../dashboard/stock_summary_stats.csv', index=False)
    
    print("✓ Summary statistics saved to: ../dashboard/stock_summary_stats.csv")
    
    return summary_df


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("TABLEAU DATASET PREPARATION SCRIPT")
    print("="*80 + "\n")
    
    # Prepare main dataset
    tableau_data = prepare_tableau_dataset()
    
    if tableau_data is not None:
        # Save dataset
        save_tableau_dataset(tableau_data)
        
        # Create summary stats
        create_summary_stats()
        
        print("\n" + "="*80)
        print("TABLEAU DATASET PREPARATION COMPLETED!")
        print("="*80)
        print("\nNext Steps:")
        print("1. Open Tableau Desktop")
        print("2. Connect to Data > Text File")
        print("3. Select: dashboard/tableau_dataset.csv")
        print("4. Build your visualizations!")
        print("="*80 + "\n")
    else:
        print("\nDataset preparation failed!")


if __name__ == "__main__":
    main()
