import os
import re as regexp

import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


INPUT_DIR = 'task_one/output/'
OUTPUT_DIR = 'task_two/output/'
LANGUAGE = 'english'
READ_MODE = 'r'
WRITE_MODE = 'w'
HTML_EXT = '.html'
LEMMAS_EXT = '_lemmas.txt'
TOKENS_EXT = '_tokens.txt'
ENCODING = 'ISO-8859-1'


def clean_text(file_data):
    pattern = r'<[ ]*script.*?\/[ ]*script[ ]*>'
    file_data = regexp.sub(pattern, ' ', file_data,
                           flags=(regexp.IGNORECASE | regexp.MULTILINE | regexp.DOTALL))
    pattern = r'<[ ]*style.*?\/[ ]*style[ ]*>'
    file_data = regexp.sub(pattern, ' ', file_data,
                           flags=(regexp.IGNORECASE | regexp.MULTILINE | regexp.DOTALL))
    pattern = r'<[ ]*meta.*?>'
    file_data = regexp.sub(pattern, ' ', file_data,
                           flags=(regexp.IGNORECASE | regexp.MULTILINE | regexp.DOTALL))
    pattern = regexp.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    output = regexp.sub(pattern, ' ', file_data)
    return output


def get_words_from_sentence(sentence):
    sentence = sentence.lower()
    sentence = regexp.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)|^rt|http.+?",
                          ' ',
                          sentence)
    sentence = regexp.sub(r"\d+", ' ', sentence)
    sentence = '  '.join([w for w in sentence.split() if w not in stopwords.words(LANGUAGE)])
    result = sentence.split()
    return result


def tokenize_and_lemmatize(text):
    tokens = []
    lemmas = {}
    if text.find('\n') != -1:
        lines = text.split('\n')
        for line in lines:
            # skip if empty
            if not line:
                continue
            sentences = sent_tokenize(line, language=LANGUAGE)
            for sentence in sentences:
                words = get_words_from_sentence(sentence)
                for word in words:
                    lemma = WordNetLemmatizer().lemmatize(word)
                    if word not in tokens:
                        tokens.append(word)
                    if lemma not in lemmas:
                        lemmas[lemma] = set()
                    lemmas[lemma].add(word)
    return tokens, lemmas


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_files = os.listdir('../{}'.format(INPUT_DIR))
    input_files.remove('links.txt')
    for file in input_files:
        print('CLEANING {}'.format(file))
        with open('../{}{}'.format(INPUT_DIR, file), READ_MODE, encoding=ENCODING) as input_file:
            cleaned_text = clean_text(input_file.read())
            tokens, lemmas = tokenize_and_lemmatize(cleaned_text)
            with open('../{}{}{}'.format(OUTPUT_DIR,file.replace(HTML_EXT, ''),TOKENS_EXT), WRITE_MODE) as output_file:
                for token in tokens:
                    output_file.write('{}\n'.format(token))
            with open('../{}{}{}'.format(OUTPUT_DIR, file.replace(HTML_EXT, ''),LEMMAS_EXT), WRITE_MODE) as output_file:
                for key, values in lemmas.items():
                    lemma = key + ' '
                    for value in values:
                        lemma += value + ' '
                    output_file.write('{}\n'.format(lemma))
