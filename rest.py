# Trying the bitvavo API
from python_bitvavo_api.bitvavo import Bitvavo
import json
import time
from datetime import datetime, timezone


class BitvavoImplementation:
    api_key = ""
    api_secret = ""
    bv = None
    bitvavo_socket = None

    def __init__(self):
        self.bv = Bitvavo(
            {
                "APIKEY": self.api_key,
                "APISECRET": self.api_secret,
            }
        )
        self.bitvavo_socket = self.bv.newWebsocket()
        self.bitvavo_socket.setErrorCallback(self.error_callback)

    def error_callback(self, error):
        print("Error: ", error)

    # Retrieve the data you need from Bitvavo in order to implement your trading logic. Use multiple workflows to return data to your callbacks.
    def trading_strat(self):
        self.bitvavo_socket.ticker24h({}, self.trading_strat_callback)

    # In your app you analyse data returned by the trading strategy, then make calls to Bitvavo to respond to market conditions.
    def trading_strat_callback(self, data):
        # going through the markets
        for market in data:
            match market["market"]:
                case "ZRX-EUR":
                    print("Eureka, the latets bid for ZRX-EUR is: ", market["bid"])
                    # case for placing an order:
                    # self.bitvavo_socket.placeOrder("ZRX-EUR", "buy", "limit", {"amount": "1", "price": "00001"}, self.order_placed_callback)
                case "a different market":
                    print("do something else")
                case _:
                    print("Not this one: ", market["market"])

    def order_placed_callback(self, response):
        # The order return parameters explain the quote and the fees for this trade.
        print("Order placed: ", json.dumps(response, indent=2))
        # Some more business logic

    # Socket are fast, but asynchronous. Keeop the socket open while you are trading
    def wait_and_close(self):
        limit = self.bv.getRemainingLimit()
        try:
            while limit > 0:
                time.sleep(1)
                limit = self.bv.getRemainingLimit()
                print("Remaining limit: ", limit)
        except KeyboardInterrupt:
            self.bitvavo_socket.closeSocket()

    def get_candles(self, markets=["BTC-EUR"]):
        candles = []
        for market in markets:
            candles.append(self.bv.candles(market, "5m"))
        for c in candles[0]:
            ts = datetime.utcfromtimestamp(c[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            c[0] = ts
            print("Fetched data:")
            print(json.dumps(c, indent=2))
        with open("solana.json", "w") as f:
            json.dump(candles, f)

    def get_data_block(self, start=None, end=None, market="BTC-EUR", interval="5m"):
        data = []
        start = start
        end = end
        limit = self.bv.getRemainingLimit()
        while limit > 0:
            d = self.bv.candles(market, "5m", start=start, end=end)
            print(d)
            # TODO: calculate the date for the next block - this can be done by the beginning time timestamp - limit size * interval etc.
            data.append(d)
            print(int(end.timestamp()))
            print(d[-1][0] / 1000)
            if int(end.timestamp()) >= d[-1][0] / 1000:
                break
            else:
                start = datetime.utcfromtimestamp(d[-1][0] / 1000)
                limit = self.bv.getRemainingLimit()
        return data

    def save_data(self, data, filename="data.json"):
        with open(filename, "w") as f:
            json.dump(data, f)

    def convert_timestamps(self, data):
        for d in data:
            ts = datetime.utcfromtimestamp(d[0] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            d[0] = ts
        return data


if __name__ == "__main__":
    bvavo = BitvavoImplementation()
    # bvavo.trading_strat()
    # bvavo.get_candles(["SOL-EUR"])
    end = datetime(2024, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
    start = datetime.now()
    data = bvavo.get_data_block(
        start=start, end=end, market="SOL-EUR"
    )  # 1.12.24 00:00:00
    print("Got data: ", len(data[0]))
    print("Limit: ", bvavo.bv.getRemainingLimit())
    data = bvavo.convert_timestamps(data[0])
    bvavo.save_data(data, "solana.json")
    bvavo.wait_and_close()
