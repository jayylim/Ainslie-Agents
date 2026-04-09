"""
Setting the Grid-world Environment
"""

class Environment:
    def __init__(self, width, height, start, rewardPosition): # __init__ defines a library of variables to call
        self.width = width
        self.height = height
        self.start = start
        self.rewardPosition = rewardPosition
        self.agentPosition = start

    def reset (self):
        self.agentPosition = self.start
        return self.agentPosition
    
    def step(self, action):
        x, y = self.agentPosition # row indexes from the top left of the grid, and count from 0

        # Updating position by action
        if action == "up":
            y += -1
        elif action == "down":
            y += +1
        elif action == "left":
            x += -1 
        elif action == "right":
            x += 1 
        
        # Keep position within boundaries
        x = max(0, min(self.width -1, x)) # clamps x to be between grid width-1 and 0
        y = max(0, min(self.height -1, y)) # clamps x to be between grid height-1 and 0
    
        # Save updated position
        self.agentPosition = (x, y)

        # Default reward
        reward_value = 0 # default reward
        finished = False # used as criteria for continuing later

        if self.agentPosition == self.rewardPosition:
            reward_value = 10
            finished = True
        
        return self.agentPosition, reward_value, finished
    
    
    # Displaying the grid with rows and columns (starting form top left)  and filling with symbols
    def display(self):
        for y in range(self.height):
            symbol = []

            for x in range(self.width):
                if (x, y) == self.agentPosition:
                    symbol.append("@")
                elif (x, y) == self.rewardPosition:
                    symbol.append("$")
                else:
                    symbol.append(".")

            print (" ".join(symbol))
        
        print() # adds a blank line
        

