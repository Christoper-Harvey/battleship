import pygame
from typing import Literal

from .config import SCREEN_HEIGHT, SCREEN_WIDTH, GRID_SIZE
from .types import Coordinate


class Ship:

    def __init__(self, x: int, y: int, length: int, direction: Literal["VERTICAL", "HORIZONTAL"]) -> None:
        self.coordinates = []
        self.length = length
        self.direction = direction
        self.createShip(x, y)

    def createShip(self, x: int, y: int):
        """
        Create the ship at the given coordinates
        """
        self.coordinates = []
        for i in range(self.length):
            if self.direction == "VERTICAL":
                self.coordinates.append((x, y - i))
            elif self.direction == "HORIZONTAL":
                self.coordinates.append((x + i, y))
        pass

    def draw(self, board) -> None:
        """
        Draw the ship on the board
        """
        for coord in self.coordinates:
            x, y = coord
            if 0 <= x < len(board.cells) and 0 <= y < len(board.cells[0]):
                board.cells[y][x].is_active = True

    def move(self, direction: Literal["UP", "RIGHT", "DOWN", "LEFT"]) -> None:
        """
        Move the ship in the given direction
        """
        dx, dy = 0, 0
        if direction == "UP":
            dy = -1
        elif direction == "RIGHT":
            dx = 1
        elif direction == "DOWN":
            dy = 1
        elif direction == "LEFT":
            dx = -1

        new_coordinates = []
        update = True

        # Calculate new coordinates
        for coord in self.coordinates:
            new_x = coord[0] + dx
            new_y = coord[1] + dy
            if 0 <= new_x <= 9 and 0 <= new_y <= 9:
                new_coordinates.append((new_x, new_y))
            else:
                update = False
                break

        # Update coordinates if all new positions are valid
        if update:
            self.coordinates = new_coordinates

    def changeDirection(self, new_direction: str) -> None:
        """
        Change the direction of the ship
        """
        x, y = self.coordinates[0]
        new_coordinates = []
        update = True

        for i in range(self.length):
            if new_direction == "VERTICAL":
                new_x, new_y = x, y - i
            elif new_direction == "HORIZONTAL":
                new_x, new_y = x + i, y

            if 0 <= new_x <= 9 and 0 <= new_y <= 9:
                new_coordinates.append((new_x, new_y))
            else:
                update = False
                break

        if update:
            self.direction = new_direction
            self.coordinates = new_coordinates

    def isValidDirection(self, direction: str):
        """
        Check if the ship can be placed in the given direction
        """
        x = self.coordinates[0][0]
        y = self.coordinates[0][1]

        if direction == "VERTICAL":
            return y - self.length+1 >= 0
        elif direction == "HORIZONTAL":
            return x + self.length-1 < 10

