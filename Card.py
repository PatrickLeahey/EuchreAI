class Card:

	def __init__(self,suit,value,worth):
		self.suit = suit
		self.value = value
		self.is_trump = False
		self.worth = int(worth)
		self.is_left = False
	
	def get_suit(self):
		return self.suit

	def get_value(self):
		return self.value

	def get_desc(self):
		return [self.suit,self.value]

	#6 was chosen because a 9 of trump can beat any non-trump ace
	def set_trump(self): 
		self.is_trump = True

		#Nine
		if self.worth == 1:
			self.worth = 7
		#Ten
		elif self.worth == 2:
			self.worth = 8
		#Jack
		elif self.worth == 3:
			self.worth = 13
		#Queen
		elif self.worth == 4:
			self.worth = 9
		#King
		elif self.worth == 5:
			self.worth = 10
		#Ace
		elif self.worth == 6:
			self.worth = 11

	def set_left(self):
		self.worth = 12
		self.is_trump = True
		self.is_left = True

	def get_is_trump(self):
		return self.is_trump

	def get_is_left(self):
		return self.is_left

	def get_worth(self):
		return self.worth

	def set_worth(self,worth):
		self.worth = worth
