from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QWidget):
	def __init__(self,*args,**kwargs):
		QWidget.__init__(self,*args,**kwargs)

		self.setWindowTitle('EuchreAI: Can you beat the bots?')
		self.resize(640,480)
		layout = QGridLayout()

		#self.start_screen_img = QLabel(self)
		#self.pixmap = QPixmap('config/card_imgs/readme_img.jpg').scaledToWidth(480)
		#self.start_screen_img.setPixmap(self.pixmap)
		#self.start_screen_img.setAlignment(Qt.AlignCenter)

		#self.layout.addWidget(start_screen_img,0,0)

		start_screen_img = QLabel(self)
		pixmap = QPixmap('config/card_imgs/readme_img.jpg').scaledToWidth(480)
		start_screen_img.setPixmap(pixmap)
		layout.addWidget(start_screen_img,0,0)
		
		#Create button
		start_screen_button = QPushButton('Start game')

		#Add button to layout
		layout.addWidget(start_screen_button,1,0)

		#Connect slot to signal
		start_screen_button.clicked.connect(lambda: play(self))

		#Connect widgets to window
		self.setLayout(layout)
		self.show()
		


