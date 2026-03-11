"""
Visualization Module
====================
Provides charting and visualization functions for stock market data.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


def plot_stock_prices(data, symbols=None, save_path=None):
    """
    Plot closing prices for multiple stocks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with columns: date, symbol, close
    symbols : list, optional
        List of symbols to plot. If None, plots all symbols
    save_path : str, optional
        Path to save the figure
    """
    if symbols is None:
        symbols = data['symbol'].unique()
    
    plt.figure(figsize=(14, 8))
    
    for symbol in symbols:
        symbol_data = data[data['symbol'] == symbol]
        plt.plot(symbol_data['date'], symbol_data['close'], 
                label=symbol, linewidth=2, marker='o', markersize=2)
    
    plt.title('Stock Price Trends', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Closing Price ($)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_volume_analysis(data, symbol, save_path=None):
    """
    Plot volume analysis with price for a single stock.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    symbol : str
        Stock symbol
    save_path : str, optional
        Path to save the figure
    """
    symbol_data = data[data['symbol'] == symbol].copy()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), 
                                    gridspec_kw={'height_ratios': [2, 1]})
    
    # Plot 1: Price
    ax1.plot(symbol_data['date'], symbol_data['close'], 
            color='#2E86AB', linewidth=2, label='Close Price')
    ax1.set_title(f'{symbol} - Price and Volume Analysis', 
                 fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Volume
    ax2.bar(symbol_data['date'], symbol_data['volume'], 
           color='#A23B72', alpha=0.7, label='Volume')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_daily_returns(data, symbols=None, save_path=None):
    """
    Plot daily returns distribution for stocks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with daily_return column
    symbols : list, optional
        List of symbols to plot
    save_path : str, optional
        Path to save the figure
    """
    if symbols is None:
        symbols = data['symbol'].unique()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    for idx, symbol in enumerate(symbols[:4]):
        symbol_data = data[data['symbol'] == symbol]
        
        # Histogram
        axes[idx].hist(symbol_data['daily_return'].dropna(), 
                      bins=50, color=colors[idx], alpha=0.7, edgecolor='black')
        axes[idx].axvline(symbol_data['daily_return'].mean(), 
                         color='red', linestyle='--', linewidth=2, 
                         label=f'Mean: {symbol_data["daily_return"].mean():.2f}%')
        axes[idx].set_title(f'{symbol} - Daily Returns Distribution', fontweight='bold')
        axes[idx].set_xlabel('Daily Return (%)')
        axes[idx].set_ylabel('Frequency')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Daily Returns Distribution Analysis', 
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_moving_averages(data, symbol, save_path=None):
    """
    Plot moving averages with price.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with ma_20 and ma_50 columns
    symbol : str
        Stock symbol
    save_path : str, optional
        Path to save the figure
    """
    symbol_data = data[data['symbol'] == symbol].copy()
    
    plt.figure(figsize=(14, 8))
    
    plt.plot(symbol_data['date'], symbol_data['close'], 
            label='Close Price', linewidth=2, color='#2E86AB')
    plt.plot(symbol_data['date'], symbol_data['ma_20'], 
            label='20-Day MA', linewidth=1.5, linestyle='--', color='#F18F01')
    plt.plot(symbol_data['date'], symbol_data['ma_50'], 
            label='50-Day MA', linewidth=1.5, linestyle='--', color='#C73E1D')
    
    plt.title(f'{symbol} - Moving Average Analysis', 
             fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_volatility(data, symbols=None, save_path=None):
    """
    Plot volatility comparison across stocks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with volatility column
    symbols : list, optional
        List of symbols to plot
    save_path : str, optional
        Path to save the figure
    """
    if symbols is None:
        symbols = data['symbol'].unique()
    
    plt.figure(figsize=(14, 8))
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    for idx, symbol in enumerate(symbols):
        symbol_data = data[data['symbol'] == symbol]
        plt.plot(symbol_data['date'], symbol_data['volatility'], 
                label=symbol, linewidth=2, color=colors[idx % len(colors)])
    
    plt.title('Volatility Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Volatility (%)', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_correlation_heatmap(data, save_path=None):
    """
    Plot correlation heatmap for stock closing prices.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    save_path : str, optional
        Path to save the figure
    """
    # Pivot data to have symbols as columns
    pivot_data = data.pivot(index='date', columns='symbol', values='close')
    
    # Calculate correlation
    correlation = pivot_data.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', 
               center=0, square=True, linewidths=1, 
               cbar_kws={"shrink": 0.8}, fmt='.2f',
               vmin=-1, vmax=1)
    
    plt.title('Stock Price Correlation Matrix', 
             fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()
    
    return correlation


def plot_cumulative_returns(data, symbols=None, save_path=None):
    """
    Plot cumulative returns for stocks.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data with cumulative_return column
    symbols : list, optional
        List of symbols to plot
    save_path : str, optional
        Path to save the figure
    """
    if symbols is None:
        symbols = data['symbol'].unique()
    
    plt.figure(figsize=(14, 8))
    
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    for idx, symbol in enumerate(symbols):
        symbol_data = data[data['symbol'] == symbol]
        plt.plot(symbol_data['date'], symbol_data['cumulative_return'] * 100, 
                label=symbol, linewidth=2, color=colors[idx % len(colors)])
    
    plt.title('Cumulative Returns Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (%)', fontsize=12)
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()


def plot_candlestick(data, symbol, start_date=None, end_date=None, save_path=None):
    """
    Create a simplified candlestick-style chart.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    symbol : str
        Stock symbol
    start_date : str, optional
        Start date for filtering
    end_date : str, optional
        End date for filtering
    save_path : str, optional
        Path to save the figure
    """
    symbol_data = data[data['symbol'] == symbol].copy()
    
    if start_date:
        symbol_data = symbol_data[symbol_data['date'] >= start_date]
    if end_date:
        symbol_data = symbol_data[symbol_data['date'] <= end_date]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create up and down days
    up = symbol_data[symbol_data['close'] >= symbol_data['open']]
    down = symbol_data[symbol_data['close'] < symbol_data['open']]
    
    # Plot bars for price range
    ax.bar(up['date'], up['high'] - up['low'], bottom=up['low'], 
          width=0.8, color='green', alpha=0.3)
    ax.bar(down['date'], down['high'] - down['low'], bottom=down['low'], 
          width=0.8, color='red', alpha=0.3)
    
    # Plot lines
    ax.plot(symbol_data['date'], symbol_data['close'], 
           color='black', linewidth=1.5, label='Close')
    
    ax.set_title(f'{symbol} - Price Chart', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved to: {save_path}")
    
    plt.show()
