import urllib.request as urllib_request
from urllib.parse import urljoin
from bs4 import *

OUTPUT_PATH = 'task_one/output/links.txt'
OUTPUT_DIR = 'task_one/output/'
WRITE_MODE = 'w'
PARSE_MODE = 'html.parser'
HREF = 'href'
HTTP = 'http'
WORDS = ['pff', 'football', 'team', 'player', 'quarterback', 'broncos', 'chiefs', 'wilson', 'mahomes']


def contains_words(string):
    return any(word in string for word in WORDS)


def crawl(pages):
    links = list()
    for page in pages:
        if page not in links:
            links.append(page)
            try:
                c = urllib_request.urlopen(page)
            except:
                continue
            beautiful_soup = BeautifulSoup(c.read(), features=PARSE_MODE)
            soup_links = beautiful_soup('a')
            for link in soup_links:
                if HREF in dict(link.attrs):
                    base_url = urljoin(page, link[HREF])
                    if base_url.find("'") != -1 or base_url.find('web.archive.org') != -1 or base_url.find('.pdf') != -1\
                            or base_url.find('.jpg') != -1 or base_url.find('.svg') != -1:
                        continue
                    base_url = base_url.split('#')[0]
                    if base_url[0:4] == HTTP:
                        links.append(base_url)
    return filter(contains_words, links)


def save(urls):
    with open(OUTPUT_PATH, WRITE_MODE) as output_file:
        file_number = 1
        for url in urls:
            name = '{}{}.html'.format(OUTPUT_DIR,str(file_number))
            try:
                urllib_request.urlretrieve(url, name)
                result_string = '{}) {}\n'.format(file_number, url.replace("\n", "") )
                print(result_string)
                output_file.write(result_string)
                output_file.flush()
                file_number += 1
                if file_number == 101:
                    output_file.close()
                    break
            except:
                continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("START CRAWLING")
    urls = set()
    urls.add('https://en.wikipedia.org/wiki/National_Football_League')
    # с запасом, на случай битых ссылок
    while len(urls) < 150:
        for i in list(urls):
            urls.update(crawl([i]))
            if len(urls) > 150:
                break
    print("FINISH, FOUND {} ITEMS. SAVING 100 OF THEM TO 'output' DIRECTORY".format(len(urls)))
    save(urls)
    print("DONE. SAVED TO links.txt")