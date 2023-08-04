import ccxt
import pandas as pd
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.trend import PSARIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import AverageTrueRange, BollingerBands

# Initialize the exchange
exchange = ccxt.binance()

# Fetch historical OHLCV data
ohlcv = exchange.fetch_ohlcv('ETH/USDT', '15m')

# Convert to DataFrame
data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

# Set the index to timestamp
data.set_index('timestamp', inplace=True)

# Add Exponential Moving Averages
data['EMA_20'] = data['close'].ewm(span=20).mean()
data['EMA_50'] = data['close'].ewm(span=50).mean()

# Add Relative Strength Index
data['RSI'] = RSIIndicator(data['close']).rsi()

# Add Average True Range
data['ATR'] = AverageTrueRange(data['high'], data['low'], data['close']).average_true_range()

# Add On Balance Volume
data['OBV'] = OnBalanceVolumeIndicator(data['close'], data['volume']).on_balance_volume()

# Add Bollinger Bands
bb = BollingerBands(data['close'])
data['BB_upper'] = bb.bollinger_hband()
data['BB_middle'] = bb.bollinger_mavg()
data['BB_lower'] = bb.bollinger_lband()

# Add Parabolic SAR
data['Parabolic_SAR'] = PSARIndicator(data['high'], data['low'], data['close']).psar()

print(data.tail())
