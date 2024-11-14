from copy import deepcopy
import statistics
import sys
import os
sys.path.insert(0,'')

# Change the file settings here.

test_folder_dir = "application/tests/test_output"
average_prefix = "xhalf_only_pig_main"
subfolder_name = "final_metrics_retention_1"
metric_suffix = "Metrics.txt"
result_folder_name = "only_pig_main_xhalf_averages"

# file_path = "{dir}/{prefix}".format(dir = test_folder_dir, prefix = average_prefix)

seen_character_dicts = dict()
empty_subdict = {"COST": [], "UNIQUE":[], "JOINTS":[], "PREFER":[], "TRUE_UNIQUE":[]}

for filename in os.listdir(test_folder_dir):
    if filename.startswith(average_prefix):
        current_filename = filename + ".txt"

        subfolder_path = "{dir}/{fname}/{sfname}".format(dir = test_folder_dir, fname = filename, sfname = subfolder_name)

        # print(subfolder_path)

        for character_filename in os.listdir(subfolder_path):

            character_name = character_filename.replace(metric_suffix, "")

            if character_name not in seen_character_dicts.keys():
                seen_character_dicts[character_name] = deepcopy(empty_subdict)

            full_file_path = "{sfpath}/{filename}".format(sfpath = subfolder_path, filename = character_filename)
            f = open(full_file_path, "r")
            for line in f:
                for metric_type in empty_subdict.keys():
                    if line.startswith(metric_type):
                        number = float("".join([ele for ele in line if ele.isdigit() or ele == "."]))

                        seen_character_dicts[character_name][metric_type].append(number)
            f.close()

results_dict = dict()
for character_name in seen_character_dicts.keys():
    
    if character_name not in results_dict.keys():

        results_dict[character_name] = deepcopy(empty_subdict)

    for metric_type in empty_subdict.keys():
        results_dict[character_name][metric_type] = statistics.mean(seen_character_dicts[character_name][metric_type])

    
    fullpath = "{dir}/{resultdir}/".format(dir = test_folder_dir, resultdir = result_folder_name)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)

    f = open(fullpath + character_name + "Averages.txt", "w")
    f.write("Graph Results\n")
    f.write(str(seen_character_dicts[character_name]) + "\n")
    f.write("\n")
    f.write("Graph Averages\n")
    f.write(str(results_dict[character_name]))


print(results_dict)