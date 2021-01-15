from extraction.database_conn import insert_posology_db, insert_stop_db, insert_duration_db, insert_relation_db, \
    insert_frequency_db, get_case_db, insert_case_db, get_target_being_db, insert_target_being_db, \
    insert_posology_target_being_db, insert_posology_case_db, get_dosage_value_db, insert_dosage_value_db, \
    get_dosage_range_db, insert_dosage_range_db, insert_dosage_db, insert_drug_posology_db


def insert_posology(posology, drug_id):
    relation_id = None
    dur_id = None
    freq_id = None
    stop_id = None
    dosage_id = None

    if posology.relation:
        relation_id = insert_relation(posology.relation)

    if posology.freq:
        freq_id = insert_frequency(posology.freq)

    if posology.dur:
        dur_id = insert_duration(posology.dur)

    if posology.stop:
        stop_id = insert_stop(posology.stop)

    if posology.dosage:
        dosage_id = insert_dosage(posology.dosage)

    posology_id = insert_posology_db(relation_id, dur_id, freq_id, stop_id, dosage_id)

    for case in posology.cases:
        case_id = insert_case(case)
        pos_case_id = insert_posology_case(case_id, posology_id)

    for target in posology.targets:
        target_id = insert_target_being(target)
        pos_target_id = insert_posology_target_being(posology_id, target_id)

    posology_durg_id = insert_drug_posology(drug_id, posology_id)
    return posology_durg_id


def insert_stop(stop):

    stop_id = insert_stop_db(stop.value)
    return stop_id


def insert_duration(dur):

    dur_id = insert_duration_db(dur.value)
    return dur_id


def insert_relation(relation):
    relation_id = insert_relation_db(relation.value)
    return relation_id


def insert_frequency(frequency):
    freq_id = insert_frequency_db(frequency.value, frequency.period)
    return freq_id


def insert_case(case):
    case_id = get_case_db(case.description)
    if case_id:
        return case_id[0][0]
    case_id = insert_case_db(case.description)
    return case_id


def insert_target_being(target_being):
    target_being_id = get_target_being_db(target_being.description)
    if target_being_id:
        return target_being_id[0][0]
    target_being_id = insert_target_being_db(target_being.description)
    return target_being_id


def insert_posology_target_being(target_being_id, posology_id):
    posology_target_being_id = insert_posology_target_being_db(target_being_id, posology_id)
    return posology_target_being_id


def insert_posology_case(case_id, posology_id):
    posology_case_id = insert_posology_case_db(posology_id, case_id)
    return posology_case_id


def insert_dosage_value(value):
    value_id = get_dosage_value_db(value.value)
    if value_id:
        return value_id[0][0]
    value_id = insert_dosage_value_db(value.value)
    return value_id


def insert_dosage_range(range):
    range_id = get_dosage_range_db(range.min, range.max)
    if range_id:
        return range_id[0][0]
    range_id = insert_dosage_range_db(range.min, range.max)
    return range_id


def insert_dosage(dosage):
    value_id = range_id = None
    if dosage.simple:
        value_id = insert_dosage_value(dosage.simple)

    if dosage.range:
        range_id = insert_dosage_range(dosage.range)
    dosage_id = insert_dosage_db(dosage.unit, value_id, range_id)
    return dosage_id


def insert_drug_posology(drug_id, posology_id):

    return insert_drug_posology_db(drug_id, posology_id)
