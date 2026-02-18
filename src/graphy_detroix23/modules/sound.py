"""
# Graphy.
/src/graphy_detroix23/modules/sound.py

Sounds for `pyxel`, using Music Macro Language.
"""

import enum
from typing import Final

import pyxel

_MML_EXAMPLE = """
'T133 L8 @ENV1{0,0,127,60,102,10,0} Q88 V96 @2 @ENV1 @VIB0 O4B2&8>GGD C8.<B8.A>C4C4 D2&8<GB16B8. 
R4.>C<BA>CC <B2&8>GGD C8.<B8.A>C4C4 D4&16<G16A16B16>D2 <A4.>F16<F16A4.>D16<A16', 

'T133 L16 @ENV1{127} @VIB1{60,20,25} Q88 V112 @0 @ENV1 @VIB1 O2G8>GR<G8>GR<G8>GR<G8>GR 
[<F8>FR<F8>FR<F8>FR<F8>FR<G8>GR<G8>GR<G8>GR<G8>GR]3 <F8>FR<F8>FR<F8>FR<F>F<F8', 

'T133 L8 @ENV1{0,0,127,60,102,10,0} Q88 V32 @2 @ENV1 @VIB0 O4A16B2&8>GGD16& D16C8.<B8.A>C4C8.& 
C16D2&8<GB16B& B16R4.>C<BA>CC16& C16<B2&8>GGD16& D16C8.<B8.A>C4C8.& C16D4&16<G16A16B16>D4.&16& D16<A4.>F16<F16A4.>D16', 

'T133 L16 @ENV1{127} Q100 V112 @0 @ENV1 @VIB0']
"""
"""Example of an MML string."""

DEGREES: Final[list[str]] = ["A", "B", "C", "D", "E", "F", "G"]
NOTE: Final[list[str]] = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_REVERSED: Final[list[str]] = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']
BIARPEGGIO: Final[list[str]] = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#",
    'B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#',
]
"""
Bi-directional arpeggio, from _A♯_, by _G_, to _A_.
"""

class Signature(enum.Enum):
    """
    # Key `Signature`.
    Enumerate:
    - `NONE`.
    - `SHARP` **♯**.
    - `FLAT` **♭**.
    """
    NONE = 0
    SHARP = 1
    FLAT = 2


class Note:
    """
    # Single MML `Note`.
    Parameters:
    - `octave` how many octaves above (>0) or under (<0)
    """
    OCTAVE_ABOVE: str = ">"
    OCTAVE_UNDER: str = "<"

    octave: int
    degree_index: int
    signature: Signature
    _note_index: int

    def __init__(
        self, 
        degree_index: int | str,
        octave: int = 0, 
        signature: Signature = Signature.NONE
    ) -> None:
        self.octave = octave
        if isinstance(degree_index, str):
            self.degree_index = DEGREES.index(degree_index)
        else:
            self.degree_index = degree_index
        
        self.signature = signature
        self._note_index = self.degree_index
        if self.signature == Signature.FLAT:
            self.increment_pitch(-1)
        elif self.signature == Signature.SHARP:
            self.increment_pitch(1)

    def __str__(self) -> str:
        octave: str = ""
        if self.octave > 0:
            octave = self.OCTAVE_ABOVE * self.octave
        elif self.octave < 0:
            octave = self.OCTAVE_UNDER * abs(self.octave)

        return f"{octave}{self.note}"

    @property
    def note(self) -> str:
        """
        Returns the `str` representation of the _note_, without octave.
        """
        """
        signature: str = ""
        if self.signature == Signature.FLAT:
            signature = "-"
        elif self.signature == Signature.SHARP:
            signature = "#"
        
        return f"{self.degree}{signature}"
        """
        return NOTE[self._note_index]

    @property
    def degree(self) -> str:
        """
        Get the letter from `degree_index`.
        """
        return DEGREES[self.degree_index]

    def increment_pitch(self, value: int) -> None:
        """
        Increment the _note_ by a `value`, and eventually the `octave`.
        """
        index: int = self._note_index + value
        self.octave += index // len(NOTE)
        self._note_index = index % len(NOTE)

    def increment_degree(self, value: int) -> None:
        """
        Increment the `degree` by a `value`.
        """
        self.degree_index = (self.degree_index + value) % len(DEGREES)


class MML:
    """
    # `MML` Music Macro Language music generator.
    """
    channel: int
    tempo: int
    division: int
    length: int
    velocity: int
    notes: list[Note]
    loop: bool

    def __init__(
        self,
        channel: int, 
        tempo: int, 
        division: int, 
        length: int,
        velocity: int, 
        notes: list[Note],
        loop: bool = False,
    ) -> None:
        self.channel = channel
        self.tempo = tempo
        self.division = division
        self.length = length
        self.velocity = velocity
        self.notes = notes
        self.loop = loop
    
    def __str__(self) -> str:
        """
        Return a correct MML string.
        """
        return f"T{self.tempo} L{self.division} Q{self.length} V{self.velocity} {self.notes_expression()}"

    def notes_expression(self) -> str:
        """
        Get a `str` of all the notes.
        """
        return " ".join([str(note) for note in self.notes])

    def play(self) -> None:
        """
        Use `pyxel` to `play` the MML string.
        """
        pyxel.play(self.channel, self.__str__(), loop=self.loop)
    

class Incrementing(MML):
    """
    # `Incrementing` pitch MML sequence. 
    """
    start_note: Note
    pitch_increment: int
    loop_length: int

    def __init__(
        self, 
        channel: int, 
        tempo: int, 
        division: int, 
        length: int, 
        velocity: int, 
        start_note: Note,
        pitch_increment: int,
        loop_length: int,
        loop: bool = False,
    ) -> None:
        super().__init__(channel, tempo, division, length, velocity, [start_note], loop)
        self.start_note = start_note
        self.pitch_increment = pitch_increment
        self.loop_length = loop_length
    
    def play(self) -> None:
        """
        Use `pyxel` to `play` the MML string and update the next note.
        """
        pyxel.play(self.channel, self.__str__(), loop=self.loop)
        self.notes[0].increment_pitch(self.pitch_increment)

        print(str(self.notes[0]))