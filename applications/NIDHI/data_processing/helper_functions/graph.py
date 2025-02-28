import numpy as np
import sys
import os
import platform
from datetime import datetime
import pandas as pd
# from pathlib import Path
import matplotlib.pyplot as plt

def graph(data_for_one_graph, output_directory): 

    # format dataframes for each of the three concurrent inoculations on the plate 
    timestamps = []
    inoculation_column1 = None
    inoculation_column2 = None 
    inoculation_column3 = None

    # extract details 
    experiment_id = None
    plate_id = None
    inoculation_num = None
    # CONTINUE HERE!

     # format data for each graph into df
    i = 0
    for i in range(len(data_for_one_graph)): 
        current_dataset = data_for_one_graph[i]
        timestamps.append(current_dataset[5])

        if experiment_id is None: 
            experiment_id = current_dataset[1]
        if plate_id is None: 
            plate_id = current_dataset[2]
        if inoculation_num is None: 
            inoculation_num = current_dataset[3]

        # inoculation set 1
        if inoculation_column1 is None: 
            data = current_dataset[7].iloc[:, 0]
            inoculation_column1 = pd.DataFrame(data).reset_index(drop=True)
            inoculation_column1.columns = [0]
        else: 
            new_column_to_add = current_dataset[7].iloc[:, 0]
            inoculation_column1[i] = new_column_to_add

        # inoculation set 2
        if inoculation_column2 is None: 
            data = current_dataset[7].iloc[:, 1]
            inoculation_column2 = pd.DataFrame(data).reset_index(drop=True)
            inoculation_column2.columns = [0]
        else: 
            new_column_to_add = current_dataset[7].iloc[:, 1]
            inoculation_column2[i] = new_column_to_add

        # inoculation set 3
        if inoculation_column3 is None: 
            data = current_dataset[7].iloc[:, 2]
            inoculation_column3 = pd.DataFrame(data).reset_index(drop=True)
            inoculation_column3.columns = [0]
        else: 
            new_column_to_add = current_dataset[7].iloc[:, 2]
            inoculation_column3[i] = new_column_to_add
        
        i += 1
    
    # convert timestamps into elapsed time in minutes
    if len(timestamps) > 0: 
        time_differences = np.round(((np.array(timestamps) - timestamps[0]) / 60).astype(int)).tolist() 

    # inoculation_column2.columns = range(len(inoculation_column1.columns)) 

    # TESTING
    print(inoculation_column1)
    print()
    print(inoculation_column2)
    print()
    print(inoculation_column3)
    print()
    print(timestamps)



    # graph each dataframe
    colors = ['r', 'g', 'b']

    # SET 1
    for i, row in inoculation_column1.iterrows(): 
        if i < 3: 
            color = colors[0]
        elif i < 6: 
            color = colors[1]
        else: 
            color = colors[2]
        plt.plot(time_differences, row.values, color=color)

    plt.xticks(time_differences, labels=[str(int(t)) for t in time_differences], rotation=90, ha='center')
    plt.xlabel("Incubation time in minutes")
    plt.ylabel("Absorbance OD(590)")
    plt.title("Set 1")
    figure_save_path = os.path.join(output_directory, f"{experiment_id}_{plate_id}_{inoculation_num}_set1")
    # figure_save_path = "/Users/cstone/Documents/RapidPrototypingLab/GitRepos/workcells/biomedal_workcell/applications/NIDHI/data_processing/graphs/test1.png"
    plt.savefig(figure_save_path, bbox_inches='tight', pad_inches=.3)
    plt.clf()

    # SET 2
    for i, row in inoculation_column2.iterrows(): 
        if i < 3: 
            color = colors[0]
        elif i < 6: 
            color = colors[1]
        else: 
            color = colors[2]
        plt.plot(time_differences, row.values, color=color)

    plt.xticks(time_differences, labels=[str(int(t)) for t in time_differences], rotation=90, ha='center')
    plt.xlabel("Incubation time in minutes")
    plt.ylabel("Absorbance OD(590)")
    plt.title("Set 2")
    figure_save_path = os.path.join(output_directory, f"{experiment_id}_{plate_id}_{inoculation_num}_set2")
    # figure_save_path = "/Users/cstone/Documents/RapidPrototypingLab/GitRepos/workcells/biomedal_workcell/applications/NIDHI/data_processing/graphs/test2.png"
    plt.savefig(figure_save_path, bbox_inches='tight', pad_inches=.3)
    plt.clf()

    # SET 3
    for i, row in inoculation_column3.iterrows(): 
        if i < 3: 
            color = colors[0]
        elif i < 6: 
            color = colors[1]
        else: 
            color = colors[2]
        plt.plot(time_differences, row.values, color=color)

    plt.xticks(time_differences, labels=[str(int(t)) for t in time_differences], rotation=90, ha='center')
    plt.xlabel("Incubation time in minutes")
    plt.ylabel("Absorbance OD(590)")
    plt.title("Set 3")
    figure_save_path = os.path.join(output_directory, f"{experiment_id}_{plate_id}_{inoculation_num}_set3")
    # figure_save_path = "/Users/cstone/Documents/RapidPrototypingLab/GitRepos/workcells/biomedal_workcell/applications/NIDHI/data_processing/graphs/test3.png"
    plt.savefig(figure_save_path, bbox_inches='tight', pad_inches=.3)
    plt.clf()



    



