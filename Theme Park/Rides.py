#
# Author : Hyejin Song
# ID : 23310067
#
# Rides.py 
#    FerrisWheel(Rides) - FerrisWheel class set direction and movement, manage break, riding and queue
#    DropTower(Rides) - DropTower class set direction and movement, manage break, riding and queue
#    Hurricane(Rides) - Hurricane class set direction and movement, manage break, riding and queue
#    PirateShip(Rides) - PirateShip class set direction and movement, manage break, riding and queue
#
# Revisions: 
#    05/10/2025 – Base version for assignment
#    07/10/2025 – Version 2 (plot each rides, entrance, exist)
#    08/10/2025 – Version 3 (plot and manage queue)
#    09/10/2025 – Version 4 (add each rides step change and update state)
#    10/10/2025 – Version 5 (add each patron step change and update state)
#

from matplotlib.patches import Circle, Rectangle

import numpy as np
import random
import queue


class Rides():
    myclass = "Ride"
    state = "stop"   # stop riding    
        
    main_xboundary_min = 0
    main_xboundary_max = 350
    main_yboundary_min = 0
    main_yboundary_max = 350
    
    main_xentrance1_min = 0
    main_xentrance1_max = 10
    main_yentrance1_min = 0
    main_yentrance1_max = 50
    
    main_xentrance2_min = 0
    main_xentrance2_max = 10
    main_yentrance2_min = 300
    main_yentrance2_max = 350
    
    main_xexist_min = 340
    main_xexist_max = 350
    main_yexist_min = 0
    main_yexist_max = 50
           
    def __init__(self, name, xpos, ypos, width, height, ride_color, state, number_of_operations, number_of_patrons, price):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.ride_color = ride_color
        self.state = state
        
        self.number_of_operations = number_of_operations
        self.number_of_patrons = number_of_patrons
        self.price = price
        
        self.ride_xboundary_min = 0
        self.ride_xboundary_max = 0
        self.ride_yboundary_min = 0
        self.ride_yboundary_max = 0
        
        self.xqueue_min = 0
        self.xqueue_max = 0
        self.yqueue_min = 0
        self.yqueue_max = 0
        
        self.xexist = 0
        self.yexist_min = 0
        self.yexist_max = 0

    def plot_main_boundary_entrance_exit(self, ax_left):         
        ax_left.plot(np.array([self.main_xboundary_min, self.main_xboundary_min, self.main_xboundary_max, self.main_xboundary_max, self.main_xboundary_min]),np.array([self.main_yboundary_min, self.main_yboundary_max, self.main_yboundary_max, self.main_yboundary_min, self.main_yboundary_min]), color="dimgrey", linewidth=5)
        
        ax_left.add_patch(Rectangle((self.main_xentrance1_min,self.main_yentrance1_min), 10, 50, edgecolor="white", facecolor='white', linewidth=2))
        ax_left.text(7, 29, "Entrance1", horizontalalignment='center', verticalalignment='center', rotation='vertical', fontsize=7.5, color='black', fontweight='bold')
        
        ax_left.add_patch(Rectangle((self.main_xentrance2_min,self.main_yentrance2_min), 10, 50, edgecolor="white", facecolor='white', linewidth=2))
        ax_left.text(7, 329, "Entrance2", horizontalalignment='center', verticalalignment='center', rotation='vertical', fontsize=7.5, color='black', fontweight='bold')
        
        ax_left.add_patch(Rectangle((self.main_xexist_min,self.main_yexist_min), 10, 50, edgecolor="white", facecolor='white', linewidth=2))
        ax_left.text(345, 28, "Exist", horizontalalignment='center', verticalalignment='center', rotation='vertical', fontsize=8, color='black', fontweight='bold')
        
    def plot_each_ride_boundary(self, ax_left):
        frame_square = Rectangle((self.xpos-10,self.ypos-self.height), self.width+20, self.height, edgecolor="darkgray", facecolor='none', linewidth=1)      
        ax_left.add_patch(frame_square)
        
        self.ride_xboundary_min = self.xpos-10
        self.ride_xboundary_max = self.xpos+self.width+10
        self.ride_yboundary_min = self.ypos-self.height
        self.ride_yboundary_max = self.ypos
        
    def plot_each_ride_entrance_exit(self, ax_left):
        ax_left.plot(np.array([self.xpos-10, self.xpos-10]),np.array([self.ypos, self.ypos-15]), color="green", linewidth=5)
        
        self.xexist = self.xpos+self.width+10
        self.yexist_min = self.ypos-self.height
        self.yexist_max = self.ypos-self.height+15
        ax_left.plot(np.array([self.xexist, self.xexist]),np.array([self.yexist_min, self.yexist_max]), color="green", linewidth=5) 
          
    def plot_each_ride_queue(self, ax_left):       
        self.xqueue_min = self.xpos-50
        self.xqueue_max = self.xpos-10
        self.yqueue_min = self.ypos-15
        self.yqueue_max = self.ypos
        ax_left.fill(np.array([self.xqueue_min, self.xqueue_max, self.xqueue_max, self.xqueue_min]),np.array([self.yqueue_min, self.yqueue_min, self.yqueue_max, self.yqueue_max]), color="gainsboro")  
        
    def plot_ride(self, ax_left):
        pass
        
    def step_change(self, ax_left):
        pass                 
    

class FerrisWheel(Rides):
    myclass = "FerrisWheel"  
    direction = "O" 
    movements=["O","T"]
    # Traceability Matrix reference 2.0.5
    break_counts = 0
    break_times = 15
    riding_counts = 0
    riding_times = 16
    # Traceability Matrix reference 2.0.6
    queue = queue.Queue()
    qlimit = 8
    qpatrons_list = []
    line_o = []
    line_t = []
    
    def plot_each_ride_stand(self, ax_left):
        frame_A1_x = np.array([self.xpos+(self.width/4), self.xpos+(self.width/2), self.xpos+(self.width*3/4), self.xpos+(self.width/4)])
        frame_A1_y = np.array([self.ypos-self.height+5, self.ypos-(self.height/2), self.ypos-self.height+5, self.ypos-self.height+5])      
        ax_left.plot(frame_A1_x, frame_A1_y, color="dimgrey", linewidth=3)
        
        ax_left.scatter(self.xpos+(self.width/2), self.ypos-(self.height/2), s=100, c="dimgrey",  zorder=2.5)
        
        ax_left.add_patch(Circle((self.xpos+(self.width/2),self.ypos-(self.height/2)), radius=20, edgecolor=self.ride_color, facecolor='none', linewidth=3))
        ax_left.add_patch(Circle((self.xpos+(self.width/2),self.ypos-(self.height/2)), radius=33, edgecolor=self.ride_color, facecolor='none', linewidth=3))
        
    def step_change(self, ax_left):
        self.plot_ride_riding_step_change(ax_left)
        
        if self.state == "riding":
            if self.riding_counts < self.riding_times:
                self.plot_patron_riding_step_change()  
                self.riding_counts += 1
                if self.riding_counts % 2 == 0:
                    self.direction = self.movements[0]
                elif self.riding_counts % 2 == 1:
                    self.direction = self.movements[1]
            else:
                self.state = "stop"
                self.riding_counts = 0
                for index, item in enumerate(self.qpatrons_list):  
                    item.state = "roaming"
                    item.xpos = self.xexist + index
                    item.ypos = random.randint(self.yexist_min, self.yexist_max)
                    item.set_target_ride = ""
        else:
            self.break_counts += 1
            if self.break_counts == self.break_times:
                self.state = "riding"
                self.break_counts = 0
                self.number_of_operations += 1
                self.number_of_patrons += self.queue.qsize()
                
                self.qpatrons_list = []
                while not self.queue.empty():
                    patron = self.queue.get()
                    self.qpatrons_list.append(patron)
                    
                self.plot_patron_riding_step_change()     
                
    def plot_ride_riding_step_change(self, ax_left):
        if self.direction == "O":
            ax_left.add_patch(Rectangle((self.xpos+(self.width*9/10)-2.5,self.ypos-(self.height/2)-5), 11, 11, edgecolor="yellow", facecolor='yellow', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos,self.ypos-(self.height/2)-5), 11, 11, edgecolor="purple", facecolor='purple', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/2)-5,self.ypos-(self.height/4)+4), 11, 11, edgecolor="red", facecolor='red', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/2)-5,self.ypos-self.height+10), 11, 11, edgecolor="blue", facecolor='blue', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*3/4),self.ypos-(self.height/4)-5), 11, 11, edgecolor="orange", facecolor='orange', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*3/4)+2.5,self.ypos-(self.height*4/5)), 11, 11, edgecolor="green", facecolor='green', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/8)-0.5,self.ypos-(self.height/4)-5), 11, 11, edgecolor="deeppink", facecolor='deeppink', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/8)-0.5,self.ypos-(self.height*4/5)), 11, 11, edgecolor="navy", facecolor='navy', linewidth=3, zorder=2.5))
        
            # vertical -
            self.frame_line1_x = np.array([self.xpos+5, self.xpos+self.width-5])  
            self.frame_line1_y = np.array([self.ypos-(self.height/2), self.ypos-(self.height/2)]) 
            # horizontal |
            self.frame_line2_x = np.array([self.xpos+(self.width/2), self.xpos+(self.width/2)])  
            self.frame_line2_y = np.array([self.ypos-15, self.ypos-self.height+15]) 
            # left diagonal \
            self.frame_line3_x = np.array([self.xpos+(self.width*1/8)+5.5, self.xpos+(self.width*7/8)-2.5])  
            self.frame_line3_y = np.array([self.ypos-(self.height/4), self.ypos-(self.height*2/3)-5]) 
            # right diagonal /
            self.frame_line4_x = np.array([self.xpos+(self.width*7/8)-5.5, self.xpos+(self.width*1/8)+3.5])  
            self.frame_line4_y = np.array([self.ypos-(self.height/4), self.ypos-(self.height*2/3)-5])          
            self.line_o = ax_left.plot(self.frame_line1_x, self.frame_line1_y, self.frame_line2_x, self.frame_line2_y, self.frame_line3_x, self.frame_line3_y, self.frame_line4_x, self.frame_line4_y, color="dimgrey", linewidth=3)       
                    
        elif self.direction == "T":
            ax_left.add_patch(Rectangle((self.xpos+(self.width*5/6),self.ypos-(self.height*2/5)-2.5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*5/6),self.ypos-(self.height*2/3)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+2.5,self.ypos-(self.height*2/5)-2.5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+2.5,self.ypos-(self.height*2/3)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/4),self.ypos-(self.height*1/4)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/4),self.ypos-(self.height*9/10)+2.5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*2/3)-5,self.ypos-(self.height*1/4)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*2/3)-5,self.ypos-(self.height*9/10)+2.5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
        
            self.frame_line5_x = np.array([self.xpos+(self.width*1/6)-5, self.xpos+(self.width*7/8)])  
            self.frame_line5_y = np.array([self.ypos-(self.height*2/5)+2.5, self.ypos-(self.height/2)-9.5]) 
            self.frame_line6_x = np.array([self.xpos+(self.width/3), self.xpos+(self.width*2/3)])  
            self.frame_line6_y = np.array([self.ypos-(self.height/5), self.ypos-(self.height*4/5)])  
            self.frame_line7_x = np.array([self.xpos+(self.width*2/3), self.xpos+(self.width/3)])  
            self.frame_line7_y = np.array([self.ypos-(self.height/5), self.ypos-(self.height*4/5)]) 
            self.frame_line8_x = np.array([self.xpos+(self.width*5/6)+5, self.xpos+(self.width/6)-2.5])  
            self.frame_line8_y = np.array([self.ypos-(self.height/3)-2.5, self.ypos-(self.height*2/3)+5])                
            self.line_t = ax_left.plot(self.frame_line5_x, self.frame_line5_y, self.frame_line6_x, self.frame_line6_y, self.frame_line7_x, self.frame_line7_y, self.frame_line8_x, self.frame_line8_y, color="gray", linewidth=3) 

    def plot_patron_riding_step_change(self): 
        if self.direction == "O":
            ridePosition_o = [[self.line_o[1].get_xdata()[0], self.line_o[1].get_ydata()[0]],
                              [self.line_o[3].get_xdata()[0], self.line_o[3].get_ydata()[0]],
                              [self.line_o[0].get_xdata()[1], self.line_o[0].get_ydata()[1]],
                              [self.line_o[2].get_xdata()[1], self.line_o[2].get_ydata()[1]],
                              [self.line_o[1].get_xdata()[1], self.line_o[1].get_ydata()[1]],
                              [self.line_o[3].get_xdata()[1], self.line_o[3].get_ydata()[1]],
                              [self.line_o[0].get_xdata()[0], self.line_o[0].get_ydata()[0]],
                              [self.line_o[2].get_xdata()[0], self.line_o[2].get_ydata()[0]]]
            
            for index, item in enumerate(self.qpatrons_list):
                newpos = ((self.riding_counts//2)+index) % 8
                item.xpos = ridePosition_o[newpos][0]
                item.ypos = ridePosition_o[newpos][1]
                item.state = "riding"
                        
        elif self.direction == "T":
            ridePosition_p = [[self.line_t[2].get_xdata()[0], self.line_t[2].get_ydata()[0]],
                              [self.line_t[3].get_xdata()[0], self.line_t[3].get_ydata()[0]],
                              [self.line_t[0].get_xdata()[1], self.line_t[0].get_ydata()[1]],
                              [self.line_t[1].get_xdata()[1], self.line_t[1].get_ydata()[1]],
                              [self.line_t[2].get_xdata()[1], self.line_t[2].get_ydata()[1]],
                              [self.line_t[3].get_xdata()[1], self.line_t[3].get_ydata()[1]],
                              [self.line_t[0].get_xdata()[0], self.line_t[0].get_ydata()[0]],
                              [self.line_t[1].get_xdata()[0], self.line_t[1].get_ydata()[0]]] 
            
            for index, item in enumerate(self.qpatrons_list):
                newpos = ((self.riding_counts//2)+index) % 8
                item.xpos = ridePosition_p[newpos][0]
                item.ypos = ridePosition_p[newpos][1]
                item.state = "riding"
     

class DropTower(Rides):
    myclass = "DropTower"     
    direction = "S" 
    movements=["S","U","D"]  
    # Traceability Matrix reference 2.0.5
    break_counts = 0
    break_times = 10
    riding_counts = 0
    riding_times = 10
    # Traceability Matrix reference 2.0.6
    queue = queue.Queue()
    qlimit = 4
    qpatrons_list = []
    frame_square_x=np.empty(5)
    frame_square_y=np.empty(5) 
    
    def plot_each_ride_queue(self, ax_left):       
        self.xqueue_min = self.xpos-35
        self.xqueue_max = self.xpos-10
        self.yqueue_min = self.ypos-15
        self.yqueue_max = self.ypos
        ax_left.fill(np.array([self.xqueue_min, self.xqueue_max, self.xqueue_max, self.xqueue_min]),np.array([self.yqueue_min, self.yqueue_min, self.yqueue_max, self.yqueue_max]), color="gainsboro")      
    
    def plot_each_ride_stand(self, ax_left):
        frame_A_x = np.array([self.xpos+(self.width/2)-15, self.xpos+(self.width/2), self.xpos+(self.width/2)+15, self.xpos+(self.width/2)-15])
        frame_A_y = np.array([self.ypos-20, self.ypos, self.ypos-20, self.ypos-20])    
        ax_left.fill(frame_A_x, frame_A_y, color='limegreen', edgecolor="dimgrey", linewidth=2)
           
        frame_f1_x = np.array([self.xpos+(self.width/2)-15, self.xpos+(self.width/4)])        
        frame_f2_x = np.array([self.xpos+(self.width/2), self.xpos+(self.width/2)])        
        frame_f3_x = np.array([self.xpos+(self.width/2)+15, self.xpos+(self.width*3/4)])
        frame_f_y = np.array([self.ypos-(self.height*4/5), self.ypos-self.height])
        ax_left.fill(frame_f1_x, frame_f_y, frame_f2_x, frame_f_y, frame_f3_x, frame_f_y, edgecolor="dimgrey", linewidth=2)
            
        square = Rectangle((self.xpos+(self.width/2)-15,self.ypos-(self.height*4/5)), 30, 60, edgecolor="dimgrey", facecolor='limegreen', linewidth=2)
        ax_left.add_patch(square)
    
    def plot_ride(self, ax_left):       
        if self.state != "riding":
            self.frame_square_x =np.array([self.xpos+(self.width/2)-15, self.xpos+(self.width/2)-15, self.xpos+(self.width/2)+15, self.xpos+(self.width/2)+15, self.xpos+(self.width/2)-15])
            self.frame_square_y = np.array([self.ypos-(self.height*4/5), self.ypos-(self.height*7/10), self.ypos-(self.height*7/10), self.ypos-(self.height*4/5), self.ypos-(self.height*4/5)])

    def step_change(self, ax_left):
        self.plot_ride_riding_step_change(ax_left) 
        
        if self.state == "riding":
            if self.riding_counts < self.riding_times:
                self.plot_patron_riding_step_change()
                self.riding_counts += 1
                if self.riding_counts <= 5:
                    self.direction = self.movements[1]
                else:
                    self.direction = self.movements[2]
            else:
                self.state = "stop"
                self.riding_counts = 0
                self.direction = self.movements[0]
                # patron get out DropTower
                for index, item in enumerate(self.qpatrons_list):  
                    item.state = "roaming"
                    item.xpos = self.xexist + index
                    item.ypos = random.randint(self.yexist_min, self.yexist_max)
                    item.set_target_ride = ""
        else:
            self.break_counts += 1
            
            if self.break_counts == self.break_times:
                self.state = "riding"
                self.break_counts = 0
                self.number_of_operations += 1
                
                self.number_of_patrons += self.queue.qsize()
                
                self.qpatrons_list = []
                while not self.queue.empty():
                    patron = self.queue.get()
                    self.qpatrons_list.append(patron)
                
                self.plot_patron_riding_step_change()  
               
    def plot_ride_riding_step_change(self, ax_left):   
        if self.direction == "U":
            self.frame_square_y = self.frame_square_y+10
        elif self.direction == "D":
            self.frame_square_y = self.frame_square_y-10
        
        ax_left.fill(self.frame_square_x, self.frame_square_y, color=self.ride_color, edgecolor="dimgrey", linewidth=2.5, zorder=2.5)     

    def plot_patron_riding_step_change(self):
        newxpos = [(self.xpos+(self.width/2)-15) + (i*6) for i in range(1,5)]
        newypos = self.ypos-(self.height*3/4)
        
        if self.direction == "S":
            for index, item in enumerate(self.qpatrons_list):
                item.xpos = newxpos[index]
                item.ypos = newypos
                item.state = "stop"
        elif self.direction == "U":
            for index, item in enumerate(self.qpatrons_list):
                item.xpos = newxpos[index]
                item.ypos += 10
                item.state = "riding"
        elif self.direction == "D":
            for index, item in enumerate(self.qpatrons_list):
                item.xpos = newxpos[index]
                item.ypos -= 10
                item.state = "riding"
        

class Hurricane(Rides):
    myclass = "Hurricane"    
    direction = "O" 
    movements=["O","T"]
    # Traceability Matrix reference 2.0.5
    break_counts = 0
    break_times = 10
    riding_counts = 0
    riding_times = 16
    # Traceability Matrix reference 2.0.6
    queue = queue.Queue()
    qlimit = 8
    qpatrons_list = []
    line_o = []
    line_t = []

    def plot_each_ride_stand(self, ax_left):
        ax_left.scatter(self.xpos+(self.width/2), self.ypos-(self.height/2), s=100, c="dimgrey", zorder=2.5)       
    
    def step_change(self, ax_left):
        self.plot_ride_riding_step_change(ax_left)
        
        if self.state == "riding":
            if self.riding_counts < self.riding_times:
                self.plot_patron_riding_step_change()   
                self.riding_counts += 1  
                if self.riding_counts % 2 == 0:
                    self.direction = self.movements[0]
                elif self.riding_counts % 2 == 1:
                    self.direction = self.movements[1]
            else:
                self.state = "stop"
                self.riding_counts = 0
                
                for index, item in enumerate(self.qpatrons_list):  
                    item.state = "roaming"
                    item.xpos = self.xexist + index
                    item.ypos = random.randint(self.yexist_min, self.yexist_max)
                    item.set_target_ride = ""
        else: 
            self.break_counts += 1

            if self.break_counts == self.break_times:
                self.state = "riding"
                self.break_counts = 0
                self.number_of_operations += 1
                self.number_of_patrons += self.queue.qsize()
                
                self.qpatrons_list = []
                while not self.queue.empty():
                    patron = self.queue.get()
                    self.qpatrons_list.append(patron)
                
                self.plot_patron_riding_step_change()    
            
    def plot_ride_riding_step_change(self, ax_left):
        if self.direction == "O":
            ax_left.add_patch(Rectangle((self.xpos+self.width-5,self.ypos-(self.height/2)-5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos-5,self.ypos-(self.height/2)-5), 11, 11, edgecolor="dodgerblue", facecolor='dodgerblue', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/2)-5,self.ypos-(self.height/5)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/2)-5,self.ypos-self.height+7.5), 11, 11, edgecolor="dodgerblue", facecolor='dodgerblue', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*7/8)-5,self.ypos-(self.height/4)-5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*7/8)-5,self.ypos-(self.height*3/4)-2.5), 11, 11, edgecolor="dodgerblue", facecolor='dodgerblue', linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/8)-5,self.ypos-(self.height/4)-5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*1/8)-5,self.ypos-(self.height*3/4)-2.5), 11, 11, edgecolor="dodgerblue", facecolor='dodgerblue', linewidth=3, zorder=2.5))
        
            # vertical -
            self.frame_line1_x = np.array([self.xpos, self.xpos+self.width])  
            self.frame_line1_y = np.array([self.ypos-(self.height/2), self.ypos-(self.height/2)]) 
            # horizontal |
            self.frame_line2_x = np.array([self.xpos+(self.width/2), self.xpos+(self.width/2)])  
            self.frame_line2_y = np.array([self.ypos-15, self.ypos-self.height+15]) 
            # left diagonal \
            self.frame_line3_x = np.array([self.xpos+(self.width*1/8), self.xpos+(self.width*7/8)])  
            self.frame_line3_y = np.array([self.ypos-(self.height/4), self.ypos-(self.height*2/3)-5]) 
            # right diagonal /
            self.frame_line4_x = np.array([self.xpos+(self.width*7/8), self.xpos+(self.width*1/8)])  
            self.frame_line4_y = np.array([self.ypos-(self.height/4), self.ypos-(self.height*2/3)-5])                
            self.line_o = ax_left.plot(self.frame_line1_x, self.frame_line1_y, self.frame_line2_x, self.frame_line2_y, self.frame_line3_x, self.frame_line3_y, self.frame_line4_x, self.frame_line4_y, color="dimgrey", linewidth=3)
            
        elif self.direction == "T":
            ax_left.add_patch(Rectangle((self.xpos-2.5,self.ypos-(self.height*2/3)), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos-2.5,self.ypos-(self.height*2/5)-2.5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/4),self.ypos-(self.height/4)+2.5), 11, 11, edgecolor="dodgerblue", facecolor="dodgerblue", linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width/4),self.ypos-(self.height*5/6)-5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*3/5)+2.5,self.ypos-(self.height/4)+2.5), 11, 11, edgecolor="dodgerblue", facecolor="dodgerblue", linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*3/5)+2.5,self.ypos-(self.height*5/6)-5), 11, 11, edgecolor=self.ride_color, facecolor=self.ride_color, linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*9/10),self.ypos-(self.height*2/3)), 11, 11, edgecolor="dodgerblue", facecolor="dodgerblue", linewidth=3, zorder=2.5))
            ax_left.add_patch(Rectangle((self.xpos+(self.width*9/10),self.ypos-(self.height*2/5)-2.5), 11, 11, edgecolor="dodgerblue", facecolor="dodgerblue", linewidth=3, zorder=2.5))

            self.frame_line5_x = np.array([self.xpos+5, self.xpos+(self.width)-5])  
            self.frame_line5_y = np.array([self.ypos-(self.height*2/5)+2.5, self.ypos-(self.height*3/5)]) 
            self.frame_line6_x = np.array([self.xpos+5, self.xpos+(self.width)-5])  
            self.frame_line6_y = np.array([self.ypos-(self.height*3/5), self.ypos-(self.height*2/5)+2.5]) 
            self.frame_line7_x = np.array([self.xpos+(self.width*3/4)-5, self.xpos+(self.width*1/4)+5])  
            self.frame_line7_y = np.array([self.ypos-(self.height/5), self.ypos-(self.height*4/5)])    
            self.frame_line8_x = np.array([self.xpos+(self.width*3/4)-5, self.xpos+(self.width*1/4)+5])  
            self.frame_line8_y = np.array([self.ypos-(self.height*4/5), self.ypos-(self.height/5)]) 
            self.line_t = ax_left.plot(self.frame_line5_x, self.frame_line5_y, self.frame_line6_x, self.frame_line6_y, self.frame_line7_x, self.frame_line7_y, self.frame_line8_x, self.frame_line8_y, color="dimgrey", linewidth=3)
            
    def plot_patron_riding_step_change(self): 
        if self.direction == "O":            
            ridePosition_o = [[self.line_o[1].get_xdata()[0], self.line_o[1].get_ydata()[0]],
                          [self.line_o[3].get_xdata()[0], self.line_o[3].get_ydata()[0]],
                          [self.line_o[0].get_xdata()[1], self.line_o[0].get_ydata()[1]],
                          [self.line_o[2].get_xdata()[1], self.line_o[2].get_ydata()[1]],
                          [self.line_o[1].get_xdata()[1], self.line_o[1].get_ydata()[1]],
                          [self.line_o[3].get_xdata()[1], self.line_o[3].get_ydata()[1]],
                          [self.line_o[0].get_xdata()[0], self.line_o[0].get_ydata()[0]],
                          [self.line_o[2].get_xdata()[0], self.line_o[2].get_ydata()[0]]]
            
            for index, item in enumerate(self.qpatrons_list):
                newpos = ((self.riding_counts//2)+index) % 8
                item.xpos = ridePosition_o[newpos][0]
                item.ypos = ridePosition_o[newpos][1]
                item.state = "riding"
                        
        elif self.direction == "T":
            ridePosition_p = [[self.line_t[2].get_xdata()[0], self.line_t[2].get_ydata()[0]],
                          [self.line_t[1].get_xdata()[1], self.line_t[1].get_ydata()[1]],
                          [self.line_t[0].get_xdata()[1], self.line_t[0].get_ydata()[1]],
                          [self.line_t[3].get_xdata()[0], self.line_t[3].get_ydata()[0]],
                          [self.line_t[2].get_xdata()[1], self.line_t[2].get_ydata()[1]],
                          [self.line_t[1].get_xdata()[0], self.line_t[1].get_ydata()[0]],
                          [self.line_t[0].get_xdata()[0], self.line_t[0].get_ydata()[0]],
                          [self.line_t[3].get_xdata()[1], self.line_t[3].get_ydata()[1]]] 
            
            for index, item in enumerate(self.qpatrons_list):
                newpos = ((self.riding_counts//2)+index) % 8
                item.xpos = ridePosition_p[newpos][0]
                item.ypos = ridePosition_p[newpos][1]
                item.state = "riding"


class PirateShip(Rides):
    myclass = "PirateShip"     
    direction = "C" 
    movements=["CL","LR","RC"]
    # Traceability Matrix reference 2.0.5
    break_counts = 0
    break_times = 20
    riding_counts = 0
    riding_times = 19
    # Traceability Matrix reference 2.0.6
    queue = queue.Queue()
    qlimit = 5
    qpatrons_list = []
    line_rotate = []
    frame_ship1_x=np.empty(3)
    frame_ship1_y=np.empty(3)
    frame_ship2_x=np.empty(4)
    frame_ship2_y=np.empty(4)
    frame_ship3_y=np.empty(4)
    fill_bottom_x=np.empty(7)
    fill_bottom_y=np.empty(7)
    
    def plot_each_ride_queue(self, ax_left):       
        self.xqueue_min = self.xpos-40
        self.xqueue_max = self.xpos-10
        self.yqueue_min = self.ypos-15
        self.yqueue_max = self.ypos
        ax_left.fill(np.array([self.xqueue_min, self.xqueue_max, self.xqueue_max, self.xqueue_min]),np.array([self.yqueue_min, self.yqueue_min, self.yqueue_max, self.yqueue_max]), color="gainsboro") 
        
    def plot_each_ride_stand(self, ax_left):
        frame_A1_x = np.array([self.xpos, self.xpos+(self.width/2), self.xpos+self.width])
        frame_A1_y = np.array([self.ypos-self.height, self.ypos, self.ypos-self.height])
        frame_A2_x = np.array([self.xpos+(self.width*1/4), self.xpos+(self.width*3/4)])
        frame_A2_y = np.array([self.ypos-(3*self.height/5), self.ypos-(3*self.height/5)])      
        ax_left.plot(frame_A1_x, frame_A1_y, frame_A2_x, frame_A2_y, color="dimgrey", linewidth=3)
        
        ax_left.scatter(self.xpos+(self.width/2), self.ypos, s=50, c="dimgrey", zorder=2.5)    
        
    def plot_ride(self, ax_left):        
        self.frame_ship1_x = np.array([self.xpos, self.xpos+(self.width/2), self.xpos+self.width])
        self.frame_ship1_y = np.array([self.ypos-(self.height/3), self.ypos, self.ypos-(self.height/3)])
        self.frame_ship2_x = np.array([self.xpos, self.xpos+(self.width*3/10), self.xpos+(self.width*7/10), self.xpos+self.width])
        self.frame_ship2_y = np.array([self.ypos-(self.height/3), self.ypos-(self.height/2), self.ypos-(self.height/2), self.ypos-(self.height/3)])
        self.frame_ship3_y = np.array([self.ypos-(self.height/3), self.ypos-(self.height*4/5), self.ypos-(self.height*4/5), self.ypos-(self.height/3)])
        
        self.fill_bottom_x = np.array([self.xpos, self.xpos+(self.width*3/10), self.xpos+(self.width*7/10), self.xpos+self.width, self.xpos+(self.width*7/10), self.xpos+(self.width*3/10), self.xpos])
        self.fill_bottom_y = np.array([self.ypos-(self.height/3), self.ypos-(self.height/2), self.ypos-(self.height/2), self.ypos-(self.height/3), self.ypos-(self.height*4/5), self.ypos-(self.height*4/5), self.ypos-(self.height/3)])
        

    def step_change(self, ax_left):
        self.plot_ride_riding_step_change(ax_left)
    
        if self.state == "riding":
            if self.riding_counts < self.riding_times:
                self.plot_patron_riding_step_change() 
                
                # Change movement according to riding_counts
                self.riding_counts += 1 
            
                if (self.riding_counts % 20) < 5:
                    self.direction = self.movements[0]  # CL (Center to Left)
                elif (self.riding_counts % 20) < 15:
                    self.direction = self.movements[1]  # LR (Left to Right)
                else:
                    self.direction = self.movements[2]  # RC (Right to Center)
            else: 
                self.state = "stop"
                self.direction = "C"
                self.riding_counts = 0
            
                # Move patron's position in front of ride's exist
                for index, item in enumerate(self.qpatrons_list):  
                    item.state = "roaming"
                    item.xpos = self.xexist + index
                    item.ypos = random.randint(self.yexist_min, self.yexist_max)
                    item.set_target_ride = ""
        else: 
            self.break_counts += 1
            if self.break_counts == self.break_times:
                self.state = "riding"
                self.break_counts = 0
                self.number_of_operations += 1
                self.number_of_patrons += self.queue.qsize()
                
                self.qpatrons_list = []
                while not self.queue.empty():
                    patron = self.queue.get()
                    self.qpatrons_list.append(patron)
                
                self.plot_patron_riding_step_change() 
    
    # Rotate the coordinate(xs, ys) by an angle relative to a pivot point
    def rotate_points(self, xs, ys, pivot, angle):
        px, py = pivot if isinstance(pivot, (tuple, list)) else (pivot, pivot)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        xs, ys = np.array(xs), np.array(ys)
        # Shift coordinate relative to a pivot
        x_shifted, y_shifted = xs - px, ys - py
        x_rotate = cos_a * x_shifted - sin_a * y_shifted + px
        y_rotate = sin_a * x_shifted + cos_a * y_shifted + py
        
        return x_rotate, y_rotate  
          
    def plot_ride_riding_step_change(self, ax_left):
        pivot = (self.xpos + self.width/2, self.ypos)

        # Calculate swing angle based on riding_counts
        if self.direction == "C":  # Center
            angle = 0
        elif self.direction == "CL":  # Center to Left
            angle = np.deg2rad(np.linspace(0, -15, 5)[self.riding_counts]) 
        elif self.direction == "LR":  # Left to Right
            angle = np.deg2rad(np.linspace(-15, 15, 10)[self.riding_counts - 5])
        elif self.direction == "RC":  # Right to Center
            angle = np.deg2rad(np.linspace(15, 0, 5)[self.riding_counts - 15])

        # Rotate 3 frames of pirate ship
        xs1, ys1 = self.rotate_points(self.frame_ship1_x, self.frame_ship1_y, pivot, angle)
        xs2, ys2 = self.rotate_points(self.frame_ship2_x, self.frame_ship2_y, pivot, angle)
        xs3, ys3 = self.rotate_points(self.frame_ship2_x, self.frame_ship3_y, pivot, angle)
        xs4, ys4 = self.rotate_points(self.fill_bottom_x, self.fill_bottom_y, pivot, angle)

        # Plot pirate ship using rotated coordinate
        self.line_rotate = ax_left.plot(xs1, ys1, xs2, ys2, xs3, ys3, color=self.ride_color, linewidth=3)
        ax_left.fill(xs4, ys4, color=self.ride_color, zorder=2.5, alpha=0.9)
   
    def plot_patron_riding_step_change(self): 
        xmove = (self.line_rotate[1].get_xdata()[2] - self.line_rotate[1].get_xdata()[1]) / self.qlimit
        ymove = (self.line_rotate[1].get_ydata()[2] - self.line_rotate[1].get_ydata()[1]) / self.qlimit

        for index, item in enumerate(self.qpatrons_list):
            item.xpos = self.line_rotate[1].get_xdata()[1] + (index*xmove)
            item.ypos = self.line_rotate[1].get_ydata()[1] + (index*ymove)
            item.state = "riding"
                             
                  
