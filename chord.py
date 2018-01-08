from typing import List, Tuple, Union
from enum import IntEnum
from collections import namedtuple

# define some handy dandy types
noteType = Union['ChordNote', None]


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
        new_note = (self.note + interval) % 12
        new_octave = self.octave + (self.note + interval) // 12
        return self.__init__(Note(new_note), new_octave)

    def shift_interval(self, interval: int):
        """
        shifts note by interval
        """
        new_note = (self.note + interval) % 12
        self.octave = self.octave + (self.note + interval) // 12
        self.note = new_note
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
        rotates to the left
        """
        tail = notes.pop()
        notes.insert(0, tail)

    def match_type(self, other: 'CCompressedChord') -> Union[None, 'Note']:
        """
        If the chords don't match, return None. Otherwise, return the tonic
        """
        for step in range(12):
            if self == other:
                return Note((other.tonic + step) % 12)
        return None



    def __iter__(self):
        """
        iterating yields all possible orientations of a chord
        """
        notes = self.notes
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


ChordName = namedtuple('ChordName', ['name', 'abv'])


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
    ('100010000100', 'six (no 5)', '6'),

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
    ('100001000000', 'suspended four (no 5)', 'sus4'),

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
    ]
chord_types = {CompressedChord(notes): ChordName(name, abv) for notes, name, abv in chord_types}


class FullChord:
    def __init__(self, notes: List[SpecificNote]):
        self.notes = notes

    def get_type(self) -> Tuple['CompressedChord', 'Note']:
        compressed_chord = CompressedChord.from_full_chord(self)
        for chord_type in chord_types:
            tonic = compressed_chord.match_type(chord_type)
            if tonic:
                return chord_type, tonic
        raise NoSuchChordException('eat cock', chord=self)

    def get_full_name(self):
        comp_chord, tonic = self.get_type()
        return tonic.name + ' ' + chord_types[comp_chord].name


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
        assert len(chord_str) == len(self.strings), 'input must have length {}'.format(self.strings)
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

    def get_chord(self, chord_str: str):
        """
        takes a list of frets and outputs a chord
        """
        frets = self.parse_input(chord_str)
        full_notes = [note.add_interval(fret) for note, fret in zip(self.strings, frets)]

        return FullChord(full_notes)


# TODO:
# - remember how many times we rotate so that we know what key the chord is in
# do command line stuff
