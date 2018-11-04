FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -e .
ENTRYPOINT gunicorn debateservice.app:api -b 0.0.0.0:8080
