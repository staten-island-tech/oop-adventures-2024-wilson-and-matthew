import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Bullet:
    damage = 5
    def __init__(self, x, y, direction_x, direction_y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = GREEN
        self.speed = 10
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
        if bullet_rect.colliderect(monster_rect):
            monster.hp -= self.damage
            return True
        return False