#!/usr/bin/env python

'''
ダジャレ判定AIの訓練
'''

import json
import glob
import random
import engine

# 訓練データを作成
data = []
for file in glob.glob('data/*.json'):
    with open(file) as f:
        data.extend(json.load(f))

random.shuffle(data)
data = data[:500]
data = [[row['joke'], row['score']] for row in data]

engine.eval_engine.train(data)
