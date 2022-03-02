import unittest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.base_case = {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2021-10-12T13:00:00Z"
        }

        cls.edge_case_time_wrong_datetime_iso_format = {
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "string"
        }
        cls.edge_case_cart_value_wrong_data_type = {
            "cart_value": "10.5",
            "delivery_distance": 1000,
            "number_of_items": 4,
            "time": "2021-10-12T13:00:00Z"
        }

    def test_home__returns_200(self):
        response = client.get("/")
        expected = 200
        self.assertEqual(response.status_code, expected)

    def test_home__displays_hello_world(self):
        response = client.get("/")
        expected = {"message": "Hello World"}
        self.assertEqual(response.json(), expected)

    def test_load__returns_422_if_posts_wrong_cart_value_data_type(self):
        resp = client.put("/calculate",
                          json=self.edge_case_cart_value_wrong_data_type
                          )
        self.assertEqual(resp.status_code, 422)

    def test_load__returns_correct_json_for_base_case(self):
        expected = {"delivery_fees": 200}
        resp = client.put("/calculate",
                          json=self.base_case
                          )
        self.assertEqual(resp.json(), expected)

    def test_load__returns_errors_if_posts_wrong_cart_value_data_type(self):
        expected = {'detail': [{'loc': ['body', 'cart_value'],
                                'msg': 'value is not a valid integer',
                                'type': 'type_error.integer'}]}
        resp = client.put("/calculate",
                          json=self.edge_case_cart_value_wrong_data_type
                          )
        self.assertEqual(resp.json(), expected)

    def test_calculate__raises_ValueError_if_time_wrong_datetime_iso_format(self):
        with self.assertRaises(ValueError):
            client.put("/calculate",
                       json=self.edge_case_time_wrong_datetime_iso_format
                       )

    def test_calculate__raises_Validate_error_(self):
        pass
