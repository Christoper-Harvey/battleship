import sys
import pygame
from typing import List

from .config import FPS, SCREEN_HEIGHT, GRID_SIZE

from .board import Board
from .types import State, Player

from .screens import MenuScreen, PlayingScreen, FinishScreen, SelectionScreen, TurnTransition, BeginGameScreen
from .screens.game_mode import GameModeScreen
from .screens.difficulty_screen import DifficultyScreen

from .cpu import CPU

HALF_HEIGHT = SCREEN_HEIGHT / 2

TURN_TRANSITION_EVENT = pygame.USEREVENT + 1

class Game:
    def __init__(self, clock, surface: pygame.Surface, grid_size: int) -> None:
        self._running = True
        self.clock = clock
        self.num_ships = 1

        self.current_player = Player.ONE
        self.player_can_shoot = True

        self.shot_selection = "single" #tracks player's powerup shot selection - can be "single", "carpet", "run_h", "run_v"
        self.powerup_activity = False #tracks if a powerup is selected so it can only happen once per turn

        self.surface = surface
        self.player_1_board = None
        self.player_2_board = None
        self.cpu = None  # Add CPU instance for AI
        self.ai_difficulty = None  # AI difficulty attribute

        self.winner = None
        self.game_over = False

        self.message = None

        self.state: State = State.START
        self.screens = {
            State.START: MenuScreen(self),
            State.GAME_MODE: GameModeScreen(self),  # Add GameMode screen
            State.AI_DIFFICULTY: DifficultyScreen(self),  # Add the AI difficulty screen
            State.SELECTION: SelectionScreen(self),
            State.TURN_TRANSITION: TurnTransition(self),
            State.PLAYING: PlayingScreen(self),
            State.END: FinishScreen(self, self.winner),
            State.BEGIN_GAME: BeginGameScreen(self)
        }

    def set_state(self, new_state):
        self.state = new_state

    def set_num_ships(self, num_ships):
        print("set num ships: ", num_ships)
        self.num_ships = num_ships
        print(self.num_ships)

        self.player_1_board = Board(y_offset=SCREEN_HEIGHT / 2, board_size=GRID_SIZE, ship_size=self.num_ships)
        self.player_2_board = Board(y_offset=0, board_size=GRID_SIZE, ship_size=self.num_ships)

    def rotate_shot_selection(self, selection = int):
        if selection == 1:
            self.shot_selection = "nuke"
            print("NUKE")
        elif selection == 2:
            self.shot_selection = "run_h"
            print("BOMBING RUN (horizontal)")
        elif selection == 3:
            self.shot_selection = "run_v"
            print("BOMBING RUN (vertical)")
        elif selection == 4:
            self.shot_selection = "volley"
            print("VOLLY")
        elif selection == 5:
            self.shot_selection = "radar"
            print("RADAR")

    def set_powerup_activity(self):
        self.powerup_activity = True

    def reset_shot_selection(self):
        self.shot_selection = "single"
        self.powerup_activity = False

    def start_ai_game(self):
        """Start a game with a CPU opponent."""
        self.cpu = CPU(self.num_ships)  # Initialize CPU
        self.player_1_board = Board(y_offset=SCREEN_HEIGHT / 2, board_size=GRID_SIZE, ship_size=self.num_ships)
        self.player_2_board = self.cpu.board  # Set player 2 board to the CPU's board

        self.set_state(State.SELECTION)  # Proceed to ship selection

    def run(self):
        while self._running:
            if self.game_over:
                self.state = State.END
                while self.game_over:
                    events = pygame.event.get()
                    self.screens[self.state].render(self.surface)
                    self.screens[self.state].handle_events(events)
                    self.screens[self.state].update()
                    pygame.display.update()
                    self.clock.tick(FPS)

                    result = self.screens[self.state].handle_events(events)
                    if result == 'restart':
                        self.reset_game()
                        break
                    elif result is None:
                        continue

            events = pygame.event.get()
            self.screens[self.state].render(self.surface)
            self.screens[self.state].handle_events(events)
            self.screens[self.state].update()

            self.handle_global_events(events)
            self.handle_global_update()

            if self.player_1_board != None and self.player_2_board != None:
                self.check_end_game()

            # If it's the AI's turn, perform the AI's attack and end its turn
            if self.current_player == Player.TWO and isinstance(self.cpu, CPU):
                self.ai_turn()

    def ai_turn(self):
        """Handles the AI's turn and switches back to Player 1."""
        if self.cpu:
            # Call the AI's attack method (easy_attack, medium_attack, or hard_attack)
            if self.ai_difficulty == "easy":
                self.cpu.easy_attack(self.player_1_board)  # AI attacks Player 1's board
            elif self.ai_difficulty == "medium":
                self.cpu.medium_attack(self.player_1_board)
            elif self.ai_difficulty == "hard":
                self.cpu.hard_attack(self.player_1_board)

            # After AI attack, switch back to Player 1's turn
            self.current_player = Player.ONE
            
            # Set a one-time event to transition after AI's turn
            pygame.time.set_timer(TURN_TRANSITION_EVENT, 1000, loops=1)  # Transition after 1 second



    def handle_global_events(self, events: List[pygame.event.Event]):
        """
        Handles catching and processing events which happen each frame: i.e., game logic
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
                sys.exit()

    def handle_global_update(self):
        """
        Handles advancing the game state
        """
        pygame.display.update()
        self.clock.tick(FPS)

    def check_end_game(self):
        """
        Check if the game has ended and set the winner.
        """
        if self.player_1_board.all_ships_sunk():
            self.game_over = True
            self.winner = Player.TWO
            # Update the FinishScreen instance in self.screens
            self.screens[State.END] = FinishScreen(self, 2)
        elif self.player_2_board.all_ships_sunk():
            self.game_over = True
            self.winner = Player.ONE
            # Update the FinishScreen instance in self.screens
            self.screens[State.END] = FinishScreen(self, 1)

    def reset_game(self):
        self.game_over = False
        self.winner = None
        self.set_state(State.START)  # Reset to the starting state
        self.set_num_ships(self.num_ships)  # Reinitialize ship count and other game components