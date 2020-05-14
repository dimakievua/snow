# FROM python:3.6-alpine
FROM python:3.7.5-slim
LABEL maintainer="Dmytro Zhernosiekov"

ENV SNOWURL httpbin.org
ENV ACTION post

# RUN apk update && apk add build-base
# RUN mkdir /usr/src/app

WORKDIR /usr/src/app
COPY . .

RUN python -m pip install parse realpython-reader && pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python3"]
CMD ["snow.py"]
