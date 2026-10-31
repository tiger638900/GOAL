FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service/ ./service/

RUN useradd -u 1000 service && chown -R service /app
USER service

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--log-level=info", "service:app"]
