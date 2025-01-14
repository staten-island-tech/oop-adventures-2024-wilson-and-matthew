import pygame
import threading
import queue
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
HIGH_SCORE_FILE = 'high_score.txt'

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Game")
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        self.initial_spawn_position = (1 * TILE_SIZE, 1 * TILE_SIZE)
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1])
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)
        self.fight_started = False
        self.proximity_message = ""
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.score = 0
        self.gold = 100
        self.input_queue = queue.Queue()
        self.merchant_menu_active = False
        self.previous_monster_position = None
        self.previous_player_position = None
        self.merchant_original_position = (self.merchant.x, self.merchant.y)
        self.high_score = self.load_high_score()

    def reset_game(self):
        self.dungeon = Dungeon(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.player = Player(self.initial_spawn_position[0], self.initial_spawn_position[1])
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)
        self.fight_started = False
        self.proximity_message = ""
        self.score = 0
        self.gold = 100

    def load_high_score(self):
        try:
            with open(HIGH_SCORE_FILE, 'r') as file:
                high_score = int(file.read())
                return high_score
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0
        
    def save_high_score(self):
        with open(HIGH_SCORE_FILE, 'w') as file:
            file.write(str(self.high_score))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.proximity_message == "Press Space to Interact":
                        self.toggle_merchant_menu()
                    elif self.proximity_message == "Press Space to Fight":
                        self.start_boss_fight()

    def clear_walls_for_merchant_interaction(self):
        self.dungeon.clear_walls()
        self.previous_monster_position = (self.monster.x, self.monster.y)
        self.previous_player_position = (self.player.x, self.player.y)
        self.monster.x = -TILE_SIZE
        self.monster.y = -TILE_SIZE
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10
        self.merchant.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        self.merchant.y = SCREEN_HEIGHT // 4 - TILE_SIZE // 2
        self.proximity_message = ""

    def teleport_monster_back(self):
        self.monster.x, self.monster.y = self.previous_monster_position
        self.previous_monster_position = None

    def teleport_player_back(self):
        self.player.x, self.player.y = self.previous_player_position
        self.previous_player_position = None
    
    def teleport_merchant_back(self):
        self.merchant.x, self.merchant.y = self.merchant_original_position

    def toggle_merchant_menu(self):
        if self.merchant_menu_active:
            self.teleport_player_back()
            self.teleport_monster_back()
            self.teleport_merchant_back()
            self.dungeon.restore_walls()
            self.merchant_menu_active = False
        else:
            self.clear_walls_for_merchant_interaction()
            self.merchant_menu_active = True
            self.input_queue = queue.Queue()
            threading.Thread(target=self.handle_terminal_input, daemon=True).start()

    def upgradedmg(self):
        cost = 20
        if self.gold >= cost:
            self.player.bullet_damage += 5
            self.gold -= cost
            print("Damage upgraded!")
        else:
            print("Not enough gold!")

    def upgradefr(self):
        cost = 20
        if self.gold >= cost:
            if self.player.fire_rate > 0.1:
                self.player.fire_rate -= 0.05
                self.gold -= cost
                print("Fire rate upgraded!")
            else:
                print("Fire rate already at maximum!")
        else:
            print("Not enough gold!")
    
    def upgradehp(self):
        cost = 20
        if self.gold >= cost:
            self.player.hp += 50
            self.gold -= cost
            print("50 HP Increased!")
        else:
            print("Not enough gold!")

    def handle_terminal_input(self):
        while self.merchant_menu_active:
                print("                        ")
                print("--------MERCHANT--------")
                print("                        ")
                print("------------------------")
                print("Your current gold is:", self.gold)
                print("1 - Upgrade Damage Current Damage:", self.player.bullet_damage)
                print("2 - Upgrade Firerate Current Firerate", self.player.fire_rate)
                print("3 - Increase 50 HP")
                print("------------------------")
                print("                        ")
                choice = input("Choose an option: ")
                if not self.merchant_menu_active:
                    break
                self.input_queue.put(choice)
    
    def process_input(self):
        if self.merchant_menu_active and not self.input_queue.empty():
            choice = self.input_queue.get()
            if choice == '1':
                self.upgradedmg()
            elif choice == '2':
                self.upgradefr()
            elif choice == '3':
                self.upgradehp()
            else:
                print("ERROR")       

    def start_boss_fight(self):
        self.starting_position = (self.player.x, self.player.y)
        self.dungeon.clear_walls()
        self.player.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        self.player.y = SCREEN_HEIGHT - TILE_SIZE - 10
        self.merchant.x = -TILE_SIZE
        self.merchant.y = -TILE_SIZE
        self.monster.x = SCREEN_WIDTH // 2 - TILE_SIZE // 2
        self.monster.y = SCREEN_HEIGHT // 2 - TILE_SIZE // 2
        self.fight_started = True
        self.player.pistol = True

    def end_boss_fight(self):
        self.dungeon.restore_walls()
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)
        self.player.x, self.player.y = self.starting_position
        self.fight_started = False
        self.proximity_message = ""

    def update(self):
        if self.player.hp <= 0:
            self.reset_game()
            return
        if self.monster.hp <= 0:
            self.monster.remove_from_game(self.dungeon)
            self.player.bullets.clear()
            self.dungeon.restore_walls()
            self.end_boss_fight()
            self.score += 10
            self.gold += 10
            self.monster.update_hp(self.score)
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(-PLAYER_SPEED, 0, self.dungeon, [self.monster])
        if keys[pygame.K_d]:
            self.player.move(PLAYER_SPEED, 0, self.dungeon, [self.monster])
        if keys[pygame.K_w]:
            self.player.move(0, -PLAYER_SPEED, self.dungeon, [self.monster])
        if keys[pygame.K_s]:
            self.player.move(0, PLAYER_SPEED, self.dungeon, [self.monster])

        if self.fight_started and pygame.mouse.get_pressed()[0]:
            self.player.shoot()

        self.proximity_message = ""
        if not self.fight_started:
            dist = self.monster.distance_to_player(self.player)
            if dist <= PROXIMITY_RANGE:
                self.proximity_message = "Press Space to Fight"

            dist_merchant = self.merchant.distance_to_player(self.player)
            if dist_merchant <= PROXIMITY_RANGE:
                self.proximity_message = "Press Space to Interact"

        if self.fight_started:
            self.monster.move_randomly(self.dungeon)
            self.monster.shoot(self.player)
            self.monster.update_projectiles(self.player)
            self.player.update_bullets(self.monster)

    def draw(self):
        screen.fill(BLACK)
        self.dungeon.draw()
        self.player.draw()
        self.monster.draw()
        self.merchant.draw()

        if self.proximity_message:
            text = self.font.render(self.proximity_message, True, GREEN)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 50))

        hp_text = self.font.render(f"HP: {self.player.hp}", True, GREEN)
        screen.blit(hp_text, (10, 10))

        if self.fight_started:
            monster_hp_text = self.font.render(f"HP: {self.monster.hp}", True, RED)
            screen.blit(monster_hp_text, (SCREEN_WIDTH - 100, 10))

        score_text = self.font.render(f"Score: {self.score}     Highscore: {self.high_score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

        if self.merchant_menu_active:
            self.draw_merchant_menu()

        pygame.display.flip()

    def draw_merchant_menu(self):
        menu_text = self.font.render("Welcome to the Merchant! (Press Space to Exit)", True, BLACK)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 3))
        item_text = self.font.render("Check Terminal", True, BLACK)
        screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))

    def run(self):
        input_thread = threading.Thread(target=self.handle_terminal_input, daemon=True)
        input_thread.start()
        while self.running:
            self.process_input()
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

game = Game()
game.run()
pygame.quit()