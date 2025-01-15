<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 12/20/2024 -->

We first started making the foundational classes for the game such as the main character class and enemy class.
Initial Code:
class Maincharacter:
    def __init__(self, name, inventory, money, hp, attack):
        self.name = name
        self.inventory = inventory
        self.money = money
        self.hp = hp
        self.attack = attack
class Enemy:
    def __init__(self, ename, ehp, eattack, espeed):
        self.name = ename
        self.ehp = ehp
        self.eattack = eattack
        self.espeed = espeed
Task/Problem:
What I wanted to do was to add more features to these classes such as dying, attacking, etc
Interaction with chatgpt:
So I asked chatgpt to create a class for my player class that had taking damage in it
it gave me 
Chatgpt’s suggestions:
class Maincharacter:
    def __init__(self, name, inventory, money, hp, attack):
        self.name = name
        self.inventory = inventory
        self.money = money
        self.hp = hp
        self.attack = attack
        self.is_alive = True
    def take_damage(self, eattack):
        self.health -= eattack
        print(f"{self.name} takes {eattack} damage!")
        if self.health <= 0:
            self.is_alive = False
            self.die()
            print(f"{self.name} has been defeated!")
Reflection:
Chatgpt gave me a baseplate for creating more features such as dying and attacking now. However, one complaint I have with this is that the taking damage feature works for turn based games but not real time games I want. Also the lines that get printed feel too strange but that is easily changeable.
Testing:
After getting this code I was able to create buying, attacking, dying, and losing items.
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

What I learned:
Through chatgpt I was able to learn how to add basically any feature to a class I want. 

<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 1/2/2025 →

Task/Problem:
We thought that it would be better if we made the game in pygame due to our prior knowledge (one mini project) on how the program works. To turn the game from a turn based game into a real time game we wanted to have the player dodge the monster’s attacks while having to attack them as well. In order to do this, we need a bullet class to show the bullets that the player will have to dodge on the screen. However, I have no idea how to add a bullet class because I only know how to write code that interacts with the terminal. I am starting to think that pygame was not the best choice but it is too late to redo the entire project all over again. My initial start with the bullet classes was just:
Initial Code:
class Bullet:
def_init_(self)
Interaction with chatgpt:
Considering how I had no idea how to make a bullet class I decided to ask Chatgpt “How do I make a bullet/projectile class for my python game in pygame” and it gave me:
Chatgpt’s suggestions:
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


Reflection/Testing:
Chatgpt told me that if I wanted to make a game in pygame I would have to add a draw function onto most of my classes to draw them in the actual game. It also made me realize that for things that are constantly changing or moving such as this projectile or even the player themselves, I will need to also add an update function to each of the classes.
I put the code into a simple pygame test code and the projectiles worked as expected which is very helpful.
What I learned:
I learned that if I wanted to continue to use pygame for my final project I would have to add draw and update functions for each of the classes that will be shown in the game. This allows me to properly understand the project I am attempting to work on and not be completely reliant on chatgpt and become completely clueless on what I am actually doing. In other words, I am now able to understand the basics of creating characters in pygame.

<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 1/3/2025 -->

Task/Problem:
Considering the entire premise of the game we are making revolves around a maze or dungeon, We need the actual dungeon that the player will be playing in. The problem is none of us understand anything about creating maps in real life let alone in python, a coding language we have very brief knowledge on. 
Initial Code:
As always, the only things we have for the initial code is the names for the class and the functions that we want the dungeon to have:
class Dungeon:
def_init_(self)

def generate_dungeon(self)

def draw_dungeon(self) 

Interaction with chatgpt:
I asked chatgpt how to create a dungeon map with walls that act as a maze in python pygame that allows me to use my previous code with and I pasted my previous code of the main character and enemy classes. 

Chatgpt’s Suggestion: 
class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.generate_maze()
        self.original_grid = [row[:] for row in self.grid]  # Store the original grid

    def generate_maze(self):
        # Initialize the grid with walls (1's)
        grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Randomized depth-first search (DFS) algorithm for maze generation
        def dfs(x, y):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < self.width and 0 < ny < self.height and grid[ny][nx] == 1:
                    grid[ny][nx] = 0  # Carve path
                    grid[y + dy][x + dx] = 0  # Carve the wall between
                    dfs(nx, ny)

        # Start DFS from a random point (e.g., 1,1)
        start_x, start_y = 1, 1
        grid[start_y][start_x] = 0  # Make the start point a path
        dfs(start_x, start_y)

        return grid

    def clear_walls(self):
        # Change all walls (1's) to paths (0's) to create an empty arena
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0  # Remove walls

    def restore_walls(self):
        # Restore the dungeon walls to their original state
        self.grid = [row[:] for row in self.original_grid]

    def draw(self):
        # Draw the dungeon
        for y in range(self.height):
            for x in range(self.width):
                color = WHITE if self.grid[y][x] == 0 else BLACK
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

Reflection:
I see that making a dungeon or any sort of randomly generated map for a game is extremely difficult and hard to understand for a beginner like me. I understand that if I want to properly be able to know exactly what’s happening with the code chatgpt produced I will have to do a lot of outside research as my current knowledge and understanding of python is clearly not enough for me to comprehend what is happening at all with this code.

What I learned:
I learned that if i want to create a proper functioning dungeon game I will need to do a lot of research on pygame mechanics but I also found out that much of what we learned is actually a part of this complicated code, it’s just hard to see at first glance due to all the variables and confusing code stuff surrounding it. The basic class and function parts of what we learned are still in the code as shown by the “class dungeon” and “def ____”. It is only the pygame parts of the code within these functions that are actually out of boundaries of what we had already learned. This chatgpt interaction has given me an entirely new perspective on python coding as a whole as now I know it all revolves around the same set of information/code just modified to serve the purpose of what you personally want it to.

<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 1/6/2025 →

Task/Problem:
Since we couldn’t just have the player fight the enemy in the dungeon map itself, we needed a way to transport said player into a separate, more open map where they could battle with the enemy. 

Initial Code:
There wasn’t any initial code for this part of the game because to be frank, we had absolutely no idea how to implement that into the game by ourselves, that would take an intense amount of time put into research that we just didn’t have since we started a little bit later on the game.

Interaction with ChatGPT:
We asked chatgpt for it to make that when interacting with the enemy on the dungeon map, for it to transport both it and the player to a separate blank map. After it was first created the code didn’t seem to work so we asked for a way to teleport back to the dungeon after defeating the monster also.

ChatGPT’s Suggestions:
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


    def end_boss_fight(self):
        # Restore dungeon grid and reinitialize the game state
        self.dungeon.restore_walls()
        self.merchant = Merchant()
        self.merchant.spawn(self.dungeon)  # Spawn merchant at a new location
        # Move monster out of the screen and reset its state
        self.monster = Monster(0, 0)
        self.monster.spawn(self.dungeon)  # Spawn monster at a new location

Reflection/Testing:
With the ability to transport the player and the enemy to a whole different map, we would also need a way for the player to actually initiate the battle. After looking at the code we decided it would be best for us to make it so that when the player got close to the enemy in the dungeon they could then press a button to initiate the fight in which they would be teleported to the map created above.

What I Learned:
I learned about a .restore feature that works similarly to .append and .remove in the sense that all three activate by placing it behind a self.___. I am not entirely sure if this is just a pygame feature or something you can do in regular python but that will need to be tested. I know that this can be used to restore the walls in our dungeon game but I wonder if there are any other use cases for this other than that. 

<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 1/8/2025 →

Task/Problem:
We now needed a scoring system and ui somewhere in the game to indicate the player’s hp, enemy hp, money, as well as score.
Initial Code:
What I first had in mind was to have a button the player could press on their keyboard to open up a sort of “main menu” in the terminal which would them print out their score with something like
print(“your score is ___, your hp is ___, your money is___”) 
But then we realized this method would be extremely tedious to have to do over and over again to check your basic stats and it just overall wasn’t a good idea. 

Interaction with ChatGPT:
We asked chat gpt to create code that would display the player’s hp, score, and enemy hp (if they were in a fight) that would be shown at the top of the screen and have it constantly be updated whenever any value changes.
ChatGPT’s Suggestions:
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


Reflection/Testing:
Chatgpt’s code was extremely difficult for either of us to understand as it used features in python and pygame that we had no idea about. We had no clue as to what blit or render meant at all and that was something that we would have to eventually find out.

What I Learned:
I learned that .render was another feature that fell into the same category as .append, .remove, and .restore, answering my question from the previous diary entry. This .render feature does exactly what the name suggests and renders the writing coming after it onto the screen. We also figured out that for the .render to work it would need to be followed up by code that stated exactly how large the text you are rendering would be. 






<!-- ChatGPT Coding Diary
Project Name: Object Oriented Adventures Project
Date: 1/10/2025 →

Task/Problem:
We needed a way to add the merchant class I created into the actual game itself.
Initial Code:
class Merchant:
	def _init_(self, name, stock, items)
		self.name = name
		self.stock = stock
		self.items = items
	def sell(self, items)
		self.stock.remove(items)

Interaction with ChatGPT:
We asked chatgpt to create a merchant menu that the player can interact with once entering the merchant area. For the merchant area itself we just used the same code as the enemy to appear in the dungeon and teleport them to a blank map.

ChatGPT’s Suggestions:
    def draw_merchant_menu(self):
        # Draw a simple merchant menu (for now, just a placeholder)
        menu_text = self.font.render("Welcome to the Merchant! (Press Space to Exit)", True, WHITE)
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 3))


        # You can add items to buy here (just a placeholder for now)
        item_text = self.font.render("1. Buy Health Potion - 10 Gold", True, WHITE)
        screen.blit(item_text, (SCREEN_WIDTH // 2 - item_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))
Reflection/Testing:
Chatgpt had given us example items for the main character to buy but we would obviously need more items that would actually do something when the player buys them. We decided on adding an attack damage upgrade that would increase the damage of your main attack each time you buy it.

What I Learned:
We learned that it was actually relatively simple to create a menu screen for our game as it was shown not only here but also in the previous diary entry as all you need to do is use the .render feature along with the .blit feature in conjunction to make the menu appear on screen. Previously we had learned what the .render feature did and now we understand what .blit does as it lets you choose how you want the text you chose in .render to appear on the actual game. 


