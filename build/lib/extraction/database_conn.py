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


def insert_drug(drug_name,normalization):
    connector = DatabaseConnector()
    query = """INSERT INTO drug (name,normalized) VALUES (%s,%s) """
    params = (drug_name, normalization)
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


def insert_composition_db(composition, translation):
    connector = DatabaseConnector()
    query = """INSERT INTO composition (name,name_en) VALUES (%s,%s) """
    params = (composition, translation)
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


def insert_interction_db(interaction_name):
    connector = DatabaseConnector()
    query = """INSERT INTO interaction (name) VALUES (%s) """
    params = (interaction_name,)
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
