import os
import emsis_templates as templates
#from templates import emsis, standard
# from musicob.notation.objects import yaml2ob
from music_format import make_score_music_string


def write_to_file(s, path=None, filename=None, extention=None, full_path=None):  
    if not full_path:
        filepath = os.path.join(path, '{0}.{1}'.format(filename, extention))
    else:
        filepath = full_path
    f = open(filepath, 'w')
    f.write(s)
    f.close()
    
def make_score(piece, ly_dir_path, midi_string): # templates)
    main_string = templates.main.format(
            title=piece.title,
            composer=piece.composer,
            emsis_number=piece.emsis_number,
            staff_size=15
        )
    strings = [main_string]
    score_music_dir = os.path.join(ly_dir_path, 'score_music')
    os.mkdir(score_music_dir)
    for movement in piece.movements:
        mv_num = movement.movement_number
        movement_dir = os.path.join(score_music_dir, 
                                    movement.movement_folder_name)
        os.mkdir(movement_dir)
        
        movement_string = templates.movement.format(
            movement_title=movement.movement_title,
            tempo_duration=movement.tempo_duration,
            tempo_bpm=movement.tempo_bpm,
            movement_number=movement.movement_number,
            instrument_name=''
        )
        strings.append(movement_string)
        
        for instrument in movement.instruments:
            
            instrument_string = templates.instrument.format(
                instrument_name=instrument.instrument_name,
                short_instrument_name=instrument.short_instrument_name,
                midi_instrument_name=instrument.midi_instrument_name,
                clef=instrument.clef,
                transpose_from_middle_c='c'
            )
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
        
        main_string = templates.main.format(
            title=piece.title,
            composer=piece.composer,
            emsis_number=piece.emsis_number,
            staff_size=20
        )
        strings = [main_string]
        
        for movement in piece.movements:
            for instrument in movement.instruments:
                if instrument.musician == musician:
                    
                    movement_string = templates.movement.format(
                        movement_title=movement.movement_title,
                        tempo_duration=movement.tempo_duration,
                        tempo_bpm=movement.tempo_bpm,
                        movement_number=movement.movement_number,
                        instrument_name=musician
                    )
                    strings.append(movement_string)
                    
                    instrument_string = templates.instrument.format(
                        instrument_name=instrument.instrument_name,
                        short_instrument_name=instrument.short_instrument_name,
                        midi_instrument_name=instrument.midi_instrument_name,
                        clef=instrument.clef,
                        transpose_from_middle_c=instrument.transpose_from_middle_c
                    )
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
