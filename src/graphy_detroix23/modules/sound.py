"""
# Graphy.
/src/graphy_detroix23/modules/sound.py

Sounds for `pyxel`, using Music Macro Language.
"""

from typing import Final

_MML_EXAMPLE = """
'T133 L8 @ENV1{0,0,127,60,102,10,0} Q88 V96 @2 @ENV1 @VIB0 O4B2&8>GGD C8.<B8.A>C4C4 D2&8<GB16B8. 
R4.>C<BA>CC <B2&8>GGD C8.<B8.A>C4C4 D4&16<G16A16B16>D2 <A4.>F16<F16A4.>D16<A16', 

'T133 L16 @ENV1{127} @VIB1{60,20,25} Q88 V112 @0 @ENV1 @VIB1 O2G8>GR<G8>GR<G8>GR<G8>GR 
[<F8>FR<F8>FR<F8>FR<F8>FR<G8>GR<G8>GR<G8>GR<G8>GR]3 <F8>FR<F8>FR<F8>FR<F>F<F8', 

'T133 L8 @ENV1{0,0,127,60,102,10,0} Q88 V32 @2 @ENV1 @VIB0 O4A16B2&8>GGD16& D16C8.<B8.A>C4C8.& 
C16D2&8<GB16B& B16R4.>C<BA>CC16& C16<B2&8>GGD16& D16C8.<B8.A>C4C8.& C16D4&16<G16A16B16>D4.&16& D16<A4.>F16<F16A4.>D16', 

'T133 L16 @ENV1{127} Q100 V112 @0 @ENV1 @VIB0']
"""

DEGREES: Final[list[str]] = ["A", "B", "C", "D", "E", "F", "G"]
NOTE: Final[list[str]] = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
NOTE_REVERSED: Final[list[str]] = ['G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C', 'B', 'A#', 'A']
# Bi-directional arpeggio.
BIARPEGGIO: Final[list[str]] = NOTE[1:] + NOTE_REVERSED[1:]
print(BIARPEGGIO)

class MML:
    """
    # `MML` Music Macro Language music generator.
    """
    tempo: int
    division: int
    length: int
    velocity: int
    notes: list[str]

    def __init__(self, tempo: int, division: int, length: int, velocity: int, notes: list[str]) -> None:
        self.tempo = tempo
        self.division = division
        self.length = length
        self.velocity = velocity
        self.notes = notes
    
    def __str__(self) -> str:
        """
        Return a correct MML string.
        """
        return f"T{self.tempo} L{self.division} Q{self.length} V{self.velocity} {' '.join(self.notes)}"
