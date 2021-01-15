# from database_conn import *
# from synonymous_bzu import *
# from side_effect_wiki import *
# from UMLS_retrieval import *
# from UMLS_check import *
import re

import pkg_resources

from extraction.UMLS_check import check
from extraction.UMLS_retrieval import get_code
from extraction.database_conn import get_synonym_id, insert_side_effect_for_drug, get_side_effect_from_code, \
    insert_side_effect_synonym, insert_side_effect
from extraction.normalize_string import normalize_arabic
from extraction.side_effect_wiki import check_words


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def read_human_parts_and_stop_words():
    global human_parts
    file = "Data/utils/human_parts_2.txt"
    file = pkg_resources.resource_filename(__name__, file)
    file = open(file, 'r', encoding="utf-8")
    parts = file.read()
    parts = normalize_arabic(parts)
    human_parts = re.split('[\n ]', parts)

def store_side_effect(side_effect_synonym, drug_id):

    from_database = get_synonym_id(side_effect_synonym)
    side_effect = None
    if len(from_database) > 0 :
        synonym_id = from_database[0][0]
        insert_side_effect_for_drug(drug_id, synonym_id)
    else:
        results, found = get_code(side_effect_synonym)

        found2 = False
        i = 0
        if found and len(results) >0:
            while not found2 and i < len(results):
                umls_code = results[i][0]
                side_effect_id = get_side_effect_from_code(umls_code)
                if side_effect_id:
                    side_effect_id =  side_effect_id[0][0]
                    synonym_id = insert_side_effect_synonym(side_effect_id,side_effect_synonym)
                    insert_side_effect_for_drug(drug_id, synonym_id)
                    found2 = True
                else:
                    UMLS_categories = ['Finding', 'Disease or Syndrome', 'Pathologic Function', 'Sign or Symptom',
                                  'Therapeutic or Preventive Procedure', 'Mental or Behavioral Dysfunction']
                    is_side_effect = check(umls_code, UMLS_categories)
                    if is_side_effect or is_side_effect == "UN":

                        side_effect_id = insert_side_effect(chunk_string(results[i][1], 255).__next__(), umls_code)
                        found2 = True
                        synonym_id = insert_side_effect_synonym(side_effect_id,side_effect_synonym)
                        insert_side_effect_for_drug(drug_id, synonym_id)
                    else:
                        found2 = False
                    i += 1

        else:
            found, side_effect = check_words(side_effect_synonym)
            if found:
                side_effect_original = side_effect
                side_effect = re.sub('(.*?)', '', side_effect)
                if side_effect == "":
                    side_effect = side_effect_original
                synonym_id_array = get_synonym_id(side_effect)
                if len(synonym_id_array) > 0:
                    synonym_id = synonym_id_array[0][0]
                    insert_side_effect_for_drug(drug_id, synonym_id)
                else:
                    side_effect_id = insert_side_effect(side_effect)
                    synonym_id_orignal = insert_side_effect_synonym(side_effect_id, side_effect_synonym)
                    if side_effect != side_effect_synonym:
                        synonym_id = insert_side_effect_synonym(side_effect_id, side_effect)
                    insert_side_effect_for_drug(drug_id, synonym_id_orignal)
            else:

                side_effect_id = insert_side_effect(side_effect_synonym)
                synonym_id = insert_side_effect_synonym(side_effect_id, side_effect_synonym)
                insert_side_effect_for_drug(drug_id, synonym_id)