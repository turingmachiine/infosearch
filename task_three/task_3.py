import glob
import os

INPUT_DIR = "task_two\\output\\*_tokens.txt"

token_values = glob.glob(INPUT_DIR)


def get_tokens(token_values):
    token_unique = set()
    token_map = {}
    for file in token_values:
        with open(file, 'r') as fs:
            value = fs.read()
            split_value = value.splitlines()
            name = file.replace("_tokens.txt", "").replace("task_two\\output\\", "")
            token_unique.update(split_value)
            token_map[name] = split_value
    return token_unique, token_map


def get_result_map(token_unique, token_map):
    result_map = {}
    for token in token_unique:
        result_map[token] = []
        for key, value in token_map.items():
            if token in value:
                result_map[token].append(key)
    return result_map


token_unique, token_map = get_tokens(token_values)
result_map = get_result_map(token_unique, token_map)


with open('task_three\\output\\inverted_index.txt', 'w') as fs:
    for key, values in result_map.items():
        result = key + " "
        for value in values:
            result += value + " "
        fs.write("%s\n" % result)


with open('task_three\\output\\inverted_index_2.txt', 'w') as fs:
    for key, values in result_map.items():
        result = {"count": len(values), "inverted_array": values, "word": key}
        fs.write("%s\n" % str(result))