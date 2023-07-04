from fastapi import FastAPI
from starlette.middleware import Middleware
from apps.shoes.dependency_injection import di
from shared.domain.bus.query_bus import QueryBus
from apps.shoes.routes.router import shoes_router
from pyxdi.ext.fastapi import RequestScopedMiddleware, install as attach_pyxdi_container

app = FastAPI(
    version='1.0.0',
    title='Shoes API',
    description='Shoes API Documentation - AtlanticaConf 2023',
    docs_url=None,
    redoc_url='/docs',
    on_startup=[di.astart],
    on_shutdown=[di.aclose],
)

app.include_router(prefix='/v1/shoes', router=shoes_router)
attach_pyxdi_container(app, di)
app.add_middleware(RequestScopedMiddleware, di=di)
