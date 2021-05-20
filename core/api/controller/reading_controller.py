from flask import Blueprint, request, jsonify
import typing

from core import engine
from core.api.request import reading_request
from core.api.response import reading_response

bp: Blueprint = Blueprint('reading', __name__)


@bp.route('/', methods=['GET'])
def reading_dajare() -> typing.Tuple[str, int]:
    status_code: int
    result = reading_response.ReadingResponse()

    # query params
    params = reading_request.ReadingRequest(request.args)

    # reading dajare
    try:
        result.reading = engine.reading_engine.exec(params.dajare)

        status_code = 200
        result.status = "OK"
        result.message = "success"

    except Exception as e:
        status_code = 500
        result.status = "NG"
        result.message = str(e)

    return jsonify(result.__dict__), status_code
