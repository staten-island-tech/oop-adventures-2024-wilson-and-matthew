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

    def toggle_merchant_menu(self):
        # Toggle the merchant menu state
        if self.merchant_menu_active:
            self.teleport_player_back()
            self.dungeon.restore_walls()  # Restore dungeon walls when leaving the merchant menu
            self.monster.spawn(self.dungeon)  # Re-spawn the monster back to its position
            self.merchant.spawn(self.dungeon)  # Re-spawn the merchant after leaving the merchant menu
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
        self.monster.hp = 0  # Remove the monster from the game when in the merchant menu

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
        self.merchant.hp = 0  # Completely remove the merchant during boss fight

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
        self.merchant.hp = 100  # Restore merchant's health after the fight

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

        # Display the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.time.Clock().tick(60)  # Run the game at 60 FPS