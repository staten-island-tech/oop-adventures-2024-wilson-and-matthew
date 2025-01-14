import pygame
import random
import math


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Merchant:
    def __init__(self):
        self.x = -TILE_SIZE
        self.y = -TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (0, 0, 255)

    def spawn(self, dungeon):
        if random.random() < 0.2:
            while True:
                x = random.randint(1, dungeon.width - 1) * TILE_SIZE
                y = random.randint(1, dungeon.height - 1) * TILE_SIZE
                grid_x = x // TILE_SIZE
                grid_y = y // TILE_SIZE
                if dungeon.grid[grid_y][grid_x] == 0:
                    self.x = x
                    self.y = y
                    break

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def distance_to_player(self, player):
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)