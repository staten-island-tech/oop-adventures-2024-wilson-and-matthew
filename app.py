import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
DUNGEON_WIDTH = SCREEN_WIDTH // TILE_SIZE
DUNGEON_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
FPS = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Game")

# Set up the clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = DUNGEON_WIDTH // 2 * TILE_SIZE
        self.rect.y = DUNGEON_HEIGHT // 2 * TILE_SIZE
        self.speed = TILE_SIZE
        self.can_move = True  # Flag to ensure only one move per key press

    def update(self, keys, dungeon):
        if self.can_move:
            new_x = self.rect.x
            new_y = self.rect.y

            # Check for movement based on key presses
            if keys[pygame.K_LEFT]:
                new_x -= self.speed
            if keys[pygame.K_RIGHT]:
                new_x += self.speed
            if keys[pygame.K_UP]:
                new_y -= self.speed
            if keys[pygame.K_DOWN]:
                new_y += self.speed

            # Ensure the player moves only to white tiles (valid empty spaces)
            if 0 <= new_x // TILE_SIZE < DUNGEON_WIDTH and 0 <= new_y // TILE_SIZE < DUNGEON_HEIGHT:
                if dungeon[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0:  # Check if it's a white space (empty)
                    self.rect.x = new_x
                    self.rect.y = new_y
                    self.can_move = False  # Prevent movement until the next update

        # Keep player within dungeon bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

    def reset_move(self):
        # Allow player to move again after 1 update cycle
        self.can_move = True

# Dungeon generation function (simple random maze)
def generate_dungeon():
    dungeon = [[random.choice([0, 1]) for _ in range(DUNGEON_WIDTH)] for _ in range(DUNGEON_HEIGHT)]
    # Ensure the starting area is empty
    dungeon[DUNGEON_HEIGHT // 2][DUNGEON_WIDTH // 2] = 0
    return dungeon

# Dungeon drawing function
def draw_dungeon(dungeon):
    for y in range(DUNGEON_HEIGHT):
        for x in range(DUNGEON_WIDTH):
            color = WHITE if dungeon[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = TILE_SIZE // 2

    def update(self, dungeon):
        direction = random.choice(['up', 'down', 'left', 'right'])
        new_x = self.rect.x
        new_y = self.rect.y

        if direction == 'up':
            new_y -= self.speed
        elif direction == 'down':
            new_y += self.speed
        elif direction == 'left':
            new_x -= self.speed
        elif direction == 'right':
            new_x += self.speed

        # Ensure the enemy stays within bounds and only moves to valid spaces
        if 0 <= new_x // TILE_SIZE < DUNGEON_WIDTH and 0 <= new_y // TILE_SIZE < DUNGEON_HEIGHT:
            if dungeon[new_y // TILE_SIZE][new_x // TILE_SIZE] == 0:  # Check if it's a white space (empty)
                self.rect.x = new_x
                self.rect.y = new_y

        # Keep enemy within bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

# Add enemies to the game
def add_enemies(all_sprites, dungeon):
    for _ in range(5):  # Create 5 enemies
        x = random.randint(0, DUNGEON_WIDTH - 1) * TILE_SIZE
        y = random.randint(0, DUNGEON_HEIGHT - 1) * TILE_SIZE
        # Ensure the enemy spawns on a white tile
        while dungeon[y // TILE_SIZE][x // TILE_SIZE] != 0:
            x = random.randint(0, DUNGEON_WIDTH - 1) * TILE_SIZE
            y = random.randint(0, DUNGEON_HEIGHT - 1) * TILE_SIZE
        enemy = Enemy(x, y)
        all_sprites.add(enemy)

# Main game loop
def main():
    running = True
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    dungeon = generate_dungeon()
    add_enemies(all_sprites, dungeon)

    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player movement (pass dungeon for validation)
        player.update(keys, dungeon)

        # Update all enemy movement (pass dungeon for validation)
        for enemy in all_sprites:
            if isinstance(enemy, Enemy):
                enemy.update(dungeon)

        # Reset player's ability to move after one update cycle
        player.reset_move()

        # Draw dungeon and all sprites
        draw_dungeon(dungeon)
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()