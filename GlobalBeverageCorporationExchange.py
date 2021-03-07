import datetime
from Trade import Trade
from Stock import Stock
from Borg import Borg
from collections import defaultdict
from sortedcontainers import SortedSet


class GlobalBeverageCorporationExchange(Borg):  # using Borg's pattern to make sure Exchange objects share trades
    stock_data = {'TEA': Stock('TEA', 'Common', 0, None, 100),
                  'POP': Stock('POP', 'Common', 8, None, 100),
                  'ALE': Stock('ALE', 'Common', 23, None, 60),
                  'GIN': Stock('GIN', 'Preferred', 8, '2%', 100),
                  'JOE': Stock('JOE', 'Common', 13, None, 250)
                  }  # more stocks can be added. add_stock method can be used to add new stocks but beyond scope here.

    def __init__(self, trades=None):
        super().__init__()
        if trades:
            self.trades = trades
        else:
            if not hasattr(self, "trades"):
                self.trades = defaultdict(SortedSet)

    @staticmethod
    def calculate_dividend_yield(stock_symbol, price):
        try:
            if stock_symbol in GlobalBeverageCorporationExchange.stock_data:
                print('Calculating Dividend Yield for stock:', stock_symbol)
                stk = GlobalBeverageCorporationExchange.stock_data[stock_symbol]
                if price <= 0:
                    raise Exception("Invalid stock price : " + str(price) + " for stock : " + stock_symbol)
                if stk.get_type() == 'Common':
                    return round(stk.get_last_dividend() / price, 3)
                elif stk.get_type() == 'Preferred':
                    return round((stk.get_fixed_dividend() * stk.get_par_value()) / price, 3)
            else:
                raise Exception("Invalid Stock Symbol : " + stock_symbol)
        except Exception as err:
            print("ERROR: Unable to calculate Dividend Yield due to", err)
            exit(1)

    @staticmethod
    def calculate_pe_ratio(stock_symbol, price):
        try:
            if stock_symbol in GlobalBeverageCorporationExchange.stock_data:
                print('Calculating P/E ratio for stock:', stock_symbol)
                stk = GlobalBeverageCorporationExchange.stock_data[stock_symbol]
                if price <= 0:
                    raise Exception("Invalid stock price : " + str(price) + " for stock : " + stock_symbol)
                return round(price / stk.get_last_dividend(), 3)
            else:
                raise Exception("Invalid Stock Symbol : " + stock_symbol)
        except ZeroDivisionError:
            print("ERROR: Unable to calculate P/E ratio due to Last Dividend being Zero for stock : " + stock_symbol)
            exit(1)
        except Exception as err:
            print("ERROR: Unable to calculate P/E ratio due to", err)
            exit(1)

    def record_trade(self, stock_symbol, price, timestamp, qty, buy_sell):
        try:
            if stock_symbol in GlobalBeverageCorporationExchange.stock_data:
                print('Recording Trade :', Trade(stock_symbol, price, timestamp, qty, buy_sell), 'on the Exchange')
                self.trades[stock_symbol].add(Trade(stock_symbol, price, timestamp, qty, buy_sell))
            else:
                raise Exception("Invalid Stock Symbol : " + stock_symbol)
        except Exception as err:
            print("ERROR: Unable to record trade due to", err)
            exit(1)

    def price_reporter(price_calculator):  # decorator on the price_calculator method for reporting the price in GBP
        def report(self, *args):
            return str(round(price_calculator(self, *args) / 100, 3)) + " GBP"

        return report

    def __calculate_volume_weighted_stock_price(self, stock_symbol, current_timestamp=None, timestamp_5_min_back=None):
        # private method. Reports price in pennies.
        try:
            if stock_symbol in GlobalBeverageCorporationExchange.stock_data:
                if not current_timestamp:
                    current_timestamp = datetime.datetime.now()
                if not timestamp_5_min_back:
                    timestamp_5_min_back = current_timestamp - datetime.timedelta(minutes=5)
                print("Current Timestamp: ", current_timestamp)
                print("5minback Timestamp: ", timestamp_5_min_back)
                sum_qty = 0
                sum_product_price_qty = 0
                for trade in reversed(self.trades[stock_symbol]):  # traversing the trades in reverse order of timestamp
                    if timestamp_5_min_back <= trade.get_timestamp() <= current_timestamp:
                        print("Trade considered for calculating Volume-Weighed-Stock-Price:", trade)
                        sum_qty += trade.get_qty()
                        sum_product_price_qty += (trade.get_price() * trade.get_qty())
                    elif trade.get_timestamp() < timestamp_5_min_back:
                        break
                if sum_qty == 0:
                    return 1  # If no trades present for relevant stock, assuming Volume-Weighted-Price to be 1 penny
                return sum_product_price_qty / sum_qty
            else:
                raise Exception("Invalid Stock Symbol : " + stock_symbol)
        except Exception as err:
            print("ERROR: Unable to calculate Volume-Weighted-Stock-Price due to", err)
            exit(1)

    @price_reporter
    def calculate_volume_weighted_stock_price(self, stock_symbol):  # wrapper to report price in GBP outside
        print('Calculating Volume-Weighted-Stock-Price for stock:', stock_symbol)
        return self.__calculate_volume_weighted_stock_price(stock_symbol)

    @price_reporter
    def calculate_gbce_all_share_index(self):  # method to report GBCE All Share Index in GBP.
        current_timestamp = datetime.datetime.now()
        timestamp_5_min_back = current_timestamp - datetime.timedelta(minutes=5)
        print('Calculating GlobalBeverageCorporationExchange All Share Index:')
        gbce_all_share_index = 1  # default GBCE All share index is 1 penny
        for stock_symbol in GlobalBeverageCorporationExchange.stock_data:
            gbce_all_share_index *= self.__calculate_volume_weighted_stock_price(stock_symbol, current_timestamp,
                                                                                 timestamp_5_min_back)
        n = len(GlobalBeverageCorporationExchange.stock_data)
        return gbce_all_share_index ** (1.0 / n)

    @classmethod
    def add_stock(cls, new_stock):
        if isinstance(new_stock, Stock):
            stock_symbol = new_stock.get_symbol()
            if stock_symbol not in cls.stock_data:
                print("Adding new Stock:", stock_symbol, "to the Exchange")
                cls.stock_data[stock_symbol] = new_stock
            else:
                print("Stock with symbol:", stock_symbol, "already exists on Exchange")
                exit(1)
        else:
            print("Invalid stock object:", type(new_stock), "cannot be added to the Exchange")
            exit(1)


if __name__ == '__main__':
    gbce = GlobalBeverageCorporationExchange()
    gbce.add_stock(Stock('KTB', 'Preferred', 20, '4%', 500))
    gbce.add_stock(Stock('REL', 'Common', 1, None, 100))
    print("Showing all Active Stocks on GlobalBeverageStockExchange: ")
    for key, value in gbce.stock_data.items():
        print(value)

    print(gbce.calculate_dividend_yield('POP', 200))
    print(gbce.calculate_dividend_yield('TEA', 10))
    print(gbce.calculate_dividend_yield('ALE', 100))
    print(gbce.calculate_dividend_yield('GIN', 1000.67))
    print(gbce.calculate_dividend_yield('JOE', 500.05))

    print(gbce.calculate_pe_ratio('POP', 200))
    print(gbce.calculate_pe_ratio('GIN', 1000.67))
    print(gbce.calculate_pe_ratio('JOE', 500.05))
    # print(gbce.calculate_pe_ratio('TEA', 10))
    # print(gbce.calculate_pe_ratio('ALE', -100))

    gbce.record_trade('POP', 200, '2021-03-07 23:51:15', 12, 'B')
    gbce.record_trade('POP', 200, '2021-03-07 23:51:14', 12, 'S')
    gbce.record_trade('TEA', 425, '2021-03-07 23:50:13', 100, 'S')
    gbce.record_trade('TEA', 430, '2021-03-07 23:50:14', 100, 'B')
    gbce.record_trade('ALE', 325, '2021-03-07 23:50:17', 500, 'B')
    gbce.record_trade('ALE', 320, '2021-03-07 23:50:18', 500, 'S')
    gbce.record_trade('GIN', 500, '2021-03-07 23:49:19', 200, 'B')
    gbce.record_trade('GIN', 495, '2021-03-07 23:49:20', 200, 'S')
    gbce.record_trade('JOE', 753, '2021-03-07 23:49:15', 300, 'B')
    gbce.record_trade('JOE', 750, '2021-03-07 23:49:16', 300, 'S')
    gbce.record_trade('KTB', 1500, '2021-03-07 23:48:47', 50, 'B')
    gbce.record_trade('KTB', 1500, '2021-03-07 23:48:27', 50, 'S')
    gbce.record_trade('REL', 152, '2021-03-07 23:51:56', 50, 'B')
    gbce.record_trade('REL', 150, '2021-03-07 23:04:51', 50, 'S')
    gbce.record_trade('REL', 150, '2021-03-07 23:04:51', 50, 'S')

    gbce2 = GlobalBeverageCorporationExchange()
    print("Trades available to another object of GBCE: ")
    for stk, trds in gbce2.trades.items():
        print(stk)
        for trd in trds:
            print(trd)  # same set of trades available to another object of GBCE
    print(gbce.calculate_volume_weighted_stock_price('TEA'))
    print(gbce2.calculate_volume_weighted_stock_price('TEA'))
    print(gbce.calculate_volume_weighted_stock_price('POP'))
    print(gbce.calculate_volume_weighted_stock_price('ALE'))
    print(gbce.calculate_volume_weighted_stock_price('GIN'))
    print(gbce.calculate_volume_weighted_stock_price('JOE'))
    print(gbce.calculate_volume_weighted_stock_price('KTB'))
    print(gbce.calculate_volume_weighted_stock_price('REL'))

    print(gbce.calculate_gbce_all_share_index())
    print(gbce2.calculate_gbce_all_share_index())
