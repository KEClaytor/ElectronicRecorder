# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# midi_UARToutdemo.py - demonstrates sending MIDI notes

import time
import board
import busio
import digitalio

import adafruit_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=1,
    out_channel=0,
    debug=False,
)
note_hold = 0.85
rest = note_hold / 5

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


from adafruit_midi.midi_message import MIDIMessage, note_parser
class InstrumentSelct(MIDIMessage):
    """Instrument Select MIDI message
    NOTE: This requires a channel to have already been selected.
    There are three ways to select an instrument:
        - 0xB0 - 0x00 - 0x05 (MSB sound bank selection)
        - 0xB0 - 0x20 - 0x01 (LSB sound bank selection)
        - 0xC0 - 0x02 (sound selection in the current sound bank)
        (https://www.cs.cmu.edu/~music/cmsip/readings/MIDI%20tutorial%20for%20programmers.html)
    This uses the last method:
        - channel message: 0x80 note off, 0x90 note on, **0xc0 program**, 0xe0 pitch wheel
        (http://www.vlsi.fi/fileadmin/datasheets/vs1053.pdf)
    TODO: Generalize this so we don't have to play a note first.
    :param int instrument: The instrument to select - see lookup table.
    """

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

old_v = 0
old_note = 0

# Play a note first, to select the channel
midi.send(NoteOn(40, 80))
time.sleep(0.5)
midi.send(NoteOff(40, 80))
# Now we can use the instrument select
midi.send(InstrumentSelct(75)) # Select recorder

while True:
    # Poll the new value
    new_v = poll(keys)
    # Debug: print the fingering
    # print("%4s" % new_v, fingering(keys))
    # On a note change play the new note
    if not (new_v == old_v):
        # Turn off the old note
        print("turning off...")
        midi.send(NoteOff(old_note, 0))
        # Turn on the new note
        try:
            new_note = notes[new_v]
            print("%4s" % new_v, new_note, fingering(keys))
            midi.send(NoteOn(new_note, 80))
        except KeyError as ex:
            new_note = 0
            print("Fingering not found!")
        # store the new notes as the old notes
        old_v = new_v
        old_note = new_note
    # time.sleep(0.1)