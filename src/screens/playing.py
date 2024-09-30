import pygame

from ._screen import Screen
from ..types import Color, Player, State
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, COL_SIZE
from ..audio import Audio

TURN_TRANSITION_EVENT = pygame.USEREVENT + 1

class PlayingScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.TURN_TRANSITION_DELAY = 1000  # 1 second delay
        self.volley_shot_clicks = 0        # Track number of volley shot clicks
        self.volley_positions = []         # Store volley shot positions

    def draw_inventory(self, surface):
        
        # determine inventory location per player
        if self.game.current_player == Player.ONE:
            inventory_x = 0  # Starting x position for Player One's inventory
            inventory_y = SCREEN_HEIGHT // 2  # Position slightly below the bottom of Player One's board
        else:  # Player Two
            inventory_x = 0  # Starting x position for Player Two's inventory
            inventory_y = SCREEN_HEIGHT // 2 - 80  # Position below Player Two's board

        # make background
        inventory_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
        inventory_surface.fill((0, 0, 0, 180))
        surface.blit(inventory_surface, (inventory_x, inventory_y))

        # get powerups for the current player
        if self.game.current_player == Player.ONE:
            powerups = self.game.player_2_board.get_powerups()
        else:
            powerups = self.game.player_1_board.get_powerups()

        font = pygame.font.SysFont('impact', 24)
        for index, (powerup, available) in enumerate(zip(["Nuke", "Horizontal Bombing Run", "Vertical Bombing Run", "Volley", "Radar"], powerups)):
            key = index + 1
            if available:
                text = font.render(f"{key}: {powerup}", True, Color.WHITE)
            else:
                text = font.render(f"{key}: {powerup}", True, Color.GREY)

            surface.blit(text, (inventory_x + 20, inventory_y + 20 * index))

    def render(self, surface):
        surface.fill(Color.BACKGROUND)

        # Create overlay if it doesn't exist
        if not hasattr(self, 'overlay'):
            self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
            self.overlay.fill((0, 0, 0, 100))  # Semi-transparent red

        if self.game.current_player == Player.ONE:
            self.game.player_1_board.draw(surface)
            self.game.player_2_board.draw(surface, False)
            # Apply overlay to bottom half (Player 2's board)
            surface.blit(self.overlay, (0, SCREEN_HEIGHT // 2))
        elif self.game.current_player == Player.TWO:
            self.game.player_1_board.draw(surface, False)
            self.game.player_2_board.draw(surface)
            # Apply overlay to top half (Player 1's board)
            surface.blit(self.overlay, (0, 0))

        self.draw_inventory(surface)



    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.game.player_can_shoot:

                mouse_pos = pygame.mouse.get_pos()
                # Check if we're using the Volley Shot
                if self.game.shot_selection == "volley":
                    # Append mouse positions
                    self.volley_positions.append(mouse_pos)
                    self.volley_shot_clicks += 1

                    print(f"Volley Shot: {self.volley_shot_clicks} clicks registered")

                    # Check if 4 clicks have been made
                    if self.volley_shot_clicks == 4:
                        print("Volley Shot: 4 shots selected, processing...")
                        # Process all 4 shots
                        for position in self.volley_positions:
                            if self.game.current_player == Player.ONE:
                                hit = self.game.player_2_board.hit_pos(position)
                            elif self.game.current_player == Player.TWO:
                                hit = self.game.player_1_board.hit_pos(position)

                            if hit:
                                print(f"Hit at {position}")
                            else:
                                print(f"Miss at {position}")

                        # Reset for next turn
                        self.game.player_can_shoot = False  # Disable shooting
                        pygame.time.set_timer(TURN_TRANSITION_EVENT, self.TURN_TRANSITION_DELAY, loops=1)
                        self.volley_shot_clicks = 0
                        self.volley_positions = []

                else:
                    mouse_pos = [mouse_pos]
                    if self.game.shot_selection == "nuke":  #adds mouse positions for all nuke tiles
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]+COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0]+COL_SIZE, mouse_pos[0][1]+COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0]+COL_SIZE, mouse_pos[0][1]))
                        mouse_pos.append((mouse_pos[0][0]+COL_SIZE, mouse_pos[0][1]-COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]-COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0]-COL_SIZE, mouse_pos[0][1]-COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0]-COL_SIZE, mouse_pos[0][1]))
                        mouse_pos.append((mouse_pos[0][0]-COL_SIZE, mouse_pos[0][1]+COL_SIZE))
                    elif self.game.shot_selection == "run_h":   #adds mouse postions for all horizontal bombing run tiles
                        mouse_pos.append((mouse_pos[0][0]+COL_SIZE, mouse_pos[0][1]))
                        mouse_pos.append((mouse_pos[0][0]+COL_SIZE+COL_SIZE, mouse_pos[0][1]))
                        mouse_pos.append((mouse_pos[0][0]-COL_SIZE, mouse_pos[0][1]))
                        mouse_pos.append((mouse_pos[0][0]-COL_SIZE-COL_SIZE, mouse_pos[0][1]))
                    elif self.game.shot_selection == "run_v":   #adds mouse positions for all vertical bombing run tiles
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]+COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]+COL_SIZE+COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]-COL_SIZE))
                        mouse_pos.append((mouse_pos[0][0], mouse_pos[0][1]-COL_SIZE-COL_SIZE))
                    elif self.game.shot_selection == "radar":   #adds mouse positions for all vertical bombing run tiles
                        if self.game.current_player == Player.ONE:
                            print(self.game.player_2_board.ships[0].coordinates)
                        elif self.game.current_player == Player.TWO:
                            print(self.game.player_1_board.ships[0].coordinates)


                    for position in mouse_pos:
                        if self.game.current_player == Player.ONE:
                            hit = self.game.player_2_board.hit_pos(position)
                        elif self.game.current_player == Player.TWO:
                            hit = self.game.player_1_board.hit_pos(position)

                        if hit:
                            # Disable shooting after the first valid shot
                            self.game.player_can_shoot = False
                            # Set a timer for turn transition
                            pygame.time.set_timer(TURN_TRANSITION_EVENT, self.TURN_TRANSITION_DELAY, loops=1)

            elif event.type == TURN_TRANSITION_EVENT:
                self.game.player_can_shoot = True
                # This event will be triggered after the delay
                self.game.set_state(State.TURN_TRANSITION)

            elif (event.type == pygame.KEYDOWN) and (self.game.powerup_activity == False):             
                #grab the powerup list for current player
                if self.game.current_player == Player.ONE:
                    powerups = self.game.player_2_board.get_powerups()
                elif self.game.current_player == Player.TWO:
                    powerups = self.game.player_1_board.get_powerups()

                #handle powerups for current player
                if event.key == pygame.K_1:
                    if powerups[0] == True:
                        self.game.rotate_shot_selection(1)
                        self.game.set_powerup_activity()
                        powerups[0] = False
                    else:
                        print("You do not have this powerup")
                if event.key == pygame.K_2:
                    if powerups[1] == True:
                        self.game.rotate_shot_selection(2)
                        self.game.set_powerup_activity()
                        powerups[1] = False
                    else:
                        print("You do not have this powerup")
                if event.key == pygame.K_3:
                    if powerups[2] == True:
                        self.game.rotate_shot_selection(3)
                        self.game.set_powerup_activity()
                        powerups[2] = False
                    else:
                        print("You do not have this powerup")
                if event.key == pygame.K_4:
                    if powerups[3] == True:
                        self.game.rotate_shot_selection(4)
                        self.game.set_powerup_activity()
                        powerups[3] = False
                    else:
                        print("You do not have this powerup")
                if event.key == pygame.K_5:
                    if powerups[4] == True:
                        self.game.rotate_shot_selection(5)
                        self.game.set_powerup_activity()
                        powerups[4] = False
                    else:
                        print("You do not have this powerup")
                        
                #set the powerup list for current player so a selected powerup is consumed
                if self.game.current_player == Player.ONE:
                    self.game.player_2_board.set_powerups(powerups)
                if self.game.current_player == Player.TWO:
                    self.game.player_1_board.set_powerups(powerups)
                
