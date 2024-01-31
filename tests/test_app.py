import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
import delivery_fee_macros


def get_client():
    return TestClient(app)


"""
#	Tests for POST method
"""


def test_free_delivery_yes():
    client = get_client()
    test_post = {
        "cart_value": 20000,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    }
    response = client.post("/delivery-fee", json=test_post)
    assert response.status_code == 201
    assert response.json() == {"delivery_fee": 0}


def test_free_delivery_no():
    client = get_client()
    test_post = {
        "cart_value": 2000,
        "delivery_distance": 2235,
        "number_of_items": 4,
        "time": "2024-01-15T13:00:00Z",
    }
    response = client.post("/delivery-fee", json=test_post)
    assert response.status_code == 201
    assert response.json()["delivery_fee"] != 0


def test_max_delivery_price():
    client = get_client()
    test_post = {
        "cart_value": 2000,
        "delivery_distance": 9235,
        "number_of_items": 13,
        "time": "2024-01-15T13:00:00Z",
    }
    response = client.post("/delivery-fee", json=test_post)
    assert response.status_code == 201
    assert response.json()["delivery_fee"] == delivery_fee_macros.MAXIMUM_DELIVERY_FEE


@pytest.mark.parametrize(
    "bad_requests",
    [
        {
            "cart_value": -790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 790,
            "delivery_distance": -2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 0,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": -1,
            "time": "2024-01-15T13:00:00Z",
        },
        {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "01-15T13:00:00Z",
        },
    ],
)
def test_incorrect_inputs(bad_requests):
    client = get_client()
    response = client.post("/delivery-fee", json=bad_requests)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "good_requests, fee",
    [
        (
            {
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            710,
        ),
        (
            {
                "cart_value": 1000,
                "delivery_distance": 1499,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            300,
        ),
        (
            {
                "cart_value": 1000,
                "delivery_distance": 1500,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            300,
        ),
        (
            {
                "cart_value": 1200,
                "delivery_distance": 1501,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            400,
        ),
        (
            {
                "cart_value": 1700,
                "delivery_distance": 500,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            200,
        ),
        (
            {
                "cart_value": 1050,
                "delivery_distance": 500,
                "number_of_items": 5,
                "time": "2024-01-15T13:00:00Z",
            },
            250,
        ),
        (
            {
                "cart_value": 1100,
                "delivery_distance": 500,
                "number_of_items": 10,
                "time": "2024-01-15T13:00:00Z",
            },
            500,
        ),
        (
            {
                "cart_value": 2000,
                "delivery_distance": 500,
                "number_of_items": 13,
                "time": "2024-01-15T13:00:00Z",
            },
            770,
        ),
        (
            {
                "cart_value": 150,
                "delivery_distance": 6500,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            1500,
        ),
        (
            {
                "cart_value": 1000,
                "delivery_distance": 500,
                "number_of_items": 4,
                "time": "2024-01-26T15:00:00Z",
            },
            240,
        ),
        (
            {
                "cart_value": 5060,
                "delivery_distance": 500,
                "number_of_items": 3,
                "time": "2024-01-26T13:00:00Z",
            },
            200,
        ),
        (
            {
                "cart_value": 0,
                "delivery_distance": 500,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            },
            1200,
        ),
    ],
)
def test_correct_inputs(good_requests, fee):
    client = get_client()
    response = client.post("/delivery-fee", json=good_requests)
    assert response.status_code == 201
    payload = response.json()
    assert payload["delivery_fee"] == fee
