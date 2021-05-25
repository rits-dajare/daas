from fastapi import APIRouter, Depends, HTTPException

from core.service.dajare_service import DajareService
from core.api.request.judge_request import JudgeRequest
from core.api.response.judge_response import JudgeResponse

dajare_service = DajareService()

router = APIRouter()


@router.get('/', status_code=200, response_model=JudgeResponse, include_in_schema=False)
@router.get('', status_code=200, response_model=JudgeResponse)
async def judge_dajare(request: JudgeRequest = Depends()):
    # judge dajare
    try:
        dajare = dajare_service.judge_dajare(request.dajare)
    except Exception:
        raise HTTPException(status_code=500)

    return JudgeResponse(
        is_dajare=dajare.is_dajare,
        applied_rule=dajare.applied_rule,
    )
