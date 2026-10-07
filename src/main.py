from starlette.applications import Starlette

from src.graphs.graph_registry import graph_registry
from src.core.lifespan import lifespan
from src.routes import routes


def create_app():
    graph_registry.init()

    app = Starlette(
        routes=routes,
        lifespan=lifespan
    )
    return app
