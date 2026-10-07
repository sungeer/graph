from starlette.applications import Starlette

from src.core.lifespan import lifespan
from src.routes import routes


def create_app():
    app = Starlette(
        routes=routes,
        lifespan=lifespan
    )
    return app
