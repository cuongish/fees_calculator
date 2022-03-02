# Delivery Fees Calculator

A simple API for calculating delivery fees based on cart value, delivery distance, number of items and ordering time. 


### Calculator Logic

If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.<br/>

A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.


Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€ <br/>
Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€ <br/>
Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€<br/>

If the number of items is five or more, an additional 50 cent surcharge is added for each item above four
Example 1: If the number of items is 4, no extra surcharge<br/>
Example 2: If the number of items is 5, 50 cents surcharge is added<br/>
Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added<br/>


The delivery fee can never be more than 15€, including possible surcharges.

The delivery is free (0€) when the cart value is equal or more than 100€.

During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.1x. However, the fee still cannot be more than the max (15€).

### Sample request and response payload
```
input = {
 "cart_value": 790,
 "delivery_distance": 2235,
 "number_of_items": 4,
 "time": "2021-10-12T13:00:00Z"
}

output = {
 "delivery_fee": 710
}
```

### Virtual environment
- Create the virtualenv
```bash 
virtualenv -p python3.8 venv
```
- Activate the virtualenv
```bash
source venv/bin/activate
```

### How to Run It

- Install requirements as usual:
    ```bash
       pip install -r requirements/requirements.txt
       pip install -r requirements/test-requirements.txt
    ```
  
- Run the FastAPI app using:
  ```bash
  uvicorn main:app --reload
  ```
  
- Open API Documentation after running to try out the API:
  http://127.0.0.1:8000/docs


- Run pytest with coverage:
  ```bash
  coverage run -m pytest
  ```