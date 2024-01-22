# import json
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import datetime
import iso8601

# macro to attach debugger debugpy 1.8.0
DEBUG = True

app = FastAPI(title="Delivery Fee API")

class OrderDetails(BaseModel):
	cart_value: int = Field(description="The total cart value in cents", ge=0)
	delivery_distance: int = Field(descirption="The distance between the store and customer's location in meters", ge=0)
	number_of_items: int = Field(description="The number of items in the customer's shopping cart", ge=0)
	time_str: str = Field(description="Order time in UTC in ISO format")

	model_config = {
		"json_schema_extra": {
			"examples": [
				{
					"cart_value":790,
					"delivery_distance":2235,
					"number_of_items":4,
					"time_str":"2024-01-15T13:00:00Z",
				}
			]
		}
	}

# inclusing of 1900 or just till 1859?
# is beyond today?
def is_friday_rush_hours(order_time: str) -> bool:
	rush_hour_range = range(15, 19)
	order_time_converted = iso8601.parse_date(order_time)
	if order_time_converted.weekday() == 4 and order_time_converted.hour in rush_hour_range:
		print(order_time_converted.hour, ":", order_time_converted.min)
		return True
	return False

@app.post("/delivery-fee") #what uri? snake case?
def calculate_delivery_fee(order_details: OrderDetails) -> Response:
	try:
		is_rush_hour_order = is_friday_rush_hours(order_details.time_str)
		print("Order day is friday: ", is_rush_hour_order)
	except iso8601.iso8601.ParseError as e:
		return JSONResponse(status_code=422, content={"error": "invalid date formating"}) #how to correctly return error case?
	
	return JSONResponse(status_code=201, content={"delivery_fee": "Hello!"})




if __name__ == "__main__":
	if DEBUG:
		import uvicorn
		uvicorn.run(app, host="0.0.0.0", port=8000)
		# import debugpy
		# # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
		# debugpy.listen(5678)
		# debugpy.wait_for_client()
		print("hello")