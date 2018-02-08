from __future__ import print_function
from datetime import datetime
import sys
import os 

INCLUDE_CHECKSUM = False
TIMESTAMP_WINDOW_S = 1

argv = sys.argv
if len(argv) != 3:
    print("Usage: sync_library.py LOCAL_PATH REMOTE_PATH")
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


print("Files in source, missing in target:       (actions: give, PURGE)")
missing_in_target = sorted(list((set(source_names).difference(set(target_names)))))
for diff in missing_in_target:
    print("  ", diff)

print("")
print("Files in target, missing in source:       (actions: take, FORSAKE)")
missing_in_source = sorted(list((set(target_names).difference(set(source_names)))))
for diff in missing_in_source:
    print("  ", diff)

print("")
print("Files in both, with non-matching timestamps:     (action: give-modified, take-modified, latest-modified)")
both_modified = sorted(list((set(target_names).intersection(set(source_names)))))
for diff in both_modified:
    source_time = datetime.fromtimestamp( source_times[source_names.index(diff)] )
    target_time = datetime.fromtimestamp( target_times[target_names.index(diff)] )
    if source_time.replace(second=0, microsecond=0) != target_time.replace(second=0, microsecond=0):
        print("  ", source_time, end='')
        if source_time < target_time:
            print(" < ", end='')
        else:
            print(" > ", end='')
        print(target_time, end='  ')
        print(diff)

print("")
keys = raw_input("Action:\n>>")
if keys == 'give':
    for diff in missing_in_target:
        target_dir = TARGET+"/"+diff.rsplit("/",1)[0]+"/"
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        command = "rsync \""+SOURCE+"/"+diff+"\" \""+target_dir+"\" -tvr"
        print(command)
        os.system(command)

if keys == 'FORSAKE':
    for diff in missing_in_source:
        os.system("rm \""+TARGET+"/"+diff+"\"")

if keys == 'PURGE':
    for diff in missing_in_target:
        os.system("rm \""+SOURCE+"/"+diff+"\"")

if keys == 'take':
    for diff in missing_in_source:
        source_dir = SOURCE+"/"+diff.rsplit("/",1)[0]+"/"
        if not os.path.exists(source_dir): os.makedirs(source_dir)
        command = "rsync \""+TARGET+"/"+diff+"\" \""+source_dir+"\" -tvr"
        print(command)
        os.system(command)

if keys == 'give-modified':
    for diff in both_modified:
        target_dir = TARGET+"/"+diff.rsplit("/",1)[0]+"/"
        if not os.path.exists(target_dir): os.makedirs(target_dir)
        command = "rsync \""+SOURCE+"/"+diff+"\" \""+target_dir+"\" -tvr"
        print(command)
        os.system(command)

if keys == 'take-modified':
    for diff in both_modified:
        source_dir = SOURCE+"/"+diff.rsplit("/",1)[0]+"/"
        if not os.path.exists(source_dir): os.makedirs(source_dir)
        command = "rsync \""+TARGET+"/"+diff+"\" \""+source_dir+"\" -tvr"
        print(command)
        os.system(command)

if keys == 'latest-modified':
    for diff in both_modified:
        source_time = source_times[source_names.index(diff)]
        target_time = target_times[target_names.index(diff)]
        if int(source_time) != int(target_time):
            if source_time < target_time:
                source_dir = SOURCE+"/"+diff.rsplit("/",1)[0]+"/"
                if not os.path.exists(source_dir): os.makedirs(source_dir)
                command = "rsync \""+TARGET+"/"+diff+"\" \""+source_dir+"\" -tvr"
            else:
                target_dir = TARGET+"/"+diff.rsplit("/",1)[0]+"/"
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                command = "rsync \""+SOURCE+"/"+diff+"\" \""+target_dir+"\" -tvr"
            print(command)
            os.system(command)

if keys == '':
    print("No action taken.")

print("Exiting.")
