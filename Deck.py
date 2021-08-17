import random
from Card import Card
import datetime

class Deck:

    def __init__(self):
        self.cards = []
        
        #Card worth is based on number of cards that can beat it when lead
        #Hearts
        self.cards.append(Card('H','9','1','config/card_imgs/9H.png'))
        self.cards.append(Card('H','10','2','config/card_imgs/10H.png'))
        self.cards.append(Card('H','J','3','config/card_imgs/JH.png'))
        self.cards.append(Card('H','Q','4','config/card_imgs/QH.png'))
        self.cards.append(Card('H','K','5','config/card_imgs/KH.png'))
        self.cards.append(Card('H','A','6','config/card_imgs/AH.png'))
        
        #Diamonds
        self.cards.append(Card('D','9','1','config/card_imgs/9D.png'))
        self.cards.append(Card('D','10','2','config/card_imgs/10D.png'))
        self.cards.append(Card('D','J','3','config/card_imgs/JD.png'))
        self.cards.append(Card('D','Q','4','config/card_imgs/QD.png'))
        self.cards.append(Card('D','K','5','config/card_imgs/KD.png'))
        self.cards.append(Card('D','A','6','config/card_imgs/AD.png'))
        
        #Spades
        self.cards.append(Card('S','9','1','config/card_imgs/9S.png'))
        self.cards.append(Card('S','10','2','config/card_imgs/10S.png'))
        self.cards.append(Card('S','J','3','config/card_imgs/JS.png'))
        self.cards.append(Card('S','Q','4','config/card_imgs/QS.png'))
        self.cards.append(Card('S','K','5','config/card_imgs/KS.png'))
        self.cards.append(Card('S','A','6','config/card_imgs/AS.png'))
        
        #Clubs
        self.cards.append(Card('C','9','1','config/card_imgs/9C.png'))
        self.cards.append(Card('C','10','2','config/card_imgs/10C.png'))
        self.cards.append(Card('C','J','3','config/card_imgs/JC.png'))
        self.cards.append(Card('C','Q','4','config/card_imgs/QC.png'))
        self.cards.append(Card('C','K','5','config/card_imgs/KC.png'))
        self.cards.append(Card('C','A','6','config/card_imgs/AC.png'))
        
        random.shuffle(self.cards)
    
    def get_cards(self):
        random.seed(datetime.datetime.now().strftime('%S'))
        return self.cards
    
    def draw_card(self):
        random.seed(datetime.datetime.now().strftime('%S'))
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card
