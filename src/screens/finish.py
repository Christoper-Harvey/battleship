import pygame
import sys
from ._screen import Screen
from ..types import Color

class FinishScreen(Screen):
    def __init__(self, game, winner):
        super().__init__(game)
        self.winner = winner

    def render(self, surface):
        font = pygame.font.SysFont("Impact", 38)
        small_font = pygame.font.SysFont("Impact", 26)

        text = f"Player {self.winner} Wins!"
        text_surface = font.render(text, True, pygame.Color('white'))

        instructions = "Press Q to Quit or R to Play Again"
        instructions_surface = small_font.render(instructions, True, pygame.Color('white'))

        surface.fill(Color.BACKGROUND)

        surface.blit(text_surface, (surface.get_width() // 2 - text_surface.get_width() // 2, surface.get_height() // 2 - text_surface.get_height() // 2 - 50))
        surface.blit(instructions_surface, (surface.get_width() // 2 - instructions_surface.get_width() // 2, surface.get_height() // 2 - instructions_surface.get_height() // 2 + 50))

        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print('quit')
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    print('restart')
                    return 'restart'

        return None