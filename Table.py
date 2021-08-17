from Player import Player

class Table:
    #Implements a circular list data structure to serve as table
    #You can visualize a four sided table with a player on each side
    #This will allow for smooth gameplay rotations for betting and playing tricks where winner leads next trick
    def __init__(self,):
        self.players = [Player(team) for team in range(4)]
        self.material = 'wood'
    
    ## Return players
    def get_players(self):
        return self.players
    
    ## Set players
    def set_players(self,players):
        self.players = players
    
    ## Get the player to the left of the given player
    def get_player_to_left(self, player):
        
        player_index = self.players.index(player)
        if player_index == len(self.players)-1:
            left_player_index = 0
        else:
            left_player_index = player_index+1
        
        left_player = self.players[left_player_index]
        
        return left_player

    ## Get the player to the left of the given player
    def get_player_to_left(self, player):
        
        player_index = self.players.index(player)
        if player_index == 0:
            right_player_index = len(self.players)-1
        else:
            right_player_index = player_index-1
        
        right_player = self.players[right_player_index]
        
        return right_player

    
    #Rotates players once around the table, to the left.. (clockwise)
    def rotate_once(self):
        first = self.players.pop(0)
        self.players.append(first)
    
    #This will rotate the table the correct number of times so that the player passed is the first in the list
    def set_first(self,player):
        num_rotations = self.players.index(player)
        for _ in range(num_rotations):
            self.rotate_once()