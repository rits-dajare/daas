from flask import Blueprint, request, jsonify
import typing

from core.service.dajare_service import DajareService
from core.api.request import eval_request
from core.api.response import eval_response

dajare_service = DajareService()

bp: Blueprint = Blueprint('eval', __name__)


@bp.route('/', methods=['GET'])
def eval_dajare() -> typing.Tuple[str, int]:
    status_code: int
    result = eval_response.EvalResponse()

    # query params
    params = eval_request.EvalRequest(request.args)

    # eval dajare
    try:
        dajare = dajare_service.eval_dajare(params.dajare)
        result.score = dajare.score

        status_code = 200
        result.status = "OK"
        result.message = "success"

    except Exception as e:
        status_code = 500
        result.status = "NG"
        result.message = str(e)

    return jsonify(result.__dict__), status_code
