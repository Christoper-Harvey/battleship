from typing import List
import pygame

from pygame import Surface
from pygame.event import Event
from ._screen import Screen

from ..types import Button, Color, State, Player
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT


class TurnTransition(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.game = game
        self.continue_button = Button("Continue", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      self.font_md, Color.WHITE, Color.BUTTON_BG, Color.BUTTON_HOVER, True, False)

    def render(self, surface: Surface):
        surface.fill(Color.BACKGROUND)
        self.write(f"Player {self.other_player().value}'s Turn",
                   self.font_md, Color.WHITE, surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, True)
        self.continue_button.draw(surface)
        self.continue_button.update(pygame.mouse.get_pos())

        pygame.display.update()

    def other_player(self):
        return Player.TWO if self.game.current_player == Player.ONE else Player.ONE

    def handle_events(self, events: List[Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.continue_button.is_clicked(mouse_pos):
                    self.continue_button.is_checked = False
                    self.game.current_player = self.other_player()
                    self.game.set_state(State.PLAYING)
                    self.game.reset_shot_selection()  #makes sure next player will fire with single shot

