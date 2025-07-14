FROM python:3.12

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD [ "python3", "-m" , "app"]
