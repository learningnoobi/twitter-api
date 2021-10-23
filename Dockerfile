FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
# RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "manage.py","runserver", "0.0.0.0:8000"]

