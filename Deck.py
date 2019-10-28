import random
from Card import Card

class Deck:

	def __init__(self):
		self.cards = []

		#Card worth is based on number of cards that can beat it when lead

		#Hearts
		self.cards.append(Card('H','9','1'))
		self.cards.append(Card('H','10','2'))
		self.cards.append(Card('H','J','3'))
		self.cards.append(Card('H','Q','4'))
		self.cards.append(Card('H','K','5'))
		self.cards.append(Card('H','A','6'))

		#Diamonds
		self.cards.append(Card('D','9','1'))
		self.cards.append(Card('D','10','2'))
		self.cards.append(Card('D','J','3'))
		self.cards.append(Card('D','Q','4'))
		self.cards.append(Card('D','K','5'))
		self.cards.append(Card('D','A','6'))

		#Spades
		self.cards.append(Card('S','9','1'))
		self.cards.append(Card('S','10','2'))
		self.cards.append(Card('S','J','3'))
		self.cards.append(Card('S','Q','4'))
		self.cards.append(Card('S','K','5'))
		self.cards.append(Card('S','A','6'))

		#Clubs
		self.cards.append(Card('C','9','1'))
		self.cards.append(Card('C','10','2'))
		self.cards.append(Card('C','J','3'))
		self.cards.append(Card('C','Q','4'))
		self.cards.append(Card('C','K','5'))
		self.cards.append(Card('C','A','6'))

	def get_cards(self):
		return self.cards

	def draw_card(self):
		card = random.choice(self.cards)
		self.cards.remove(card)
		return card
