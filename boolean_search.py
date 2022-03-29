import json
import re

requests = ['denver & broncos']



def make_corpus(filename):
    token_corpuses = {}
    with open(filename, 'r') as fs:
        data = fs.readlines()
        for elem in data:
            elem = elem.replace("\'", "\"")
            string_data = json.loads(elem)
            print(string_data)
            token_corpuses[string_data['word']] = string_data['inverted_array']
    return token_corpuses


def make_index(filename):
    index_url = {}
    with open(filename, 'r') as fs:
        data = fs.readlines()
        for elem in data:
            res = re.split('\)', elem)
            index_url[res[0]] = res[1].replace("\n", "")
    return index_url


token_corpuses = make_corpus('task_three\\output\\inverted_index_2.txt')
index_url = make_index('task_one\\output\\links.txt')

for i in requests:
    res = set()
    links = []
    r = re.split('&', i)
    for r in r:
        r = r.strip()
        if len(res) == 0:
            res.update(token_corpuses[r])
        else:
            res = res.intersection(token_corpuses[r])
    for r in res:
        links.append(index_url[r])
    print("\n")
    print("Request: " + i)
    print("Result: " + str(links))
    print("Result size: " + str(len(links)))