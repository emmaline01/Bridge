import pygame
import random

class Card(object):
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

class Deck(object):
    def __init__(self):
        suits = ['C', 'D', 'H', 'S']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 
            'Q', 'K', 'A']

        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck += [Card(suit, rank)]

class Player(object):
    def __init__(self, game, seat): 
        # game is the app object
        # seat is supposed to be N,S,E,W in str
        self.seat = seat
        allSeats = {'N': ['North', 1], 'E':['East', 2], 'S':['South',3],'W':['West',4]}
        self.seatName = allSeats[seat][0]
        self.playerNum = allSeats[seat][1]
        self.hand = None #game.deck[13 * (self.playerNum-1), 13 * self.playerNum]
        self.partner = None #game.allPlayers[(self.playerNum + 2) % 4]

    def __hash__(self):
        hashable = (self.seat)
        return hash(hashable)

    def __eq__(self, other):
        return isinstance(self,player) and self.seat == other.seat
        
class RealPlayer(Player):
    def makeBid(self, game, bid): # bid is from user input
        game.bidSequence.append(bid)


class AI(Player):
    def __init__(self,game,seat):
        super().__init__(self,game,seat)
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


    def makeBid(self, game, turn): # turn should be some count % 4
        # mute opponent first
        if self.partner != game.player: return 'Pass'

        if self.hcp < 6:
            return 'Pass'
        elif len(game.bidSequence) < 1:
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
                    print("clicked!")

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

        self.deck = Deck()
        self.player = Player(self, 'S')
        self.allPlayers = []
        for AISeat in ['N','E','W']:
            self.allPlayers.append(Player(self,AISeat))
        self.allPlayers.insert(2,self.player)
        self.bidSequence = []

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

    def initButtons(self):

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False

                for row in range(len(self.buttons)):
                    for col in range(len(self.buttons[0])):
                        self.buttons[row][col].event_handler(event)

            screen.fill((70, 130, 50))
            self.biddingOptScreen.fill((50, 110, 30))
            self.biddingBarScreen.fill((0, 0, 0))
            self.handScreen.fill((255, 255, 255))

            for row in range(len(self.buttons)):
                for col in range(len(self.buttons[0])):
                    self.buttons[row][col].draw(self.biddingOptScreen)
            
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
