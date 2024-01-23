from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import is_rush_hours, app, calculate_distance_fees
import pytest
import json
import delivery_fee_macros

def get_client():
	return TestClient(app)

'''
#  Tests for `is_rush_hours' function
- tests written for Rush hours friday 15:00 - 19:00
'''
@pytest.mark.parametrize("not_rush_hours", [
	"2024-01-15T13:00:00Z",
	"2024-01-21T15:00:00Z",
	"2024-01-19T13:00:00Z",
	"2024-01-19T19:00:00Z"
])

def test_is_rush_hours_not_rush_hours(not_rush_hours):
	assert is_rush_hours(not_rush_hours) ==  False

@pytest.mark.parametrize("rush_hours", [
	"2024-01-19T15:00:00Z",
	"2024-01-12T16:00:00Z",
	"2024-01-5T18:59:00Z",
	"2024-01-5T15:01:00Z"
])
def test_is_friday_rush_hours_rush_hours(rush_hours):
	assert is_rush_hours(rush_hours) == True


# NOTE: tests for bad dates (old, future, not formatted corrrectly) , on edge of range times

'''
#  Tests for `calculate_distance_fees' function
- test writtin with BASE_DISTANCE of 1000 meters before addtional fees
'''

@pytest.mark.parametrize("min_fees", [
	0, 50, 500, 900, 999, 1000
])
def test_calculate_distance_fees_minimum_fees(min_fees):
	assert calculate_distance_fees(min_fees) == delivery_fee_macros.BASE_DISTANCE_FEE

@pytest.mark.parametrize("larger_fees", [
	1001, 1300, 1500, 1501, 2000, 2499
])
def test_calculate_distance_fees_not_minimum_fees(larger_fees):
	assert calculate_distance_fees(larger_fees) != delivery_fee_macros.BASE_DISTANCE_FEE

def test_calculate_distance_fees_one_extra_fee():
	distance = 1001
	assert calculate_distance_fees(distance) == delivery_fee_macros.BASE_DISTANCE_FEE + delivery_fee_macros.ADDITIONAL_DISTANCE_FEE

def test_calculate_distance_fees_two_extra_fees():
	distance = 1501
	assert calculate_distance_fees(distance) == delivery_fee_macros.BASE_DISTANCE_FEE + (delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * 2)


'''
#	Tests for POST method
'''

def test_free_delivery_yes():
	client = get_client()
	testPost = {"cart_value": 20000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
	response = client.post("/delivery-fee", json = testPost)
	assert response.status_code == 201
	assert response.json() == {"delivery_fee": 0}

def test_free_delivery_no():
	client = get_client()
	testPost = {"cart_value": 2000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
	response = client.post("/delivery-fee", json = testPost)
	assert response.status_code == 201
	assert response.json()["delivery_fee"] != 0

def test_max_delivery_price():
	client = get_client()
	testPost = {"cart_value": 2000, "delivery_distance": 9235, "number_of_items": 13, "time": "2024-01-15T13:00:00Z"}
	response = client.post("/delivery-fee", json = testPost)
	assert response.status_code == 201
	assert response.json()["delivery_fee"] == delivery_fee_macros.MAXIMUM_DELIVERY_FEE