"""
# >>> get_chord_class([4,6,8])
# [0, 2, 4]

# >>> get_chord_class([3, 6, 11])
# [0, 4, 7]

# >>> get_chord_class([7, 10])
# [0, 3]

>>> zero(5, [2, 5, 9])
[0, 4, 9]

>>> a = [0, 4, 7]
>>> [zero(x, a) for x in a]
[[0, 4, 7], [0, 3, 8], [0, 5, 9]]

>>> is_transposition([0, 4, 7], [8, 0, 3])
True

>>> is_transposition([0, 4, 7], [4, 5, 6, 7])
False

>>> is_chord_in_opts([1, 6, 10], [[0],[0,3],[0,4],[0,3,7],[0,4,7]])
True

>>> is_chord_in_opts([1, 2, 3], [[0],[0,3],[0,4],[0,3,7],[0,4,7]])
False

>>> is_chord_in_opts([7], [[0],[0,3],[0,4],[0,3,7],[0,4,7]])
True

>>> sort_chord([2, 3, 10, 11])
[10, 11, 2, 3]

>>> sort_chord([1, 3, 11])
[11, 1, 3]

>>> sort_chord([0, 9, 10, 11])
[9, 10, 11, 0]

>>> sort_chord([11, 1, 7, 6, 8])
[6, 7, 8, 11, 1]

>>> get_intervals([0, 4, 7])
[4, 3, 5]

>>> get_intervals([4, 5, 6, 9, 10])
[1, 1, 3, 1, 6]

>>> octavate(0, 4)
48

>>> octavate(3, 2)
27



"""


def octavate(pitchclass, octave):
    octave = octave * 12
    pitch = octave + pitchclass
    return pitch


def get_intervals(pitchclasses):
    intervals = []
    for i in range(1, len(pitchclasses)):
        interval = pitchclasses[i] - pitchclasses[i - 1]
        intervals.append(interval)
    # last interval is between (first and last) mod 12
    intervals.append((pitchclasses[0] - pitchclasses[-1]) % 12)
    return intervals


def sort_intervals(intervals):
    biggest = max(intervals)
    i = intervals.index(biggest)
    return intervals[i + 1:] + intervals[:i + 1]


def sort_chord(chord):
    """Takes the pitchclasses of a spelled chord and sorts them so that the top
    note of the largest interval is first and the bot`tom note of the largest
    interval is last."""

    chord.sort()

    intervals = get_intervals(chord)
    biggest = max(intervals)
    i = intervals.index(biggest)
    return chord[i + 1:] + chord[:i + 1]


def is_chord_in_opts(chord, opts):
    """Check if a spelled chord (absolute pitchclasses) is in a list of chord classes."""
    transpositions = set([tuple(set(zero(p, chord))) for p in chord])
    opts = set([tuple(opt) for opt in opts])
    if set.intersection(*[transpositions, opts]):
        return True
    else:
        return False


def is_transposition(a, b):
    """Return True if chord a is a transposition of (or the same as) chord b."""
    a_transpositions = set([tuple(zero(x, a)) for x in a])
    b_transpositions = set([tuple(zero(y, b)) for y in b])

    if set.intersection(*[a_transpositions, b_transpositions]):
        return True
    else:
        return False


def get_all_transpositions(chord):
    return [zero(p, chord) for p in chord]


def zero(root, chord):
    """Give the pitch classes of `chord` as if `root` was 0."""
    return sorted([(p - root) % 12 for p in chord])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
