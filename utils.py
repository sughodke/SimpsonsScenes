import json
from collections import defaultdict


def clean_str(c):
    return c.replace('[', '').replace(']', '').strip()


def build_occurence_matrix(key='Locations'):
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
