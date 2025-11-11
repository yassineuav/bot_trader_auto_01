FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=core.settings
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
