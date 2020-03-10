import os

subdirectories = sorted(next(os.walk("/usr/jquery-data"))[1])
i = 0
for directory1 in subdirectories:
    cloc_command = f"cloc {directory1}/src --json --out=/usr/jquery-data/cloc/{directory1}.json"
    os.system(cloc_command)
    print(f"{cloc_command}")
    for directory2 in subdirectories:
        if directory1 == directory2:
            os.system("echo Break")
            break
        jsinspect_command = f"jsinspect {directory2}/src {directory1}/src -I -L --truncate 1 -r json > " \
            f"/usr/jquery-data/jsinspect/{directory2}-{directory1}.json"
        os.system(jsinspect_command)
        print(f"{jsinspect_command}")
        print(f"Voortgang {i}")
        i += 1
