import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()
        self.original_grid = [row[:] for row in self.grid]

    def generate_maze(self):
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        def dfs(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < self.width and 0 < ny < self.height and grid[ny][nx] == 1:
                    grid[ny][nx] = 0
                    grid[y + dy][x + dx] = 0
                    dfs(nx, ny)

        start_x, start_y = 1, 1
        grid[start_y][start_x] = 0
        dfs(start_x, start_y)
        return grid

    def clear_walls(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0

    def restore_walls(self):
        self.grid = [row[:] for row in self.original_grid]

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                color = WHITE if self.grid[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))