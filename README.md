# WoltApp2024 Backend Application 

Applicant: (Jenny Boucher)[https://www.github.com/jboucher154]

Technologies used: 
- Python 3.10
- FastAPI 0.108.0
- Pytest 7.4.4

Thank you for considering my application to Wolt as a backend engineer intern!

## To Run Program

- change ports to be compatible for your local setup, default is set to 8000 in commands given and in docker-compose.yml

### For local venv:

#### Setup virtual environment in root of poject:

> python3.10 -m venv env
> source env/bin/activate
> pip install -r requirements.txt

#### Run program:

> uvicorn --host 0.0.0.0 --port 8000 app.main:app --reload

To test POST api endpoint navigate to the FastAPI docs OR use curl or equvalent from the command line

To view FastAPI docs
> localhost:8000/docs

### For Docker:

If you prefer to test the assignment in a docker container you can create the image an run it using the provided Dockerfile and docker-compose

> docker compose up

To end program

> docker compose down

## Tests

Tests are written for the individual functions in the 'test_fucntion.py' file. Tests that use a test client from FastAPI are in the 'test_app.py' file

To run tests:

from project root run:
> pytest
OR for more detailed output
> pytest -v 
