"""Split note durations at barlines or beats.

arguments:

durs: list of ints or floats.  Note durations.
meter: list of ints or floats.  Durations of bars or beats.
by: 'meter', 'durs', or 'flat'.
- 'meter' will return a list of lists where the sum of the numbers in the
    sub-lists are the numbers from the meter argument.
- 'durs' will return a list of lists where the sum of the numbers in the
    sub-lists are the numbers from the durs argument.
- 'flat' will return the same numbers as 'durs' and 'meter' but not grouped into
    sub-lists.


# doctests

>>> metrify([3, 3, 3, 3, 2, 2], [4, 4, 4, 4], by='meter')
[[3, 1], [2, 2], [1, 3], [2, 2]]

>>> d = [9, 1, 1, 1, 3, 3, 2, 2, 2]
>>> m = [4, 4, 4, 3, 3, 3, 3]
>>> metrify(d, m, by='meter')
[[4], [4], [1, 1, 1, 1], [3], [3], [2, 1], [1, 2]]

>>> metrify([3, 3, 2], [7, 9], by='meter')
[[3, 3, 1], [1]]

>>> metrify([3, 3, 2], [7, 9, 4, 4], by='meter')
[[3, 3, 1], [1]]

>>> metrify([3, 3, 3, 3, 2, 2], [4, 4], by='meter')
[[3, 1], [2, 2], [1, 3, 2, 2]]

>>> half_triplet = 4.0 / 3
>>> d = [1.5, 1.5, 1.5, 2, 1.5, 3, 1, half_triplet, half_triplet, half_triplet]
>>> m = [4, 4, 4, 4]
>>> metrify(d, m, by='meter')
[[1.5, 1.5, 1], [0.5, 2, 1.5], [3, 1], [1.3333333333333333, 1.3333333333333333, 1.3333333333333333]]


>>> metrify([3, 3, 3, 3, 2, 2], [4, 4, 4, 4], by='durs')
[[3], [1, 2], [2, 1], [3], [2], [2]]

>>> d = [9, 1, 1, 1, 3, 3, 2, 2, 2]
>>> m = [4, 4, 4, 3, 3, 3, 3]
>>> metrify(d, m, by='durs')
[[4, 4, 1], [1], [1], [1], [3], [3], [2], [1, 1], [2]]

>>> metrify([3, 3, 2], [7, 9], by='durs')
[[3], [3], [1, 1]]

>>> metrify([3, 3, 2], [7, 9, 4, 4], by='durs')
[[3], [3], [1, 1]]

>>> metrify([3, 3, 3, 3, 2, 2], [4, 4], by='durs')
[[3], [1, 2], [2, 1], [3], [2], [2]]

>>> half_triplet = 4.0 / 3
>>> d = [1.5, 1.5, 1.5, 2, 1.5, 3, 1, half_triplet, half_triplet, half_triplet]
>>> m = [4, 4, 4, 4]
>>> metrify(d, m, by='durs')
[[1.5], [1.5], [1, 0.5], [2], [1.5], [3], [1], [1.3333333333333333], [1.3333333333333333], [1.3333333333333333]]


>>> metrify([3, 3, 3, 3, 2, 2], [4, 4, 4, 4], by='flat')
[3, 1, 2, 2, 1, 3, 2, 2]

>>> d = [9, 1, 1, 1, 3, 3, 2, 2, 2]
>>> m = [4, 4, 4, 3, 3, 3, 3]
>>> metrify(d, m, by='flat')
[4, 4, 1, 1, 1, 1, 3, 3, 2, 1, 1, 2]

>>> metrify([3, 3, 2], [7, 9], by='flat')
[3, 3, 1, 1]

>>> metrify([3, 3, 2], [7, 9, 4, 4], by='flat')
[3, 3, 1, 1]

>>> metrify([3, 3, 3, 3, 2, 2], [4, 4], by='flat')
[3, 1, 2, 2, 1, 3, 2, 2]

>>> half_triplet = 4.0 / 3
>>> d = [1.5, 1.5, 1.5, 2, 1.5, 3, 1, half_triplet, half_triplet, half_triplet]
>>> m = [4, 4, 4, 4]
>>> metrify(d, m, by='flat')
[1.5, 1.5, 1, 0.5, 2, 1.5, 3, 1, 1.3333333333333333, 1.3333333333333333, 1.3333333333333333]


>>> for x in range(10):
...    _stress_test(10000)


"""


import logging


def metrify(durs, meter, by='durs'):
    if by == 'meter':
        result = _metrify_by_meter(durs, meter)
    elif by == 'durs':
        result = _metrify_by_durs(durs, meter)
    elif by == 'flat':
        result = []
        metered = _metrify_by_meter(durs, meter)
        for batch in metered:
            for d in batch:
                result.append(d)
    return result


def _metrify_by_meter(durs, meter):
    sum_durs = sum(durs)
    sum_meter = sum(meter)

    if sum_durs > sum_meter:
        logging.warning('Durs is {} longer than meter.'.format(sum_durs - sum_meter))
        diff = sum_durs - sum_meter
        meter.append(diff)
        sum_meter = sum(meter)
    elif sum_durs < sum_meter:
        logging.warning('Meter is {} longer than durs.'.format(sum_meter - sum_durs))

    durs = iter(durs)
    meter = iter(meter)

    sum_result = 0
    result = []
    from_previous = None

    no_more_durs = False
    while sum_result < sum_durs and not no_more_durs:
        sum_batch = 0
        batch = []
        result.append(batch)

        try:
            beat = meter.next()
        except StopIteration:
            # make beat longer than what's reamaining in durs
            beat = sum_durs

        while sum_batch < beat:
            if from_previous:
                dur = from_previous
            else:
                try:
                    dur = durs.next()
                except StopIteration:
                    no_more_durs = True
                    break
            if sum_batch + dur <= beat:
                sum_batch += dur
                sum_result += dur
                batch.append(dur)
                from_previous = None
            else:
                include = beat - sum_batch
                sum_batch += include
                sum_result += include
                batch.append(include)
                from_previous = dur - include
    new_result = []
    for batch in result:
        new_batch = []
        for dur in batch:
            if dur % 1 == 0.0:
                dur = int(dur)
            new_batch.append(dur)
        new_result.append(new_batch)
    return new_result


def _metrify_by_durs(durs, meter):
    sum_durs = sum(durs)
    sum_meter = sum(meter)

    if sum_durs > sum_meter:
        logging.warning('Durs is {} longer than meter.'.format(
            sum_durs - sum_meter))
        diff = sum_durs - sum_meter
        meter.append(diff)
        sum_meter = sum(meter)
    elif sum_durs < sum_meter:
        logging.warning('Meter is {} longer than durs.'.format(
            sum_meter - sum_durs))

    durs = iter(durs)
    meter = iter(meter)

    sum_result = 0
    result = []
    from_previous = None
    while sum_result < sum_durs:
        sum_batch = 0
        batch = []
        result.append(batch)

        try:
            dur = durs.next()
        except StopIteration:
            break

        while sum_batch < dur:
            if from_previous:
                beat = from_previous
            else:
                try:
                    beat = meter.next()
                except StopIteration:
                    break

            if sum_batch + beat <= dur:
                sum_batch += beat
                sum_result += beat
                batch.append(beat)
                from_previous = None
            else:
                include = dur - sum_batch
                sum_batch += include
                sum_result += include
                batch.append(include)
                from_previous = beat - include
    new_result = []
    for batch in result:
        new_batch = []
        for dur in batch:
            if dur % 1 == 0.0:
                dur = int(dur)
            new_batch.append(dur)
        new_result.append(new_batch)
    return new_result


def _stress_test(total=100):
    import random
    from pprint import pprint

    def get_random_durs(total):
        results = []
        tot = 0
        while tot < total:
            i = random.randint(1, 12)
            r = random.random()
            n = i - r
            tot += n
            results.append(n)
        return results

    a = get_random_durs(total)
    print 'durs: {}'.format(a)
    b = get_random_durs(total)
    print 'meter: {}'.format(b)

    print 'by durs...'
    result = metrify(a, b, by='durs')
    pprint(result)
    print 'done'
    print

    print 'by meter...'
    result = metrify(a, b, by='meter')
    pprint(result)
    print 'done'
    print

    print 'by flat...'
    result = metrify(a, b, by='flat')
    pprint(result)
    print 'done'
    print


if __name__ == '__main__':
    import doctest
    doctest.testmod()
