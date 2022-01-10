FROM python:3.9-slim

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .

ENV PYTHONUNBUFFERED 1
CMD ["gunicorn", "-b 0.0.0.0:8080", "main:app", "--access-logfile -", "--capture-output"]
