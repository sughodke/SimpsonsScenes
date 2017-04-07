import json
from collections import defaultdict


co_occurrence = defaultdict(lambda: defaultdict(int))


def clean_str(c):
    return c.replace('[', '').replace(']', '').strip()


with open('./output.json', 'r') as output:
    dataset = json.load(output)
    for ep, occ in dataset.items():
        try:
            characters = occ['Locations']
        except KeyError:
            characters = []

        for char in characters:
            for cmp_char in characters:
                char = clean_str(char)
                cmp_char = clean_str(cmp_char)
                co_occurrence[char][cmp_char] += 1

nodes = sorted(co_occurrence,
               key=lambda k: len(co_occurrence[k]),
               reverse=True)

shrink_ratio = 0.10  # 0.05
nodes = nodes[:int(len(nodes) * shrink_ratio)]
links = []

for source in nodes:
    d = co_occurrence[source]
    source = nodes.index(source)

    for target, value in d.items():
        try:
            target = nodes.index(target)

            links.append({
                'source': source,
                'target': target,
                'value': value
            })
        except ValueError:
            continue

r = {
    'nodes': [{'name': name, "group": i % 5}
              for i, name in enumerate(nodes)],
    'links': links
}
with open('./miserables.json', 'w') as output:
    json.dump(r, output)
print("Saved dataset")
