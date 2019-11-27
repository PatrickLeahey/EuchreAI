import random
from Deck import Deck
from Table import Table
from Display import Display
import config.play_config as con
import pygame
import datetime

class Game:
	#Instantiate Game Instance
	def __init__(self):
		self.game_id = random.randint(1000000,9000000)
		self.deck = Deck()
		self.table = Table()
		self.user = False
		self.user_player = None
		self.display = None
		
		random.seed(datetime.datetime.now().strftime('%S'))

	def get_players(self):
		return self.table.get_players()

	def set_teams(self):
		for i,player in zip(range(4),self.table.get_players()):
			if i in [0,2]:
				player.set_team(0) 
			else:
				player.set_team(1)

	#We will want to provide the players to the games after the first round
	def provide_players(self,players):
		self.table.set_players(players)	

	#Deal the cards to the players
	#5 cards each
	def deal(self):

		#GUI version
		if self.user:
			self.display.pump()
			game_on = True
			while game_on == True:

				self.display.prompt_event()

				for event in self.display.get_events():

					if event.type == pygame.QUIT:
						self.display.quit()

					else:
						for player in self.table.get_players():
							for _ in range(5):
								player.get_hand().add_card(self.deck.draw_card())

							#Cards you were dealt - display image for each and end while loop
						rects = self.display.display_hand(self.user_player.get_hand().get_cards())
						#Add rects to Hand object 
						self.user_player.get_hand().set_rects(rects)
						return 

		#Non-GUI version
		for player in self.table.get_players():
			for _ in range(5):
				player.get_hand().add_card(self.deck.draw_card())

	def get_display(self):
		return self.display

	#Following each round, the dealer rotates up
	def next_dealer(self):
		#There will not be a set dealer in the first round
		#After this point, there should only be one dealer
		#Dealer rotates up

		dealer_index = 0

		if True in [player.is_dealer() for player in self.table.get_players()]:
			dealer_index = [player.is_dealer() for player in self.table.get_players()].index(True)

			self.table.get_players()[dealer_index].toggle_dealer()
			if self.user:
				self.display.unset_dealer(self.table.get_players()[dealer_index])

			if dealer_index != 3:
				lead_index = dealer_index + 1
				self.table.get_players()[lead_index].toggle_dealer()
				if lead_index != 3:
					self.table.set_first(self.table.get_players()[lead_index])
				else:
					self.table.set_first(self.table.get_players()[0])

			else:
				self.table.get_players()[0].toggle_dealer()
				self.table.set_first(self.table.get_players()[1])
		else:

			#Random first dealer
			deal = random.randint(0,3)
			first = 0 if deal == 3 else deal + 1

			self.table.get_players()[deal].toggle_dealer()
			self.table.set_first(self.table.get_players()[first])

		if self.user:
			#If user is dealer
			if self.table.get_players()[[player.is_dealer() for player in self.table.get_players()].index(True)].get_is_user():
				self.display.update_announcement('You are now dealer')
			else:
				dealer_name = self.table.get_players()[[player.is_dealer() for player in self.table.get_players()].index(True)].get_name()
				self.display.update_announcement(f'{dealer_name} is now dealer')

		dealer = self.table.get_players()[[player.is_dealer() for player in self.table.get_players()].index(True)]
		if self.user:
			self.display.set_dealer(dealer)

		return dealer_index
		
	#A trick involves 4 cards
	def play_trick(self):

		#GUI version
		if self.user:
			self.display.pump()
			game_on = True
			while game_on == True:

				self.display.prompt_event()

				for event in self.display.get_events():

					if event.type == pygame.QUIT:
						self.display.quit()

					else:

						#Each player will get a chance to lay down a card, in order
						#The first time, the player after the dealer will lead
						#THEN, the winner of the previous trick will lead

						#This list keeps track of the cards played so far so that the player will know to follow suit and what needs to be beaten
						played_so_far = []

						for player in self.table.get_players():

							#If the player's teammate went alone, skip their turn
							#Otherwise, do the following
							if True not in [p.get_went_alone() for p in self.table.get_players() if player.get_team() == p.get_team()] \
								and not self.user_player.get_went_alone():

								self.display.set_current(player)

								if player == self.user_player:
									if not played_so_far:
										self.display.update_announcement("It's your turn to lead")

									played_so_far.append(self.display.select_card(self.user_player,played_so_far))
									self.display.add_card_to_table(played_so_far[-1].get_img_path(),len(played_so_far),False)
									self.display.display_hand(self.user_player.get_hand().get_cards())
								
								else:
									played_so_far.append(player.play_card(played_so_far))
						
									self.display.update_announcement(f"Player {player.get_name()} played {played_so_far[-1].get_value()} of {played_so_far[-1].get_suit()}'s")
									self.display.add_card_to_table(played_so_far[-1].get_img_path(),len(played_so_far),False)
									
									self.display.wait(750)

								self.display.unset_current(player)


						#Generate score of format score = [0,1] or [1,0] as only one team can win
						#We will optimize for team win rather than individual win because the goal of the game is for the team to win
						score = []

						#The winning card is the highest worth card contingent upon the fact that the card follows suit or is trump
						leading_suit = played_so_far[0].get_suit()
						for played_card in played_so_far:
							if played_card.get_suit() != leading_suit:
								if not played_card.get_is_trump():
									played_card.set_worth(0)

						card_values = [card.get_worth() for card in played_so_far]
						winning_value = sorted(card_values, reverse = True)[0]
						winning_card = played_so_far[card_values.index(winning_value)]

						#We want to let the winner of the trick lead the next trick
						#We need to get the player that won the trick to do this
						#We need to find out if anyone went alone to help us not misidentify the winning player
						partner_went_alone_index = None

						for player,i in zip(self.table.get_players(),range(len(self.table.get_players()))):
							if player.get_went_alone():
								if i == 0:
									partner_went_alone_index = 2
								elif i == 1:
									partner_went_alone_index = 3
								elif i == 2:
									partner_went_alone_index = 0
								else:
									partner_went_alone_index = 1

						winner_index = played_so_far.index(winning_card)

						if partner_went_alone_index == None:
							#Partner did not go alone
							#Set winner of trick first for next round
							self.table.set_first(self.table.get_players()[winner_index])
						else:
							#Partner went alone
							#Set winner of trick first for next round
							#We account for the missing card by adding 1
							if winner_index >= partner_went_alone_index:
								self.table.set_first(self.table.get_players()[winner_index+1])
							else:
								self.table.set_first(self.table.get_players()[winner_index])

						winning_team = None
						if played_so_far.index(winning_card) in [0,2]:
							winning_team = self.table.get_players()[0].get_team()
						else:
							winning_team = self.table.get_players()[1].get_team()

						if self.user:
							self.display.update_announcement(f'Team {winning_team} won the trick!')
							self.display.wait(750)

						if winning_team == 0:
							score = [1,0]
						else:
							score = [0,1]

						#Add points to player score 
						for player in self.table.get_players():
							player.add_to_player_score(score[player.get_team()])

						self.display.clear_table()
						return score

		#Non-GUI version
		else:

			#Each player will get a chance to lay down a card, in order
			#The first time, the player after the dealer will lead
			#THEN, the winner of the previous trick will lead

			#This list keeps track of the cards played so far so that the player will know to follow suit and what needs to be beaten
			played_so_far = []

			for player in self.table.get_players():

				#If the player's teammate went alone, skip their turn
				#Otherwise, do the following
				if True not in [p.get_went_alone() for p in self.table.get_players() if player.get_team() == p.get_team()]:
					played_so_far.append(player.play_card(played_so_far))

			#Generate score of format score = [0,1] or [1,0] as only one team can win
			#We will optimize for team win rather than individual win because the goal of the game is for the team to win
			score = []

			#The winning card is the highest worth card contingent upon the fact that the card follows suit or is trump
			leading_suit = played_so_far[0].get_suit()
			for played_card in played_so_far:
				if played_card.get_suit() != leading_suit:
					if not played_card.get_is_trump():
						played_card.set_worth(0)

			card_values = [card.get_worth() for card in played_so_far]
			winning_value = sorted(card_values, reverse = True)[0]
			winning_card = played_so_far[card_values.index(winning_value)]
			winning_team = 'NA'
			if played_so_far.index(winning_card) in [0,2]:
				winning_team = self.table.get_players()[0].get_team()
			else:
				winning_team = self.table.get_players()[1].get_team()

			if winning_team == 0:
				score = [1,0]
			else:
				score = [0,1]

			#Add points to player score 
			for player in self.table.get_players():
				player.add_to_player_score(score[player.get_team()])

			return score

	#A round involves 20 cards and is equal to 5 tricks
	#Teams can receive 1, 2, or 4 points for each team
	def play_round(self):
		if self.user:

			game_on = True
			while game_on == True:
				self.display.prompt_event()

				for event in self.display.get_events():
					if event.type == pygame.QUIT:
						self.display.quit()

					else:
						
						#Initial deal of cards
						dealer_index = self.next_dealer()
						self.deal()

						self.display.pump()
						#Remainder of cards in self.deck (4) are the kitty -- select the card on top
						flipped_card = self.deck.get_cards()[3]

						self.display.pump()

						self.display.add_card_to_table(flipped_card.get_img_path(),4,True)

						self.display.pump()

						self.display.update_announcement('Dealer has dealt!')

						trump_suit = ''
						dealer_team = ''

						#First roound betting
						picked_up = False
						picked_up_round = ''

						self.display.display_suits(flipped_card.get_suit())

						for player in self.table.get_players():
							self.display.set_current(player)

							#Which team is dealing - we want to be able to tell this information to the players when they're betting
							dealer_team = [player.get_team() for player in self.table.get_players() if player.is_dealer()][0]

							if player == self.user_player:
								bet = self.display.select_suit(flipped_card.get_suit())
								
							else:
								bet = player.bet(flipped_card,dealer_team,0)

								if bet != '':
									if bet == 'H':
										s = 'Hearts'
									elif bet == 'D':
										s = 'Diamonds'
									elif bet == 'C':
										s = 'Clubs'
									else:
										s = 'Spades'

									self.display.update_announcement(f'Player {player.get_name()} chose {s} as trump suit for team {player.get_team()}')
									self.display.wait(1000)

							if bet != '':
								picked_up = True
								picked_up_round = 0
								trump_suit = flipped_card.get_desc()[0]
								self.display.update_suit(trump_suit)
								self.display.unset_current(player)

								break

							else:
								if self.user:
									self.display.update_announcement(f'Player {player.get_name()} passed')
									self.display.unset_current(player)
									self.display.wait(1000)

						#Second round betting
						if picked_up == False:
							self.display.clear_table()

							all_suits = ['H','D','C','S']
							all_suits.remove(flipped_card.get_suit())

							self.display.display_suits(all_suits)

							for player in self.table.get_players():
								self.display.set_current(player)

								if player == self.user_player:
									bet = self.display.select_suit(all_suits)
								
								else:
									bet = player.bet(flipped_card,dealer_team,1)

									if bet != '':
										if bet == 'H':
											s = 'Hearts'
										elif bet == 'D':
											s = 'Diamonds'
										elif bet == 'C':
											s = 'Clubs'
										else:
											s = 'Spades'

										self.display.wait(1000)
										self.display.update_announcement(f'Player {player.get_name()} chose {s} as trump suit for team {player.get_team()}')
										

								if bet != '':
									self.display.clear_table()
									picked_up = True
									trump_suit = bet
									self.display.update_suit(trump_suit)
									self.display.unset_current(player)

									break
								else:
									if self.user:
										self.display.wait(1000)
										self.display.update_announcement(f'Player {player.get_name()} passed')
										self.display.unset_current(player)


						if trump_suit != '':
							self.display.clear_table()
							for player in self.table.get_players():
								player.get_hand().set_trump(trump_suit)

							if picked_up_round == 0:
								#Dealer drops one of their cards
								#Dealer picks up flipped card
								dealer_index = [player.is_dealer() for player in self.table.get_players()].index(True)
								#Dealer decide which card to drop -- their worst card unless the flipped card is worse than all
								dealer_cards = self.table.get_players()[dealer_index].get_hand().get_cards()
								dealer_card_vals = [card.get_worth() for card in dealer_cards]
								dealer_worst_card = sorted(dealer_card_vals)[0]
								remove_card = dealer_cards[dealer_card_vals.index(dealer_worst_card)]
								if flipped_card.get_worth() + 6 < remove_card.get_worth():
									remove_card = flipped_card
								self.table.get_players()[dealer_index].get_hand().add_card(flipped_card)
								self.table.get_players()[dealer_index].get_hand().remove_card(remove_card)

							score = [0,0]
							for _ in range(5):
								score0,score1 = self.play_trick()
								score[0] = score[0] + score0
								score[1] = score[1] + score1
								self.display.update_trick_score(score)
							
							#Score based on number of tricks won

							#Need to know this so we can see if a team got euchred or not
							#And whether one player went alone
							team_called_trump = 'NA'
							went_alone = 'NA'
							for player in self.table.get_players():
								if player.get_called_trump():
									team_called_trump = player.get_team()
									if player.get_went_alone():
										went_alone = player.get_team()


							self.display.update_trick_score([0,0])

							if score[0] > score[1]:
								if self.user:
									self.display.update_announcement('Team 0 won this round')
									
								if score[0] == 5:
									if self.user:
										self.display.update_announcement('Team 0 won all 5')
										
									return [2,0]
								elif team_called_trump == 1:
									if self.user:
										self.display.update_announcement('Team 0 euchred Team 1')
										
									return [2,0]
								elif went_alone == 0 and score[0] == 5:
									if self.user:
										self.display.update_announcement('Team 0 went alone and won all 5')
										
									return [4,0]
								else: 
									return [1,0]

							else:
								if self.user:
									self.display.update_announcement('Team 1 won this round')
									
								if score[1] == 5:
									if self.user:
										self.display.update_announcement('Team 1 won all 5')

									return [0,2]
								elif team_called_trump == 0:
									if self.user:
										self.display.update_announcement('Team 1 euchred Team 0')

									return [0,2]
								elif went_alone == 1 and score[1] == 5:
									if self.user:
										self.display.update_announcement('Team 1 went alone and won all 5')

									return [0,4]
								else: 

									return [0,1]
							
						#The suit was not set during betting
						else:
							if self.user:
								self.display.update_announcement('Neither team wanted to bet')
								
							return [0,0]
		else:

			#Initial deal of cards
			dealer_index = self.next_dealer()
			self.deal()

			#Remainder of cards in self.deck (4) are the kitty -- select the card on top
			flipped_card = self.deck.get_cards()[3]

			trump_suit = ''
			dealer_team = ''

			#First roound betting
			picked_up = False
			picked_up_round = ''

			for player in self.table.get_players():
				#Which team is dealing - we want to be able to tell this information to the players when they're betting
				dealer_team = [player.get_team() for player in self.table.get_players() if player.is_dealer()][0]

				bet = player.bet(flipped_card,dealer_team,0)
				if bet != '':
					picked_up = True
					picked_up_round = 0
					trump_suit = flipped_card.get_desc()[0]
					break

			#Second round betting
			if picked_up == False:
				for player in self.table.get_players():
					bet = player.bet(flipped_card,dealer_team,1)
					if bet != '':
						picked_up = True
						trump_suit = bet
						break
			

			if trump_suit != '':

				for player in self.table.get_players():
					player.get_hand().set_trump(trump_suit)

				if picked_up_round == 0:
					#Dealer drops one of their cards
					#Dealer picks up flipped card
					dealer_index = [player.is_dealer() for player in self.table.get_players()].index(True)
					#Dealer decide which card to drop -- their worst card unless the flipped card is worse than all
					dealer_cards = self.table.get_players()[dealer_index].get_hand().get_cards()
					dealer_card_vals = [card.get_worth() for card in dealer_cards]
					dealer_worst_card = sorted(dealer_card_vals)[0]
					remove_card = dealer_cards[dealer_card_vals.index(dealer_worst_card)]
					if flipped_card.get_worth() + 6 < remove_card.get_worth():
						remove_card = flipped_card
					self.table.get_players()[dealer_index].get_hand().add_card(flipped_card)
					self.table.get_players()[dealer_index].get_hand().remove_card(remove_card)

				score = [0,0]
				for _ in range(5):
					score0,score1 = self.play_trick()
					score[0] = score[0] + score0
					score[1] = score[1] + score1
				
				#Score based on number of tricks won

				#Need to know this so we can see if a team got euchred or not
				#And whether one player went alone
				team_called_trump = None
				went_alone = None
				for player in self.table.get_players():
					if player.get_called_trump():
						team_called_trump = player.get_team()
						if player.get_went_alone():
							went_alone = player.get_team()


				if score[0] > score[1]:
					if score[0] == 5:
						return [2,0]
					elif team_called_trump == 1:
						return [2,0]
					elif went_alone == 0 and score[0] == 5:
						return [4,0]
					else: 
						return [1,0]

				else:
					if score[1] == 5:
						return [0,2]
					elif team_called_trump == 0:
						return [0,2]
					elif went_alone == 1 and score[1] == 5:
						return [0,4]
					else: 
						return [0,1]
				
			#The suit was not set during betting
			else:
				return [0,0]

	#A game is over when one team reaches 10 points
	def play_game(self):

		if self.user:

			self.display.pump()

			score = [0,0]
			num_round = 1

			game_on = True
			while score[0] < 10 and score[1] < 10 and game_on == True:

				self.display.prompt_event()
				for event in self.display.get_events():
					if event.type == pygame.QUIT:
						self.display.quit()

					else:
						round_score = self.play_round()

						score = [score[0] + round_score[0], score[1] + round_score[1]]

						if self.user:
							self.display.update_announcement(f'End of round number {num_round}')
							self.display.update_score(score)
	
						self.deck = Deck()
						for player in self.table.get_players():
							player.reset_hand()

							if player.is_dealer():
								player.toggle_dealer()

							if player.get_called_trump():
								player.toggle_called_trump()

								if player.get_went_alone():
									player.toggle_went_alone()

						num_round = num_round + 1
						self.display.update_score([0,0])


			winner_number = 0 if score[0] > score[1] else 1
			
			self.display.update_announcement(f'GAME OVER! Team {winner_number} is victorious!')


		#If there is no user
		else:
			score = [0,0]
			num_round = 1
			while score[0] < 10 and score[1] < 10:
				round_score = self.play_round()

				score = [score[0] + round_score[0], score[1] + round_score[1]]

				self.deck = Deck()
				for player in self.table.get_players():
					player.reset_hand()

					if player.is_dealer():
						player.toggle_dealer()

					if player.get_called_trump():
						player.toggle_called_trump()

						if player.get_went_alone():
							player.toggle_went_alone()

				num_round = num_round + 1

	def create_user(self):
		self.user = True
		self.user_player = self.table.get_players()[2]
		self.display = Display()

		seats = [(int(self.display.get_width()//2),int(self.display.get_height()//9)), \
			(int(self.display.get_width()//10*8.5),int(self.display.get_height()//2.4)), \
			(int(self.display.get_width()//2),int(self.display.get_height()//10*7.3)), \
			(int(self.display.get_width()//10*1.5),int(self.display.get_height()//2.4))]

		self.display.pump()

		#Give players fun names
		names = []
		for i,player in zip(range(4),self.table.get_players()):
			named = False
			player.set_seat(seats[i])
			while named == False:
				name = random.choice(con.names)
				if name not in names:
					player.set_name(name)
					names.append(name)
					named = True

		self.display.pump()

		background = pygame.Surface((self.display.get_width(),self.display.get_height()))
		background.fill((0,128,0))
		background_rect = background.get_rect()
		background_rect.center = (self.display.get_width()//2,self.display.get_height()//2)
		self.display.blit(background,background_rect)
		self.display.flip()

		rects = []

		#Create title text 'EuchreAI'
		font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//12) 
		text = font.render('EuchreAI', True, (255,255,255)) 
		text_rect = text.get_rect()  
		text_rect.center = (self.display.get_width()//2,self.display.get_height()//12) 
		self.display.blit(text,text_rect) 
		rects.append(text_rect)

		#Image
		image = pygame.image.load('config/card_imgs/title_img.png')
		image = pygame.transform.smoothscale(image, (self.display.get_width()//2,self.display.get_height()//2)).convert_alpha()
		image_rect = image.get_rect()
		image_rect.center = (self.display.get_width()//2,self.display.get_height()//2)
		self.display.blit(image,image_rect)
		rects.append(image_rect)

		#Button
		button = pygame.Surface((self.display.get_width()//5,self.display.get_height()//12))
		button.fill((245,245,245))
		button_rect = button.get_rect()
		button_rect.center = (self.display.get_width()//2,self.display.get_height()//10*9)
		self.display.blit(button,button_rect)
		rects.append(button_rect)

		#Button text
		font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//12) 
		button_text = font.render('PLAY', True, (0,0,0)) 
		button_text_rect = button_text.get_rect()  
		button_text_rect.center = button_rect.center
		self.display.blit(button_text,button_text_rect) 
		rects.append(button_text_rect)

		self.display.display_credit_and_title()

		#Update specific rectangles
		self.display.update(rects)

		game_on = True

		while game_on == True:
			self.display.prompt_event()
			for event in self.display.get_events():
				if event.type == pygame.QUIT:
					self.display.quit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if button_rect.collidepoint(pos):
						background = pygame.Surface((self.display.get_width(),self.display.get_height()))
						background.fill((0,128,0))
						background_rect = background.get_rect()
						background_rect.center = (self.display.get_width()//2,self.display.get_height()//2)
						self.display.blit(background,background_rect)
						self.display.display_credit_and_title()
						self.display.flip()
						self.display.clear_table()
						self.user_player.set_is_user()
						for player in self.table.get_players():
							self.display.add_text(player.get_name(),player.get_seat())
						self.display.update_announcement('Welcome to EuchreAI! Goodluck!')
						self.display.update_score([0,0])
						self.display.update_team(self.user_player.get_team())


						self.play_game()

