import re
import json
import time

from bs4 import BeautifulSoup


with open('./simpsons_pages_current.xml') as html_doc:
    t0 = time.time()
    soup = BeautifulSoup(html_doc, 'lxml')
    print('Wiki XML file parsed in {:3f}s'.format(time.time() - t0))

    t0 = time.time()
    dataset = {}
    for tag in soup.find_all('title', string=re.compile('Appearances')):
        page = tag.parent
        title = page.title
        text = page.text

        text = text.split("==")
        appearances = dict(zip(text[1::2], text[2::2]))

        for k, v in appearances.items():
            appearances[k.strip()] = re.findall("\[\[.*\]\]", v)

        dataset[title.text] = appearances
    print('Transformed in {:3f}s'.format(time.time() - t0))


with open('./output.json', 'w') as output:
    json.dump(dataset, output)
print("Saved dataset")
