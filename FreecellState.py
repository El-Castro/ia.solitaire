import FreecellMove
import Card
import tkinter as tk
from tkinter import Canvas
import random
import copy
import heapq

class FreeCellState:
    def __init__(self, tableau, free_cells=None, foundations=None):
        self.tableau = tableau  # 8 tableau columns
        self.free_cells = free_cells if free_cells else [None] * 4  # 4 free cells
        self.foundations = foundations if foundations else {suit: [] for suit in ['hearts', 'diamonds', 'clubs', 'spades']}
        self.history = []


    def copy(self):
        return FreeCellState([col[:] for col in self.tableau], self.free_cells[:], self.foundations.copy())
    
    def is_solved(self):
        # Check if all foundations are complete
        return all(len(self.foundations[suit]) == 13 for suit in self.foundations)

    @staticmethod
    def create_random_state():
        # Create a deck of cards
        deck = [Card(suit, rank) for suit in ['hearts', 'diamonds', 'clubs', 'spades'] for rank in range(1, 14)]
        random.shuffle(deck)
        
        # Distribute cards to tableau columns
        tableau = [[] for _ in range(8)]
        for i, card in enumerate(deck):
            tableau[i % 8].append(card)
        
        return FreeCellState(tableau)

    def save_state(self):
        self.history.append(self.copy())

    def undo(self):
        if self.history:
            previous_state = self.history.pop()
            self.tableau = previous_state.tableau
            self.free_cells = previous_state.free_cells
            self.foundations = previous_state.foundations





