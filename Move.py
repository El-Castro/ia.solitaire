from Card import Card

class Move:
    def __init__(self, move_type, source, destination=None):
        """Initialize a Move object."""
        if move_type not in [
            "tableau_to_tableau", "tableau_to_foundation", "tableau_to_freecell",
            "freecell_to_foundation", "freecell_to_tableau", "foundation_to_tableau",
            "foundation_to_freecell"
        ]:
            raise ValueError(f"Invalid move type: {move_type}")
        
        self.move_type = move_type
        self.source = source
        self.destination = destination

    def __repr__(self):
        """Return a string representation of the Move object."""
        return f"Move(type={self.move_type}, source={self.source}, destination={self.destination})"

    def __eq__(self, other):
        """Check if two Move objects are equal."""
        if isinstance(other, Move):
            return (self.move_type == other.move_type and
                    self.source == other.source and
                    self.destination == other.destination)
        return False

    def __hash__(self):
        """Return the hash value of the Move object."""
        return hash((self.move_type, self.source, self.destination))

