# Python
FROM python:3.11.5-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apk --no-cache add postgresql-dev gcc musl-dev

# Install dependencies
COPY requirements.txt /app/
# speicifed version to prevent future malfunction 
RUN pip install --upgrade pip==23.2.1 && \
    pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]