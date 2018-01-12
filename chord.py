import re
import copy
from typing import List, Union
from enum import IntEnum
from collections import namedtuple


sharp = u"\u266F"
flat = u"\u266D"


class NoSuchChordException(ValueError):
    def __init__(self, message, chord: 'FullChord', *args):
        self.message = message
        self.chord = chord
        super().__init__(message, chord, *args)


class Note(IntEnum):
    C = 0
    Cs = 1
    Df = 1
    D = 2
    Ds = 3
    Ef = 3
    E = 4
    F = 5
    Fs = 6
    Gb = 6
    G = 7
    Gs = 8
    Af = 8
    A = 9
    As = 10
    Bf = 10
    B = 11
    Cf = 11

    def pretty_name(self):
        if 's' in self.name:
            return self.name[0] + sharp
        if 'f' in self.name:
            return self.name[0] + flat
        return self.name


class SpecificNote:
    """
    A note with a numbered octave
    """
    def __init__(self, note: 'Note', octave: int):
        self.note = note
        self.octave = octave

    def __repr__(self):
        return repr((self.note, self.octave))

    def __lt__(self, other):
        """
        sort from lowest to highest
        """
        return self.octave < other.octave and self.note < other.note

    def add_interval(self, interval: int):
        """
        Note: returns a NEW note
        """
        new_note = (self.note.value + interval) % 12
        new_octave = self.octave + (self.note + interval) // 12
        return SpecificNote(Note(new_note), new_octave)

    def shift_interval(self, interval: int):
        """
        shifts note by interval
        """
        new_note = (self.note + interval) % 12
        self.octave = self.octave + (self.note + interval) // 12
        self.note = Note(new_note)
        return self


class CompressedChord:
    def __init__(self, bin_notes: str):
        """
        takes a binary representation of a chord and allows operations

        Compressed because we don't care about octaves, only notes
        """
        assert len(bin_notes) == 12, 'str must be length 12'
        # notes is a list of booleans
        self.notes = list(map(lambda x: int(x) == 1, bin_notes))
        self._hash = bin_notes

    def __hash__(self):
        return self._hash.__hash__()

    @classmethod
    def from_int(cls, bin_notes: int):
        str_notes = bin(bin_notes)[2:]
        str_notes = '0' * (12 - len(str_notes)) + str_notes
        return cls(str_notes)

    @classmethod
    def from_notes(cls, notes: List['Note']):
        chord = ['0'] * 12
        for note in notes:
            chord[note] = '1'
        return cls(''.join(chord))

    @classmethod
    def from_specific_notes(cls, specific_notes: List['SpecificNote']):
        return cls.from_notes(list(map(lambda x: x.note, specific_notes)))

    @classmethod
    def from_full_chord(cls, chord: 'FullChord'):
        return cls.from_specific_notes(chord.notes)

    @staticmethod
    def rotate(notes: List[bool]):
        """
        rotates to the right
        """
        tail = notes.pop()
        notes.insert(0, tail)

    def match_type(self, other: 'CCompressedChord') -> Union[None, 'Note']:
        """
        If the chords don't match, return None. Otherwise, return the tonic
        """
        for step, rotation in enumerate(self):
            if rotation == other.notes:
                return Note((other.tonic - step) % 12)
        return None

    def __iter__(self):
        """
        iterating yields all possible orientations of a chord
        """
        notes = copy.copy(self.notes)
        for i in range(12):
            yield notes
            self.rotate(notes)

    def __eq__(self, other):
        return self.notes == other.notes


class CCompressedChord(CompressedChord):
    """
    a compressed chord with tonic of C
    """
    def __init__(self, bin_notes: str):
        self.tonic = Note.C
        super().__init__(bin_notes)


ChordTypeName = namedtuple('ChordName', ['name', 'abv'])


chord_types = [
    # major chords
    ('100010010000', 'major', ''),

    ('100010010001', 'major seven', 'maj7'),
    ('100010000001', 'major seven (no 5)', 'maj7'),

    ('101010010001', 'major nine', 'maj9'),
    ('101010000001', 'major nine (no 5)', 'maj9'),

    ('101010010101', 'major thirteen', 'maj13'),
    ('101010000101', 'major thirteen (no 5)', 'maj13'),
    ('100010010101', 'major thirteen (no 9)', 'maj13'),
    ('101011010101', 'major thirteen (but you\'d be happier without the 11)', 'maj13'),

    ('100010010100', 'six', '6'),
    # ('100010000100', 'six (no 5)', '6'),

    ('101010010100', 'six/nine', '6/9'),
    ('101010000100', 'six/nine (no 5)', '6/9'),

    ('101010011001', 'major seven flat 6', 'maj7b6'),

    ('101010010000', 'major add nine', 'add9'),
    ('100010010100', 'major add thirteen', 'add13'),

    # dominant chords
    ('100010010010', 'seven', '7'),

    ('101010010010', 'nine', '9'),

    ('101010010110', 'thirteen', '13'),
    ('101010000110', 'thirteen (no 5)', '13'),
    ('100010010110', 'thirteen (no 9)', '13'),

    ('110010010010', 'seven flat 9', '7b9'),
    ('100110010010', 'seven sharp 9', '7#9'),

    # suspended chords
    ('100001010000', 'suspended four', 'sus4'),

    ('101000010000', 'suspended two', 'sus2'),
    ('101000000000', 'suspended two (no 5)', 'sus2'),

    ('100001010010', 'seven suspended four', '7sus4'),
    ('100001000010', 'seven suspended four (no 5)', '7sus4'),

    ('101001010010', 'eleven', '11'),
    ('101001000010', 'eleven (no 5)', '11'),
    ('100001010010', 'eleven (no 9)', '11'),
    ('101011010010', 'eleven (but you\'d be happier with no third)', '11'),

    ('110001010000', 'flat nine suspended', 'b9sus'),
    ('110001000000', 'flat nine suspended (no 5)', 'b9sus'),

    # minor chords
    ('100100010000', 'minor', 'm'),

    ('100100010010', 'minor seven', 'm7'),
    ('100100000010', 'minor seven (no 5)', 'm7'),

    ('100100010001', 'minor/major seven', 'mM7'),
    ('100100000001', 'minor/major seven (no 5)', 'mM7'),

    ('100100010100', 'minor six', 'm6'),
    ('100100000100', 'minor six (no 5)', 'm6'),

    ('101100010010', 'minor nine', 'm9'),
    ('101100000010', 'minor nine (no 5)', 'm9'),

    ('101101010010', 'minor eleven', 'm11'),
    ('101101000010', 'minor eleven (no 5)', 'm11'),

    ('101100010110', 'minor thirteen', 'm13'),
    ('101100000110', 'minor thirteen (no 5)', 'm13'),
    ('100100010110', 'major thirteen (no 9)', 'maj13'),
    # ('101101010110', 'major thirteen (but you\'d be happier without the 11)', 'maj13'),

    ('101100010000', 'minor add nine', 'madd9'),
    ('100100010100', 'minor add thirteen', 'madd13'),

    # diminished chords
    ('100100100000', 'diminished', 'dim'),
    ('100100100100', 'diminished seven', 'dim7'),
    ('100100100010', 'half-diminished', 'm7b5'),

    # augmented chords
    ('100010001000', 'augmented', 'aug'),
    ('100010001001', 'augmented 7', '7#5'),

    # other chords
    ('100000010000', 'five', '5'),

    ]
chord_types = {CCompressedChord(notes): ChordTypeName(name, abv) for notes, name, abv in chord_types}


class ChordName:
    """
    basic chord info, type and note

    Just used for outputting strings
    """
    def __init__(self, chord_type: 'CompressedChord', note: 'Note'):
        self.name, self.abv = chord_types[chord_type]
        self.note = note.pretty_name()

    def __str__(self):
        return '{}{}'.format(self.note, self.abv)

    def long_name(self):
        return '{} {}'.format(self.note, self.name)


class FullChord:
    def __init__(self, notes: List[SpecificNote]):
        self.notes = notes

    def get_matches(self):
        """
        returns all possible chord matches as a list
        """
        chords = []
        compressed_chord = CompressedChord.from_full_chord(self)
        for chord_type in chord_types:
            tonic = compressed_chord.match_type(chord_type)
            if tonic is not None:
                chords.append(ChordName(chord_type, tonic))
        return chords

    def __iter__(self):
        """
        returns all possible compressed chord matches
        """
        for c in self.get_matches():
            yield c


class StringedThing:
    """
    represents a stringed instrument
    """
    def __init__(self, strings: List[SpecificNote]):
        self.strings = strings

    def parse_input(self, chord_str: str) -> List[int]:
        """
        takes something like '332010x and turns it into [3, 3, 2, 0, 1, 0, None]
        """
        # deal with space separated case
        if len(chord_str.split()) == len(self.strings):
            chord_str = chord_str.split
        else:
            assert len(chord_str) == len(self.strings), 'input must have length {}'.format(len(self.strings))
        frets = []
        for note_str in chord_str:
            if note_str == 'x' or note_str == 'X':
                frets.append(None)
                continue
            try:
                fret = int(note_str)
            except ValueError as e:
                e.message = 'invalid character {}'.format(note_str)
                raise
            frets.append(fret)
        return frets

    def get_chords(self, chord_str: str):
        """
        takes a list of frets and outputs a chord
        """
        frets = self.parse_input(chord_str)
        full_notes = [note.add_interval(fret)
                      for note, fret in zip(self.strings, frets)
                      if fret is not None]
        return FullChord(full_notes)


def parse_tuning(tuning) -> List['SpecificNote']:
    def parse_note(full_note):
        match = re.search('(?P<note>[A-Ga-g])(?P<octave>[0-9]*)', full_note).groupdict()
        return SpecificNote(Note[match['note']], int(match['octave']))
    notes = tuning.split()
    return list(map(parse_note, notes))


class Interactive:
    def __init__(self):
        standard = 'E2 A3 D3 G3 B4 E4'
        self.instrument = StringedThing(parse_tuning(standard))

    def main_loop(self):
        while True:
            print('Enter a chord')
            text = input()
            if text == 'quit':
                print('Goodbye!')
                exit(0)
            try:
                full_chord = self.instrument.get_chords(text)
                out = list(full_chord)
                if len(out) == 0:
                    print('sucks, no matches')
                else:
                    for choice in out:
                        print(choice.long_name())
            except Exception as e:
                print('Whoops! you messed up\n')
                print(e)

    def change_instrument(self):
        while True:
            print('enter the names of the notes of the strings in order from left to right.\n'
                  '\n'
                  'for example, guitar looks like \'E2 A3 D3 G3 B4 E4\'\n'
                  '\n'
                  'To cancel, just hit <enter>.')
            strings = input()
            if strings == '':
                return
            try:
                strings = parse_tuning(strings)
                self.instrument = StringedThing(strings)
            except Exception as e:
                print('Whoops! you messed up')
                print(e)
                pass

    def welcome(self):
        print('Welcome to the awesome chord namer tool thingy\n'
              '\n'
              'The default instrument is guitar. Do you want to change this?\n'
              'Type \'yes\' to change, or type anything else to not change\n')
        answer = input("change instrument?")
        if answer == 'yes':
            self.change_instrument()
        print("Now you're ready to start! enter the frets of the chord from left to right\n"
              "\n"
              "for example E major on guitar could look like:\n"
              "     '022100' or\n"
              "     '0 2 2 1 0 0' or even\n"
              "     '0 2 2 1 0 X'")
        self.main_loop()


if __name__ == '__main__':
    console = Interactive()
    console.welcome()


# TODO:
# - remember how many times we rotate so that we know what key the chord is in
# do command line stuff
