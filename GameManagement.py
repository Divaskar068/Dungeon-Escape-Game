
#This file runs the game mechanics

import random
import time
from time import sleep
from PlayerInventory import PlayerInventory  # Import PlayerInventory

class GameManagement:
    def __init__(self):
        self.map_size = 5
        self.dungeon_map = [] #This map has the actual random generated features
        self.visible_map = [] #This map is what the player sees i.e. to hide the features
        self.item_counts = {
            'door': 3,
            'wdoor': 1, #win door
            'chest': 3,
            'key': 3,
            'beast': 3,
            'trap': 5
        }
        self.riddles = [
            {"question": "I am an odd number. Take away a letter and I become even. What number am I?", "answer": "seven"},
            {"question": "What has keys but no locks, space but no room, and you can enter but not go in?", "answer": "keyboard"},
            {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
            {"question": "I have a head and a tail, but no legs. What am I?", "answer": "coin"},
            {"question": "What gets wetter as it dries?", "answer": "towel"}
        ]
        # Building the dungeon
        self.create_dungeon()

    def create_dungeon(self):
        
        self.dungeon_map = []
        for i in range(self.map_size):
            row = []
            for j in range(self.map_size):
                row.append(' ')
            self.dungeon_map.append(row)
        # Clear and add 'x' to visible map
        self.visible_map = []
        for i in range(self.map_size):
            row = []
            for j in range(self.map_size):
                row.append('x')
            self.visible_map.append(row)
        self.visible_map[0][0] = ' '
        
        # Place items on the map
        for item, count in self.item_counts.items():
            placed = 0
            while placed < count:
                # random places
                x = random.randint(0, 4)
                y = random.randint(0, 4)
                if self.dungeon_map[x][y] == ' ':
                    if item == 'door':
                        self.dungeon_map[x][y] = 'D'
                    elif item == 'wdoor':
                        self.dungeon_map[x][y] = 'W'
                    elif item == 'chest':
                        self.dungeon_map[x][y] = 'C'
                    elif item == 'key':
                        self.dungeon_map[x][y] = 'K'
                    elif item == 'beast':
                        self.dungeon_map[x][y] = 'B'
                    elif item == 'trap':
                        self.dungeon_map[x][y] = 'T'
                    placed += 1

    def print_map(self, player_pos, player_inventory):
        print("\nDungeon Map:")
        for i in range(self.map_size):
            row_display = []
            for j in range(self.map_size):
                if [i, j] == player_pos:
                    row_display.append("-")  # Player's position as '-'
                else:
                    row_display.append(self.visible_map[i][j])  # Show only what's been revealed
            print("| " + " | ".join(row_display) + " |")
        print(f"Health: {player_inventory.health} | Score: {player_inventory.score} | Keys: {player_inventory.keys}")


    def check_position(self, player_pos, player_inventory):
        x, y = player_pos
        old_cell = self.visible_map[x][y] # this place should have 'x'
        self.visible_map[x][y] = self.dungeon_map[x][y] # showing features
        item = self.dungeon_map[x][y]
        if item == ' ':
            if old_cell == 'x':
                print("\nNew place explored")
                player_inventory.update_score(5)
            else:
                print("\nYou revisited an explored space.")
                player_inventory.update_score(-5)
        elif item == 'T':
            self.handle_trap(player_pos, player_inventory)
        elif item == 'K':
            self.handle_key(player_pos, player_inventory)
        elif item == 'D':
            self.handle_door(player_pos, player_inventory)
        elif item == 'W':
            self.handle_wdoor(player_pos, player_inventory)   
        elif item == 'B':
            self.handle_beast(player_pos, player_inventory)
        elif item == 'C':
            self.handle_chest(player_pos, player_inventory)


    def handle_trap(self, player_pos, player_inventory):
        x, y = player_pos
        print("\n\t\tA TRAP!")
        sleep(0.40) 
        print('\nGenerating a pattern to escape the trap',end='',flush=True)
        for i in range(3):
            print('.', end='', flush=True)
            sleep(0.25)
        sleep(0.75)
        
        # Generate random trap pattern with < and > and spaces
        pattern_chars = ['<', '>', ' ']
        pattern = ''.join([random.choice(pattern_chars) for i in range(6)]) #To join a list of chars into a single string using join
        print(f"\nTrap pattern found:{pattern}.")
        user_input = input("\nEnter the pattern (Do not include \'.\'): ")
        if user_input != pattern:
            print("You failed to escape the trap.")
            player_inventory.update_health(-10)
            player_inventory.update_score(-30)     
        else:
            print("Trap escaped! Score +50")
            player_inventory.update_score(50)
            
        # Clear the trap from the dungeon map
        self.dungeon_map[x][y] = ' '
        self.visible_map[x][y] = ' '


    def handle_key(self, player_pos, player_inventory):
        x, y = player_pos
        print('\n          You found a Key!')
        player_inventory.add_key()
        self.dungeon_map[x][y] = ' '  
        self.visible_map[x][y] = ' '  


    def handle_door(self, player_pos, player_inventory):
        x, y = player_pos
        # is_exit = (player_pos == self.exit_door_pos)
        
        print("\n-------------DOOR FOUND-------------")
        sleep(0.25)  
        riddle = random.choice(self.riddles)
        self.riddles.remove(riddle) #removing the riddle to avoid duplicates
        print(f"| Something is written on the door |")
        sleep(0.75)
        print(f'" {riddle["question"]} "')
        
        while player_inventory.keys > 0:
            if player_inventory.keys == 3:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: The answer starts with '{riddle['answer'][0]}'")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
            elif player_inventory.keys == 2:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: The answer ends with '{riddle['answer'][len(riddle['answer'])-1]}'")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
            elif player_inventory.keys == 1:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: It is a {len(riddle['answer'])} letter word")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            user_answer = input("\nYour answer: ").strip().lower()
            if user_answer == riddle["answer"]:
                print("\nCORRECT!")
                sleep(0.25)
                print('Opening door', end='', flush=True)
                for _ in range(3):
                    time.sleep(0.25)
                    print('.', end='', flush=True)
                sleep(0/50)
                print('\nThis door was not the EXIT')
                sleep(0.25)
                # Add a key as reward for solving the riddle
                print("You found a key hidden behind the door!")
                player_inventory.add_key()
                
                self.dungeon_map[x][y] = ' ' 
                self.visible_map[x][y] = ' '  
                return
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"Wrong answer! You have {remaining} more attempts.")
                else:
                    print("You failed to solve the riddle. Health -10")
                    player_inventory.update_health(-10)
                    self.dungeon_map[x][y] = ' '  
                    self.visible_map[x][y] = ' ' 
                    return
   
   
    def handle_wdoor(self, player_pos, player_inventory):
        x, y = player_pos
        print("\n-------------DOOR FOUND-------------")
        sleep(0.25)  
        riddle = random.choice(self.riddles)
        self.riddles.remove(riddle) # Removing the riddle to avoid duplicates
        print(f"| Something is written on the door |")
        sleep(0.75)  
        print(f'" {riddle["question"]} "')
        
        while player_inventory.keys > 0:
            if player_inventory.keys == 3:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: The answer starts with '{riddle['answer'][0]}'")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
            elif player_inventory.keys == 2:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: The answer ends with '{riddle['answer'][len(riddle['answer'])-1]}'")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
            elif player_inventory.keys == 1:
                choice = input("\nEnter 'y' to use a key for a hint or 'n' to skip: ").strip().lower()
                if choice == 'y':
                    player_inventory.keys -= 1
                    print(f"Hint: It is a {len(riddle['answer'])} letter word")
                elif choice == 'n':
                    break
                else:
                    print('Invalid')
        
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            user_answer = input("\nYour answer: ").strip().lower()
            if user_answer == riddle["answer"]:
                print("\nCORRECT!")
                print('Opening door', end='', flush=True)
                for _ in range(3):
                    time.sleep(0.25)
                    print('.', end='', flush=True)
                print('\n')
                player_inventory.update_score(200) #200 score for winning the game
                print('\n************** Hurray! You found the EXIT! *****************')
                sleep(0.25)
                self.display_fancy_win(player_inventory.score)
                exit()  # End the game
                self.dungeon_map[x][y] = ' ' 
                self.visible_map[x][y] = ' ' 
                return
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"Wrong answer! You have {remaining} more attempts.")
                else:
                    sleep(0.25)
                    print('Wrong! EXIT DOOR!')
                    player_inventory.update_score(-20)
                    if player_inventory.score < 0:
                        player_inventory.score = 0
                    sleep(0.50)
                    print('\n************ Oh no! The dungeon has collapsed! *************')
                    sleep(0.50)
                    self.display_fancy_game_over(player_inventory.score)
                    exit()  # End the game
                    self.dungeon_map[x][y] = ' ' 
                    self.visible_map[x][y] = ' ' 
                    return
    

    def display_fancy_win(self, score):
        print("*" * 60)
        print("*" + " " * 58 + "*")
        print("*" + " " * 20 + "DUNGEON ESCAPED!" + " " * 22 + "*")
        print("*" + " " * 58 + "*")
        print("*" + " " * 19 + f"FINAL SCORE: {score}" + " " * (26 - len(str(score))) + "*")
        print("*" + " " * 58 + "*")
        print("*" + " " * 14 + "Congratulations on your victory!" + " " * 12 + "*")
        print("*" + " " * 58 + "*")
        print("*" * 60)
    

    def display_fancy_game_over(self, score):
        print("*" * 60)
        print("*" + " " * 58 + "*")
        print("*" + " " * 24 + "GAME OVER" + " " * 25 + "*")
        print("*" + " " * 58 + "*")
        print("*" + " " * 19 + f"FINAL SCORE: {score}" + " " * (26 - len(str(score))) + "*")
        print("*" + " " * 58 + "*")
        print("*" + " " * 15 + "Better luck next time, explorer!" + " " * 11 + "*")
        print("*" + " " * 58 + "*")
        print("*" * 60)


    def handle_beast(self, player_pos, player_inventory):
        x, y = player_pos
        
        print("\n\tA BEAST! ")
        sleep(0.25) 
        print('>>>>> Fighting beast ', end='',flush=True)
        for i in range(5):
            print('<', end='', flush=True)
            sleep(0.25)
        beast_attack = random.choice(['win','lose'])
        if beast_attack == 'lose':
            print('\n\nYou lost the fight, Health -10, Score -40')
            player_inventory.update_health(-20)
            player_inventory.update_score(-40)
        else:
            print('\n\nFight Won ! Rewards: Healing portion!')
            player_inventory.update_health(10)
            player_inventory.update_score(50)
            
        self.dungeon_map[x][y] = ' '  
        self.visible_map[x][y] = ' ' 


    def handle_chest(self, player_pos, player_inventory):
        x, y = player_pos
        print("\n------------CHEST FOUND------------")

        chest_content = random.choice(['key', 'hk', 'empty'])      
        if chest_content == 'key':
            sleep(0.50)
            print("|          You got a key!          |")
            player_inventory.add_key()
        elif chest_content == 'hk':
            sleep(0.50)
            print("|  Health potion found! Health +10 |")
            print("|          You got a key!          |")
            player_inventory.add_key()
            player_inventory.update_health(10)
        else:
            sleep(0.50)
            print("|        The chest is empty       |")
        
        self.dungeon_map[x][y] = ' '
        self.visible_map[x][y] = ' ' 
