
# Author : Hyejin Song
# ID : 23310067
#
# Statistics.py 
#    LinePlot(Statistics) - plot line graph about 'Each Ride Profits Per Time Stamp'
#    TablePlot(Statistics) - plot table about '# Operations', '# Patrons', 'Price', '# Profit'
#    ScatterPlot(Statistics) - Plot scatter graph about 'Patrons movement'
#
# Revisions: 
#    09/10/2025 – Base version for assignment
#    10/10/2025 – Version 2 (add ScatterPlot)
#

import matplotlib.pyplot as plt
import numpy as np

class Statistics():
    myclass = "Statistics"
    
    def __init__(self, ferryWheel_color, dropTower_color, hurricane_color, pirateShip_color, number_of_ride):   
        self.ferryWheel_color = ferryWheel_color 
        self.dropTower_color = dropTower_color 
        self.hurricane_color = hurricane_color 
        self.pirateShip_color = pirateShip_color
        self.number_of_ride = number_of_ride
          
        self.time_list = []
        self.ferrisWheel_list = []
        self.dropTower_list = []
        self.hurricane_list = []
        self.pirate_list = [] 
     
    def set_each_time_info(self, time, name, number_of_operations, number_of_patrons, price):            
        if name == "FerryWheel":
            self.time_list.append(time)
            self.ferrisWheel_list.append(number_of_patrons*price)
        elif name == "DropTower":
            self.dropTower_list.append(number_of_patrons*price)
        elif name == "Hurricane":
            self.hurricane_list.append(number_of_patrons*price)
        elif name == "PirateShip":
            self.pirate_list.append(number_of_patrons*price) 
     

class LinePlot(Statistics): 
    myclass = "LinePlot"    
        
    def plot_each_ride_profit(self, ax_center_top): 
        ax_center_top.plot(self.time_list, self.ferrisWheel_list, color=self.ferryWheel_color, label='FerryWheel') 
        ax_center_top.plot(self.time_list, self.dropTower_list, color=self.dropTower_color, label='DropTower') 
        
        if self.number_of_ride == 3:
            ax_center_top.plot(self.time_list, self.hurricane_list, color=self.hurricane_color, label='Hurricane') 
        elif self.number_of_ride == 4:
            ax_center_top.plot(self.time_list, self.hurricane_list, color=self.hurricane_color, label='Hurricane') 
            ax_center_top.plot(self.time_list, self.pirate_list, color=self.pirateShip_color, label='PirateShip') 
        
        ax_center_top.set_title("Each Ride Profits Per Time Stamp", fontsize = 10)
        ax_center_top.set_xlabel("Time (seconds)")
        ax_center_top.set_ylabel("Profit ($ AUD)")      
        ax_center_top.legend()


class TablePlot(Statistics):    
    myclass = "TablePlot"   
    columns = ['# Operations', '# Patrons', 'Price', '# Profit']
    rows = []

    def __init__(self, ferryWheel_color, dropTower_color, hurricane_color, pirateShip_color, number_of_ride):
        super().__init__(ferryWheel_color, dropTower_color, hurricane_color, pirateShip_color, number_of_ride)  
        self.table_data = [[0 for _ in range(4)] for _ in range(self.number_of_ride)]
        
    def set_each_time_info(self, class_Rides_instance):   
        self.rows.clear() 
        for index, item in enumerate(class_Rides_instance):
            self.rows.append(item.name)
            self.table_data[index][0] = item.number_of_operations
            self.table_data[index][1] = item.number_of_patrons
            self.table_data[index][2] = "$" + str(item.price) + " AUD"
            self.table_data[index][3] = "$" + str(item.number_of_patrons * item.price) + " AUD"
      
    def plot_all_ride_info(self, ax_center_bottom):
        rowColours_list = [self.ferryWheel_color, self.dropTower_color]
        if self.number_of_ride == 3:
            rowColours_list.append(self.hurricane_color)
        elif self.number_of_ride == 4:
            rowColours_list.append(self.hurricane_color)
            rowColours_list.append(self.pirateShip_color)

        # Add a table at the bottom of the axes.
        table = ax_center_bottom.table(cellText=self.table_data,
                          rowLabels=self.rows,
                          colLabels=self.columns,
                          rowColours=rowColours_list,
                          colColours=['lightsteelblue','lightsteelblue','lightsteelblue','lightsteelblue'],
                          bbox=[0, -0.1, 1, 0.8])  # x0, y0, width, height
        table.set_zorder(0)
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        
        
class ScatterPlot(Statistics):
    myclass = "ScatterPlot"
    
    def __init__(self):
        self.colorbar = None
        self.scatter_plot = None
    
    def plot_patrons_movement(self, ax_right, hist_posx, hist_posy, fig):
        # Set color value
        c = np.random.rand(len(hist_posx))
        
        # Create and update scatter object. 
        if self.scatter_plot is None:
            self.scatter_plot = ax_right.scatter(hist_posx, hist_posy, c=c, cmap='nipy_spectral', s=3, alpha=0.5)
        else:
            self.scatter_plot.set_offsets(np.c_[hist_posx, hist_posy])
            self.scatter_plot.set_array(c)
        
        # Create colorbar object.
        if self.colorbar is None:
            self.colorbar = fig.colorbar(self.scatter_plot, ax=ax_right)
            self.colorbar.set_label('Color Value')

        ax_right.set_xlim(0, 350)
        ax_right.set_ylim(0, 450)
        ax_right.set_title('Patrons movement', fontsize = 10)

       
