import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSound
from Game import Game
from Window import Window
import config.play_config as con
import random


def play(window):
	game = Game()
	game.set_window(window)
	game.create_user()
	names = []
	for player in game.get_players():
		named = False
		while named == False:
			name = random.choice(con.names)
			if name not in names:
				player.set_name(name)
				names.append(name)
				named = True

	game.play_game()

def create_app():
	#Start App
	app = QApplication(sys.argv)

	# Force the style to be the same on all OSs:
	app.setStyle('Fusion')

	#QSound.play('sound_file.wav')

	# Now use a palette to switch to dark colors:
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53, 53, 53))
	palette.setColor(QPalette.WindowText, QColor(5,5,5))
	...
	app.setPalette(palette)

	window = Window(QWidget())
	return app

#If run from the command line
if __name__ == "__main__":
	app = create_app()
	app.exec_()



