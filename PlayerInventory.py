
# This file handles all player information like health, key, and score.

class PlayerInventory:
    def __init__(self):
        self.health = 50  # Starting health is now 50
        self.score = 0
        self.keys = 0
    
    def update_health(self, value):
        self.health += value
        if value > 0:
            print(f"--Health increased by {value}. Current health: {self.health}--")
        else:
            print(f"--Health decreased by {abs(value)}. Current health: {self.health}--")
    
    def update_score(self, value):
        if value < 0 and self.score + value < 0:
            # Don't let score go below 0
            value = -self.score
        
        self.score += value
        
        if value > 0:
            print(f"--Score increased by {value}. Current score: {self.score}--")
        elif value < 0:
            print(f"--Score decreased by {abs(value)}. Current score: {self.score}--")
    
    def add_key(self):
        if self.keys < 3:
            self.keys += 1
            self.score += 10
            print(f"-------- Score +10, Keys: {self.keys} -------")
        else:
            print("You already have 3 keys.")
