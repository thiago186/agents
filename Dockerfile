FROM python:3.10-slim

COPY ./app /code/app
WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

COPY .docker/entrypoint.sh /entrypoint.sh

RUN apt update
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade  -r /code/requirements.txt \
    && chmod +x /entrypoint.sh


EXPOSE "8000"

CMD ["/entrypoint.sh"]
