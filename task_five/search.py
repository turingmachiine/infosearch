import nltk
import math
import os

nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

LANGUAGE = 'english'
STOP_WORDS = stopwords.words(LANGUAGE)
INPUT_LINE = 'patrick mahomes'
CWD = '/'.join([path for path in os.getcwd().split('/') if os.getcwd().split('/').index(path)
                <= os.getcwd().split('/').index('infosearch')])


def compare_vectors(sample, search):
    sum = 0
    suma = 0
    sumb = 0
    for token in sample.keys():
        sum = sum + sample[token] * search[token]
        suma = suma + sample[token] * sample[token]
        sumb = sumb + search[token] * search[token]
    if sum == 0 or suma == 0 or sumb == 0:
        return 0
    return sum / (math.sqrt(suma) * math.sqrt(sumb))


def get_vector_from_file(name):
    vector_dict = {}
    file = open('{}/task_four/output/{}'.format(CWD, name))
    vecotor_strings = file.read().split("\n")
    file.close()
    for vecotor_string in vecotor_strings:
        if vecotor_string != "":
            vector_dict[vecotor_string.split(" ")[0]] = float(vecotor_string.split(" ")[2])
    return vector_dict


def get_all_tokens():
    tokens = set()

    for filename in filter(lambda x: '_tokens.txt' in x, os.listdir('{}/task_two/output'.format(CWD))):
        with open('{}/task_two/output/{}'.format(CWD, filename), 'r') as file:
            for line in file:
                tokens.add(line[:-1])
    return tokens


def make_vector(sentence):
    tokens = set()
    dictionary = {}
    vector = {}
    all_tokens = get_all_tokens()
    for token in all_tokens:
        dictionary[WordNetLemmatizer().lemmatize(token)] = 0
    words = list(filter(lambda x: x not in STOP_WORDS and x in all_tokens, sentence.split()))
    for word in words:
        current_lemma = WordNetLemmatizer().lemmatize(word)
        dictionary[current_lemma] = dictionary[current_lemma] + 1
        tokens.add(current_lemma)

    # make vector
    for token in all_tokens:
        vector[WordNetLemmatizer().lemmatize(token)] = 0
    for token in tokens:
        vector[token] = dictionary[token] / float(len(words))
    return vector


def search(request):
    search_vector = make_vector(request)
    print(CWD)
    result_dict = {}
    vectors_files = filter(lambda x: '_lemma.txt' in x, os.listdir('{}/task_four/output/'.format(CWD)))
    for name in vectors_files:
        result_dict[name.replace('_lemma.txt', '.html')] = compare_vectors(get_vector_from_file(name), search_vector)
    return dict(sorted(result_dict.items(), key=lambda x: x[1], reverse=True))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result = search("kansas mahomes smith henne")
    print(result)
