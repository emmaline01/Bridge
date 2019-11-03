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
        self.hand = game.deck[13 * (self.playerNum-1), 13 * self.playerNum]
        self.partner = game.allPlayers[(self.playerNum + 2) % 4]

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

#edited from http://blog.lukasperaza.com/getting-started-with-pygame/
class PygameGame(object):

    """
    a bunch of stuff is left out of this file, but you can check it out in the Github repo
    """

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

        pygame.init()

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

            screen.fill((70, 130, 50))
            self.biddingOptScreen.fill((50, 110, 30))
            self.biddingBarScreen.fill((0, 0, 0))
            self.handScreen.fill((255, 255, 255))
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
