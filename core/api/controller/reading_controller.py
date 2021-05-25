from fastapi import APIRouter, Depends, HTTPException

from core.service.dajare_service import DajareService
from core.api.request.reading_request import ReadingRequest
from core.api.response.reading_response import ReadingResponse

dajare_service = DajareService()

router = APIRouter()


@router.get('/', status_code=200, response_model=ReadingResponse, include_in_schema=False)
@router.get('', status_code=200, response_model=ReadingResponse)
async def reading_dajare(request: ReadingRequest = Depends()):
    # convert reading
    try:
        dajare = dajare_service.convert_reading(request.dajare)
    except Exception:
        raise HTTPException(status_code=500)

    return ReadingResponse(
        reading=dajare.reading,
    )
