from fastapi import APIRouter, Depends

from app.handler.dto.eval_dto import EvalV1
from app.handler.dto.judge_dto import JudgeV1
from app.handler.dto.reading_dto import ReadingV1
from app.service.dajare_service import DajareService

dajare_service = DajareService()

router = APIRouter()


@router.get('/eval/', status_code=200, response_model=EvalV1.Response, include_in_schema=False)
@router.get('/eval', status_code=200, response_model=EvalV1.Response)
async def eval_v1(request: EvalV1.Request = Depends()):
    dajare = dajare_service.eval_dajare(request.dajare)
    return EvalV1.Response(
        score=dajare.score,
    )


@router.get('/judge/', status_code=200, response_model=JudgeV1.Response, include_in_schema=False)
@router.get('/judge', status_code=200, response_model=JudgeV1.Response)
async def judge_v1(request: JudgeV1.Request = Depends()):
    dajare = dajare_service.judge_dajare(request.dajare)
    return JudgeV1.Response(
        is_dajare=dajare.is_dajare,
        applied_rule=dajare.applied_rule,
    )


@router.get('/reading/', status_code=200, response_model=ReadingV1.Response, include_in_schema=False)
@router.get('/reading', status_code=200, response_model=ReadingV1.Response)
async def reading_v1(request: ReadingV1.Request = Depends()):
    dajare = dajare_service.convert_reading(request.dajare)
    return ReadingV1.Response(
        reading=dajare.reading,
    )
