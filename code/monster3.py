import pygame
import random
import math
import time
from projectile import Projectile

YELLOW = (255, 255, 0)
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Monster3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = YELLOW
        self.base_hp = 100
        self.scaling_factor = 5
        self.hp = self.base_hp
        self.projectiles = []
        self.last_shot_time = time.time()
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.last_direction_change_time = time.time()
        self.direction_change_interval = random.uniform(1, 3)
        self.speed = 5
        self.shoot_speed = 1
        self.half_hp_reduced = False
        self.half_hp = self.hp

    def phrase_2(self):
        if not self.half_hp_reduced and self.hp <= self.half_hp / 2:
            self.half_hp_reduced = True

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

    def shoot(self, player):
        self.phrase_2()
        current_time = time.time()
        if current_time - self.last_shot_time > self.shoot_speed:
            if random.random() < 0.5:
                self.shoot_laser(player)
            else:
                self.shoot_bones(player)
            self.last_shot_time = current_time

    def shoot_laser(self, player):
        target_x = player.x + player.width // 2
        target_y = player.y + player.height // 2

        for _ in range(3):
            spawn_side = random.choice(["top", "bottom", "left", "right"])
            if spawn_side == "top":
                start_x = random.randint(0, SCREEN_WIDTH)
                start_y = -50
                if start_x in range(player.x, player.x + player.width):
                    start_x = random.randint(0, SCREEN_WIDTH)
            elif spawn_side == "bottom":
                start_x = random.randint(0, SCREEN_WIDTH)
                start_y = SCREEN_HEIGHT + 50
                if start_x in range(player.x, player.x + player.width):
                    start_x = random.randint(0, SCREEN_WIDTH)
            elif spawn_side == "left":
                start_x = -50
                start_y = random.randint(0, SCREEN_HEIGHT)
                if start_y in range(player.y, player.y + player.height):
                    start_y = random.randint(0, SCREEN_HEIGHT)
            else:
                start_x = SCREEN_WIDTH + 50
                start_y = random.randint(0, SCREEN_HEIGHT)
                if start_y in range(player.y, player.y + player.height):
                    start_y = random.randint(0, SCREEN_HEIGHT)

            laser = LaserProjectile(start_x, start_y, target_x, target_y)
            self.projectiles.append(laser)

    def shoot_bones(self, player):
        if self.half_hp_reduced:
            angles = [random.uniform(-math.pi, math.pi) for _ in range(50)]
        else:
            angles = [random.uniform(-math.pi, math.pi) for _ in range(25)]
            
        for angle in angles:
                direction_x = math.cos(angle)
                direction_y = math.sin(angle)
                bone = Projectile(
                    self.x + self.width // 2, self.y + self.height // 2,
                    direction_x, direction_y
                )
                bone.color = YELLOW
                self.projectiles.append(bone)

    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            if isinstance(projectile, LaserProjectile):
                result = projectile.update()
            else:
                result = projectile.update()

            if result == "remove":
                self.projectiles.remove(projectile)
            elif projectile.collides_with(player):
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
        
class LaserProjectile(Projectile):
    def __init__(self, start_x, start_y, target_x, target_y, horizontal=False, vertical=False):
        dx = target_x - start_x
        dy = target_y - start_y
        self.angle = math.atan2(dy, dx)
        self.lifespan = 15
        self.start_time = time.time()
        self.speed = 10
        self.x = start_x
        self.y = start_y
        self.color = YELLOW
        self.distance = math.sqrt(dx**2 + dy**2)
        self.width = random.randint(10, 30) if horizontal else random.randint(10, 50)
        self.height = 500 if vertical else 10

    def draw(self):
        pygame.draw.line(
            screen, 
            self.color, 
            (self.x, self.y), 
            (self.x + math.cos(self.angle) * self.distance, self.y + math.sin(self.angle) * self.distance), 
            self.width)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time > self.lifespan:
            return "remove"
        return "keep"
    
    def collides_with(self, player):
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if projectile_rect.colliderect(player_rect):
            return True
        return False
    
    def collides_with_bullet(self, bullets):
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if bullet_rect.colliderect(projectile_rect):
                bullets.remove(bullet)
                return True
        return False