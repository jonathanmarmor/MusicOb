#!/usr/bin/env python2.7

import os
import templates
# from music_format import make_score_music_string


def write_to_file(s, path=None, filename=None, extention=None, full_path=None):  
   if not full_path:
      full_path = os.path.join(path, '{0}.{1}'.format(filename, extention))
   f = open(full_path, 'w')
   f.write(s)
   f.close()
    
def make_score(piece, ly_dir_path, midi_string): # templates)
   main_string = templates.main.format(
                 title=piece.title,
                 composer=piece.composer,
                 emsis_number=piece.emsis_number,
                 staff_size=15)
   strings = [main_string]
   score_music_dir = os.path.join(ly_dir_path, 'score_music')
   os.mkdir(score_music_dir)
   for movement in piece.movements:
      mv_num = movement.movement_number
      movement_dir = os.path.join(score_music_dir, movement.movement_folder_name)
      os.mkdir(movement_dir)
      movement_string = templates.movement.format(
                        movement_title=movement.movement_title,
                        tempo_duration=movement.tempo_duration,
                        tempo_bpm=movement.tempo_bpm,
                        movement_number=movement.movement_number,
                        instrument_name='')
      strings.append(movement_string)
      for instrument in movement.instruments:      
         instrument_string = templates.instrument.format(
                instrument_name=instrument.instrument_name,
                short_instrument_name=instrument.short_instrument_name,
                midi_instrument_name=instrument.midi_instrument_name,
                clef=instrument.clef,
                transpose_from_middle_c='c')
         strings.append(instrument_string)
         music_ly_filename = '{}_music.ly'.format(instrument.music_yaml_file_name)
         music_ly_file_path = os.path.join(movement_dir, music_ly_filename)
         relative_music_ly_file_path = os.path.join('.', 'score_music', movement.movement_folder_name, music_ly_filename)            
         instrument_end_string = templates.instrument_end.format(path_to_music_file=relative_music_ly_file_path)
         strings.append(instrument_end_string)
         music_string = make_score_music_string(instrument.music)
         write_to_file(music_string, full_path=music_ly_file_path)  
      movement_end_string = templates.movement_end.format(midi=midi_string)
      strings.append(movement_end_string)        
   strings.append(templates.main_end.format())
   score_string = ''.join(strings)
   write_to_file(score_string, ly_dir_path, piece.filename, 'ly')


def make_parts(piece, ly_dir_path, midi_string): # templates)
   parts_music_dir = os.path.join(ly_dir_path, 'parts_music')
   os.mkdir(parts_music_dir)  
   for musician in piece.musicians:
      musician_dir = os.path.join(parts_music_dir, musician)
      os.mkdir(musician_dir)
        
      main_string = templates.main.format(title=piece.title,
                                          composer=piece.composer,
                                          emsis_number=piece.emsis_number,
                                          staff_size=20)
      strings = [main_string]
        
      for movement in piece.movements:
         for instrument in movement.instruments:
            if instrument.musician == musician:
               movement_string = templates.movement.format(
                  movement_title=movement.movement_title,
                  tempo_duration=movement.tempo_duration,
                  tempo_bpm=movement.tempo_bpm,
                  movement_number=movement.movement_number,
                  instrument_name=musician)
               strings.append(movement_string)
                    
               instrument_string = templates.instrument.format(
                  instrument_name=instrument.instrument_name,
                  short_instrument_name=instrument.short_instrument_name,
                  midi_instrument_name=instrument.midi_instrument_name,
                  clef=instrument.clef,
                  transpose_from_middle_c=instrument.transpose_from_middle_c)
               strings.append(instrument_string)
                    
               music_ly_filename = '{}_music.ly'.format(movement.movement_folder_name)
               music_ly_file_path = os.path.join(musician_dir, music_ly_filename)
               relative_music_ly_file_path = os.path.join('.', 'parts_music', musician, music_ly_filename)            
                    
               instrument_end_string = templates.instrument_end.format(path_to_music_file=relative_music_ly_file_path)
               strings.append(instrument_end_string)
                    
               music_string = make_score_music_string(instrument.music)
               write_to_file(music_string, full_path=music_ly_file_path)
            else:
               pass
               # what should be done when an instrument isn't playing in a movement?    
         movement_end_string = templates.movement_end.format(midi=midi_string)
         strings.append(movement_end_string)
      strings.append(templates.main_end.format())
      parts_string = ''.join(strings)
      write_to_file(parts_string, ly_dir_path, musician, 'ly')




def format_articulations(articulations):
   artics_list = []
   for a in articulations:
      artic = templates.articulation.format(articulation=a)
      artics_list.append(artic)
   return ''.join(artics_list)

def format_note(note):
   d = get_format_dict(note)
   return templates.note.format(**d)

def format_grace_note(note):
   d = get_format_dict(note)
   
   if note.text_spanner_start:
      d['text_spanner_init_tab'] = '\t'
   else:
      d['text_spanner_init_tab'] = ''    

   if note.tempo_instruction:
      d['tempo_instruction_init_tab'] = '\t'
   else:
      d['tempo_instruction_init_tab'] = ''
       
   d['pitches_tab'] = '\t'
   
   return templates.grace_note.format(**d)


def get_format_dict(note):
   d = {}

   if note.rehearsal_mark:
      d['rehearsal'] = templates.rehearsal.format(rehearsal_text=note.rehearsal_mark)
   else:
      d['rehearsal'] = ''
       
   if note.bar:
      d['bar'] = templates.bar.format(bar_number=note.bar)
   else:
      d['bar'] = ''
       
   if note.time_signature_numerator:
      d['time_signature'] = templates.time_signature.format(numerator=note.time_signature_numerator, 
                                                          denominator=note.time_signature_denominator)
   else:
      d['time_signature'] = ''
       
   if note.text_spanner_start:
      d['text_spanner_init'] = templates.text_spanner_init.format(text_spanner_text=note.text_spanner_start)
      d['start_text_spanner'] = templates.start_text_spanner
   else:
      d['text_spanner_init'] = ''
      d['start_text_spanner'] = ''
       
   if note.text_spanner_stop:
      d['stop_text_spanner'] = templates.stop_text_spanner
   else:
      d['stop_text_spanner'] = ''
       
   if note.tempo_instruction:
      d['tempo_instruction_init'] = templates.tempo_instruction_init
      d['tempo_instruction'] = templates.tempo_instruction.format(tempo_instruction_text=note.tempo_instruction)
   else:
      d['tempo_instruction_init'] = ''
      d['tempo_instruction'] = ''
       
   if note.grace_notes:
      d['grace_notes_init'] = templates.grace_notes_init
      grace_list = []
      for g in note.grace_notes:
          grace_string = format_grace_note(g)
          grace_list.append(grace_string)
      d['grace_notes'] = ''.join(grace_list)
      d['grace_notes_close'] = templates.grace_notes_close
   else:     
      d['grace_notes_init'] = ''
      d['grace_notes'] = ''
      d['grace_notes_close'] = ''
   
   d['pitches'] = note.pitches
   d['duration'] = note.duration
   
   if note.tie:
      d['tie'] = templates.tie
   else:
      d['tie'] = ''
   
   if note.beam == 'start':
      d['beam'] = templates.beam_start
   elif note.beam == 'stop':
      d['beam'] = templates.beam_stop
   else:
      d['beam'] = ''
   
   if note.slur == 'start':
      d['slur'] = templates.slur_start
   elif note.slur == 'stop':
      d['slur'] = templates.slur_stop
   else:
      d['slur'] = ''
   
   if note.articulations:
      d['articulations'] = format_articulations(note.articulations)
   else:
      d['articulations'] = ''
   
   if note.dynamic:
      d['dynamic'] = templates.dynamic.format(dynamic=note.dynamic)   
   else:
      d['dynamic'] = ''
   
   if note.fermata:
      d['fermata'] = templates.fermata
   else:
      d['fermata'] = ''
   
   if note.text_above:
      d['text_above'] = templates.text_above.format(text=note.text_above)
   else:
      d['text_above'] = ''
   
   if note.text_below:
      d['text_below'] = templates.text_below.format(text=note.text_below)
   else:
      d['text_below'] = ''
   
   if note.breathe:
      d['breathe'] = templates.breathe
   else:
      d['breathe'] = ''
       
   return d


def make_score_music_string(music):    
   music_string_list = []
   music_string_list.append(templates.page_start)
   for note in music:
      note_string = format_note(note)
      music_string_list.append(note_string)
   music_string_list.append(templates.page_end)
   music_string = ''.join(music_string_list)
   return music_string




def ob2ly(piece, ly_dir_path, score=True, parts=False, midi=False): # template='emsis'   
   if not midi:
      midi_string = '%'
   else:
      midi_string = ' '
           
#    if template == 'standard':
#        templates = standard
#    elif template == 'emsis':
#        templates = emsis
    
   if score:
      make_score(piece, ly_dir_path, midi_string) # templates)
   if parts:
      make_parts(piece, ly_dir_path, midi_string) # templates)


   

def test():
   pass

if __name__ == '__main__':
   test()
