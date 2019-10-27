import random
from Player import Player
from Deck import Deck

class Game:

    def __init__(self):
        self.game_id = random.randint(1000000,9000000)
        self.players = [Player(team) for team in range(4)]
        self.deck = Deck()

    def provide_players(self,players):
        self.players = players
        
    def deal(self):
        for player in self.players:
            for _ in range(5):
                player.get_hand().add_card(self.deck.draw_card())

    def get_table_raw(self):
        #Return list of cards for each player in game at current state
        return [[card.get_desc() for card in player.get_hand().get_cards()] for player in self.players]

    def get_table_readable(self):
        
        print(f'Game {self.game_id} Player Hands:')
        for player_hand in self.get_table_raw():
            print(player_hand)
        print('\n')
        print('Kitty:')
        print([card.get_desc() for card in self.deck.get_cards()])
        
        print('\n')

    def next_dealer(self):
        #There will not be a dealer in the first round
        #After this point, there should only be one dealer
        #Dealer rotates up

        dealer_index = 0

        if True in [player.is_dealer() for player in self.players]:
            dealer_index = [player.is_dealer() for player in self.players].index(True)
            self.players[dealer_index].toggle_dealer()
            if dealer_index != 3:
                self.players[dealer_index + 1].toggle_dealer()
            else:
                self.players[0].toggle_dealer()
        else:
            self.players[0].toggle_dealer()

        return dealer_index
        
    #A trick involves 4 cards
    def play_trick(self):
        return [0,1]

    #A round involves 20 cards and is equal to 5 tricks
    def play_round(self):
        #Initial deal of cards
        dealer_index = self.next_dealer()
        self.deal()

        #Remainder of cards in self.deck (4) are the kitty -- select the card on top
        flipped_card = self.deck.get_cards()[3]

        trump_suit = ''

        print('Players are betting:')
        picked_up = False
        for player in self.players:
            bet = player.bet(flipped_card,0)
            if bet != '':
                #Dealer drops one of their cards
                #Dealer picks up flipped card
                dealer_index = [player.is_dealer() for player in self.players].index(True)
                remove_card = random.choice(self.players[dealer_index].get_hand().get_cards())
                self.players[dealer_index].get_hand().remove_card(remove_card)
                self.players[dealer_index].get_hand().add_card(flipped_card)
                picked_up = True
                trump_suit = flipped_card.get_desc()[0]
                break

        if picked_up == False:
            for player in self.players:
                bet = player.bet(flipped_card,1)
                if bet != '':
                    picked_up = True
                    trump_suit = bet
                    break

        print(f'Player chose {trump_suit} as trump_suit')
        print('\n')

        if trump_suit != '':

            for player in self.players:
                player.get_hand().set_trump(trump_suit)

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
            for player in self.players:
                if player.get_called_trump():
                    team_called_trump = player.get_team()
                    if player.get_went_alone():
                        went_alone = player.get_team()

            if score[0] > score[1]:
                print('Team 0 won this round')
                if score[0] == 5:
                    print('Team 0 won all 5')
                    return [2,0]
                elif team_called_trump == 1:
                    print('Team 0 euchred Team 1')
                    return [2,0]
                elif went_alone == 0 and score[0] == 5:
                    print('Team 0 went alone and won all 5')
                    return [4,0]
                else: 
                    return [1,0]

            else:
                print('Team 1 won this round')
                if score[1] == 5:
                    print('Team 1 won all 5')
                    return [0,2]
                elif team_called_trump == 0:
                    print('Team 1 euchred Team 0')
                    return [0,2]
                elif went_alone == 1 and score[1] == 5:
                    print('Team 1 went alone and won all 5')
                    return [0,4]
                else: 
                    return [0,1]

        #The suit was not set during betting
        else:
            print('Neither team wanted to bet')
            print('\n')
            return [0,0]

    #A game is over when one team reaches 10 points
    def play_game(self):

        print(f'Game started with id: {self.game_id}')
        print('\n')

        score = [0,0]
        num_round = 0
        while score[0] < 10 and score[1] < 10:
            num_round = num_round + 1
            round_score = self.play_round()

            score = [score[0] + round_score[0], score[1] + round_score[1]]

            print('----------------------------------------')
            print(f'-------------Round Number: {num_round} -----------')
            print(f'-------------------Team 0: {score[0]} -----------')
            print(f'-------------------Team 1: {score[1]} -----------')
            print('----------------------------------------')
            print('\n')

            self.get_table_readable()

            self.deck = Deck()
            for player in self.players:
                player.reset_hand()

                if player.get_called_trump():
                    player.toggle_called_trump()

                    if player.get_went_alone():
                        player.toggle_went_alone()

        winner_number = 0 if score[0] > score[1] else 1
        print('----------------------------------------')
        print('-------------GAME-----OVER--------------')
        print(f'--------------TEAM {winner_number} WINS --------------')
        print('----------------------------------------')


            

            


        



        






        
        





   






