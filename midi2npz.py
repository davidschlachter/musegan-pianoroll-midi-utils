#!/usr/local/bin/python3.7

# Convert midi files in the src_directory, ouput as npz files in the dest_directory

import pypianoroll
import os
import sys
from shutil import copyfile
import ntpath # just don't use backslashes in file or folder names
import multiprocessing as mp

def main(argv):
	if len(argv) is not (2+1):
		print("Usage: convert-midi.py src_dir dest_dir")
		exit(1)
	else:
		convert_midi(argv[1], argv[2])

def convert_file(file):
	try:
		midi = pypianoroll.parse(file[0])
		pypianoroll.save( file[1]+"/"+ntpath.basename(file[0]), midi )
	except:
		print("  Error, skipping "+str(file))

def convert_midi(src_dir, dest_dir):
	file_list = []

	try:
		os.mkdir( dest_dir )
	except FileExistsError as e:
		pass

	# Recursively find all midi files in the source directory
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			if file.endswith(".mid"):
				file_list.append([os.path.join(root, file), dest_dir])

	# Converting MIDI files is CPU-intensive
	pool = mp.Pool(mp.cpu_count())
	midi_files = pool.map(convert_file, [file for file in file_list])
	pool.close()


if __name__ == "__main__":
	# execute only if run as a script
	main(sys.argv)