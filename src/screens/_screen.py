import pygame

from typing import List

class Screen:
    def __init__(self, game) -> None:
        self.game = game

        # Load the font
        self.font_sm = pygame.font.SysFont('impact', 20)
        self.font_md = pygame.font.SysFont('impact', 45)
        self.font_lg = pygame.font.SysFont('impact', 65)

    def handle_events(self, events: List[pygame.event.Event]):
        pass

    def update(self):
        pass

    def render(self, surface: pygame.Surface):
        pass

    def write(self, text: str, font: pygame.font.Font, color: tuple, surface: pygame.Surface, x: int, y: int, center=False):
        text = font.render(text, True, color)
        if center:
            rect = text.get_rect(center=(x, y))
        else:
            rect = text.get_rect(topleft=(x, y))

        surface.blit(text, rect)
