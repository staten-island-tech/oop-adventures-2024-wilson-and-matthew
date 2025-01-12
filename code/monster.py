import pygame
import random
import math
import time
from projectile import Projectile

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED = (255, 0, 0)
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = RED
        self.base_hp = 100
        self.scaling_factor = 10
        self.hp = self.base_hp
        self.projectiles = [] 
        self.last_shot_time = time.time()

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

    def shoot(self, player):
        current_time = time.time()
        if current_time - self.last_shot_time > 0.5:
            direction_x = player.x - self.x
            direction_y = player.y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            direction_x /= distance
            direction_y /= distance
            projectile = Projectile(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y)
            self.projectiles.append(projectile)
            self.last_shot_time = current_time

    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.collides_with(player):
                player.hp -= 5
                self.projectiles.remove(projectile)

    def distance_to_player(self, player):
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

    def spawn(self, dungeon):
        while True:
            x = random.randint(1, dungeon.width - 1) * TILE_SIZE
            y = random.randint(1, dungeon.height - 1) * TILE_SIZE
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            if dungeon.grid[grid_y][grid_x] == 0:
                self.x = x
                self.y = y
                break

    def remove_from_game(self, dungeon):
        self.x = -TILE_SIZE
        self.y = -TILE_SIZE
        self.projectiles.clear()
        self.hp = 0
        dungeon.grid[self.y // TILE_SIZE][self.x // TILE_SIZE] = 0

    def update_hp(self, score):
        self.hp = self.base_hp + score * self.scaling_factor