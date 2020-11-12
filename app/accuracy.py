#!/usr/bin/env python

'''
ダジャレ判定AIの精度評価
'''

import json
import glob
import tqdm
import random
import engine

enable_judge = True
enable_eval = True

# データセットを作成
data = []
for file in glob.glob('data/*.json'):
    with open(file) as f:
        data.extend(json.load(f))
if len(data) == 0:
    exit(0)

random.shuffle(data)
data = data[:300]

if enable_judge:
    print('判定AIの評価...')
    n_correct = 0
    for row in tqdm.tqdm(data):
        try:
            if row['is_joke'] == \
                    engine.judge_engine.execute(row['joke'], False):
                n_correct += 1
            else:
                pass
        except Exception as e:
            print(row['joke'])
            print(e)

    print('精度：%f' % (n_correct / len(data)))

if enable_eval:
    print('評価AIの評価...')
    score_map = [0, 0, 0, 0, 0]

    a = []
    for row in tqdm.tqdm(data):
        score = engine.eval_engine.execute(row['joke'], False)
        a.append(score)
        score = int(round(score))
        score_map[score - 1] += 1

print(score_map)
