class Maincharacter:
    def __init__(self, name, inventory, money, hp, attack):
        self.name = name
        self.inventory = inventory
        self.money = money
        self.hp = hp
        self.attack = attack
        self.is_alive = True

    def buy(self, item, money):
        self.inventory.append(item)
        print(self.inventory)
        self.inventory.remove(money)
        
    def attack_enemy(self, enemy):
        damage = max(0, self.attack)  # Basic attack calculation
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def take_damage(self, eattack):
        self.health -= eattack
        print(f"{self.name} takes {eattack} damage!")
        if self.health <= 0:
            self.is_alive = False
            self.die()
            # print(f"{self.name} has been defeated!")

    def die(self):
        print(f"{self.name} has died! hahaha loser")
        self.lose_items()

    def lose_items(self):
        items_to_keep = [special]

        self.inventory = [item for item in self.inventory if item in items_to_keep]

        self.money = 0
        
        print(f"{self.name} has died and lost all their stuff hahahaha")
        print(f"Remaining items: {self.inventory}")
        print(f"Remaining money: {self.money}")





inventory = {

}

special = {

}



player_name = input("Enter your character's name: ")
player = Maincharacter(player_name, inventory=[], money=50, hp=100, attack=5, speed=5)
###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################
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
###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################
import pygame
import time
import math

TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)

class Player:
    def __init__(self, x, y, name, attack, rate, hp, speed, inventory=None, money=0):
        # Player Position and Size
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = GREEN
        
        # Stats
        self.name = name
        self.attack = attack  # Attack stat affects bullet damage
        self.hp = hp  # Health points
        self.rate = rate  # Rate affects how many bullets you can shoot per second
        self.speed = speed  # Speed affects bullet speed
        
        # Inventory and Money
        self.inventory = inventory if inventory else []
        self.money = money

        # Gameplay mechanics
        self.pistol = None  # Pistol will be assigned when the fight starts
        self.bullets = []  # List of bullets shot by the player
        self.last_shot_time = time.time()  # Time of last shot
        self.last_attack_time = time.time()  # Time of last attack

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.draw()

    def move(self, dx, dy, dungeon, monsters):
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Ensure player stays within bounds
        if new_x < 0 or new_x + self.width > SCREEN_WIDTH or new_y < 0 or new_y + self.height > SCREEN_HEIGHT:
            return
        
        # Check for walls and monsters
        if self.can_move(new_x, new_y, dungeon, monsters):
            self.x = new_x
            self.y = new_y

    def can_move(self, new_x, new_y, dungeon, monsters):
        # Same logic for grid and monster collision
        top_left_x = new_x // TILE_SIZE
        top_left_y = new_y // TILE_SIZE
        bottom_right_x = (new_x + self.width - 1) // TILE_SIZE
        bottom_right_y = (new_y + self.height - 1) // TILE_SIZE

        if not (0 <= top_left_x < dungeon.width and 0 <= top_left_y < dungeon.height and
                0 <= bottom_right_x < dungeon.width and 0 <= bottom_right_y < dungeon.height):
            return False

        if dungeon.grid[top_left_y][top_left_x] == 1 or \
           dungeon.grid[top_left_y][bottom_right_x] == 1 or \
           dungeon.grid[bottom_right_y][top_left_x] == 1 or \
           dungeon.grid[bottom_right_y][bottom_right_x] == 1:
            return False

        for monster in monsters:
            monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
            player_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            if player_rect.colliderect(monster_rect):
                return False  # Collided with monster

        return True

    def shoot(self):
        current_time = time.time()
        # Rate of fire check based on 'rate' stat
        if self.pistol and current_time - self.last_shot_time >= (1 / self.rate):  # Cooldown based on rate
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
            direction_x = mouse_x - (self.x + self.width // 2)  # Direction to mouse
            direction_y = mouse_y - (self.y + self.height // 2)

            # Normalize direction
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
            if distance != 0:
                direction_x /= distance
                direction_y /= distance

            # Create bullet with attack-based damage and player speed
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y, self.attack, self.speed)
            self.bullets.append(bullet)

            # Update last shot time
            self.last_shot_time = current_time

    def update_bullets(self, monsters):
        for bullet in self.bullets[:]:
            bullet.update()
            for monster in monsters:
                if bullet.collides_with(monster):
                    monster.hp -= bullet.damage  # Bullet deals damage based on its attack stat
                    self.bullets.remove(bullet)  # Remove the bullet on collision

    def buy(self, item, money):
        # Allow the player to buy items (using money)
        if self.money >= money:
            self.inventory.append(item)
            self.money -= money
            print(f"Purchased {item}. Current inventory: {self.inventory}")
        else:
            print("Not enough money.")

class Bullet:
    def __init__(self, x, y, direction_x, direction_y, attack, speed):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = GREEN  # Green bullet to match player
        self.speed = speed  # Bullet speed based on player stats
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.damage = attack  # Bullet damage based on player's attack stat

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collides_with(self, monster):
        monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
        bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return bullet_rect.colliderect(monster_rect)

# Sample Usage
player = Player(100, 100, "Player1", 20, 2, 100, 15)  # Player with attack 20, rate of 2 shots/sec, speed of 15
player.shoot()  # Shoots a bullet with damage based on the player's attack stat and speed based on the player's speed

# Now, the bullet's speed is affected by the player's speed stat
