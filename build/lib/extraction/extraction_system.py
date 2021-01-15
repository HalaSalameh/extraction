# -*- coding: utf-8 -*-

import os
import re
# from sectioning_labeling import *
# from predict_composition_deep import *
# from database_conn import *
# from extract_side_effects import *
# from extract_drug_interactions import *
# from extract_composition_deep import *
from extraction.database_conn import insert_drug, insert_file_db
from extraction.extract_composition_deep import read_deep_res
from extraction.extract_drug_interactions import extract_interactions_for_one_file
from extraction.extract_side_effects import side_effect_extraction
from extraction.predict_composition_deep import get_composition_deep_predict
from extraction.sectioning_labeling import section_and_label

prefixs_array = ['BJ_', 'BPC_', 'DSH_', 'JER_', 'IMP_']
#prefixs_array = ['IMP_']
companies_files_names =["beitJala_docx", "bpc_docx", "Dar_Al_Shefaa_docx", "JER_docx", "imported_docx"]
#companies_files_names =["imported_docx"]
company_prefix = 'BJ_'
#company_prefix = 'BPC_'
#company_prefix = 'DSH_'
#company_prefix = 'JER_'
# company_prefix = 'IMP_'

#company_file_name = "beitJala_docx"
#company_file_name = "bpc_docx"
#company_file_name = "Dar_Al_Shefaa_docx"
company_file_name = "JER_docx"
# company_file_name = "imported_docx"

def extract_all_files():

    global company_file_name, company_prefix

    for file_name in os.listdir("/graduation_new/leaflets/" + company_file_name):


        section_and_label(company_file_name, company_prefix, file_name)
        file_name = re.sub(' ', '_', file_name)
        file_name = re.sub('&', '_', file_name)
        file_name = re.sub('\(', '_', file_name)
        file_name = re.sub('\)', '_', file_name)

        composition_intro_section_file = "../Data/Outputs/Introduction_composition/" + company_prefix + \
                                         file_name.split(".")[0] + ".txt"
        side_effect_file = "../Data/Outputs/Side_Effects/" + company_prefix + file_name.split(".")[0] + ".txt"
        drug_interaction_file = "../Data/Outputs/Drug_Interactions/" + company_prefix + file_name.split(".")[0] + ".txt"
        drug_id = 0
        drug_name = ""
        if os.path.isfile(composition_intro_section_file) and os.stat(composition_intro_section_file).st_size > 1:
            get_composition_deep_predict(company_prefix + file_name.split(".")[0]+".txt")
            drug_id,drug_name = read_deep_res(company_prefix + file_name.split(".")[0]+".txt")

        else:
            drug_id = insert_drug("default")
            drug_name = "default"

        if os.path.isfile(side_effect_file):
            side_effect_extraction(company_prefix + file_name.split(".")[0] + ".txt", drug_id, drug_name)

        if os.path.isfile(drug_interaction_file):
            extract_interactions_for_one_file(company_prefix + file_name.split(".")[0] + ".txt", drug_id)

        insert_file_db(company_prefix + file_name.split(".")[0], drug_id)



def loop_over_companies():
    global company_prefix,company_file_name
    for i in range(len(prefixs_array)):
        company_prefix = prefixs_array[i]
        company_file_name = companies_files_names[i]
        extract_all_files()


# loop_over_companies()
