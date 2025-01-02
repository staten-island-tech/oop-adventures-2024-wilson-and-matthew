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

class Enemy:
    def __init__(self, ename, ehp, eattack):
        self.name = ename
        self.ehp = ehp
        self.eattack = eattack
        self.is_alive = True

    # def attack(self, player):
    #     if self.is_alive:
    #         print(f"{self.name} attacks {player.name} for {self.attack_damage} damage!")
    #         player.take_damage(self.attack_damage)

    def attack(self, player):
        if self.is_alive:
            damage = self.eattack
            print(f"{self.name} attacks {player.name} for {damage} damage!")
            player.take_damage(damage)


    def move(self, direction):
        print(f"{self.name} moves {direction} with a speed of {self.speed}.")

class shopdude:
    def __init__(self, name, stock, items):
        self.name = name
        self.stock = stock
        self.items = items
    def sell(self, item):
        self.stock.append(item)
        print(self.inventory)
