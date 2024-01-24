import pytest
from main import is_rush_hours, app, calculate_distance_fees, check_for_small_order_fee, calculate_item_count_surcharges
import delivery_fee_macros

"""
#  Tests for `is_rush_hours' function
- tests written for Rush hours friday 15:00 - 19:00
"""
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

"""
#  Tests for `calculate_distance_fees' function
- test writtin with BASE_DISTANCE of 1000 meters before addtional fees
"""

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

def test_calculate_distance_fees_4500():
	distance = 4500
	expected = delivery_fee_macros.BASE_DISTANCE_FEE + (delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * 7)
	fees = calculate_distance_fees(distance)
	assert fees == expected

def test_calculate_distance_fees_4501():
	distance = 4501
	expected = delivery_fee_macros.BASE_DISTANCE_FEE + (delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * 8)
	fees = calculate_distance_fees(distance)
	assert fees == expected

"""
# Tests for check_for_small_order_fee func
setup for small order threshold of 1000 cents or 10€
"""

@pytest.mark.parametrize("normal_orders", [
	1300, 2000, 1000, 1001
])

def test_check_for_small_order_fee_not_applied(normal_orders):
	assert check_for_small_order_fee(normal_orders) == 0

@pytest.mark.parametrize("small_orders", [
	700, 999, 1, 300, 75
])

def test_check_for_small_order_fee_applied(small_orders):
	assert check_for_small_order_fee(small_orders) != 0

def test_check_for_small_order_fee_exact_425():
	cart_value = 425
	expected = delivery_fee_macros.SMALL_ORDER_THRESHOLD - cart_value
	res = check_for_small_order_fee(cart_value)
	assert res == expected

def test_check_for_small_order_fee_exact_999():
	cart_value = 999
	expected = delivery_fee_macros.SMALL_ORDER_THRESHOLD - cart_value
	res = check_for_small_order_fee(cart_value)
	assert res == expected

"""
#	Tests for calculate_item_count_surcharges
- test cases writted with large order surchages starting at 5 items and 
bulk order starting at 13
"""

@pytest.mark.parametrize("no_charges", [
	1, 2, 3, 4
])

def test_calculate_item_count_surcharges_none(no_charges):
	assert calculate_item_count_surcharges(no_charges) == 0

@pytest.mark.parametrize("large_charges, expected_number_of_fees", [
	(5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 6), (11, 7)
])

def test_calculate_item_count_surcharges_large(large_charges, expected_number_of_fees):
	assert calculate_item_count_surcharges(large_charges) == expected_number_of_fees * delivery_fee_macros.LARGE_ORDER_ITEM_FEE

@pytest.mark.parametrize("mixed_charges, expected_num_fees_to_apply", [
	(3, 0), (6, 2), (1, 0), (12, 8), (15, 11), (13, 9)
])

def test_calculate_item_count_surcharges_none(mixed_charges, expected_num_fees_to_apply):
	expected = expected_num_fees_to_apply * delivery_fee_macros.LARGE_ORDER_ITEM_FEE
	if mixed_charges > delivery_fee_macros.BULK_ORDER_THRESHOLD:
		expected += delivery_fee_macros.BULK_ORDER_FEE
	res = calculate_item_count_surcharges(mixed_charges)
	assert res == expected