# from database_conn import *
from extraction.database_conn import get_interaction, insert_interction_db, insert_drug_interaction_db


def insert_interaction(interaction_name):

    interaction_id = get_interaction(interaction_name)
    if interaction_id:
        return interaction_id[0][0]

    interaction_id = insert_interction_db(interaction_name)

    return interaction_id


def insert_drug_interaction(interaction_name, drug_id):
    interaction_id = insert_interaction(interaction_name)
    return insert_drug_interaction_db(drug_id,interaction_id)
