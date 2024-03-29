# Use a python based image
FROM python:3.9-alpine

# environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create a work directory
WORKDIR /app

# Instal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code to container contêiner
COPY . /app/

# runserver
EXPOSE 8080
CMD python manage.py runserver 0.0.0.0:8080
