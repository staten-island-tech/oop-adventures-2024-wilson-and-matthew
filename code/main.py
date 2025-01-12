import pygame
from dungeon import Dungeon
from player import Player
from monster import Monster
from merchant import Merchant

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TILE_SIZE = 40
PLAYER_SPEED = 5
PROXIMITY_RANGE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Game")
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
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
        self.previous_monster_position = None
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
                    if self.proximity_message == "Press Space to Interact":
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
            self.teleport_monster_back()
            self.teleport_merchant_back()  # Teleport merchant back to their original position
            self.dungeon.restore_walls()  # Restore dungeon walls when leaving the merchant menu
            self.merchant_menu_active = False  # Deactivate the merchant menu
        else:
            self.clear_walls_for_merchant_interaction()
            self.merchant_menu_active = True  # Activate the merchant menu

    def clear_walls_for_merchant_interaction(self):
        # Clear all walls in the dungeon and move the player to a special position near the merchant
        self.dungeon.clear_walls()
        self.previous_monster_position = (self.monster.x, self.monster.y)
        self.previous_player_position = (self.player.x, self.player.y)  # Save the player's current position
        self.monster.x = -TILE_SIZE
        self.monster.y = -TILE_SIZE
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Center player
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10  # Place player near the top middle of the screen
        self.merchant.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2  # Place merchant near the top center of the screen
        self.merchant.y = SCREEN_HEIGHT // 4 - TILE_SIZE // 2  # Position the merchant near the center
        self.proximity_message = ""  # Clear the proximity message as the player is at the merchant
    def teleport_monster_back(self):
        self.monster.x, self.monster.y = self.previous_monster_position
        self.previous_monster_position = None
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
        self.merchant.x = -TILE_SIZE
        self.merchant.y = -TILE_SIZE
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
        self.player.x, self.player.y = self.starting_position

        # End the fight and reset state
        self.fight_started = False
        self.proximity_message = ""  # Clear any messages

    def update(self):
        if self.player.hp <= 0:  # Check if the player's HP is 0 or less
            self.reset_game()  # Reset the game state
            return  # Stop updating the rest of the game logic
        if self.monster.hp <= 0:
            self.monster.remove_from_game(self.dungeon)
            self.player.bullets.clear()
            self.dungeon.restore_walls()  # Restore dungeon walls
            self.end_boss_fight()  # End the boss fight and return to the starting position
            self.score += 10  # Increase score when the player defeats a monster
            self.monster.update_hp(self.score)
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
                self.proximity_message = "Press Space to Interact"

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
            text = self.font.render(self.proximity_message, True, GREEN)
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
        item_text = self.font.render("Check Terminal", True, BLACK)
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