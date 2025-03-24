class Card:
    def __init__(self, rank, suit):
        """Initialize a Card object with a rank, suit, and colour."""
        self.rank = rank
        self.suit = suit
        self.colour = self.get_colour()

    def get_colour(self):
        """Determine the colour of the card based on its suit."""
        if self.suit in ['hearts', 'diamonds']:
            return 'red'
        elif self.suit in ['clubs', 'spades']:
            return 'black'
        else:
            return 'unknown'

    def __repr__(self):
        """Return a string representation of the card."""
        return f"{self.rank} of {self.suit} ({self.colour})"
    
    def to_dict(self):
        """Convert the card object to a dictionary."""
        return {
            'rank': self.rank,
            'suit': self.suit,
            'colour': self.colour
        }

    @staticmethod
    def from_dict(card_dict):
        """Create a Card object from a dictionary."""
        return Card(card_dict['rank'], card_dict['suit'])
    