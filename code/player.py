import pygame
import math
import time
from bullet import Bullet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)
TILE_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = GREEN  # Set player color to green
        self.hp = 100  # Player's health points
        self.pistol = None  # Pistol will be assigned later when the fight starts
        self.bullets = []  # List of bullets the player shoots
        self.last_shot_time = time.time()  # Track the last time the player shot a bullet
        self.fire_rate = 0.5
        self.bullet_damage = 5

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw all bullets
        for bullet in self.bullets:
            bullet.draw()

    def move(self, dx, dy, dungeon, monsters):
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Ensure the player doesn't move out of bounds
        if new_x < 0 or new_x + self.width > SCREEN_WIDTH or new_y < 0 or new_y + self.height > SCREEN_HEIGHT:
            return  # Don't move if out of bounds

        # Check if the new position is within bounds and not a wall
        if self.can_move(new_x, new_y, dungeon, monsters):
            self.x = new_x
            self.y = new_y

    def can_move(self, new_x, new_y, dungeon, monsters):
        # Calculate the grid coordinates for the new position
        top_left_x = new_x // TILE_SIZE
        top_left_y = new_y // TILE_SIZE
        bottom_right_x = (new_x + self.width - 1) // TILE_SIZE
        bottom_right_y = (new_y + self.height - 1) // TILE_SIZE

        # Ensure the indices are within the bounds of the grid
        if not (0 <= top_left_x < dungeon.width and 0 <= top_left_y < dungeon.height and
                0 <= bottom_right_x < dungeon.width and 0 <= bottom_right_y < dungeon.height):
            return False

        # Check all four corners of the player's new position
        if dungeon.grid[top_left_y][top_left_x] == 1 or \
           dungeon.grid[top_left_y][bottom_right_x] == 1 or \
           dungeon.grid[bottom_right_y][top_left_x] == 1 or \
           dungeon.grid[bottom_right_y][bottom_right_x] == 1:
            return False  # One of the corners is a wall, so the move is not allowed

        # Check if the new position collides with any monsters
        for monster in monsters:
            monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
            player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            if player_rect.colliderect(monster_rect):
                return False  # Collided with the monster, can't move

        return True

    def shoot(self):
        current_time = time.time()
        if self.pistol and current_time - self.last_shot_time >= self.fire_rate:  # Check cooldown
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
            direction_x = mouse_x - (self.x + self.width // 2)  # Direction to mouse
            direction_y = mouse_y - (self.y + self.height // 2)

            # Normalize the direction
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y)
            bullet.damage = self.bullet_damage
            self.bullets.append(bullet)

            # Update last shot time
            self.last_shot_time = current_time

    def update_bullets(self, monster):
        # Update bullet positions and check for collisions with the monster
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.collides_with(monster):
                self.bullets.remove(bullet)  # Remove the bullet on collision