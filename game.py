import random

class Enemy:
    def __init__(self, ename, ehp, eattack, espeed):
        self.name = ename
        self.ehp = ehp
        self.eattack = eattack
        self.espeed = espeed
        self.is_alive = True

    def attack(self, player):
        if self.is_alive:
            damage = self.eattack
            print(f"{self.name} attacks {player.name} for {damage} damage!")
            player.take_damage(damage)

    def take_damage(self, damage):
        self.ehp -= damage
        if self.ehp <= 0:
            self.is_alive = False
            print(f"{self.name} has been defeated!")

class ShopDude:
    def __init__(self, name, stock, prices):
        self.name = name
        self.stock = stock
        self.prices = prices  # Dictionary of item prices

    def sell(self, item, player):
        if item in self.stock:
            price = self.prices[item]
            if player.money >= price:
                player.inventory.append(item)
                player.money -= price
                print(f"{player.name} bought a {item} for {price}. Remaining money: {player.money}")
            else:
                print(f"Not enough money to buy {item}.")
        else:
            print(f"{item} is not in stock!")

class MainCharacter:
    def __init__(self, name, inventory, money, hp, attack, speed):
        self.name = name
        self.inventory = inventory
        self.money = money
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.defense = 0  # Start with no defense
        self.is_alive = True

    def buy(self, item, shop):
        shop.sell(item, self)

    def take_damage(self, eattack):
        # Reduce damage based on defense
        damage_taken = max(0, eattack - self.defense)  # Damage cannot be negative
        self.hp -= damage_taken
        print(f"{self.name} takes {damage_taken} damage (after defense)!")
        if self.hp <= 0:
            self.is_alive = False
            self.die()

    def attack_enemy(self, enemy):
        damage = max(0, self.attack)  # Basic attack calculation
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def use_item(self, item):
        if item == "Health Potion" and "Health Potion" in self.inventory:
            healing = 30  # Heal for 30 HP
            self.hp += healing
            self.inventory.remove("Health Potion")
            print(f"{self.name} uses a Health Potion and heals for {healing} HP!")
        else:
            print(f"{item} is not available in your inventory!")

    def die(self):
        print(f"{self.name} has died! Game Over.")
        self.lose_items()

    def lose_items(self):
        print(f"{self.name} has lost all their items.")
        self.inventory = []
        self.money = 0
        print(f"Remaining items: {self.inventory}")
        print(f"Remaining money: {self.money}")

    def check_alive(self):
        return self.hp > 0

    def display_status(self):
        print(f"{self.name}'s HP: {self.hp} | Money: {self.money} | Attack: {self.attack} | Defense: {self.defense}")
        print(f"Inventory: {self.inventory}")

class Game:
    def __init__(self):
        self.map = {
            'start': ['forest', 'shop'],
            'forest': ['start', 'goblin', 'ogre'],
            'shop': ['start'],
            'goblin': ['forest'],
            'ogre': ['forest'],
        }
        self.locations = {
            'start': "You are at the start of your adventure. You can go to the forest or the shop.",
            'forest': "You are in a dense forest. You can see a Goblin and an Ogre nearby. You can go back to the start.",
            'shop': "You are in a small shop. You can buy items from the shopkeeper.",
            'goblin': "A Goblin is here! Prepare for battle!",
            'ogre': "An Ogre blocks your way! Prepare for battle!",
        }
        self.player = None
        self.shopkeeper = ShopDude(
            "Shopkeeper",
            stock=["Health Potion", "Sword", "Shield"],
            prices={"Health Potion": 10, "Sword": 25, "Shield": 30}
        )

    def setup_game(self):
        # Create the player
        player_name = input("Enter your character's name: ")
        self.player = MainCharacter(player_name, inventory=[], money=50, hp=100, attack=20, speed=5)

    def display_location(self, location):
        if location not in self.locations:
            print("Invalid location! You are at the start.")
            return False
        print(self.locations[location])
        if location == 'forest':
            print("1. Fight Goblin")
            print("2. Fight Ogre")
            print("3. Go back to the start")
        elif location == 'shop':
            print("Items available for purchase:")
            for item, price in self.shopkeeper.prices.items():
                print(f"{item}: {price} gold")
            print("1. Buy Health Potion")
            print("2. Buy Sword")
            print("3. Buy Shield")
            print("4. Go back to the start")
        elif location == 'start':
            print("1. Go to the forest")
            print("2. Go to the shop")
        return True

    def move(self, current_location, choice):
        # Proper movement logic
        if choice == "1":
            if current_location == 'start':
                return 'forest'
            elif current_location == 'forest':
                return 'goblin'  # Going to fight Goblin
            elif current_location == 'shop':
                return 'start'
        elif choice == "2":
            if current_location == 'start':
                return 'shop'
            elif current_location == 'forest':
                return 'ogre'  # Going to fight Ogre
            elif current_location == 'shop':
                return 'start'
        elif choice == "3":
            return 'start'

    def fight(self, enemy):
        while enemy.is_alive and self.player.check_alive():
            # Display stats and inventory before each turn
            print(f"\n{self.player.name}'s stats: HP = {self.player.hp}, Attack = {self.player.attack}, Defense = {self.player.defense}, Inventory: {self.player.inventory}")
            print(f"{enemy.name}'s stats: HP = {enemy.ehp}, Attack = {enemy.eattack}")
            
            print("\nWhat would you like to do?")
            print("1. Attack")
            print("2. Use Item")
            print("3. Flee")
            action = input("Choose your action: ")

            if action == "1":
                self.player.attack_enemy(enemy)
                if enemy.is_alive:
                    enemy.attack(self.player)
            elif action == "2":
                print("Which item would you like to use?")
                print("1. Health Potion")
                item_choice = input("Choose an item to use: ")
                if item_choice == "1":
                    self.player.use_item("Health Potion")
                    if enemy.is_alive:
                        enemy.attack(self.player)
                else:
                    print("Invalid item.")
            elif action == "3":
                print(f"You fled from the {enemy.name}!")
                break
            else:
                print("Invalid action.")
            # After the action, display updated stats
            print(f"\n{self.player.name}'s stats: HP = {self.player.hp}, Attack = {self.player.attack}, Defense = {self.player.defense}, Inventory: {self.player.inventory}")
            print(f"{enemy.name}'s stats: HP = {enemy.ehp}, Attack = {enemy.eattack}")
            
            if not self.player.check_alive():
                break

    def play(self):
        self.setup_game()
        current_location = 'start'

        while self.player.check_alive():
            if not self.display_location(current_location):
                current_location = 'start'  # Reset to a valid location (start)
                continue
            choice = input("What will you do? ")

            # Handle movement logic
            if current_location == 'start':
                if choice == "1":
                    current_location = self.move(current_location, "1")
                elif choice == "2":
                    current_location = self.move(current_location, "2")
                else:
                    print("Invalid action.")

            elif current_location == 'forest':
                if choice == "1":
                    goblin = Enemy("Goblin", 30, 10, 3)
                    print("\nYou encounter a Goblin!")
                    self.fight(goblin)
                elif choice == "2":
                    ogre = Enemy("Ogre", 50, 15, 2)
                    print("\nYou encounter an Ogre!")
                    self.fight(ogre)
                elif choice == "3":
                    current_location = self.move(current_location, "3")

            elif current_location == 'shop':
                if choice == "1":
                    self.player.buy("Health Potion", self.shopkeeper)
                elif choice == "2":
                    self.player.buy("Sword", self.shopkeeper)
                    self.player.attack += 10  # Sword increases attack
                    print(f"{self.player.name} now has {self.player.attack} attack!")
                elif choice == "3":
                    self.player.buy("Shield", self.shopkeeper)
                    self.player.defense += 5  # Shield increases defense
                    print(f"{self.player.name} now has {self.player.defense} defense!")
                elif choice == "4":
                    current_location = self.move(current_location, "4")
                else:
                    print("Invalid option.")

            self.player.display_status()

        print("Game Over")

if __name__ == "__main__":
    game = Game()
    game.play()
