# WoltApp2024

//define tests 
- friday


- install and run instructions
- change ports to be compatible for your local setup, default is set to 8000

For Docker:
- If you prefer to test the assignment in a docker container
- 

For local venv:

Setup virtual environment:
> python3.10 -m venv env
> source env/bin/activate
> pip install -r requirements.txt

Run program:
> uvicorn --host 0.0.0.0 --port 8000 app.main:app --reload

	To test POST api endpoint navigate to:
	> localhost:8000 ...
	
	To view FastAPI docs
	> localhost:8000/docs

To run tests:
