import pygame

from ._screen import Screen
from ..types import Color, Player, State
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, COL_SIZE
from ..audio import Audio

TURN_TRANSITION_EVENT = pygame.USEREVENT + 1

class PlayingScreen(Screen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.TURN_TRANSITION_DELAY = 1000
        self.volley_shot_clicks = 0
        self.volley_positions = []
        self.message = None
        self.message_timer = 0
        self.MESSAGE_DISPLAY_DURATION = 2000
        self.powerup_icons = {
            "Nuke": pygame.image.load("images/nuke_icon.png").convert_alpha(),
            "Horizontal Bombing Run": pygame.image.load("images/horizontal_icon.png").convert_alpha(),
            "Vertical Bombing Run": pygame.image.load("images/vertical_icon.png").convert_alpha(),
            "Volley": pygame.image.load("images/volley_icon.png").convert_alpha(),
            "Radar": pygame.image.load("images/radar_icon.png").convert_alpha(),
        }

    def draw_message(self, surface):

        if self.message:
            
            # determine message location per player
            if self.game.current_player == Player.ONE:
                message_x = SCREEN_WIDTH // 2
                message_y = SCREEN_HEIGHT // 4
            else:
                message_x = SCREEN_WIDTH // 2
                message_y = (SCREEN_HEIGHT // 4) * 3
            
            # render the message
            font = pygame.font.SysFont('impact', 32)
            message_surface = font.render(self.message, True, Color.RED)
            message_width = message_surface.get_width()
            message_x = (SCREEN_WIDTH - message_width) // 2
            surface.blit(message_surface, (message_x, message_y))
            if pygame.time.get_ticks() - self.message_timer > self.MESSAGE_DISPLAY_DURATION:
                self.message = None
    
    def draw_inventory(self, surface):
        # determine inventory location per player
        if self.game.current_player == Player.ONE:
            inventory_x = 0
            inventory_y = SCREEN_HEIGHT // 2
        else:
            inventory_x = 0
            inventory_y = SCREEN_HEIGHT // 2 - 80

        # make background
        inventory_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
        inventory_surface.fill((0, 0, 0, 100))
        surface.blit(inventory_surface, (inventory_x, inventory_y))

        # get powerups for the current player
        if self.game.current_player == Player.ONE:
            powerups = self.game.player_2_board.get_powerups()
        else:
            powerups = self.game.player_1_board.get_powerups()

        font = pygame.font.SysFont('impact', 16)
        for index, (powerup, available) in enumerate(zip(["Nuke", "Horizontal Bombing Run", "Vertical Bombing Run", "Volley", "Radar"], powerups)):
           
            icon_color = (255, 255, 255) if available else (100, 100, 100)
            icon = self.powerup_icons[powerup]
            icon = pygame.transform.scale(icon, (60, 60))  # scale icons to a fixed size
            tinted_icon = icon.copy()
            tinted_icon.fill(icon_color, special_flags=pygame.BLEND_RGBA_MULT)

            # Draw the icon
            icon_x = inventory_x + index * 80  # space icons horizontally
            icon_y = inventory_y + 10
            surface.blit(tinted_icon, (icon_x, icon_y))

            # Display key bind under the icon
            key_bind_text = font.render(f"({index + 1})", True, icon_color)
            key_bind_x = icon_x + 40  # center the key bind below the icon
            key_bind_y = inventory_y + 40
            surface.blit(key_bind_text, (key_bind_x, key_bind_y))

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

        self.draw_message(surface)
        self.draw_inventory(surface)


    def get_grid_position(self, mouse_pos):
        """Converts mouse position to grid coordinates."""
        grid_x = int(mouse_pos[0] // COL_SIZE)  # Convert to int to avoid float issues
        grid_y = int(mouse_pos[1] // COL_SIZE)  # Convert to int to avoid float issues
        return (grid_x, grid_y)


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.game.player_can_shoot:

                mouse_pos = pygame.mouse.get_pos()
                grid_pos = self.get_grid_position(mouse_pos)  # Convert to grid position
                # Check if we're using the Volley Shot
                if self.game.shot_selection == "volley":
                    # Append mouse positions
                    self.volley_positions.append(mouse_pos)
                    self.volley_shot_clicks += 1
                    if self.game.current_player == Player.ONE:
                        self.game.player_2_board.highlight_cells([grid_pos])
                        self.render(self.game.surface)
                    elif self.game.current_player == Player.TWO:
                        self.game.player_1_board.highlight_cells([grid_pos])
                        self.render(self.game.surface)

                    # Check if 4 clicks have been made
                    if self.volley_shot_clicks == 4:
                        # Reset highlights after processing
                        if self.game.current_player == Player.ONE:
                            self.game.player_2_board.reset_highlights()
                        elif self.game.current_player == Player.TWO:
                            self.game.player_1_board.reset_highlights()
                        # Process all 4 shots
                        for position in self.volley_positions:
                            if self.game.current_player == Player.ONE:
                                hit = self.game.player_2_board.hit_pos(position)
                            elif self.game.current_player == Player.TWO:
                                hit = self.game.player_1_board.hit_pos(position)

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
                            self.message = "Ship detected at " + str(self.game.player_2_board.ships[0].coordinates)
                            self.message_timer = pygame.time.get_ticks()
                            self.game.player_2_board.highlight_cells(self.game.player_2_board.ships[0].coordinates)
                        elif self.game.current_player == Player.TWO:
                            self.message = "Ship detected at " + str(self.game.player_1_board.ships[0].coordinates)
                            self.message_timer = pygame.time.get_ticks()
                            self.game.player_2_board.highlight_cells(self.game.player_2_board.ships[0].coordinates)


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
                        else:
                            self.message = "Not Valid"
                            self.message_timer = pygame.time.get_ticks()
                            # Audio.play_error()

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
                        # Audio.play_use()
                    else:
                        self.message = "Not Available"
                        self.message_timer = pygame.time.get_ticks()
                        # Audio.play_error()
                if event.key == pygame.K_2:
                    if powerups[1] == True:
                        self.game.rotate_shot_selection(2)
                        self.game.set_powerup_activity()
                        powerups[1] = False
                        # Audio.play_use()
                    else:
                        self.message = "Not Available"
                        self.message_timer = pygame.time.get_ticks()
                        # Audio.play_error()
                if event.key == pygame.K_3:
                    if powerups[2] == True:
                        self.game.rotate_shot_selection(3)
                        self.game.set_powerup_activity()
                        powerups[2] = False
                        # Audio.play_use()
                    else:
                        self.message = "Not Available"
                        self.message_timer = pygame.time.get_ticks()
                        # Audio.play_error()
                if event.key == pygame.K_4:
                    if powerups[3] == True:
                        self.game.rotate_shot_selection(4)
                        self.game.set_powerup_activity()
                        powerups[3] = False
                        # Audio.play_use()
                    else:
                        self.message = "Not Available"
                        self.message_timer = pygame.time.get_ticks()
                        # Audio.play_error()
                if event.key == pygame.K_5:
                    if powerups[4] == True:
                        self.game.rotate_shot_selection(5)
                        self.game.set_powerup_activity()
                        powerups[4] = False
                        # Audio.play_use()
                    else:
                        self.message = "Not Available"
                        self.message_timer = pygame.time.get_ticks()
                        # Audio.play_error()
                        
                #set the powerup list for current player so a selected powerup is consumed
                if self.game.current_player == Player.ONE:
                    self.game.player_2_board.set_powerups(powerups)
                if self.game.current_player == Player.TWO:
                    self.game.player_1_board.set_powerups(powerups)
                
