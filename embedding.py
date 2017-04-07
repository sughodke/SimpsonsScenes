import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

from utils import build_occurence_matrix

###############################################################################
# Retrieve the data

adjacency_list = build_occurence_matrix('Characters')
df = pd.DataFrame(adjacency_list).T.fillna(0)

names = df.index
print('loaded adjacency matrix {}'.format(df.shape))
print('')


###############################################################################
# Learn a latent structure from the correlations

X = df.as_matrix()

mask = X > 2
X = X[[np.any(m) for m in mask]]
names = names[[np.any(m) for m in mask]]

X /= np.linalg.norm(X)


###############################################################################
# Cluster using KMeans++

labels = KMeans(n_clusters=64).fit_predict(X)
n_labels = labels.max()

for i in range(n_labels + 1):
    print('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))


###############################################################################
# Find a low-dimension embedding for visualization: find the best position of
# the nodes (the characters) on a 2D plane

model = TSNE(n_components=2, random_state=0)
embedding = model.fit_transform(X)


###############################################################################
# Visualization
plt.figure(1, facecolor='w', figsize=(10, 8))
plt.clf()
ax = plt.axes([0., 0., 1., 1.])
plt.axis('off')

# Plot the nodes using the coordinates of our embedding
for point, word, label in zip(embedding, names, labels):
    plt.annotate(
        word,
        xy=(point[0], point[1]),
        ha='center',
    )
    plt.scatter(point[0], point[1],
                c=label)

plt.show()
