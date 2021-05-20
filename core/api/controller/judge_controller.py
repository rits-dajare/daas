from flask import Blueprint, request, jsonify
import typing

from core.service.dajare_service import DajareService
from core.api.request import judge_request
from core.api.response import judge_response

dajare_service = DajareService()

bp: Blueprint = Blueprint('judge', __name__)


@bp.route('/', methods=['GET'])
def judge_dajare() -> typing.Tuple[str, int]:
    status_code: int
    result = judge_response.JudgeResponse()

    # query params
    params = judge_request.JudgeRequest(request.args)

    # judge dajare
    try:
        dajare = dajare_service.judge_dajare(params.dajare)
        result.is_dajare = dajare.is_dajare
        result.applied_rule = dajare.applied_rule

        status_code = 200
        result.status = "OK"
        result.message = "success"

    except Exception as e:
        status_code = 500
        result.status = "NG"
        result.message = str(e)

    return jsonify(result.__dict__), status_code
