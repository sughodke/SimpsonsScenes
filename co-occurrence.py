import json
from collections import defaultdict


co_occurrence = defaultdict(lambda: defaultdict(int))
with open('./output.json', 'r') as output:
    dataset = json.load(output)
    for ep, occ in dataset.items():
        try:
            characters = occ['Characters']
        except KeyError:
            characters = []

        for char in characters:
            for cmp_char in characters:
                char = char.replace('[', '').replace(']', '')
                cmp_char = cmp_char.replace('[', '').replace(']', '')
                co_occurrence[char][cmp_char] += 1

nodes = tuple(co_occurrence.keys())
links = []
for source, d in co_occurrence.items():
    source = nodes.index(source)

    for target, value in d.items():
        target = nodes.index(target)

        links.append({
            'source': source,
            'target': target,
            'value': value
        })

r = {
    'nodes': [{'name': name, "group": i % 5}
              for i, name in enumerate(nodes)],
    'links': links
}
with open('./miserables.json', 'w') as output:
    json.dump(r, output)
print("Saved dataset")