class Stock:
	def __init__(self, symbol, stock_type, last_div, fixed_div, par_value):
		self.__symbol = symbol
		self.__stock_type = stock_type
		self.__lastDiv = last_div
		self.__fixedDiv = fixed_div
		self.__parValue = par_value
		self.validate_stock_info()

	def validate_stock_info(self):
		assert isinstance(self.__symbol, str), "Incorrect Stock Symbol : {}".format(self.__symbol)
		assert isinstance(self.__stock_type, str) and self.__stock_type in ('Common', 'Preferred'), \
			"Incorrect Stock Type : {}".format(self.__stock_type)
		assert isinstance(self.__lastDiv, (int, float)) and self.__lastDiv >= 0, \
			"Incorrect Last Dividend : {}".format(self.__lastDiv)
		if self.__stock_type == 'Preferred':
			assert (isinstance(self.__fixedDiv, str) and self.__fixedDiv.endswith('%')), \
				"Incorrect Fixed Dividend : {} for a Preferred Stock".format(self.__fixedDiv)
		elif self.__stock_type == 'Common':
			assert (not self.__fixedDiv), "Incorrect Fixed Dividend : {} for a Common stock".format(self.__fixedDiv)
		assert isinstance(self.__parValue, (int, float)) and self.__parValue > 0, \
			"Incorrect ParValue : {}".format(self.__parValue)
	
	def get_symbol(self):
		return self.__symbol
		
	def get_type(self):
		return self.__stock_type
		
	def get_last_dividend(self):
		return self.__lastDiv
		
	def get_fixed_dividend(self):
		return float(self.__fixedDiv.split('%')[0])/100
		
	def get_par_value(self):
		return self.__parValue

	def __str__(self):
		return "Stock(Symbol={}, Type={}, LastDividend(p)={}, FixedDividend={}, ParValue(p)={})".format(self.__symbol, self.__stock_type, self.__lastDiv, self.__fixedDiv,
												  self.__parValue)