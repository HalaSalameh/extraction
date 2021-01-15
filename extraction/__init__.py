import pkg_resources
from extraction.extract_company import extract_company

from extraction.extract_therapeutic import therapeutic_extraction

from extraction.database_conn import insert_drug, insert_file_db
from extraction.extract_composition_deep import read_deep_res
from extraction.extract_drug_interactions import extract_interactions_for_one_file
from extraction.extract_interaction_deep import read_interaction_deep_res
from extraction.extract_side_effects import side_effect_extraction
from extraction.extraction_system import extract_all_files
import os
import re

from extraction.predict_composition_deep import get_composition_deep_predict
from extraction.predict_interactions_deep import get_interaction_deep_predict
from extraction.sectioning_labeling import section_and_label
from extraction.predict_dosage_deep import get_dosage_deep_predict
from extraction.extract_dosage_deep import read_dosage_deep_res
from extraction.store_composition import insert_drug_database


def extract_file(path, file_name):

    section_and_label(file_name, path)
    file_name = re.sub(' ', '_', file_name)
    file_name = re.sub('&', '_', file_name)
    file_name = re.sub('\(', '_', file_name)
    file_name = re.sub('\)', '_', file_name)

    path = "Data/Outputs/Introduction_composition/"
    path = pkg_resources.resource_filename(__name__, path)
    composition_intro_section_file = path + os.sep + file_name.split(".")[0] + ".txt"

    path = "Data/Outputs/Side_Effects/"
    path = pkg_resources.resource_filename(__name__, path)
    side_effect_file =path + os.sep + file_name.split(".")[0] + ".txt"

    path = "Data/Outputs/Drug_Interactions/"
    path = pkg_resources.resource_filename(__name__, path)
    drug_interaction_file =path + os.sep + file_name.split(".")[0] + ".txt"

    path = "Data/Outputs/Dosage/"
    path = pkg_resources.resource_filename(__name__, path)
    drug_dosage_file = path + os.sep + file_name.split(".")[0] + ".txt"

    path = "Data/Outputs/Therapeutic/"
    path = pkg_resources.resource_filename(__name__, path)
    drug_thera_file = path + os.sep + file_name.split(".")[0] + ".txt"

    path = "Data/Outputs/Company/"
    path = pkg_resources.resource_filename(__name__, path)
    company_file = path + os.sep + file_name.split(".")[0] + ".txt"

    drug_id = 0
    drug_name = ""

    print(composition_intro_section_file)
    if os.path.isfile(composition_intro_section_file) and os.stat(composition_intro_section_file).st_size > 1:
        get_composition_deep_predict(file_name.split(".")[0] + ".txt")
        drug_id, drug_name = read_deep_res(file_name.split(".")[0] + ".txt")

    else:
        drug_id = insert_drug_database(None)
        drug_name = "default"

    if os.path.isfile(side_effect_file):
        side_effect_extraction(file_name.split(".")[0] + ".txt", drug_id, drug_name)

    if os.path.isfile(company_file):
        extract_company(file_name.split(".")[0] + ".txt", drug_id)

    if os.path.isfile(drug_thera_file):
        therapeutic_extraction(file_name.split(".")[0] + ".txt", drug_id)

    if os.path.isfile(drug_dosage_file):
        get_dosage_deep_predict(file_name.split(".")[0] + ".txt")
        read_dosage_deep_res(file_name.split(".")[0] + ".txt", drug_id)

    if os.path.isfile(drug_interaction_file):
        get_interaction_deep_predict(file_name.split(".")[0] + ".txt")
        read_interaction_deep_res(file_name.split(".")[0] + ".txt", drug_id)

    insert_file_db(file_name.split(".")[0], drug_id)

    return drug_id