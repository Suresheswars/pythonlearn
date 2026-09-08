FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

# Default port both the container and Azure's WEBSITES_PORT app setting agree on.
# Deliberately different from FastAPI's internal 8000 to avoid a bind collision.
# Render overrides this at runtime via its own $PORT env var — entrypoint.sh handles both.
EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
