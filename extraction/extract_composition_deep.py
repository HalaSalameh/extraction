# -*- coding: utf-8 -*-

import os
import re
import  pkg_resources
from extraction.modify_data_for_deep import modify
from extraction.store_composition import insert_composition, insert_comosition_non_effective, insert_drug_database, \
    insert_comosition_effective, insert_drug_composition_for, insert_for

NECHEM_DIRECTORY = 'Data/nechem_prediction_all_files'

CHEM_DIRECTORY = 'Data/chem_prediction_all_files'

ALL_COMP_DIRECTORY = 'Data/without_prediction_all_files'


ORIGINAL_DATA_DIRECTORY = 'Data/Outputs/Introduction_composition'


original_words = []
chem_tags = []
nechem_tags = []
all_tags = []
counter = 0
all = 0
drug_indexes_chem = []
b_names_chem = []

class CompositionNum:

    def __init__(self, num, taken, index):
        self.num = num
        self.taken = taken
        self.index = index

    def __repr__(self):
        return str(self.num) + " " + str(self.index)


class CompositionUnit:

    def __init__(self, unit, taken, index):
        self.unit = unit
        self.taken = taken
        self.index = index

    def __repr__(self):
        return str(self.unit) + " " +str(self.index)


class CompositionName:

    def __init__(self, chem, index):
        self.chem = chem
        self.description = ""
        self.index = index

    def __repr__(self):

        if self.description != "":
            return str(self.chem) + " " + " ( " + str(self.description) + " ) "

        else:
            return str(self.chem) + " "


class Composition:
    def __init__(self,chem,num,unit):
        self.chem = chem
        self.num = num
        self.unit = unit

    def __repr__(self):
        if self.num and self.unit:

            return "( " + str(self.chem) + " , " + str(self.num.num) + " , " + str(self.unit.unit)+" )"
        else:
            if self.num:
                return "( " + str(self.chem) + " , " + str(self.num.num) + " , " + "NO UNIT" + " )"
            else:
                if self.unit:
                    return "( " + str(self.chem) + " , " + "NO NUM" + " , " + str(self.unit.unit)+ " )"
                else:
                    return "( " + str(self.chem) + " , " + "NO NUM" + " , " + "NO UNIT" + " )"


class CompositionFor:

    def __init__(self, for_name, index):
        self.for_name = for_name
        self.index = index
        self.comps = []

    def __repr__(self):
        return str(self.for_name) + ":\n" + str(self.comps) + "\n\n"


def get_list(data):
    data = re.sub("\n", " ", data)
    data = re.sub("\r", " ", data)
    data = re.sub(' +', ' ', data)

    words = data.split(' ')
    try:
        while True:
            words.remove('')
    except Exception as e:
        pass
    return words


def is_drug_name(name):

    if name != "التركیبة" and name != "الدوائية" and name != "التركيبه" and name != "الدوائيه":
        return True


def get_drug_name(B_TAGS,b_indexes,I_TAGS,i_indexes):

    global flag, drug_name, found_name, index_ichem,counter
    drug_names = list(set(B_TAGS))
    drug_names.sort()
    if len(drug_names) >= 1:
        max_count = 0
        drug_name = found_name = ""
        index = -1

        if len(drug_names) > 1:

            for i in range(len(drug_names)):

                name = drug_names[i]
                if drug_names.count(name) > max_count and is_drug_name(name):
                    max_count = drug_names.count(name)
                    drug_name = name
                    index = b_indexes[i]

        else:
            index = b_indexes[0]
            drug_name = drug_names[0]

        found_name = drug_name
        i_chems =[]
        flag = True
        index_ichem = -1
        for i in range(len(I_TAGS)):
            i_chem = I_TAGS[i]
            if i_indexes[i] - index <= 4:
                i_chems.append(i_chem)
                index_ichem = i_indexes[i]
                flag = False
            else:
                if flag:
                    index_ichem = i_indexes[i]
                    global i_chem_new
                    i_chem_new = i_chem

            if flag:
                flag2 = True
                for i in range(len(B_TAGS)):
                    name = B_TAGS[i]
                    if b_indexes[i] - index_ichem <= 4:
                        found_name = name
                        drug_name = found_name
                        i_chems.clear()
                        i_chems.append(i_chem_new)
                        flag2 = False

                    if not flag2:
                        for index in i_indexes:
                            if abs(index - index_ichem) <=3:
                                i_chems.append(I_TAGS[i_indexes.index(index)])
            drug_name = found_name
            i_chems = list(set(i_chems))
            i_chems.sort()
        return drug_name, i_chems

    else:

        return None


def get_drug():

    global counter, all, chem_tags, nechem_tags, all_tags,drug_indexes_chem,b_names_chem

    drug_indexes_chem = [i for i, x in enumerate(chem_tags) if x == "B-DRUG"]
    b_names_chem = [original_words[x] for x in drug_indexes_chem]

    drug_indexes_nechem = [i for i, x in enumerate(nechem_tags) if x == "B-DRUG"]
    b_names_nechem = [original_words[x] for x in drug_indexes_nechem]

    drug_indexes_all = [i for i, x in enumerate(all_tags) if x == "B-DRUG"]
    b_names_all = [original_words[x] for x in drug_indexes_all]

    drug_inside_indexes_chem = [i for i, x in enumerate(chem_tags) if x == "I-DRUG"]
    b_names_inside_chem = [original_words[x] for x in drug_inside_indexes_chem]

    drug_inside_indexes_nechem = [i for i, x in enumerate(nechem_tags) if x == "I-DRUG"]
    b_names_inside_nechem = [original_words[x] for x in drug_inside_indexes_nechem]

    drug_inside_indexes_all = [i for i, x in enumerate(all_tags) if x == "I-DRUG"]
    b_names_inside_all = [original_words[x] for x in drug_inside_indexes_all]

    result = get_drug_name(b_names_all, drug_indexes_all, b_names_inside_all, drug_inside_indexes_all)
    drug_name = ""
    if result:
        drug_name = result[0]
        if result[1] != []:
            for res in result[1]:
                drug_name = drug_name + " " + res
    else:
        result = get_drug_name(b_names_nechem, drug_indexes_nechem, b_names_inside_nechem, drug_inside_indexes_nechem)
        if result:
            drug_name = result[0]
            if result[1] != []:
                for res in result[1]:
                    drug_name = drug_name + " " + res
        else:
            result = get_drug_name(b_names_chem, drug_indexes_chem, b_names_inside_chem, drug_inside_indexes_chem)
            if result:

                drug_name = result[0]
                if result[1] != []:
                    for res in result[1]:
                        drug_name = drug_name + " " + res
            else:
                all += 1
                counter += 1
                return None
    all += 1
    return drug_name


def normalize_num(num):

    num = re.sub('٫', '.', num)
    num = re.sub(',', '.', num)
    num = re.sub('‚', '.', num)
    num = re.sub('٬', '.', num)
    num = re.sub('٫', '.', num)
    num = re.sub('ه', '5', num)
    num = re.sub("[^\d\.]", "", num)

    if str(num)==".":
        return 0
    if len(num.split('.')) > 2:
        try:
            num = float(num.split('.')[0])
        except:
            num = float(num.split('.')[1])

    try:
        float(num)

    except:
        return None

    return num


def get_composition_parts(nums,units,chems):

    compositions= []
    for i  in range(len(chems)):

        obj = Composition(chem=chems[i],unit=None,num=None)
        unit_obj = None
        num_obj = None
        global min_dest
        min_dest = 100
        for num in nums:

            if abs(num.index - chems[i].index) <= min_dest and (not num.taken):

                min_dest = abs(num.index - chems[i].index)
                num_obj = num


        obj.num = num_obj

        if num_obj:
            num_obj.taken = True

        min_dest = 100
        dest = 0
        for unit in units:

            if num_obj:
                dest = abs(unit.index - num_obj.index)
            if abs(unit.index - chems[i].index) + dest <= min_dest and (not unit.taken):
                min_dest = abs(unit.index - chems[i].index)
                unit_obj = unit

        obj.unit = unit_obj
        if unit_obj:
            unit_obj.taken = True

        compositions.append(obj)

        if i != 0 and len(chems) != len(nums):

            flag_unit= True
            flag_num = True
            if compositions[i-1].unit:
                dest_unit = abs(chems[i].index - compositions[i-1].unit.index)

                if dest_unit < abs(compositions[i-1].chem.index - compositions[i-1].unit.index):
                    if obj.unit:
                        if dest_unit < abs(obj.unit.index - obj.chem.index):

                            flag_unit = True
                        else :
                            flag_unit = False
                    else:
                        flag_unit = True
                else:
                    flag_unit = False

            if compositions[i-1].num:
                dest_num = abs(chems[i].index - compositions[i-1].num.index)
                if dest_num < abs(compositions[i-1].chem.index - compositions[i-1].num.index):
                    if obj.num:
                        if dest_num < abs(obj.num.index - obj.chem.index):

                            flag_num  = True
                        else:
                            flag_num = False
                    else:
                        flag_num = True
                else:
                    flag_num = False

            if flag_unit and flag_num:
                if compositions[i-1].unit:
                    if obj.unit:
                        obj.unit.taken = False
                    obj.unit = compositions[i-1].unit
                    compositions[i - 1].unit = None


                if compositions[i-1].num:
                    if obj.num:
                        obj.num.taken = False
                    obj.num = compositions[i-1].num
                    compositions[i-1].num = None
    return compositions


def find_from_to(compositions, start, end, first):

    i = 0
    if first:
        while i < len(compositions) and compositions[i].chem.index < start:
            i += 1

        if i == len(compositions):
            return None
        return compositions[i]

    else:
        while i < len(compositions) and compositions[i].chem.index <= end:
            i += 1

        if i == len(compositions):
            return None

        return compositions[i-1]


def look_for_closest_for(composition, fors):

    min_dest = 10000
    index = -1
    for i in range(len(fors)):
        if 0 < composition.chem.index - fors[i].index < min_dest:
            index = i
            min_dest = composition.chem.index - fors[i].index

    if index != -1:
        fors[index].comps.append(composition)


def get_fors(compositions, fors):

    for i in range(len(compositions)):

        look_for_closest_for(compositions[i], fors)


def get_compositions(drug_id):

    global chem_tags, original_words

    # nums arrays
    num_indexes = [i for i, x in enumerate(chem_tags) if x == "B-NUM"]
    num_tags = [original_words[x] for x in num_indexes]

    # units arrays
    unit_indexes = [i for i, x in enumerate(chem_tags) if x == "B-UNIT"]
    unit_tags  = [original_words[x] for x in unit_indexes]

    unit_in_indexes = [i for i, x in enumerate(chem_tags) if x == "I-UNIT"]
    unit_in_tags = [original_words[x] for x in unit_in_indexes]

    # chems arrays
    chem_start_indexes = [i for i, x in enumerate(chem_tags) if x == "B-CHEM"]
    chem_start_tags = [original_words[x] for x in chem_start_indexes]

    chem_in_indexes = [i for i, x in enumerate(chem_tags) if x == "I-CHEM"]
    chem_in_tags = [original_words[x] for x in chem_in_indexes]

    # equ arrays
    equ_indexes = [i for i, x in enumerate(chem_tags) if x == "B-EQU"]
    equ_tags = [original_words[x] for x in equ_indexes]

    # for arrays
    for_indexes = [i for i, x in enumerate(chem_tags) if x == "B-FOR"]
    for_tags = [original_words[x] for x in for_indexes]

    for_in_indexes = [i for i, x in enumerate(chem_tags) if x == "I-FOR"]
    for_in_tags = [original_words[x] for x in for_in_indexes]

    # D-chem array
    chem_des_indexes = [i for i, x in enumerate(chem_tags) if x == "B-DCHEM"]
    chem_des_tags = [original_words[x] for x in chem_des_indexes]

    chem_des_in_indexes = [i for i, x in enumerate(chem_tags) if x == "I-DCHEM"]
    chem_des_in_tags = [original_words[x] for x in chem_des_in_indexes]

    # final arrays
    nums = []
    units = []
    chems = []
    fors = []

    # get num final array
    for i in range(len(num_indexes)):
        num_tags[i] = normalize_num(num_tags[i])
        if num_tags[i]:
            nums.append(CompositionNum(float(num_tags[i]), False, num_indexes[i]))

    # get units final array from minimizing the B and I tags
    for i in range(len(unit_indexes)):
        units.append(CompositionUnit(unit_tags[i], False, unit_indexes[i]))

    for i in range(len(unit_in_indexes)):
        for unit_obj in units:
            if 2 >= unit_in_indexes[i] - unit_obj.index > 0:
                unit_obj.unit = unit_obj.unit + " " + unit_in_tags[i]
                break

    # get chem final array from minimizing the B and I tags
    for i in range(len(chem_start_indexes)):
        chems.append(CompositionName(chem_start_tags[i], chem_start_indexes[i]))

    for i in range(len(chem_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(chems)):
            chem_obj = chems[j]
            if min_dest >= chem_in_indexes[i] - chem_obj.index > 0:
                index = j

        if index != -1:
            chems[index].chem = chems[index].chem + " " + chem_in_tags[i]

    # join b-dchem and i-dchem

    for i in range(len(chem_des_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(chem_des_indexes)):

            if min_dest >= chem_des_in_indexes[i] - chem_des_indexes[j] > 0:
                index = j

        if index != -1:
            chem_des_tags[index] = chem_des_tags[index] + " " + chem_des_in_tags[i]

    for i in range(len(chem_des_indexes)):
        min_dest = 5
        index = -1
        for j in range(len(chems)):
            chem_obj = chems[j]
            if min_dest >= chem_des_indexes[i] - chem_obj.index > 0:
                index = j

        if index != -1:
            chems[index].description = chem_des_tags[i]


    # get for final array from minimizing the B and I tags

    for i in range(len(for_indexes)):
        fors.append(CompositionFor(for_tags[i], for_indexes[i]))

    for i in range(len(for_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(fors)):
            for_obj = fors[j]
            if min_dest >= for_in_indexes[i] - for_obj.index > 0:
                index = j

        if index != -1:
            fors[index].for_name = fors[index].for_name + " " + for_in_tags[i]

    if len(drug_indexes_chem) > 2:
        for i in range(len(drug_indexes_chem)):
            if i != len(original_words)-1:
                if original_words[drug_indexes_chem[i] + 1].isdigit():
                    fors.append(CompositionFor(b_names_chem[i] +" "+ original_words[drug_indexes_chem[i] + 1],
                                               drug_indexes_chem[i]))

    compositions = get_composition_parts(nums, units, chems)

    # delete the extra compositions from equ
    for i in range(len(equ_tags)):

        before = find_from_to(compositions, 0, equ_indexes[i],False)
        after = find_from_to(compositions, equ_indexes[i], compositions[len(compositions)-1].chem.index,True)

        if after and after.unit and after.num:
            if before:
                compositions.remove(before)
        else:
            if after:
                compositions.remove(after)

    if len(fors) > 1:
        get_fors(compositions, fors)
        print("Effective Substances:\n")
        for for_obj in fors:
            for_id = insert_for(for_obj.for_name)
            for comp in for_obj.comps:
                comp_id = insert_composition(comp.chem.chem)
                composition_id = insert_comosition_effective(comp_id, comp.num and comp.num.num or "", comp.unit and comp.unit.unit or "", drug_id)
                for_comp_id = insert_drug_composition_for(for_id,composition_id)

        # print(fors)
    else:
        print("Effective Substances:\n")
        for comp in compositions:
            comp_id = insert_composition(comp.chem.chem)
            composition_id = insert_comosition_effective(comp_id,comp.num and comp.num.num or "",comp.unit and comp.unit.unit or "",drug_id)

        # print(compositions)


def get_non_chems(drug_id):

    global nechem_tags,original_words
    num_indexes = [i for i, x in enumerate(nechem_tags) if x == "B-NENUM"]
    num_tags = [original_words[x] for x in num_indexes]

    # units arrays
    unit_indexes = [i for i, x in enumerate(nechem_tags) if x == "B-NEUNIT"]
    unit_tags = [original_words[x] for x in unit_indexes]

    unit_in_indexes = [i for i, x in enumerate(nechem_tags) if x == "I-NEUNIT"]
    unit_in_tags = [original_words[x] for x in unit_in_indexes]

    # chems arrays
    chem_start_indexes = [i for i, x in enumerate(nechem_tags) if x == "B-NECHEM"]
    chem_start_tags = [original_words[x] for x in chem_start_indexes]

    chem_in_indexes = [i for i, x in enumerate(nechem_tags) if x == "I-NECHEM"]
    chem_in_tags = [original_words[x] for x in chem_in_indexes]

    chem_des_indexes = [i for i, x in enumerate(nechem_tags) if x == "B-NEDCHEM"]
    chem_des_tags = [original_words[x] for x in chem_des_indexes]

    chem_des_in_indexes = [i for i, x in enumerate(nechem_tags) if x == "I-NEDCHEM"]
    chem_des_in_tags = [original_words[x] for x in chem_des_in_indexes]

    # final arrays
    nums = []
    units = []
    chems = []

    # get num final array
    for i in range(len(num_indexes)):
        num_tags[i] = normalize_num(num_tags[i])
        if num_tags[i]:
            nums.append(CompositionNum(float(num_tags[i]), False, num_indexes[i]))

    # get units final array from minimizing the B and I tags
    for i in range(len(unit_indexes)):
        units.append(CompositionUnit(unit_tags[i], False, unit_indexes[i]))

    for i in range(len(unit_in_indexes)):
        for unit_obj in units:
            if 2 >= unit_in_indexes[i] - unit_obj.index > 0:
                unit_obj.unit = unit_obj.unit + " " + unit_in_tags[i]
                break

    # get chem final array from minimizing the B and I tags
    for i in range(len(chem_start_indexes)):
        chems.append(CompositionName(chem_start_tags[i], chem_start_indexes[i]))

    for i in range(len(chem_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(chems)):
            chem_obj = chems[j]
            if min_dest >= chem_in_indexes[i] - chem_obj.index > 0:
                index = j

        if index != -1:
            chems[index].chem = chems[index].chem + " " + chem_in_tags[i]

    # join b-dchem and i-dchem

    for i in range(len(chem_des_in_indexes)):
        min_dest = 100
        index = -1
        for j in range(len(chem_des_indexes)):

            if min_dest >= chem_des_in_indexes[i] - chem_des_indexes[j] > 0:
                index = j

        if index != -1:
            chem_des_tags[index] = chem_des_tags[index] + " " + chem_des_in_tags[i]

    for i in range(len(chem_des_indexes)):
        min_dest = 5
        index = -1
        for j in range(len(chems)):
            chem_obj = chems[j]
            if min_dest >= chem_des_indexes[i] - chem_obj.index > 0:
                index = j

        if index != -1:
            chems[index].description = chem_des_tags[i]

    # get for final array from minimizing the B and I tags

    compositions = get_composition_parts(nums, units, chems)
    print("Non Effective Substances:\n")
    # print(compositions)
    for comp in compositions:
        print(comp)
        comp_id = insert_composition(comp.chem.chem)
        composition_id = insert_comosition_non_effective(comp_id, comp.num and comp.num.num or "", comp.unit and comp.unit.unit or "", drug_id)

    # delete the extra compositions from equ


def read_deep_res(file_name):
    global chem_tags, nechem_tags, all_tags, original_words, ORIGINAL_DATA_DIRECTORY, ALL_COMP_DIRECTORY, CHEM_DIRECTORY, NECHEM_DIRECTORY

    first_in = ORIGINAL_DATA_DIRECTORY
    first_in = first_in + os.path.sep + file_name
    # print(ORIGINAL_DATA_DIRECTORY)
    first_in = pkg_resources.resource_filename(__name__, first_in)

    file = open(first_in, 'r', encoding='utf-8')
    original_data = modify(file.read())
    original_words = get_list(original_data)

    sec_in = ALL_COMP_DIRECTORY
    sec_in = sec_in + os.path.sep + file_name
    sec_in = pkg_resources.resource_filename(__name__, sec_in)

    file = open(sec_in, 'r', encoding='utf-8')
    all_without_data = file.read()
    all_tags = get_list(all_without_data)

    third_in = CHEM_DIRECTORY
    third_in = third_in + os.path.sep + file_name
    third_in = pkg_resources.resource_filename(__name__, third_in)

    file = open(third_in, 'r', encoding='utf-8')
    chem_data = file.read()
    chem_tags = get_list(chem_data)

    fourth_in = NECHEM_DIRECTORY
    fourth_in = fourth_in + os.path.sep + file_name
    fourth_in = pkg_resources.resource_filename(__name__, fourth_in)

    file = open(fourth_in, 'r', encoding='utf-8')
    nechem_data = file.read()
    nechem_tags = get_list(nechem_data)

    drug_name = get_drug()
    drug_id , drug_name = insert_drug_database(drug_name)
    get_compositions(drug_id)

    get_non_chems(drug_id)
    return drug_id,drug_name














