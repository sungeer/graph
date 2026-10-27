# Multi-stage production container for LangGraph Agent
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime image
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    LOG_DIR=/app/logs \
    PYTHONPATH=/app

COPY --from=builder /install /usr/local
COPY . .

RUN mkdir -p logs

EXPOSE 8848

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8848/agent.ask', timeout=3)" || exit 0

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8848"]
