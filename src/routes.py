from starlette.routing import Route

from src.domains.agent import views as agent_views

routes = [
    Route('/agent.chat', agent_views.chat, methods=['POST']),
]
