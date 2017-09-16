import json
import re
import time
from collections import defaultdict

from bs4 import BeautifulSoup
from joblib import dump
import numpy as np
from sklearn.metrics.pairwise import paired_distances


def clean_str(c):
    return c.replace('[', '').replace(']', '').strip()


def build_occurrence_matrix(key='Locations'):
    co_occurrence = defaultdict(lambda: defaultdict(int))

    with open('./output.json', 'r') as output:
        dataset = json.load(output)
        for ep, occ in dataset.items():
            try:
                characters = occ[key]
            except KeyError:
                characters = []

            for char in characters:
                for cmp_char in characters:
                    char = clean_str(char)
                    cmp_char = clean_str(cmp_char)
                    co_occurrence[char][cmp_char] += 1

    return co_occurrence


def build_episode_map():
    with open('./simpsons_pages_current.xml') as html_doc:
        t0 = time.time()
        soup = BeautifulSoup(html_doc, 'lxml')
        print('Wiki XML file parsed in {:3f}s'.format(time.time() - t0))

        episode_names = {}
        for pg in soup.find_all('page'):
            episode_name = pg.title.text

            episode_num = re.findall('Episode Number.*[0-9]*', pg.revision.text)
            try:
                episode_num = episode_num[0].split('=')[1]

                # work-around, for some meta-data which doesn't use newlines
                episode_num = episode_num.split('|')[0]

                episode_num = int(episode_num.strip().split(' ')[0])

                print(episode_num)
                episode_names[episode_num] = episode_name

            except (IndexError, ValueError) as e:
                # print('No episode number for {}'.format(episode_name))
                pass

        dump(episode_names, 'simpsons_episode_lookup.pkl')
        return episode_names


def analogy_solver(man, woman, king, W, top_n=5, return_score=False):
    """
    In the famous "man is to woman as king is to queen" example, queen
    is the word w that maximizes: cos(w, king) - cos(w, man) + cos(w, woman).
    """
    A = np.array([king] * len(W))
    B = np.array([man] * len(W))
    Y = np.array([woman] * len(W))

    score = paired_distances(W, A, 'cosine') - paired_distances(W, B, 'cosine') + paired_distances(W, Y, 'cosine')

    # score = score.flatten()
    sorted_score = score.argsort()  # [::-1]

    if not return_score:
        return sorted_score[:top_n]
    else:
        return sorted_score[:top_n], score[sorted_score][:top_n]
