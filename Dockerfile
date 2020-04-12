FROM python:3.8-alpine

USER 0

RUN apk add bash curl && \
    addgroup webapp -g 1000 && \
    adduser webapp -G webapp -u 1000 -g webapp -D

USER 1000

WORKDIR /app
ENV PATH=$PATH:/home/webapp/.local/bin

COPY --chown=webapp:webapp . /app
RUN pip3 install flask gunicorn python-dotenv --user

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]
