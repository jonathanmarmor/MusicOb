"""

>>> from musicob.music import Piece, Note
>>> import random
>>> piece_template = '/path/to/music/yaml/' # Piece, one Movement, one Instrument, no notes, all metadata
>>> p = Piece(piece_template)
>>> for x in range(100):
...    n = Note()
...    pitch = random.choice(0, 127)
...    n.pitches = [pitch]
...    n.duration = random.randint(1, 24) # sixteenth note through dotted whole note
...    p.movements[0].instruments[0].music.append(n)
>>> p.write(music_yaml=True, notation_yaml=True, ly=True, pdf=True, midi=True, score=True, parts=True)


"""



class Piece(object):
   pass

class Movement(object):
   pass

class Instrument(object):
   pass

class Note(object):
   pass


class MusicToNotation(object):
   def __init__(self, music_piece):
      self.pc_names = ['c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', 'aes', 'a', 'bes', 'b']
      

   def pitch(self, midi):
      pc = midi % 12
      name = self.pc_names[pc]
      octave = get_lily_octave(midi)
      return name + octave

   def get_lily_octave(self, midi):
      ticks = (midi / 12) - 4
      if ticks >= 0:
         return "'" * ticks
      if ticks < 0:
         return "," * abs(ticks)

   def translate(self, music_piece):
      notation_piece = notation.Piece()
      notation_piece.title = music_piece.title
      notation_piece.filename = music_piece.filename
      notation_piece.composer = music_piece.composer
      notation_piece.emsis_number = music_piece.emsis_number

      for m in music_piece.movements:
