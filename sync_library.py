from __future__ import print_function
import sys
import os 

INCLUDE_CHECKSUM = False
TIMESTAMP_WINDOW_S = 1

argv = sys.argv
if len(argv) != 3:
    print("Usage: sync_library.py LIBRARY_PATH TARGET_PATH")
    raise NotImplementedError

SOURCE = argv[1]
TARGET = argv[2]

source_index = "/tmp/source_index.txt"
target_index = "/tmp/target_index.txt"

if INCLUDE_CHECKSUM:
    os.system("find " + SOURCE + " -type f -printf '%T@ ' -exec shasum {} \; > " + source_index)
else:
    os.system("find " + SOURCE + " -type f -printf '%T@ %P\n' > " + source_index)

if INCLUDE_CHECKSUM:
    os.system("find " + TARGET + " -type f -printf '%T@ ' -exec shasum {} \; > " + target_index)
else:
    os.system("find " + TARGET + " -type f -printf '%T@ %P\n' > " + target_index)

def read_index(filepath):
    return [line.strip().split(' ', 1) for line in open(filepath, 'rb')]

source = read_index(source_index)
target = read_index(target_index)

source_names = [data[1] for data in source]
source_times = [float(data[0]) for data in source]
target_names = [data[1] for data in target]
target_times = [float(data[0]) for data in target]


print("Files in source, missing in target:")
missing_in_target = sorted(list((set(source_names).difference(set(target_names)))))
for diff in missing_in_target:
    print("  ", diff)

print("")
print("Files in target, missing in source:")
missing_in_source = sorted(list((set(target_names).difference(set(source_names)))))
for diff in missing_in_source:
    print("  ", diff)

print("")
print("Files in both, with non-matching timestamps:")
for diff in sorted(list((set(target_names).intersection(set(source_names))))):
    source_time = source_times[source_names.index(diff)]
    target_time = target_times[target_names.index(diff)]
    if int(source_time) != int(target_time):
        print("  ", source_time, end='')
        if source_time < target_time:
            print(" < ", end='')
        else:
            print(" > ", end='')
        print(target_time, end='  ')
        print(diff)

print("")
keys = raw_input("Action:\n>>")
if keys == 'sync':
    for diff in missing_in_target:
        target_path = TARGET+"/"+diff.rsplit("/",1)[0]+"/"
        if not os.path.exists(target_path): os.makedirs(target_path)
        command = "rsync \""+SOURCE+"/"+diff+"\" \""+target_path+"\" -tvr"
        print(command)
        os.system(command)
if keys == 'dry-run':
    for diff in missing_in_target:
        if not os.path.exists(TARGET+"/"+diff): os.makedirs(TARGET+"/"+diff)
        command = "rsync \""+SOURCE+"/"+diff+"\" \""+TARGET+"/"+diff+"\" -tvrn"
        print(command)
        os.system(command)

if keys == 'delete':
    for diff in missing_in_source:
        os.system("rm \""+TARGET+"/"+diff+"\"")
