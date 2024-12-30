# your local path to API keys and logs folder

# KEY: 7545580e2eb29fd2314a63be5108906cecacdf794ae3c2ce1757d01803b23dae
# SECRET: 01669294787779b1ba12be7afced13d07c41a178b6acbbb6c3cca5b6dd89b260eae82b68fa0bf7d1b9ef385b21b709fb6c56195bb58986837bff5967973bab49

path_key = "pathtokeydirectory"
path_logs = "pathtologsdirectory"

# sell_levels and buy_levels are lists of lists. It defines:
# [ [ percented of balance to trade, price level, unique userref ], [ ... ] ]
sell_levels = [[0.5, 1.008, 101], [0.5, 1.002, 102]]
buy_levels = [[0.5, 0.992, 201], [0.3, 0.996, 202], [0.2, 0.998, 203]]

# pairs is a list if list that defines tradable pairs and assets:
# [ [ base asset, quote asset, altname from AssetPairs endpoint ], [ ... ] ]
pairs = [["USDC", "ZUSD", "USDCUSD"]]
