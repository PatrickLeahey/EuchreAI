import pygame

class Display:

	def __init__(self):

		#Initialize game and display
		pygame.init()
		pygame.display.init()

		screen_info = pygame.display.Info() #Required to set a good resolution for the game screen
		self.width,self.height = 1280,720
		self.display = pygame.display.set_mode((self.width,self.height))
		self.announcement_rect = pygame.Rect(20,20,self.width//10,self.height//10)
		self.score_rect = pygame.Rect(self.width-150,20,self.width//10,self.height//10)
		self.table_rect = pygame.Rect(self.width//5*2,self.height//5*2,self.width//5,self.height//5)

		#Create main surface (display) and set Window title
		pygame.display.set_caption('EuchreAI')

	def update(self,rects):
		pygame.display.update(rects)

	def flip(self):
		pygame.display.flip()

	def blit(self,surf,dest):
		self.display.blit(surf,dest)

	def get_height(self):
		return self.height

	def get_width(self):
		return self.width

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

	def update_score(self,score):
		#Cover area and print score text
		self.pump()
		background = pygame.Surface((self.width//10,self.height//10))
		background.fill((0,128,0))
		self.display.blit(background,score_rect)

		self.pump()
		font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//60) 
		text = font.render(f'Team 0: {score[0]}   Team 1: {score[1]}', True, (255,255,255))    
		self.display.blit(text,self.score_rect) 
		self.update(self.score_rect)

	def update_announcement(self,text):
		#Cover area and print announcement text
		self.pump()
		background = pygame.Surface((self.width//10,self.height//10))
		background.fill((0,128,0))
		self.display.blit(background,announcement_rect)

		self.pump()
		font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//60) 
		announcement = font.render(f'{text}', True, (255,255,255))    
		self.display.blit(announcement,self.announcement_rect) 

		self.update(self.announcement_rect)

	def clear_table(self):
		image = pygame.image.load('config/card_imgs/wooden_tabletop.jpg').convert_alpha()
		image = pygame.transform.smoothscale(image, (self.width//5*1,self.height//5*1))
		self.display.blit(image,self.table_rect)
		self.update(self.table_rect)












