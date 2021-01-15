import os

import pkg_resources

from extraction.modify_dosage import modify_dosage_text

INPUT_FOLDER_PATH = 'Data/Outputs/Dosage'
INPUT_FOLDER_PATH = pkg_resources.resource_filename(__name__, INPUT_FOLDER_PATH)

OUTPUT_FOLDER_PATH = 'Data/dosage_deep_predict'
OUTPUT_FOLDER_PATH = pkg_resources.resource_filename(__name__, OUTPUT_FOLDER_PATH)

MODEL_PATH = 'Data/models/dosage_model_13_12/drug_dosage_train_13_12_epoch48.model'
MODEL_PATH = pkg_resources.resource_filename(__name__, MODEL_PATH)


def get_dosage_deep_predict(file_name):

    file_path_in = INPUT_FOLDER_PATH
    file_path_in = file_path_in + os.path.sep + file_name
    file = open(file_path_in, 'r', encoding='utf-8')
    section = file.read()
    data = modify_dosage_text(section)
    file.close()
    file = open(file_path_in, 'w', encoding='utf-8')
    file.write(data)
    file.close()

    model = "Data/models/dosage_model_13_12"
    model = pkg_resources.resource_filename(__name__, model)

    command = "deep-crf predict " + INPUT_FOLDER_PATH + '/' + file_name + "  --delimiter=\" \" --model_filename " + \
              MODEL_PATH + " --save_dir " + model + " --save_name  drug_dosage_train_13_12" \
              + " --predicted_output " + OUTPUT_FOLDER_PATH + '/' + file_name
    os.system(command)
    print(file_name, 'dosage prediction ready')
