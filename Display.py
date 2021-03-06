import pygame

class Display:
    
    def __init__(self):

        #Initialize game and display
        pygame.init()
        pygame.display.init()

        screen_info = pygame.display.Info() #Required to set a good resolution for the game screen
        self.width,self.height = 1280,720
        self.display = pygame.display.set_mode((self.width,self.height))
        self.announcement_rect = pygame.Rect(20,20,self.width//2,self.height//10)
        self.score_rect = pygame.Rect(self.width-150,20,self.width//10,self.height//10)
        self.table_rect = pygame.Rect(self.width//4,self.height//6,self.width//2,self.height//2)
        self.button_rect = (self.width//20,self.height//10*2)
        self.suit_rects = [(self.width//20,self.height//10*3),(self.width//20,self.height//10*4), \
                            (self.width//20,self.height//10*5),(self.width//20,self.height//10*6)]
        self.trick_score_center = (self.width//2,self.height//20)
        self.rects = 'To_be_set'
        self.button_rect_actual = 'To_bet_set'
        
        #Create main surface (display) and set Window title
        pygame.display.set_caption('EuchreAI')
    
    def update(self,rects):
        self.pump()
        pygame.display.update(rects)
    
    def flip(self):
        self.pump()
        pygame.display.flip()
    
    def blit(self,surf,dest):
        self.display.blit(surf,dest)
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def get_events(self):
        return pygame.event.get()
    
    def prompt_event(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {}))
    
    def user_quit(self):
        self.prompt_event()
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
    
    def wait(self,time):
        pygame.time.wait(time)
    
    def update_score(self,score):
        #Cover area and print score text
        self.pump()
        background = pygame.Surface((self.width//3,self.height//10))
        background.fill((0,128,0))
        self.display.blit(background,self.score_rect)
        
        self.pump()
        font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//60) 
        text = font.render(f'Team 0: {score[0]}   Team 1: {score[1]}', True, (255,255,255))    
        self.display.blit(text,self.score_rect) 
        
        self.update(self.score_rect)
    
    def update_team(self,team):
        self.pump()
        font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//60) 
        text = font.render(f'You are on team: {team}', True, (255,255,255))    
        text_rect = text.get_rect(center = (self.width//2,self.height//60))
        self.display.blit(text,text_rect) 
        self.update(text_rect)
    
    def update_announcement(self,text):
        #Cover area and print announcement text
        self.pump()
        background = pygame.Surface((self.width//3,self.height//10))
        background.fill((0,128,0))
        self.display.blit(background,self.announcement_rect)
        
        self.pump()
        font = pygame.font.Font(pygame.font.get_default_font(), self.display.get_height()//60) 
        announcement = font.render(f'{text}', True, (255,255,255))    
        self.display.blit(announcement,self.announcement_rect) 
        
        self.update(self.announcement_rect)
    
    def clear_table(self):
        image = pygame.image.load('config/card_imgs/wooden_tabletop.jpg').convert_alpha()
        image.set_alpha(255)
        image = pygame.transform.smoothscale(image, (self.width//2,self.height//2))
        self.display.blit(image,self.table_rect)
        self.update(self.table_rect)
    
    def display_credit_and_title(self):
        image = pygame.image.load('config/card_imgs/logo.png').convert_alpha()
        image = pygame.transform.smoothscale(image, (self.width//10,self.width//10))
        image_rect = image.get_rect(bottomright = (self.width-10,self.height-10))
        self.blit(image,image_rect)
        self.pump()
        font = pygame.font.Font(pygame.font.get_default_font(), self.get_height()//60) 
        word = font.render('Developed by Patrick Leahey', True, (255,255,255)) 
        word_rect = word.get_rect(center = (self.get_width()//13,self.get_height()//60*59))
        self.blit(word, word_rect)
        self.update([image_rect,word_rect])

    def add_card_to_table(self,img,num,backs):
            
        self.pump()

        left_start = self.table_rect.centerx - (2 * self.width//50)

        self.pump()

        if backs:
            for i in range(num-1):
                self.pump()
                image = pygame.image.load('config/card_imgs/back.png').convert_alpha()
                image = pygame.transform.smoothscale(image, (self.width//9,self.height//3))
                image_rect = image.get_rect()
                image_rect.centery = self.table_rect.centery
                self.pump()
                image_rect.centerx = left_start + i * self.width//50
                self.display.blit(image,image_rect)
                self.pump()

                self.update(image_rect)

        self.pump()

        image = pygame.image.load(img).convert_alpha()
        image = pygame.transform.smoothscale(image, (self.width//9,self.height//3))

        self.pump()

        image_rect = image.get_rect()
        image_rect.centery = self.table_rect.centery
        image_rect.centerx = left_start + num * self.width//50
        self.display.blit(image,image_rect)

        self.pump()            

        self.update(image_rect)

    def add_text(self,text,rect):

        self.pump()
        background = pygame.Surface((self.width//50,self.height//50))
        background.fill((0,128,0))
        background_rect = background.get_rect(center = rect)
        self.display.blit(background,background_rect)

        self.pump()

        font = pygame.font.Font(pygame.font.get_default_font(), self.get_height()//50) 
        words = font.render(f'{text}', True, (255,255,255))    
        words_rect = words.get_rect(center = rect)
        self.display.blit(words,words_rect) 

        self.pump()

        self.update(words_rect)

    def display_hand(self,hand):
        self.pump()
        game_on = True
        while game_on == True:
            self.pump()
            self.prompt_event()
            for event in self.get_events():
                if event.type == pygame.QUIT:
                    self.display.quit()
                else:
                    self.pump()

                    background = pygame.Surface((self.get_width()//4*3, self.get_height()//6))
                    background.fill((0,128,0))
                    background_rect = background.get_rect()
                    background_rect.center = (self.get_width()//2,self.get_height()//8*7)
                    self.blit(background,background_rect)
                    self.update(background_rect)
                    self.pump()

                    rects = []

                    self.pump()
                    for i,card in zip(range(len(hand)),hand):
                        img_path = card.get_img_path()
                        image = pygame.image.load(img_path)
                        image = pygame.transform.smoothscale(image, (self.get_width()//10,self.get_height()//6)).convert_alpha()
                        image_rect = image.get_rect()
                        space = self.get_width()//50
                        start_left = self.get_width()//2 - (2 * space) - (2 * self.get_width()//8)
                        image_rect.center = ((start_left + i * (space + self.get_width()//8)), (self.get_height()//8 * 7))

                        self.pump()
                        
                        rects.append(image_rect)
                        self.blit(image,image_rect)
                        self.update(image_rect)
                        self.wait(100)

                    self.pump()

                    return rects


    def set_current(self,player):
        player_seat = player.get_seat()

        pygame_circ = pygame.draw.circle(self.display,(6, 30, 250),(player_seat[0],player_seat[1] + self.height//35),self.width//120)

    def unset_current(self,player):
        player_seat = player.get_seat()

        background = pygame.Surface((self.get_width()//30,self.get_height()//30))
        background.fill((0,128,0))
        background_rect = background.get_rect()
        background_rect.center = (player_seat[0],player_seat[1] + self.height//35)
        self.blit(background,background_rect)

        self.update(background_rect)

    def set_dealer(self,dealer):
        dealer_seat = dealer.get_seat()

        self.pump()

        font = pygame.font.Font(pygame.font.get_default_font(), self.get_height()//45) 
        words = font.render('DEALER', True, (252,186,3))    
        words_rect = words.get_rect(center = (dealer_seat[0],dealer_seat[1] - self.height//35))
        self.display.blit(words,words_rect) 

        self.pump()

        self.update(words_rect)
        
        self.pump()

    def unset_dealer(self,dealer):
        dealer_seat = dealer.get_seat()

        background = pygame.Surface((self.get_width()//15,self.get_height()//45))
        background.fill((0,128,0))
        background_rect = background.get_rect()
        background_rect.center = (dealer_seat[0],dealer_seat[1] - self.height//35)
        self.blit(background,background_rect)

        self.update(background_rect)

    def update_trick_score(self,score):

        line = pygame.Surface((2,self.get_height()//30))
        line.fill((0,0,0))
        line_rect = line.get_rect(center = self.trick_score_center)
        self.blit(line,line_rect)
        self.update(line_rect)

        rects = []

        for i in range(score[0]):
            pygame_circ = pygame.draw.circle(self.display,(224, 22, 22),(self.trick_score_center[0] - (i+1)  * 45,self.trick_score_center[1]),self.width//120)
            rects.append(pygame_circ)

        for i in range(score[1]):
            pygame_circ = pygame.draw.circle(self.display,(224, 22, 22),(self.trick_score_center[0] + (i+1) * 45,self.trick_score_center[1]),self.width//120)
            rects.append(pygame_circ)

        self.update(rects)

    def cover_suits(self):

        self.pump()
        background = pygame.Surface((self.width//20,self.height//3*2))
        background.fill((0,128,0))
        background_rect = background.get_rect(center = self.suit_rects[2])
        self.display.blit(background,background_rect)
        self.update(background_rect)
        self.pump()

    def update_suit(self,suit):
        
        self.pump()

        if suit == 'H':
            img_path = 'config/card_imgs/heart.png'
        elif suit == 'D':
            img_path = 'config/card_imgs/diamond.png'
        elif suit == 'C':
            img_path = 'config/card_imgs/club.png'
        else:
            img_path = 'config/card_imgs/spade.png'

        self.cover_suits()

        self.pump()
        image = pygame.image.load(img_path).convert_alpha()
        image = pygame.transform.smoothscale(image, (self.get_width()//20,self.get_height()//15))
        image_rect = image.get_rect()
        image_rect.center = self.button_rect

        self.pump()
        
        self.blit(image,image_rect)

        self.update(image_rect)

    def display_suits(self,suits):

        self.cover_suits()

        suit_paths = []

        self.update_announcement('Click on a suit to call it trump')

        self.pump()

        for suit in suits:
            if suit == 'H':
                suit_paths.append('config/card_imgs/heart.png')
            elif suit == 'D':
                suit_paths.append('config/card_imgs/diamond.png')
            elif suit == 'C':
                suit_paths.append('config/card_imgs/club.png')
            else:
                suit_paths.append('config/card_imgs/spade.png')

        rects = []

        for i,img_path in zip(range(len(suit_paths)),suit_paths):
            self.pump()
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.smoothscale(image, (self.get_width()//20,self.get_height()//15))
            image_rect = image.get_rect()
            image_rect.center = self.suit_rects[i]

            self.pump()
            
            rects.append(image_rect)
            self.blit(image,image_rect)

        self.update(rects)
        self.pump()

        #Button
        button = pygame.Surface((self.get_width()//20,self.get_height()//15))
        button.fill((255,255,255))
        button_rect_actual = button.get_rect()
        button_rect_actual.center = self.button_rect
        self.blit(button,button_rect_actual)

        self.pump()

        #Button text
        font = pygame.font.Font(pygame.font.get_default_font(), self.get_height()//50) 
        button_text = font.render('PASS', True, (0,0,0)) 
        button_text_rect = button_text.get_rect()  
        button_text_rect.center = self.button_rect
        self.blit(button_text,button_text_rect) 

        self.pump()

        self.update(button_rect_actual)

        self.rects = rects
        self.button_rect_actual = button_rect_actual

    def select_suit(self,suits):

        user_clicked = False
        while user_clicked == False:
            for event in self.get_events():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if True in [suit_rect.collidepoint(pos) for suit_rect in self.rects]:
                        suit_index = [suit_rect.collidepoint(pos) for suit_rect in self.rects].index(True)
                        selected_suit = suits[suit_index]

                        #self.cover_suits()

                        self.pump()

                        self.update_suit(selected_suit)

                        self.pump()

                        if selected_suit == 'H':
                            s = 'Hearts'
                        elif selected_suit == 'D':
                            s = 'Diamonds'
                        elif selected_suit == 'C':
                            s = 'Clubs'
                        else:
                            s = 'Spades'

                        self.update_announcement(f'You selected {s} as trump')
                        return selected_suit

                    if self.button_rect_actual.collidepoint(pos):
                        self.update_announcement('You passed')
                        return ''
    
    def select_card(self,user,played_so_far):
        
        self.update_announcement('Click a card to play it')

        user_clicked = False
        while user_clicked == False:
            for event in self.get_events():

                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    pos = pygame.mouse.get_pos()
        
                    if True in [card_rect.collidepoint(pos) for card_rect in user.get_hand().get_rects()]:

                        card_index = [card_rect.collidepoint(pos) for card_rect in user.get_hand().get_rects()].index(True)
                        selected_card = [card for card in user.get_hand().get_cards()][card_index]
                        
                        #If the user is following 
                        if len(played_so_far) != 0:
                            
                            #If user has card of led suit and didn't play it
                            if True in [card.get_suit()==played_so_far[0].get_suit() for card in user.get_hand().get_cards()] \
                                                        and selected_card.get_suit() != played_so_far[0].get_suit():
                                self.update_announcement('You must follow suit!')

                            else:
                                user.get_hand().remove_card(selected_card)
                                user.get_hand().remove_rect(card_index)
                                return selected_card
                        
                        ## If the user is leading
                        else:
                            user.get_hand().remove_card(selected_card)
                            user.get_hand().remove_rect(card_index)
                            return selected_card
