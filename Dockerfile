FROM python:3.12.1-alpine3.19


RUN apk update
RUN apk upgrade
RUN apk add --no-cache ffmpeg

RUN mkdir /code
WORKDIR /code

COPY reqs.txt .

RUN pip install -r reqs.txt

COPY . .

CMD ["python", "-u", "main.py"]