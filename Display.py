import pygame

class Display:

	def __init__(self):

		#Initialize game and display
		pygame.init()
		pygame.display.init()

		#Create main surface (display) and set Window title
		self.display = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('EuchreAI')

	def update(self,rects):
		pygame.display.update(rects)

	def flip(self):
		pygame.display.flip()

	def blit(self,surf,dest):
		self.display.blit(surf,dest)

	def get_events(self):
		return pygame.event.get()

	def user_quit(self):
		for event in pygame.event.get():
			if event == pygame.QUIT:
				return True
			else:
				return False

	def get_events(self):
		return pygame.event.get()

	def quit(self):
		pygame.quit()

	def get_error(self):
		pygame.get_error()

	def pump(self):
		pygame.event.pump()