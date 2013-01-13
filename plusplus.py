#-*- coding:utf-8 -*-

import unicodedata

class PlusPlus(object): # For compatibility issue
    @classmethod
    def plusone(cls, raw_src):
        return plusone(raw_src)

hanja_normal = set([u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百'])
hanja_difficult = set([u'壹', u'貳', u'參', u'拾'])
roma_normal = set([u'i', u'v', 'x', 'l'])
roma_capital_normal = set([u'I', u'V', u'X', 'L'])
roma_special = set([u'ⅰ', u'ⅱ', u'ⅲ', u'ⅳ', u'ⅴ', u'ⅵ', u'ⅶ', u'ⅷ', u'ⅸ', u'ⅹ'])
roma_capital_special = set([u'Ⅰ', u'Ⅱ', u'Ⅲ', u'Ⅳ', u'Ⅴ', u'Ⅵ', u'Ⅶ', u'Ⅷ', u'Ⅸ', u'Ⅹ'])

def find_hanja(src):
    start, end, position = -1, -1, -1
    mode = 'hanja_normal'
    for char in src:
        position += 1
        if char in hanja_normal or char in hanja_difficult:
            if end == position:
                end = position + 1
            else:
                start, end = position, position + 1
    for char in src[start:end]:
        if char in hanja_difficult:
            mode = 'hanja_difficult'
    if start == -1:
        mode = None
    return start, end, mode

def find_roma(src):
    start, end, position = -1, -1, -1
    mode = 'roma_normal'
    for char in src:
        position += 1
        if ('a' <= char <= 'z' or 'A' <= char <= 'Z') \
                and char not in roma_normal \
                and char not in roma_capital_normal:
            start, end, mode = -1, -1, None
            break
        if char in roma_normal or char in roma_capital_normal:
            if char in roma_capital_normal:
                mode = 'roma_capital_normal'
            if end == position:
                end = position + 1
            else:
                start, end = position, position + 1

    position = -1
    for char in src:
        position += 1
        if char in roma_special and start < position:
            start, end, mode = position, position + 1, 'roma_special'
        if char in roma_capital_special and start < position:
            start, end, mode = position, position + 1, 'roma_capital_special'

    if start == -1:
        mode = None

    return start, end, mode

def find_arabia(src):
    start, end, position = -1, -1, -1
    mode = 'arabia'
    for char in src:
        position += 1
        if '0' <= char <= '9':
            if end == position:
                end = position + 1
            else:
                start, end = position, position + 1

    if start == -1:
        mode = None

    return start, end, mode

def find_value(src):
    result_hanja = find_hanja(src)
    result_roma = find_roma(src)
    result_arabia = find_arabia(src)
    result = (-1, -1, None)
    if result[0] < result_hanja[0] and result_hanja[2] != None:
        result = result_hanja
    if result[0] < result_roma[0] and result_roma[2] != None:
        result = result_roma
    if result[0] < result_arabia[0] and result_arabia[2] != None:
        result = result_arabia
    return result

def process_value(src, mode):
    result = src

    if mode == 'arabia':
        length = 0
        if src[0] == '0':
            length = len(src)
        result = str(int(src) + 1)
        if length > len(result):
            result = '0' * (length - len(result)) + result
    if mode == 'hanja_normal' or mode == 'hanja_difficult':
        if mode == 'hanja_normal':
            hanja_map = {  0: u'零'
                        ,  1: u'一'
                        ,  2: u'二'
                        ,  3: u'三'
                        ,  4: u'四'
                        ,  5: u'五'
                        ,  6: u'六'
                        ,  7: u'七'
                        ,  8: u'八'
                        ,  9: u'九'
                        , 10: u'十'
                        ,100: u'百'}
        elif mode == 'hanja_difficult':
            hanja_map = {  0: u'零'
                        ,  1: u'壹'
                        ,  2: u'貳'
                        ,  3: u'參'
                        ,  4: u'四'
                        ,  5: u'五'
                        ,  6: u'六'
                        ,  7: u'七'
                        ,  8: u'八'
                        ,  9: u'九'
                        , 10: u'拾'
                        ,100: u'百'}
        hanja_rev_map = dict()
        for hanja in hanja_map:
            hanja_rev_map[hanja_map[hanja]] = hanja

        mode = 'non_unit'
        for char in src:
            if hanja_rev_map[char] >= 10:
                mode = 'has_unit'
        if len(src) == 1:
            mode = 'has_unit'
        
        if mode == 'has_unit':
            value = 0
            cur_value = 0
            for char in src:
                tmp_value = hanja_rev_map[char]
                if tmp_value < 10:
                    cur_value = tmp_value
                else:
                    if cur_value == 1:
                        mode = 'has_unit_include_one'
                    if cur_value == 0:
                        cur_value = 1
                    value += cur_value * tmp_value
                    cur_value = 0
            value += tmp_value if tmp_value < 10 else 0
            value += 1
            result = u''

            for mod in [100, 10, 1]:
                cur_value = value / mod
                value %= mod
                if cur_value != 0:
                    if mod == 1:
                        result += hanja_map[cur_value]
                    elif mode == 'has_unit' and cur_value == 1:
                        result += hanja_map[mod]
                    else:
                        result += hanja_map[cur_value] + hanja_map[mod]
        else:
            value = 0
            for char in src:
                tmp_value = hanja_rev_map[char]
                value = value * 10 + tmp_value
            value += 1

            result = u''

            for mod in [100, 10, 1]:
                cur_value = value / mod
                value %= mod
                if result == u'' and cur_value == 0:
                    continue
                result += hanja_map[cur_value]
    if mode == 'roma_normal' or mode == 'roma_capital_normal':
        src = src.upper()
        value = [0, 0, 0]
        for char in src:
            if char == 'I': value[0] += 1
            if char == 'X':
                if value[0] > 0: value[0] = -value[0]
                value[1] += 1
            if char == 'V':
                if value[0] > 0: value[0] = -value[0]
                value[0] += 5
            if char == 'L':
                if value[1] > 0: value[1] = -value[1]
                value[1] += 5
        value = value[0] + value[1] * 10 + value[2] * 100 + 1

        if value >= 90: # Current version do not support more than or equal 90
            result = src
        else:
            result = u''
            while value:
                if value >= 50:
                    result += 'L'
                    value -= 50
                    continue
                if value >= 40:
                    result += 'XL'
                    value -= 40
                    continue
                if value >= 10:
                    result += 'X'
                    value -= 10
                    continue
                if value >= 9:
                    result += 'IX'
                    value -= 9
                    continue
                if value >= 5:
                    result += 'V'
                    value -= 5
                    continue
                if value >= 4:
                    result += 'IV'
                    value -= 4
                    continue
                if value >= 1:
                    result += 'I'
                    value -= 1
                    continue
        if mode == 'roma_normal':
            result = result.lower()

    if mode == 'roma_special' or mode == 'roma_capital_special':
        # 특수문자의 경우 1~10까지만 처리. 
        if mode == 'roma_special':
            roma = [u'ⅰ', u'ⅱ', u'ⅲ', u'ⅳ', u'ⅴ', u'ⅵ', u'ⅶ', u'ⅷ', u'ⅸ', u'ⅹ']
        else:
            roma = [u'Ⅰ', u'Ⅱ', u'Ⅲ', u'Ⅳ', u'Ⅴ', u'Ⅵ', u'Ⅶ', u'Ⅷ', u'Ⅸ', u'Ⅹ']

        for i in xrange(0, 8):
            if src == roma[i]:
                result = roma[i + 1]

    return result

def plusone(raw_src, encoding='utf-8'):
    if type(raw_src) is str:
        src = raw_src.decode(encoding)
    else:
        src = raw_src
        encoding = None
    src = unicodedata.normalize('NFC', src)

    result = find_value(src)
    if result[2] != None:
        processed_value = process_value(src[result[0]:result[1]], result[2])
        dest = src[:result[0]] + processed_value + src[result[1]:]
    else:
        dest = src

    if encoding is not None:
        dest = dest.encode(encoding)

    return dest
