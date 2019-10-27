class Card:

	def __init__(self,suit,value,worth):
		self.suit = suit
		self.value = value
		self.is_trump = False
		self.worth = int(worth)
	
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
		if self.worth == 2:
			self.worth = 8
		#Jack
		if self.worth == 3:
			self.worth = 13
		#Queen
		if self.worth == 4:
			self.worth = 9
		#King
		if self.worth == 5:
			self.worth = 10
		#Ace
		if self.worth == 6:
			self.worth = 11

	def set_left(self):
		self.worth = 12

	def is_trump(self):
		return self.is_trump

	def get_worth(self):
		return self.worth
