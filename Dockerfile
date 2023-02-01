FROM ubuntu:focal as build

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install "poetry==1.3.2"

COPY . /app
WORKDIR /app
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main

FROM ubuntu:focal

COPY --from=build /app /app

RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

VOLUME /app/_irc-logs
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "run.py", "-p", "80"]
EXPOSE 80
