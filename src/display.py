import pygame

from .types import Color

def initialize_game_window(width, height):
    GAME_WINDOW = pygame.display.set_mode(size=(width, height))
    GAME_WINDOW.fill(Color.WHITE)

    pygame.display.set_caption("Battleship")
    return GAME_WINDOW
