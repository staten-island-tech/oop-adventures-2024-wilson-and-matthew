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
    def is_dead(self):
        return self.hp <= 0

    def remove_from_game(self, dungeon):
        # Reset the monster's position to be out of the player's path
        self.x = -TILE_SIZE  # Move the monster off-screen
        self.y = -TILE_SIZE
        # Optionally, remove any projectiles as well
        self.projectiles.clear()
        self.hp = 0  # Set the HP to 0 to signify it is dead
        # Restore the dungeon grid (no monster blocking path)
        dungeon.grid[self.y // TILE_SIZE][self.x // TILE_SIZE] = 0  # Make sure the monster's position is clear

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

# Main function to run the game
def run_game():
    dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
    player = Player(100, 100)
    monster = Monster(-TILE_SIZE, -TILE_SIZE)  # Initially position the monster off-screen
    monster.spawn(dungeon)
    monsters = [monster]

    # Main game loop
    running = True
    while running:
        screen.fill(BLACK)
        dungeon.draw()
        player.draw()

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-PLAYER_SPEED, 0, dungeon, monsters)
                elif event.key == pygame.K_RIGHT:
                    player.move(PLAYER_SPEED, 0, dungeon, monsters)
                elif event.key == pygame.K_UP:
                    player.move(0, -PLAYER_SPEED, dungeon, monsters)
                elif event.key == pygame.K_DOWN:
                    player.move(0, PLAYER_SPEED, dungeon, monsters)
                elif event.key == pygame.K_SPACE:
                    player.shoot()

        # Check if the player is close enough to fight the monster
        distance_to_monster = monster.distance_to_player(player)
        if distance_to_monster < PROXIMITY_RANGE:
            # Show the 'Fight' message
            font = pygame.font.SysFont(None, 36)
            fight_text = font.render('Press "F" to Fight', True, WHITE)
            screen.blit(fight_text, (SCREEN_WIDTH // 2 - fight_text.get_width() // 2, SCREEN_HEIGHT // 2))
            if pygame.key.get_pressed()[pygame.K_f]:  # Fight action
                # Trigger the fight
                # Reset dungeon walls
                dungeon.restore_walls()
                monster.hp = 100  # Reset monster HP for the fight

        # Update bullets and check if any hit the monster
        player.update_bullets(monster)

        # Update and shoot projectiles from the monster
        monster.shoot(player)
        monster.update_projectiles(player)

        # Check if the monster is dead
        if monster.is_dead():
            monster.remove_from_game(dungeon)
            monster.spawn(dungeon)  # Respawn a new monster

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_game()
