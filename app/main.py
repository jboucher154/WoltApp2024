# import json
from fastapi import FastAPI
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

def test_time(order_time):
	order_time_date = datetime.datetime.fromtimestamp(order_time)
	print("Order day: ", order_time_date.weekday())

@app.post("/delivery-fee") #what uri?
def calculate_delivery_fee(order_details: OrderDetails):
	# print(order_details)
	print(order_details.cart_value, order_details.delivery_distance, order_details.number_of_items, order_details.time)
	order_time = iso8601.parse_date(order_details.time)
	print("Order day: ", order_time.weekday())
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