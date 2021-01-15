# -*- coding: utf-8 -*-

import os
import re

import pkg_resources
from nltk.tokenize import StanfordSegmenter
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag
from snowballstemmer import stemmer
import nltk

from extraction.store_side_effect import store_side_effect
from extraction.utils.spell_correction import get_google_spelling

INPUT_PATH = "Data/Outputs/Side_Effects"
OUTPUT_PATH = "Data/side_effects_res"

side_effects_keywords = ["مثل", "طبيب", "طبيبك", "جانبية", "الطبيب", "تاثيرات", "التاثيرات", "الجانبية", "الطبيب",
                         "مثال", "يسبب", 'يشمل', "تحدث", "يحدث", "يحصل", "يؤدي الى", "هي:", "شائعة", "شائعة:",
                         "شائعة جدا", "غير شائعة", "نادرة", "نادرة:", "نادرة جدا", "غير معروفة", "الاكثر شيوعا",
                         "الاتية", "مثلا", "اعراضه", "العلاج", "الحوامل", "تناول", "في حال", "لاحظت", "يصنف", "العام",
                         "حاملا", "جانبية غير معروف", "احدى تلك الاعراض", "غير المرغوب فيها", "اهتماما", "اعراض",
                         "الاعراض", "التالية", "الدواء", "دواء", "الجرعات", "شىوعا", "السىاقة", "النشرة", "صيدلي",
                         "الاطفال", "الصيدلي", 'للدواء', "الصيدلاني", "صحتك", "بشكل", "بشكل عام", "الجرعة", "يسبب",
                         "استعمال", "نادرا", "يؤدي", "اوقف", "احيانا", "يسبب", "راجع", "ىحدث", "أحيانا", "الاعراض"
                         , "تتطلب", "راجع", "اوقف", "يترتب", "فورا", "الاستعمال", "الاستعمال", "عانيت", "تعاني", "تسبب",
                         "كنت", "تعاني", "خاصة"

                         ]

stop_keywords = ["مثال", "يشمل", "مثل", "تشمل", "يشملون", "تضم", "تحدث", "يحدث", "يضم", "في حال"]

self_standing_words = ["صداع", "الصداع", "جوع", "الجوع", "اعياء", "الاعياء", "نعاس", "النعاس", "النعس", "تعب", "التعب",
                       "دوار", "الدوار", "غثيان", "الغثيان", "قيء", "القيء", "الاسھال", "اسهال", "تقيؤ", "التقيؤ",
                       "حكة", "الحكة", "امساك", "الامساك", "طفح", "الطفح", "ارتيكاريا", "الارتيكاريا", "جلوكوما",
                       "الجلوكوما", "شري", "الشري", "بثور", "البثور", "لسعة", "اللسعة", "تحوصل", "التحوصل", "دوخان",
                       "الدوخان", "تقشر", "التقشر", "التقشير", "تقشير", "ارهاق", "الارهاق", "سعال", "السعال",
                       "ارتباك", "الارتباك", "التعرق", "تعرق", "صفير", "الصفير", "الدوخة", "دوخة", "اكتئاب", "الاكتئاب",
                       "انتحار", "الانتحار", 'نفخة', "النفخة", "صمم", "الصمم", "عمى", "العمى", "بكم", "البكم",
                       "طرش", "الطرش", "تشنجات", "التشنجات", "القلق", "قلق", "العصبية", "عصبية", "غضب", "الغضب",
                       "الارتعاش", "ارتعاش", "الهلوسة", "هلوسة", "التململ", "تململ", "التوهان", "توهمان", "كدمات",
                       "الكدمات", "الاغماء", "اغماق", "العطش", "عطش", "جفاف", "الجفاف", "الحمى", "حمى", "العدوانية",
                       "عدوانية", "وهن", "الوهن", "تجشؤ", "التجشؤ", "ظمأ", "الظمأ", "تلوث", "التلوث", "شمق", "الشمق",
                       "وذمات", "سخونة", "الوذمات", "السخونة", "قشعريرة", "القشعريرة", "برد", "البرد", "تجفاف",
                       "التجفاف", "الرجفان", "رجفان", "اهتياج", "الاهتياج", "ارق", "الارق", "ربو", "الربو", "تقيؤات",
                       "التقيؤات", "عدائية", "العدائية"]

all_side_effects = []
human_parts = []
stop_words_ar = []
patterns = []
pattern_side_effects = []
medical_terms = []
human_parts_stemmed = []
ar_stemmer = stemmer("arabic")
drug_name = ""

print("hello there")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def read_human_parts_and_stop_words():
    global human_parts, stop_words_ar, patterns, medical_terms, human_parts_stemmed, side_effects_keywords, pattern_side_effects, self_standing_words
    path = "utils/human_parts_2.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file = open(path, 'r', encoding="utf-8")
    parts = file.read()
    parts = normalize_arabic(parts)
    human_parts = re.split('[\n ]', parts)
    for i in range(len(human_parts)):
        human_parts_stemmed.append(stemming(human_parts[i]))

    path = "utils/stopwords.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file = open(path, 'r', encoding="utf-8")
    stop_words = file.read()
    stop_words = normalize_arabic(stop_words)
    stop_words_ar = re.split('[\n ]', stop_words)
    patterns = []
    pattern_side_effects = []
    for arr in chunks(stop_words_ar, 15):
        stop_words_arr = ' | '.join(arr)
        stop_words_arr = " " + stop_words_arr + " "
        patterns.append(re.compile(stop_words_arr))

    for arr in chunks(side_effects_keywords, 15):
        side_effects_keywords = ' | '.join(arr)
        side_effects_keywords = " " + side_effects_keywords + " "
        pattern_side_effects.append(re.compile(side_effects_keywords))

    path = "utils/medical_terms.txt"
    path = pkg_resources.resource_filename(__name__, path)
    file = open(path, 'r', encoding="utf-8")
    terms = file.read()
    medical_terms = normalize_arabic(terms)
    medical_terms = re.split('[\n ]', medical_terms)

    for i in range(len(medical_terms)):
        medical_terms[i] = stemming(medical_terms[i])
    self_standing_words = [normalize_arabic(word) for word in self_standing_words ]


def remove_stop_words(text):
    text = " " + text + " "
    for pattern in patterns:
        text = re.sub(pattern, " ", text)

    return text


def normalize_arabic(text):
    text = re.sub("[إأٱا]", "ا", text)
    text = re.sub("[ىی]", "ي", text)
    text = re.sub("[إأٱآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    text = re.sub("[یییيىی]", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("ـ", "", text)
    text = re.sub("  ", " ", text)
    text = re.sub("َ", "", text)
    text = re.sub("ً", "", text)
    text = re.sub("ُ", "", text)
    text = re.sub("ٌ", "", text)
    text = re.sub("ِ", "", text)
    text = re.sub("ٍ", "", text)
    text = re.sub("ّ", "", text)
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub("[ککککک]", "ك", text)
    text = re.sub("ھ", "ه", text)
    text = re.sub("چ", "ج", text)
    text = re.sub("ھ", "ه", text)
    return text


def stemming(word):
    global ar_stemmer
    return ar_stemmer.stemWord(word)


def check_if_string_contains(string, word):
    string_words = string.split()
    if word in string_words:
        return string_words.index(word)
    return -1


def split_string(string, word):
    all_words = string.split()
    if word in all_words:
        i = all_words.index(word)
        str1 = " ".join(all_words[:i + 1])
        if i != len(all_words) - 1:
            str2 = " ".join(all_words[i + 1:])
        else:
            str2 = ""

        return str1, str2
    else:
        return string, None


def remove_non_keywords(text):
    text = re.sub("[ىی]", "ي", text)
    text = " " + text + " "
    global pattern_side_effects

    for pattern in pattern_side_effects:
        text = re.sub(pattern, " ", text)

    text = re.sub(drug_name, "", text)

    return text


def check_if_keyword(section):
    global all_side_effects
    section_sentences = []
    initial_section_sentences = re.split("[(-,.\\؛،_:\];[?ـ\-\)\n-]", section)
    # initial_section_sentences = [re.sub(r'[^ء-يa-zA-Z \n]', '', sent) for sent in initial_section_sentences]

    stop_words_arr = ' | '.join(stop_keywords)
    for sentence in initial_section_sentences:
        pattern = re.compile(stop_words_arr)
        arrs = re.split(pattern, sentence)
        for word in arrs:
            section_sentences.append(word)

    for i in range(len(section_sentences)):
        if section_sentences[i].strip() != '\n' and section_sentences[i].strip() != '' and len(
                section_sentences[i].strip()) != 0:
            sentence = normalize_arabic(section_sentences[i].strip())
            sentence = re.sub(r'[^ء-يa-zA-Z \n]', '', sentence)
            if check_if_side_effect(sentence):
                new_sentence = remove_non_keywords(section_sentences[i].strip())
                new_sentence = remove_stop_words(new_sentence)
                all_side_effects.append(new_sentence)



nltk.download('stopwords')
#print('C:/Users/dell/Documents/graduation_backup/standford/stanford-segmenter-2018-10-16' \
      #'/data/;C:/Users/dell/Documents/graduation_backup/standford/stanford-postagger-full' \
      #'-2018-10-16/models/ ')
#os.environ['STANFORD_MODELS'] = 'C:/Users/dell/Documents/graduation_backup/standford/stanford-segmenter-2018-10-16' \
                                #'/data/'
path = "standford/stanford-segmenter-2018-10-16/data/"
path = pkg_resources.resource_filename(__name__, path)
os.environ['STANFORD_MODELS'] = path

path="standford/stanford-parser-full-2018-10-16"
path = pkg_resources.resource_filename(__name__, path)
os.environ['CLASSPATH'] = path
# os.environ['JAVAHOME'] = 'C:/Program Files/Java/jre1.8.0_171'

path="standford/stanford-segmenter-2018-10-16/stanford-segmenter-3.9.2.jar"
path = pkg_resources.resource_filename(__name__, path)
segmenter = StanfordSegmenter(path)
segmenter.default_config('ar')


def check_if_side_effect(sentence):
    for word in sentence.split(" "):
        word = stemming(word)
        if word and word in medical_terms or word in human_parts_stemmed and word.strip() != "":
            return True

    return False


def split_conjunc(sentence):

    path_1 = "standford/stanford-postagger-full-2018-10-16/models/arabic.tagger"
    path_1 = pkg_resources.resource_filename(__name__, path_1)
    path_2 = "standford/stanford-postagger-full-2018-10-16/stanford-postagger.jar"
    path_2 = pkg_resources.resource_filename(__name__, path_2)

    arabic_postagger = POS_Tag(path_1,path_2)
    sentences = sentence.split("\n")
    sentences = [x for x in sentences if x.strip()]
    is_adjective = lambda pos: pos[:2] == 'NN' or pos[:2] == 'VB'
    side_effects_values = []

    for sentence in sentences:

        full_sentence = sentence

        array = full_sentence.split()
        if len(array) > 0 and (array[0] == 'و' or array[0] == 'او'):
            array = array[1:]
        if not 'و' in array and not 'او' in array:
            side_effects_values.append(' '.join(array))
            continue

        tokenized = nltk.word_tokenize(' '.join(array))
        tags_tok = arabic_postagger.tag(tokenized)
        adjective = [(pos + word).split('/')[0] for (word, pos) in tags_tok if is_adjective((pos + word).split('/')[1])]
        tags = [(pos + word).split('/')[1] for (word, pos) in tags_tok]
        current_adj = []
        prev_adj = []
        new_list = []

        if len(adjective) > 0 and adjective[0] not in human_parts:
            side_effect_common_sentence = adjective[0]
            for i in range(len(array)):

                if array[i] in self_standing_words:
                    side_effects_values.append(array[i])
                    side_effects_values += current_adj
                    current_adj = []
                    prev_adj = []
                    continue

                if tags[i] == "DTNN" and array[i] not in human_parts and (i == 0 or array[i - 1] in (["و", "او"])):
                    adjective.append(array[i])
                    current_adj.append(array[i])

                elif array[i] not in (["و", "او"]) and array[i] not in human_parts \
                        and array[i] not in adjective:
                    side_effect_common_sentence = side_effect_common_sentence + " " + array[i]
                    current_adj = [(adj + " " + array[i]) for adj in current_adj]
                    if len(current_adj) == 0 and len(prev_adj) != 0:
                        if len(side_effects_values) > 0:
                            side_effects_values[len(side_effects_values) - 1] += " " + array[i]

                elif array[i] not in (["و", "او"]) and array[i] in human_parts:
                    prev_adj = current_adj
                    sentence1 = side_effect_common_sentence + " " + array[i]
                    current_effects = [(adj + " " + array[i]) for adj in current_adj]

                    for effect in current_effects:
                        effect_check = normalize_arabic(effect)
                        if check_if_side_effect(effect_check):
                            side_effects_values.append(effect)
                            new_list.append(effect)
                    current_adj = []

                elif array[i] in (["و", "او"]):
                    if i + 1 != len(array):
                        if array[i + 1] in human_parts:
                            current_effects = [(adj + " " + array[i + 1]) for adj in prev_adj]
                            for effect in current_effects:
                                effect_check = normalize_arabic(effect)
                                if check_if_side_effect(effect_check):
                                    side_effects_values.append(effect)
                                    new_list.append(effect)
                            i += 1

                elif array[i] in adjective and i != 0 and array[i - 1] in adjective:
                    current_adj = [(adj + " " + array[i]) for adj in current_adj]

                else:
                    current_adj.append(array[i])

        elif array[0] not in human_parts:

            sentences = re.split("و | او", full_sentence)
            for sent in sentences:
                effect_check = normalize_arabic(sent)
                if check_if_side_effect(effect_check):
                    side_effects_values.append(sent)
                    new_list.append(sent)

        for effect in current_adj:
            effect_check = normalize_arabic(effect)
            if check_if_side_effect(effect_check):
                side_effects_values.append(effect)
                new_list.append(effect)

    return side_effects_values

read_human_parts_and_stop_words()


def side_effect_extraction(file_name, drug_id, drug_name_str):
    print("inside side effects")
    global all_side_effects, drug_name,INPUT_PATH
    drug_name = re.sub("[ىی]", "ي", drug_name_str)
    file_path_in = INPUT_PATH
    file_path_in = file_path_in + os.path.sep + file_name
    file_path_in = pkg_resources.resource_filename(__name__, file_path_in)
    file = open(file_path_in, 'r', encoding='utf-8')
    section = file.read()
    section = re.sub("[ىی]", "ي", section)
    all_side_effects = []
    check_if_keyword(section)
    file_path = OUTPUT_PATH + os.path.sep + file_name
    file_path = pkg_resources.resource_filename(__name__, file_path)
    out = open(file_path, "w", encoding="utf8")
    
    side_effects_string = '\n'.join(all_side_effects)
    
    out.write(side_effects_string)
    out.close()

    side_effects_string_after_seg = segmenter.segment_file(file_path)
    
    side_effects_new = side_effects_string_after_seg.split('\n')
    side_effects_new = '\n'.join(side_effects_new)
        
    side_effects_new = split_conjunc(side_effects_new)
    side_effects_new = list(set(side_effects_new))

    for i in range(len(side_effects_new)):
        side_effects_new[i] = get_google_spelling(side_effects_new[i])

    side_effects_new = list(set(side_effects_new))

    for side_effect in side_effects_new:
        if side_effect.strip() == "" or side_effect in human_parts or side_effect in human_parts_stemmed:
            continue
        print(side_effect)
        # side_effect = get_google_spelling(side_effect)
        store_side_effect(side_effect, drug_id)
    out = open(file_path, "w", encoding="utf8")
    out.write('\n'.join(side_effects_new))
    out.close()
    print("done")
