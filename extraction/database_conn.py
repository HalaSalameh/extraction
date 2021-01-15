import mysql.connector


class DatabaseConnector(object):
    def __init__(self):
        self._db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd='root',
            db="graduation_new"
        )
        self._db_cur = self._db_connection.cursor()

    def query(self, query, params):
        self._db_cur.execute(query , params)
        return self._db_cur.fetchall()

    def query_insert(self, query, params):
        self._db_cur.execute(query , params)
        self._db_connection.commit()
        return self._db_cur.lastrowid

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()


def insert_drug(drug_name, normalized, name_en):
    connector = DatabaseConnector()
    query = """INSERT INTO drug (name,normalized,name_en) VALUES (%s,%s,%s) """
    params = (drug_name, normalized, name_en)
    return connector.query_insert(query, params)


def get_drug(drug_name):
    connector = DatabaseConnector()
    query = """select id from side_effect where name = %s"""
    params = (drug_name,)
    return connector.query(query, params)


def insert_side_effect(side_effect,umls_code=None):
    connector = DatabaseConnector()
    query = """INSERT INTO side_effect (name,umls_code) VALUES (%s,%s) """
    params = (side_effect,umls_code or "")
    return connector.query_insert(query, params)


def get_side_effect_from_code(code):
    connector = DatabaseConnector()
    query = """select id from side_effect where umls_code = %s"""
    params = (code,)
    return connector.query(query, params)


def insert_side_effect_synonym(side_effect_id, synonym):
    connector = DatabaseConnector()
    query = """INSERT INTO side_effect_synonym (side_effect_id, name) values 
            (%s,%s);"""
    params = (side_effect_id, synonym)
    return connector.query_insert(query, params)


def insert_side_effect_for_drug(drug_id, synonym_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_side_effect_synonym (drug_id,  synonym_id) values 
              (%s,%s)"""
    params = (drug_id, synonym_id)
    return connector.query_insert(query, params)


def get_synonym_id(synonym):
    connector = DatabaseConnector()
    query = """SElECT id from side_effect_synonym  where name = %s ;"""
    params = (synonym,)
    return connector.query(query, params)


def insert_composition_db(composition, translation, umls_code):
    connector = DatabaseConnector()
    query = """INSERT INTO composition (name,name_en,umls_code) VALUES (%s,%s,%s) """
    params = (composition,translation,umls_code)
    return connector.query_insert(query, params)


def get_composition(composition_name):
    connector = DatabaseConnector()
    query = """select id from composition where name = %s"""
    params = (composition_name,)
    return connector.query(query, params)


def insert_composition_for_db(composition_for):
    connector = DatabaseConnector()
    query = """INSERT INTO composition_for (name) VALUES (%s) """
    params = (composition_for,)
    return connector.query_insert(query, params)


def insert_drug_composition_for_db(drug_composition_id, composition_for_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_composition_for (drug_composition_id,composition_for_id) VALUES (%s,%s) """
    params = (drug_composition_id, composition_for_id)
    return connector.query_insert(query, params)


def insert_drug_composition_effective(drug_id, composition_id, value, unit):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_composition_effective (drug_id,composition_id,unit,value) VALUES (%s,%s,%s,%s) """
    if value != "":
        params = (drug_id, composition_id, unit, float(value))
    else:

        query = """INSERT INTO drug_composition_effective (drug_id,composition_id,unit) VALUES (%s,%s,%s) """
        params = (drug_id, composition_id, unit)

    print(query, params)
    return connector.query_insert(query, params)


def insert_drug_composition_non_effective(drug_id, composition_id, value, unit):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_composition_non_effective (drug_id,composition_id,unit,value) VALUES (%s,%s,%s,%s) """
    if value != "":
        params = (drug_id, composition_id, unit, float(value))
    else:
        query = """INSERT INTO drug_composition_non_effective (drug_id,composition_id,unit) VALUES (%s,%s,%s) """
        params = (drug_id, composition_id, unit)

    return connector.query_insert(query, params)


def insert_interction_db(interaction_name, name_en, type):
    connector = DatabaseConnector()
    query = """INSERT INTO interaction (name, name_en, inter_type) VALUES (%s,%s,%s) """
    params = (interaction_name, name_en, type)
    return connector.query_insert(query, params)


def get_interaction(interaction_name):
    connector = DatabaseConnector()
    query = """select id from interaction where name = %s"""
    params = (interaction_name,)
    return connector.query(query, params)


def insert_drug_interaction_db(drug_id, interaction_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_interaction (drug_id,interaction_id) VALUES (%s,%s) """
    params = (drug_id, interaction_id)
    return connector.query_insert(query, params)


def insert_file_db(file_name,drug_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_file_name (file_name,drug_id) VALUES (%s,%s) """
    params = (file_name, drug_id)
    return connector.query_insert(query, params)


def get_all_files_db():
    connector = DatabaseConnector()
    query = """select file_name, drug_id from drug_file_name"""
    params = ()
    return connector.query(query, params)


def get_composition_en(drug_id):
    connector = DatabaseConnector()
    query = """select composition_id from drug_composition_effective where drug_id = %s"""
    params = (drug_id,)
    comps = []
    comp_ids = connector.query(query, params)
    for comp in comp_ids:
        query = """select name_en from composition where id = %s"""
        params = (comp[0],)
        comp_en = connector.query(query, params)
        comps.append(comp_en[0])
    return comps


def get_therapeutic(therapeutic_name):
    connector = DatabaseConnector()
    query = """select id from therapeutic where name = %s"""
    params = (therapeutic_name,)
    return connector.query(query, params)


def get_therapeutic_from_names(therapeutic_name, name_en):
    connector = DatabaseConnector()
    query = """select id from therapeutic where name = %s or name_en = %s"""
    params = (therapeutic_name,name_en)
    return connector.query(query, params)


def get_therapeutic_arabic_name(name_en):
    print("inside???")
    connector = DatabaseConnector()
    query = """select name from therapeutic where  name_en = %s"""
    params = (name_en,)
    return connector.query(query, params)


def insert_drug_therapeutic_db(drug_id, therapeutic_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_therapeutic (drug_id,therapeutic_id) VALUES (%s,%s) """
    params = (drug_id, therapeutic_id)
    return connector.query_insert(query, params)


def insert_therapeutic_db(therapeutic_name, therapeutic_en_name):
    connector = DatabaseConnector()
    query = """INSERT INTO therapeutic (name,name_en) VALUES (%s,%s) """
    params = (therapeutic_name, therapeutic_en_name)
    return connector.query_insert(query, params)


def insert_stop_db(stop_value):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_stop (value) VALUES (%s) """
    params = (stop_value,)
    return connector.query_insert(query, params)


def insert_duration_db(dur_value):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_duration (value) VALUES (%s) """
    params = (dur_value,)
    return connector.query_insert(query, params)


def insert_relation_db(relation_value):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_relation (value) VALUES (%s) """
    params = (relation_value,)
    return connector.query_insert(query, params)


def insert_frequency_db(value, period):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_frequency (value,period) VALUES (%s,%s) """
    params = (value, period)
    return connector.query_insert(query, params)


def insert_case_db(description):
    connector = DatabaseConnector()
    query = """INSERT INTO target_case (description) VALUES (%s) """
    params = (description,)
    return connector.query_insert(query, params)


def insert_target_being_db(description):
    connector = DatabaseConnector()
    query = """INSERT INTO target_being (description) VALUES (%s) """
    params = (description,)
    return connector.query_insert(query, params)


def insert_posology_target_being_db(posology_id, target_id):
    connector = DatabaseConnector()
    query = """INSERT INTO posology_target_being (posology_id,target_being_id) VALUES (%s,%s) """
    print(posology_id, target_id)
    params = (posology_id, target_id)
    return connector.query_insert(query, params)


def insert_posology_case_db(posology_id, case_id):
    connector = DatabaseConnector()
    query = """INSERT INTO posology_target_case (posology_id,target_case_id) VALUES (%s,%s) """
    params = (posology_id, case_id)
    return connector.query_insert(query, params)


def insert_dosage_value_db(value):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_value (value) VALUES (%s) """
    params = (value,)
    return connector.query_insert(query, params)


def insert_dosage_range_db(min, max):
    connector = DatabaseConnector()
    query = """INSERT INTO dosage_range (min_value, max_value) VALUES (%s,%s) """
    params = (min, max)
    return connector.query_insert(query, params)


def insert_dosage_db(unit, value_id, range_id):
    connector = DatabaseConnector()
    if value_id:
        query = """INSERT INTO dosage (unit,simple_value_id) VALUES (%s,%s) """
        params = (unit, value_id)
        return connector.query_insert(query, params)

    if range_id:
        query = """INSERT INTO dosage (unit,range_id) VALUES (%s,%s) """
        params = (unit, range_id)

        return connector.query_insert(query, params)

    query = """INSERT INTO dosage (unit) VALUES (%s) """
    params = (unit,)
    return connector.query_insert(query, params)


def insert_posology_db(relation_id, dur_id, freq_id, stop_id, dosage_id):

    connector = DatabaseConnector()
    query = """INSERT INTO posology (relation_id,duration_id,frequency_id,stop_id,dosage_id) VALUES (%s,%s,%s,%s,%s) """
    params = (relation_id, dur_id, freq_id, stop_id, dosage_id)
    return connector.query_insert(query, params)


def get_target_being_db(description):
    connector = DatabaseConnector()
    query = """select id from target_being where description = %s"""
    params = (description,)
    return connector.query(query, params)


def get_case_db(description):
    connector = DatabaseConnector()
    query = """select id from target_case where description = %s"""
    params = (description,)
    print(query)
    return connector.query(query, params)


def get_dosage_value_db(value):
    connector = DatabaseConnector()
    query = """select id from dosage_value where value = %s"""
    params = (value,)
    return connector.query(query, params)


def get_dosage_range_db(min, max):
    connector = DatabaseConnector()
    query = """select id from dosage_range where min_value = %s and max_value = %s"""
    params = (min, max)
    return connector.query(query, params)


def insert_drug_posology_db(drug_id, posology_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_posology (drug_id,posology_id) VALUES (%s,%s) """
    params = (drug_id, posology_id)
    return connector.query_insert(query, params)


def insert_drug_comapny_db(drug_id, comp_id):
    connector = DatabaseConnector()
    query = """INSERT INTO drug_company (drug_id,company_id) VALUES (%s,%s) """
    params = (drug_id, comp_id)
    return connector.query_insert(query, params)


def insert_company_db(comapny):
    connector = DatabaseConnector()
    query = """INSERT INTO company (name) VALUES (%s) """
    params = (comapny,)
    return connector.query_insert(query, params)


def get_company_db(name):
    connector = DatabaseConnector()
    query = """select id from company where name = %s"""
    params = (name,)
    return connector.query(query, params)
