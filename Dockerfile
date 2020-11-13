FROM debian:buster-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install "poetry==1.1.4"

COPY . /app
WORKDIR /app
RUN poetry install --no-dev
VOLUME /app/_irc-logs
ENTRYPOINT ["poetry", "run", "python", "run.py", "-p", "80"]
EXPOSE 80
