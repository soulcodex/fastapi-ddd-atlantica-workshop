import databases
from fastapi import FastAPI, Depends
from fastapi.dependencies.utils import get_flat_dependant
from typing_extensions import Annotated
from starlette.middleware import Middleware
from typing import cast, Callable, AsyncIterator
from shared.domain.bus.query_bus import QueryBus
from apps.shoes.routes.router import shoes_router
from apps.shoes.dependency_injection.common import configure_mysql_connection_pool as database_pool

app = FastAPI(
    version='1.0.0',
    title='Shoes API',
    description='Shoes API Documentation - AtlanticaConf 2023',
    docs_url=None,
    redoc_url='/docs',
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(prefix='/v1/shoes', router=shoes_router)
