FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64 -O /usr/local/bin/mihomo && \
    chmod +x /usr/local/bin/mihomo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs output

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
