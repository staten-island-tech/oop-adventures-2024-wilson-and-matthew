import pygame
import random
import math

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

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

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

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = RED  # Set monster color to red

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def distance_to_player(self, player):
        # Calculate distance from the monster to the player using Euclidean distance
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

class Game:
    def __init__(self):
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(1 * TILE_SIZE, 1 * TILE_SIZE)  # Start at (1, 1) for point A
        self.exit = (SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE)  # Exit at bottom-right corner
        self.monsters = [Monster(random.randint(1, SCREEN_WIDTH // TILE_SIZE - 1) * TILE_SIZE, 
                                 random.randint(1, SCREEN_HEIGHT // TILE_SIZE - 1) * TILE_SIZE)]
        self.running = True
        self.proximity_message = ""  # Message to show when near a monster

        # Font for text
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.proximity_message == "Press Space to Fight":
                    print("Fighting started!")  # Trigger the battle (placeholder)

    def update(self):
        keys = pygame.key.get_pressed()

        # Player movement handling with WASD keys
        if keys[pygame.K_a]:  # Move left
            self.player.move(-PLAYER_SPEED, 0, self.dungeon, self.monsters)
        if keys[pygame.K_d]:  # Move right
            self.player.move(PLAYER_SPEED, 0, self.dungeon, self.monsters)
        if keys[pygame.K_w]:  # Move up
            self.player.move(0, -PLAYER_SPEED, self.dungeon, self.monsters)
        if keys[pygame.K_s]:  # Move down
            self.player.move(0, PLAYER_SPEED, self.dungeon, self.monsters)

        # Check proximity to monsters
        self.proximity_message = ""
        for monster in self.monsters:
            if monster.distance_to_player(self.player) <= PROXIMITY_RANGE:
                self.proximity_message = "Press Space to Fight"
                break  # Display the message if near any monster

    def draw(self):
        # Fill the screen with black
        screen.fill(BLACK)

        # Draw dungeon, player, and monsters
        self.dungeon.draw()
        self.player.draw()

        # Draw exit (point B) as a yellow square
        pygame.draw.rect(screen, YELLOW, (self.exit[0], self.exit[1], TILE_SIZE, TILE_SIZE))

        for monster in self.monsters:
            monster.draw()

        # Display the "Press Space to Fight" message if proximity condition is met
        if self.proximity_message:
            text = self.font.render(self.proximity_message, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 50))

        # Update the display
        pygame.display.flip()

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
