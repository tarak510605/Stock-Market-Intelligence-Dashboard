"""
Helper Functions Module
========================
Provides utility and helper functions for the project.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def load_data(file_path):
    """
    Load data from CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to CSV file
    
    Returns:
    --------
    pd.DataFrame
        Loaded data
    """
    try:
        data = pd.read_csv(file_path)
        # Convert date column to datetime if it exists
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


def filter_by_date(data, start_date=None, end_date=None):
    """
    Filter data by date range.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data with 'date' column
    start_date : str or datetime
        Start date
    end_date : str or datetime
        End date
    
    Returns:
    --------
    pd.DataFrame
        Filtered data
    """
    filtered_data = data.copy()
    
    if start_date:
        start_date = pd.to_datetime(start_date)
        filtered_data = filtered_data[filtered_data['date'] >= start_date]
    
    if end_date:
        end_date = pd.to_datetime(end_date)
        filtered_data = filtered_data[filtered_data['date'] <= end_date]
    
    return filtered_data


def filter_by_symbol(data, symbols):
    """
    Filter data by stock symbols.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data with 'symbol' column
    symbols : str or list
        Symbol or list of symbols
    
    Returns:
    --------
    pd.DataFrame
        Filtered data
    """
    if isinstance(symbols, str):
        symbols = [symbols]
    
    return data[data['symbol'].isin(symbols)]


def create_date_features(data):
    """
    Create additional date-based features.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data with 'date' column
    
    Returns:
    --------
    pd.DataFrame
        Data with new features
    """
    df = data.copy()
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    
    return df


def calculate_percentage_change(start_value, end_value):
    """
    Calculate percentage change.
    
    Parameters:
    -----------
    start_value : float
        Starting value
    end_value : float
        Ending value
    
    Returns:
    --------
    float
        Percentage change
    """
    return ((end_value - start_value) / start_value) * 100


def format_currency(value):
    """
    Format value as currency.
    
    Parameters:
    -----------
    value : float
        Value to format
    
    Returns:
    --------
    str
        Formatted currency string
    """
    return f"${value:,.2f}"


def format_percentage(value):
    """
    Format value as percentage.
    
    Parameters:
    -----------
    value : float
        Value to format
    
    Returns:
    --------
    str
        Formatted percentage string
    """
    return f"{value:.2f}%"


def format_large_number(value):
    """
    Format large numbers with K, M, B suffixes.
    
    Parameters:
    -----------
    value : float
        Value to format
    
    Returns:
    --------
    str
        Formatted string
    """
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def get_latest_prices(data):
    """
    Get latest prices for all symbols.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    
    Returns:
    --------
    pd.DataFrame
        Latest prices by symbol
    """
    latest = data.sort_values('date').groupby('symbol').tail(1)
    return latest[['symbol', 'date', 'close', 'volume']]


def calculate_returns_matrix(data):
    """
    Create returns matrix (symbols as columns).
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with daily_return column
    
    Returns:
    --------
    pd.DataFrame
        Returns matrix
    """
    returns_pivot = data.pivot(index='date', columns='symbol', values='daily_return')
    return returns_pivot


def calculate_price_matrix(data):
    """
    Create price matrix (symbols as columns).
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    
    Returns:
    --------
    pd.DataFrame
        Price matrix
    """
    price_pivot = data.pivot(index='date', columns='symbol', values='close')
    return price_pivot


def get_top_performers(data, n=5, metric='total_return'):
    """
    Get top performing stocks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    n : int
        Number of top performers
    metric : str
        Metric to use ('total_return', 'avg_return', 'volatility')
    
    Returns:
    --------
    pd.DataFrame
        Top performers
    """
    performance = []
    
    for symbol in data['symbol'].unique():
        symbol_data = data[data['symbol'] == symbol]
        
        if metric == 'total_return':
            value = ((symbol_data['close'].iloc[-1] / symbol_data['close'].iloc[0]) - 1) * 100
        elif metric == 'avg_return':
            value = symbol_data['daily_return'].mean()
        elif metric == 'volatility':
            value = symbol_data['daily_return'].std()
        else:
            value = 0
        
        performance.append({
            'symbol': symbol,
            metric: value
        })
    
    df = pd.DataFrame(performance).sort_values(metric, ascending=False).head(n)
    return df


def export_to_excel(data, file_path, sheet_name='Data'):
    """
    Export data to Excel file.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data to export
    file_path : str
        Output file path
    sheet_name : str
        Sheet name
    """
    try:
        data.to_excel(file_path, sheet_name=sheet_name, index=False)
        print(f"✓ Data exported to: {file_path}")
    except Exception as e:
        print(f"✗ Error exporting to Excel: {str(e)}")


def create_summary_table(data):
    """
    Create summary statistics table.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    
    Returns:
    --------
    pd.DataFrame
        Summary table
    """
    summary = []
    
    for symbol in data['symbol'].unique():
        symbol_data = data[data['symbol'] == symbol]
        
        summary.append({
            'Symbol': symbol,
            'Start Date': symbol_data['date'].min().strftime('%Y-%m-%d'),
            'End Date': symbol_data['date'].max().strftime('%Y-%m-%d'),
            'Start Price': format_currency(symbol_data['close'].iloc[0]),
            'End Price': format_currency(symbol_data['close'].iloc[-1]),
            'Min Price': format_currency(symbol_data['close'].min()),
            'Max Price': format_currency(symbol_data['close'].max()),
            'Avg Price': format_currency(symbol_data['close'].mean()),
            'Total Return': format_percentage(
                ((symbol_data['close'].iloc[-1] / symbol_data['close'].iloc[0]) - 1) * 100
            ),
            'Avg Daily Return': format_percentage(symbol_data['daily_return'].mean()),
            'Volatility': format_percentage(symbol_data['daily_return'].std())
        })
    
    return pd.DataFrame(summary)


def validate_data(data):
    """
    Validate data quality.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data to validate
    
    Returns:
    --------
    dict
        Validation results
    """
    results = {
        'total_records': len(data),
        'missing_values': data.isnull().sum().to_dict(),
        'duplicate_records': data.duplicated().sum(),
        'date_range': {
            'min': data['date'].min() if 'date' in data.columns else None,
            'max': data['date'].max() if 'date' in data.columns else None
        },
        'symbols': data['symbol'].unique().tolist() if 'symbol' in data.columns else []
    }
    
    return results


def resample_data(data, freq='W', agg_func='last'):
    """
    Resample data to different frequency.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Data with date index or column
    freq : str
        Frequency ('D' daily, 'W' weekly, 'M' monthly)
    agg_func : str
        Aggregation function ('last', 'mean', 'first')
    
    Returns:
    --------
    pd.DataFrame
        Resampled data
    """
    if 'date' in data.columns:
        data = data.set_index('date')
    
    if agg_func == 'last':
        resampled = data.resample(freq).last()
    elif agg_func == 'mean':
        resampled = data.resample(freq).mean()
    elif agg_func == 'first':
        resampled = data.resample(freq).first()
    else:
        resampled = data.resample(freq).last()
    
    return resampled.reset_index()
