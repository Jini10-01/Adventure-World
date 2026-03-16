#
# Author : 23310067
# ID : Hyejin Song
#
# Patrons.py
#    Patrons() - manage the movement, state, and position of Patron walking around an theme park
#
# Revisions: 
#    06/10/2025 – Base version for assignment
#    07/10/2025 – Version 2 (add random marker, color, name)
#    08/10/2025 – Version 3 (add riding state and plot)
#

import numpy as np
import random

class Patrons():
    myclass = "Patrons"
    
    def __init__(self, xpos, ypos, name, state, color, marker, set_target_ride, class_Rides_instance, class_Terrains_instance):
        self.xpos = xpos
        self.ypos = ypos
        self.name = name
        self.state = state   # roaming, queuing, riding
        self.color = color
        self.marker = marker
        self.set_target_ride = set_target_ride
        self.class_Rides_instance = class_Rides_instance
        self.class_Terrains_instance = class_Terrains_instance
        self.artist = None       

    # Check if the patron's position is in the ride queue.     
    def inside_ride_queue(self, newxpos, newypos, i):
        return (self.class_Rides_instance[i].xqueue_min <= newxpos <= self.class_Rides_instance[i].xqueue_max) \
           and (self.class_Rides_instance[i].yqueue_min <= newypos <= self.class_Rides_instance[i].yqueue_max)
        
    # Check if the patron's position is in the pond.     
    def inside_pond_boundary(self, newxpos, newypos):
        return (self.class_Terrains_instance.xpos-10 <= newxpos <= self.class_Terrains_instance.xpos + self.class_Terrains_instance.width+10) \
           and (self.class_Terrains_instance.ypos -self.class_Terrains_instance.height-10 <= newypos <= self.class_Terrains_instance.ypos+10)
 
    # Check if the patron's position is in each ride boundary.  
    def inside_ride_boundary(self, newxpos, newypos, i):
        return (self.class_Rides_instance[i].ride_xboundary_min <= newxpos <= self.class_Rides_instance[i].ride_xboundary_max) \
           and (self.class_Rides_instance[i].ride_yboundary_min <= newypos <= self.class_Rides_instance[i].ride_yboundary_max)
    
    # Check if the patron's position is in the main boundary.
    def inside_main_boundary(self, newxpos, newypos):
        return (self.class_Rides_instance[0].main_xboundary_min < newxpos < self.class_Rides_instance[0].main_xboundary_max) \
           and (self.class_Rides_instance[0].main_yboundary_min < newypos < self.class_Rides_instance[0].main_yboundary_max)    
        
    # Check conditions - inside main boundary & outside each ride boundary.
    def is_valid(self, newxpos, newypos):
        if not self.inside_main_boundary(newxpos, newypos):
            return False 
        if self.inside_pond_boundary(newxpos, newypos):
            return False       
        for i in range(len(self.class_Rides_instance)):   
            if self.inside_ride_boundary(newxpos, newypos, i):
                return False
        return True    
          
    # Check new position, and if it valid, move new position  
    def new_position_check_boundary(self, xpos, ypos):  
        distance = [(-5, 5), (-5, 0), (-5, -5), (0, -5), (5, -5),
                    (random.choice([-5, 5, 10]), random.choice([10, 20, 30])),
                    (random.choice([-10, -20, -30]), random.choice([-5, -10, -20])),
                    (0, 15), (15, 15), (15, 0), (15, -15)] 
                           
        candidates = [(xpos+dx, ypos+dy) for dx, dy in distance]                                   
        valid_candidates = [p for p in candidates if self.is_valid(p[0], p[1])]

        if valid_candidates:
            newxpos, newypos = random.choice(valid_candidates)
        else:
            newxpos, newypos = xpos, ypos

        return newxpos, newypos   
        
    # Check if the patron's position is inside the queue's xposition or yposition.  
    def inside_targeted_queue_boundary(self, xpos, ypos):  
        if self.class_Rides_instance[self.set_target_ride].xqueue_min <= xpos <= self.class_Rides_instance[self.set_target_ride].xqueue_max:
            return "X"
        if self.class_Rides_instance[self.set_target_ride].yqueue_min <= ypos <= self.class_Rides_instance[self.set_target_ride].yqueue_max:  
            return "Y"
        return "N"   
        
    # Check new position, and if it valid, move new position.
    def new_targeted_position_check_boundary(self, xpos, ypos): 
        distance = []   
        returnVal = self.inside_targeted_queue_boundary(xpos, ypos)  
        
        if returnVal == "X":
            distance = [(0, 5), (0, 10), (0, -5), (0, -10)]
        elif returnVal == "Y":
            distance = [(5, 0), (10, 0), (-5, 0), (-10, 0)]
        else: 
            return self.new_position_check_boundary(xpos, ypos) 
    
        candidates = [(xpos+dx, ypos+dy) for dx, dy in distance]
        valid_candidates = [p for p in candidates if self.is_valid(p[0], p[1])]
    
        if valid_candidates:
            newxpos, newypos = random.choice(valid_candidates)
        else:
            newxpos, newypos = xpos, ypos
    
        return newxpos, newypos   
        
    # Move patrons. If they are inside the ride queue, then change the state and line up.       
    def step_change(self, ax_left):
        if self.state == "roaming": 
            # If patron doesn't set target ride, then move randomly
            if self.set_target_ride == "":
                self.xpos, self.ypos = self.new_position_check_boundary(self.xpos, self.ypos)
            # If patron set target ride, then move to the targeted ride
            else:
                self.xpos, self.ypos = self.new_targeted_position_check_boundary(self.xpos, self.ypos)
                           
            for i in range(len(self.class_Rides_instance)):    
                if self.inside_ride_queue(self.xpos, self.ypos, i): 
                    if self.class_Rides_instance[i].queue.qsize() < self.class_Rides_instance[i].qlimit:                        
                        self.class_Rides_instance[i].queue.put(self)
                        self.state = "queuing"
                        self.xpos = self.class_Rides_instance[i].xqueue_max - (self.class_Rides_instance[i].queue.qsize()*5)
                        self.ypos = (self.class_Rides_instance[i].yqueue_min+self.class_Rides_instance[i].yqueue_max)/2
        
    def plot_me(self, ax_left):  
        # If patrons meet exist range, then change state 
        if (self.class_Rides_instance[0].main_xexist_min <= self.xpos <= self.class_Rides_instance[0].main_xexist_max) \
       and (self.class_Rides_instance[0].main_yexist_min <= self.ypos <= self.class_Rides_instance[0].main_yexist_max):  
            self.artist = None
        else:    
            self.artist = ax_left.scatter(self.xpos, self.ypos, s=20, marker=self.marker,
                                          c=np.array([self.color]), cmap="hsv", zorder=2.5, vmin=0, vmax=1)
            ax_left.text(self.xpos+0.1, self.ypos+0.1, self.name, fontsize=7) 
            
