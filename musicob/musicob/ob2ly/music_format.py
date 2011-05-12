rehearsal_format = """\\mark \\markup {{ \\override #\'(font-name . "Minion Semibold") \\override #\'(thickness . 0.01) \\override #'(box-padding . 0.4) \\box {{ "{rehearsal_text}" }} }}\n"""

bar_format = '| %  ----------  {bar_number} ----------  {bar_number} ----------  {bar_number} ----------  {bar_number} ----------  {bar_number}\n'
time_signature_format = '\\time {numerator}/{denominator}\n'
text_spanner_init_format = """\\override TextSpanner #\'staff-padding = #3.0 \\override TextSpanner #\'(bound-details left text) = \\markup {{ \\override #\'(font-name . "Minion Italic") {{ "{text_spanner_text}" }} }}\n"""

tempo_instruction_init_constant = """\\override TextScript #\'staff-padding = #3.0\n"""
grace_notes_init_constant = '\\grace {\n'
grace_notes_close_constant = '}\n'
tie_constant = '~'
beam_start = '['
beam_stop = ']'
slur_start = '('
slur_stop = ')'
articulation_format = '-{articulation}'
dynamic_format = ' \\{dynamic}'
fermata_constant = ' \\fermata'
text_above_format = ' ^"{text}"'
text_below_format = ' _"{text}"'
breathe_constant = ' \\breathe'
start_text_spanner_constant = ' \\startTextSpan'
stop_text_spanner_constant = ' \\stopTextSpan'
tempo_instruction_format = """ ^\\markup {{ \\override #\'(font-name . "Minion Italic") {{ "{tempo_instruction_text}" }} }}"""


note_format = """{rehearsal}{bar}{time_signature}{text_spanner_init}{tempo_instruction_init}{grace_notes_init}{grace_notes}{grace_notes_close}{pitches}{duration}{tie}{beam}{slur}{articulations}{dynamic}{fermata}{text_above}{text_below}{breathe}{start_text_spanner}{stop_text_spanner}{tempo_instruction}\n"""

grace_note_format = """{text_spanner_init_tab}{text_spanner_init}{tempo_instruction_init_tab}{tempo_instruction_init}{pitches_tab}{pitches}{duration}{tie}{beam}{slur}{articulations}{dynamic}{text_above}{text_below}{start_text_spanner}{stop_text_spanner}{tempo_instruction}\n"""


def format_articulations(articulations):
    artics_list = []
    for a in articulations:
        artic = articulation_format.format(articulation=a)
        artics_list.append(artic)  
    return ''.join(artics_list)    

def format_note(note):
    d = get_format_dict(note)
    return note_format.format(**d)

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
    
    return grace_note_format.format(**d)


def get_format_dict(note):
    d = {}

    if note.rehearsal_mark:
        d['rehearsal'] = rehearsal_format.format(rehearsal_text=note.rehearsal_mark)
    else:
        d['rehearsal'] = ''
        
    if note.bar:
        d['bar'] = bar_format.format(bar_number=note.bar)
    else:
        d['bar'] = ''
        
    if note.time_signature_numerator:
        d['time_signature'] = time_signature_format.format(numerator=note.time_signature_numerator, 
                                                           denominator=note.time_signature_denominator)
    else:
        d['time_signature'] = ''
        
    if note.text_spanner_start:
        d['text_spanner_init'] = text_spanner_init_format.format(text_spanner_text=note.text_spanner_start)
        d['start_text_spanner'] = start_text_spanner_constant
    else:
        d['text_spanner_init'] = ''
        d['start_text_spanner'] = ''
        
    if note.text_spanner_stop:
        d['stop_text_spanner'] = stop_text_spanner_constant
    else:
        d['stop_text_spanner'] = ''
        
    if note.tempo_instruction:
        d['tempo_instruction_init'] = tempo_instruction_init_constant
        d['tempo_instruction'] = tempo_instruction_format.format(tempo_instruction_text=note.tempo_instruction)
    else:
        d['tempo_instruction_init'] = ''
        d['tempo_instruction'] = ''
        
    if note.grace_notes:
        d['grace_notes_init'] = grace_notes_init_constant
        grace_list = []
        for g in note.grace_notes:
            grace_string = format_grace_note(g)
            grace_list.append(grace_string)
        d['grace_notes'] = ''.join(grace_list)
        d['grace_notes_close'] = grace_notes_close_constant
    else:     
        d['grace_notes_init'] = ''
        d['grace_notes'] = ''
        d['grace_notes_close'] = ''
    
    d['pitches'] = note.pitches
    d['duration'] = note.duration
    
    if note.tie:
        d['tie'] = tie_constant
    else:
        d['tie'] = ''
    
    if note.beam == 'start':
        d['beam'] = beam_start
    elif note.beam == 'stop':
        d['beam'] = beam_stop
    else:
        d['beam'] = ''
    
    if note.slur == 'start':
        d['slur'] = slur_start
    elif note.slur == 'stop':
        d['slur'] = slur_stop
    else:
        d['slur'] = ''
    
    if note.articulations:
        d['articulations'] = format_articulations(note.articulations)
    else:
        d['articulations'] = ''
    
    if note.dynamic:
        d['dynamic'] = dynamic_format.format(dynamic=note.dynamic)   
    else:
        d['dynamic'] = ''
    
    if note.fermata:
        d['fermata'] = fermata_constant
    else:
        d['fermata'] = ''
    
    if note.text_above:
        d['text_above'] = text_above_format.format(text=note.text_above)
    else:
        d['text_above'] = ''
    
    if note.text_below:
        d['text_below'] = text_below_format.format(text=note.text_below)
    else:
        d['text_below'] = ''
    
    if note.breathe:
        d['breathe'] = breathe_constant
    else:
        d['breathe'] = ''
        
    return d


def make_score_music_string(music):    
    music_string_list = []
    page_start = '\\new Voice {\n\n'
    music_string_list.append(page_start)
    
    for note in music:
        note_string = format_note(note)
        music_string_list.append(note_string)
    page_end = '\n\\bar "|."\n}'
    music_string_list.append(page_end)
    music_string = ''.join(music_string_list)
    return music_string


