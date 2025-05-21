
# THIS IS THE MAIN FILE - RUN THIS FILE cmd- python3 DungeonEscape.py

from time import sleep
from GameManagement import GameManagement  
from PlayerInventory import PlayerInventory  

class DungeonEscape:
    def __init__(self):
        self.player_pos = [0, 0]  # Player starts at (0,0)
        self.player_inventory = PlayerInventory()
        self.game_management = GameManagement()

    def move_player(self, direction):
        x, y = self.player_pos
        if direction == 'w' and x > 0:
            self.player_pos = [x-1, y]
            self.game_management.print_map(self.player_pos, self.player_inventory)
        elif direction == 's' and x < 4:
            self.player_pos = [x+1, y]
            self.game_management.print_map(self.player_pos, self.player_inventory)
        elif direction == 'a' and y > 0:
            self.player_pos = [x, y-1]
            self.game_management.print_map(self.player_pos, self.player_inventory)
        elif direction == 'd' and y < 4:
            self.player_pos = [x, y+1]
            self.game_management.print_map(self.player_pos, self.player_inventory)
        else:
            print("Invalid move! Try again.")
            return

        self.game_management.check_position(self.player_pos, self.player_inventory)

    def play(self):
        
        for i in range(3):
            print('.', end='', flush=True)
            sleep(0.25)

        self.game_management.print_map(self.player_pos, self.player_inventory)
        while self.player_inventory.health > 0:
            move = input("\nMove (w/a/s/d): ").strip().lower()
            self.move_player(move)
            if self.player_inventory.health <= 0:
                sleep(0.25)
                print("\nYou have lost all your health!")
                sleep(0.50)
                self.game_management.display_fancy_game_over(self.player_inventory.score)
                break

def main():
    print('\n>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<')
    print('\n>>> STARTING DUNGEON ESCAPE GAME <<<\n')
    print('>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<')
    game = DungeonEscape()
    game.play()

if __name__ == "__main__":
    main()
