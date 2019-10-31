import random
from Card import Card

class Deck:

	def __init__(self):
		self.cards = []

		#Card worth is based on number of cards that can beat it when lead

		#Hearts
		self.cards.append(Card('H','9','1','config/card_imgs/9H.jpg'))
		self.cards.append(Card('H','10','2','config/card_imgs/10H.jpg'))
		self.cards.append(Card('H','J','3','config/card_imgs/JH.jpg'))
		self.cards.append(Card('H','Q','4','config/card_imgs/QH.jpg'))
		self.cards.append(Card('H','K','5','config/card_imgs/KH.jpg'))
		self.cards.append(Card('H','A','6','config/card_imgs/AH.jpg'))

		#Diamonds
		self.cards.append(Card('D','9','1','config/card_imgs/9D.jpg'))
		self.cards.append(Card('D','10','2','config/card_imgs/10D.jpg'))
		self.cards.append(Card('D','J','3','config/card_imgs/JD.jpg'))
		self.cards.append(Card('D','Q','4','config/card_imgs/QD.jpg'))
		self.cards.append(Card('D','K','5','config/card_imgs/KD.jpg'))
		self.cards.append(Card('D','A','6','config/card_imgs/AD.jpg'))

		#Spades
		self.cards.append(Card('S','9','1','config/card_imgs/9S.jpg'))
		self.cards.append(Card('S','10','2','config/card_imgs/10S.jpg'))
		self.cards.append(Card('S','J','3','config/card_imgs/JS.jpg'))
		self.cards.append(Card('S','Q','4','config/card_imgs/QS.jpg'))
		self.cards.append(Card('S','K','5','config/card_imgs/KS.jpg'))
		self.cards.append(Card('S','A','6','config/card_imgs/AS.jpg'))

		#Clubs
		self.cards.append(Card('C','9','1','config/card_imgs/9C.jpg'))
		self.cards.append(Card('C','10','2','config/card_imgs/10C.jpg'))
		self.cards.append(Card('C','J','3','config/card_imgs/JC.jpg'))
		self.cards.append(Card('C','Q','4','config/card_imgs/QC.jpg'))
		self.cards.append(Card('C','K','5','config/card_imgs/KC.jpg'))
		self.cards.append(Card('C','A','6','config/card_imgs/AC.jpg'))

	def get_cards(self):
		return self.cards

	def draw_card(self):
		card = random.choice(self.cards)
		self.cards.remove(card)
		return card
