FROM python:3.8-slim

WORKDIR /app
RUN apt update && apt install -y gcc g++ python3-grpc-tools python3-grpcio
COPY . .

RUN pip install --upgrade pip && \
	pip install -r requirements.txt

USER nobody
CMD exec gunicorn -b 0.0.0.0:8080 --error-logfile - --access-logfile - --capture-output main:app

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION python
