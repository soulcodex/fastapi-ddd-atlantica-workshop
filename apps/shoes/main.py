from fastapi import FastAPI
from fastapi_injector import attach_injector
from apps.shoes.container import di_container
from apps.shoes.routes.router import shoes_router

app = FastAPI(
    version='1.0.0',
    title='Shoes API',
    description='Shoes API Documentation - AtlanticaConf 2023',
    docs_url=None,
    redoc_url='/docs'
)

attach_injector(app, di_container)

app.include_router(prefix='/v1/shoes', router=shoes_router)
