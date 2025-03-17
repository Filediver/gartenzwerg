# Stage 1: Build-Stage – Installation aller Abhängigkeiten
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04 as builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

# Stage 2: Runtime-Stage – schlankes End-Image erstellen und Abhängigkeiten installieren
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Kopiere die requirements.txt in die Runtime-Stage und installiere die Abhängigkeiten erneut
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Kopiere den Rest des Codes aus der Build-Stage
COPY --from=builder /app /app

CMD ["python3", "start.py"]
