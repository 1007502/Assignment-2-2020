import os

subdirectories = sorted(next(os.walk("/usr/jquery-data"))[1])
i = 0
for directory1 in subdirectories:
    cloc_command = f"cloc {directory1}/src --json > /usr/jquery-data/cloc/{directory1}.json"
    os.system(cloc_command)
    os.system(f"echo {cloc_command}")
    for directory2 in subdirectories:
        if directory1 == directory2:
            os.system("echo Break")
            break
        jsinspect_command = f"jsinspect {directory1}/src {directory2}/src -I -L --truncate 1 -r json > " \
            f"/usr/jquery-data/jsinspect/{directory1}-{directory2}.json"
        os.system(jsinspect_command)
        os.system(f"echo {jsinspect_command}")
        os.system(f"echo Voortgang {i}")
        i += 1
