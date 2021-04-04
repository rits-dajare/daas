#!/usr/bin/env python
import json
import glob
import tqdm
import random
import argparse

from core import config
from core import message
from webapi import create_app


def start_mode():
    app = create_app()
    app.run(debug=config.API_DEBUG, host=config.API_HOST, port=config.API_PORT)


def accuracy_mode():
    # load dajare samples
    data: list = []
    files: list = glob.glob(config.DATA_FILE_PATH)
    for file_name in tqdm.tqdm(files):
        print(message.LOAD_FILE_MSG(file_name))
        with open(file_name, 'r') as f:
            data.extend(json.load(f))

    # specify the number of samples to use
    input_str = input(message.N_SAMPLES_INPUT_GUIDE(len(data))) or str(len(data))
    n_samples: int = int(input_str)
    data = random.sample(data, n_samples)

    # set api
    app = create_app().test_client()

    # measure accuracy
    n_correct: int = 0
    print(message.MEASURE_ACCURACY_MSG(n_samples))
    for sample in tqdm.tqdm(data):
        res = app.get('judge/', query_string={'dajare': sample['dajare']})
        if res.json['is_dajare'] == sample['is_dajare']:
            n_correct += 1
    print(message.ACCURACY_MSG(n_correct / n_samples))


if __name__ == '__main__':
    # options
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start',
                        help='start app',
                        action='store_true')
    parser.add_argument('-a', '--accuracy',
                        help='measure accuracy',
                        action='store_true')
    args = parser.parse_args()

    if args.start:
        start_mode()
    if args.accuracy:
        accuracy_mode()
