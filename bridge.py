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

class Hand(object):
    def __init__(self, deckObj):
        self.hand = []
        for i in range(13):
            newCard = deckObj.deck[random.randint(0, len(deckObj.deck) - 1 )]
            self.hand += [newCard]
            deckObj.deck.remove(newCard)

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
        self.playerHand = Hand(self.deck)

        self.biddingOptScreen = pygame.Surface((self.width, self.height/2))

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
            screen.blit(self.biddingOptScreen, (0, self.height/4))

            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

game = PygameGame()
game.run()