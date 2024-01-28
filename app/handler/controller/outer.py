from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.handler.controller import dajare_controller


def fastapi_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(dajare_controller.router, prefix='/v1', tags=['dajare'])
    app.include_router(dajare_controller.router, prefix='', tags=['dajare'])

    @app.get('/')
    def index():
        return "health"

    app.title = 'DaaS API'
    app.openapi_tags = [
        {"name": "dajare", "description": "Operation with dajare _(ダジャレ)_ ."}
    ]

    return app
