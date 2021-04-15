#!/usr/bin/env python
import json
import glob
import tqdm
import random
import argparse

from core import config
from core import message
from core import webapi


def start_mode():
    app = webapi.create_app()
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
    default_samples: int = len(data)
    input_str = input(message.N_SAMPLES_INPUT_GUIDE(default_samples, len(data))) or default_samples
    n_samples: int = int(input_str)
    data = random.sample(data, n_samples)

    # set api
    app = webapi.create_app().test_client()

    # measure accuracy
    error_samples: list = []
    print(message.MEASURE_ACCURACY_MSG(n_samples))
    for sample in tqdm.tqdm(data):
        judge_res = app.get('judge/', query_string={'dajare': sample['dajare']}).json
        reading_res = app.get('reading/', query_string={'dajare': sample['dajare']}).json
        if judge_res['is_dajare'] != sample['is_dajare']:
            error_samples.append({
                'dajare': sample['dajare'],
                'reading': reading_res['reading'],
                'is_dajare': sample['is_dajare'],
                'judge_result': judge_res['is_dajare'],
                'applied_rule': judge_res['applied_rule'],
            })
    print(message.ACCURACY_MSG((n_samples - len(error_samples)) / n_samples))

    # dump error samples
    with open(config.DATA_ERROR_FILE_PATH, 'w') as f:
        f.write(json.dumps(error_samples, ensure_ascii=False, indent=2))


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
