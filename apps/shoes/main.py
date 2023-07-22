from fastapi import FastAPI
from typing import Optional
from starlette.types import Lifespan
from fastapi.applications import AppType


def create_app(lifespan: Optional[Lifespan[AppType]] = None) -> FastAPI:
    app = FastAPI(
        version='1.0.0',
        title='Shoes API',
        description='Shoes API Documentation - AtlanticaConf 2023',
        docs_url=None,
        redoc_url='/docs',
        lifespan=lifespan
    )

    @app.on_event('startup')
    async def startup():
        pass

    @app.on_event('shutdown')
    async def shutdown():
        pass

    from apps.shoes.routes.router import shoes_router

    app.include_router(prefix='/v1/shoes', router=shoes_router)

    return app
