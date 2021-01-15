import os
import re

import pkg_resources
from extraction.store_drug_interaction import insert_drug_interaction

from extraction.modify_data_for_deep import modify

PREDICTED_DIR = 'Data/drug_interactions_deep_predict'
PREDICTED_DIR = pkg_resources.resource_filename(__name__, PREDICTED_DIR)

ORIGINAL_DATA_DIRECTORY = 'Data/Outputs/Drug_Interactions'
ORIGINAL_DATA_DIRECTORY = pkg_resources.resource_filename(__name__, ORIGINAL_DATA_DIRECTORY)


def get_list(data):
    data = re.sub("\n", " ", data)
    data = re.sub("\r", " ", data)
    data = re.sub(' +', ' ', data)

    words = data.split(' ')
    try:
        while True:
            words.remove('')
    except Exception as e:
        pass
    return words


all_tags = []


def get_interactions():
    global all_tags, original_words
    interaction_indexes = [i for i, x in enumerate(all_tags) if x == "B-INTER"]
    interaction_tags = [original_words[x] for x in interaction_indexes]

    inter_in_indexes = [i for i, x in enumerate(all_tags) if x == "I-INTER"]
    inter_in_tags = [original_words[x] for x in inter_in_indexes]

    interactions = []

    for i in range(len(interaction_indexes)):
        interactions.append(interaction_tags[i])

    for i in range(len(inter_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(interactions)):
            inter_obj = interactions[j]
            if min_dest >= inter_in_indexes[i] - interaction_indexes[j] > 0:
                index = j

        if index != -1:
            interactions[index] = interactions[index] + " " + inter_in_tags[i]

    return interactions


def read_interaction_deep_res(file_name,drug_id):
    global all_tags, original_words

    or_file = ORIGINAL_DATA_DIRECTORY + os.path.sep + file_name
    file = open(or_file, 'r', encoding='utf-8')
    original_data = modify(file.read())
    original_words = get_list(original_data)

    file_pred = PREDICTED_DIR + os.path.sep + file_name
    file = open(file_pred, 'r', encoding='utf-8')
    INTERACTIONS_tags = file.read()
    all_tags = get_list(INTERACTIONS_tags)

    interactions = get_interactions()
    for inter in interactions:
        insert_drug_interaction(inter, drug_id)
