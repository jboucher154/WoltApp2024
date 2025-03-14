from fastapi import FastAPI, Response, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import iso8601
import delivery_fee_macros
from math import ceil


app = FastAPI(title="Delivery Fee API")


class OrderDetails(BaseModel):
    """
    OrderDetails class inherits from pydantic BaseModel and maps to fields in
    POST request body for delivery fee calculation
    """

    cart_value: int = Field(description="The total cart value in cents", ge=0)
    delivery_distance: int = Field(
        descirption="The distance between the store and customer's location in meters",
        ge=0,
    )
    number_of_items: int = Field(
        description="The number of items in the customer's shopping cart", ge=1
    )
    time: str = Field(description="Order time in UTC in ISO format")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cart_value": 790,
                    "delivery_distance": 2235,
                    "number_of_items": 4,
                    "time": "2024-01-15T13:00:00Z",
                }
            ]
        }
    }


def is_rush_hours(order_time: str) -> bool:
    """
    Checks if the string passed is for the rush hour times dictated by the
    constants imported by delivery_fee_macros: RUSH_HOUR_BEGIN, RUSH_HOUR_END,
    RUSH_DAY. Returns bool indicating fir the order time is in the rush hours,
    not the fee or modifier to apply

    :param order_time: string of ISO formated date, e.g. "2024-01-15T13:00:00Z"
    :return: bool indicating if time of order is during rush hours
    """
    rush_hour_range = range(
        delivery_fee_macros.RUSH_HOUR_BEGIN, delivery_fee_macros.RUSH_HOUR_END
    )
    order_time_converted = iso8601.parse_date(order_time)
    if (
        order_time_converted.weekday() == delivery_fee_macros.RUSH_DAY
        and order_time_converted.hour in rush_hour_range
    ):
        print(order_time_converted.hour, ":", order_time_converted.min)
        return True
    return False


def calculate_distance_fees(delivery_distance: int) -> int:
    """
    Applies the base distance fee and if distance is greater than that calculates the
    number of extra fees to apply. If the ADDITIONAL_DISTANCE_UNIT is 0 no additional
    fees will be applied. Returns the fee total in cents.

    Uses these constants from delivery_fee_macros to calculate all fees for distance:
    BASE_DISTANCE_FEE, BASE_DISTANCE, ADDITIONAL_DISTANCE_UNIT, ADDITIONAL_DISTANCE_FEE

    :param delivery_distance: int of total delivery distance in meters
    :return: int of total delivery fees for distance in cents
    """
    fees = delivery_fee_macros.BASE_DISTANCE_FEE
    extra_fees = 0

    if (
        delivery_distance > delivery_fee_macros.BASE_DISTANCE
        and delivery_fee_macros.ADDITIONAL_DISTANCE_UNIT != 0
    ):
        distance = delivery_distance - delivery_fee_macros.BASE_DISTANCE
        num_extra_fees = ceil(distance / delivery_fee_macros.ADDITIONAL_DISTANCE_UNIT)
        extra_fees = delivery_fee_macros.ADDITIONAL_DISTANCE_FEE * num_extra_fees
    return fees + extra_fees


def check_for_small_order_fee(cart_value: int) -> int:
    """
    Checks if the value of the cart qulaifies as a small order using the constant
    SMALL_ORDER_THRESHOLD from the delivery_fee_macros. The returned fee is calculated
    to be the SMALL_ORDER_THRESHOLD - the cart value.

    :param cart_value: int of cart value
    :return: int of fee to be added to delivery fee total
    """
    fee = 0

    if cart_value < delivery_fee_macros.SMALL_ORDER_THRESHOLD:
        fee = delivery_fee_macros.SMALL_ORDER_THRESHOLD - cart_value
    return fee


def calculate_item_count_surcharges(item_count: int) -> int:
    """
    Determines fees associated with orders over the LARGE_ORDER_THRESHOLD and
    BULK_ORDER_THRESHOLD, calculating the fees using the LARGE_ORDER_ITEM_FEE and
    BULK_ORDER_FEE respectively.

    :param item_count: int of number of items in cart
    :return: int of total fees applied for item count in cents
    """
    fees = 0
    if item_count > delivery_fee_macros.LARGE_ORDER_THRESHOLD:
        items_over = item_count - delivery_fee_macros.LARGE_ORDER_THRESHOLD
        fees = items_over * delivery_fee_macros.LARGE_ORDER_ITEM_FEE
    if item_count > delivery_fee_macros.BULK_ORDER_THRESHOLD:
        fees += delivery_fee_macros.BULK_ORDER_FEE
    return fees


@app.post(
    "/delivery-fee",
    summary="calculates delivery fee based for an order",
    description="Applies all relevant fees based on the order details JSON data including delivery_fee",
)
def calculate_delivery_fee(
    order_details: OrderDetails = Body(
        title="order details",
        description="order details in JSON format containing cart value, delivery distance, "
        "number of items, and the date in ISO8601 format",
    )
) -> Response:
    """
    POST method for /delivery-fee location. Applies all relevant fees based on the order details
    and returns JSON data including delivery_fee

    :param order_details: json data from request body used to calculate the delivery fee
    :return: JSONResponse with status code and content set. In case of out of range order_details
    the response will be generated by FastAPI with HTTP code 422
    """
    fee = 0
    try:
        if order_details.cart_value < delivery_fee_macros.FREE_THRESHOLD:
            is_rush_hour_order = is_rush_hours(order_details.time)
            fee = calculate_distance_fees(order_details.delivery_distance)
            fee += check_for_small_order_fee(order_details.cart_value)
            fee += calculate_item_count_surcharges(order_details.number_of_items)
            if is_rush_hour_order:
                fee *= delivery_fee_macros.RUSH_HOUR_MULTIPLIER
    except iso8601.iso8601.ParseError as e:
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Invalid date formating. Provide iso8601 formatting in UTC"
            },
        )  # how to correctly return error case?
    if fee > delivery_fee_macros.MAXIMUM_DELIVERY_FEE:
        fee = delivery_fee_macros.MAXIMUM_DELIVERY_FEE
    return JSONResponse(status_code=201, content={"delivery_fee": fee})
