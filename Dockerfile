# Use a imagem oficial Python Alpine mais recente
FROM python:3.10-alpine as builder

# Instale as dependências de compilação
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Atualize pip e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Segunda etapa para a imagem final
FROM python:3.10-alpine

# Copie os pacotes Python instalados da etapa anterior
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copie o código da aplicação
COPY ./app /code/app
WORKDIR /code

# Copie e configure o script de entrypoint
COPY .docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]