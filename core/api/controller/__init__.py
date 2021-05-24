from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import judge_controller
from . import eval_controller
from . import reading_controller


def create_app() -> FastAPI:
    app = FastAPI()

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # routing
    app.include_router(judge_controller.router, prefix='/judge', tags=['dajare'])
    app.include_router(eval_controller.router, prefix='/eval', tags=['dajare'])
    app.include_router(reading_controller.router, prefix='/reading', tags=['dajare'])

    # index
    @app.get('/')
    def index():
        return 'Hello, World!'

    # OpenAPI
    app.title = 'DaaS API'
    app.description = 'This is a document of DaaS.'
    app.version = '1.0.0'

    app.openapi_tags = [
        {"name": "dajare", "description": "Operation with dajare _(ダジャレ)_ ."}
    ]

    return app
