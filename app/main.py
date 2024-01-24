# import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import datetime
import iso8601
import delivery_fee_macros
from math import ceil

# macro to attach debugger debugpy 1.8.0
DEBUG = True

app = FastAPI(title="Delivery Fee API")

'''
OrderDetails class maps to fields in POST request body for delivery fee calculation
'''
class OrderDetails(BaseModel):
	cart_value: int = Field(description="The total cart value in cents", ge=0)
	delivery_distance: int = Field(descirption="The distance between the store and customer's location in meters", ge=0)
	number_of_items: int = Field(description="The number of items in the customer's shopping cart", ge=0)
	time: str = Field(description="Order time in UTC in ISO format")

	model_config = {
		"json_schema_extra": {
			"examples": [
				{
					"cart_value":790,
					"delivery_distance":2235,
					"number_of_items":4,
					"time":"2024-01-15T13:00:00Z",
				}
			]
		}
	}

'''
# is_rush_hours
input: string of ISO formated date, e.g. "2024-01-15T13:00:00Z"
output: bool indicating if time of order is during rush hours
'''
def is_rush_hours(order_time: str) -> bool:
	rush_hour_range = range(delivery_fee_macros.RUSH_HOUR_BEGIN, delivery_fee_macros.RUSH_HOUR_END)
	order_time_converted = iso8601.parse_date(order_time)
	if order_time_converted.weekday() == delivery_fee_macros.RUSH_DAY and order_time_converted.hour in rush_hour_range:
		print(order_time_converted.hour, ":", order_time_converted.min)
		return True
	return False

'''
# calculate_distance_fees
input: int of total delivery distance in meters
output: int of total delivery fees for distance in cents
- uses BASE_DISTANCE_FEE, BASE_DISTANCE, ADDITIONAL_DISTANCE_UNIT, ADDITIONAL_DISTANCE_FEE
to calculate all fees for distance
'''
def calculate_distance_fees(delivery_distance: int) -> int:
	fees = delivery_fee_macros.BASE_DISTANCE_FEE
	extra_fees = 0

	if (delivery_distance > delivery_fee_macros.BASE_DISTANCE):
		distance = delivery_distance - delivery_fee_macros.BASE_DISTANCE
		num_extra_fees = ceil(distance / delivery_fee_macros.ADDITIONAL_DISTANCE_UNIT)
		extra_fees = delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * num_extra_fees
	return fees + extra_fees

'''
# check_for_small_order_fee
input: int of cart value
output: int of fee to be added to delivery fee total
if cart value if less than the SMALL_ORDER_THRESHOLD the fee is calculated
to to be the SMALL_ORDER_THRESHOLD - the cart value
'''
def check_for_small_order_fee(cart_value: int) -> int:
	fee = 0
	
	if cart_value < delivery_fee_macros.SMALL_ORDER_THRESHOLD:
		fee = delivery_fee_macros.SMALL_ORDER_THRESHOLD - cart_value
	return fee

'''
# calculate_item_count_surcharges
input: int of number of items in cart
output: int of total fees applied for item count in cents
'''
def calculate_item_count_surcharges(item_count: int) -> int:
	fees = 0
	if item_count > delivery_fee_macros.LARGE_ORDER_THRESHOLD:
		items_over = item_count - delivery_fee_macros.LARGE_ORDER_THRESHOLD
		fees = items_over * delivery_fee_macros.LARGE_ORDER_ITEM_FEE
	if item_count > delivery_fee_macros.BULK_ORDER_THRESHOLD:
		fees += delivery_fee_macros.BULK_ORDER_FEE
	return fees

'''
#
'''
@app.post("/delivery-fee") #what uri?
def calculate_delivery_fee(order_details: OrderDetails) -> Response:
	fee = 0
	try:
		if order_details.cart_value < delivery_fee_macros.FREE_THRESHOLD:
			is_rush_hour_order = is_rush_hours(order_details.time)
			fee = calculate_distance_fees(order_details.delivery_distance)
			fee += check_for_small_order_fee(order_details.cart_value)
			fee += calculate_item_count_surcharges(order_details.number_of_items)
			if is_rush_hour_order == True:
				fee *= delivery_fee_macros.RUSH_HOUR_MULTIPLIER
	except iso8601.iso8601.ParseError as e:
		return JSONResponse(status_code=422, content={"detail": "Invalid date formating. Provide iso8601 formatting in UTC"}) #how to correctly return error case?
	if fee > delivery_fee_macros.MAXIMUM_DELIVERY_FEE:
		fee = delivery_fee_macros.MAXIMUM_DELIVERY_FEE
	return JSONResponse(status_code=201, content={"delivery_fee": fee})



if __name__ == "__main__":
	if DEBUG:
		import uvicorn
		uvicorn.run(app, host="0.0.0.0", port=8000)
		# import debugpy
		# # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
		# debugpy.listen(5678)
		# debugpy.wait_for_client()
		print("debugging session complete")

# error msg for bad cart value
# {
#   "detail": [
#     {
#       "type": "greater_than_equal",
#       "loc": [
#         "body",
#         "cart_value"
#       ],
#       "msg": "Input should be greater than or equal to 0",
#       "input": -790,
#       "ctx": {
#         "ge": 0
#       },
#       "url": "https://errors.pydantic.dev/2.5/v/greater_than_equal"
#     }
#   ]
# }
		
'''
im sending for bad date:
{
  "msg": "invalid date formating. Provide iso8601 formatting in UTC"
}
'''