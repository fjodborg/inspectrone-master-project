import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

def is_float(string):
    # string.isdecimal()
    try:
        float_value = float(string)
        return True
    except ValueError:  # String is not a number
        return False



log_dir = "/home/fjod/repos/inspectrone/docs/performance_real_time"
log_names = ["0.025_timings.txt", "0.040_timings.txt"]
legends = ["0.025m", "0.040m"]

log_dir = "/home/fjod/repos/inspectrone/docs/performance_real_time"
log_names = ["0.025_timings_random.txt", "0.040_timings_random.txt"]
legends = ["0.025m", "0.040m"]

# log_dir = "/home/fjod/repos/inspectrone/docs/performance_real_time/bad"
# log_names = ["0.025_16D_timings.txt", "0.025_32D_timings.txt"]
# legends = ["16D", "32D"]

# log_dir = "/home/fjod/repos/inspectrone/docs/performance_frames"
# log_names = ["0.025_timings.txt", "0.040_timings.txt"]
# legends = ["0.025m", "0.040m"]

# log_dir = "/home/fjod/repos/inspectrone/docs/performance_real_time/limiting"
# log_names = ["0.025_timings.txt", "0.040_timings.txt", "0.025_timings_random.txt", "0.040_timings_random.txt"]
# legends = ["0.025m dist", "0.040m dist", "0.025m ran", "0.040m ran"]



log_dir = "/home/fjod/repos/inspectrone/docs/performance_real_time/best_model"
log_names = ["0.040_timings_last.txt", "0.040_timings_best.txt"]
legends = ["0.040m last", "0.040m best"]

# Remeber to clean the file so only one log is present in the log files
all_lists = []
for i, log_name in enumerate(log_names):
    f = open(os.path.join(log_dir, log_name), "r")
    content = f.read()
    f.close()
    process_times = [float(time.split(':')[1]) for time in [line for line in content.split('\n') if "5 process" in line]]
    transform_times = [float(time.split(':')[1]) for time in [line for line in content.split('\n') if "6 find" in line]]
    pub_pcd_times = [float(time.split(':')[1]) for time in [line for line in content.split('\n') if "7 publish" in line]]
    pub_pose_times = [float(time.split(':')[1]) for time in [line for line in content.split('\n') if "8 publish" in line]]
    fitness_percent = [float(time.split(':')[1]) * 100 for time in [line for line in content.split('\n') if "0 fit" in line]]
    pcd_id = [int(float(time.split(':')[1])) for time in [line for line in content.split('\n') if "0 pcd" in line]]

    # print(pcd_id)
    
    lists = [process_times, transform_times, pub_pcd_times, pub_pose_times]
    total_time = [sum(x) for x in (list(zip(*lists)))]
    lists.append(fitness_percent)
    lists.append(total_time)

    all_lists.append(lists)
    



# print(all_lists)
# total_times = sum([process_times, transform_times, pub_pcd_times, pub_pose_times, fitness_percent])

# print(total_times)

# print( [x for x in all_lists[0]])
print(len(all_lists[0]))
all_lists = (list(zip(*all_lists)))
# print(all_lists)
# print()

# print([x for x in all_lists])
# print(all_lists)

all_labels = ["Processing time [s]", "Transform time [s]", "Publish point cloud time [s]", "Publish pose time [s]", "Fitness [%]", "Total time [s]"]
figsize = (10, 5)
pltratio = [8,4]
box_label_range = range(len(legends))
linewidth=2


for k, sets in enumerate(all_lists):
    data = list(zip(*sets))
    plt.rcParams.update({'font.size': 18,
                        'axes.titlesize': 22})
    fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': pltratio}, figsize=figsize)
    # print(data)
    # for data in sets :
        # print(data_1)
    for ax in axs:
        ax.grid()

    axs[0].plot(data, linewidth=linewidth)
    axs[0].set(xlabel='pcd id', ylabel=all_labels[k])
    axs[0].legend(legends)
    # plt.legend(["hr="+hit_ratio for hit_ratio in hit_ratio_group])
    # plt.ylabel(all_labels[k])
    # plt.yticks(np.arange(0, max_met+0.01, step=max_met/8))
    # plt.xlabel("")
    # plt.xticks(np.arange(0, len(metrics_group[j]), step=10))
    # plt.title(titles[i])
    bp = axs[1].boxplot(sets, widths=(0.75), positions=box_label_range,
        # color=dict(boxes='r', whiskers='r', medians='r', caps='r'),
        boxprops=dict(linestyle='-', linewidth=linewidth),
        flierprops=dict(linestyle='-', linewidth=linewidth, marker="o",  markerfacecolor='k'),
        medianprops=dict(linestyle='-', linewidth=linewidth),
        meanprops=dict(linestyle='-', linewidth=linewidth),
        whiskerprops=dict(linestyle='-', linewidth=linewidth),
        capprops=dict(linestyle='-', linewidth=linewidth),
    )
    # bp.set_linewidth(4)
    # [[item.set_linewidth(4) for item in bp[key]['boxes']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['boxes']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['fliers']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['medians']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['means']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['whiskers']] for key in bp.keys()]
    # [[item.set_linewidth(linewidth) for item in bp[key]['caps']] for key in bp.keys()]

    # axs[1].set(xlabel="model", ylabel=all_labels[k])
    axs[1].set(ylabel=all_labels[k])
    # axs[1].set(xticks=([0,1], legends))
    axs[1].set_xticks(box_label_range)
    axs[1].set_xticklabels(legends, rotation=40)
    
    
    plt.tight_layout()
    plt.show()
    
    # string_prefix = "[{}]".format(log_names[i])
    # string_suffix = "[{}]".format("_".join(hit_ratio_group))
    # file_name = "{}_{}_{}.eps".format(string_prefix, metric_name, string_suffix)
    # print("saving file in", docs_path+file_name)
    # fig.savefig(docs_path+file_name, format='eps')

    # for k, metric_name in enumerate(metric_names):
    #     plt.rcParams.update({'font.size': 18,
    #                         'axes.titlesize': 22})
    #     fig, ax = plt.subplots() # ?

    #     max_met = 0
    #     for j, log_dir in enumerate(log_dir_group):
    #         metric = np.array(metrics_group[j])[:,k]
    #         if max(metric) > max_met:
    #             max_met = max(metric)
            
    #         plt.plot(metric, linewidth=4)

    #     plt.ylabel(metric_name)
    #     plt.yticks(np.arange(0, max_met+0.01, step=max_met/8))
    #     plt.xlabel("epoch")
    #     plt.xticks(np.arange(0, len(metrics_group[j]), step=10))
    #     plt.title(titles[i])
    #     plt.grid()
    #     plt.tight_layout()
    #     # plt.show()
    #     string_prefix = "[{}]".format(log_names[i])
    #     string_suffix = "[{}]".format("_".join(hit_ratio_group))
    file_name = "{}.pdf".format(all_labels[k])
    #     print("saving file in", docs_path+file_name)
    print(os.path.join(log_dir, file_name))
    fig.savefig(os.path.join(log_dir, file_name), format='pdf')

#print(final_lines)