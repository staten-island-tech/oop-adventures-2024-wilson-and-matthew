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
        self.scaling_factor = 5
        self.hp = self.base_hp
        self.projectiles = [] 
        self.last_shot_time = time.time()
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.last_direction_change_time = time.time()
        self.direction_change_interval = random.uniform(1, 3)
        self.speed = 5
        self.shoot_speed = 0.5
        self.half_hp_reduced = False
        self.half_hp = self.hp

    def update_shoot_speed(self):
        if not self.half_hp_reduced and self.hp <= self.half_hp / 2:
            self.shoot_speed = 0.25
            self.half_hp_reduced = True

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

    def shoot(self, player):
        self.update_shoot_speed()
        current_time = time.time()
        if current_time - self.last_shot_time > self.shoot_speed:
            if random.random() < 0.2:
                self.shoot_octagon()
            else:
                self.shoot_toward_player(player)
            self.last_shot_time = current_time

    def shoot_toward_player(self, player):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        direction_x /= distance
        direction_y /= distance
        projectile = Projectile(
            self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y
        )
        self.projectiles.append(projectile)

    def shoot_octagon(self):
        angles = [i * math.pi / 4 for i in range(8)]
        for angle in angles:
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)
            projectile = Projectile(
                self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y
            )
            self.projectiles.append(projectile)

    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.collides_with(player):
                player.hp -= 5
                self.projectiles.remove(projectile)
    
    def move_randomly(self, dungeon):
        current_time = time.time()

        if current_time - self.last_direction_change_time > self.direction_change_interval:
            self.direction = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
            if self.direction == [0, 0]:
                self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
            self.last_direction_change_time = current_time
            self.direction_change_interval = random.uniform(1, 3)
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        if not (0 <= new_x <= SCREEN_WIDTH - self.width):
            self.direction[0] *= -1
        else:
            grid_x = new_x // TILE_SIZE
            if dungeon.grid[self.y // TILE_SIZE][grid_x] == 0:
                self.x = new_x
            else:
                self.direction[0] *= -1

        if not (0 <= new_y <= SCREEN_HEIGHT - self.height):
            self.direction[1] *= -1
        else:
            grid_y = new_y // TILE_SIZE
            if dungeon.grid[grid_y][self.x // TILE_SIZE] == 0:
                self.y = new_y
            else:
                self.direction[1] *= -1

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
        self.half_hp = self.hp