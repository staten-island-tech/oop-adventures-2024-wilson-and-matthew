import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Player color (green)
RED = (255, 0, 0)    # Monster color (red)
YELLOW = (255, 255, 0)  # Exit color (yellow)

# Tile size
TILE_SIZE = 40

# Player movement speed
PLAYER_SPEED = 5

# Proximity range to trigger fight message
PROXIMITY_RANGE = 80  # The player must be within 80 pixels of the monster

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Clock to control game frame rate
clock = pygame.time.Clock()

# Define the classes
class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()
        self.original_grid = [row[:] for row in self.grid]  # Store the original grid

    def generate_maze(self):
        # Initialize the grid with walls (1's)
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Randomized depth-first search (DFS) algorithm for maze generation
        def dfs(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < self.width and 0 < ny < self.height and grid[ny][nx] == 1:
                    grid[ny][nx] = 0  # Carve path
                    grid[y + dy][x + dx] = 0  # Carve the wall between
                    dfs(nx, ny)

        # Start DFS from a random point (e.g., 1,1)
        start_x, start_y = 1, 1
        grid[start_y][start_x] = 0  # Make the start point a path
        dfs(start_x, start_y)

        return grid

    def clear_walls(self):
        # Change all walls (1's) to paths (0's) to create an empty arena
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0  # Remove walls

    def restore_walls(self):
        # Restore the dungeon walls to their original state
        self.grid = [row[:] for row in self.original_grid]

    def draw(self):
        # Draw the dungeon
        for y in range(self.height):
            for x in range(self.width):
                color = WHITE if self.grid[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

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
        if self.pistol and current_time - self.last_shot_time >= 0.5:  # Check cooldown
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
            direction_x = mouse_x - (self.x + self.width // 2)  # Direction to mouse
            direction_y = mouse_y - (self.y + self.height // 2)

            # Normalize the direction
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y)
            self.bullets.append(bullet)

            # Update last shot time
            self.last_shot_time = current_time

    def update_bullets(self, monster):
        # Update bullet positions and check for collisions with the monster
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.collides_with(monster):
                monster.hp -= 5  # Bullet does 5 damage to the monster
                self.bullets.remove(bullet)  # Remove the bullet on collision

class Bullet:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = GREEN  # Green bullet to match the player
        self.speed = 10  # Bullet speed
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, monster):
        monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
        bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return bullet_rect.colliderect(monster_rect)

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = RED  # Set monster color to red
        self.hp = 100  # Add HP for the monster
        self.projectiles = []
        self.last_shot_time = time.time()  # To manage projectile shooting interval

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()

    def shoot(self, player):
        # Fire a projectile every 0.5 seconds
        current_time = time.time()
        if current_time - self.last_shot_time > 0.5:  # Adjusted to 0.5 seconds
            # Calculate the direction from the monster to the player
            direction_x = player.x - self.x
            direction_y = player.y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            # Normalize the direction
            direction_x /= distance
            direction_y /= distance
            # Create a new projectile
            projectile = Projectile(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y)
            self.projectiles.append(projectile)
            self.last_shot_time = current_time

    def update_projectiles(self, player):
        # Move projectiles and check for collisions with the player
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.collides_with(player):
                player.hp -= 5  # Decrease player HP by 5 when hit
                self.projectiles.remove(projectile)  # Remove the projectile upon collision

    def distance_to_player(self, player):
        # Calculate the distance from the monster to the player using Euclidean distance
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

    def spawn(self, dungeon):
        # Spawn the monster only on a valid white tile (path)
        while True:
            x = random.randint(1, dungeon.width - 1) * TILE_SIZE
            y = random.randint(1, dungeon.height - 1) * TILE_SIZE
            grid_x = x // TILE_SIZE
            grid_y = y // TILE_SIZE
            if dungeon.grid[grid_y][grid_x] == 0:  # 0 represents a path
                self.x = x
                self.y = y
                break

    def remove_from_game(self, dungeon):
        # Reset the monster's position to be out of the player's path
        self.x = -TILE_SIZE  # Move the monster off-screen
        self.y = -TILE_SIZE
        # Optionally, remove any projectiles as well
        self.projectiles.clear()
        self.hp = 0  # Set the HP to 0 to signify it is dead
        # Restore the dungeon grid (no monster blocking path)
        dungeon.grid[self.y // TILE_SIZE][self.x // TILE_SIZE] = 0  # Make sure the monster's position is clear
class Merchant:
    def __init__(self):
        self.x = -TILE_SIZE  # Initial off-screen position
        self.y = -TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (0, 0, 255)  # Blue color for the merchant

    def spawn(self, dungeon):
        # 20% chance to spawn on a valid white square (path)
        if random.random() < 0.2:
            while True:
                x = random.randint(1, dungeon.width - 1) * TILE_SIZE
                y = random.randint(1, dungeon.height - 1) * TILE_SIZE
                grid_x = x // TILE_SIZE
                grid_y = y // TILE_SIZE
                if dungeon.grid[grid_y][grid_x] == 0:  # 0 represents a path
                    self.x = x
                    self.y = y
                    break

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def distance_to_player(self, player):
        # Calculate the distance from the merchant to the player using Euclidean distance
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
class Projectile:
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = RED  # Red projectile to match the enemy's color
        self.speed = 3
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, player):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        projectile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(projectile_rect)

# Replace this part of your Game class to fix the bug:

class Game:
    def __init__(self):
        # Track initial spawn position
        self.initial_spawn_position = (1 * TILE_SIZE, 1 * TILE_SIZE)  # Initial spawn position
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1])  # Set to initial spawn position
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  # Spawn merchant with 20% chance
        self.fight_started = False
        self.proximity_message = ""  # Message to show when near a monster or merchant
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.score = 0  # Initialize the score
        self.merchant_menu_active = False  # To track if the merchant menu is active
        self.previous_player_position = None  # Store the player's position when they interact with the merchant
        self.merchant_original_position = (self.merchant.x, self.merchant.y)

    def reset_game(self):
        # Reset the dungeon, player, monster, and other game states
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1])  # Reset player to the initial spawn position
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)  # Spawn monster at a new location
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  # Spawn merchant at a new location
        self.fight_started = False
        self.proximity_message = ""  # Reset message
        self.score = 0  # Reset score to 0 when the game is reset

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # If near the merchant, open the merchant menu
                    if self.proximity_message == "Press Space to Open Merchant Menu":
                        self.toggle_merchant_menu()

                    # If the fight message is showing and space is pressed, start the fight
                    elif self.proximity_message == "Press Space to Fight":
                        self.start_boss_fight()
    def teleport_merchant_back(self):
        # Teleport the merchant back to their original position
        self.merchant.x, self.merchant.y = self.merchant_original_position
    def toggle_merchant_menu(self):
        # Toggle the merchant menu state
        if self.merchant_menu_active:
            self.teleport_player_back()
            self.teleport_merchant_back()  # Teleport merchant back to their original position
            self.dungeon.restore_walls()  # Restore dungeon walls when leaving the merchant menu
            self.merchant_menu_active = False  # Deactivate the merchant menu
        else:
            self.clear_walls_for_merchant_interaction()
            self.merchant_menu_active = True  # Activate the merchant menu

    def clear_walls_for_merchant_interaction(self):
        # Clear all walls in the dungeon and move the player to a special position near the merchant
        self.dungeon.clear_walls()
        self.previous_player_position = (self.player.x, self.player.y)  # Save the player's current position
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Center player
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10  # Place player near the top middle of the screen
        self.merchant.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Place merchant near the top center of the screen
        self.merchant.y = SCREEN_HEIGHT // 4 - TILE_SIZE // 2  # Position the merchant near the center
        self.proximity_message = ""  # Clear the proximity message as the player is at the merchant

    def teleport_player_back(self):
        # Teleport the player back to their previous position before interacting with the merchant
        self.player.x, self.player.y = self.previous_player_position
        self.previous_player_position = None  # Clear the stored position

    def start_boss_fight(self):
        # Store the player's position before starting the fight
        self.starting_position = (self.player.x, self.player.y)
        
        # Clear all walls to create an empty arena
        self.dungeon.clear_walls()
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Center player
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10
        self.monster.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Center monster
        self.monster.y = SCREEN_HEIGHT // 2 - TILE_SIZE // 2  # Center monster
        self.fight_started = True
        self.player.pistol = True  # Equip player with a pistol

    def end_boss_fight(self):
        # Restore dungeon grid and reinitialize the game state
        self.dungeon.restore_walls()
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  # Spawn merchant at a new location
        # Move monster out of the screen and reset its state
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)  # Spawn monster at a new location

        # Reset score after player death
        self.player.x, self.player.y = self.starting_position

        # End the fight and reset state
        self.fight_started = False
        self.proximity_message = ""  # Clear any messages

    def update(self):
        if self.player.hp <= 0:  # Check if the player's HP is 0 or less
            self.reset_game()  # Reset the game state
            return  # Stop updating the rest of the game logic

        # Check if the monster is dead
        if self.monster.hp <= 0:
            self.monster.remove_from_game(self.dungeon)
            self.dungeon.restore_walls()  # Restore dungeon walls
            self.end_boss_fight()  # End the boss fight and return to the starting position
            self.score += 10  # Increase score when the player defeats a monster
            return  # Stop further updates for the monster

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            self.player.move(-PLAYER_SPEED, 0, self.dungeon, [self.monster])
        if keys[pygame.K_d]:  # Move right
            self.player.move(PLAYER_SPEED, 0, self.dungeon, [self.monster])
        if keys[pygame.K_w]:  # Move up
            self.player.move(0, -PLAYER_SPEED, self.dungeon, [self.monster])
        if keys[pygame.K_s]:  # Move down
            self.player.move(0, PLAYER_SPEED, self.dungeon, [self.monster])

        # Handle shooting when space key is pressed
        if self.fight_started and pygame.mouse.get_pressed()[0]:  # Left mouse button
            self.player.shoot()

        # Check proximity to monsters and merchant
        self.proximity_message = ""
        if not self.fight_started:
            dist = self.monster.distance_to_player(self.player)
            if dist <= PROXIMITY_RANGE:
                self.proximity_message = "Press Space to Fight"

            dist_merchant = self.merchant.distance_to_player(self.player)
            if dist_merchant <= PROXIMITY_RANGE:
                self.proximity_message = "Press Space to Open Merchant Menu"

        # Boss fight logic
        if self.fight_started:
            self.monster.shoot(self.player)
            self.monster.update_projectiles(self.player)
            self.player.update_bullets(self.monster)

    def draw(self):
        # Fill the screen with black
        screen.fill(BLACK)

        # Draw dungeon, player, and monsters
        self.dungeon.draw()
        self.player.draw()

        # Draw monster
        self.monster.draw()

        # Draw merchant
        self.merchant.draw()

        # Display the "Press Space to Fight" message if proximity condition is met
        if self.proximity_message:
            text = self.font.render(self.proximity_message, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 50))

        # Display player's HP
        hp_text = self.font.render(f"HP: {self.player.hp}", True, GREEN)
        screen.blit(hp_text, (10, 10))

        # Display monster's HP if fight has started
        if self.fight_started:
            monster_hp_text = self.font.render(f"HP: {self.monster.hp}", True, RED)
            screen.blit(monster_hp_text, (SCREEN_WIDTH - 100, 10))  # Display monster's HP at the top-right

        # Display score in yellow text at the top middle of the screen
        score_text = self.font.render(f"Score: {self.score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

        # If merchant menu is active, show the menu
        if self.merchant_menu_active:
            self.draw_merchant_menu()

        # Update the display
        pygame.display.flip()

    def draw_merchant_menu(self):
        # Draw a simple merchant menu (for now, just a placeholder)
        menu_text = self.font.render("Welcome to the Merchant! (Press Space to Exit)", True, BLACK)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # You can add items to buy here (just a placeholder for now)
        item_text = self.font.render("1. Buy Health Potion - 10 Gold", True, BLACK)
        screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

# Create the game object
game = Game()

# Start the game loop
game.run()

# Quit Pygame
pygame.quit()