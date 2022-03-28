import glob
import math
import collections
import json
import os
from pathlib import Path

path = Path(os.getcwd())
os.chdir(path.parent.absolute())

tokens_files_list = glob.glob("task_two\\output\\*_tokens.txt")
lemmas_files_list = glob.glob("task_two\\output\\*_lemmas.txt")


def calculate_idf_value(current_word):
    return math.log10(len(tokens_map) / tokens_data_count[current_word])


def calculate_tf_value(current_text):
    tf_texts = collections.Counter(current_text)
    for txt in tf_texts:
        tf_texts[txt] = tf_texts[txt] / float(len(current_text))
    return tf_texts


def get_tokens_count(file):
    tokens_data_count = {}
    with open(file, 'r') as f:
        data = f.readlines()
        for item in data:
            item = item.replace("\'", "\"")
            str_data = json.loads(item)
            tokens_data_count[str_data['word']] = str_data['count']
    return tokens_data_count


def get_tokens_map(tokens_files_list):
    tokens_map = {}
    for file in tokens_files_list:
        with open(file, 'r') as fs:
            data = fs.read()
            data_list = data.splitlines()
            name = file.replace("_tokens.txt", "").replace("task_two\\output\\", "")
            tokens_map[name] = data_list
    return tokens_map


def get_tf_idf_term(tokens_map):
    for key, value in tokens_map.items():
        tf_idf_map = {}
        calculated_tf = calculate_tf_value(value)
        for word in calculated_tf:
            idf = calculate_idf_value(word)
            tf_idf_map[word] = [idf, calculated_tf[word] * idf]
        with open('task_four\\output\\' + key + '_term.txt', 'w') as f:
            for key1, value1 in tf_idf_map.items():
                result = key1 + " " + str(value1[0]) + " " + str(value1[1])
                f.write("%s\n" % result)
    return tf_idf_map


def get_lemmas(lemmas_file_list):
    lemmas_map = {}
    for file in lemmas_files_list:
        with open(file, 'r') as fs:
            data = fs.read()
            data_list = data.splitlines()
            name = file.replace("_lemmas.txt", "").replace("task_two\\output\\", "")
            lemmas_map[name] = data_list
    return lemmas_map


def get_tf_idf_lemmas(tokens_map, lemmas_map):
    for key, value in tokens_map.items():
        tf_idf_map = {}
        calculated_tf = calculate_tf_value(value)
        current_lemmas = lemmas_map[key]
        for lemma in current_lemmas:
            values = lemma.split(' ')
            tf_lemma_sum = float(0)
            idf_sum = float(0)
            for i in range(1, len(values) - 1):
                tf_lemma_sum += calculated_tf[values[i]]
                idf_sum += calculate_idf_value(values[i])
            tf_idf_map[values[0].replace(":", "")] = [idf_sum, tf_lemma_sum * idf_sum]
        with open('task_four\\output\\' + key + '_lemma.txt', 'w') as f:
            for key1, value1 in tf_idf_map.items():
                result = key1 + " " + str(value1[0]) + " " + str(value1[1])
                f.write("%s\n" % result)
    return tf_idf_map


tokens_data_count = get_tokens_count("task_three\\output\\inverted_index_2.txt")
tokens_map = get_tokens_map(tokens_files_list)
tf_idf_term = get_tf_idf_term(tokens_map)
lemmas_map = get_lemmas(lemmas_files_list)
tf_idf_lemm = get_tf_idf_lemmas(tokens_map, lemmas_map)







