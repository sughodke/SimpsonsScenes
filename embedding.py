import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

from utils import build_occurrence_matrix, analogy_solver

###############################################################################
# Retrieve the data

adjacency_list = build_occurrence_matrix('Characters')
df = pd.DataFrame(adjacency_list).T.fillna(0)

names = df.index
print('loaded adjacency matrix {}'.format(df.shape))
print('')


###############################################################################
# Learn a latent structure from the correlations

X = df.as_matrix()

min_count = 5  # None
if min_count:
    mask = X > min_count
    X = X[[np.any(m) for m in mask]]
    names = names[[np.any(m) for m in mask]]

# X /= np.linalg.norm(X)


model = TruncatedSVD(n_components=40,  # 40
                     random_state=0)
embedding = model.fit_transform(X)
print(embedding.shape)
print(model.explained_variance_ratio_.sum())

characters = ['Ned Flanders', 'Homer Simpson', 'Marge Simpson', 'Bart Simpson', 'Milhouse', 'Lenny Leonard',
              'Charles Montgomery Burns', 'Skinner', 'Chalmers', 'Mr. Burns', 'Waylon Smithers']
indices = [names.str.contains(char).argmax() for char in characters]
char2vec = dict(zip(characters, [embedding[l] for l in indices]))

print('Homer appears with Mr Burns, as much as Skinner appears with X')

solns, scores = analogy_solver(
    char2vec['Charles Montgomery Burns'], char2vec['Homer Simpson'],
    char2vec['Skinner'],
    embedding, return_score=True)

for n, s in zip(names[solns], scores):
    print('{} matches with {} score'.format(n, s))

print('Milhouse : Smithers :: Bart : X')

solns, scores = analogy_solver(
    char2vec['Milhouse'], char2vec['Waylon Smithers'],
    char2vec['Bart Simpson'],
    embedding, return_score=True)

for n, s in zip(names[solns], scores):
    print('{} matches with {} score'.format(n, s))


print('Bart : Milhouse :: Lenny : Carl')

solns, scores = analogy_solver(
    char2vec['Bart Simpson'], char2vec['Milhouse'],
    char2vec['Lenny Leonard'],
    embedding, return_score=True)

for n, s in zip(names[solns], scores):
    print('{} matches with {} score'.format(n, s))


print('Maggie : Mr Burns :: Itchy : Scratchy')

solns, scores = analogy_solver(
    char2vec['Bart Simpson'], char2vec['Milhouse'],
    char2vec['Lenny Leonard'],
    embedding, return_score=True)

for n, s in zip(names[solns], scores):
    print('{} matches with {} score'.format(n, s))