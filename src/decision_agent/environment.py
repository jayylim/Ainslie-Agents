"""
Setting the Grid-world Environment
"""

class Environment:
    def __init__(self, width, height, reward_position, reward, start=(0,0)): # __init__ defines a library of variables to call
        self.width = width
        self.height = height
        self.reward_position = reward_position
        self.start = start
        self.agent_position = start
        self.reward = reward # the environment's sole reward

    def reset (self): #resets agent position when environment.reset()
        self.agent_position = self.start
        return self.agent_position
    
    def step(self, action):
        # position counting starts from the top left of the grid, and count from 0
        row, col = self.agent_position

        # Updating position by action
        if action == "up":
            row += -1
        elif action == "down":
            row += +1
        elif action == "left":
            col += -1 
        elif action == "right":
            col += +1 
        
        # Keep position within boundaries
        col = max(0, min(self.width -1, col)) # clamps columns to be between grid width-1 and 0
        row = max(0, min(self.height -1, row)) # clamps rows to be between grid height-1 and 0
    
        # Save updated position
        self.agent_position = (row, col)

        # Default reward
        earned_reward = 0 # actual reward gained for making step 
        finished = False # used as criteria for continuing later

        if self.agent_position == self.reward_position:
            earned_reward = self.reward
            finished = True
        
        return self.agent_position, earned_reward, finished
    
    
    # Displaying the grid with rows and columns (starting form top left) and fill with symbols
    def display(self):
        for y in range(self.height): # y is the row index (vertical plane)
            symbol = []

            for x in range(self.width): # x is the column index (horizontal plane)
                if (y, x) == self.agent_position:
                    symbol.append("@")
                elif (y, x) == self.reward_position:
                    symbol.append("$")
                else:
                    symbol.append(".")

            print (" ".join(symbol))
        
        print() # adds a blank line
        

