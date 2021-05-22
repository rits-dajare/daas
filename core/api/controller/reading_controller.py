from flask import Blueprint, request, jsonify
from flask.wrappers import Response
import typing

from core.service.dajare_service import DajareService
from core.api.request import reading_request
from core.api.response import reading_response

dajare_service = DajareService()

bp: Blueprint = Blueprint('reading', __name__)


@bp.route('/', methods=['GET'])
def reading_dajare() -> typing.Tuple[Response, int]:
    status_code: int
    result = reading_response.ReadingResponse()

    # query params
    params = reading_request.ReadingRequest(request.args)

    # convert reading
    try:
        dajare = dajare_service.convert_reading(params.dajare)
        result.reading = dajare.reading

        status_code = 200
        result.status = "OK"
        result.message = "success"

    except Exception as e:
        status_code = 500
        result.status = "NG"
        result.message = str(e)

    return jsonify(result.__dict__), status_code
