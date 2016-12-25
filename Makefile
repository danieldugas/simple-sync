SOURCE=/sanctuary/Music/Musique
TARGET=/media/daniel/a

all:
	find $(SOURCE) -type f -printf "%t %P\n" > ./library_index.txt
	git add -u
	git diff --cached
