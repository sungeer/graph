from contextlib import asynccontextmanager

from src.core.logger import setup_logger
from src.core.llm_registry import llm_registry
from src.agents.graph_registry import graph_registry


@asynccontextmanager
async def lifespan(app):
    setup_logger()

    llm_registry.init()

    graph_registry.init()

    yield

    llm_registry.close()
