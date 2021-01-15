import os

import pkg_resources
from extraction.modify_data_for_deep import modify

INPUT_FOLDER_PATH = 'Data/Outputs/Drug_Interactions'
INPUT_FOLDER_PATH = pkg_resources.resource_filename(__name__, INPUT_FOLDER_PATH)

OUTPUT_FOLDER_PATH = 'Data/drug_interactions_deep_predict'
OUTPUT_FOLDER_PATH = pkg_resources.resource_filename(__name__, OUTPUT_FOLDER_PATH)

MODEL_PATH = 'Data/models/interaction_model_9_12/drug_interaction_train_9_12_epoch67.model'
MODEL_PATH = pkg_resources.resource_filename(__name__, MODEL_PATH)


def get_interaction_deep_predict(file_name):
    file_path_in = INPUT_FOLDER_PATH
    file_path_in = file_path_in + os.path.sep + file_name
    file = open(file_path_in, 'r', encoding='utf-8')
    section = file.read()
    data = modify(section)
    file.close()
    file = open(file_path_in, 'w', encoding='utf-8')
    file.write(data)
    file.close()

    model = "Data/models/interaction_model_9_12"
    model = pkg_resources.resource_filename(__name__, model)

    command = "deep-crf predict " + INPUT_FOLDER_PATH + '/' + file_name + "  --delimiter=\" \" --model_filename " + \
              MODEL_PATH + " --save_dir " + model + " --save_name  drug_interaction_train_9_12" \
              + " --predicted_output " + OUTPUT_FOLDER_PATH + '/' + file_name
    os.system(command)
    print(file_name, 'interaction prediction ready')
