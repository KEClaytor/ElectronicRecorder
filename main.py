
import time
import board
import busio
import digitalio
import adafruit_lps2x

i2c = busio.I2C(board.SCL, board.SDA)
lps = adafruit_lps2x.LPS22(i2c)

# Capture ambient pressure on startup
avg_pressure = []
for ii in range(10):
    avg_pressure.append(lps.pressure)
    time.sleep(0.1)
avg_pressure = sum(avg_pressure)/10
print(avg_pressure)

# # Debug: Print pressure values for plotting
# while True:
#     print((lps.pressure - avg_pressure,))
#     time.sleep(0.05)

import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=1,
    out_channel=0,
    debug=False,
)

print("MIDI Out demo")
print("Default output channel:", midi.out_channel)

rp_keys = list(
    map(
        digitalio.DigitalInOut,
        [
            board.D25,
            board.D13,
            board.D12,
            board.D11,
            board.D10,
            board.D9,
            board.D6,
            board.D5,
        ]
    )
)
keys = rp_keys

for k in keys:
    k.switch_to_input(pull=digitalio.Pull.UP)

notes_soprano = {
    255: 60,
    254: 62,
    252: 64,
    251: 65,
    246: 66,
    240: 67,
    236: 68,
    224: 69,
    216: 70,
    192: 71,
    160: 72,
    96: 81,
    32: 74,
    62: 75,
    124: 76,
    122: 77,
    116: 78,
    112: 79,
    104: 80,
    102: 82,
    108: 83,
    76: 84,
    90: 86
}
notes = notes_soprano


from adafruit_midi.midi_message import MIDIMessage
class InstrumentSelect(MIDIMessage):

    _STATUS = 0xC0
    _STATUSMASK = 0xF0
    LENGTH = 3

    def __init__(self, instrument, *, channel=None):
        self.instrument = instrument
        super().__init__(channel=channel)
        if not 0 <= self.instrument <= 127:
            self._raise_valueerror_oor()

    def __bytes__(self):
        return bytes(
            [self._STATUS | (self.channel & self.CHANNELMASK), self.instrument]
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1], msg_bytes[2], channel=msg_bytes[0] & cls.CHANNELMASK)


NoteOn.register_message_type()

def poll(keys):
    """Poll the keys to determine the note value.
    """
    value = 0
    for ii, k in enumerate(keys):
        # Buttons are pull-up, pressed = off
        if not k.value:
            value += 2**(7 - ii)
    return value

def fingering(keys):
    str = ""
    for ii, k in enumerate(keys):
        # Buttons are pull-up, pressed = off
        if not k.value:
            str += "|x"
        else:
            str += "|o"
    return str


class PressureButton():

    def __init__(self, sensor, ambient, threshold, down_on_increase=True) -> None:
        self._sensor = sensor
        self._ambient = ambient
        self._threshold = threshold
        self._last_state = False
        self._current_state = False
        self._thresh_pos = down_on_increase

    def poll(self):
        self._last_state = self._current_state
        delta = self._sensor.pressure - self._ambient
        if self._thresh_pos:
            # Positive pressure is a button press
            self._current_state = delta > self._threshold
        else:
            # Negative pressure is a button press
            self._current_state = delta < self._threshold
        self._delta = delta

    @property
    def rising(self):
        if (not self._last_state) and (self._current_state):
            return True
        return False

    @property
    def falling(self):
        if (self._last_state) and (not self._current_state):
            return True
        return False

    @property
    def pressed(self):
        return self._current_state

    @property
    def delta(self):
        return self._delta


button = PressureButton(lps, avg_pressure, 1.5)

print("selecting instrument")
# Pipe:
# 73 Piccolo
# 74 Flute
# 75 Recorder
# 76 Pan Flute
# 77 Blown Bottle
# 78 Shakuhachi
# 79 Whistle
# 80 Ocarina
midi.send(InstrumentSelect(79))
midi.send(ControlChange(7, 127))

old_v = 0
old_note = 0
while True:
    button.poll()
    print((button.delta, ))

    # Poll the new value
    new_v = poll(keys)
    new_note = notes.get(new_v, None)
    if new_note is None:
        continue

    if button.rising:
        # Starting a note
        print("Rising")
        midi.send(NoteOn(new_note))
    elif button.falling:
        # Ending a note
        print("Falling")
        midi.send(NoteOff(old_note))
    if button.pressed:
        # See if we've changed fingerings while blowing
        if not (new_v == old_v):
            print("Switching notes")
            print("%4s" % new_v, new_note, fingering(keys))
            # Swap the active note
            midi.send(NoteOff(old_note))
            midi.send(NoteOn(new_note))
    # store the new notes as the old notes
    old_v = new_v
    old_note = new_note
