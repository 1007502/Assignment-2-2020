import json
import os
import sys
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot

# order of arguments:
#   version1 version2 loc1 loc2
path = "/usr/jquery-data/jsinspect"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for file in onlyfiles:
    version1 = file.split(".json")[0].split("-")[0]
    version2 = file.split(".json")[0].split("-")[1]
    if version1 == "jsinspect" or version1 == "cloc" or version2 == "jsinspect" or version2 == "cloc":
        continue
    loc1_file = json.load(open(f"/usr/jquery-data/cloc/{version1}.json"))
    loc1 = loc1_file["JavaScript"]["blank"] + loc1_file["JavaScript"]["comment"] + loc1_file["JavaScript"]["code"]
    loc2_file = json.load(open(f"/usr/jquery-data/cloc/{version2}.json"))
    loc2 = loc2_file["JavaScript"]["blank"] + loc2_file["JavaScript"]["comment"] + loc2_file["JavaScript"]["code"]
    print(f"/usr/jquery-data/jsinspect/{file}")
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

    print(2*coverage/(loc1 + loc2))
