#!/usr/local/bin/python3.7

import pretty_midi
import sys
import os


def main(argv):
    if len(argv) < 1:
        print("Usage: fix-glissando.py file-1.mid file-2.mid ... file-n.mid")
        print("Files are saved to clean-file-1.mid ... clean-file-n.mid")
        print("Removes glissandi in two-track generated MIDI files")
        exit(1)
    for file in argv:
        if os.path.isfile("clean-"+file):
            continue
            
        try:
            a = pretty_midi.PrettyMIDI(midi_file=file)
        except:
            continue

        index = 0
        if len(a.instruments[1].notes) > len(a.instruments[index].notes):
            index = 1
        
        b = []
        for note in range(0, len(a.instruments[index].notes)):
            try:
                    if a.instruments[index].notes[note+1].pitch == (a.instruments[index].notes[note].pitch +1):
                            b.append(note)
            except:
                    pass
        for note in sorted(b, reverse=True):
            del a.instruments[index].notes[note]

        del b
        a.write("clean-"+file)


if __name__ == "__main__":
    main(sys.argv[1:])
