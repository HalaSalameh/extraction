# from database_conn import *
import re

import pkg_resources
from pyphonetics import Soundex, Metaphone, RefinedSoundex

from extraction.UMLS_Composition import get_code

from extraction.normalize_string import normalize_arabic, translate_and_fix, distance_words

from extraction.database_conn import insert_drug, get_composition, insert_composition_db, \
    insert_drug_composition_effective, insert_drug_composition_for_db, insert_drug_composition_non_effective, \
    insert_composition_for_db

drug_id = 0

from mtranslate import translate


def translate_drug_name(word):
    term = "اسمي"
    full_word = term+" "+word
    en_word = translate(full_word, "en", "ar")
    en_word = en_word.replace('My name is', '').strip()
    return en_word


def insert_drug_database(drug_name):

    drug_id = 0
    if drug_name:
        soundex = Soundex()
        metaphone = Metaphone()
        rs = RefinedSoundex()
        file_path = "utils//DRUGS_ALL_EDITTED.csv"
        file_path = pkg_resources.resource_filename(__name__, file_path)
        file = open(file_path, "r")
        section = file.read()
        parts = re.split('[\n]', section)
        min_dist = 100
        new_name = re.sub("چ", "غ", drug_name)
        new_name = re.sub("ﻏ", "غ", new_name)
        new_name = normalize_arabic(new_name)
        name_en = translate_drug_name(drug_name)
        equals = []
        min_index = -1
        min_dist_all = 100
        min_index_all = -1
        chosen = False

        for part in parts:

            if distance_words(name_en, part) == 0 or distance_words(name_en, part) == 1:
                chosen = True
                print(" Matched To ->", part)
                drug_id = insert_drug(drug_name, normalize_arabic(drug_name), part)
                return drug_id, drug_name

            dist = rs.distance(name_en, part)
            if dist <min_dist_all:
                min_dist_all = dist
                min_index_all = parts.index(part)

            if soundex.sounds_like(new_name, part) or soundex.sounds_like(name_en, part):

                if rs.distance(new_name, part) < min_dist:
                    min_dist = rs.distance(new_name, part)
                    min_index = parts.index(part)
                equals.append((part,metaphone.phonetics(part)))

        if min_index != -1:
            for equ in equals:
                if equ[1] == metaphone.phonetics(name_en) or equ == metaphone.phonetics(new_name):
                    drug_id = insert_drug(drug_name, normalize_arabic(drug_name), equ[0])
                    chosen = True
                    return drug_id, drug_name

        if not chosen and min_index != -1:
            chosen = True
            drug_id = insert_drug(drug_name, normalize_arabic(drug_name), parts[min_index])
            return drug_id, drug_name

        if not chosen:
            drug_id = insert_drug(drug_name, normalize_arabic(drug_name), parts[min_index_all])
            return drug_id, drug_name

    else:
        drug_id = insert_drug("----------", "----------", "----------")
        drug_name = "default"
        return drug_id, drug_name

    return drug_id, drug_name


def insert_composition(composition_name):

    print("inserting ",composition_name)
    comp_id = get_composition(composition_name)
    # print(comp_id)
    if comp_id:
        return comp_id[0][0]
    translation = translate_and_fix(composition_name, 'ar', 'en')
    umls_code = ""
    result, found2 = get_code(translation)
    if found2:
        umls_code = result
    comp_id = insert_composition_db(composition_name, translation, umls_code)
    return comp_id


def insert_comosition_effective(composition_id, num, unit, drug_id):

    compossition_effective_id = insert_drug_composition_effective(drug_id,composition_id,num,unit)
    return compossition_effective_id


def insert_drug_composition_for(for_id,comp_id):

    drug_for_comp_id = insert_drug_composition_for_db(comp_id,for_id)
    return drug_for_comp_id


def insert_comosition_non_effective(composition_id, num, unit, drug_id):
    compossition_effective_id = insert_drug_composition_non_effective(drug_id, composition_id, num, unit)
    return compossition_effective_id


def insert_for(for_name):
    for_id = insert_composition_for_db(for_name)
    return for_id



