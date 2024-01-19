import json
from fastapi import FastApi
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastApi(title="Delivery Fee API")

class OrderDetails(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: str


#look up decorators
@app.post("/delivery-fee") #what uri?
def calculate_delivery_fee(order_details: OrderDetails):
	print(order_details.cart_value, order_details.delivery_distance, order_details.number_of_items, order_details.time)
	return JSONResponse(status_code=201, {"delivery_fee": "Hello!"})