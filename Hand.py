class Hand:

	def __init__(self):
		self.cards = []

	def get_cards(self):
		return self.cards

	def add_card(self,card):
		self.cards.append(card)

	def remove_card(self,card):
		self.cards.remove(card)

	def set_trump(self,trump_suit):
		for card in self.get_cards():
			if card.get_desc()[0] == trump_suit:
				card.set_trump()
				print(f'Set card {card.get_desc()} to trump')
				print(f'This card now has worth {card.get_worth()}')

			if trump_suit == 'H':
				left_bower = ['D','J']
			elif trump_suit == 'D':
				left_bower = ['H','J']
			elif trump_suit == 'C':
				left_bower = ['S','J']
			elif trump_suit == 'S':
				left_bower = ['C','J']

			
			if card.get_desc() == left_bower:
				print(f'Set left bower to {left_bower}')
				card.set_left()


		