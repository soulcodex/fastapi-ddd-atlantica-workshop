from fastapi import FastAPI

from shoes.infrastructure.fastapi.lifespan_handler import lifespan_manager


def create_app() -> FastAPI:
    app = FastAPI(
        version='1.0.0',
        title='Shoes API',
        description='Shoes API Documentation - AtlanticaConf 2023',
        docs_url=None,
        redoc_url='/docs',
        lifespan=lifespan_manager
    )

    from apps.shoes.routes.router import shoes_router

    app.include_router(prefix='/v1/shoes', router=shoes_router)

    return app
