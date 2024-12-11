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
FPS = 60

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

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep player within the dungeon bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

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

# Main game loop
def main():
    running = True
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    dungeon = generate_dungeon()

    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player movement
        player.update(keys)

        # Draw dungeon and player
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = TILE_SIZE // 2

    def update(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.rect.y -= self.speed
        elif direction == 'down':
            self.rect.y += self.speed
        elif direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed

        # Keep enemy within bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - TILE_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - TILE_SIZE))

# Add enemies to the game
def add_enemies(all_sprites):
    for _ in range(5):  # Create 5 enemies
        x = random.randint(0, DUNGEON_WIDTH - 1) * TILE_SIZE
        y = random.randint(0, DUNGEON_HEIGHT - 1) * TILE_SIZE
        enemy = Enemy(x, y)
        all_sprites.add(enemy)

# Modify the main function to add enemies
def main():
    running = True
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    add_enemies(all_sprites)

    dungeon = generate_dungeon()

    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player and enemy movement
        player.update(keys)
        all_sprites.update()

        # Draw dungeon and all sprites
        draw_dungeon(dungeon)
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(FPS)

    pygame.quit()
