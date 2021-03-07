import datetime


class Trade:
	def __init__(self, stock, price, timestamp, qty, buy_sell):
		self.__stock = stock
		self.__price = price
		self.__timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		self.__qty = qty
		self.__buySell = buy_sell
		self.validate_trade_info()

	def __eq__(self, other):
		return ((self.__stock == other.__stock) and (self.__price == other.__price) and
				(self.__timestamp == other.__timestamp) and (self.__qty == other.__qty) and
				(self.__buySell == other.__buySell))

	def __lt__(self, other):
		return self.__timestamp < other.__timestamp

	def __hash__(self):
		return hash(str(self))

	def validate_trade_info(self):
		assert isinstance(self.__stock, str), "Incorrect Stock Symbol : {}".format(self.__stock)
		assert isinstance(self.__price, (int, float)) and self.__price > 0, "Incorrect Price : {}".format(self.__price)
		assert isinstance(self.__timestamp, datetime.datetime)
		assert isinstance(self.__qty, int) and self.__qty > 0, "Incorrect Quantity : {}".format(self.__qty)
		assert self.__buySell in ('B', 'S'), "Incorrect BuySell : {}".format(self.__buySell)
		
	def get_price(self):
		return self.__price
		
	def get_timestamp(self):
		return self.__timestamp
	
	def get_qty(self):
		return self.__qty
		
	def get_buy_sell(self):
		return self.__buySell

	def __str__(self):
		return "Trade(Stock={}, Price(p)={}, Timestamp(YYYY-MM-DD HH:MM:SS)={}, Quantity={}, BuySell={})".format(self.__stock, self.__price, self.__timestamp, self.__qty, self.__buySell)