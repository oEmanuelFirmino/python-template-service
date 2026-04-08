from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging
from app.core.settings import Settings
from app.api.root_router import router as root_router
from app.api.health_router import router as health_router

setup_logging()

def create_app() -> FastAPI:
    settings = Settings()

    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.state.settings = settings

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=settings.allowed_credentials,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    app.include_router(root_router)
    app.include_router(health_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=app.state.settings.host,
        port=app.state.settings.port,
        reload=True,
    )
