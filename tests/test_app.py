from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import is_friday_rush_hours, app

def get_client():
	return TestClient(app)

'''
#  Tests for `is_friday_rush_hours' function
'''
def test_is_friday_rush_hours_not_friday():
	test_date = "2024-01-15T13:00:00Z"
	result = is_friday_rush_hours(test_date)
	assert(result == False)

def test_is_friday_rush_hours_is_friday():
	test_date = "2024-01-19T13:00:00Z"
	result = is_friday_rush_hours(test_date)
	assert(result == False)

def test_is_friday_rush_hours_is_friday_rush_hours():
	test_date = "2024-01-19T15:00:00Z"
	result = is_friday_rush_hours(test_date)
	assert(result == True)

def test_is_friday_rush_hours_not_friday_rush_hours():
	test_date = "2024-01-21T15:00:00Z"
	result = is_friday_rush_hours(test_date)
	assert(result == False)

# tests for bad dates (old, future, not formatted corrrectly) , on edge of range times

'''
#	Tests for POST method
'''