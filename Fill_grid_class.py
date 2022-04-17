import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import MaxNLocator
import numpy as np

class fill_grid_plotter():
    """Takes an integer and returns a animated plot of a grid being filled with
    that many blocks"""
    
    def __init__(self, blocks=25, fill_empties=False, clean_figure=False
           , x_blocks=None, y_blocks=None):
        self.blocks = int(blocks)
        self.x_blocks = x_blocks if x_blocks is not None else int(np.sqrt(blocks))
        self.y_blocks = y_blocks if y_blocks is not None else np.ceil(self.blocks/self.x_blocks)
        self.fill_empties = fill_empties
        self.clean_figure = clean_figure
        self.patches_dict = {}
        self.micro_pause_secs = 0.001 # small plt.pause time to prevent auto plotting
        
    
    def create_figure_window(self):
        fig = plt.figure(figsize=(5,6))
        self.ax = fig.add_subplot(111, aspect='equal')
        self.ax.set_xlim([0, self.x_blocks])
        self.ax.set_ylim([0, self.y_blocks + 1])
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # add upper boundary line
        self.boundary = self.ax.plot(np.linspace(0, self.x_blocks), [self.y_blocks]*50,'--k', linewidth=3)
    
    def initialise_positions(self):
        # generate random block positions
        self.x_pos = np.arange(0, self.x_blocks)
        self.x = np.random.choice(self.x_pos, size=self.blocks)

        # start each block one block width below the start
        self.y = [-1] * self.blocks
        
    
    def add_block(self, i, x, y, fc=False):
        # create the block at location (x,y), with dimensions (1,1), with black edge color
        
        if fc is False:
            # face color with smoothly varying RBG vals as block number goes up
            fc = (1-i/self.blocks, i/(2*self.blocks), i/self.blocks)
            
        p = patches.Rectangle((x, y), 1, 1, ec='k', fc=fc)
        self.ax.add_patch(p)
        plt.pause(self.micro_pause_secs)
        return p
    
    def down(self, p, z):
        z -= 1 # slide the block down by one block length
        p.set_y(z)
        plt.pause(self.micro_pause_secs)
        return z
    
    def right(self, p, j):
        # avoid indexing errors on last item
        if j == self.x_blocks-1:
            j = -1
            
        # move block to the right
        j += 1
        p.set_x(self.x_pos[j])
        plt.pause(self.micro_pause_secs)
        return j
        
    
    def block_handler(self, block_num):
        self.ax.set_title('N='+str(block_num+1)+'/'+str(self.blocks))
        
        # initial block height will be above the max height of the stack
        z = self.y_blocks + 1
        
        # index of x position
        # n.b. == returns a tuple of 1s and 0s, argmax finds the index of the first 1
        j = np.argmax(self.x[block_num] == self.x_pos)
        
        # add the patch
        p = self.add_block(block_num, self.x_pos[j], z)
        
        # slide patch down so now is on top of the grid boundary line
        z = self.down(p, z)
        
        moves = 0
        # if the stack in the blocks x position is full slide the block right
        while self.y[j] >= self.y_blocks - 1 and moves < self.x_blocks:
            j = self.right(p, j)
            moves += 1
            
        # if every column has been tried the grid is full, stop
        if moves == self.x_blocks:
            exit
            
        # if the stack has spare space, slide the block down
        while z > self.y[j] + 1:
            z = self.down(p, z)
        self.y[j] = z
        
        self.patches_dict[block_num] = p
            
        
    def plot(self):
        self.create_figure_window()
        self.initialise_positions()
        
        i = 0
        while i <= min(self.blocks-1, self.x_blocks*self.y_blocks-1):
            self.block_handler(block_num=i)
            i += 1
        
        max_y = max(self.y)
        
        if self.fill_empties:
            self.fill_empty()

        if self.clean_figure:
            self.clean(max_y)

            
    def fill_empty(self):
        # once all blocks are added there may be gaps
        # fill the gaps with grey blocks
        col = 0
        patch_idx = self.blocks + 1
        while col < self.x_blocks:
            while self.y[col] + 1 < self.y_blocks:
                self.y[col] += 1
                p = self.add_block(patch_idx, self.x_pos[col], self.y[col], fc='lightgrey')
                self.patches_dict[patch_idx] = p
                patch_idx += 1
            col += 1
    
    def clean(self, max_y):
        pause_len_secs = 0.2
        self.boundary.pop(0).remove()
        self.ax.xaxis.set_visible(False), plt.pause(pause_len_secs)
        self.ax.yaxis.set_visible(False), plt.pause(pause_len_secs)
        self.ax.axis('off'), plt.pause(pause_len_secs)
        self.ax.set_title(''), plt.pause(pause_len_secs)
        self.ax.set_ylim([0, max_y + 1])
        for key, val in self.patches_dict.items():
            val.set_edgecolor(None), plt.pause(pause_len_secs/100)
        

fill_grid_plotter(blocks=57
                , fill_empties=True
                , clean_figure=True
                , x_blocks=10
                , y_blocks=None ).plot()
