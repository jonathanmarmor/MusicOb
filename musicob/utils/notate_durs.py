# """Notate a list of notes with aribitrary durations.


# """

# import random

# from metrify import metrify


# DURATION_SPELLINGS = {
#     4: '1',
#     3: '2.',
#     2: '2',
#     1.5: '4.',
#     1: '4',
#     0.75: '8.',
#     0.5: '8',
#     0.25: '16'
# }
# OTHER_DURS = [1.25, 1.75, 2.25, 2.5, 2.75, 3.25, 3.5, 3.75]


# class MusicNote(object):
#     pass

# class NotationNote(object):
#     pass

# class Beat(object):
#     pass

# class Bar(object):
#     pass


# def split_at_barlines(notes):
#     durs = [n.dur for n in notes]
#     meter = []
#     while sum(meter) <= sum(durs):
#         meter.append(4)
#     by_meter = metrify(durs, meter, by='meter')

#     for d in by_meter:



#     return notes


# def split_at_beats(notes):


#     return notes



# def test():
#     opts = [opt / 100.0 for opt in range(25, 800, 25)]

#     total = 100
#     durs = []
#     notes = []
#     while sum(durs) < total:
#         dur = random.choice(opts)
#         durs.append(dur)
#         n = MusicNote()
#         n.dur = dur

#     meter = []
#     beats = []
#     while sum(meter) <= sum(durs):
#         dur = 1
#         meter.append(dur)
#         beat = Beat()
#         beat.dur = dur


#     by_durs = metrify(durs, meter, by='durs')
#     by_meter = metrify(durs, meter, by='meter')

