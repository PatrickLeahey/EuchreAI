import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSound
from Game import Game
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

	window = QWidget()

	window.setWindowTitle('EuchreAI: Can you beat the bots?')
	window.setWindowIcon(QIcon('config/card_imgs/readme_img.jpg'))
	window.resize(640,480)

	layout = QVBoxLayout()

	#Create signal
	button = QPushButton('Start game')

	layout.addWidget(button)

	#Connect buttons to window
	window.setLayout(layout)

	#Connect slot to signal
	button.clicked.connect(lambda: play(window))

	window.show()
	app.exec_()

create_app()



