# import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import datetime
import iso8601
import delivery_fee_macros

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
		num_extra_fees = distance // delivery_fee_macros.ADDITIONAL_DISTANCE_UNIT
		num_extra_fees += 0 if distance % delivery_fee_macros.ADDITIONAL_DISTANCE_UNIT == 0 else 1
		extra_fees = delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * num_extra_fees
	return fees + extra_fees

@app.post("/delivery-fee") #what uri? snake case?
def calculate_delivery_fee(order_details: OrderDetails) -> Response:
	fee = 0
	try:
		if (order_details.cart_value < delivery_fee_macros.FREE_THRESHOLD):
			fee = 2000
		#modifiers after total is known
		is_rush_hour_order = is_rush_hours(order_details.time)
	except iso8601.iso8601.ParseError as e:
		return JSONResponse(status_code=422, content={"msg": "invalid date formating. provide iso8601 formatting in UTC"}) #how to correctly return error case?
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
		print("hello")