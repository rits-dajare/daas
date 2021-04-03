import os
import copy
import requests
from flask import Blueprint, request, jsonify, current_app

from core import config
from core import message
from core import nnet
from core import preprocessing

bp: Blueprint = Blueprint('infer', __name__)

nnet_: nnet.NNet = nnet.NNet(True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('number', methods=['POST'])
def predict_number():
    result: dict = copy.copy(config.API_RESPONSE)
    status: int = 200

    wav_file_key: str = 'wavfile'
    # received wav file
    if wav_file_key in request.files:
        file = request.files[wav_file_key]
        file.save(config.UPLOAD_WAV_PATH)
        print(message.CREATED_FILE_MSG(config.UPLOAD_WAV_PATH))

    # not received wav file
    else:
        result['status'] = config.API_ERROR_STATUS
        result['message'] = 'wav file not sent'
        status = 400
        return jsonify(result), status

    # predict
    mfcc = preprocessing.extract_feature(config.UPLOAD_WAV_PATH)
    mfcc = preprocessing.resample(mfcc)
    mfcc = preprocessing.normalize(mfcc)
    pred_class_str: str = config.CLASSES[nnet_.predict(mfcc)]
    print(message.PREDICT_CLASS_MSG(pred_class_str))
    result['text'] = pred_class_str

    return jsonify(result), status


@bp.route('text', methods=['POST'])
def predict_text():
    result: dict = copy.copy(config.API_RESPONSE)
    status: int = 200

    wav_file_key: str = 'wavfile'
    # received wav file
    if wav_file_key in request.files:
        file = request.files[wav_file_key]
        file.save(config.UPLOAD_WAV_PATH)
        print(message.CREATED_FILE_MSG(config.UPLOAD_WAV_PATH))

    # not received wav file
    else:
        result['status'] = config.API_ERROR_STATUS
        result['message'] = 'wav file not sent'
        status = 400
        return jsonify(result), status

    # predict
    try:
        APIKEY: str = os.environ['DOCOMO_TOKEN']
        url: str = config.DOCOMO_URL + APIKEY
        res = requests.post(
            url,
            files={'a': open(config.UPLOAD_WAV_PATH, 'rb')}
        )
        pred_text: str = res.json()['text']
        result['text'] = pred_text
        print(message.PREDICT_CLASS_MSG(pred_text))

    except Exception as e:
        result['status'] = config.API_ERROR_STATUS
        result['message'] = str(e)
        status = 500

    return jsonify(result), status
