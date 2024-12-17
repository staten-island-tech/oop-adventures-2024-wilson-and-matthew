class maincharacter:
    def __init__(self, name, inventory, money, hp, attack, speed):
        self.name = name
        self.inventory = inventory
        self.money = money
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.is_alive = True

    def buy(self, item, money):
        self.inventory.append(item)
        print(self.inventory)
        self.inventory.remove(money)

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
