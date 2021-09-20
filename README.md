# ElectronicRecorder
Code for the electronic recorder project


## Key Table

[Fingering Chart](http://www.prescottworkshop.com/bar_finger_c.pdf)
[MIDI Notes](https://newt.phys.unsw.edu.au/jw/notes.html)

| Key of C  | C | C#| D | Eb| E | F | F#| G | G#| A | Bb| B | C | C#| D | Eb| E | F | F#| G | G#| A | Bb| B | C | C#| D |
|-----------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Value:    |255|254|254|252|252|251|246|240|236|224|216|192|160| 96| 32| 62|124|122|116|112|104| 96|102|108| 76| 90| 90|
|MIDI:      | 60| 61| 62| 63| 64| 65| 66| 67| 68| 69| 70| 71| 72| 73| 74| 75| 76| 77| 78| 79| 80| 81| 82| 83| 84| 85| 86|
| 2^7 (128) | x | x | x | x | x | x | x | x | x | x | x | x | x | o | o | o | / | / | / | / | / | / | / | / | / | / | / |
| 2^6 (64)  | x | x | x | x | x | x | x | x | x | x | x | x | o | x | o | o | x | x | x | x | x | x | x | x | x | x | x |
| 2^5 (32)  | x | x | x | x | x | x | x | x | x | x | o | o | x | x | x | x | x | x | x | x | x | x | x | x | o | o | o |
| 2^4 (16)  | x | x | x | x | x | x | x | x | o | o | x | o | o | o | o | x | x | x | x | x | o | o | o | o | o | x | x |
| 2^3 (8)   | x | x | x | x | x | x | o | o | x | o | x | o | o | o | o | x | x | x | o | o | x | o | o | x | x | x | x |
| 2^2 (4)   | x | x | x | x | x | o | x | o | x | o | o | o | o | o | o | x | x | o | x | o | o | o | x | x | x | o | o |
| 2^1 (2)   | x | x | x | / | o | x | x | o | / | o | o | o | o | o | o | x | o | x | o | o | o | o | x | o | o | x | x |
| 2^0 (1)   | x | / | o | o | o | x | o | o | o | o | o | o | o | o | o | o | o | o | o | o | o | o | / | o | o | x'| / |

o = open
x = closed
/ = partial open
' = close bell with knee

## Development Notes

The instrument select requires that a channel already be selected, eg; by playing a note.

The MIDI chip keeps a memory of all of the commands, so if it's not doing what you think, it may be time to reset the chip and get back to a "fresh" state.

## References

[Music Maker Featherwing Tutorial](https://learn.adafruit.com/adafruit-music-maker-featherwing/)
[VS1053b Datasheet](http://www.vlsi.fi/fileadmin/datasheets/vs1053.pdf)

[adafruit_midi @ github](https://github.com/adafruit/Adafruit_CircuitPython_MIDI)
[adafruit_midi @ readthedocs](https://circuitpython.readthedocs.io/projects/midi/en/latest/index.html)
[adafruit_midi example](https://learn.adafruit.com/adafruit-midi-featherwing/circuitpython-midi-example)

[Sparkfun MIDI tutorial](https://learn.sparkfun.com/tutorials/midi-tutorial/all)
[CMU MIDI tutorial](https://www.cs.cmu.edu/~music/cmsip/readings/MIDI%20tutorial%20for%20programmers.html)
