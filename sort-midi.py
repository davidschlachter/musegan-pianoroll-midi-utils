#!/usr/local/bin/python3.7

# Sort midi files in the src directory into folders in dest_dir corresponding to the number of tracks and their programs

import pretty_midi
import os
from shutil import copyfile
import ntpath # just don't use backslashes in file or folder names

src_dir  = "/home/david/2020-maitrise/inf8225/project/datasets/bach/"
dest_dir = "/home/david/2020-maitrise/inf8225/project/datasets/sorted-test"
midi_files = []
n_instr = 0
dirname = ""

# Recursively find all midi files in the source directory
for root, dirs, files in os.walk(src_dir):
	for file in files:
		if file.endswith(".mid"):
			try:
				file_path = os.path.join(root, file)
				midi = pretty_midi.PrettyMIDI( file_path )
				n_instr = str(len(midi.instruments))
				programs = []
				for instr in midi.instruments:
					if instr.is_drum is True:
						programs.append(str(instr.program)+"D")
					else:
						programs.append(str(instr.program))
				programs_str = '-'.join(programs)
				midi_files.append([file_path, n_instr+"_"+programs_str])
			# malformed midi files
			except IOError as e:
				print("  Skipped: error on " + file_path)
			except EOFError as e:
				print("  Skipped: error on " + file_path)

midi_bins = {}

# First mode: just separate by number of tracks
i = 0
for file in midi_files:
	try:
		i = file[1]
		midi_bins[i].append(file[0])
	except:
		midi_bins[i] = []
		i = file[1]
		midi_bins[i].append(file[0])

print( "Found " + str(len(midi_bins)) + " different numbers of instruments" )

for a_bin in midi_bins:
	try:
		os.mkdir(dest_dir+"/"+str(a_bin))
	except FileExistsError as e:
		pass
	for file in midi_bins[a_bin]:
		copyfile(file, dest_dir+"/"+str(a_bin)+"/"+ntpath.basename(file))