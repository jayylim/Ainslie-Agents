"""
Setting the Grid-world Environment
"""
from matplotlib.patches import Rectangle

class GridEnvironment:
    def __init__(self, width, height, rewards, start=(0,0)): # __init__ defines a library of variables to call
        self.width = width
        self.height = height
        self.rewards = rewards # this will be a dictionary in initialisation
        self.start = start
        self.agent_position = start


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

        # now check the reward dict to assign value
        for rewards in self.rewards.values(): 
            if self.agent_position == rewards["position"]:
                earned_reward = rewards["value"]
                finished = True
                break # stops after the first match

        return self.agent_position, earned_reward, finished

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
    
    # For agent to compute next state and check outcomes
    def simulate(self, state, action):

        next_state = self.transitions(state, action) # simulating next position using an internal model

        outcomes = {} # dictionary for storing possible reward targets (next states)
        row, col = next_state

        for name, rewards in self.rewards.items(): # iterate through all rewards in the environment
            goal_row, goal_col = rewards["position"]
           
            distance = abs(row - goal_row) + abs(col - goal_col) # distance from reward; in this case, absolute manhattan distance in the grid
            
            outcomes[name] = (rewards["value"], distance) # store the value and distance for each reward in evironment

        return next_state, outcomes
    
 # === Rendering the grid world as a window ===

    def render(self, axes, action=None):
        # Set coordinate system to match grid
        axes.clear()
        axes.set_xlim(0, self.width)
        axes.set_ylim(self.height, 0)  # invert y so (0,0) is top-left
        axes.set_aspect("equal")
        
        for col in range(self.width):
            for row in range(self.height):
                
                cell_colour = "white"
                # specified colours and labels
                colour_map = { # manually designate colours to reward type
                    "SS": "orange",
                    "LL": "gold"
                }
                for name, rewards in self.rewards.items(): # checks the rewards dict for 
                    if (row, col) == rewards["position"]:
                        cell_colour = colour_map.get(name, "white") # white is the defualt colour
                    
                        axes.text(
                            col + 0.5, 
                            row + 0.5 , 
                            f"{rewards['value']}", # create label in the center of the square
                            ha = "center", 
                            va = "center", 
                            fontsize = 12) 
                        break
                        
                if (row, col) == self.agent_position:
                    cell_colour = "dodgerblue"
                
                # creating rectangular cells with coloured outlines
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