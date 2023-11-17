from bookmapapi import API, BmDataTypes, BmChartTypes

import bookmap as bm

# Replace these with your actual API credentials
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Initialize Bookmap API
api = API(api_key, api_secret)

# Define trading parameters
target_profit = 100  # Target profit in USD
symbol = 'BTCUSD'   # Trading pair symbol

# Initialize trading variables
current_profit = 0
trade_active = False

# Define trading logic
def execute_trade(side, qty):
    global current_profit, trade_active

    if side == 'buy':
        current_profit -= qty  # Deduct buying cost
    elif side == 'sell':
        current_profit += qty  # Add selling revenue

    trade_active = False  # Reset trade flag

# Define callback for Bookmap updates
def on_bm_data_update(bm_data):
    global current_profit, trade_active

    # Accessing data from Bookmap
    last_price = bm_data[BmDataTypes.LAST_PRICE]

    # Your trading strategy logic here (replace with your actual strategy)
    if not trade_active and last_price < target_profit:
        # Place a buy order
        execute_trade('buy', last_price)
        trade_active = True

    elif trade_active and last_price >= target_profit:
        # Place a sell order
        execute_trade('sell', last_price)

# Connect to Bookmap API
api.start(on_bm_data_update=on_bm_data_update, chart_type=BmChartTypes.TOTAL_VIEW)

# Keep the script running
api.await_termination()
