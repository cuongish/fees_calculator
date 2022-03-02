import unittest
from delivery_fees_calculator import add_friday_rush_surcharge
from delivery_fees_calculator import calculate_base_delivery_fee
from delivery_fees_calculator import calculate_delivery_fees
from delivery_fees_calculator import cap_delivery_fee

from main import Cart


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_case = Cart(cart_value=1000,  # 10 eur in cents no extra surcharge
                             delivery_distance=1000,  # base fee 2eur (in cents)
                             number_of_items=4,  # no extra surcharge
                             time="2021-10-12T13:00:00Z")  # not friday nor rush hour

        cls.expected_delivery_fee_for_base_case = 200
        cls.surcharge_in_cents_for_extra_item = 50
        cls.surcharge_in_cents_for_extra_500m = 100
        cls.surcharge_multiple_for_friday_rush_hour = 1.1

        # Edge case delivery fee
        cls.edge_case_max_delivery_fee = 1500
        cls.edge_case_min_delivery_fee = 0

        # Edge case cart value
        cls.edge_case_cart_value_less_than_10 = 890
        cls.edge_case_cart_value_is_equal_or_more_than_100 = 10000

        # Edge case delivery distance
        cls.edge_case_distance_is_1499 = 1499
        cls.edge_case_distance_is_1500 = 1500
        cls.edge_case_distance_is_1501 = 1501

        # Edge case number of items
        cls.edge_case_item_is_5 = 5
        cls.edge_case_item_more_than_5 = 10

        # Edge case time
        cls.edge_case_friday_rush_hour = "2021-10-15T15:00:00Z"
        cls.edge_case_friday_not_rush_hour = "2021-10-15T19:00:01Z"
        cls.edge_case_rush_hour_not_friday = "2021-10-14T15:00:00Z"
        cls.edge_case_not_friday_not_rush_hour = "2021-10-14T19:00:01Z"

    def test_calculate_base_delivery_fee__no_surcharge_if_cart_value_more_than_10(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_surcharge_cart_value_less_than_10(self):
        expected = self.expected_delivery_fee_for_base_case \
                   + (self.base_case.cart_value - self.edge_case_cart_value_less_than_10)

        result = calculate_base_delivery_fee(cart_value=self.edge_case_cart_value_less_than_10,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__no_surcharge_if_number_of_items_less_than_5(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_surcharge_if_number_of_items_is_5(self):
        expected = self.expected_delivery_fee_for_base_case \
                   + self.surcharge_in_cents_for_extra_item * (self.edge_case_item_is_5 - self.base_case.number_of_items)

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.edge_case_item_is_5)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_surcharge_if_number_of_items_more_than_5(self):
        expected = self.expected_delivery_fee_for_base_case \
                   + self.surcharge_in_cents_for_extra_item \
                   * (self.edge_case_item_more_than_5 - self.base_case.number_of_items)

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.edge_case_item_more_than_5)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_500m_surcharge_if_delivery_distance_is_1499m(self):
        expected = self.expected_delivery_fee_for_base_case + self.surcharge_in_cents_for_extra_500m

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.edge_case_distance_is_1499,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_500m_surcharge_if_delivery_distance_is_1500m(self):
        expected = self.expected_delivery_fee_for_base_case + self.surcharge_in_cents_for_extra_500m

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.edge_case_distance_is_1500,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__adds_1000m_surcharge_if_delivery_distance_is_1501m(self):
        expected = self.expected_delivery_fee_for_base_case \
                   + self.surcharge_in_cents_for_extra_500m * 2

        result = calculate_base_delivery_fee(cart_value=self.base_case.cart_value,
                                             delivery_distance=self.edge_case_distance_is_1501,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_calculate_base_delivery_fee__free_delivery_if_cart_value_is_equals_or_more_than_100e(self):
        expected = self.edge_case_min_delivery_fee

        result = calculate_base_delivery_fee(cart_value=self.edge_case_cart_value_is_equal_or_more_than_100,
                                             delivery_distance=self.base_case.delivery_distance,
                                             number_of_items=self.base_case.number_of_items)

        self.assertEqual(expected, result)

    def test_cap_delivery_fee__delivery_fees_capped_at_15_even_for_max_surcharges(self):
        expected = self.edge_case_max_delivery_fee

        base_fee_above_15 = calculate_base_delivery_fee(cart_value=99,
                                                        delivery_distance=1000000000,
                                                        number_of_items=100000000)

        result = cap_delivery_fee(base_fee_above_15)

        self.assertEqual(expected, result)

    def test_add_friday_rush_surcharge__if_cart_order_is_during_friday_rush_hour(self):
        expected = self.expected_delivery_fee_for_base_case * self.surcharge_multiple_for_friday_rush_hour

        result = add_friday_rush_surcharge(self.expected_delivery_fee_for_base_case,
                                           self.edge_case_friday_rush_hour)

        self.assertEqual(expected, result)

    def test_add_friday_rush_surcharge__if_cart_order_is_during_friday_not_rush_hour(self):
        expected = self.expected_delivery_fee_for_base_case

        result = add_friday_rush_surcharge(self.expected_delivery_fee_for_base_case,
                                           self.edge_case_friday_not_rush_hour)

        self.assertEqual(expected, result)

    def test_add_friday_rush_surcharge__if_cart_order_is_during_not_friday_not_rush_hour(self):
        expected = self.expected_delivery_fee_for_base_case

        result = add_friday_rush_surcharge(self.expected_delivery_fee_for_base_case,
                                           self.edge_case_not_friday_not_rush_hour)

        self.assertEqual(expected, result)

    def test_add_friday_rush_surcharge__if_cart_order_is_during_rush_hour_not_friday(self):
        expected = self.expected_delivery_fee_for_base_case

        result = add_friday_rush_surcharge(self.expected_delivery_fee_for_base_case,
                                           self.edge_case_rush_hour_not_friday)

        self.assertEqual(expected, result)

    def test_calculate_delivery_fees__for_base_case_with_no_surcharge(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_delivery_fees(cart_value=self.base_case.cart_value,
                                         delivery_distance=self.base_case.delivery_distance,
                                         number_of_items=self.base_case.number_of_items,
                                         time=self.base_case.time)

        self.assertEqual(expected, result)

    def test_calculate_delivery_fees__if_cart_is_during_friday_not_rush_hour(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_delivery_fees(cart_value=self.base_case.cart_value,
                                         delivery_distance=self.base_case.delivery_distance,
                                         number_of_items=self.base_case.number_of_items,
                                         time=self.edge_case_friday_not_rush_hour)

        self.assertEqual(expected, result)

    def test_calculate_delivery_fees__if_cart_is_during_friday_rush_hour(self):
        expected = self.expected_delivery_fee_for_base_case * self.surcharge_multiple_for_friday_rush_hour

        result = calculate_delivery_fees(cart_value=self.base_case.cart_value,
                                         delivery_distance=self.base_case.delivery_distance,
                                         number_of_items=self.base_case.number_of_items,
                                         time=self.edge_case_friday_rush_hour)

        self.assertEqual(expected, result)

    def test_calculate_delivery_fees__if_cart_order_is_during_rush_hour_not_friday(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_delivery_fees(cart_value=self.base_case.cart_value,
                                         delivery_distance=self.base_case.delivery_distance,
                                         number_of_items=self.base_case.number_of_items,
                                         time=self.base_case.time)

        self.assertEqual(expected, result)

    def test_calculate_delivery_fees__if_cart_order_is_during_not_rush_hour_not_friday(self):
        expected = self.expected_delivery_fee_for_base_case

        result = calculate_delivery_fees(cart_value=self.base_case.cart_value,
                                         delivery_distance=self.base_case.delivery_distance,
                                         number_of_items=self.base_case.number_of_items,
                                         time=self.base_case.time)

        self.assertEqual(expected, result)
