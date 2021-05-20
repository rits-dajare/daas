from flask import Blueprint, request, jsonify
import typing

from core import engine
from core.api.request import judge_request
from core.api.response import judge_response

bp: Blueprint = Blueprint('judge', __name__)


@bp.route('/', methods=['GET'])
def judge_dajare() -> typing.Tuple[str, int]:
    status_code: int
    result = judge_response.JudgeResponse()

    # query params
    params = judge_request.JudgeRequest(request.args)

    # judge dajare
    try:
        result.is_dajare = engine.judge_engine.exec(params.dajare)
        result.applied_rule = engine.judge_engine.applied_rule

        status_code = 200
        result.status = "OK"
        result.message = "success"

    except Exception as e:
        status_code = 500
        result.status = "NG"
        result.message = str(e)

    return jsonify(result.__dict__), status_code
