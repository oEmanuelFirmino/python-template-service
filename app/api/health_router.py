from fastapi import APIRouter

from app.core.settings import HealthRouterResponse
from app.contracts.http_status import error_responses

router = APIRouter(tags=["health"])


@router.get("/health", responses=error_responses)
async def health_check() -> HealthRouterResponse:
    return HealthRouterResponse(
        status="ok", message="O serviço está funcionando corretamente!"
    )
