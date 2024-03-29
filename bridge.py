import pygame
import random
import socket
from network import Network

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Card(object):
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f'{self.suit},{self.rank}'

    def __hash__(self):
        return hash((self.suit,self.rank))

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

class Deck(object):
    def __init__(self):
        suits = ['C', 'D', 'H', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 
            'Q', 'K', 'A']

        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck += [Card(suit, rank)]
                random.shuffle(self.deck)

class Player(object):
    bids = {(0,0):'Pass',(0,1):'Double',(0,2):'Redouble',(1,0): '1NT',(1,1): '1S',(1,2):'1H',(1,3):'1D',(1,4):'1C'}

    def __init__(self, game, seat): 
        # game is the app object
        # seat is supposed to be N,S,E,W in str
        self.seat = seat
        allSeats = {'N': ['North', 1], 'E':['East', 2], 'S':['South',3],'W':['West',4]}
        self.seatName = allSeats[seat][0]
        self.playerNum = allSeats[seat][1]

        self.hand = game.deck.deck[13 * (self.playerNum-1): 13 * self.playerNum]
        self.bids = []

    def __hash__(self):
        hashable = (self.seat)
        return hash(hashable)

    def __eq__(self, other):
        return isinstance(self,Player) and self.seat == other.seat
    
    def setPartner(self, game):
        self.partner = game.allPlayers[(self.playerNum + 2) % 4]

    def recordBid(self, game, bid):
        self.bids.append(bid)
        game.bidSequence.append(bid)
        print(Player.bids[bid])
        
class RealPlayer(Player):

    def __init__(self, game, seat):
        super().__init__(self,game,seat)
        # sorted hand is a dict with suit as key
        self.hand = self.sortHand()

    def sortHand(self):
        sortedHand = {'S':[],'H':[],'D':[],'C':[]}
        # sort according to suits
        for card in self.hand:
            sortedHand[card.suit].append(card)
        for suit in sortedHand:
            sortedHand[suit] = mySort(sortedHand[suit])    
    
    def mySort(L):
        numList = []
        caseList = []
        for i in range(len(L)):
            if L[i].isdigit():
                numList.append(L[i])
            elif L[i].isalpha():
                caseList.append(L[i])
        numList.sort()
        if "J" in caseList:
            numList.append("J")
        if "Q" in caseList:
            numList.append("Q")
        if "K" in caseList:
            numList.append("K")
        if "A" in caseList:
            numList.append("A")
        return numList

    def makeBid(self, game, bid): # bid is from user input
        super().recordBid(game,bid)
    

class AI(Player):
    def __init__(self,game,seat):
        super().__init__(game,seat)
        self.hcp = 0
        for card in self.hand:
            if card.rank == 'A': self.hcp += 4
            elif card.rank == 'K': self.hcp += 3
            elif card.rank == 'Q': self.hcp += 2
            elif card.rank == 'J': self.hcp += 1
        self.countHand()
        
    def countHand(self):
        self.distribution = {'S':0, 'H':0, 'D':0, 'C':0}
        for card in self.hand:
            self.distribution[card.suit] += 1
            return self.distribution

    def isBalancedHand(self):
        for suit in self.distribution:
            if self.distribution[suit] < 2 or self.distribution[suit] > 5:
                return False
        return True

    def makeBid(self, game): # turn should be some count % 4
        # mute opponent first
        if self.partner != game.player: 
            bid = (0, 0)

        # actually dumb bidding
        # (2,4) is the strong 2C opening
        if not self.partner.bids[0] == (2,4) and self.hcp < 6: # pass if you have nothing
            bid =  (0, 0)

        # opening bid
        elif len(game.bidSequence) < 1:
            bid = self.makeOpeningBid()
        
        elif partner.bids[0] == (1, 0):
            bid = self.respondTo1NT()
        else:
            bid = (0,0)
        super().recordBid(game,bid)


    def makeOpeningBid(self):
        if self.hcp > 21:
            bid = (2, 4) # 2C opening
        elif 12 <= self.hcp <= 21 or (self.hcp == 11 and not self.isBalancedHand()):
            if 15 <= self.hcp <= 17 and self.isBalancedHand():
                bid = (1, 0)
            elif 20 <= self.hcp <= 21 and self.isBalancedHand():
                bid = (2, 0)
            elif self.distribution['S'] >= 5:
                bid = (1, 1)
            elif self.distribution['H'] >= 5:
                bid = (1, 2)
            elif self.distribution['D'] >= 4:
                bid = (1, 3)
            else: bid = (1, 4)
        # pre - empts
        elif 6 <= self.hcp <= 10:
            bidOptions = ['S','H','D','C']
            for i in range(len(bidOptions)-1):
                if self.distribution[bidOptions[i]] >= 6:
                    bid = (2, i + 1)
                elif self.distribution[bidOptions[-1]] >= 7:
                    bid = (3, 4) # club has to start from 3C
        return bid

    def respondTo1NT(self): 
        pass


class Button(object):
    def __init__ (self, tableScreenHeight, position, image):
        self.image = image
        topLeft, bottomRight = position
        self.x0, self.y0 = topLeft
        self.x, self.y = bottomRight
        self.y0 += tableScreenHeight
        self.y += tableScreenHeight
        self._rect = pygame.Rect(position)
    
    def draw(self, screen):
        screen.blit(self.image, self._rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                eventX, eventY = event.pos
                if (eventX > self.x0 and eventX < self.x
                    and eventY < self.y and eventY > self.y0):
                        if self.y < 410:
                            return (((self.y0-200)//50 + 1, self.x0//80 ))
                        elif self.x0//100 == 2: 
                            return ((0,0)) # pass
                        elif self.x0//100 == 0: 
                            return ((0,1)) # double
                        elif self.x0//100 == 1:
                            return ((0,2)) # redouble

#edited from http://blog.lukasperaza.com/getting-started-with-pygame/
class PygameGame(object):

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=400, height=600, fps=50, title="Bridge"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title

        #self.net = Network()

        self.deck = Deck()
        self.player = RealPlayer(self, 'S')
        self.allPlayers = []
        for AISeat in ['N','E','W']:
            self.allPlayers.append(AI(self,AISeat))
        self.allPlayers.insert(2,self.player)
        for player in self.allPlayers:
            player.setPartner(self)
        self.bidSequence = []
        self.turn = 0



        #does this work
        print(f'sending,{self.parse_data(self.send_data())}')
        self.player2.bids.append(self.parse_data(self.send_data()))
        self.tableScreenHeight = 200
        self.biddingOptScreenHeight = 200
        self.biddingOptScreen = pygame.Surface((self.width, 
            self.biddingOptScreenHeight))
        self.biddingBarScreenHeight = 80
        self.biddingBarScreen = pygame.Surface((self.width, 80))
        self.handScreen = pygame.Surface(
            (self.width, self.height - self.tableScreenHeight - self.biddingBarScreenHeight - self.biddingOptScreenHeight))

        self.initButtons()

        pygame.init()


#    def send_data(self):
        """
        Send position to server
        :return: None
        """
    #    data = str(self.net.id) + ":" + str(self.bid) # shouldnt be the case
    #    reply = self.net.send(data)
    #    return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

    def initButtons(self):

        #biddingOptScreen buttons
        buttonNames = [0, 141, 282, 423, 564]
        self.buttons = []
        newRow = []
        for i in range(5):
            newPos = ((i*80 + 10, 0), ((i+1)*80, 50))
            newImg = pygame.image.load(f'imgs/button{buttonNames[i]}.jpeg')
            newButton = Button(self.tableScreenHeight, newPos, pygame.transform.scale(newImg, (60, 40)))
            newRow.append(newButton)   
        self.buttons.append(newRow)

        for row in range(2, 5):
            newRow = []
            for col in range(5):
                newPos = ((col*80 + 10, 50*(row-1)), ((col+1)*80 + 10, 50*row))
                newImg = pygame.image.load(f'imgs/row{row}button{buttonNames[col]}.jpeg')
                newButton = Button(self.tableScreenHeight, newPos, pygame.transform.scale(newImg, (60, 40)))
                newRow.append(newButton)  
            self.buttons.append(newRow)


        self.biddingBarButtons = []
        #biddingBarScreen buttons
        for bb in range(1, 5):
            newPos = (((bb-1)*100 + 10, 10), (bb*100 + 10, 50*row))
            newImg = pygame.image.load(f'imgs/bar{bb}.jpg')
            newButton = Button(self.tableScreenHeight + self.biddingOptScreenHeight, newPos, pygame.transform.scale(newImg, (80, 60)))
            self.biddingBarButtons.append(newButton)

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # call game-specific initialization
        #self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            
            # take turns bid
            '''
            while True:
                turn = self.turn % 4
                if turn != 2:
                    self.allPlayers[turn].makeBid(self)'''
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

                for row in range(len(self.buttons)):
                    for col in range(len(self.buttons[0])):
                        response = self.buttons[row][col].event_handler(event)
                        if response != None:
                            self.player.makeBid(self,response)

                for bb in range(len(self.biddingBarButtons)):
                    self.biddingBarButtons[bb].event_handler(event)

            #fill background colors of surfaces
            screen.fill((70, 130, 50))
            self.biddingOptScreen.fill((50, 110, 30))
            self.biddingBarScreen.fill((0, 0, 0))
            self.handScreen.fill((70, 130, 50))

            #draw buttons
            for row in range(len(self.buttons)):
                for col in range(len(self.buttons[0])):
                    self.buttons[row][col].draw(self.biddingOptScreen)
            for bb in range(len(self.biddingBarButtons)):
                self.biddingBarButtons[bb].draw(self.biddingBarScreen)
            
            #draw compass
            self.compass = pygame.transform.scale(pygame.image.load(f'imgs/compass.png').convert_alpha(), (120, 150))
            screen.blit(self.compass, (10, 10))

            #put all the other surfaces on the back screen
            screen.blit(self.biddingOptScreen, (0, self.tableScreenHeight))
            screen.blit(self.biddingBarScreen, 
                (0, self.tableScreenHeight + self.biddingOptScreenHeight))
            screen.blit(self.handScreen, 
                (0, self.tableScreenHeight + self.biddingOptScreenHeight + self.biddingBarScreenHeight))

            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

game = PygameGame()
game.run()
