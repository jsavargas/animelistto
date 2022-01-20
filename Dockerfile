FROM python:3.10.2-alpine

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5757


# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

RUN apk add --no-cache gcc musl-dev linux-headers 

RUN apk update
RUN apk add chromium chromium-chromedriver



COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5000
COPY ./src .
CMD ["flask", "run"]
