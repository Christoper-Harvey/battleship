#Name: Ian Collins
#Date: 9/22/2024
#Course: EECS 581
#Purpose: Define the AI player class and methods to player battleship with the user

from random import randint
from . import ship, cell, board
from .config import COL_SIZE, SCREEN_HEIGHT, GRID_SIZE

class CPU():
    #The CPU manages the hits, misses, ships sunk, its board, and its ships after being randomly generated
    def __init__(self, num_ships):
        self.ships = []
        self.hits = []
        self.miss = []
        self.ships_sunk = 0
        self.board = board.Board(y_offset=0, board_size=GRID_SIZE, ship_size=num_ships)
        self.create_ships(num_ships)
        self.board.ships = self.ships
    
    #Randomly generates and adds all of the ships to CPU's ships
    def create_ships(self, num_ship):
        # Defines coordinates that are used
        used_coord = []
        shipLength = [1, 2, 3, 4, 5]
        i = 0
        # Iterates ship lengths until all ships are populated
        while i < num_ship:
            new_ship = None
            
            # Generates ships coordinates until a valid ship is generated
            while new_ship is None:
                new_ship = self.place_ships(shipLength[i], used_coord)
            # Adds ships to CPU's ships and used coordinates
            self.ships.append(new_ship)
            used_coord.extend(new_ship.coordinates)  # Make sure to update used coordinates
            self.board.mark_ship_cells(new_ship)
            i += 1

    def record_hit(self, coord_cell, otherBoard):
        coord = coord_cell.coordinate
        #Checks if the shoot is a hit or miss
        if coord_cell.hit(coord, otherBoard):
            self.hits.append(coord)
        else:
            self.miss.append(coord)

    # Generates coordinates for ships and either returns a valid ship or None
    def place_ships(self, size, used_coord):
        # Determines direction of ship
        direction = randint(0, 1)
        
        # Creates head of ship
        x = randint(0, 9)
        y = randint(0, 9)

        # Vertical direction
        if direction == 0:
            direction = 'VERTICAL'
            if (y + size) > 9:
                y -= size
            ship_coord = [(x, i) for i in range(y, y + size)]
        # Horizontal direction
        else:
            direction = 'HORIZONTAL'
            if (x + size) > 9:
                x -= size
            ship_coord = [(n, y) for n in range(x, x + size)]
        
        # Checks if ship coordinates are already in use
        for coord in ship_coord:
            if coord in used_coord:
                return None

        # Returns a valid ship
        return ship.Ship(x, y, size, direction)
    
    def easy_attack(self, otherBoard):
        # Generates random points to attack that have not been used yet
        cond = True
        while cond:
            # Generate coordinates
            x = randint(0, 9)
            y = randint(0, 9)
            coord = (x, y)

            # Check if coordinates have been used
            if coord in self.miss or coord in self.hits:
                continue
            cond = False

        # Get the cell from Player 1's board and perform the hit
        coord_cell = otherBoard.cells[y][x]  # Make sure you're accessing the correct cell

        # Register the hit or miss
        self.record_hit(coord_cell, otherBoard)

        # If a ship is sunk, handle it
        if otherBoard.check_ship_sunk(coord_cell):
            self.ships_sunk += 1


    def medium_attack(self, otherBoard):
        #Sets up variable to track which ship is currently being attacked
        global cur_hits 
        cur_hits = []

        #Random hits mode
        if len(cur_hits) == 0:
            #Generates random points to attack that has not been used yet
            cond = True
            while cond:
                #Generate coordinates
                x = randint(0, 9)
                y = randint(0, 9)
                coord = (x,y)

                #Checks if coordinates have been used to continue generation
                if coord in self.miss or coord in self.hits:
                    continue
                #Break loop
                cond = False

            #Gets cell and coordinate from board array
            coord_cell = otherBoard.cells[coord[1], coord[0]]

            #Checks if the shoot is a hit or miss
            self.record_hit(coord_cell, otherBoard)
            cur_hits.append(coord)

        #Targeted attack mode
        else:
            #Generates coordinate from generated cell index
            coord = cur_hits[0]
            #Gets cell and coordinate from board array
            coord_cell = otherBoard.cells[coord[1], coord[0]]
            #Finds direction after intial hit
            if len(cur_hits) == 1:
                #Checks coord of cell above 
                if (coord[1] - 1) >= 0 and coord != self.miss:
                    #Checks if the shoot is a hit or miss
                    self.record_hit(coord_cell, otherBoard)
                    cur_hits.append(coord)
                    
                #Checks coord of cell to the right
                elif (coord[0] + 1) % 10 != 0 and coord != self.miss:
                    #Checks if the shoot is a hit or miss
                    self.record_hit(coord_cell, otherBoard)
                    cur_hits.append(coord)
                    
                #Checks coord of cell below
                elif (coord[1] + 1) <= 9 and coord != self.miss:
                    #Checks if the shoot is a hit or miss
                    self.record_hit(coord_cell, otherBoard)
                    cur_hits.append(coord)
                    
                #Checks coord of cell to the left
                elif (coord[0] - 1) >= 0 and coord != self.miss:
                    #Checks if the shoot is a hit or miss
                    self.record_hit(coord_cell, otherBoard)
                    cur_hits.append(coord)
                    
            elif len(cur_hits) > 1:
                #Ship verticle
                if cur_hits[0][0] == cur_hits[1][0]:
                    #Checks upper bound
                    if coord[1] == 0:
                        coord = (coord[0], len(cur_hits))
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
                        
                    #Checks lower bound
                    elif coord[1] == 9:
                        coord = (coord[0], 10-len(cur_hits))
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
                        
                    #Attacks down the ship before going up
                    else:
                        x = coord[0]
                        y = coord[1]
                        if y + len(cur_hits) <= 9 and (x,y+len(cur_hits)) not in self.miss:
                            coord = (coord[0], y+len(cur_hits))
                        else:
                            coord = (coord[0], y-len(cur_hits))
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
                        
                #Ship horizontal
                elif coord[1] == cur_hits[1][1]:
                    #Checks upper bound
                    if coord[0] == 0:
                        coord = (coord[0], len(cur_hits))
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
                        
                    #Checks lower bound
                    elif coord[0] == 9:
                        coord = (cur_hits[0][0], 10-len(cur_hits))
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
                        
                    #Attacks down the ship before going up
                    else:
                        x = coord[0]
                        y = coord[1]
                        if x + len(cur_hits) <= 9 and (x+len(cur_hits),y) not in self.miss:
                            coord = (x+len(cur_hits), y)
                        else:
                            coord = (x-len(cur_hits), y)
                        self.record_hit(otherBoard.cells[coord[1]][coord[0]], otherBoard)
                        cur_hits.append(coord)
        #Checks if ship was sunk
        coord_cell = otherBoard.cells[coord[1],coord[0]]
        if otherBoard.check_ship_sunk(coord_cell):
            self.ships_sunk += 1
            cur_hits = []

    #Attack function that knows where all of the ships are
    #This mode utilizes the self.hits differently than the other functions as hits will be used to store the locations of all of the player ships
    def hard_attack(self, otherBoard):
        #Populates self.hits of the coordinates of the player's ships
        if len(self.hits) == 0 and self.ships_sunk == 0:
            for ship in otherBoard.ships:
                self.hits.append(ship.coordinates)
        else:
            if len(self.hits) != 0:
                hit = self.hits[0]
                coord_cell = otherBoard.cells[hit[1]][hit[0]]
                coord_cell.hit(hit)
                self.hits.pop(0)
            