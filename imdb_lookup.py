import json

import pandas as pd
import joblib

from utils import build_episode_map

with open('./simpsons-ratings.json') as inp:
    dataset = json.load(inp)
    dataset = {i['key']: float(i['value']) for i in dataset}

    df = pd.DataFrame.from_dict(dataset, orient='index')
    df['season'] = df.index.map(lambda x: int(x[1:].split('e')[0]))
    df['episode'] = df.index.map(lambda x: int(x[1:].split('e')[1]))

    grouper = df.groupby('season')
    season_length = {int(k): len(g) for k, g in grouper}

    cum_length = {k: sum([season_length[i] for i in range(1, k+1)]) for k in season_length.keys()}
    cum_length[0] = 0

    df['episode_num'] = (df['season'] - 1).map(cum_length) + df['episode']

try:
    episode_names = joblib.load('simpsons_episode_lookup.pkl')
except FileNotFoundError:
    episode_names = build_episode_map()

df['episode_name'] = df['episode_num'].map(episode_names)
print(df[pd.isnull(df['episode_name'])])
df.to_csv('episode_ratings.csv')
