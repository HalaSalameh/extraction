import os
import re
import sys

import pkg_resources
from mtranslate import translate

from extraction.store_dosage import insert_posology
from extraction.utilities import text2int, is_float

PREDICTED_DIR = 'Data/dosage_deep_predict'
PREDICTED_DIR = pkg_resources.resource_filename(__name__, PREDICTED_DIR)

ORIGINAL_DATA_DIRECTORY = 'Data/Outputs/Dosage'
ORIGINAL_DATA_DIRECTORY = pkg_resources.resource_filename(__name__, ORIGINAL_DATA_DIRECTORY)


class DosageUnit:

    def __init__(self, unit, index):
        self.unit = unit
        self.index = index

    def __repr__(self):
        return str(self.unit) + " " + str(self.index)


class Dosage:

    def __init__(self, unit, range, simple, index):
        self.unit = unit
        self.range = range
        self.simple = simple
        self.index = index

    def __repr__(self):
        if self.range:
            return str(self.unit) + " range is " + str(
                self.range.max) + "-" + str(self.range.min) + " index is " + str(self.index) + "\n"
        else:
            if self.simple:
                return str(self.unit) + " simple is " + str(
                    self.simple.value) + " index is " + str(self.index) + "\n"
            else:
                return str(self.unit) + " \n"


class TargetBeing:

    def __init__(self, description, index):
        self.description = description
        self.index = index

    def __repr__(self):
        return str(self.description) + " " + str(self.index)


class Case:

    def __init__(self, description, index):
        self.description = description
        self.index = index

    def __repr__(self):
        return str(self.description) + " " + str(self.index)


class Frequency:

    def __init__(self, value, period, index):
        self.value = value
        self.period = period
        self.index = index

    def __repr__(self):
        return str(self.value) + " " + str(self.index) + " " + str(self.period)


class Duration:

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return str(self.value) + " " + str(self.index)


class Stop:

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return str(self.value) + " " + str(self.index)


class Range:

    def __init__(self, min, max, index):
        self.min = min
        self.max = max
        self.index = index

    def __repr__(self):
        return "(" + str(self.min) + " , " + str(self.max) + ") index is " + str(self.index)


class DosageValue:
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return "" + str(self.value) + "index is " + str(self.index)


class Relation:

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return str(self.value) + " " + str(self.index)


class CasePosology:

    def __init__(self, case, posology, index):
        self.case = case
        self.posology = posology
        self.index = index

    def __repr__(self):
        return str(self.posology) + " " + " case " + str(self.case)


class TargetPosology:

    def __init__(self, target_being, posology, index):
        self.target_being = target_being
        self.posology = posology
        self.index = index

    def __repr__(self):
        return str(self.posology) + " " + str(self.target_being)


class Posology:
    def __init__(self, dosage, dur, freq, stop, relation, index):
        self.dosage = dosage
        self.dur = dur
        self.freq = freq
        self.stop = stop
        self.relation = relation
        self.index = index
        self.cases = []
        self.targets = []

    def __repr__(self):
        if len(self.cases) > 0:
            if len(self.targets) > 0:
                return " Target Being : \n" + str(self.targets) + "\nCases : \n" + str(
                    self.cases) + "\nDosage :\n" + str(self.dosage) + "\nfreq:\n" + str(self.freq) + "\ndur:\n" + str(
                    self.dur) + "\nrel:\n" + str(
                    self.relation) + "\nstop:\n" + str(self.stop) + "\n-------------------------\n"
            else:
                return "\nCases : \n" + str(
                    self.cases) + "\nDosage :\n" + str(self.dosage) + "\nfreq:\n" + str(self.freq) + "\ndur:\n" + str(
                    self.dur) + "\nrel:\n" + str(
                    self.relation) + "\nstop:\n" + str(self.stop) + "\n-------------------------\n"
        else:
            if len(self.targets) > 0:
                print(self.dosage, "honaaa")
                return " Target Being : \n" + str(self.targets) + "\nDosage :\n" + str(self.dosage) + "\nfreq:\n" + str(
                    self.freq) + "\ndur:\n" + str(self.dur) + "\nrel:\n" + str(self.relation) + "\nstop:\n" + \
                       str(self.stop) + "\n-------------------------\n"
            else:
                return "\nDosage :\n" + str(self.dosage) + "\nfreq:\n" + str(
                    self.freq) + "\ndur:\n" + str(self.dur) + "\nrel:\n" + str(
                    self.relation) + "\nstop:\n" + str(self.stop) + "\n-------------------------\n"


def get_list(data):
    data = re.sub("\n", " ", data)
    data = re.sub("\r", " ", data)
    data = re.sub(' +', ' ', data)

    words = data.split(' ')
    try:
        while True:
            words.remove('')

    except Exception as e:
        pass
    return words


all_tags = []
original_words = []


def put_together(b_indexes, b_tags, in_indexes, in_tags):
    arr = []
    for i in range(len(b_indexes)):
        arr.append(b_tags[i])

    for i in range(len(in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(arr)):
            obj = arr[j]
            if min_dest >= in_indexes[i] - b_indexes[j] > 0:
                index = j

        if index != -1:
            arr[index] = arr[index] + " " + in_tags[i]

    return arr


def get_tags(tag_name):
    global all_tags, original_words
    indexes = [i for i, x in enumerate(all_tags) if x == tag_name]
    tags = [original_words[x] for x in indexes]

    return indexes, tags


def get_ranges(ranges_initial, sranges, eranges, dsranges, deranges):
    ranges = []
    dosages_extra = []
    for range in ranges_initial:

        min_max = re.split("[-_]", range[0])
        if len(min_max) < 2:
            continue

        new_range = Range(min_max[0], min_max[1], range[1])
        ranges.append(new_range)

    end_chosen = {}
    for start in sranges:
        min_obj = None
        min_dist = sys.maxsize
        for end in eranges:
            if end[1] in end_chosen:
                continue

            if 0 < end[1] - start[1] < min_dist:
                min_obj = end
                min_dist = end[1] - start[1]

        if not min_obj:
            continue

        end_chosen[min_obj[1]] = "True"

        translation = translate(start[0], "en", "ar")
        start_new = text2int(translation)
        # if not is_float(start_new):
        #     start_new = 1
        translation = translate(min_obj[0], "en", "ar")
        end_new = text2int(translation)
        # if not is_float(end_new):
        #     end_new = 1
        new_range = Range(start_new, end_new, start[1])
        ranges.append(new_range)

    for start in dsranges:
        min_obj = None
        min_dist = sys.maxsize
        for end in deranges:
            if end[1] in end_chosen:
                continue

            if 0 < end[1] - start[1] < min_dist:
                min_obj = end
                min_dist = end[1] - start[1]

        if not min_obj:
            continue

        translation = translate(start[0], "en", "ar")
        # print(translation)
        start_new = text2int(translation.lower())
        # print(start_new)
        splits = start_new.split(" ")
        start_num = 1
        for split in splits:
            if is_float(split):
                start_num = float(split)
                print(' '.join(splits[splits.index(split):]))
                dosage_ar = translate(' '.join(splits[1 + splits.index(split):]), "ar", "en")
                dosages_extra.append(DosageUnit(dosage_ar, start[1]))
                break

        translation = translate(min_obj[0], "en", "ar")
        # print(translation)
        end_new = text2int(translation.lower())
        # print(end_new)
        splits = end_new.split(" ")
        end_num = 1
        for split in splits:
            if is_float(split):
                end_num = float(split)

                break
        end_chosen[min_obj[1]] = "True"
        new_range = Range(start_num, end_num, start[1])
        ranges.append(new_range)

    return ranges, dosages_extra


def sort_dosage(val):
    return val.index


def get_dosage(file_name, drug_id):
    global all_tags, original_words

    option_indexes, option_tags = get_tags("B-OPTION")

    range_indexes, range_tags = get_tags("B-RANGE")

    dosage_b_indexes, dosage_b_tags = get_tags("B-DOSAGE")
    dosage_in_indexes, dosage_in_tags = get_tags("I-DOSAGE")

    case_b_indexes, case_b_tags = get_tags("B-CASE")
    case_in_indexes, case_in_tags = get_tags("I-CASE")

    srange_b_indexes, srange_b_tags = get_tags("B-SRANGE")
    srange_in_indexes, srange_in_tags = get_tags("I-SRANGE")

    dsrange_b_indexes, dsrange_b_tags = get_tags("B-DSRANGE")
    dsrange_in_indexes, dsrange_in_tags = get_tags("I-DSRANGE")

    erange_b_indexes, erange_b_tags = get_tags("B-ERANGE")
    erange_in_indexes, erange_in_tags = get_tags("I-ERANGE")

    derange_b_indexes, derange_b_tags = get_tags("B-DERANGE")
    derange_in_indexes, derange_in_tags = get_tags("I-DERANGE")

    dur_b_indexes, dur_b_tags = get_tags("B-DUR")
    dur_in_indexes, dur_in_tags = get_tags("I-DUR")

    stop_b_indexes, stop_b_tags = get_tags("B-STOP")
    stop_in_indexes, stop_in_tags = get_tags("I-STOP")

    per_b_indexes, per_b_tags = get_tags("B-PER")
    per_in_indexes, per_in_tags = get_tags("I-PER")

    value_b_indexes, value_b_tags = get_tags("B-VALUE")
    value_in_indexes, value_in_tags = get_tags("I-VALUE")

    freq_b_indexes, freq_b_tags = get_tags("B-FREQ")
    freq_in_indexes, freq_in_tags = get_tags("I-FREQ")

    math_b_indexes, math_b_tags = get_tags("B-MATH")
    math_in_indexes, math_in_tags = get_tags("I-MATH")

    fvalue_b_indexes, fvalue_b_tags = get_tags("B-FVALUE")
    fvalue_in_indexes, fvalue_in_tags = get_tags("I-FVALUE")

    durations = [Duration(value, dur_b_indexes[index]) for index, value in
                 enumerate(put_together(dur_b_indexes, dur_b_tags, dur_in_indexes, dur_in_tags))]

    cases = [Case(value, case_b_indexes[index] + len(value.split()) - 1 ) for index, value in
             enumerate(put_together(case_b_indexes, case_b_tags, case_in_indexes, case_in_tags))]

    stops = [Stop(value, stop_b_indexes[index]) for index, value in
             enumerate(put_together(stop_b_indexes, stop_b_tags, stop_in_indexes, stop_in_tags))]

    relations = [Relation(value, math_b_indexes[index]) for index, value in
                 enumerate(put_together(math_b_indexes, math_b_tags, math_in_indexes, math_in_tags))]

    target_beings = [TargetBeing(value, per_b_indexes[index] + len(value.split()) - 1) for index, value in
                     enumerate(put_together(per_b_indexes, per_b_tags, per_in_indexes, per_in_tags))]

    values = [DosageValue(value, value_b_indexes[index]) for index, value in
              enumerate(put_together(value_b_indexes, value_b_tags, value_in_indexes, value_in_tags))]

    dsranges = [(value, dsrange_b_indexes[index]) for index, value in
                enumerate(put_together(dsrange_b_indexes, dsrange_b_tags, dsrange_in_indexes, dsrange_in_tags))]

    deranges = [(value, derange_b_indexes[index]) for index, value in
                enumerate(put_together(derange_b_indexes, derange_b_tags, derange_in_indexes, derange_in_tags))]

    sranges = [(value, srange_b_indexes[index]) for index, value in
               enumerate(put_together(srange_b_indexes, srange_b_tags, srange_in_indexes, srange_in_tags))]

    eranges = [(value, erange_b_indexes[index]) for index, value in
               enumerate(put_together(erange_b_indexes, erange_b_tags, erange_in_indexes, erange_in_tags))]

    freqs = [(value, freq_b_indexes[index]) for index, value in
             enumerate(put_together(freq_b_indexes, freq_b_tags, freq_in_indexes, freq_in_tags))]

    fvalues = [(value, fvalue_b_indexes[index]) for index, value in
               enumerate(put_together(fvalue_b_indexes, fvalue_b_tags, fvalue_in_indexes, fvalue_in_tags))]

    dosages = [DosageUnit(value, dosage_b_indexes[index]) for index, value in
               enumerate(put_together(dosage_b_indexes, dosage_b_tags, dosage_in_indexes, dosage_in_tags))]

    ranges_initial = [(value, range_indexes[index]) for index, value in
                      enumerate(put_together(range_indexes, range_tags, [], []))]

    options = [(value, option_indexes[index]) for index, value in
               enumerate(put_together(option_indexes, option_tags, [], []))]

    ranges, extra_dosages = get_ranges(ranges_initial, sranges, eranges, dsranges, deranges)

    dosages += extra_dosages
    frequencies = []
    print(ranges)
    end_chosen = {}
    for value in fvalues:
        min_obj = None
        min_dist = sys.maxsize
        for freq in freqs:
            if freq[1] in end_chosen:
                continue

            if abs(value[1] - freq[1]) < min_dist:
                min_obj = freq
                min_dist = abs(value[1] - freq[1])

        if min_obj:
            end_chosen[min_obj[1]] = "True"
            frequencies.append(Frequency(value[0], min_obj[0], min_obj[1]))

    for freq in freqs:
        if freq[1] not in end_chosen:
            frequencies.append(Frequency(None, freq[0], freq[1]))

    dosages_original = []
    end_chosen = {}
    for value in values:
        min_obj = None
        min_dist = sys.maxsize
        for dosage in dosages:
            if dosage.index in end_chosen:
                continue

            if abs(value.index - dosage.index) < min_dist:
                min_obj = dosage
                min_dist = abs(value.index - dosage.index)

        if min_obj:
            dosages_original.append(Dosage(min_obj.unit, None, value, min_obj.index))
            end_chosen[min_obj.index] = True

    for range in ranges:
        min_obj = None
        min_dist = sys.maxsize
        for dosage in dosages:
            if dosage.index in end_chosen:
                continue

            if abs(range.index - dosage.index) < min_dist:
                min_obj = dosage
                min_dist = abs(range.index - dosage.index)

        if min_obj:
            dosages_original.append(Dosage(min_obj.unit, range, None, min_obj.index))
            end_chosen[min_obj.index] = True

    for dosage in dosages:
        if dosage.index in end_chosen:
            continue
        dosages_original.append(Dosage(dosage.unit, None, None, dosage.index))

    freq_chosen = {}
    dur_chosen = {}
    stop_chosen = {}
    relation_chosen = {}
    posologies = []
    dosages_original.sort(key=sort_dosage)

    for dosage in dosages_original:

        min_obj_freq = None
        min_dist_freq = sys.maxsize
        for freq in frequencies:
            if freq.index in freq_chosen:
                continue

            if abs(freq.index - dosage.index) < min_dist_freq:
                min_obj_freq = freq
                min_dist_freq = abs(freq.index - dosage.index)

        min_obj_dur = None
        min_dist_dur = sys.maxsize
        for dur in durations:
            if dur.index in dur_chosen:
                continue

            if abs(dur.index - dosage.index) < min_dist_dur:
                print("hhhhhhhhhhhhhhhhhhhhhhhh")
                min_obj_dur = dur
                min_dist_dur = abs(dur.index - dosage.index)

        min_obj_stop = None
        min_dist_stop = sys.maxsize
        for stop in stops:
            if stop.index in stop_chosen:
                continue

            if abs(stop.index - dosage.index) < min_dist_stop:
                min_obj_stop = stop
                min_dist_stop = abs(stop.index - dosage.index)

        min_obj_relation = None
        min_dist_relation = sys.maxsize
        for relation in relations:
            if relation.index in relation_chosen:
                continue

            if abs(relation.index - dosage.index) < min_dist_relation:
                min_obj_relation = relation
                min_dist_relation = abs(relation.index - dosage.index)

        p = Posology(dosage, None, None, None, None, dosage.index)
        if min_obj_freq:
            new_freq = min_obj_freq
            if len(posologies) > 0 and posologies[len(posologies) - 1].freq:
                last_freq = posologies[len(posologies) - 1].freq
                if abs(dosage.index - last_freq.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_freq.index):
                    dist =  abs(dosage.index - last_freq.index)
                    if dist < abs(min_obj_freq.index - dosage.index):
                        new_freq = last_freq
                        posologies[len(posologies) - 1].freq = None


            p.freq = new_freq
            freq_chosen[new_freq.index] = True
        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].freq:
                last_freq = posologies[len(posologies) - 1].freq
                if abs(dosage.index - last_freq.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_freq.index):
                    p.freq = last_freq
                    posologies[len(posologies) - 1].freq = None

        if min_obj_dur:
            print("hhhhhhhhhhhhhhhhhhhhhhhh", min_obj_dur)
            new_dur = min_obj_dur
            # dur_chosen[min_obj_dur.index] = True

            if len(posologies) > 0 and posologies[len(posologies) - 1].dur:
                last_dur = posologies[len(posologies) - 1].dur
                if abs(dosage.index - last_dur.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_dur.index):
                    dist = abs(dosage.index - last_dur.index)
                    if dist < abs(min_obj_dur.index - dosage.index):
                        new_dur = last_dur
                        posologies[len(posologies) - 1].dur = None

            p.dur = new_dur
            dur_chosen[new_dur.index] = True

            # print(p)

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].dur:
                last_dur = posologies[len(posologies) - 1].dur
                if abs(dosage.index - last_dur.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_dur.index):
                    p.dur = last_dur
                    posologies[len(posologies) - 1].dur = None

        if min_obj_stop:
            new_stop = min_obj_stop
            # dur_chosen[min_obj_dur.index] = True

            if len(posologies) > 0 and posologies[len(posologies) - 1].stop:
                last_stop = posologies[len(posologies) - 1].stop
                if abs(dosage.index - last_stop.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_stop.index):
                    dist = abs(dosage.index - last_stop.index)
                    if dist < abs(min_obj_stop.index - dosage.index):
                        new_stop = last_stop
                        posologies[len(posologies) - 1].stop = None

            p.stop = new_stop
            stop_chosen[new_stop.index] = True

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].stop:
                last_stop = posologies[len(posologies) - 1].stop
                if abs(dosage.index - last_stop.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_stop.index):
                    p.stop = last_stop
                    posologies[len(posologies) - 1].stop = None

        if min_obj_relation:
            new_relation = min_obj_relation
            # dur_chosen[min_obj_dur.index] = True

            if len(posologies) > 0 and posologies[len(posologies) - 1].relation:
                last_relation = posologies[len(posologies) - 1].relation
                if abs(dosage.index - last_relation.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_relation.index):
                    dist = abs(dosage.index - last_relation.index)
                    if dist < abs(min_obj_relation.index - dosage.index):
                        new_relation = last_relation
                        posologies[len(posologies) - 1].relation = None

            p.relation = new_relation
            relation_chosen[new_relation.index] = True

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].relation:
                last_relation = posologies[len(posologies) - 1].relation
                if abs(dosage.index - last_relation.index) < abs(
                        posologies[len(posologies) - 1].dosage.index - last_relation.index):
                    p.relation = last_relation
                    posologies[len(posologies) - 1].relation = None

        print("))))))))))))))))))))))))))))))))))))))))))))")
        print(p)

        posologies.append(p)
    for freq in frequencies:
        if freq.index in freq_chosen:
            continue

        min_obj_dur = None
        min_dist_dur = sys.maxsize

        for dur in durations:
            if dur.index in dur_chosen:
                continue

            if abs(dur.index - freq.index) < min_dist_dur:
                min_obj_dur = dur
                min_dist_dur = abs(dur.index - freq.index)

        min_obj_stop = None
        min_dist_stop = sys.maxsize
        for stop in stops:
            if stop.index in stop_chosen:
                continue

            if abs(stop.index - freq.index) < min_dist_stop:
                min_obj_stop = stop
                min_dist_stop = abs(stop.index - freq.index)

        p = Posology(None, None, freq, None, None, freq.index)

        if min_obj_dur:
            p.dur = min_obj_dur
            dur_chosen[min_obj_dur.index] = True

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].dur:
                last_dur = posologies[len(posologies) - 1].dur
                if abs(freq.index - last_dur.index) < abs(posologies[len(posologies) - 1].freq.index - last_dur.index):
                    p.dur = last_dur
                    posologies[len(posologies) - 1].dur = None

        if min_obj_stop:
            p.stop = min_obj_stop
            stop_chosen[min_obj_stop.index] = True

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].stop:
                last_stop = posologies[len(posologies) - 1].stop
                if abs(freq.index - last_stop.index) < abs(
                        posologies[len(posologies) - 1].freq.index - last_stop.index):
                    p.stop = last_stop
                    posologies[len(posologies) - 1].stop = None
        posologies.append(p)

    for dur in durations:
        if dur.index in dur_chosen:
            continue

        min_obj_stop = None
        min_dist_stop = sys.maxsize
        for stop in stops:
            if stop.index in stop_chosen:
                continue

            if abs(stop.index - dur.index) <= min_dist_stop:
                min_obj_stop = stop
                min_dist_stop = abs(stop.index - dur.index)

        p = Posology(None, dur, None, None, None, dur.index)

        if min_obj_stop:
            p.stop = min_obj_stop
            stop_chosen[min_obj_stop.index] = True

        else:
            if len(posologies) > 0 and posologies[len(posologies) - 1].stop:
                last_stop = posologies[len(posologies) - 1].stop
                if abs(dur.index - last_stop.index) < abs(
                        posologies[len(posologies) - 1].stop.index - last_stop.index):
                    p.stop = last_stop
                    posologies[len(posologies) - 1].stop = None



        posologies.append(p)

    target_posologies = []
    for target_being in target_beings:

        min_obj_posology = None
        min_dist_posology = sys.maxsize
        for posology in posologies:

            if abs(posology.index - target_being.index) <= min_dist_posology:
                min_obj_posology = posology
                min_dist_posology = abs(posology.index - target_being.index)

        if min_obj_posology:
            min_obj_posology.targets.append(target_being)
            target_posologies.append(TargetPosology(target_being, min_obj_posology, min_obj_posology.index))

    case_posologies = []
    for case in cases:

        min_obj_posology = None
        min_dist_posology = sys.maxsize
        for posology in posologies:

            if abs(posology.index - case.index) <= min_dist_posology:
                min_obj_posology = posology
                min_dist_posology = abs(posology.index - case.index)

        if min_obj_posology:
            min_obj_posology.cases.append(case)
            case_posologies.append(CasePosology(case, min_obj_posology, min_obj_posology.index))

    for pos in posologies:
        insert_posology(pos, drug_id)


def read_dosage_deep_res(file_name, drug_id):
    global all_tags, original_words

    file = open(ORIGINAL_DATA_DIRECTORY + os.path.sep + file_name, 'r', encoding='utf-8')
    original_data = (file.read())
    original_words = get_list(original_data)

    file = open(PREDICTED_DIR + os.path.sep + file_name, 'r', encoding='utf-8')
    DOSAGE_TAGS = file.read()
    all_tags = get_list(DOSAGE_TAGS)
    get_dosage(file_name, drug_id)
