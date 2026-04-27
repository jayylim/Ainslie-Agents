"""
Setting the Grid-world Environment
"""
from matplotlib.patches import Rectangle

class GridEnvironment:
    def __init__(self, width, height, reward_position, reward, start=(0,0)): # __init__ defines a library of variables to call
        self.width = width
        self.height = height
        self.reward_position = reward_position
        self.start = start
        self.agent_position = start
        self.reward = reward # the environment's sole reward

# === Environment-Specific Methods ===

    # reset function (essential for all enviornments)
    def reset (self): #resets agent position when environment.reset()
        self.agent_position = self.start
        return self.agent_position
    
    # environment interaction rules
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
          
    # Rendering the grid world as a window  
    def render(self, axes, action=None):
        # Set coordinate system to match grid
        axes.clear()
        axes.set_xlim(0, self.width)
        axes.set_ylim(self.height, 0)  # invert y so (0,0) is top-left
        axes.set_aspect("equal")
        
        for col in range(self.width):
            for row in range(self.height):

                # specified colours
                cell_colour = "white"

                if (row, col) == self.reward_position:
                    cell_colour = "gold" 
                    axes.text(col + 0.5, row + 0.5 , f"{self.reward}", # create label in the center of the square
                              ha = "center", va = "center", fontsize = 12) 
                if (row, col) == self.agent_position:
                    cell_colour = "dodgerblue"
                
                # creating rectangular cells with specified colours
                cells = Rectangle( 
                    (col, row),
                    1,
                    1,
                    facecolor = cell_colour,
                    edgecolor = "black",
                    linewidth = 1
                )      
                axes.add_patch(cells)

        # set title text as agent action choice  
        if action is None:
            axes.set_title(f"Starting...")
        else:
            axes.set_title(f"Agent moved {action}") 

        # grid cell boundaries
        axes.set_xticks(range(self.width))
        axes.set_yticks(range(self.height))
        axes.grid(True)

        # remove tick labels
        axes.set_xticklabels([])
        axes.set_yticklabels([])
        axes.tick_params(left=False, bottom=False)

# === Agent-facing Layer (what the agent queries from the environment)=== 
    def get_actions(self, state=None):
        return ["up", "down", "right", "left"]
    
    # for model-based planning; assume full awareness of transition structure
    def transitions(self, state, action):
        row, col = state
        
        # Updating position by action
        if action == "up":
            row += -1
        elif action == "down":
            row += +1
        elif action == "left":
            col += -1 
        elif action == "right":
            col += +1 
        
        col = max(0, min(self.width -1, col)) # clamps columns to be between grid width-1 and 0
        row = max(0, min(self.height -1, row)) # clamps rows to be between grid height-1 and 0
    
        return (row, col) # return new position
    
    # Calculate distance from goal; agent has full awareness of reward position
    def distance(self, state):
        row, col = state
        goal_row, goal_col = self.reward_position
        return abs(row - goal_row) + abs(col - goal_col) # absolute manhattan distance from reward
 