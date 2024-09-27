FROM python:3.12-slim

ENV PYTHONPATH "/app"

RUN apt-get update
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["/venv/bin/python", "-m", "qa_workflow_test"]
