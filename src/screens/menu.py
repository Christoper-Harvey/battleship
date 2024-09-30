import pygame

from ._screen import Screen
from ..types import State, Color, Button
from ..config import SCREEN_WIDTH

class MenuScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)

        self.ship_count = None

        button_text_color = Color.WHITE
        button_bg_color = Color.BUTTON_BG
        button_hover_color = Color.BUTTON_HOVER

        self.buttons = [
            Button(str(i), (SCREEN_WIDTH // 6) + (i-1) * 60, 225, self.font_sm, button_text_color, button_bg_color, button_hover_color, True)
            for i in range(1, 6)
        ]

        self.start_game_button = Button('PLAY', SCREEN_WIDTH // 2, 400, self.font_md, button_text_color, button_bg_color, button_hover_color, True, False)
        self.selected_ships = None

    def render(self, surface):
        surface.fill(Color.BACKGROUND)

        # Title text
        self.write('BATTLESHIP', self.font_lg, Color.WHITE, surface, SCREEN_WIDTH // 2, 75, True)
        self.write('——————————', self.font_sm, Color.WHITE, surface, SCREEN_WIDTH // 2, 125, True)

        # Ship selection text
        self.write('Select the number of ships:', self.font_sm, Color.WHITE, surface, SCREEN_WIDTH // 2, 175, True)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(surface)

        # start game button
        self.start_game_button.update(mouse_pos)
        self.start_game_button.draw(surface)

        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.is_clicked(mouse_pos):
                        if button.is_checked:
                            print("setting num ships to", i + 1)
                            self.selected_ships = i + 1
                            self.game.set_num_ships(i + 1)
                        else:
                            self.selected_ships = None
                            self.game.set_num_ships(None)

                        # Uncheck all other buttons
                        for other_button in self.buttons:
                            if other_button != button:
                                other_button.is_checked = False
                                other_button.current_color = other_button.bg_color
                        break

                if self.start_game_button.is_clicked(mouse_pos):
                    if self.selected_ships is not None:
                        self.game.set_state(State.SELECTION)

