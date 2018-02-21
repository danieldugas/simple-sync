from __future__ import print_function
from datetime import datetime
import sys
import os 

def trailing_slash(path):
    try:
        path[-1]
    except IndexError:
        return ''
    return path+ ('' if path[-1] == '/' else '/')

def parent_dir(path):
    return trailing_slash("/".join(path.split("/")[:-1]))

argv = sys.argv
if len(argv) != 2:
    print("Usage: empty_dirs.py PATH")
    raise NotImplementedError

SOURCE = trailing_slash(argv[1])

source_index = "/tmp/empty_dir_index.txt"

retvalue = os.system("find " + SOURCE + " -type d -empty  > " + source_index)
if retvalue != 0:
    raise SystemError

def read_index(filepath):
    return [line.strip().split(' ', 1) for line in open(filepath, 'rb')]

source = read_index(source_index)

source_names = [data[0] for data in source]


print("Empty directories in library:       (actions: PURGE)")
missing_in_target = sorted(source_names)
for path in missing_in_target:
    print("  ", path)

print("")
keys = raw_input("Action:\n>>")
if keys == 'PURGE':
    for path in missing_in_target:
        command = "rm -r \""+path+"\""
        print(command)
        os.system(command)

if keys == '':
    print("No action taken.")

print("Exiting.")
