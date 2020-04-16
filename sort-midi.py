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

def process_file(file_path):
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
		return [file_path, n_instr+"_"+programs_str]
	# malformed midi files
	except:
		print("  Skipped: error on " + file_path)

def sort_midi(src_dir, dest_dir):
	file_list = []
	midi_files = []
	n_instr = 0
	dirname = ""

	# Recursively find all midi files in the source directory
	for root, dirs, files in os.walk(src_dir):
		for file in files:
			if file.endswith(".mid"):
				file_list.append(os.path.join(root, file))
				
	# Reading MIDI files is CPU-intensive
	pool = mp.Pool(mp.cpu_count())
	midi_files = pool.map(process_file, [file for file in file_list])
	pool.close()

	if len(midi_files) is 0:
		raise NoMIDI("Error: no MIDI files could be read. Exiting...")

	midi_bins = {}

	# First mode: just separate by number of tracks
	i = 0
	for file in midi_files:
		try:
			i = file[1]
			midi_bins[i].append(file[0])
		except TypeError:
			print("  Skipping a file, TypeError on "+str(file))
		except KeyError:
			midi_bins[i] = []
			i = file[1]
			midi_bins[i].append(file[0])
		except:
			print("  Skipping a file, exception raised.")

	print( "Found " + str(len(midi_bins)) + " different numbers of instruments" )

	for a_bin in midi_bins:
		try:
			os.mkdir(dest_dir+"/"+str(a_bin))
		except FileExistsError as e:
			pass
		except OSError:
				print("  Skipped a directory, file name too long?")
		for file in midi_bins[a_bin]:
			try:
				copyfile(file, dest_dir+"/"+str(a_bin)+"/"+ntpath.basename(file))
			except OSError:
				print("  Skipped a directory, file name too long?")

if __name__ == "__main__":
	# execute only if run as a script
	main(sys.argv)