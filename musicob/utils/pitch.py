"""Utils for converting pitch data.

Large parts of this module are taken from the music21 pitch.py module
http://mit.edu/music21/

E0 -- Theoretical lowest audible pitch
    fq = 10.300861153527183
    ps = 4.0
    (pc=4, octave=-1)
D#10 -- Theoretical highest audible pitch
    fq = 19912.12695821318
    ps = 135.0
    (pc=3, octave=10)

# Initialize with Pitch Space
>>> Pitch(ps=12)
Pitch(ps=12, octave=0, pc=0, cent=0, fq=16.3515978313)

# Initialize with octave, pitchclass, and cent
>>> Pitch(octave=4, pc=9, cent=4)
Pitch(ps=69.04, octave=4, pc=9, cent=4, fq=441.017791211)

# Initialize with frequency
>>> Pitch(fq=440)
Pitch(ps=69.0, octave=4, pc=9, cent=0, fq=440)

# Check attributes
>>> p = Pitch(ps=105.4)
>>> p
Pitch(ps=105.4, octave=7, pc=9, cent=40, fq=3602.27609983)

>>> p.ps
105.4

>>> p.octave
7

>>> p.pc
9

>>> p.cent
40

>>> p.fq
3602.2760998286485

>>> p.pc_name
'A+40'

>>> p.name
'7A+40'

>>> p.ly_pc
'a'

>>> p.ly_octave
"''''"

>>> p.ly
"a''''"

>>> p.transpose(5)
Pitch(ps=110.4, octave=8, pc=2, cent=40, fq=4808.46170378)

# initialize with Pitch Space float
>>> Pitch(ps=12.5)
Pitch(ps=12.5, octave=0, pc=0, cent=50, fq=16.8307362204)

"""

import math


PC_NAMES = {
    'sharps': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
    'flats': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
}
LY_PC_NAMES = {
    'sharps': ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais',
        'b'],
    'flats': ['c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', 'aes', 'a', 'bes',
        'b']
}
LY_OCTAVES = [",,,", ",,", ",", '', "'", "''", "'''", "''''", "'''''",
    "''''''", "'''''''", ',,,,']  # -1 is four commas


class PitchInitError(Exception):
    pass


class Pitch(object):
    def __init__(self, ps=None, octave=None, pc=None, cent=0, fq=None,
        a440=440.0):
        if ps != None:
            self.ps = ps
            self.octave = self.ps_to_octave(ps)
            self.pc = self.ps_to_pc(ps)
            self.cent = self.ps_to_cent(ps)
            self.fq = self.ps_to_fq(ps, a440=a440)
        elif pc != None and octave != None:
            self.ps = self.octave_pc_cent_to_ps(pc, octave, cent)
            self.octave = octave
            self.pc = pc
            self.cent = cent
            self.fq = self.ps_to_fq(self.ps, a440=a440)
        elif fq != None:
            self.ps = self.fq_to_ps(fq, a440=a440)
            self.octave = self.ps_to_octave(self.ps)
            self.pc = self.ps_to_pc(self.ps)
            self.cent = self.ps_to_cent(self.ps)
            self.fq = fq
        else:
            msg = 'ps={}, octave={}, pc={}, cent={}, fq={}'
            msg = msg.format(ps, octave, pc, cent, fq)
            raise PitchInitError(msg)

        self.pc_name = self.pc_to_name(self.pc, self.cent)
        self.name = str(self.octave) + self.pc_name
        self.ly_pc = self.get_ly_pc(self.pc)
        self.ly_octave = self.get_ly_octave(self.octave)
        self.ly = self.ly_pc + self.ly_octave

    def __repr__(self):
        msg = 'Pitch(ps={}, octave={}, pc={}, cent={}, fq={})'
        msg = msg.format(self.ps, self.octave, self.pc, self.cent, self.fq)
        return msg

    @classmethod
    def ps_to_pc(cls, ps):
        return int(math.floor(ps % 12))

    @classmethod
    def ps_to_octave(cls, ps):
        return int(math.floor(ps / 12.0)) - 1

    @classmethod
    def ps_to_cent(cls, ps):
        return int(round((ps % 1), 2) * 100)

    @classmethod
    def octave_pc_cent_to_ps(cls, pc, octave, cent):
        return pc + (cent / 100.0) + ((octave + 1) * 12)

    @classmethod
    def ps_to_fq(cls, ps, a440=440.0):
        try:
            fq = a440 * (2.0 ** (((ps - 60.0) - 9.0) / 12.0))
        except OverflowError:
            fq = 0
        return fq

    @classmethod
    def fq_to_ps(cls, fq, a440=440.0):
        return 12 * (math.log(fq / a440) / math.log(2)) + 69

    @classmethod
    def pc_to_name(cls, pc, cent, accidentals='sharps'):
        name = PC_NAMES[accidentals][pc]
        if cent:
            name = '{}+{}'.format(name, cent)
        return name

    @classmethod
    def get_ly_pc(cls, pc, accidentals='sharps'):
        return LY_PC_NAMES[accidentals][pc]

    @classmethod
    def get_ly_octave(cls, octave):
        return LY_OCTAVES[octave]


    # @todo: comparison methods
    # @todo: methods to return pitches specified intervals away

    def transpose(self, steps):
        """Quick method to return a new Pitch `steps` half steps from self."""
        return Pitch(ps=self.ps + steps)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
