FROM python:3.12-slim

ENV PATH="/app:${PATH}"

RUN apt-get update
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
COPY ./qa-workflow-test /app/qa-workflow-test

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["/venv/bin/python", "-m", "qa-workflow-test"]
