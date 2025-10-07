import os
from datetime import datetime
import pandas as pd
# from pathlib import Path


def collect_and_sort(input_data_folder):
    data_files = []

    # check that data directory is a folder
    if os.path.isdir(input_data_folder):
        for filename in os.listdir(input_data_folder):
            if filename.endswith(".txt"):
                # format the full file path
                full_file_path = os.path.join(input_data_folder, filename)

                # extract details from the filename
                experiment_id = filename.split("_")[0]
                plate_number = filename.split("_")[1]
                inoculation_number = filename.split("_")[2]
                reading_number = (filename.split("_")[3]).replace(".txt", "")

                # extract time of reading from file details
                mtime = os.path.getmtime(
                    full_file_path
                )  # uses mtime because ctime was altered in download
                formatted_ctime = datetime.fromtimestamp(mtime).strftime(
                    "%I:%M:%S %p %Y-%m-%d"
                )

                # extract data from columns of the correct inoculation
                df = pd.read_csv(full_file_path, header=None)
                if int(inoculation_number) == 1:
                    relevant_column_data = df.iloc[:, [0, 4, 8]]
                elif int(inoculation_number) == 2:
                    relevant_column_data = df.iloc[:, [1, 5, 9]]
                elif int(inoculation_number) == 3:
                    relevant_column_data = df.iloc[:, [2, 6, 10]]
                elif int(inoculation_number) == 4:
                    relevant_column_data = df.iloc[:, [3, 7, 11]]

                # format list of file details
                all_file_details = [
                    full_file_path,
                    experiment_id,
                    plate_number,
                    inoculation_number,
                    reading_number,
                    mtime,
                    formatted_ctime,
                    relevant_column_data,
                ]

                # append to list of all data file details
                data_files.append(all_file_details)

    data_files.sort(key=lambda x: x[5])

    # sort data files by graph
    all_data_sorted_by_graph = []

    plate1_inoculation1_data = []
    plate1_inoculation2_data = []
    plate1_inoculation3_data = []
    plate1_inoculation4_data = []

    plate2_inoculation1_data = []
    plate2_inoculation2_data = []
    plate2_inoculation3_data = []
    plate2_inoculation4_data = []

    plate3_inoculation1_data = []
    plate3_inoculation2_data = []
    plate3_inoculation3_data = []
    plate3_inoculation4_data = []

    plate4_inoculation1_data = []
    plate4_inoculation2_data = []
    plate4_inoculation3_data = []
    plate4_inoculation4_data = []

    plate5_inoculation1_data = []
    plate5_inoculation2_data = []
    plate5_inoculation3_data = []
    plate5_inoculation4_data = []

    plate6_inoculation1_data = []
    plate6_inoculation2_data = []
    plate6_inoculation3_data = []
    plate6_inoculation4_data = []

    try:
        for data_list in data_files:
            if int(data_list[2]) == 1:  # plate 1
                if int(data_list[3]) == 1:  # inoculation 1
                    plate1_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate1_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate1_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate1_inoculation4_data.append(data_list)

            elif int(data_list[2]) == 2:  # plate 2
                if int(data_list[3]) == 1:  # inoculation 1
                    plate2_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate2_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate2_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate2_inoculation4_data.append(data_list)

            elif int(data_list[2]) == 3:  # plate 3
                if int(data_list[3]) == 1:  # inoculation 1
                    plate3_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate3_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate3_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate3_inoculation4_data.append(data_list)

            elif int(data_list[2]) == 4:  # plate 4
                if int(data_list[3]) == 1:  # inoculation 1
                    plate4_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate4_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate4_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate4_inoculation4_data.append(data_list)

            elif int(data_list[2]) == 2:  # plate 5
                if int(data_list[3]) == 1:  # inoculation 1
                    plate5_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate5_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate5_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate5_inoculation4_data.append(data_list)

            elif int(data_list[2]) == 6:  # plate 6
                if int(data_list[3]) == 1:  # inoculation 1
                    plate6_inoculation1_data.append(data_list)
                elif int(data_list[3]) == 2:  # inoculation 2
                    plate6_inoculation2_data.append(data_list)
                elif int(data_list[3]) == 3:  # inoculation 3
                    plate6_inoculation3_data.append(data_list)
                elif int(data_list[3]) == 4:  # inoculation 4
                    plate6_inoculation4_data.append(data_list)

        all_data_sorted_by_graph = [
            plate1_inoculation1_data,
            plate1_inoculation2_data,
            plate1_inoculation3_data,
            plate1_inoculation4_data,
            plate2_inoculation1_data,
            plate2_inoculation2_data,
            plate2_inoculation3_data,
            plate2_inoculation4_data,
            plate3_inoculation1_data,
            plate3_inoculation2_data,
            plate3_inoculation3_data,
            plate3_inoculation4_data,
            plate4_inoculation1_data,
            plate4_inoculation2_data,
            plate4_inoculation3_data,
            plate4_inoculation4_data,
            plate5_inoculation1_data,
            plate5_inoculation2_data,
            plate5_inoculation3_data,
            plate5_inoculation4_data,
            plate6_inoculation1_data,
            plate6_inoculation2_data,
            plate6_inoculation3_data,
            plate6_inoculation4_data,
        ]

    except Exception as e:
        print("Sorting by graphs did not work")
        print(e)

    return all_data_sorted_by_graph
