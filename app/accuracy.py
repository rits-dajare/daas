#!/usr/bin/env python

'''
ダジャレ判定AIの精度評価
'''

import sys
import json
import glob
import tqdm
import numpy as np
import engine
import argparse


def prepare_data(num=None, shuffle=True):
    result = []

    for file in glob.glob('data/*.json'):
        with open(file, 'r') as f:
            result.extend(json.load(f))

    if shuffle:
        np.random.shuffle(result)
    if num is not None:
        result = result[:num]

    return result


def measure_judge_engine(data):
    n_correct = 0
    for row in tqdm.tqdm(data):
        try:
            if row['is_joke'] == \
                    engine.judge_engine.execute(row['joke'], False):
                n_correct += 1
        except Exception as e:
            print('エラー発生：', row['joke'])
            print(e)
            sys.exit(1)

    return '判定精度：%f' % (n_correct / len(data))


def measure_eval_engine(data):
    score_map = [0, 0, 0, 0, 0]

    for row in tqdm.tqdm(data):
        score = engine.eval_engine.execute(row['joke'], False)
        score = int(round(score))
        score_map[score - 1] += 1

    result = ''
    for i, n in enumerate(score_map):
        result += ' - 星%d：%3.1f%%\n' % (i + 1, n / len(data) * 100)

    return result


if __name__ == '__main__':
    # opts conf
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--judge', help='measure the judge accuracy',
                        action='store_true')
    parser.add_argument('-e', '--eval', help='measure the eval accuracy',
                        action='store_true')
    parser.add_argument('-n', '--num', help='number to measure',
                        type=int)
    args = parser.parse_args()

    # 検証用データを用意
    data = prepare_data(args.num)

    if args.judge:
        print('判定AIの評価...')
        print(measure_judge_engine(data))
    if args.eval:
        print('評価AIの評価...')
        print(measure_eval_engine(data))
