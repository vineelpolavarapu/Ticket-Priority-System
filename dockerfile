FROM python:3.11-slim

WORKDIR /app

COPY backend/core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

ENV FLASK_APP=backend.core.app:app
ENV PYTHONUNBUFFERED=1
ENV DB_TYPE=sqlite
ENV SQLITE_DB_PATH=/tmp/tickets.db

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 60 backend.core.app:app