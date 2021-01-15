# -*- coding: utf-8 -*-

import os
import re
import zipfile

import pkg_resources

from extraction.modify_data_for_deep import modify

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

composition_keywords = ["Composition", "التركيب",
                        "المادة الفعالة", "لتركيب الدوائي", "التركيبه", "المواد الفعالة"]
therapeutic_keywords = ["Therapeutic", "الفعالية العلاجية", "الفاعلية العلاجية",
                        "التاثير العلاجي", "فعالية الدواء الطبية", "الفاعلية الدوائية", "الاستطباب", "الفعالية الطبية",
                        "الفصيلة العلاجية", "تأثيرات الدواء الطبية", "التصنيف",
                        "المجموعة الصيدلانية", "المجموعة العلاجیة", "الإستطبابات", "المجموعة الطبية"]
before_using_keywords = ["Before_Using", "قبل استعمال", "قبل الاستعمال", "قبل استخدام", "قبل الاستخدام", "قبل تناول",
                         "قبل البدء بتناول", "قبل البدء باستخدام", "قبل البدء باستعمال"]

indications_keywords = ["Indications", "الاستعمالات", "دواعي الاستعمال", "لماذا يستعمل",
                        "استخدامات",
                        "لاي يستعمل", "استعمالات", "لماذا يستعمل", "اعد الدواء", "غرض", "دواعي الاستعمال"]

should_not_be_used_keywords = ["Should_Not_Be_Used", "لا يجوز استعمال", "متى يمنع", "لا تتناول الاقراص عندما",
                               "لا يجوز استخدام", "يمنع استخدام",
                               "لا يجوز لك استعمال", "يمنع استعمال", "موانع الاستعمال ", "يمنع تناول الأدویة",
                               "لا يجوز تناول الأدوية", "يمنع تناول الدواء", "لا يجوز تناول الدواء", "يمنع تناول أدویة",
                               "لا يجوز تناول ادوية", "الظلام", "العتمة"]

doctor_notifying_keywords = ["Doctor_Notifying", "قبل مراجعة الطبيب", "اعلم الطبيب", "استشر طبيب", "استشارة طبيب",
                             "ابلغ الطبيب", "قبل استشارة الطبيب", "تخبر طبيبك", "اسال الطبيب", "أخبر الطبيب",
                             "يقرر الطبيب"]

side_effects_keywords = ["Side_Effects", "التاثيرات الجانبية", "الاعراض الجانبية", "الأعراض الجانبية",
                         "الاثار الجانبية", "اعراض جانبية", "تعاني"]
warnings_keywoards = ["Warning", "تحذيرات", "ملاحظات", "احتياطات", "معلومات هامة", "مزيد من المعلومات",
                      "معلومات اضافية", "التحذيرات", "احتياطات:", "التحذيرات:", "الاحتياطات:", "تنبیه", "تحذيرات:",
                      "انتبه", "ملاحظة", "ملاحظة"]

drug_interaction_keywoards = ["Drug_Interactions", "تعارض", "تداخلات", "تفاعلات ادوية", "تفاعلات مع", "تفاعلات بين",
                              "تفاعلات الدواء",
                              "تفاعلات بين الادوية", "تفاعلات ما بين الادوية", "تفاعلات الدوائية",
                              "ردود فعل بين الأدوية",
                              "تناولــت مؤخـرا أدويــة أخــرى", "تناولت مؤخرا, أدوية أخرى", "تناولت في الاونة الاخيرة",
                              "تعاطيت مؤخرا",
                              "الادوية الاخرى و", "تناولت في الفترة الأخيرة", "تفاعلات الأدوية", "والأدوية الأخرى",
                              "ادوية اخرى", "تناولت مؤخرا",
                              "تناولت مؤخراً", "التفاعلات بين الأدوية", "الأدوية التي يجب عدم تناولها"]

dosage_keywoards = ["Dosage", "جرعة دوائية", "جرعة موصى", "جرعة الموصى", "جرعة:", "جرعة :", "جرعة \n",
                    "جرعة الدوائية", "جرعة\n", "الجرعة", "مساء", "صباح", "يوميا", "بشكل يومي", "الجرعة الإعتيادية",
                    "المقدار الدوائي"]

forgotten_dosage_keywoards = ["Forgotten_Dosage", "في حال نسي", "في حال نسیان", "الجرعة المنسية", "نسيت تناول",
                              "نسيت إستعمال الدواء", "إذا نسيت", "الجرعة الدوائية المنسية", "فاتتك جرعة",
                              "نسيت مقدار دوائي", "نسيت تعاطي" , "الجرعة التي نسيتها"]

over_dosage_keywoards = ["Over_Dose", "افرطت", "الجرعة الزائدة", "مضاعفة الجرعه", "افراط", "الجرعة المفرطة",
                         "تجاوز الجرعة", " جرعة أعلى", " جرعة مفرطة", "جرعة دوائية اكبر", "فرط الجرعة", "جرعة إضافية",
                         "استعملت بالخطأ مقدار دوائي", "مقداراً دوائياً مفرطاً", "جرعة مضاعفة", "جرعة دوائية مفرطة",
                         "مقداراً دوائياً أكبر", "أكثر مما يجب", "جرعة أكبر"]

storage_keywoards = ["Storage", "تخزين :", "تخزين\n", "تخزين:"]
avoid_poisoning_keywoards = ["Avoid_Poisoning", "تجنب التسمم", "تجنب التسمّم", "تتجنب التسمم", "تجنبي التسمم",
                             "تجنب حدوث التسمم"]
contribution_keywoards = ["Contribution", "مساهمة في انجاح", "تساهم في انجاح", "مساهمة في نجاح", "تساهم في نجاح"]
instructions_keywoards = ["Instructions", "الاستعمال الصحيح", "إرشادات الاستعمال", "ارشادات الاستعمال",
                          "طريقة الاستعمال", "طريقة الاستخدام", "تعليمات الاستخدام", "كيفية استخدام", "تعليمات الحقن",
                          "طريقة استعمال", "كيفية إستعمال", "كيفية أخذ",
                          "الفحوصات والمتابعة", "لاختبارات والمتابعة", "الفحوص والمتابعة"]
presentation_keywoards = ["Presentation",
                          "الشكل الصيدلاني", "العبوات", "العبوة:", "العبوة :", "التعبئة", "العبوة\n", "العبوة \n",
                          "الاشكال الدوائية", "الشكل الدوائي"]
companies_keywoards = ["Company", "شركة", "شارع", "المنطقة الصناعية", "ص.ب", "شركة", "م.ض.", "م.ض", "ص.ب", "م.ش",
                       "شركة", "ص. ب."]
stop_using_keywords = ['Stop_Using', " توقفك عن إستعمال", "ايقاف استعمال", "انتهاء استعمال", "إذا توقفت عن تناول",
                       "تم التوقف عن تناول", "التوقف عن العلاج"]

keywords = [therapeutic_keywords, composition_keywords, should_not_be_used_keywords,
            doctor_notifying_keywords, side_effects_keywords, warnings_keywoards, drug_interaction_keywoards,
            stop_using_keywords,
            forgotten_dosage_keywoards, over_dosage_keywoards, dosage_keywoards, indications_keywords,
            storage_keywoards,
            avoid_poisoning_keywoards, contribution_keywoards, instructions_keywoards, presentation_keywoards,
            companies_keywoards, before_using_keywords]
outputs = []

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML


#
# previous_index = 0
# current_index = 0


def print_between(start_index, end_index, text):
    to_return = ""
    for k in range(end_index - start_index - 1):
        to_return += text[k + start_index] + "\n"
        # print(text[k + start_index ])

    # to_return += "====================\n"

    return to_return


def check_if_keywoard(title, flags, text):
    global previous_index, prev_keywoard, current_index, flag_for_before_use
    to_return = ""
    # print(title)
    # print("============")
    for i in range(len(keywords)):
        if not flag_for_before_use and i == keywords.index(before_using_keywords):
            continue
        for key in keywords[i]:
            if key in title and not flags[i]:
                if prev_keywoard == i:
                    return to_return
                flag_for_before_use = True
                to_return = print_between(previous_index,
                                          current_index, text) + "\n"
                previous_index = current_index
                if prev_keywoard == -1:
                    outputs[len(keywords)] += to_return
                else:
                    outputs[prev_keywoard] += to_return

                prev_keywoard = i
                # print(i)
                # print(to_return)
                return to_return

                # break

                # print(to_return)
    # print("***************************8")
    return to_return


def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):

        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)


def normalize_arabic(text):
    # text = re.sub(" ال", " ", text)
    text = re.sub("[إأٱآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    text = re.sub("[یىی]", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("[ھة]", "ه", text)
    text = re.sub("ـ", "", text)
    text = re.sub("  ", " ", text)
    text = re.sub("َ", "", text)
    text = re.sub("ً", "", text)
    text = re.sub("ُ", "", text)
    text = re.sub("ٌ", "", text)
    text = re.sub("ِ", "", text)
    text = re.sub("ّ", "", text)
    text = re.sub("ٍ", "", text)
    return text


for keys in keywords:
    outputs.append("")
    for i in range(len(keys)):
        keys[i] = normalize_arabic(keys[i])
outputs.append("")

previous_index = 0
prev_keywoard = -1
current_index = 0
flag_for_before_use = False


def section_and_label(file , path, company_file_name="", company_prefix=""):
    for i in range(len(outputs)):
        outputs[i] = ""
    global prev_keywoard, previous_index, current_index
    previous_index = 0
    current_index = 0
    prev_keywoard = -1

    # path = pkg_resources.resource_filename(__name__, path)
    text = get_docx_text(path + os.sep + file)

    flags = []
    for i in range(len(keywords)):
        flags.append(False)
    text = text.splitlines()
    file = file.split(".")[0]
    file = re.sub(' ', '_', file)
    file = re.sub('&', '_', file)
    file = re.sub('\(', '_', file)
    file = re.sub('\)', '_', file)
    print("in section and label")
    path = "Data/labeling_output"
    path = pkg_resources.resource_filename(__name__, path)
    out_file_name = (path + os.sep + file + ".txt")
    with open(out_file_name, 'w', encoding='utf-8') as out:
        print("printing.....", file)
        out.write("Introduction\n")
        out.write("***************\n")

        for i in range(len(text)):
            words = text[i].split(" ")
            title = ""
            current_index = i
            for j in range(min(15, len(words))):
                title = title + " " + words[j]
            back = (check_if_keywoard(normalize_arabic(title), flags, text))
            out.write(back)

        for word in text[previous_index:len(text)]:
            out.write(word)
        last = print_between(previous_index, len(text) + 1, text)
        outputs[prev_keywoard] += last

    for i in range(len(keywords)):
        if outputs[i] == "":
            continue
        path = "Data/Outputs" + os.sep + keywords[i][0] + os.sep + file + ".txt"
        path = pkg_resources.resource_filename(__name__, path)

        with open(path, 'w', encoding='utf-8') as out:
            out.write(outputs[i])

    if outputs[len(outputs) - 1] != "":

        path = "Data/Outputs/Introduction/" + file + ".txt"
        path = pkg_resources.resource_filename(__name__, path)

        with open(path, 'w', encoding='utf-8') as out:
            out.write(outputs[len(outputs) - 1])

    path = "Data/Outputs/Introduction_composition/" + file + ".txt"
    path = pkg_resources.resource_filename(__name__, path)
    with open(path, 'w', encoding='utf-8') as out:
        out.write(modify(outputs[len(outputs) - 1]) + '\n' + modify(outputs[1]))
