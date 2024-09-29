import pygame

from typing import Tuple
from enum import Enum

Coordinate = Tuple[int, int]


class Color:
    BACKGROUND = pygame.Color(28, 50, 93)
    CELL_NEUTRAL = pygame.Color(44, 73, 127)
    CELL_HIT = pygame.Color(255, 0, 0)
    CELL_SHIP = pygame.Color(0, 255, 0)
    GREEN = pygame.Color(106, 141, 115)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREY = pygame.Color(128, 128, 128)
    RED = pygame.Color(219, 48, 105)
    BLUE = pygame.Color(0, 0, 255)
    DARK_BLUE = pygame.Color(0, 0, 139)
    BUTTON_BG = pygame.Color(0, 128, 255)  # A dark blue
    BUTTON_HOVER = pygame.Color(0, 200, 255)  # a lighter blue than BUTTON_BG
    PLAYER_1_BOARD_COLOR = pygame.Color(30, 93, 156)
    PLAYER_2_BOARD_COLOR = pygame.Color(111, 169, 227)


class State(Enum):
    START = 1
    SELECTION = 2
    TURN_TRANSITION = 3
    PLAYING = 4
    END = 5
    BEGIN_GAME = 6


class Player(Enum):
    ONE = 1
    TWO = 2


class Button:
    def __init__(self, text, x: int, y: int, font: pygame.font.Font, text_color: pygame.Color, bg_color: pygame.Color, hover_color: pygame.Color, center=False, square=True):
        self.square = square
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.center = center
        self.current_color = bg_color
        self.clicked_color = Color.GREEN
        self.rect = None
        self.is_checked = False  # New attribute to track checked state

    def draw(self, surface: pygame.Surface):
        text_surface = self.font.render(self.text, True, self.text_color)
        if self.rect is None:
            if self.center:
                self.rect = text_surface.get_rect(center=(self.x, self.y))
            else:
                self.rect = text_surface.get_rect(topleft=(self.x, self.y))

            if self.square:
                self.rect.width = self.rect.height = max(
                    self.rect.width + 10, self.rect.height + 10)
            else:
                self.rect.inflate_ip(75, 10)  # Add some padding

        pygame.draw.rect(surface, self.current_color, self.rect)
        surface.blit(text_surface, text_surface.get_rect(
            center=self.rect.center))

    def update(self, mouse_pos):
        if self.rect is None:
            return
        if self.rect.collidepoint(mouse_pos):
            if not self.is_checked:
                self.current_color = self.hover_color
        else:
            if not self.is_checked:
                self.current_color = self.bg_color

    def is_clicked(self, mouse_pos: Coordinate):
        if self.rect is None:
            return False
        if self.rect.collidepoint(mouse_pos):
            self.is_checked = not self.is_checked
            self.current_color = self.clicked_color if self.is_checked else self.bg_color
            return True
        return False
