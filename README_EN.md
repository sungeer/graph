# graph

*An asynchronous agent runtime built with LangGraph and Starlette.*

[ [中文文档 (Chinese)](README.md) | [English Documentation](README_EN.md) ]

---

## Features

- **High-Performance Async Engine:** Built on Starlette and Uvicorn for asynchronous agent workflows.
- **Streaming Responses:** Real-time token streaming endpoint (`/agent.stream`).
- **Standard Ask Endpoint:** Synchronous/batched agent query endpoint (`/agent.ask`).
- **Container Ready:** Multi-stage production `Dockerfile` and `docker-compose.yml`.
- **Automated CI:** Matrix testing across Python 3.10, 3.11, and 3.12.

---

## Quick Start

### 1. Installation

```bash
git clone https://github.com/sungeer/graph.git
cd graph

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

### 2. Run Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8848
```

The server will be listening at `http://127.0.0.1:8848/`.

---

## Docker Deployment

Run with Docker Compose:

```bash
docker compose up -d
```

Or build and run directly:

```bash
docker build -t graph-agent:latest .
docker run -d -p 8848:8848 --name graph-agent -e ENVIRONMENT=production graph-agent:latest
```

---

## API Endpoints

- `POST /agent.stream`: Streams agent thought tokens in real-time.
- `POST /agent.ask`: Executes complete agent task and returns response.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
