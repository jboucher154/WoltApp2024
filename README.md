# WoltApp2024 Backend Application 

Applicant: [Jenny Boucher](https://www.github.com/jboucher154)

Technologies used: 
- Python 3.10
- FastAPI 0.108.0
- Pytest 7.4.4

Thank you for considering my application to Wolt as a backend engineer intern!

## About Data Handling

Some basic data validation is included with the use of a class that inherits from Pydantic Base Model and a few additional checks. 
This includes rejection of:
- Negative values for all integer fields 
- An empty cart, no calculation will occur for empty carts

I chose to allow the following:
- 0 value carts, as they may be discounted
- Past and future dates, validation of date time frame should be the responsibility of another function. This API endpoint will simply calculate the delivery fee given a valid date format.
- 0 distance deliveries

## To Run The Program

- Change ports to be compatible with your local setup. The default is set to 8000 in commands given and in docker-compose.yml

### For local venv:

#### Setup virtual environment at the root of the project:

For Mac/Linux:

```commandline
python3.10 -m venv env

source env/bin/activate

pip install -r requirements.txt
```


For Windows:
```commandline
path/to/python/3.10 -m venv env

path/to/myenv/Scripts/activate

pip install -r requirements.txt
```


#### Run program:

```commandline
uvicorn --host 0.0.0.0 --port 8000 app.main:app --reload
```

To test the POST API endpoint, navigate to the FastAPI docs OR use curl or equivalent from the command line

To view FastAPI docs
```commandline
localhost:8000/docs
```

When complete, deactivate the virtual environment with the command: 
```
deactivate
```

### For Docker:

If you prefer to test the assignment in a docker container, you can create the image and run it using the provided Dockerfile and docker-compose

```
docker compose up
```

To end program

```
docker compose down
```

## Tests

Tests are written for the individual functions in the `test_functions.py` file. Tests that use a test client from FastAPI are in the `test_app.py` file

To run tests in the venv:

from project root run:
```
pytest
```
OR for more detailed output
```
pytest -v
``` 

