# from database_conn import *
import re

import pkg_resources
import pubchempy as pcp
from mtranslate import translate

from extraction.UMLS_Composition import get_code
from extraction.UMLS_check import check
from extraction.therapeutic_drugs_site import get_drug_class_from_drugs_site

from extraction.database_conn import get_interaction, insert_interction_db, insert_drug_interaction_db, \
    get_therapeutic_arabic_name, get_therapeutic_from_names, get_composition
from extraction.utils.spell_correction import get_google_spelling


def insert_interaction(interaction_name):

    print(interaction_name)
    translated = translate(interaction_name, 'en', 'ar')
    translated_spelled = get_google_spelling(translated)

    interaction_id = get_interaction(interaction_name)
    if interaction_id:
        return interaction_id[0][0]

    comp_id = get_composition(interaction_name)
    if comp_id:

        interaction_id = insert_interction_db(interaction_name, translated_spelled,  "0")
        return interaction_id

    thera_id = get_therapeutic_from_names(interaction_name, translated_spelled)
    if thera_id:
        thera_id = insert_interction_db(interaction_name, translated_spelled,  "1")
        return thera_id


    try:
        results = pcp.get_substances(translated_spelled, 'name')
        if len(results) > 0:
            print("from pcp")
            interaction_id = insert_interction_db(interaction_name, translated_spelled, "0")
            return interaction_id
        else:
            res = re.sub(" - ", "", translated_spelled)
            res = re.sub("-", "", res)
            res = re.sub(r"/\s+/", " ", res)
            res = re.sub(r"[^a-zA-Z ]", "", res)
            res = res.strip()
            print(res)
            thera = get_drug_class_from_drugs_site(res)
            if len(thera) > 0:
                print("thera now " , thera[0])
                thera_ar = get_therapeutic_arabic_name(thera[0])
                if thera_id:
                    interaction_id = insert_interction_db(thera_ar, translated_spelled, "1")
                    return interaction_id
                else:
                    file_en_dir = "utils/drug_classes_drug.txt"
                    file_en_dir = pkg_resources.resource_filename(__name__, file_en_dir)
                    file_en = open(file_en_dir, 'r', encoding="utf-8")
                    parts_en = file_en.read()

                    file_ar_dir = "utils/drug_classes_ar.txt"
                    file_ar_dir = pkg_resources.resource_filename(__name__, file_ar_dir)
                    parts_en = re.split('[\n]', parts_en)
                    file_ar = open(file_ar_dir, 'r', encoding="utf-8")
                    parts_ar = file_ar.read()
                    drug_site_class = re.sub(" agents", " ", thera[0])
                    drug_site_class = re.sub("agents ", " ", drug_site_class)
                    drug_site_class = re.sub(" for ", " ", drug_site_class)
                    drug_site_class = re.sub(" drugs", " ", drug_site_class)
                    drug_site_class = re.sub("drugs ", " ", drug_site_class)
                    drug_site_class = re.sub("-", "", drug_site_class)

                    for i in range(len(parts_en)):
                        parts_en[i] = parts_en[i].split('.')[0]
                        parts_en[i] = re.sub(" agents", " ", parts_en[i])
                        parts_en[i] = re.sub("agents ", " ", parts_en[i])
                        parts_en[i] = re.sub(" for ", " ", parts_en[i])
                        parts_en[i] = re.sub(" drugs", " ", parts_en[i])
                        parts_en[i] = re.sub("drugs ", " ", parts_en[i])
                        parts_en[i] = re.sub("-", "", parts_en[i])

                        if drug_site_class.strip().lower() == parts_en[i].strip().lower():
                            print("matched with thera", parts_ar[i])
                            interaction_id = insert_interction_db(parts_ar[i], translated_spelled, "1")
                            return interaction_id

                    print("couldnt match with thera ")
                    print(interaction_name, translated_spelled)
                    interaction_id = insert_interction_db(interaction_name, translated_spelled, "1")
                    return interaction_id

            else:
                print("no thera came back")
                interaction_id = insert_interction_db(interaction_name, translated_spelled, "1")

            return interaction_id

    except Exception as e:
        results, found = get_code(interaction_name)
        if found and len(results) > 0:
            categories = ["Biologically Active Substance", "Pharmacologic Substance", "Element, Ion, or Isotope",
                          "Organic Chemical", "Antibiotic"]
            found_translation = check(results[0][0], categories)
            if found_translation:
                print("from umls")
                interaction_id = insert_interction_db(interaction_name, translated_spelled, "0")
                return interaction_id

        res = re.sub(" - ", "", translated_spelled)
        res = re.sub("-", "", res)
        res = re.sub(r"/\s+/", " ", res)
        res = re.sub(r"[^a-zA-Z ]", "", res)
        res = res.strip()
        print(res)
        thera = get_drug_class_from_drugs_site(res)
        if len(thera) > 0:
            print("thera now ", thera[0])
            thera_ar = get_therapeutic_arabic_name(thera[0])
            if thera_id:
                print("from thera")
                interaction_id = insert_interction_db(thera_ar, translated_spelled, "1")
                return interaction_id
            else:
                file_en_dir = "utils/drug_classes_drug.txt"
                file_en_dir = pkg_resources.resource_filename(__name__, file_en_dir)
                file_en = open(file_en_dir, 'r', encoding="utf-8")
                parts_en = file_en.read()

                file_ar_dir = "utils/drug_classes_ar.txt"
                file_ar_dir = pkg_resources.resource_filename(__name__, file_ar_dir)
                parts_en = re.split('[\n]', parts_en)
                file_ar = open(file_ar_dir, 'r', encoding="utf-8")
                parts_ar = file_ar.read()

                for i in range(len(parts_en)):
                    drug_site_class = re.sub(" agents", " ", thera[0])
                    drug_site_class = re.sub("agents ", " ", drug_site_class)
                    drug_site_class = re.sub(" for ", " ", drug_site_class)
                    drug_site_class = re.sub(" drugs", " ", drug_site_class)
                    drug_site_class = re.sub("drugs ", " ", drug_site_class)
                    drug_site_class = re.sub("-", "", drug_site_class)

                    if drug_site_class.strip().lower() == parts_en[i].strip().lower():
                        print("matched with thera", parts_ar[i])
                        interaction_id = insert_interction_db(parts_ar[i], translated_spelled, "1")
                        return interaction_id

                print("couldnt match with thera ")
                interaction_id = insert_interction_db(interaction_name, translated_spelled, "1")
                return interaction_id

        else:
            print("no thera came back")
            interaction_id = insert_interction_db(interaction_name, translated_spelled, "1")

        return interaction_id


def insert_drug_interaction(interaction_name, drug_id):
    interaction_id = insert_interaction(interaction_name)
    return insert_drug_interaction_db(drug_id,interaction_id)
