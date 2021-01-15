from extraction.database_conn import get_therapeutic, insert_therapeutic_db, insert_drug_therapeutic_db


def insert_therapeutic(therapeutic_name, therapeutic_name_en):

    therapeutic_id = get_therapeutic(therapeutic_name)
    if therapeutic_id:
        return therapeutic_id[0][0]

    therapeutic_id = insert_therapeutic_db(therapeutic_name, therapeutic_name_en)

    return therapeutic_id


def insert_drug_therapeutic(therapeutic_name, drug_id, therapeutic_name_en):
    therapeutic_id = insert_therapeutic(therapeutic_name, therapeutic_name_en)
    return insert_drug_therapeutic_db(drug_id, therapeutic_id)


