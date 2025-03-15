class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.colour = self.get_colour()

    def get_colour(self):
        if self.suit in ['hearts', 'diamonds']:
            return 'red'
        elif self.suit in ['clubs', 'spades']:
            return 'black'
        else:
            return 'unknown'

    def __repr__(self):
        return f"{self.rank} of {self.suit} ({self.colour})"
    
    def to_dict(self):
        return {
            'rank': self.rank,
            'suit': self.suit,
            'colour': self.colour
        }

    @staticmethod
    def from_dict(card_dict):
        return Card(card_dict['rank'], card_dict['suit'])
    