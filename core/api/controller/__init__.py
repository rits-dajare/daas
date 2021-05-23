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
    app.include_router(judge_controller.router, prefix='/judge', tags=['判定API'])
    app.include_router(eval_controller.router, prefix='/eval', tags=['評価API'])
    app.include_router(reading_controller.router, prefix='/reading', tags=['読み変換API'])

    # index
    @app.get('/', tags=['index'])
    def index():
        return 'Hello, World!'

    # OpenAPI
    app.title = 'DaaS API'
    app.description = 'This is a document of DaaS.'
    app.version = '1.0.0'

    return app
