import pygame
from ._screen import Screen
from ..types import Color, Button, State
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT

class GameModeScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        button_text_color = Color.WHITE
        button_bg_color = Color.BUTTON_BG
        button_hover_color = Color.BUTTON_HOVER

        # Create buttons for Player vs Player and Player vs AI
        self.buttons = [
            Button("Player vs Player", (SCREEN_WIDTH // 2) - 100, 225, self.font_sm, button_text_color, button_bg_color, button_hover_color, True),
            Button("Player vs AI", (SCREEN_WIDTH // 2) - 100, 300, self.font_sm, button_text_color, button_bg_color, button_hover_color, True)
        ]

        self.start_game_button = Button('START', SCREEN_WIDTH // 2, 400, self.font_md, button_text_color, button_bg_color, button_hover_color, True, False)
        self.selected_mode = None  # Stores whether Player vs Player or Player vs AI is selected

    def render(self, surface):
        surface.fill(Color.BACKGROUND)

        # Title text
        self.write('BATTLESHIP - Select Mode', self.font_lg, Color.WHITE, surface, SCREEN_WIDTH // 2, 75, True)

        # Draw buttons for Player vs Player and Player vs AI
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(surface)

        # Draw start button
        self.start_game_button.update(mouse_pos)
        self.start_game_button.draw(surface)

        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        # Set the selected mode based on button clicked
                        if button.text == "Player vs Player":
                            self.selected_mode = "PvP"
                        elif button.text == "Player vs AI":
                            self.selected_mode = "PvAI"

                        # Uncheck other buttons
                        for other_button in self.buttons:
                            if other_button != button:
                                other_button.is_checked = False
                                other_button.current_color = other_button.bg_color
                        button.is_checked = True

                if self.start_game_button.is_clicked(mouse_pos):
                    if self.selected_mode:
                        if self.selected_mode == "PvP":
                            self.game.set_state(State.SELECTION)  # Move to player selection
                        elif self.selected_mode == "PvAI":
                            self.game.set_state(State.AI_DIFFICULTY)  # Transition to the difficulty selection
