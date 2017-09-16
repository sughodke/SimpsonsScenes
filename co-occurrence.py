import json

from utils import build_occurrence_matrix

co_occurrence = build_occurrence_matrix()

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
