class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.colour = self.get_colour()

    def get_colour(self):
        if self.suit in ['Hearts', 'Diamonds']:
            return 'Red'
        elif self.suit in ['Clubs', 'Spades']:
            return 'Black'
        else:
            return 'Unknown'

    def __repr__(self):
        return f"{self.rank} of {self.suit} ({self.colour})"