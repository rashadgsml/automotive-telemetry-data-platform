
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/
COPY sql/ ./sql/

EXPOSE 8000

CMD ["uvicorn", "telemetry.api:app", "--host", "0.0.0.0", "--port", "8000"]
