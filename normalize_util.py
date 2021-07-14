import jieba
from typing import List
import re


def test_is_num(val: str) -> bool:
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def check_is_unit(val: str) -> bool:
    val = val.upper()
    if "ML" in val or "L" in val or "KG" in val or "G" in val:
        return True
    else:
        return False


def get_middle_eng_index(val: str) -> int:
    regex = re.compile("[A-Z]{1,2}")
    mo = regex.search(val)
    try:
        end_index = mo.end()
    except Exception:
        len(val)
    if end_index < len(val)-1:
        return end_index
    else:
        return len(val)


def unit_normalize(val: str) -> float:
    regex = re.compile("[A-Z]{1,2}")
    mo = regex.search(val)
    try:
        start = mo.start()
    except Exception:
        return 0.0
    else:
        num_str = val[0:start]
        unit = mo.group()
    try:
        num_float = float(num_str)
    except:
        return 0.0
    else:
        if unit == 'KG':
            num_float = num_float * 1000000
        if unit == 'L':
            num_float = num_float * 1000
        if unit == 'MG':
            num_float = num_float/1000
        return num_float


def need_swap(a: str, b: str) -> tuple:
    a_val = unit_normalize(a)
    b_val = unit_normalize(b)
    if a_val > b_val:
        return b, a
    return a, b


def gen_new_list(cut_list_result: List) -> List:
    new_list = []
    i = 0
    while i < len(cut_list_result):
        if test_is_num(cut_list_result[i]) and check_is_unit(cut_list_result[i + 1]):
            new_list.append(cut_list_result[i] + cut_list_result[i + 1])
            i += 2
        else:
            if check_is_unit(cut_list_result[i]) and "*" not in cut_list_result[i] and "X" not in cut_list_result[i]:
                index = get_middle_eng_index(cut_list_result[i])
                new_list.append(cut_list_result[i][:index])
                i += 1
            else:
                i += 1
    return new_list


def pre_process(line_string: str) -> str:
    line_string = line_string.strip()
    if len(line_string) <= 1:
        return ''
    line_string = line_string.replace(' ', '').replace('...', '').replace('(', '').replace('（', '').replace('）', '').replace(')', '')
    line_string = line_string.upper()
    line_string = line_string.replace('千克', 'KG').replace('毫克', 'MG').replace('毫升', 'ML').replace('克', 'G').replace('升', 'L')
    line_string = line_string.replace('每百G', '100G').replace('百G', '100G').replace('100毫升', '100G').replace('100ML','100ML')
    return line_string


if __name__ == '__main__':
    jieba.add_word('100G')
    jieba.add_word('100ML')

    with open('input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line_before = line
            line = pre_process(line)
            cut_list = jieba.lcut(line)
            new_cut_list = gen_new_list(cut_list)
            # print(line_before)
            if len(new_cut_list) == 0:
                print("其他")
            elif len(new_cut_list) == 1:
                print(new_cut_list[0])
            elif len(new_cut_list) == 2:
                val_one, val_two = need_swap(new_cut_list[0], new_cut_list[1])
                print(val_one + '/' + val_two)
            else:
                print(new_cut_list)

