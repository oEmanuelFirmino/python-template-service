from fastapi import APIRouter

from app.core.settings import ApplicationInfo, RootResponse, ServerInfo, Settings
from app.contracts.http_status import error_responses

router = APIRouter(tags=["root"])
settings = Settings()


@router.get("/", responses=error_responses)
async def root() -> RootResponse:
    return RootResponse(
        application=ApplicationInfo(
            name=settings.app_name,
            description=settings.description,
            environment=settings.environment,
        ),
        server=ServerInfo(
            host=settings.host,
            port=settings.port,
            debug=settings.debug,
        ),
    )
