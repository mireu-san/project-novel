# Python
FROM python:3.11.5-alpine3.18

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
# caution - celery
RUN apk --no-cache add postgresql-dev gcc musl-dev

# speicifed version to prevent future malfunction 
RUN pip install --upgrade pip==23.2.1
# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files into the docker image
COPY . /app/
