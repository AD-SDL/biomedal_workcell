import argparse
from helper_functions.collect_info_and_sort_by_graph import collect_and_sort
from helper_functions.graph import graph

# import numpy as np
# from pathlib import Path


def graph_results(input_file_dir, output_graphs_dir):
    data_sorted_by_graph = collect_and_sort(input_file_dir)

    # Testing
    for set in data_sorted_by_graph:
        if len(set) > 0:
            graph(set, output_graphs_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", help="input dirextory path")
    parser.add_argument("-o", help="output graphs directory")

    args = parser.parse_args()
    input_file_dir = args.i
    output_graphs_dir = args.o

    graph_results(input_file_dir, output_graphs_dir)
