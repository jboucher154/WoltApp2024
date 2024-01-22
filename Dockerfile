FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app ./app/

COPY tests ./tests/

# no expose port here?