FROM python:3.11-slim

WORKDIR /app

COPY backend/core/requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

ENV FLASK_APP=backend.core.app:app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.core.app:app"]