FROM python:3.10-alpine

# Instala as dependências de compilação e execução em uma única camada
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    libffi-dev \
    openssl-dev \
    && pip install --no-cache-dir --upgrade pip

# Copia apenas o necessário e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copia o código da aplicação
COPY ./app /code/app
WORKDIR /code

# Copia e configura o script de entrypoint
COPY .docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]