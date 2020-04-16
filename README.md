# Prepare MIDI files for MuseGAN

Scripts to process MIDI files for use in MuseGAN and similar neural networks accepting input as multitrack pianorolls (\*.npz).

## `sort-midi.py`

Usage: `sort-midi.py `src-dir dest-dir`

Recursively find MIDI files in `src-dir` and categorizes them by instrumentation into subdirectories of `dest-dir`. Format of `dest-dir` directories is the number of tracks, followed by underscore, followed by a hyphen-separated list of each track indicated by program, with suffix "D" if the track is a drum track.

## `convert-midi.py`

Usage: `convert-midi.py `src-dir dest-dir`

Convert all MIDI files in `src-dir` to NPZ files in the destination folder `dest-dir`.
