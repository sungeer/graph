import pytest
from starlette.testclient import TestClient
from src.main import create_app
from src import settings

def test_settings_integrity():
    assert settings.VERSION is not None
    assert settings.ENVIRONMENT in ('development', 'testing', 'production')

def test_app_routes():
    app = create_app()
    client = TestClient(app)
    # Ensure routes are registered
    route_paths = [r.path for r in app.routes]
    assert '/agent.stream' in route_paths
    assert '/agent.ask' in route_paths
