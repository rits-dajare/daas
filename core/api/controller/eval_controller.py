from fastapi import APIRouter, Depends, HTTPException

from core.service.dajare_service import DajareService
from core.api.request.eval_request import EvalRequest
from core.api.response.eval_response import EvalResponse

dajare_service = DajareService()

router = APIRouter()


@router.get('/', status_code=200, response_model=EvalResponse, include_in_schema=False)
@router.get('', status_code=200, response_model=EvalResponse)
async def eval_dajare(request: EvalRequest = Depends()):
    # eval dajare
    try:
        dajare = dajare_service.eval_dajare(request.dajare)
    except Exception:
        raise HTTPException(status_code=500)

    return EvalResponse(
        score=dajare.score,
    )
