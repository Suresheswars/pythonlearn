FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

#Enable for Render Deployment
CMD ["bash", "-c", "\
    echo '🚀 Starting FastAPI (internal)...' && \
    uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 --loop asyncio & \
    echo '⏳ Waiting for FastAPI...' && \
    until curl -s http://127.0.0.1:8000/health > /dev/null; do sleep 1; done && \
    echo '🚀 Starting Streamlit (public)...' && \
    python -m streamlit run src/frontend/app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
"]

#Enable for local run
# CMD ["bash", "-c", "\
#     echo '🚀 Starting FastAPI (internal)...' && \
#     uvicorn src.backend.main:app --host 127.0.0.1 --port 8000 & \
#     echo '⏳ Waiting for FastAPI...' && \
#     until curl -s http://127.0.0.1:8000/health > /dev/null; do sleep 1; done && \
#     echo '🚀 Starting Streamlit (public)...' && \
#     python -m streamlit run src/frontend/app.py \
#     --server.port=10000 \
#     --server.address=0.0.0.0 \
#     --server.headless=true \
# "]