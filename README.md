## simple-sync

A simple UNIX tool based on python for syncing two directories.

for example:
```
simple-sync /home/me/music-library /media/my_friends_server/music-library
```

#### output
Outputs all the files in A but not in B, all files in B but not in A. (B is the target, A the source)

#### actions
A rudimentary shell allows broad actions, 'take' (constructive: files in B but not in A copied into A), 'give' (same as take but from A to B), 'forsake' (destructive: remove all files in A which are not in B), 'purge' (same as forsake but reversed for B).

## find-empty-dirs

UNIX tool to recursively find all empty folders in a directory.


for example:
```
find-empty-dirs /home/me/Downloads
```

#### output
Outputs all the empty folders in the given directory.

#### actions
A rudimentary shell allows the 'purge' action (deletion of the empty folders).
