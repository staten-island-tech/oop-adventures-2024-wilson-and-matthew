class Enemy:
    def __init__(self, ename, ehp, eattack, espeed):
        self.name = ename
        self.ehp = ehp
        self.eattack = eattack
        self.espeed = espeed
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
ename1 = "cube"
enemy = Enemy(ename1, ehp=100, eattack=5, espeed=10)
###########################################################################################################################################################################################
###########################################################################################################################################################################################
###########################################################################################################################################################################################
import pygame
import time
import math

TILE_SIZE = 32
RED = (255, 0, 0)
screen = pygame.display.set_mode((800, 600)) 

class Projectile:
    def __init__(self, x, y, direction_x, direction_y, speed):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = (0, 255, 0)  #
        self.speed = speed 
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, ename, x, y, ehp, eattack, espeed, erate):
        self.name = ename
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = RED
        self.ehp = ehp
        self.eattack = eattack
        self.speed = espeed 
        self.erate = erate  
        self.is_alive = True
        self.projectiles = []
        self.last_shot_time = time.time()

    def attack(self, player):
        if self.is_alive:
            damage = self.eattack
            print(f"{self.name} attacks {player.name} for {damage} damage!")
            player.take_damage(damage)

"""     def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
        print(f"{self.name} moves {direction}.") """

def shoot(self, player):
        current_time = time.time()
        if current_time - self.last_shot_time > (1 / self.erate):  
            direction_x = player.x - self.x
            direction_y = player.y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            direction_x /= distance
            direction_y /= distance
            projectile = Projectile(self.x + self.width // 2, self.y + self.height // 2, direction_x, direction_y, self.speed)
            self.projectiles.append(projectile)
            self.last_shot_time = current_time

def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()  

def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for projectile in self.projectiles:
            projectile.draw()  

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.hp} HP remaining.")

Monster = Enemy(ename="Monster", x=100, y=100, ehp=100, eattack=5, espeed=8, erate=2)  