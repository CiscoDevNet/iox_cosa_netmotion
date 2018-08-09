FROM python:alpine

RUN apk update

RUN apk add --no-cache --virtual .run-deps openssh libffi rsync && \
    apk add --no-cache --virtual .build-deps gcc libc-dev libffi-dev openssl-dev make

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py cell_data.py gps_data.py wifi_data.py .

CMD python app.py

