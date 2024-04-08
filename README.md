# Trading System

A simple trading system built using Django REST Framework.
The purpose of this system is to allow/grant authenticated users the ability to place orders to buy and sell stocks and track
the overall value of their investments.

### Built With:

* Python
* Django
* Django REST Framework


## Getting Started

### Prerequisites


### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/karlguevarra/trading-system.git
   ```
2. Change directory to the project folder.
3. Create Virtual Environment.
    ```sh
   python -m venv .venv
   ```
4. Install the requirements.
   ```sh
   pip install -r requirements.txt
   ```
5. Create and run migrations, make sure you are in the directory where the `manage.py` is.
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create user.
   ```sh
   python manage.py createsuperuser --username admin --email admin@test.com
   ```
   After creating a user, create a dummy data for stocks model
7. Run the server
   ```sh
   python manage.py runserver
   ```
8. Create stocks data by using curl
   ```sh
   curl --location 'http://127.0.0.1:8000/api/stocks/create/' \
   --header 'Content-Type: application/json' \
   --data '{
       "name": "HET",
       "price": "500.00",
       "supply": 1000
   }'

   curl --location 'http://127.0.0.1:8000/api/stocks/create/' \
   --header 'Content-Type: application/json' \
   --data '{
       "name": "CST",
       "price": "200.00",
       "supply": 1500
   }'

   curl --location 'http://127.0.0.1:8000/api/stocks/create/' \
   --header 'Content-Type: application/json' \
   --data '{
       "name": "LST",
       "price": "100.00",
       "supply": 222
   }'
   ```

## Using the Trading System

Before buying or selling a stock in the sytem, the user must get an access token by logging in or submitting a request through API. 

## Authentication

### Login
ENDPOINT: `api/login/`
To get an Access Token, submit a request using the endpoint and use JSON Format.
   ```sh
   {
       "username": "admin",
       "password": "password"
   }
   ```
The API should send a response together with the Access Token and Refresh Token
e.g:
   ```sh
   {
       "refresh": "refresh_token",
       "access": "access_token"
   }
   ```
Please note that the access token expires every 5mins. If the access token expires, you can send another request using the Refresh Token Endpoint.

### Refresh Token
ENDPOINT: `api/token/refresh/`
e.g:
   ```sh
   {
       "refresh": "refresh_token"
   }
   ```
Once submitted, the endpoint `api/token/refresh/` will send another JSON response with the access token and refresh token.
e.g:
   ```sh
   {
       "access": "access_token",
       "refresh": "refresh_token"
   }
   ```

Now that you know how to get an access token, let's proceed in using the sytem.

## Stocks
Endpoint and descriptions

### `api/stocks/`
To list all stocks
   ```sh
   curl --location 'http://127.0.0.1:8000/api/stocks/'
   ```
### `api/stocks/<id>/`
To list a single stock
   ```sh
   curl --location 'http://127.0.0.1:8000/api/stocks/1/'
   ```
## Trade
Endpoint and descriptions

### `api/stocks/trade/`
There are two transactions that can be made using the endpoint `api/stocks/trade/`.
If the parameter `is_buy` is equals to `true`, the system will treat it as Buy Stock.
If the parameter `is_buy` is equals to `false`, the system will treat it as Sell Stock.

Please note that this is using `Authorization: Bearer` in the header for the access token.
All authorized users are the only one that can submit a request using the endpoint `api/stocks/trade/`.
```sh
curl --location 'http://127.0.0.1:8000/api/stocks/trade/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNTUyMjg1LCJpYXQiOjE3MTI0OTIyODUsImp0aSI6Ijk3YWU1MTVhN2ExMDRhZDhiOThiNjk4N2FiNjQyZWQ1IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJzdGFmZiJ9.bHSytu8i-Px4ZqXZ2yFYImpQASYYB85jYiCrv7QiTQ8' \
--data '{
    "stock_id": 1,
    "quantity": 50,
    "is_buy": [true or false]
}'
```

## Trade (using CSV)

### `api/stocks/trade/csv/`
For this one to work, you need to place your CSV file in the path `project\api\csv\test.csv`.
Name your csv to `trade.csv`.

```sh
curl --location --request POST 'http://127.0.0.1:8000/api/stocks/trade/csv/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNTUyMjg1LCJpYXQiOjE3MTI0OTIyODUsImp0aSI6Ijk3YWU1MTVhN2ExMDRhZDhiOThiNjk4N2FiNjQyZWQ1IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJzdGFmZiJ9.bHSytu8i-Px4ZqXZ2yFYImpQASYYB85jYiCrv7QiTQ8'
```

## Stock Inventory

### `api/stocks/inventory/`
To list all your stocks in your inventory.

```sh
curl --location 'http://127.0.0.1:8000/api/stocks/inventory/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNTUyMjg1LCJpYXQiOjE3MTI0OTIyODUsImp0aSI6Ijk3YWU1MTVhN2ExMDRhZDhiOThiNjk4N2FiNjQyZWQ1IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJzdGFmZiJ9.bHSytu8i-Px4ZqXZ2yFYImpQASYYB85jYiCrv7QiTQ8'
```

## Testing

In Progress
