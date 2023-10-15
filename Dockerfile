FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip3.10 install -r requirements.txt

EXPOSE 8080

CMD [ "python3.10", "/app/app/main.py" ]
