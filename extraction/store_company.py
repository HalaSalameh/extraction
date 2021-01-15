from extraction.database_conn import insert_company_db, insert_drug_comapny_db, get_company_db


def insert_company(comapny):
    comp_id = get_company_db(comapny)
    if comp_id:
        return comp_id[0][0]

    comp_id = insert_company_db(comapny)
    return comp_id


def insert_drug_company(comapny, drug_id):
    comp_id = insert_company(comapny)
    return insert_drug_comapny_db(drug_id, comp_id)


