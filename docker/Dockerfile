FROM alpine:3.7

RUN apk add --no-cache alpine-sdk linux-headers libxml2-dev gcc musl-dev python3-dev libffi-dev openssl-dev jpeg-dev

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN pip install --upgrade pip


WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN pip3 install openpyxl python-dateutil
EXPOSE 5050
CMD python3 manage.py runserver