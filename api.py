from python_bitvavo_api.bitvavo import Bitvavo
import pandas as pd
from datetime import datetime, timedelta
import time

# Initialize API connection
bitvavo = Bitvavo(
    {
        "APIKEY": "7545580e2eb29fd2314a63be5108906cecacdf794ae3c2ce1757d01803b23dae",
        "APISECRET": "01669294787779b1ba12be7afced13d07c41a178b6acbbb6c3cca5b6dd89b260eae82b68fa0bf7d1b9ef385b21b709fb6c56195bb58986837bff5967973bab49",
    }
)


# Fetch historical data
def fetch_historical_data(market, interval, start, end):
    """
    Fetch historical candlestick data for a specific market and time interval.
    :param market: Market symbol (e.g., 'BTC-EUR')
    :param interval: Candlestick interval (e.g., '1m', '5m', '1h', '1d')
    :param start: Start time in milliseconds
    :param end: End time in milliseconds
    :return: List of candlestick data
    """
    try:
        # start_iso = start.isoformat()
        # end_iso = end.isoformat()
        data = bitvavo.candles(symbol=market, interval=interval, start=start, end=end)
        return data
    except Exception as e:
        print("An error occurred:", e)
        return []


# # Example: Get the list of available markets
# try:
#     markets = bitvavo.markets({})
#     print("Available Markets:")
#     for market in markets:
#         print(market["market"])
# except Exception as e:
#     print("An error occurred:", e)

# # 	Example: Get account balance
# try:
#     balance = bitvavo.balance({})
#     print("\nAccount Balance:")
#     for asset in balance:
#         if float(asset["available"]) > 0 or float(asset["inOrder"]) > 0:
#             print(
#                 f"{asset['symbol']}: Available={asset['available']}, In Order={asset['inOrder']}"
#             )
# except Exception as e:
#     print("An error occurred:", e)


# Fetch and save data in chunks
def fetch_and_save_data(market, interval, start, end, filename):
    all_data = []

    current_start = start
    while current_start < end:
        # Calculate the end of the current chunk (1440 * 5 minutes = 7200 minutes = 5 days)
        current_end = min(current_start + timedelta(days=5), end)

        print(f"Fetching data from {current_start} to {current_end}...")

        remaining_limit = bitvavo.getRemainingLimit()
        print("Remaining limit:", remaining_limit)
        if remaining_limit <= 1:
            print(f"API rate limit reached. Waiting for 60 seconds...")
            time.sleep(60)  # Wait 60 seconds to reset the limit

        data = fetch_historical_data(market, interval, current_start, current_end)

        if data:
            all_data.extend(data)
        else:
            print(f"No data fetched for the interval {current_start} to {current_end}.")

        # Move to the next interval
        current_start = current_end

        # Sleep for 100 ms between API calls
        time.sleep(0.1)

        # Move to the next interval
        current_start = current_end

    # Convert data to DataFrame and save to CSV
    if all_data:
        df = pd.DataFrame(
            all_data, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], unit="ms"
        )  # Convert timestamp to readable format
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    else:
        print("No data collected.")


# Example usage
if __name__ == "__main__":
    # Market symbol and interval
    market = "SOL-EUR"  # Bitcoin to Euro
    interval = "5m"  # 1-hour candlesticks

    # Define time range (timestamps in milliseconds)
    start_time = datetime(2020, 1, 1, 0, 0, 0)  # Example: January 1, 2023 00:00:00 GMT
    # end_time = datetime(2024, 12, 28, 0, 0, 0)  # Example: January 2, 2023 00:00:00 GMT
    end_time = datetime.now()

    filename = "SOL_EUR.csv"

    fetch_and_save_data(market, interval, start_time, end_time, filename)

    # Fetch data
    # historical_data = fetch_historical_data(market, interval, start_time, end_time)
    # Print or process the data
    # if historical_data:
    # df = pd.DataFrame(
    # historical_data,
    # columns=["timestamp", "open", "high", "low", "close", "volume"],
    # )
    # df["timestamp"] = pd.to_datetime(
    # df["timestamp"], unit="ms"
    # )
    # print(df)
    # else:
    #     print("No data fetched.")
