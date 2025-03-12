from Card import Card

class Move:
    def __init__(self, move_type, source, destination=None, card=None):
        if not isinstance(card, Card):
            raise TypeError("card must be an instance of Card")
        if move_type not in [
            "tableau_to_tableau", "tableau_to_foundation", "tableau_to_freecell",
            "freecell_to_foundation", "freecell_to_tableau", "foundation_to_tableau",
            "foundation_to_freecell"
        ]:
            raise ValueError(f"Invalid move type: {move_type}")
        
        self.move_type = move_type
        self.source = source
        self.destination = destination
        self.card = card

    def __repr__(self):
        return f"Move(type={self.move_type}, source={self.source}, destination={self.destination}, card={self.card})"

    def __eq__(self, other):
        if isinstance(other, Move):
            return (self.move_type == other.move_type and
                    self.source == other.source and
                    self.destination == other.destination and
                    self.card == other.card)
        return False

    def __hash__(self):
        return hash((self.move_type, self.source, self.destination, self.card))

