"""
Financial Metrics Module
=========================
Provides financial calculation and metric functions.
This module is part of the Stock Market Intelligence Dashboard.

Author: Data Analyst
Date: March 2026
"""

import pandas as pd
import numpy as np
from scipy import stats


def calculate_returns(prices):
    """
    Calculate returns from price series.
    
    Parameters:
    -----------
    prices : pd.Series or np.array
        Price series
    
    Returns:
    --------
    pd.Series or np.array
        Returns
    """
    if isinstance(prices, pd.Series):
        return prices.pct_change()
    else:
        return np.diff(prices) / prices[:-1]


def calculate_log_returns(prices):
    """
    Calculate logarithmic returns.
    
    Parameters:
    -----------
    prices : pd.Series or np.array
        Price series
    
    Returns:
    --------
    pd.Series or np.array
        Log returns
    """
    if isinstance(prices, pd.Series):
        return np.log(prices / prices.shift(1))
    else:
        return np.log(prices[1:] / prices[:-1])


def calculate_volatility(returns, window=20):
    """
    Calculate rolling volatility (standard deviation of returns).
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    window : int
        Rolling window size
    
    Returns:
    --------
    pd.Series
        Volatility
    """
    return returns.rolling(window=window).std() * np.sqrt(252)  # Annualized


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio.
    
    Parameters:
    -----------
    returns : pd.Series or np.array
        Return series
    risk_free_rate : float
        Annual risk-free rate (default: 2%)
    
    Returns:
    --------
    float
        Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()


def calculate_max_drawdown(prices):
    """
    Calculate maximum drawdown.
    
    Parameters:
    -----------
    prices : pd.Series
        Price series
    
    Returns:
    --------
    float
        Maximum drawdown (as percentage)
    """
    cumulative = (1 + prices.pct_change()).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min() * 100


def calculate_rsi(prices, window=14):
    """
    Calculate Relative Strength Index (RSI).
    
    Parameters:
    -----------
    prices : pd.Series
        Price series
    window : int
        RSI period (default: 14)
    
    Returns:
    --------
    pd.Series
        RSI values
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Parameters:
    -----------
    prices : pd.Series
        Price series
    fast : int
        Fast EMA period
    slow : int
        Slow EMA period
    signal : int
        Signal line period
    
    Returns:
    --------
    dict
        Dictionary with MACD, signal, and histogram
    """
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    }


def calculate_bollinger_bands(prices, window=20, num_std=2):
    """
    Calculate Bollinger Bands.
    
    Parameters:
    -----------
    prices : pd.Series
        Price series
    window : int
        Rolling window
    num_std : int
        Number of standard deviations
    
    Returns:
    --------
    dict
        Dictionary with upper, middle, and lower bands
    """
    middle_band = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return {
        'upper': upper_band,
        'middle': middle_band,
        'lower': lower_band
    }


def calculate_beta(stock_returns, market_returns):
    """
    Calculate beta (systematic risk).
    
    Parameters:
    -----------
    stock_returns : pd.Series
        Stock return series
    market_returns : pd.Series
        Market return series
    
    Returns:
    --------
    float
        Beta coefficient
    """
    covariance = np.cov(stock_returns.dropna(), market_returns.dropna())[0][1]
    market_variance = np.var(market_returns.dropna())
    
    return covariance / market_variance


def calculate_alpha(stock_returns, market_returns, risk_free_rate=0.02):
    """
    Calculate alpha (excess return).
    
    Parameters:
    -----------
    stock_returns : pd.Series
        Stock return series
    market_returns : pd.Series
        Market return series
    risk_free_rate : float
        Annual risk-free rate
    
    Returns:
    --------
    float
        Alpha
    """
    beta = calculate_beta(stock_returns, market_returns)
    
    stock_mean = stock_returns.mean() * 252  # Annualized
    market_mean = market_returns.mean() * 252  # Annualized
    
    alpha = stock_mean - (risk_free_rate + beta * (market_mean - risk_free_rate))
    
    return alpha


def calculate_portfolio_return(weights, returns):
    """
    Calculate portfolio return.
    
    Parameters:
    -----------
    weights : dict or pd.Series
        Asset weights
    returns : pd.DataFrame
        Return series for each asset
    
    Returns:
    --------
    float
        Portfolio return
    """
    if isinstance(weights, dict):
        weights = pd.Series(weights)
    
    return (weights * returns.mean()).sum() * 252  # Annualized


def calculate_portfolio_volatility(weights, returns):
    """
    Calculate portfolio volatility.
    
    Parameters:
    -----------
    weights : dict or pd.Series
        Asset weights
    returns : pd.DataFrame
        Return series for each asset
    
    Returns:
    --------
    float
        Portfolio volatility
    """
    if isinstance(weights, dict):
        weights = pd.Series(weights)
    
    cov_matrix = returns.cov() * 252  # Annualized
    portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
    
    return np.sqrt(portfolio_variance)


def calculate_var(returns, confidence=0.95):
    """
    Calculate Value at Risk (VaR).
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    confidence : float
        Confidence level (default: 0.95)
    
    Returns:
    --------
    float
        VaR value
    """
    return np.percentile(returns.dropna(), (1 - confidence) * 100)


def calculate_cvar(returns, confidence=0.95):
    """
    Calculate Conditional Value at Risk (CVaR) / Expected Shortfall.
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    confidence : float
        Confidence level
    
    Returns:
    --------
    float
        CVaR value
    """
    var = calculate_var(returns, confidence)
    return returns[returns <= var].mean()


def calculate_information_ratio(portfolio_returns, benchmark_returns):
    """
    Calculate Information Ratio.
    
    Parameters:
    -----------
    portfolio_returns : pd.Series
        Portfolio return series
    benchmark_returns : pd.Series
        Benchmark return series
    
    Returns:
    --------
    float
        Information ratio
    """
    active_returns = portfolio_returns - benchmark_returns
    tracking_error = active_returns.std() * np.sqrt(252)
    
    return (active_returns.mean() * 252) / tracking_error


def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sortino Ratio (downside risk-adjusted return).
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    risk_free_rate : float
        Annual risk-free rate
    
    Returns:
    --------
    float
        Sortino ratio
    """
    excess_returns = returns - (risk_free_rate / 252)
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = downside_returns.std() * np.sqrt(252)
    
    return (excess_returns.mean() * 252) / downside_std


def get_stock_statistics(data, symbol):
    """
    Calculate comprehensive statistics for a stock.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Stock data
    symbol : str
        Stock symbol
    
    Returns:
    --------
    dict
        Dictionary of statistics
    """
    stock_data = data[data['symbol'] == symbol].copy()
    
    returns = stock_data['close'].pct_change().dropna()
    
    stats_dict = {
        'symbol': symbol,
        'start_date': stock_data['date'].min(),
        'end_date': stock_data['date'].max(),
        'start_price': stock_data['close'].iloc[0],
        'end_price': stock_data['close'].iloc[-1],
        'min_price': stock_data['close'].min(),
        'max_price': stock_data['close'].max(),
        'avg_price': stock_data['close'].mean(),
        'std_price': stock_data['close'].std(),
        'total_return': ((stock_data['close'].iloc[-1] / stock_data['close'].iloc[0]) - 1) * 100,
        'avg_daily_return': returns.mean() * 100,
        'volatility': returns.std() * np.sqrt(252) * 100,
        'max_drawdown': calculate_max_drawdown(stock_data['close']),
        'sharpe_ratio': calculate_sharpe_ratio(returns),
        'avg_volume': stock_data['volume'].mean()
    }
    
    return stats_dict
