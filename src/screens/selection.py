import pygame

from ._screen import Screen
from ..types  import Color, State, Player
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE


class SelectionScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.shipsToPlace = game.num_ships

    def render(self, surface):
        surface.fill(Color.BACKGROUND)

        self.place_ship_instructions(surface, self.game.current_player)

        if self.game.current_player == Player.ONE:
            self.game.player_1_board.spawnShip()
            self.game.current_player = Player.TWO
        elif self.game.current_player == Player.TWO:
            self.game.player_2_board.spawnShip()
            self.game.current_player = Player.ONE
            self.game.set_state(State.BEGIN_GAME)

    def place_ship_instructions(self, surface: pygame.Surface, player: Player):
        if player == Player.ONE:
            half_of_player_screen = SCREEN_HEIGHT / 4
            initial_offset = half_of_player_screen - (half_of_player_screen / 2)
        elif player == Player.TWO:
            half_of_player_screen =  3 * SCREEN_HEIGHT / 4
            initial_offset = half_of_player_screen - (half_of_player_screen / 6)

        middle_of_screen = SCREEN_WIDTH // 2

        self.write('PLACE YOUR SHIPS', self.font_md, Color.WHITE, surface, middle_of_screen, initial_offset, True)
        self.write('————————————————', self.font_sm, Color.WHITE, surface, middle_of_screen, initial_offset + 25, True)
        self.write("Use ←↑→↓ to move the ship", self.font_sm, Color.WHITE, surface, middle_of_screen, initial_offset + 55, True)
        self.write("Use R to rotate the ship", self.font_sm, Color.WHITE, surface, middle_of_screen, initial_offset + 85, True)
        self.write("Press ENTER to confirm ship location", self.font_sm, Color.WHITE, surface, middle_of_screen, initial_offset + 115, True)
        self.write(f"Ships to place: {self.game.num_ships}", self.font_sm, Color.WHITE, surface, middle_of_screen, initial_offset + 145, True)
