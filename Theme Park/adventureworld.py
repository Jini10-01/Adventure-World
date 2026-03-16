#
# Author : Hyejin Song
# ID : 23310067
#
# adventureworld.py - driver program to simulate ButtonControl.py, Patrons.py, Rides.py, Statistics.py and Terrains.py 
#                     2 mode(interactive mode and batch mode) and error handling
#                     after timestamp, save 'Adventureworld Statistics YYYY-mm-dd_HH:MM:SS.png' image
#
# Revisions: 
#    05/10/2025 – Base version for assignment
#    06/10/2025 – Version 2 (add and show Rides Class)
#    07/10/2025 – Version 2 (add and show Patrons, Terrains Class)
#    08/10/2025 – Version 3 (set interactive mode and batch mode, add error handling)
#    09/10/2025 – Version 3 (add and show Statistics, ButtonControl Class)
#    10/10/2025 – Version 3 (modify Statistics, ButtonControl Class)
#

from Terrains import Terrains, Pond
from Rides import Rides, FerrisWheel, DropTower, Hurricane, PirateShip
from Patrons import Patrons
from Statistics import Statistics, LinePlot, TablePlot, ScatterPlot
from ButtonControl import SpeedControl, WeatherControl

import random
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button

import sys
import csv
import pandas as pd
import names
from datetime import datetime

# Check the color entered by the user(interactive mode) or csv file(batch mode).
def ride_color_check(mode, params, param_num, ride_name, dride_color):
    if mode == "interactive":
        ride_color = input('Enter color for "'+ride_name+'" (Y=yellow, O=orange, H=hotpink, P=purple, B=blue)... ').upper() 
    else:
        ride_color = params[param_num]  
    if ride_color == "":
        ride_color = dride_color
    else:    
        while (ride_color != "Y" and ride_color != "O" and ride_color != "H" and ride_color != "P" and ride_color != "B" and ride_color != ""):
            print("Unexpected value, please re-enter...")
            ride_color = input('Enter color for "'+ride_name+'" (Y=yellow, O=orange, H=hotpink, P=purple, B=blue)... ').upper() 
            if ride_color == "":
                ride_color = dride_color
        if(ride_color == 'Y'):
            ride_color = 'yellow'
        elif(ride_color == 'O'):
            ride_color = 'orange'
        elif(ride_color == 'H'):
            ride_color = 'hotpink'
        elif(ride_color == 'P'):
            ride_color = 'purple'
        elif(ride_color == 'B'):
            ride_color = 'blue'
        elif(ride_color == ""):
            ride_color = dride_color   
            
    return ride_color      
       
# Check the parameters entered by the user(interactive mode) or csv file(batch mode).
def input_check_param(mode, dtimestamp, dpatrons, ddropTower_color, dferryWheel_color, params):
    if mode == "interactive":
        timestamp = input("Enter number of Timestamp (200 - 500) :  ")
    else:
        timestamp = params[0]
    if timestamp == "":
        timestamp = dtimestamp
    else:
        while int(timestamp) < 200 or int(timestamp) > 500:
            print("Out of range, please re-enter...")
            timestamp = input("Enter number of Timestamps (200 - 500) :  ")
            if timestamp == "":
                timestamp = dtimestamp

    if mode == "interactive":
        patrons = input("Enter number of Patrons (10 - 30) :  ")
    else:
        patrons = params[1]        
    if patrons == "":
        patrons = dpatrons
    else:
        while int(patrons) < 10 or int(patrons) > 30:
            print("Out of range, please re-enter...")
            patrons = input("Enter number of Patrons (10 - 30) :  ")
            if patrons == "":
                patrons = dpatrons
    
    ferryWheel_color = ride_color_check(mode, params, 2, "Ferry Wheel", dferryWheel_color)      
    dropTower_color = ride_color_check(mode, params, 3, "Drop Tower", ddropTower_color) 
        
    return int(timestamp), int(patrons), dropTower_color, ferryWheel_color                             

# Traceability Matrix reference 2.0.4
# Check the parameters entered by the scenario batch mode.
def input_check_scenario_param(ddropTower_color, dferryWheel_color, params):
    timestamp = params[0]     
    patrons = params[1]        
    number_of_ride = params[2]    
    dropTower_color = ddropTower_color
    ferryWheel_color = dferryWheel_color
        
    return int(timestamp), int(patrons), int(number_of_ride), dropTower_color, ferryWheel_color 

# Set Patrons object. 
def set_patrons(state, number_of_patrons, rand_start, rand_end, start_posx, start_posy, rides_list, pond):
    patrons_list = []  
    cList = []
    # circle, triangle, square, star, diamond
    shapes = ['o', '^', 's', '*', 'D']
   
    for i in range(number_of_patrons):
        color = np.random.rand()
        cList.append(color)
        random_markers = random.choice(shapes)
        
        name = names.get_first_name()
        if state == "new":
            if i < number_of_patrons/2:
                set_target_ride = random.randint(rand_start, rand_end) 
            else:
                set_target_ride = "" 
        else:
            set_target_ride = random.randint(1,1)     

        patron = Patrons(start_posx, start_posy, name, "roaming", color, random_markers, set_target_ride, rides_list, pond)
        patrons_list.append(patron)

    return patrons_list
    


def main():
    # Set default values.
    dtimestamp = 300
    dpatrons = 20
    dferryWheel_color = "hotpink" 
    ddropTower_color = "orange" 
    dhurricane_color = "blue"
    dpirateShip_color = "purple"
    total_number_of_patrons = 0
    scenario = False
    
    
    # Handels 2 modes and variables. - arg : -i(interactive mode) / -f(batch mode - Hmap(sky, ground) csv) / -p(batch mode - parameter csv)
    # Handles missing file(s)
    argvs = sys.argv[1:]
    for i, arg in enumerate(argvs):
        if arg == "-i":
            timestamp, patrons, dropTower_color, ferryWheel_color = input_check_param("interactive", dtimestamp, dpatrons, ddropTower_color, dferryWheel_color, [])       
            filename = "map_mix"
            color_map = pd.read_csv(filename+".csv").to_numpy(dtype=int)
            terrains = Terrains(color_map, filename)   
        elif arg == "-f": 
            try:
                color_map = pd.read_csv(argvs[i+1]).to_numpy(dtype=int)
                filename = argvs[i+1].split(".csv")[0]
                terrains = Terrains(color_map, filename)  
            except FileNotFoundError as err:
                print("!!!!! Can't find file. Use default map !!!!!")
                print("Error Type : "+str(type(err)))
                print("Error Message : "+str(err))
                filename = "map_mix"
                color_map = pd.read_csv(filename+".csv").to_numpy(dtype=int)
                terrains = Terrains(color_map, filename)                
        elif arg == "-p":
            params = []
            
            if argvs[i+1].startswith("scenario"):
                scenario = True
                try:
                    with open(argvs[i+1], 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            params.append(row[0])
                        timestamp, patrons, number_of_ride, dropTower_color, ferryWheel_color = input_check_scenario_param(ddropTower_color, dferryWheel_color, params)   
                except FileNotFoundError as err:
                    print("!!!!! Can't find file !!!!!")
                    print("!!!!! If you want to run the scenario file, check the file name again !!!!!")
                    print("Error Type : "+str(type(err)))
                    print("Error Message : "+str(err))   
                    sys.exit(1)     
            else:
                try:
                    with open(argvs[i+1], 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            try:
                                if len(row) == 0 or row == "":
                                    params.append("")
                                else:
                                    params.append(row[0])
                            except IndexError as err:
                                print("!!!!! list index out of range !!!!!")
                                print("Error Type : "+str(type(err)))
                                print("Error Message : "+str(err))
                    while len(params) < 4:
                        params.append("")                      
                    timestamp, patrons, dropTower_color, ferryWheel_color = input_check_param("batch", dtimestamp, dpatrons, ddropTower_color, dferryWheel_color, params)
                except FileNotFoundError as err:
                    print("!!!!! Can't find file. Use default parameters !!!!!")
                    print("Error Type : "+str(type(err)))
                    print("Error Message : "+str(err))
                    timestamp, patrons, dropTower_color, ferryWheel_color = input_check_param("batch", dtimestamp, dpatrons, ddropTower_color, dferryWheel_color, ["", "", "", ""])
            
    
    # Set Pond object.
    pond = Pond(300, 350, 50, 40)
    
    
    # Set each Rides object.          
    rides_list = []      
    ferrisWheel = FerrisWheel("FerryWheel", 75, 275, 80, 100, ferryWheel_color, "stop", 0, 0, 16)
    dropTower = DropTower("DropTower", 220, 275, 80, 100, dropTower_color, "stop", 0, 0, 10)
    hurricane = Hurricane("Hurricane", 75, 150, 80, 100, dhurricane_color, "stop", 0, 0, 16)
    pirate = PirateShip("PirateShip", 220, 150, 80, 100, dpirateShip_color, "stop", 0, 0, 19)
    
    rides_list.append(ferrisWheel)  
    rides_list.append(dropTower)
    
    # Traceability Matrix reference 2.0.4
    if scenario:
        if number_of_ride == 3:
            rides_list.append(hurricane)
        elif number_of_ride == 4:
            rides_list.append(hurricane)
            rides_list.append(pirate)
    else:
        number_of_ride = 4
        rides_list.append(hurricane)
        rides_list.append(pirate)
    
    
    # Set Patrons object.   
    patrons_list = set_patrons("new", patrons, 0, number_of_ride-1, 0, 0, rides_list, pond)  
    total_number_of_patrons += len(patrons_list)   
    hist_posx = [] 
    hist_posy = []


    # Interactive mode on.     
    plt.ion() 
    
    fig = plt.figure(figsize=(16, 6))
    
    # Traceability Matrix reference 6.0.1
    # Set 1 row, 3 columns on the grid.
    gs = gridspec.GridSpec(1, 3, figure=fig, width_ratios=[4.5, 2.4, 2.3], wspace=0.2)
    ax_left = plt.subplot(gs[0,0])
    ax_right = plt.subplot(gs[0,2])
    
    # Set 2 rows, 1 column on the right side grid.
    right = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[0, 1], height_ratios=[3, 2], hspace=0.05)
    ax_center_top = plt.subplot(right[0,0])
    ax_center_bottom = plt.subplot(right[1,0])

    plt.suptitle("2025 S2 FOP Assignment 23310067 Hyejin Song")

    # Traceability Matrix reference 2.0.4
    # Set Statistics object.
    statistics_line_plot = LinePlot(ferryWheel_color, dropTower_color, dhurricane_color, dpirateShip_color, number_of_ride)     
    statistics_table_plot = TablePlot(ferryWheel_color, dropTower_color, dhurricane_color, dpirateShip_color, number_of_ride)  
    statistics_scatter_plot = ScatterPlot()
    
    
    # Traceability Matrix reference 5.0
    # Set Button object.
    btn_speed = SpeedControl(2.5, 0.05, 0.5) 
    btn_speed_up = plt.axes([0.05, 0.95, 0.05, 0.035])  # [left, bottom, width, height]
    btn_speed_up = Button(btn_speed_up, 'Speed +', color='lightpink', hovercolor='darkgrey')
    btn_speed_up.on_clicked(btn_speed.speed_up)
    
    btn_speed_down = plt.axes([0.05, 0.9, 0.05, 0.035])
    btn_speed_down = Button(btn_speed_down, 'Speed -', color='lightpink', hovercolor='darkgrey')
    btn_speed_down.on_clicked(btn_speed.speed_down)
    
    btn_weather = WeatherControl(ax_left)
    btn_rain_drop = plt.axes([0.05, 0.85, 0.05, 0.035])
    btn_rain_drop = Button(btn_rain_drop, 'Rain Drop', color='lightblue', hovercolor='darkgrey')
    btn_rain_drop.on_clicked(btn_weather.rain_drop)
    
    btn_rain_stop = plt.axes([0.05, 0.8, 0.05, 0.035])
    btn_rain_stop = Button(btn_rain_stop, 'Rain Stop', color='lightblue', hovercolor='darkgrey')
    btn_rain_stop.on_clicked(btn_weather.rain_stop)
    
    
    for time in range(timestamp):
        terrains.plot_sky_and_ground(ax_left, color_map, filename, timestamp, time)  
        terrains.plot_sun_moon_cloud(ax_left, timestamp, time)
        pond.plot_pond(ax_left)
        pirate.plot_main_boundary_entrance_exit(ax_left)

        for ride in rides_list:       
            ride.plot_each_ride_boundary(ax_left)
            ride.plot_each_ride_entrance_exit(ax_left)
            ride.plot_each_ride_queue(ax_left)
            ride.plot_each_ride_stand(ax_left)
            ride.plot_ride(ax_left)
            ride.step_change(ax_left)               
            statistics_line_plot.set_each_time_info(time, ride.name, ride.number_of_operations, ride.number_of_patrons, ride.price)
            
        statistics_line_plot.plot_each_ride_profit(ax_center_top)  
        statistics_table_plot.set_each_time_info(rides_list)          
        statistics_table_plot.plot_all_ride_info(ax_center_bottom)
        statistics_scatter_plot.plot_patrons_movement(ax_right, hist_posx, hist_posy, fig)  
        
        
        # Traceability Matrix reference 3.5
        # Add new Patrons object every quarter of the timestamp.
        if time == timestamp//4 or time == 2*timestamp//4 or time == 3*timestamp//4:
            add_patrons_list = set_patrons("add", 10, 1, 1, 0, 330, rides_list, pond)    
            total_number_of_patrons += len(add_patrons_list)
            for a in add_patrons_list:
                patrons_list.append(a)   
        
        # If patrons exist the theme park, remove the plot.
        newpatrons_list = []
        for p in patrons_list:
            hist_posx.append(p.xpos)
            hist_posy.append(p.ypos) 
             
            p.plot_me(ax_left)   
            p.step_change(ax_left)
            
            if p.artist is not None:
                newpatrons_list.append(p)       
        patrons_list = newpatrons_list      
        
        # Set the xlim to left, right of the scale.
        ax_left.set_xlim(0,350) 
        ax_center_top.set_xlim(0,timestamp) 
        # Set the ylim to bottom, upper of the scale. 
        ax_left.set_ylim(0,450)
        ax_center_top.set_ylim(0, None) 
        # Set the aspect ratio of the Axes scaling.
        ax_left.set_aspect(0.7)   
              
        ax_left.set_title("Adventure World - Timestamps : " + str(time) + " / " + str(timestamp) + " (interval:" + str(btn_speed.interval) + ")"\
         + "\nTotal number of patrons : "+str(total_number_of_patrons)+", and "+str(len(patrons_list))+" patrons were left" \
         ,fontsize = 10)
        
        # Hide all visual components of the x- and y-axis.
        ax_left.axis('off')
        ax_center_bottom.axis('off')
            
        plt.pause(btn_speed.interval)
        
        if time == timestamp-1:
            plt.savefig("Adventureworld Statistics " + datetime.now().strftime("%Y-%m-%d_%H:%M:%S.png"))
        
        ax_left.clear()
        ax_center_top.clear()
        ax_center_bottom.clear()
                
        plt.show()


    
if __name__ == "__main__":
    print("\n!!!!! ADVENTURE WORLD OPEN !!!!!\n")
    main()
    print("\n!!!!! THANK YOU FOR COMING !!!!!\n")
