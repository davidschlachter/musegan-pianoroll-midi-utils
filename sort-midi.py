#!/usr/local/bin/python3.7

# Sort midi files in the src directory into folders in dest_dir corresponding to the number of tracks and their programs

import pretty_midi
import os
import sys
from shutil import copyfile
import ntpath # just don't use backslashes in file or folder names
import multiprocessing as mp

class Error(Exception):
	"""Base class for exceptions in this module."""
	pass
class NoMIDI(Error):
	def __init__(self, message):
		self.message = message

def main(argv):
	if len(argv) is not (2+1):
		print("Usage: sort-midi.py src_dir dest_dir")
		exit(1)
	else:
		sort_midi(argv[1], argv[2])

def process_file(input):
	file_path = input[0]
	dest_dir  = input[1]
	file = []
	# Get instrumentation
	try:
		midi = pretty_midi.PrettyMIDI( file_path )
		n_instr = str(len(midi.instruments))
		programs = []
		for instr in midi.instruments:
			if instr.is_drum is True:
				programs.append(str(instr.program)+"D")
			else:
				programs.append(str(instr.program))
		programs_str = '-'.join(programs)
		file.append(file_path)
		file.append(n_instr+"_"+programs_str)
	except: # Malformed midi files
		print("  Skipped: error on " + file_path)
		return
	# Ensure dest_dir subdirectory exists
	try:
		os.mkdir( dest_dir )
	except FileExistsError as e:
		pass
	try:
		os.mkdir( dest_dir+"/"+file[1] )
	except FileExistsError as e:
		pass
	except OSError:
		print("  Skipped a directory, file name too long?")
		pass
	# Copy to bin
	try:
		copyfile(file[0], dest_dir+"/"+file[1]+"/"+ntpath.basename(file[0]))
	except OSError:
		print("  Skipped a directory, file name too long?")
		pass

def sort_midi(src_dir, dest_dir):
	file_list = []
	midi_files = []
	n_instr = 0
	dirname = ""

	# Recursively find all midi files in the source directory
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			if file.endswith(".mid"):
				file_list.append([os.path.join(root, file), dest_dir])
	
	n_files = len(file_list)
	if n_files is 0:
		raise NoMIDI("Error: no MIDI files could be read. Exiting...")

	# Reading MIDI files is CPU-intensive
	pool = mp.Pool(mp.cpu_count())
	#midi_files = pool.imap(process_file, [file for file in file_list], n_files / 100)
	for i, _ in enumerate(pool.imap(process_file, [file for file in file_list], int(n_files / 100)) , 1):
		sys.stderr.write('\rdone {0:.2%}'.format(i/n_files))
	pool.close()


if __name__ == "__main__":
	# execute only if run as a script
	main(sys.argv)