import pandas as pd
import numpy as np
import yfinance as yf

def fetch_stock_data(symbol: str, timeframe: str, interval: str = 'hour') -> pd.DataFrame:
    """
    Fetch historical stock data with timeframe and interval selection.
    
    Parameters:
        symbol (str): Stock symbol, e.g., 'AAPL', 'MSFT'
        timeframe (str): Time period, e.g., '1M', '3M', '1Y'
        interval (str): Data frequency - 'hour', 'day', '15m', etc.
    
    Returns:
        pd.DataFrame: Historical stock data
    """
    try:
        end_date = pd.Timestamp.now()
        
        # Map timeframes to days
        timeframe_dict = {
            '1M': 30,
            '3M': 90, 
            '6M': 180,
            '1Y': 365,
            '2Y': 730,
            '5Y': 1825
        }
        
        # Map interval parameter to yfinance interval strings
        interval_dict = {
            'minute': '1m',    # 1 minute
            '5min': '5m',      # 5 minutes
            '15min': '15m',    # 15 minutes
            '30min': '30m',    # 30 minutes
            'hour': '1h',      # 1 hour
            'day': '1d',       # 1 day
            'week': '1wk',     # 1 week
            'month': '1mo'     # 1 month
        }
        
        # Set the interval (default to 1h if not specified)
        yf_interval = interval_dict.get(interval, '1h')
        

        days = timeframe_dict[timeframe]
        if yf_interval in ['1m', '5m', '15m', '30m', '1h'] and days > 60:
            days_limit = min(days, 60)  # Limit to 60 days for intraday data
            print(f"Warning: Limiting {yf_interval} data to {days_limit} days instead of {days}")
        else:
            days_limit = days
            
        # Handle cryptocurrency symbols
        if symbol.upper() in ['BTC', 'ETH', 'DOGE', 'XRP', 'SOL']:
            symbol = f"{symbol}-USD"
            
        start_date = (end_date - pd.Timedelta(days=days_limit)).strftime('%Y-%m-%d')
        
        data = yf.download(
            symbol,
            start=start_date,
            end=end_date.strftime('%Y-%m-%d'),
            interval=yf_interval
        )
        
        if data.empty:
            raise Exception(f"No data found for symbol {symbol} with {yf_interval} interval")
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        data = data.dropna()

        return data
    
    except Exception as e:
        raise Exception(f"Error fetching {interval} data for {symbol}: {str(e)}")
    
def momentum_trading_strategy(data, short_window=5, long_window=20):
    """Generate trading signals based on moving average crossover strategy."""
    # Create a copy to avoid modifying original
    signals = pd.DataFrame(index=data.index)
    
    # Create price and moving average columns
    signals['price'] = data['Close']
    signals['short_mavg'] = data['Close'].rolling(window=short_window).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window).mean()
    
    # Create signals
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    
    # Generate positions
    signals['positions'] = signals['signal'].diff()
    
    return signals