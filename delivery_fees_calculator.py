import math
from datetime import datetime
from typing import Text

base_delivery_fees_in_cents = 200
surcharge_multiple_for_friday_rush_hour = 1.1
surcharge_in_cents_for_extra_item = 50
surcharge_in_cents_for_extra_500m = 100
delivery_distance_multiple_for_surcharge = 500

min_delivery_fee = 0
max_delivery_fee = 1500
rush_hour_lower_bound = 14
rush_hour_upper_bound = 19
rush_hour_iso_week_day = 5

cutoff_max_no_of_items = 4
cutoff_free_delivery_if_cart_value_exceeds = 10000
cutoff_cart_value_no_surcharge = 1000
cutoff_delivery_distance = 1000


def calculate_base_delivery_fee(cart_value: int,
                                delivery_distance: int,
                                number_of_items: int) -> float:
    """
    Calculate base delivery fees based on cart value, delivery distance and amount of items.
    Setting base fees to 0 ie. free delivery if cart value is above 100EUR
    :param cart_value: Value of the shopping cart in cents.
    :param delivery_distance: The distance between the store and customer’s location in meters.
    :param number_of_items: The number of items in the customer's shopping cart.
    :return: delivery_fee: Base delivery fees on cart in cents.
    """
    if cart_value < cutoff_free_delivery_if_cart_value_exceeds:
        surcharge = 0
        if cart_value < cutoff_cart_value_no_surcharge:
            surcharge += (cutoff_cart_value_no_surcharge - cart_value)
        if delivery_distance > cutoff_cart_value_no_surcharge:
            surcharge += math.ceil((delivery_distance - cutoff_delivery_distance)
                                   / delivery_distance_multiple_for_surcharge)*surcharge_in_cents_for_extra_500m
        if number_of_items > cutoff_max_no_of_items:
            surcharge += (number_of_items - cutoff_max_no_of_items) * surcharge_in_cents_for_extra_item
        delivery_fee = base_delivery_fees_in_cents + surcharge
    else:
        delivery_fee = min_delivery_fee
    return delivery_fee


def add_friday_rush_surcharge(delivery_fee: float, time: Text) -> float:
    """
    Apply Friday peak hour 3-7pm UTC surcharge on top of base delivery fees
    :param delivery_fee: Base delivery fees on cart in cents.
    :param time: Order time in ISO format.
    :return: Rush-hour filtered delivery fees on cart in cents.
    """
    timestamp = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
    if timestamp.isoweekday() == rush_hour_iso_week_day and rush_hour_lower_bound < timestamp.hour < rush_hour_upper_bound:
        delivery_fee *= surcharge_multiple_for_friday_rush_hour
    return delivery_fee


def cap_delivery_fee(delivery_fee: float) -> float:
    """
    Apply 15EUR cap on delivery fees
    :param delivery_fee: Base delivery fees on cart in cents.
    :return: Capped delivery fee in cents.
    """
    if delivery_fee > max_delivery_fee:
        delivery_fee = max_delivery_fee

    return delivery_fee


def calculate_delivery_fees(cart_value: int, delivery_distance: int,
                            number_of_items: int, time: Text) -> float:
    """
    :param cart_value: Value of the shopping cart in cents.
    :param delivery_distance: The distance between the store and customer’s location in meters.
    :param number_of_items: The number of items in the customer's shopping cart.
    :param time: Order time in ISO format.
    :return: 
    """
    base_fee = calculate_base_delivery_fee(cart_value=cart_value,
                                           delivery_distance=delivery_distance,
                                           number_of_items=number_of_items)

    applied_friday_rush_fee = add_friday_rush_surcharge(base_fee, time)

    final_fee = cap_delivery_fee(applied_friday_rush_fee)

    return final_fee
