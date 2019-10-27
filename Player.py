import random
from Hand import Hand

class Player:

	def __init__(self,team):
		self.player_id = random.randint(1000000,9000000)
		self.score = 0
		self.hand = Hand()
		self.dealer = False
		self.team = 0 if team in [0,2] else 1
		self.called_trump = False
		self.went_alone = False
		self.order = 'NA'

		#Player Stats
		#Stats increase for higher integers
		self.lead_with_trump = random.uniform(0,1)
		self.lead_with_ace = random.uniform(0,1)
		self.call_trump_round_one = random.uniform(0,1)
		self.call_trump_round_two = random.uniform(0,1)
		self.count_on_partner = random.uniform(0,1)
		self.go_alone = random.uniform(0,1)

	def get_player_id(self):
		return self.player_id

	def get_player_score(self):
		return self.score

	def add_to_player_score(self,amount):
		self.score = self.score + amount

	def reset_player_score(self):
		self.score = 0

	def get_hand(self):
		return self.hand

	def get_lead_with_trump(self):
		return self.lead_with_trump 

	def get_lead_with_ace(self):
		return self.lead_with_ace 

	def get_call_trump_round_one(self):
		return self.call_trump_round_one 

	def get_call_trump_round_two(self):
		return self.call_trump_round_two 

	def get_count_on_partner(self):
		return self.count_on_partner 

	def get_go_alone(self):
		return self.go_alone 

	def is_dealer(self):
		return self.dealer

	def get_team(self):
		return self.team

	def toggle_dealer(self):
		if self.dealer == True: 
			self.dealer = False
		else:
			self.dealer = True

	def reset_hand(self):
		self.hand = Hand()

	def get_called_trump(self):
		return self.called_trump

	def toggle_called_trump(self):
		if self.called_trump == True:
			self.called_trump = False
		else:
			self.called_trump = True

	def get_order(self):
		return self.order

	def set_order(self, order):
		self.order = order

	def get_went_alone(self):
		return self.went_alone

	def toggle_went_alone(self):
		if self.went_alone == True:
			self.went_alone = False
		else:
			self.went_alone = True

	#This function handles betting for trump at beginning of each round
	def bet(self,flipped_card,round):

		card_suit = flipped_card.get_desc()[0]
		card_value = flipped_card.get_desc()[1]

		#How do I decide whether to bet or not?
		#How many trump cards do I have in my hand?
		#How many non-trump aces do I have?
		#for card in self.get_hand().get_cards():
			#if card

		#For round one, the player has to choose whether or not to call the flipped card trump or not
		if round == 0:
			print(f'Player {self.player_id} selecting suit from {card_suit}')
			chosen = ''
			
			if chosen != '':
				self.toggle_called_trump()

		#For round two, the player has to choose whether or not to call one of the remainder of the suits trump or not
		else:
			all_suits = ['H','D','C','S']
			all_suits.remove(card_suit)
			print(f'Player {self.player_id} selecting suit from {all_suits}')
			chosen = 'H'
			
			if chosen != '':
				self.toggle_called_trump()

		return chosen

	def play_card(self,played_so_far):
		#If no cards have been played yet, the player must lead

		pass
		#Have to follow suit
		#Check first element in list
		#Get cards in hand that have the same suit as first card in list - make sure to check for 







