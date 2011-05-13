#!/usr/bin/env python2.7

"""Creates PDF music notataion from LilyPond files created by musicob.notation.

ly_dir_path:  The full path to the lilypond files used as input.
pdf_dir_path:  The full path where pdf output files will be written.
piece_filename:  The name of main score lilypond file (sans .ly extension).
score:  If True, the pdf files for the score will be created.  
    Default is True.
parts:  If True, the pdf files for all instruments' parts will be 
    created.  Default is False.

"""


import subprocess
import os

        
class LilyPondToPdf(object):
   def __init__(self, ly_dir_path, pdf_dir_path, piece_filename, score=True, parts=False):
      if not os.path.isdir(pdf_dir_path):
         os.mkdir(pdf_dir_path)
      input_filenames = os.listdir(ly_dir_path)
      if score:
         i = input_filenames.index('{}.ly'.format(piece_filename))
         score_filename = input_filenames.pop(i)
         score_path = os.path.join(ly_dir_path, score_filename)
         self.run_lilypond(score_path, pdf_dir_path)        
      if parts:
         parts_filenames = [f for f in input_filenames if f[-3:] == '.ly']
         for part_filename in parts_filenames:
            part_path = os.path.join(ly_dir_path, part_filename)
            self.run_lilypond(part_path, pdf_dir_path)
      self.cleanup(pdf_dir_path)

   def run_lilypond(self, in_file, pdf_dir_path):
      process = subprocess.Popen(['lilypond', '--output={}'.format(pdf_dir_path), in_file], shell=False)
      process.wait()

   def cleanup(self, pdf_dir_path):
      filenames = [f for f in os.listdir(pdf_dir_path) if f[-3:] == '.ps']
      for filename in filenames:
         file_to_delete = os.path.join(pdf_dir_path, filename)
         subprocess.Popen(['rm', file_to_delete], shell=False)   

if __name__ == '__main__':
   import argparse
   parser = argparse.ArgumentParser(description='Creates PDF music notataion from LilyPond files.', 
                                    epilog='Default makes score but not parts')
    
   parser.add_argument('ly_dir_path', help='path to input directory containing lilypond files')
   parser.add_argument('pdf_dir_path', help='path to output directory for pdf files')
   parser.add_argument('piece_filename', help='the filename of the piece')
   parser.add_argument('-s', '--score', action='store_true', dest='score', help='make the score pdf file')
   parser.add_argument('-p', '--parts', action='store_true', dest='parts', help='make the parts lilypond files')
   args = parser.parse_args()

   LilyPondToPdf(args.ly_dir_path, args.pdf_dir_path, args.piece_filename, score=args.score, parts=args.parts)
