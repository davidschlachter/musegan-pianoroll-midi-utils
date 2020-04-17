# Prepare MIDI files for MuseGAN

Scripts to process MIDI files for use in MuseGAN and similar neural networks accepting input as multitrack pianorolls (\*.npz).

## Typical workflow

Source MIDI files are in `./midi-files` and are separated by instrumentation into the `./sorted-midi` folder:

`python sort-midi.py ./midi-files ./sorted-midi`

The most common instrumentation is identified:

`$ for f in ./sorted-midi/*; do nfiles=$(find "$f" -type f -print | wc -l); echo "$nfiles  $f"; done | sort -n`

The folder containing the largest number of files (e.g. `./sorted-midi/2_0-0`) with the same instrumentation is converted to NPZ files:

`convert-midi.py ./sorted-midi/2_0-0 ./2_0-0-NPZ`

## `sort-midi.py`

Usage: `sort-midi.py src-dir dest-dir`

Recursively find MIDI files in `src-dir` and categorizes them by instrumentation into subdirectories of `dest-dir`. Format of `dest-dir` directories is the number of tracks, followed by underscore, followed by a hyphen-separated list of each track indicated by program, with suffix "D" if the track is a drum track.

It may be convenient to normalize the file names. This can easily be done by converting names to md5 hashes, e.g.

`for i in *; do sum=$(echo -n "$i"|md5 -q); mv -- "$i" "${sum%% *}.${i##*.}"; done`

## `convert-midi.py`

Usage: `convert-midi.py src-dir dest-dir`

Convert all MIDI files in `src-dir` to NPZ files in the destination folder `dest-dir`.

