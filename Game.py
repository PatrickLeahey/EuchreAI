import random
from Deck import Deck
from Table import Table
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class Game:
    #Instantiate Game Instance
    def __init__(self):
        self.game_id = random.randint(1000000,9000000)
        self.deck = Deck()
        self.table = Table()
        self.user = False
        self.user_player = 'NA'
        self.window = 'NA'

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
        for player in self.table.get_players():
            for _ in range(5):
                player.get_hand().add_card(self.deck.draw_card())

        if self.user:
            #Cards you were dealt
            for card in self.user_player.get_hand().get_cards():
                label = QLabel(self.window)
                pixmap = QPixmap(card.get_img_path())
                label.setPixmap(pixmap)

    def set_window(self,window):
        self.window = window

    def get_window(self):
        return self.window

    def create_user(self):
        self.user = True
        self.user_player = self.table.get_players()[0]
        self.user_player.set_is_user()

        print('\n')

        print('                            |----|  |    |  |----|  |    |  |----   |----|')
        print('                            |       |    |  |       |    |  |    |  |     ')
        print('                            |--|    |    |  |       |----|  |----   |--|  ')
        print('                            |       |    |  |       |    |  |  |    |     ')
        print('                            |----|  |----|  |----|  |    |  |   |   |----|')

        print('\n')

        print('                                          By: Patrick Leahey')

        print('\n')

        print(f'Welcome to game {self.game_id}')
        print(f'You are on team: {self.user_player.get_team()}')
        print('\n')

    #Get raw details about the current table state
    def get_table_raw(self):
        #Return list of cards for each player in game at current state
        return [[card.get_desc() for card in player.get_hand().get_cards()] for player in self.table.get_players()]

    #Get human readable details about the tables state
    def get_table_readable(self):
        print(f'Game {self.game_id} Player hands:')
        for player_hand in self.get_table_raw():
            print(player_hand)
        print('\n')
        print('Kitty:')
        print([card.get_desc() for card in self.deck.get_cards()])
        print('\n')

    #Following each round, the dealer rotates up
    def next_dealer(self):
        #There will not be a set dealer in the first round
        #After this point, there should only be one dealer
        #Dealer rotates up

        dealer_index = 0

        if True in [player.is_dealer() for player in self.table.get_players()]:
            dealer_index = [player.is_dealer() for player in self.table.get_players()].index(True)

            print(f'Dealer index before switching: {dealer_index}')

            self.table.get_players()[dealer_index].toggle_dealer()
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
                print('You are now dealer!')
            else:
                dealer_id = self.table.get_players()[[player.is_dealer() for player in self.table.get_players()].index(True)].get_player_id()
                print(f'Player {dealer_id} is now dealer!')

        return dealer_index
        
    #A trick involves 4 cards
    def play_trick(self):
        
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

                if self.user:
                    if player.get_is_user():
                        if not played_so_far:
                            Print('It is your turn to lead')
                        print(f'You played {played_so_far[-1].get_desc()}')

                    else:
                        print(f'Player {player.get_player_id()} played {played_so_far[-1].get_desc()}')





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

        if self.user:
            print(f'Team {winning_team} won the trick!')

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
        #Initial deal of cards
        dealer_index = self.next_dealer()
        self.deal()

        #Remainder of cards in self.deck (4) are the kitty -- select the card on top
        flipped_card = self.deck.get_cards()[3]

        if self.user:
            print(f'Dealer flipped {flipped_card.get_desc()}')

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

                if self.user:
                    print(f'Player {player.get_player_id()} chose {trump_suit} as trump suit for {player.get_team()}')
                    print(f'Dealer (Player {self.table.get_players()[dealer_index].get_player_id()}) picked up {flipped_card.get_desc()} and discarded')

                break

            else:
                if self.user:
                    print(f'Player {player.get_player_id()} passed')

        #Second round betting
        if picked_up == False:
            for player in self.table.get_players():
                bet = player.bet(flipped_card,dealer_team,1)
                if bet != '':
                    picked_up = True
                    trump_suit = bet

                    if self.user:
                        print(f'Player {player.get_player_id()} chose {trump_suit} as trump suit for {player.get_team()}')

                    break
                else:
                    if self.user:
                        print(f'Player {player.get_player_id()} passed')

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
            team_called_trump = 'NA'
            went_alone = 'NA'
            for player in self.table.get_players():
                if player.get_called_trump():
                    team_called_trump = player.get_team()
                    if player.get_went_alone():
                        went_alone = player.get_team()

            print('---------')

            if score[0] > score[1]:
                if self.user:
                    print('Team 0 won this round')
                    print('---------')
                    print('\n')
                if score[0] == 5:
                    if self.user:
                        print('Team 0 won all 5')
                        print('---------')
                        print('\n')
                    return [2,0]
                elif team_called_trump == 1:
                    if self.user:
                        print('Team 0 euchred Team 1')
                        print('---------')
                        print('\n')
                    return [2,0]
                elif went_alone == 0 and score[0] == 5:
                    if self.user:
                        print('Team 0 went alone and won all 5')
                        print('---------')
                        print('\n')
                    return [4,0]
                else: 
                    if self.user:
                        print('---------')
                        print('\n')
                    return [1,0]

            else:
                if self.user:
                    print('Team 1 won this round')
                    print('---------')
                    print('\n')
                if score[1] == 5:
                    if self.user:
                        print('Team 1 won all 5')
                        print('---------')
                        print('\n')
                    return [0,2]
                elif team_called_trump == 0:
                    if self.user:
                        print('Team 1 euchred Team 0')
                        print('---------')
                        print('\n')
                    return [0,2]
                elif went_alone == 1 and score[1] == 5:
                    if self.user:
                        print('Team 1 went alone and won all 5')
                        print('---------')
                        print('\n')
                    return [0,4]
                else: 
                    if self.user:
                        print('---------')
                        print('\n')
                    return [0,1]
            
        #The suit was not set during betting
        else:
            if self.user:
                print('Neither team wanted to bet')
                print('\n')
            return [0,0]

    #A game is over when one team reaches 10 points
    def play_game(self):

        score = [0,0]
        num_round = 1
        while score[0] < 10 and score[1] < 10:
            round_score = self.play_round()

            score = [score[0] + round_score[0], score[1] + round_score[1]]

            if self.user:
                print('----------------------------------------')
                print(f'-------------Round Number: {num_round} -----------')
                print(f'----------------Team 0: {score[0]} --------------')
                print(f'----------------Team 1: {score[1]} --------------')
                print('----------------------------------------')
                print('\n')

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

        if self.user:

            winner_number = 0 if score[0] > score[1] else 1
            print('----------------------------------------')
            print('-------------GAME-----OVER--------------')
            print(f'--------------TEAM {winner_number} WINS --------------')
            print('----------------------------------------')
            print('\n')
