import pkg_resources

from extraction.database_conn import insert_drug, insert_file_db
from extraction.extract_composition_deep import read_deep_res
from extraction.extract_drug_interactions import extract_interactions_for_one_file
from extraction.extract_side_effects import side_effect_extraction
from extraction.extraction_system import extract_all_files
import os
import re

from extraction.predict_composition_deep import get_composition_deep_predict
from extraction.sectioning_labeling import section_and_label


def extract_file(path,file_name):

    # path = path + os.path.sep + file_name
    # path = pkg_resources.resource_filename(__name__, path)
    # file = open(path + os.path.sep + file_name, 'r', encoding='utf-8')
    # print(file.read())
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
    drug_id = 0
    drug_name = ""
    print(composition_intro_section_file)
    if os.path.isfile(composition_intro_section_file) and os.stat(composition_intro_section_file).st_size > 1:
        get_composition_deep_predict(file_name.split(".")[0] + ".txt")
        drug_id, drug_name = read_deep_res(file_name.split(".")[0] + ".txt")

    else:
        drug_id = insert_drug("default")
        drug_name = "default"

    if os.path.isfile(side_effect_file):
        side_effect_extraction(file_name.split(".")[0] + ".txt", drug_id, drug_name)

    if os.path.isfile(drug_interaction_file):
        extract_interactions_for_one_file(file_name.split(".")[0] + ".txt", drug_id)

    return drug_id
