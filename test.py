class Merchant:
    def __init__(self):
        self.x = -TILE_SIZE  # Initial off-screen position
        self.y = -TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (0, 0, 255)  # Blue color for the merchant

    def spawn(self, dungeon):
        # 20% chance to spawn on a valid white square (path)
        if random.random() < 0.2:  # 20% chance
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

    def reset_game(self):
        # Reset the dungeon, player, monster, and other game states
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1])  # Reset player to the initial spawn position
        self.exit = (SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE)  # Reset exit
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

    def toggle_merchant_menu(self):
        # Toggle the merchant menu state
        self.merchant_menu_active = not self.merchant_menu_active

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
            dist_monster = self.monster.distance_to_player(self.player)
            if dist_monster <= PROXIMITY_RANGE:
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

        # Display the "Press Space to Fight" or "Press Space to Open Merchant Menu" message
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
        menu_text = self.font.render("Welcome to the Merchant! (Press Space to Exit)", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # You can add items to buy here (just a placeholder for now)
        item_text = self.font.render("1. Buy Health Potion - 10 Gold", True, WHITE)
        screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)  # Maintain the frame rate

        pygame.quit()

# Initialize the game
game = Game()
game.run()
