FROM python:3.10-slim

RUN apt update
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN pip install --upgrade pip

COPY ./app /code/app
WORKDIR /code/

COPY ./requirements.txt /code/requirements.txt

COPY .docker/entrypoint.sh /entrypoint.sh

RUN pip install --no-cache-dir --upgrade  -r /code/requirements.txt \
    && chmod +x /entrypoint.sh

EXPOSE "8000"

CMD ["/entrypoint.sh"]
