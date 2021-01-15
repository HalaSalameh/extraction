import os
import pkg_resources

INPUT_FOLDER_PATH = 'Data/Outputs/Introduction_composition'
INPUT_FOLDER_PATH = pkg_resources.resource_filename(__name__, INPUT_FOLDER_PATH)

OUTPUT_FOLDER_PATH_CHEM = 'Data/chem_prediction_all_files'
OUTPUT_FOLDER_PATH_CHEM = pkg_resources.resource_filename(__name__, OUTPUT_FOLDER_PATH_CHEM)

OUTPUT_FOLDER_PATH_NECHEM = 'Data/nechem_prediction_all_files'
OUTPUT_FOLDER_PATH_NECHEM = pkg_resources.resource_filename(__name__, OUTPUT_FOLDER_PATH_NECHEM)

OUTPUT_FOLDER_PATH_WITHOUT = 'Data/without_prediction_all_files'
OUTPUT_FOLDER_PATH_WITHOUT = pkg_resources.resource_filename(__name__, OUTPUT_FOLDER_PATH_WITHOUT)


MODEL_CHEM_PATH = 'Data/models/model_chem_spaces/compositions_chem_spaces_epoch53.model'
MODEL_CHEM_PATH = pkg_resources.resource_filename(__name__, MODEL_CHEM_PATH)

MODEL_NECHEM_PATH = 'Data/models/model_nechem_spaces/compositions_nechem_spaces_epoch31.model'
MODEL_NECHEM_PATH = pkg_resources.resource_filename(__name__, MODEL_NECHEM_PATH)

MODEL_WITHOUT_PATH = 'Data/models/model_without_spaces/compositions_without_spaces_epoch55.model'
MODEL_WITHOUT_PATH = pkg_resources.resource_filename(__name__, MODEL_WITHOUT_PATH)



def get_composition_deep_predict(file_name):

    # chem predict
    chem_model = "Data/models/model_chem_spaces"
    chem_model = pkg_resources.resource_filename(__name__, chem_model)

    command = "deep-crf predict " + INPUT_FOLDER_PATH + '/' + file_name + "  --delimiter=\" \" --model_filename " + MODEL_CHEM_PATH + " --save_dir " + \
        chem_model +  " --save_name  compositions_chem_spaces" + \
       " --predicted_output "+ \
              OUTPUT_FOLDER_PATH_CHEM + '/' + file_name
    # print(command)
    os.system(command)

    # without predict
    without_model ="Data/models/model_without_spaces"
    without_model = pkg_resources.resource_filename(__name__, without_model)

    command = "deep-crf predict " + INPUT_FOLDER_PATH + '/' + file_name + "  --delimiter=\" \" --model_filename " + MODEL_WITHOUT_PATH + " --save_dir " + \
              without_model+ " --save_name  compositions_without_spaces" + \
              " --predicted_output " + \
              OUTPUT_FOLDER_PATH_WITHOUT + '/' + file_name
    os.system(command)

    nechem_model = "Data/models/model_nechem_spaces"
    nechem_model = pkg_resources.resource_filename(__name__, nechem_model)

    # nechem predict
    command = "deep-crf predict " + INPUT_FOLDER_PATH + '/' + file_name + "  --delimiter=\" \" --model_filename " + MODEL_NECHEM_PATH + " --save_dir " + \
             nechem_model + " --save_name  compositions_nechem_spaces" + \
              " --predicted_output " + \
              OUTPUT_FOLDER_PATH_NECHEM + '/' + file_name
    os.system(command)

    print(file_name, 'composition prediction ready')