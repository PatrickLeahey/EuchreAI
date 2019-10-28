from Game import Game
from Player import Player
import train_config
import random
import pandas as pd
import os
from datetime import datetime
import numpy as np

def mutate(players):

	best = players[0:train_config.num_kept]

	next_gen = []

	for player in best:

		for _ in range(train_config.num_babies):

			player = Player(0)

			l = player.get_lead_with_trump()
			a = player.get_lead_with_ace()
			o = player.get_call_trump_round_one()
			t = player.get_call_trump_round_two()
			p = player.get_count_on_partner()
			g = player.get_go_alone()

			pct_variation_max = train_config.pct_variation_max

			player.set_lead_with_trump(random.uniform(-pct_variation_max,pct_variation_max)+l)
			player.set_lead_with_ace(random.uniform(-pct_variation_max,pct_variation_max)+a)
			player.set_call_trump_round_one(random.uniform(-pct_variation_max,pct_variation_max)+o)
			player.set_call_trump_round_two(random.uniform(-pct_variation_max,pct_variation_max)+t)
			player.set_count_on_partner(random.uniform(-pct_variation_max,pct_variation_max)+p)
			player.set_go_alone(random.uniform(-pct_variation_max,pct_variation_max)+g)

			next_gen.append(player)

	return next_gen

players = []

for i in range(train_config.num_generations):

	for _ in range(train_config.num_games):

		if i == 0:

			game = Game()
			game.set_teams()
			game.play_game()

			for player in game.get_players():
				players.append(player)

		else:

			if len(players) >= 4:
				
				players_for_this_game = players[0:4]
				
				for player in players_for_this_game:
					players.remove(player)

			game = Game()
			game.provide_players(players_for_this_game)
			game.set_teams()
			game.play_game()

			for player in game.get_players():
				players.append(player)

	players = mutate(players)
	print(f'------ {(i/train_config.num_generations * 100)}% Complete ------')

player_info = []

for player in players:
			l = player.get_lead_with_trump()
			a = player.get_lead_with_ace()
			o = player.get_call_trump_round_one()
			t = player.get_call_trump_round_two()
			p = player.get_count_on_partner()
			g = player.get_go_alone()

			player_info.append([l,a,o,t,p,g])

df = pd.DataFrame(player_info, columns = ['Lead_Trump','Lead_Ace','Call_1','Call_2','Count_On_Partner','Go_Alone'])
print(df)
df.to_csv(f'output/train_{datetime.today().strftime("%Y-%m-%d")}.csv')


