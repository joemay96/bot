# Trying the bitvavo API
from python_bitvavo_api.bitvavo import Bitvavo
import json
import time


class BitvavoImplementation:
    api_key = ""
    api_secret = ""
    bitvavo_engine = None
    bitvavo_socket = None

    def __init__(self):
        self.bitvavo_engine = Bitvavo(
            {
                "APIKEY": self.api_key,
                "APISECRET": self.api_secret,
            }
        )
        self.bitvavo_socket = self.bitvavo_engine.newWebsocket()
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
        limit = self.bitvavo_engine.getRemainingLimit()
        try:
            while limit > 0:
                time.sleep(1)
                limit = self.bitvavo_engine.getRemainingLimit()
        except KeyboardInterrupt:
            self.bitvavo_socket.closeSocket()

    # def get_data(self):


if __name__ == "__main__":
    bvavo = BitvavoImplementation()
    bvavo.trading_strat()
    bvavo.wait_and_close()
