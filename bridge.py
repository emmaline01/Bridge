import pygame
import random
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
        self.hand = game.deck.deck[13 * (self.playerNum-1): 13 * self.playerNum]
        self.bids = []

    def __hash__(self):
        hashable = (self.seat)
        return hash(hashable)

    def __eq__(self, other):
        return isinstance(self,player) and self.seat == other.seat
    
    def setPartner(self, game):
        self.partner = game.allPlayers[(self.playerNum + 2) % 4]
        
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

    def isBalancedHand(self):
        for suit in self.distribution:
            if self.distribution[suit] < 2 or self.distribution[suit] > 5:
                return False
        return True

    def recordBid(self,game, bid):
        self.bids.append(bid)
        game.bidSequence.append(bid)

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
        
        self.recordBid(game,bid)

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
        for player in self.allPlayers:
            player.setPartner(self)
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
