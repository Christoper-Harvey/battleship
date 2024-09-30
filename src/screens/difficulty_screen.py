import pygame
from typing import List
from ._screen import Screen
from ..types import Color, Button, State

class DifficultyScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        # Buttons for difficulty selection
        button_text_color = Color.WHITE
        button_bg_color = Color.BUTTON_BG
        button_hover_color = Color.BUTTON_HOVER

        self.buttons = [
            Button("    Easy    ", game.surface.get_width() // 2, 200, self.font_md, button_text_color, button_bg_color, button_hover_color, True),
            Button("Medium", game.surface.get_width() // 2, 400, self.font_md, button_text_color, button_bg_color, button_hover_color, True),
            Button("    Hard    ", game.surface.get_width() // 2, 600, self.font_md, button_text_color, button_bg_color, button_hover_color, True),
        ]

    def render(self, surface):
        surface.fill(Color.BACKGROUND)

        # Title text
        self.write('DIFFICULTY', self.font_lg, Color.WHITE, surface, surface.get_width() // 2, 75, True)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(surface)

        pygame.display.flip()

    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.is_clicked(mouse_pos):
                        if i == 0:  # Easy
                            self.game.ai_difficulty = "easy"
                        elif i == 1:  # Medium
                            self.game.ai_difficulty = "medium"
                        elif i == 2:  # Hard
                            self.game.ai_difficulty = "hard"

                        self.game.start_ai_game()  # Now start the AI game
                        break
