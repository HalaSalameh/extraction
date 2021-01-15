import os
import re
import pkg_resources

from extraction.store_company import insert_drug_company

INPUT_DIR = 'Data/Outputs/Company'
INPUT_DIR = pkg_resources.resource_filename(__name__, INPUT_DIR)

key_words = ["بيت جالا", "Co.", "شركة", "فارما", "مختبرات", "مختبرات", "مختبر", "الصيدلانية", "للصناعة الدوائية",
             "المستحضرات الطبية", "لصناعات الدوائية"]
special_key_words = ["مصنع من قبل", "المنتج", "صاحب التسجيل", "اسم المنتج", "الشركة المصنعة", "صاحب الامتياز"]
stop_words = ["م.ض.", "م.ض", "ص.ب", "م.ش"]


def normalize_arabic(text):

    text = re.sub("-", " - ", text)
    text = re.sub("ـ", "", text)
    text = re.sub("ــ", "", text)
    text = re.sub("ـــ", "", text)
    text = re.sub("ــــ", "", text)
    text = re.sub("ـــــ", "", text)
    text = re.sub("ــ", "", text)
    text = re.sub("- ", " - ", text)
    text = re.sub("یٍ", "ي", text)
    text = re.sub("ی","ي" , text)
    text = re.sub("ّ", "", text)
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub("ھ", "ة", text)
    text = re.sub("  ", " ", text)
    text = re.sub("َ", "", text)
    text = re.sub("ً", "", text)
    text = re.sub("ُ", "", text)
    text = re.sub("ٌ", "", text)
    text = re.sub("ِ", "", text)
    text = re.sub("ٍ", "", text)
    text = re.sub("ّ", "", text)
    text = re.sub("إ", "ا", text)
    return text


def company_name(section):

    section = normalize_arabic(section)
    section = re.split("[\n,:،]", section)
    section = [sec.strip() for sec in section if sec.strip()]

    comp = ""
    for i in range(len(section)):

        section[i] = ' '.join([sec for sec in section[i].split(" ") if len(sec) != 1])
        section[i] = section[i]
        if i != len(section) and any(sent in section[i] for sent in special_key_words):

            comp = section[i+1]
            break
        elif any(sent in section[i] for sent in key_words):
            comp = section[i]
            break

        if len(comp) == 0:
            comp = section[0]

    return comp


def filter_result(section):

    comp = company_name(section)
    comp = re.sub(r"[\(\[].*?[\)\]]", "", comp)

    comp = comp.split(" ")
    comp_sent = []

    if len(comp) > 5:
        comp = comp[:5]
    for i in range(len(comp)):

        if comp[i] in stop_words:
            break
        else:
            comp_sent.append(comp[i])

    return comp_sent


def extract_company(file_name, drug_id):
    file = open(INPUT_DIR + os.path.sep + file_name, 'r', encoding='utf-8')
    company = file.read()
    company = re.sub('[0-9]+', '', company)

    comp = filter_result(company)
    company_final_name = ' '.join(comp)
    company_final_name = re.sub('بالامكان', '', company_final_name)
    company_final_name = re.sub('تبليغ', '', company_final_name)
    company_final_name = re.sub('بواسطة', '', company_final_name)
    company_final_name = re.sub('انتاج', '', company_final_name)
    company_final_name = re.sub('http', '', company_final_name)
    company_final_name = re.sub('شارع', '', company_final_name)
    insert_drug_company(company_final_name, drug_id)

