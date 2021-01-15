import os
import re
from googletrans import Translator

from extraction.UMLS_check import check
from extraction.UMLS_retrieval import get_code
from extraction.drug_interactions_wiki import check_if_chemical
from extraction.normalize_string import chunks, normalize_arabic
from extraction.store_drug_interaction import insert_drug_interaction
from extraction.webteb import get_web_teb_text
import pkg_resources

translator = Translator()

INPUT_DIR = 'Data/Outputs/Drug_Interactions'
OUTPUT_DIR = 'Data/drug_interactions_res'
interactions_key_words = ["التالية", "يلي", "الاتية", "المجموعات", "التفاعلات مع", "خاصة مع", "خاصة", "المتزامن مع",
                          "في نفس الوقت مع", "تنتمي إلى", "مثل", ":"]

removed_keywords = ["ناجعة", "تفاعلات", "طبيبك", "صيدلاني", "ممرض", "الاخرى", "اخرى", "كبير", "كثير", "مثل", "مجموعة",
                    "مجموعات", "العلاج", "حاملا", "دواء", "مرضعا", "اطفال", "نجاح", "علاج", "اخر", "نجاعة",
                    "للدواء", "علاجا", "دواءا", "مخاطر", "المخاطر", "يسبب", "تجنب", "الجرعة", "لتجنب", "بدواء",
                    "انهيت", "تناول", "الدواء", "التفاعلات", "التوقف", "الاطفال", "الرضع", "الدوائية", "ظهور",
                    "بالعلاج", "الدواء", "النجاعة", "الجرعه", "الصيدلي", "تحتاج", "طبية", "طبي", "طب", "الطبيب"
                    "عقاقير", "لتفادي", "المعالج", "تتعاطي", "اعلام", "انهيت", "الناتجه", "اضافيا", "ناجمة", "ساعتين",
                    "اعراض", "جانبية", "تناولها", "المرضي", "انتباه", "مهم", "تنتمي", "تفاعل", "مرضعه", "تحذير",
                    "للاستعمال", "الخارجي", "استخدام", "استشارة", "الصيدلاني", "يقلل", "فعالية", "اخطار", "حوامل",
                    "فترة", "وحدة", "انتظار", "يجب", "الحمل", "استعمال", "ابلاغ", "تاثير ", "جانبي", "طفل", "وسائل",
                    "ساعة", "تناول", "استشر", "استشارة", "مدة", "موضعي", "تقارير", "فئات", "تتعارض", "الاخطار", "ارضاع"]

patterns = []


def read_stop_words():

    global patterns
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


read_stop_words()


def remove_stop_words(text):
    text = " " + text + " "
    for pattern in patterns:
        text = re.sub(pattern, " ", text)

    return text


def check_if_interaction(interaction):

    categories = ["Biologically Active Substance", "Pharmacologic Substance", "Element, Ion, or Isotope",
                  "Organic Chemical", "Antibiotic"]
    translated = ""
    try:
        translation = translator.translate(interaction, src='ar')
        # print("Translation ", translation.text)
        (code, found_UMLS) = get_code(translation.text)
        if found_UMLS:
            found_translation = check(code[0][0], categories)
            if found_translation:
                return True
        translated = translation.text
    except:
        translated=""
    (found, title) = get_web_teb_text(interaction)
    
    found_web_teb = False
    if found:
        i = 0
        while not found_web_teb and i < len(title):
            (code, found_UMLS) = get_code(title[i])
            if found_UMLS:
                found_web_teb = check(code[0][0], categories)
                # print("found from webteb ", title[i])
                if found_web_teb:
                    return True
            i += 1

    wiki = check_if_chemical(translated)
    if not wiki:
        wiki = check_if_chemical(interaction)
        print("from Arabic wiki ", wiki, "word ",interaction)
    else:
        print("from english wiki ", wiki," word ", interaction)

    return wiki


def check_if_keyword(section):
    global removed_keywords
    removed_keywords = [normalize_arabic(word) for word in removed_keywords]
    for key in interactions_key_words:
        key = normalize_arabic(key)
        if normalize_arabic(key) in normalize_arabic(section):
            text_parts = section.split(key)
            if len(text_parts) >= 2:
                interactions_text = ' '.join(text_parts[1:])
                interactions_text = interactions_text.strip()
                possible_interactions = re.split("[(-,;\*\\.،،؛::)\n-]| و | او | و", interactions_text)
                possible_interactions = [interaction.strip() for interaction in possible_interactions
                                         if len(interaction) > 1]

                interactions = []
                for inter in possible_interactions:
                    inter = ' '.join([inter_word for inter_word in inter.split(" ")
                                      if not any(xs in inter_word for xs in removed_keywords)])
                    inter = re.sub(r'[^ء-يa-zA-Z \n]', '', inter)
                    if check_if_interaction(inter):
                        interactions.append(inter)
                    else:
                        pass
                        # print("out : ", inter)
                return interactions

    return ""


def extract_interactions_for_one_file(file_name, drug_id):
    global OUTPUT_DIR
    file_path = INPUT_DIR + os.path.sep + file_name
    file_path = pkg_resources.resource_filename(__name__, file_path)
    section = ''
    if os.path.isfile(file_path):
        file = open(file_path, 'r', encoding='utf8')
        section = file.read()
    else:
        print("No section found")
        return 
    section = normalize_arabic(section)
    section = remove_stop_words(section)
    results = check_if_keyword(section)
    results = [result.strip() for result in results if len(result) > 1]
    out_path = OUTPUT_DIR
    out_path = out_path + os.path.sep + file_name
    out_path = pkg_resources.resource_filename(__name__, out_path)
    out_file = open(out_path, 'w', encoding='utf8')
    out_file.write('\n'.join(results))
    for interaction in results:
        insert_drug_interaction(interaction,drug_id)


