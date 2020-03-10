import json
from os import listdir
from os.path import isfile, join

# order of arguments:
#   version1 version2 loc1 loc2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

path = "/usr/jquery-data/jsinspect"
onlyfiles = sorted([f for f in listdir(path) if isfile(join(path, f))])

previousVersion = ""
labels = []
values_list = []

for file in onlyfiles:
    version1 = file.split(".json")[0].split("-")[0]
    version2 = file.split(".json")[0].split("-")[1]
    if version1 == "jsinspect" or version1 == "cloc" or version2 == "jsinspect" or version2 == "cloc":
        continue
    loc1_file = json.load(open(f"/usr/jquery-data/cloc/{version1}.json"))
    loc1 = loc1_file["JavaScript"]["blank"] + loc1_file["JavaScript"]["comment"] + loc1_file["JavaScript"]["code"]
    loc2_file = json.load(open(f"/usr/jquery-data/cloc/{version2}.json"))
    loc2 = loc2_file["JavaScript"]["blank"] + loc2_file["JavaScript"]["comment"] + loc2_file["JavaScript"]["code"]
    # print(f"/usr/jquery-data/jsinspect/{file}")
    code_dup_json = json.load(open(f"/usr/jquery-data/jsinspect/{file}"))
    coverage = 0
    for match in code_dup_json:
        version1_min = 0
        version2_min = 0
        for instance in match["instances"]:
            if version1 in instance["path"]:
                loc = instance["lines"][-1] - instance["lines"][0] + 1
                if version1_min == 0 or version1_min > loc:
                    version1_min = loc

            if version2 in instance["path"]:
                loc = instance["lines"][-1] - instance["lines"][0] + 1
                if version2_min == 0 or version2_min > loc:
                    version2_min = loc

        match_min = min(version1_min, version2_min)
        coverage += match_min

    value = 2*coverage/(loc1 + loc2)

    if previousVersion != version1:
        labels += [version1]
        values_list += [[value]]
        previousVersion = version1
    else:
        values_list[-1] += [value]

labels += ["3.4.1"]
length = len(labels) - 1
for i in range(len(values_list)):
    x_values: list = values_list[i]
    for j in range(length - len(x_values)):
        x_values.insert(0, 0.0)
    x_values.insert(0, 0.0)
    # x_values = list(reversed(x_values))

values_list += [[0.0 for _ in range(len(labels))]]

# values_list = list(reversed(values_list))
print(values_list)

array = np.transpose(np.array(values_list))
# array = np.array([[14, 345],
#                   [45, 67]])
fig, ax = plt.subplots()
fig.set_size_inches(20, 20)
im = ax.imshow(array)

# We want to show all ticks...
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
# ... and label them with the respective list entries
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)
plt.colorbar(im)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")


plt.show()
plt.tight_layout()
plt.savefig("/out/test.png")

print(values_list)
