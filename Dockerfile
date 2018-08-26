FROM debian:stretch-slim

RUN apt-get update && apt-get install -y \
    python3-requests \
    python3-flask \
    python3-twisted \
    irclog2html \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
VOLUME /app/_irc-logs
ENTRYPOINT ["python3", "run.py", "-p", "80"]
EXPOSE 80
