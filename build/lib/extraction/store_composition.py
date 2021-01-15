# from database_conn import *
from extraction.normalize_string import normalize_arabic, translate_and_fix

from extraction.database_conn import insert_drug, get_composition, insert_composition_db, \
    insert_drug_composition_effective, insert_drug_composition_for_db, insert_drug_composition_non_effective, \
    insert_composition_for_db

drug_id = 0

def insert_drug_database(drug_name):

    drug_id = 0
    if drug_name:
        drug_id = insert_drug(drug_name,normalize_arabic(drug_name))
    else:
        drug_id = insert_drug("default","default")
        drug_name = "default"

    return drug_id, drug_name


def insert_composition (composition_name):

    comp_id = get_composition(composition_name)
    # print(comp_id)
    if comp_id:
        return comp_id[0][0]
    translation =  translate_and_fix(composition_name,'ar','en')
    comp_id = insert_composition_db(composition_name,translation)
    return comp_id


def insert_comosition_effective(composition_id,num,unit,drug_id):

    compossition_effective_id = insert_drug_composition_effective(drug_id,composition_id,num,unit)
    return compossition_effective_id


def insert_drug_composition_for(for_id,comp_id):

    drug_for_comp_id = insert_drug_composition_for_db(comp_id,for_id)
    return drug_for_comp_id


def insert_comosition_non_effective(composition_id,num,unit,drug_id):
    compossition_effective_id = insert_drug_composition_non_effective(drug_id, composition_id, num, unit)
    return compossition_effective_id


def insert_for(for_name):
    for_id = insert_composition_for_db(for_name)
    return for_id



