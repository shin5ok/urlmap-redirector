FROM python:3.9-slim

WORKDIR /app
RUN apt update && apt install -y gcc g++ python3-grpc-tools python3-grpcio
COPY . .

RUN pip install --upgrade pip 
RUN pip install flask gunicorn
USER nobody

CMD exec gunicorn -b 0.0.0.0:8080 --error-logfile - --capture-output main:app