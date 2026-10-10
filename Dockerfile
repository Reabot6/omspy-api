FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/omspy-api

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends less procps && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
