class Enemy:
    def __init__(self, ename, ehp, eattack):
        self.name = ename
        self.ehp = ehp
        self.eattack = eattack
        self.is_alive = True

    def attack(self, player):
        if self.is_alive:
            print(f"{self.name} attacks {player.name} for {self.attack_damage} damage!")
            player.take_damage(self.attack_damage)

    def move(self, direction):
        print(f"{self.name} moves {direction} with a speed of {self.speed}.")

