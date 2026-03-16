
# Author : Hyejin Song
# ID : 23310067
#
# BottonControl.py
#    SpeedControl() - manages the temporal speed of the simulation loop
#    WeatherControl() - manages the rain visualization using animation loop on a matplotlib Axes object
#
# Revisions: 
#    10/10/2025 – Base version for assignment
#    11/10/2025 – Version 2
#

import random
import numpy as np
import names

 
class SpeedControl():
    myclass = "SpeedControl"
   
    def __init__(self, interval, min_interval, speed_factor):   
        self.interval = interval
        self.min_interval = min_interval
        self.speed_factor = speed_factor
    
    def speed_up(self, event):
        new_interval = self.interval * self.speed_factor
        self.interval = max(new_interval, self.min_interval) 

    def speed_down(self, event):
        self.interval /= self.speed_factor
        
        
class WeatherControl():
    myclass = "WeatherControl"   
    
    def __init__(self, ax_left):
        self.ax_left = ax_left
        
        self.xpos = random.randint(0,350)
        self.ypos = random.randint(0,450)
        self.sizes = random.randint(10,50)
        
        self.is_running = False
        self.timer = None
        self.scatter_plot = self.ax_left.scatter(self.xpos, self.ypos, s=self.sizes, alpha=0, color="aqua")
        
    def update_rain(self):
        if not self.is_running:
            return

        # Update scatter plot 
        self.xpos = random.randint(0,350)
        self.ypos = random.randint(0,450)
        self.sizes = random.randint(10,50)
        self.scatter_plot = self.ax_left.scatter(self.xpos, self.ypos, s=self.sizes, alpha=0.8, color="aqua")
           
        # Update scatter data   
        self.scatter_plot.set_offsets(np.c_[self.xpos, self.ypos])    
        
        # Redraw scatter plot
        self.ax_left.figure.canvas.draw_idle()
        
        # Restart timer to the next renewal(each 50ms)
        self.timer = self.ax_left.figure.canvas.new_timer(interval=50)
        self.timer.add_callback(self.update_rain)
        self.timer.start()
        
    def rain_drop(self, event):
        if not self.is_running:
            self.is_running = True
            self.update_rain()
             
    def rain_stop(self, event):
        if self.is_running:
            self.is_running = False
            
            if self.timer:
                self.timer.stop()
 
