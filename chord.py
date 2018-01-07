# blah
from typing import List, Tuple, Union
from functools import reduce
from operator import eq

# define some handy dandy types
noteType = Union['ChordNote', None]


class ChordNote:
    def __init__(self, note: int, prev: noteType, next: noteType):
        """
        Node in circular data structure for a chord
        """
        self.note = note
        self.prev = prev
        self.next = next

    @classmethod
    def _init_notes_rec(cls,
                       first: noteType,
                       prev: noteType,
                       remaining_notes: List[int]
                       ) -> Tuple['ChordNote', 'ChordNote']:
        """
        recursively initialize notes
        :return: the next note in the chord
        """
        if len(remaining_notes) == 0:
            return first, prev
        curr = cls(remaining_notes[0], prev, None)
        curr.next, last = cls._init_notes_rec(first, curr, remaining_notes[1:])
        return curr, last

    @classmethod
    def from_list(cls, notes: List[int]) -> noteType:
        """
        creates a circle chord from a list of notes
        :return: the first note in the list
        """
        first = cls(notes[0], None, None)
        second, last = cls._init_notes_rec(first, first, notes[1:])
        first.next = second
        first.prev = last
        return first

    def __iter__(self):
        note = self
        while True:
            yield note.note
            note = note.next
            if note is self:
                break

    def __repr__(self):
        """
        just shows the chord like a list
        """
        return str(list(self))


class AbstractChord:
    def __init__(self, notes: List[int]):
        if len(notes) == 0:
            raise ValueError('chord must have length greater than 0!')
        # Do we enforce the format / order of the input list?
        self.notes = ChordNote.from_list(notes)
        self.length = len(notes)

    def __len__(self):
        return self.length

    def _itereq(self, other):
        """
        is the particular
        :param other:
        :return:
        """
        if len(self) != len(other):
            return False
        # NOT RIGHT...
        reduce((lambda a, b: a and b), [a == b for a, b in zip(self.notes, other.notes)])


