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

	def set_lead_with_trump(self,l):
		self.lead_with_trump = l

	def set_lead_with_ace(self,a):
		self.lead_with_ace = a

	def set_call_trump_round_one(self,o):
		self.call_trump_round_one = o 

	def set_call_trump_round_two(self, t):
		self.call_trump_round_two = t

	def set_count_on_partner(self, p):
		self.count_on_partner = p

	def set_go_alone(self, g):
		self.go_alone = g

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

	def set_team(self,team):
		self.team = team

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
			chosen = ''
			
			if chosen != '':
				self.toggle_called_trump()

		#For round two, the player has to choose whether or not to call one of the remainder of the suits trump or not
		else:
			all_suits = ['H','D','C','S']
			all_suits.remove(card_suit)
			chosen = 'H'
			
			if chosen != '':
				self.toggle_called_trump()

		return chosen

	def play_card(self,played_so_far):
		#If no cards have been played yet, the player must lead

		#Have to follow suit
		#Check first element in list
		#Get cards in hand that have the same suit as first card in list - make sure to check for 

		card_to_play = 'NA'

		available = self.hand.get_cards()
		trump_cards = [card for card in available if card.get_is_trump() == True]
		non_trump_aces = [card for card in available if card.get_worth() == 6]		

		#You are leading
		if not played_so_far:
			
			card_to_play = random.choice(self.hand.get_cards())

		else:
			#Let's figure out what has been played

			#The winning card is the highest worth card contingent upon the fact that the card follows suit or is trump
			leading_suit = played_so_far[0].get_suit()
			for played_card in played_so_far:
				if played_card.get_suit() != leading_suit:
					if not played_card.get_is_trump():
						played_card.set_worth(0)

			card_values = [card.get_worth() for card in played_so_far]

			#These stats will help us decide what to play
			winning_value = sorted(card_values, reverse = True)[0]
			winning_card = played_so_far[card_values.index(winning_value)]
			winning_team = 'NA'

			winning_card_index = played_so_far.index(winning_card)
			if winning_card_index == len(played_so_far) - 1:
				winning_team = self.team
			else:
				winning_team = 0 if self.team == 1 else 1

			#We must follow the suit of the card that was played first (led) if we want any points
			cards_following_suit = [card for card in available if card.get_suit() == leading_suit]

			#Add left bower to following suit list if trump was led
			if played_so_far[0].get_is_trump() == True:
				if True in [card.get_is_left() for card in available]:
					left_index = [card.get_is_left() for card in available].index(True)
					cards_following_suit.append(available[left_index])

			#If we do not have any cards that follow suit, then we can play any of our cards, inlcuding trump
			if not cards_following_suit:
				cards_following_suit = available

			#If we can't follow suit
			if not cards_following_suit:
				hand_values = [card.get_worth() for card in available]
				least_value = sorted(hand_values)[0]
				least_valuable = cards_following_suit[hand_values.index(least_valuable)]
				card_to_play = least_valuable
			else:
				how_many_cards = len(cards_following_suit)
				hand_values = [card.get_worth() for card in cards_following_suit]

				cards_in_order = []

				if how_many_cards == 1:
					most_value = sorted(hand_values, reverse = True)[0]
					most_valuable = cards_following_suit[hand_values.index(most_value)]
		
					cards_in_order = [most_valuable]

				if how_many_cards == 2:
					most_value = sorted(hand_values, reverse = True)[0]
					most_valuable = cards_following_suit[hand_values.index(most_value)]
					least_value = sorted(hand_values)[0]
					least_valuable = cards_following_suit[hand_values.index(least_value)]

					cards_in_order = [most_valuable,least_valuable]

				if how_many_cards == 3:
					most_value = sorted(hand_values, reverse = True)[0]
					most_valuable = cards_following_suit[hand_values.index(most_value)]
					middle_value = sorted(hand_values, reverse = True)[1]
					middle_valuable = cards_following_suit[hand_values.index(middle_value)]
					least_value = sorted(hand_values)[0]
					least_valuable = cards_following_suit[hand_values.index(least_value)]

					cards_in_order = [most_valuable,middle_valuable,least_valuable]

				if how_many_cards == 4:
					most_value = sorted(hand_values, reverse = True)[0]
					most_valuable = cards_following_suit[hand_values.index(most_value)]
					sec_most_value = sorted(hand_values, reverse = True)[1]
					sec_most_valuable = cards_following_suit[hand_values.index(sec_most_value)]
					middle_value = sorted(hand_values, reverse = True)[2]
					middle_valuable = cards_following_suit[hand_values.index(middle_value)]
					least_value = sorted(hand_values)[0]
					least_valuable = cards_following_suit[hand_values.index(least_value)]

					cards_in_order = [most_valuable,sec_most_valuable,middle_valuable,least_valuable]

				if how_many_cards == 5:
					most_value = sorted(hand_values, reverse = True)[0]
					most_valuable = cards_following_suit[hand_values.index(most_value)]
					sec_most_value = sorted(hand_values, reverse = True)[1]
					sec_most_valuable = cards_following_suit[hand_values.index(sec_most_value)]
					middle_value = sorted(hand_values, reverse = True)[2]
					middle_valuable = cards_following_suit[hand_values.index(middle_value)]
					sec_least_value = sorted(hand_values)[3]
					sec_least_valuable = cards_following_suit[hand_values.index(sec_least_value)]
					least_value = sorted(hand_values)[0]
					least_valuable = cards_following_suit[hand_values.index(least_value)]

					cards_in_order = [most_valuable,sec_most_valuable,middle_valuable,sec_least_valuable]
					
					
				#If our partner is winning the trick, let's see if we want to count on them
				#If a random number is generated that is less than the player's count on partner stat, the player will not one-up their partner
				count_on_partner = random.uniform(0,1) <= self.count_on_partner 

				#If going second
				if len(played_so_far) == 1:
					

					#Play least valuable card
					if count_on_partner:
						card_to_play =  cards_in_order[-1]

					#Play most valuable card
					else:
						card_to_play =  cards_in_order[0]

				#If going third 
				elif len(played_so_far) in [2]:
					#Partner has already played, and you're losing, play least valuable card that wins
					if winning_team != self.team:
						
						least_valuable_winning_card = next((card for card in reversed(cards_in_order) if card.get_worth() > winning_value), None)
						#If you have a card that can win, play it
						if least_valuable_winning_card != None:
							card_to_play = least_valuable_winning_card
						#If not, just throw off least valuable
						else:
							card_to_play = cards_in_order[-1]

					#If not, just throw off least valuable unless we are going to beat our partner
					else:

						#Play least valuable card
						if count_on_partner:
							card_to_play =  cards_in_order[-1]

						#Play most valuable card - no reason to play least valuable that will win if we're going all in!
						else:
							card_to_play =  cards_in_order[0]
					
				#If going fourth
				elif len(played_so_far) in [3]:
					
					#Partner has already played, and you're losing, play least valuable card that wins
					if winning_team != self.team:
						least_valuable_winning_card = next((card for card in reversed(cards_in_order) if card.get_worth() > winning_value), None)
						#If you have a card that can win, play it
						if least_valuable_winning_card != None:
							card_to_play = least_valuable_winning_card
							
						#If not, just throw off least valuable
						else:
							
							card_to_play = cards_in_order[-1]

					#If not, just throw off least valuable -- there is no reason to play a good card if you can't beat the winning card
					else:
						card_to_play = cards_in_order[-1]

		self.hand.remove_card(card_to_play)
		return card_to_play

