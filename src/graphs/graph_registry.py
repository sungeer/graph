from src.graphs.assistant.graph import build_graph as build_assistant_graph


class _GraphRegistry:

    def __init__(self):
        self._store = {}

    def init(self):
        self._store = {
            'assistant': build_assistant_graph(),
        }

    def get(self, name):
        if not self._store:
            raise RuntimeError('graph registry has not been initialized')
        if name not in self._store:
            raise KeyError(f'graph [{name}] not registered, available: {list(self._store.keys())}')
        return self._store[name]

    # registry['game']
    def __getitem__(self, name):
        return self.get(name)


graph_registry = _GraphRegistry()
