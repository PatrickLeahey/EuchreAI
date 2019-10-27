from Game import Game

game1 = Game()
game1.play_game()
for i,player in zip(range(len(game1.get_players())),game1.get_players()):
	print(f'Player {i} has score: {player.get_player_score()}')










