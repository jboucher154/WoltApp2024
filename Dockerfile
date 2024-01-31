FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app ./app/

COPY tests ./tests/

ENV PYTHONPATH "${PYTHONPATH}:/code/app"
