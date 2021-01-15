# -*- coding: utf-8 -*-

import re


def modify(text):
    units = ['ملغم', 'وحدة', 'غم', 'مليليتر', 'مايكرو', 'مم','ملغ']
    # punc
    # text = re.sub('(?<=\d)\.(?=\d)', '#', text)

    text = re.sub('\(', ' ( ', text)
    text = re.sub('\)', ' ) ', text)
    text = re.sub('؟', ' ؟ ', text)
    text = re.sub('!', ' ! ', text)
    text = re.sub('%', ' % ', text)
    text = re.sub('٪', ' % ', text)
    text = re.sub('٪', ' % ', text)
    text = re.sub(':', ' : ', text)
    text = re.sub('/', ' / ', text)
    text = re.sub('ـ', ' ـ ', text)
    text = re.sub('-', ' - ', text)
    text = re.sub('_', ' _ ', text)
    text = re.sub('؛', ' ؛ ', text)
    text = re.sub(';', ' ; ', text)
    # numbers
    text = re.sub('٠', '0', text)
    text = re.sub('۰', '0', text)
    text = re.sub('١', '1', text)
    text = re.sub('۱', '1', text)
    text = re.sub('٢', '2', text)
    text = re.sub('٣', '3', text)
    text = re.sub('۳', '3', text)
    text = re.sub('٤', '4', text)
    text = re.sub('٥', '5', text)
    text = re.sub('٦', '6', text)
    text = re.sub('٧', '7', text)
    text = re.sub('٨', '8', text)
    text = re.sub('٩', '9', text)
    text = re.sub('۲', '2', text)
    text = re.sub('۹', '9', text)
    text = re.sub('۸', '8', text)
    text = re.sub('۵', '5', text)
    text = re.sub('۲', '2', text)

    # for the 0,4
    text = re.sub('(?<=\d),(?=\d)', '#', text)
    text = re.sub('(?<=\d)‚(?=\d)', '#', text)
    text = re.sub('(?<=\d)٫(?=\d)', '#', text)
    text = re.sub('(?<=\d),(?=\d)', '#', text)
    text = re.sub('(?<=\d)‚(?=\d)', '#', text)
    text = re.sub('(?<=\d)٬(?=\d)', '#', text)
    text = re.sub('(?<=\d)٫(?=\d)', '#', text)
    text = re.sub('(?<=\d)٫(?=\d)', '#', text)
    text = re.sub('(?<=\d)٫(?=\d)', '#', text)
    text = re.sub('(?<=\d)\.(?=\d)', '#', text)
    text = re.sub('(?<=\d)\.(?=\d)', '#', text)

    text = re.sub('\.', ' . ', text)
    text = re.sub('،', ' . ', text)

    text = re.sub('#', '.', text)

    # space before and after numbers
    text = re.sub(r"([0-9]+(\.[0-9]+)?)", r" \1 ", text).strip()


    # units
    for unit in units: 
        text = re.sub('(?<=\d)' + unit, ' ' + unit, text)

    text = re.sub('\n', ' ', text)
    words = text.split(' ')
    text = ' '.join(words)
    
    return text
    


