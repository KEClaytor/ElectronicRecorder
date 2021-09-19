# ElectronicRecorder
Code for the electronic recorder project


## Key Table

[Reference](http://www.prescottworkshop.com/bar_finger_c.pdf)

| Key of C  | C | C#| D | Eb| F | F#| G | G#| A | Bb| B | C | C#| D | Eb| E | F | F#| G | G#| A | Bb| B | C | C#| D |
|-----------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Value:    |255|254|252|252|250|245|240|236|224|216|192|160| 96| 32| 62|124|122|116|112|104| 96|102|108| 76| 90| 90|
| 2^7 (128) | x | x | x | x | x | x | x | x | x | x | x | x | o | o | o | / | / | / | / | / | / | / | / | / | / | / |
| 2^6 (64)  | x | x | x | x | x | x | x | x | x | x | x | o | x | o | o | x | x | x | x | x | x | x | x | x | x | x |
| 2^5 (32)  | x | x | x | x | x | x | x | x | x | o | o | x | x | x | x | x | x | x | x | x | x | x | x | o | o | o |
| 2^4 (16)  | x | x | x | x | x | x | x | o | o | x | o | o | o | o | x | x | x | x | x | o | o | o | o | o | x | x |
| 2^3 (8)   | x | x | x | x | x | o | o | x | o | x | o | o | o | o | x | x | x | o | o | x | o | o | x | x | x | x |
| 2^2 (4)   | x | x | x | x | o | x | o | x | o | o | o | o | o | o | x | x | o | x | o | o | o | x | x | x | o | o |
| 2^1 (2)   | x | x | / | o | x | / | o | / | o | o | o | o | o | o | x | o | x | o | o | o | o | x | o | o | x | x |
| 2^0 (1)   | x | / | o | o | o | x | o | o | o | o | o | o | o | o | o | o | o | o | o | o | o | / | o | o | x'| / |

o = open
x = closed
/ = partial open
' = close bell with knee
