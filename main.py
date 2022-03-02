from typing import Dict
from typing import Optional

from fastapi import FastAPI
from pydantic import validate_arguments
from pydantic import BaseModel

from delivery_fees_calculator import calculate_delivery_fees


class Cart(BaseModel):
    cart_value: int  # in cents
    delivery_distance: int  # in meters
    number_of_items: int
    time: str


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.put("/calculate")
@validate_arguments
def calculate(cart: Cart) -> Optional[Dict]:
    delivery_fees = calculate_delivery_fees(cart_value=cart.cart_value,
                                            delivery_distance=cart.delivery_distance,
                                            number_of_items=cart.number_of_items,
                                            time=cart.time)
    return {"delivery_fees": delivery_fees}