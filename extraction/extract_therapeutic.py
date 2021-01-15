import os
import re

import copy
import pkg_resources
from mtranslate import translate
from snowballstemmer import stemmer
from extraction.database_conn import get_composition_en
from extraction.drug_bank import get_class_from_composition
from extraction.extract_side_effects import normalize_arabic
from extraction.normalize_string import chunks
from extraction.similarity import sim_word
from extraction.store_therapeutic import insert_drug_therapeutic
from extraction.therapeutic_drugs_site import  get_drug_class_from_drugs_site
from extraction.utils.spell_correction import get_google_spelling

INPUT_DIR = 'Data/Outputs/Therapeutic'
INPUT_DIR = pkg_resources.resource_filename(__name__, INPUT_DIR)

OUTPUT_DIR = 'Data/Therapeutic_res'
OUTPUT_DIR = pkg_resources.resource_filename(__name__, OUTPUT_DIR)

LOG_DIR = 'Data/therapeutic_res_log'
LOG_DIR = pkg_resources.resource_filename(__name__, LOG_DIR)

# TODO for pip add resourse

non_theraupeutic_keywords = ["التاثير العلاجي", "الفصيلة العلاجية", "الفعالية العلاجية", "الفاعلية العلاجية",
                             "فعاليه الدواء الطبيه", "الفعاليه الطبيه", 'المجموعة العلاجية', "الفاعليه الدواءيه",
                             'المجموعة الطبية', 'تأثيرات الدواء الطبية', "طبية", "طب", "دكتور", "طبيب", "طيف واسع",
                             "مدى واسع", "مستحضر", "اسع الطيف", "تاثيرات", "الفاعليه العلاجيه", "دواء", "الدواء",
                             "الادوية", "الأدوية", "ادوية", "أدوية", "الطبية", "طبيه", "الطبيه", "واسع", "لطيف",
                             "معا", "الفعالية", "الفعالية", "يؤخذ", "عن طريق", "ايام", "أيام", "اكبر", "أكبر",
                             "نجاعة", "مغم", "ملغم", "كغم", "ساعة", "ساعه", "ساعات", "تصنيف", "التصنيف", "فئة",
                             "الفئة", "فئه", "الفئه", "حبوب", "اقراص", "حقن", "مثل", "المستحضر", "استعمال",
                             "يجوز", "الفصيله العلاجيه"]

patterns = []
drug_classes = []
non_stemmed_classes = []
drug_classes_level = []
drug_classes_ar = []
drug_class_non_stemmed = []

ar_stemmer = stemmer("arabic")
en_stemmer = stemmer("english")


class TherapeuticActivity():
    def __init__(self, en_name, ar_name, en_non_stemmed,level):
        self.en_name = en_name
        self.ar_name = ar_name
        self.en_non_stemmed = en_non_stemmed
        self.level = level


def stemming(word):
    global en_stemmer
    return en_stemmer.stemWord(word)


def read_stop_words_drug_classes():
    global patterns, drug_classes, non_stemmed_classes, drug_class_non_stemmed

    path = "utils/stopwords.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file = open(path, 'r', encoding="utf-8")
    stop_words = file.read()
    stop_words = normalize_arabic(stop_words)
    stop_words_ar = re.split('[\n ]', stop_words)
    for arr in chunks(stop_words_ar, 15):
        stop_words_arr = ' | '.join(arr)
        stop_words_arr = " " + stop_words_arr + " "
        patterns.append(re.compile(stop_words_arr))

    path = "utils/drug_classes_drug.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file_en = open(path, 'r', encoding="utf-8")
    parts_en = file_en.read()
    parts_en = re.split('[\n]', parts_en)
    path = "utils/drug_classes_ar.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file_ar = open(path, 'r', encoding="utf-8")
    parts_ar = file_ar.read()
    parts_ar = re.split('[\n]', parts_ar)
    drug_classes = []
    drug_class_non_stemmed = []

    for i in range(len(parts_en)):
        splits_en = parts_en[i].split('.')
        thera = TherapeuticActivity(splits_en[1], parts_ar[i], splits_en[0], splits_en[0])
        thera.en_name = re.sub(" agents", " ", thera.en_name)
        thera.en_name = re.sub("agents ", " ", thera.en_name)
        thera.en_name = re.sub(" for ", " ", thera.en_name)
        thera.en_name = re.sub(" drugs", " ", thera.en_name)
        thera.en_name = re.sub("drugs ", " ", thera.en_name)
        thera.en_name = re.sub("-", "", thera.en_name)
        thera.en_non_stemmed = re.sub("-", "", thera.en_name)
        thera_new = copy.deepcopy(thera)
        drug_class_non_stemmed.append(thera_new)
        thera.en_name = " ".join([stemming(word) for word in thera.en_name.split(" ")])
        drug_classes.append(thera)


read_stop_words_drug_classes()


def remove_stop_words(text):
    text = " " + text + " "
    for pattern in patterns:
        text = re.sub(pattern, " ", text)

    return text


def get_sim_words(drug_class, sentence):
    corrected = []
    drug_class_sent = drug_class.split(" ")
    words = sentence.split(" ")
    for word in words:
        word = stemming(word)
        for drug_word in drug_class_sent:
            if sim_word(word.lower(), drug_word.lower()) <= 0:
                corrected.append(word)
                break
    corrected = len(list(set(corrected)))
    return corrected / len(drug_class_sent)


def get_english_compositions(drug_id):
    compositions = get_composition_en(drug_id)
    return list(set(compositions))


def is_leaf(thera):
    return thera.level != 1


def get_drug_class_from_compositions(compositions):
    classes = []
    base_url = ''
    # print(compositions)
    for comp in compositions:
        comp = comp[0]
        comp = re.sub(r"[^a-zA-Z ]", "", comp)
        found, class_obj = get_class_from_composition(comp)
        if found:
            classes += class_obj
    return list(set(classes))


def therapeutic_extraction(file_name, drug_id):
    file_path = INPUT_DIR + os.path.sep + file_name
    logs = []

    if os.path.isfile(file_path):
        file = open(INPUT_DIR + os.path.sep + file_name, 'r', encoding='utf8')
        section = file.read()
    else:
        # print("No section found")
        logs.append("NO section found")
        out_file = open(LOG_DIR + os.path.sep + file_name, 'w', encoding='utf8')
        out_file.write('\n'.join(logs))
        out_file.close()
        return
    section = normalize_arabic(section)
    section = remove_stop_words(section)
    results = re.split("[\n+:,)(()?!،:.]| و | او | و", section)
    thers = []
    en_thers = []

    leafs = []
    print(results)
    for res in results:
        res = res.strip()
        # res = re.sub(r'\([^)]*\)', '', res)
        for non_thera in non_theraupeutic_keywords:
            if non_thera in res:
                # print(non_thera)
                res = res.replace(non_thera, ' ')
        res = translate(res, "en", "ar")
        res = get_google_spelling(res)
        res = re.sub(" - ", "", res)
        res = re.sub("-", "", res)
        res = re.sub(r"/\s+/", " ", res)
        res = re.sub(r"[^a-zA-Z ]", "", res)
        res = res.strip()
        if len(res) == 0:
            continue
        print(res)
        logs.append("res: " + res)
        flag = False
        for i in range(len(drug_classes)):
            drug_class_name = drug_classes[i].en_name.strip()
            if len(drug_class_name) == 0:
                continue
            res = re.sub("-", "", res)
            sim_deg = get_sim_words(drug_class_name, res)
            if sim_deg >= 0.65:
                # print(drug_class_name, " match with ", res, "sith sim = ", sim_deg)
                logs.append("1. from the ordinary match : " + drug_classes[i].ar_name)
                if is_leaf(drug_classes[i]):
                    leafs.append(drug_classes[i])
                if drug_classes[i].ar_name not in thers:
                    thers.append(drug_classes[i].ar_name)
                    en_thers.append(drug_class_non_stemmed[i].en_name)
                    print(drug_classes[i].ar_name, "---", drug_class_non_stemmed[i].en_name)
                flag = True

        if not flag:
            drugs_site_classes = get_drug_class_from_drugs_site(res)
            print(drugs_site_classes)
            if len(drugs_site_classes) > 0:
                drug_site_class = re.sub(" agents", " ", drugs_site_classes[0])
                drug_site_class = re.sub("agents ", " ", drug_site_class)
                drug_site_class = re.sub(" for ", " ", drug_site_class)
                drug_site_class = re.sub(" drugs", " ", drug_site_class)
                drug_site_class = re.sub("drugs ", " ",drug_site_class)
                drug_site_class = re.sub("-", "", drug_site_class)
                drug_site_class = " ".join([stemming(word) for word in drug_site_class.split(" ")])
                print(drug_site_class)
                for class_obj in drug_classes:
                    # print(class_obj.en_name.strip())
                    if class_obj.en_name.strip().lower() == drug_site_class.strip().lower():
                        thers.append(class_obj.ar_name)
                        en_thers.append(drug_class_non_stemmed[drug_classes.index(class_obj)].en_name)
                        print(class_obj.ar_name, "---", drug_class_non_stemmed[drug_classes.index(class_obj)].en_name)
                        print("matched")
                        logs.append("2. from the drugs.com match : " + class_obj.ar_name)
                        if is_leaf(class_obj):
                            leafs.append(class_obj)
                        break
        logs.append("=======================================================================")

    if len(leafs) == 0:
        logs.append("No results from 1 & 2")
        drug_bank_results = get_drug_class_from_compositions(get_english_compositions(drug_id))
        for drug_bank_res in drug_bank_results:
            # if drug_bank_res != ""
            drugs_site_classes = get_drug_class_from_drugs_site(drug_bank_res)
            if len(drugs_site_classes) > 0:
                drug_site_class = re.sub("-", "", drugs_site_classes[0])
                drug_site_class = " ".join([stemming(word) for word in drug_site_class.split(" ")])
                for class_obj in drug_classes:
                    if class_obj.en_name.strip() == drug_site_class.strip():
                        thers.append(class_obj.ar_name)
                        en_thers.append(drug_class_non_stemmed[drug_classes.index(class_obj)].en_name)
                        print(class_obj.ar_name, "---", drug_class_non_stemmed[drug_classes.index(class_obj)].en_name)
                        logs.append("3. from the drugBank & drugs.com match : " + class_obj.ar_name)
                        break

    print(en_thers)
    # thers = list(set(thers))
    # en_thers = list(set(en_thers))
    print(thers)
    taken = []
    for i in range(len(thers)):
        if thers[i] in taken:
            continue
        taken.append(thers[i])
        print(en_thers[i], "   ^^^^   ",thers[i])
        insert_drug_therapeutic(thers[i], drug_id, en_thers[i])

    # out_file = OUTP
    #
    #
    # UT_DIR + os.path.sep + file_name
    # out_file = pkg_resources.resource_filename(__name__, out_file)
    # out_file = open(out_file, 'w', encoding='utf8')
    # out_file.write('\n'.join(thers))
    # out_file.close()
    # out_file = LOG_DIR + os.path.sep + file_name
    # out_file = pkg_resources.resource_filename(__name__, out_file)
    # out_file = open(out_file, 'w', encoding='utf8')
    # out_file.write('\n'.join(logs))
    # out_file.close()
    print("Done")
