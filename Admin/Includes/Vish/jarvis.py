import pandas as pd
from nsetools import Nse

def calculate_ema(data, period):
    return data['Close'].ewm(span=period, adjust=False).mean()

def generate_trade_signal(data):
    data['EMA_9'] = calculate_ema(data, 9)
    data['EMA_100'] = calculate_ema(data, 100)
    data['Signal'] = 0

    for i in range(1, len(data)):
        if data['EMA_9'].iloc[i] > data['EMA_100'].iloc[i] and data['EMA_9'].iloc[i-1] < data['EMA_100'].iloc[i-1]:
            data['Signal'].iloc[i] = 1  # Buy signal
        elif data['EMA_9'].iloc[i] < data['EMA_100'].iloc[i] and data['EMA_9'].iloc[i-1] > data['EMA_100'].iloc[i-1]:
            data['Signal'].iloc[i] = -1  # Sell signal

    return data

def execute_trades(data):
    positions = []
    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and data['Signal'].iloc[i-1] == 0:
            positions.append("Buy")
        elif data['Signal'].iloc[i] == -1 and data['Signal'].iloc[i-1] == 0:
            positions.append("Sell")
        else:
            positions.append("Hold")

    return positions

# Define the symbol and time period
symbol = "RELIANCE"
start_date = "2020-01-01"
end_date = "2022-01-01"

# Retrieve historical data using nsetools
nse = Nse()
historical_data = nse.get_history(symbol, start=start_date, end=end_date)

# Create a DataFrame from the historical data
data = pd.DataFrame(historical_data)
data = data[['Date', 'Close']]

# Convert the date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the date column as the index
data.set_index('Date', inplace=True)

# Generate trade signals based on the strategy
data = generate_trade_signal(data)

# Execute trades based on the signals
positions = execute_trades(data)

# Create a DataFrame to display the trading positions
positions_df = pd.DataFrame({'Date': data.index, 'Position': positions})
positions_df = positions_df[positions_df['Position'] != "Hold"]

# Print the trading positions
print(positions_df)
