import re
import unicodedata

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


def text2int(textnum, numwords={}):
    textnum = textnum.lower()
    textnum = re.sub("halves", "half", textnum)
    textnum = re.sub("a half", "half", textnum)
    textnum = re.sub("thirds", "third", textnum)
    textnum = re.sub("a third", "third", textnum)
    textnum = re.sub("quarters", "quarter", textnum)
    textnum = re.sub("a quarter", "quarter", textnum)

    units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
    ]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    scales2 = ["hundreds", "thousands", "millions", "billions", "trillions"]

    fractions = ["half", "third", "quarter"]

    if not numwords:

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)
        for idx, word in enumerate(scales2):
            numwords[word] = (10 ** (idx * 3 or 2), 0)
        for idx, word in enumerate(fractions):
            numwords[word] = (1 / (idx + 2), 0)

    ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12,
                     "half": 0.5, "third": 0.3333, "quarter": 0.25
                     }
    ordinal_endings = [('ieth', 'y'), ('th', '')]

    textnum = textnum.replace('-', ' ')

    # current = result = 0
    curstring = ""
    # onnumber = False
    texts = textnum.split("and")
    num_all = 0
    for text in texts:
        text = text.strip()
        current = result = 0
        onnumber = False
        for word in text.split():
            # print(word)
            try:
                inc = float(word)
                current += inc
                onnumber = True
                continue
            except:
                pass

            try:
                frac = unicodedata.numeric(word)
                current += frac
                onnumber = True
                continue
            except:
                pass
            if word == "and":
                onnumber = False
                continue

            if word in fractions and onnumber:
                scale, increment = numwords[word]
                current = current * scale + increment
                onnumber = True
                continue

            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if word not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word]
                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True
        # print("current is ", current, " text is ", text, " result", result)
        if onnumber:
            curstring += repr(result + current) + " "
        num_all += current
        # current = 0

    # print(current, num_all)
    new_str = ""
    prev_boolean = False
    prev = ""
    for cur in curstring.split():

        if is_float(cur) and prev_boolean:
            prev_boolean = True
            # new_str += (float(prev) + float(cur)) +" "
            prev = (float(prev) + float(cur))
        else:
            if is_float(cur):
                prev_boolean = True
                prev = cur

            else:
                if prev_boolean:
                    new_str += str(prev) + " "

                prev_boolean = False
                prev = ""
                new_str += cur + " "
            prev = cur

    if prev_boolean:
        new_str += str(prev)

    # print(new_str)


    return new_str

#
# print(text2int("a half and two"))
# print(text2int("half"))
# print(text2int("two and a half"))
# print(text2int("two halves"))
# print(text2int("one and four halves yyyyyyyyyyyyy"))

