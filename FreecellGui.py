import tkinter as tk
from tkinter import Canvas

class FreeCellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FreeCell Solitaire")
        self.canvas = Canvas(root, width=1000, height=1000, bg="green")
        self.canvas.pack()
        self.draw_board()
    
    def draw_board(self):
        for i in range(4):
            self.canvas.create_rectangle(50 + i * 100, 50, 130 + i * 100, 130, outline="white", width=2)
            self.canvas.create_text(90 + i * 100, 90, text=f"Free {i+1}", fill="white")
        for i in range(4):
            self.canvas.create_rectangle(450 + i * 100, 50, 530 + i * 100, 130, outline="white", width=2)
            self.canvas.create_text(490 + i * 100, 90, text=f"Found {i+1}", fill="white")
        for i in range(8):
            self.canvas.create_rectangle(50 + i * 100, 200, 130 + i * 100, 280, outline="white", width=2)
            self.canvas.create_text(90 + i * 100, 240, text=f"Col {i+1}", fill="white")