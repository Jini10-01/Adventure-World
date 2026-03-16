
# Author : Hyejin Song
# ID : 23310067
#
# Terrains.py
#    Terrains() - plot map(sky, ground, sun, moon, and cloud)
#    Pond() - plot barrier(pond)
#
# Revisions: 
#    05/10/2025 – Base version for assignment
#    07/10/2025 – Version 2 (add sun, moon, and cloud)
#    10/10/2025 – Version 3 (plot barrier(pond))
#

from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from matplotlib.patches import Circle, Rectangle

import matplotlib.patches as patches
import csv
import pandas as pd
import numpy as np

class Terrains():
    myclass = "Terrains"
    
    # Traceability Matrix reference 4.1
    # dawn
    color_palette1 = ["cornflowerblue",  # 0 cornflowerblue
                     "orchid",           # 1 orchid
                     "lemonchiffon",     # 2 lemonchiffon
                     "#8cc751"]          # 12 HTC Green  
                     
    # morning                 
    color_palette2 = ["deepskyblue",     # 3 deepskyblue
                     "lightcoral",       # 4 lightcoral
                     "gold",             # 5 gold
                     "lightgreen"]       # 12 lightgreen  
    # sunset
    color_palette3 = ["darkmagenta",     # 6 darkmagenta
                     "crimson",          # 7 crimson
                     "orangered",        # 8 orangered
                     "#8cc751"]          # 12 HTC Green              
    # midnight                                  
    color_palette4 = ["midnightblue",    # 9 midnightblue
                     "darkslateblue",    # 10 darkslateblue
                     "dimgray",          # 11 dimgray
                     "olivedrab"]        # 12 olivedrab            


    def __init__(self, color_map, filename):
        self.color_map= color_map
        self.filename = filename
  
    def plot_sky_and_ground(self, ax_left, color_map, filename, timestamp, time):
        if filename == "map_mix":
            time_of_day = timestamp / 4
            if time < time_of_day:
                self.filename = "map_dawn.csv"
            elif time_of_day <= time < time_of_day*2:
                self.filename = "map_morning.csv"
            elif time_of_day*2 <= time < time_of_day*3:
                self.filename = "map_sunset.csv"
            else:
                self.filename = "map_midnight.csv"
            self.color_map = pd.read_csv(self.filename).to_numpy(dtype=int)
            self.filename = self.filename.split(".csv")[0]

        blurred = gaussian_filter(self.color_map.astype(float), sigma=1.0)
        
        # Set color palette.
        if self.filename == "map_dawn":
            cmap = LinearSegmentedColormap.from_list("sky", self.color_palette1, N=512)
        elif self.filename == "map_morning":
            cmap = LinearSegmentedColormap.from_list("sky", self.color_palette2, N=512)
        elif self.filename == "map_sunset":
            cmap = LinearSegmentedColormap.from_list("sky", self.color_palette3, N=512)
        elif self.filename == "map_midnight":
            cmap = LinearSegmentedColormap.from_list("sky", self.color_palette4, N=512)

        ax_left.imshow(blurred, cmap=cmap, aspect="equal", interpolation='bicubic', extent=[0,350,0,450])
        
    def plot_sun_moon_cloud(self, ax_left, timestamp, time):
        if self.filename == "map_dawn":
            color = '#FF6666'
        elif self.filename == "map_morning":
            color = '#FFFF99'
        elif self.filename == "map_sunset":
            color = 'orangered'
        elif self.filename == "map_midnight":
            color = 'gold'
            
        sun_or_moon_shape = Circle((400 / timestamp * time, 400), radius=20, edgecolor=color, facecolor=color, linewidth=3)
        ax_left.add_patch(sun_or_moon_shape)    
    
        # Plot 12 sunrays
        if self.filename == "map_morning" or self.filename == "map_sunset":
            for i in range(12):
                angle = i * (2 * np.pi / 12)
                x_start = (400 / timestamp * time) + 20 * np.cos(angle)
                y_start = 400 + 20 * np.sin(angle)
                x_end = (400 / timestamp * time) + 35 * np.cos(angle) 
                y_end = 400 + 35 * np.sin(angle)
                ax_left.plot([x_start, x_end], [y_start, y_end], color=color, lw=5)
   
        # Plot clouds
        if self.filename == "map_dawn" or self.filename == "map_midnight":    
            cloud_center = [(105, 383), (260, 420)] 
            cloud_color = ['lightgray', 'grey']
            cloud_edge_color = ['lightgray', 'grey']  
                   
            for index, cloud in enumerate(cloud_center):                
                ax_left.add_patch(patches.Ellipse(cloud, width=25, height=15, angle=0, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] - 10, cloud[1] + 8), radius=8, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] + 8, cloud[1] + 8), radius=7, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] - 8, cloud[1] - 8), radius=7, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] + 8, cloud[1] - 8), radius=8, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] + 16, cloud[1]), radius=6, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                ax_left.add_patch(patches.Circle((cloud[0] - 16, cloud[1]), radius=6, facecolor=cloud_color[index], edgecolor=cloud_edge_color[index], linewidth=3))
                

class Pond():  
    myclass = "Pond"

    def __init__(self, xpos, ypos, width, height):
        self.xpos= xpos
        self.ypos = ypos
        self.width= width
        self.height = height
        
    def plot_pond(self, ax_left):  
        ax_left.add_patch(Rectangle((self.xpos-10, self.ypos-self.height-10), self.width+10, self.height+10, edgecolor="dimgrey", facecolor="dimgrey", linewidth=2))
        ax_left.add_patch(Rectangle((self.xpos-5, self.ypos-self.height-5), self.width, self.height, edgecolor="deepskyblue", facecolor="deepskyblue", linewidth=2, zorder=2.5))
        
