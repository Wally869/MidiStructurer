from enum import Enum

from .utils import OrderedEnum

ALL_NOTES = [
    "A", "As", "B", "C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs"
]


# Values give the distance between notes in term of halftones
# s denotes a Sharp
class NoteNames(OrderedEnum):
    A = 0
    As = 1
    B = 2
    C = 3
    Cs = 4
    D = 5
    Ds = 6
    E = 7
    F = 8
    Fs = 9
    G = 10
    Gs = 11


class Note(object):
    def __init__(self, Name: str = "A", Octave: int = 5):
        self.Name = Name
        self.Octave = Octave

    def __str__(self):
        return "Note({})".format(self.Name + str(self.Octave))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) is not Note:
            return False
        else:
            if self.Name == other.Name and self.Octave == other.Octave:
                return True
            else:
                return False

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() >= other.ComputeHeight()
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() > other.ComputeHeight()
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() <= other.ComputeHeight()
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.ComputeHeight() < other.ComputeHeight()
        return NotImplemented

    def __add__(self, other: int):
        if type(other) is not int:
            return NotImplemented
        else:
            # error if other is negative. Fixing this
            if (other < 0):
                return self.__sub__(abs(other))
            else:
                currNoteId = self.GetNoteId() + other
                deltaOctave = 0
                while currNoteId >= len(NoteNames):
                    deltaOctave += 1
                    currNoteId -= len(NoteNames)

                return Note(
                    Name=NoteNames[
                        self.GetNoteNameFromNamesEnum(currNoteId)
                    ].name,
                    Octave=self.Octave + deltaOctave
                )

    def __sub__(self, other: int):
        if type(other) != int:
            return NotImplemented
        else:
            if (other < 0):
                return self.__add__(abs(other))
            else:
                currNoteId = self.GetNoteId() - other
                deltaOctave = 0
                # handling negative values
                while currNoteId <= 0:
                    deltaOctave -= 1
                    currNoteId += len(NoteNames)

                return Note(
                    Name=NoteNames[
                        self.GetNoteNameFromNamesEnum(currNoteId)
                    ].name,
                    Octave=self.Octave + deltaOctave
                )

    def GetNoteId(self) -> int:
        for n in NoteNames:
            if n.name == self.Name:
                return n.value
        return KeyError

    def ComputeHeight(self) -> int:
        return self.Octave * 12 + self.GetNoteId()

    # Return distance between this note and another in term of semitones
    def ComputeTonalDistance(self, otherNote) -> int:
        return self.ComputeHeight() - otherNote.ComputeHeight()

    @staticmethod
    def GetNoteNameFromNamesEnum(idNote: int) -> str:
        for n in NoteNames:
            if n.value == idNote:
                return n.name
        return KeyError


def CreateNoteFromHeight(height: int) -> Note:
    octave = height // 12
    name = Note.GetNoteNameFromNamesEnum(height - octave * 12)

    return Note(Name=name, Octave=octave)
