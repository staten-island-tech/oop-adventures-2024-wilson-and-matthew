import pygame
import random
import math
import time
from projectile import Projectile
from monster import Monster

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Monster2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = PURPLE
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
            if random.random() < 0.2:
                self.four_direction()
            elif self.half_hp_reduced is True and random.random() < 0.2:
                self.shoot_orbiting_projectiles()
            else:
                self.shoot_homing(player)
            self.last_shot_time = current_time

    def shoot_homing(self, player):
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)
        direction_x /= distance
        direction_y /= distance
        projectile = HomingProjectile(
            self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y
        )
        self.projectiles.append(projectile)

    def four_direction(self):
        angles = [i * math.pi / 2 for i in range(4)]
        for angle in angles:
            direction_x = math.cos(angle)
            direction_y = math.sin(angle)
            projectile = HomingProjectile(
                self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y
            )
            self.projectiles.append(projectile)

    def shoot_orbiting_projectiles(self):
        left_offset = -self.width // 2 - 20
        top_offset = -self.height // 2 - 20
        right_offset = self.width // 2 + 20
        bottom_offset = self.height // 2 + 20
        projectile_left = OrbitingProjectile(self.x + left_offset, self.y, -1, 0, self, angle_offset=math.pi / 2)
        self.projectiles.append(projectile_left)
        projectile_top = OrbitingProjectile(self.x, self.y + top_offset, 0, -1, self, angle_offset=0)
        self.projectiles.append(projectile_top)
        projectile_right = OrbitingProjectile(self.x + right_offset, self.y, 1, 0, self, angle_offset=-math.pi / 2)
        self.projectiles.append(projectile_right)
        projectile_bottom = OrbitingProjectile(self.x, self.y + bottom_offset, 0, 1, self, angle_offset=math.pi)
        self.projectiles.append(projectile_bottom)
            
    def update_projectiles(self, player):
        for projectile in self.projectiles[:]:
            result = projectile.update(player)
            if result == "remove":
                self.projectiles.remove(projectile)
            elif projectile.collides_with(player):
                player.hp -= 5
                self.projectiles.remove(projectile)
            elif projectile.collides_with_bullet(player.bullets):
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

    def spawn_monster():
        if random.random() < 0.5:
            return Monster(0, 0)
        else:
            return Monster2(0, 0)
        
class HomingProjectile(Projectile):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__(x, y, direction_x, direction_y)
        self.color = PURPLE
        self.speed = 4
        self.width = 20
        self.height = 20
        self.start_time = time.time()
        self.lifespan = 10
        self.chase_delay = 1
        self.initial_direction_x = direction_x
        self.initial_direction_y = direction_y

    def update(self, player):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time > self.lifespan:
            return "remove"
        if elapsed_time > self.chase_delay:
            direction_x = player.x - self.x
            direction_y = player.y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            if distance != 0:
                self.direction_x = direction_x / distance
                self.direction_y = direction_y / distance
        else:
            self.direction_x = self.initial_direction_x
            self.direction_y = self.initial_direction_y
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        return "keep"

    def collides_with_bullet(self, bullets):
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if bullet_rect.colliderect(projectile_rect):
                bullets.remove(bullet)
                return True
        return False

class OrbitingProjectile(Projectile):
    def __init__(self, x, y, direction_x, direction_y, monster, angle_offset=0):
        super().__init__(x, y, direction_x, direction_y)
        self.color = PURPLE
        self.speed = 4
        self.width = 20
        self.height = 20
        self.start_time = time.time()
        self.lifespan = 30
        self.hp = 1
        self.monster = monster
        self.angle_offset = angle_offset

    def update(self, player):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time > self.lifespan:
            return "remove"
        angle = self.angle_offset + elapsed_time * 5
        orbit_radius = 50
        self.x = self.monster.x + self.monster.width // 2 + orbit_radius * math.cos(angle)
        self.y = self.monster.y + self.monster.height // 2 + orbit_radius * math.sin(angle)
        return "keep"

    def collides_with(self, player):
        return False

    def collides_with_bullet(self, bullets):
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if bullet_rect.colliderect(projectile_rect):
                bullets.remove(bullet)
                self.hp -= 1
                if self.hp <= 0:
                    return True
        return False