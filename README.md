# REST todo's web app

## Table of content
 - [installation](#installation)
 - [deploy using docker-compose](#deploy-using-docker-compose)
 - [API](#api)


## installation
1. Clone the repo
    ```shell script
    git clone https://github.com/nabakirov/flight_prices.git
    ```
2. Step into repo dir
    ```shell script
    cd rest-todo
    ```
3. Install dependencies   
    using [pipenv](https://github.com/pypa/pipenv)
    ```shell script
    pipenv install && pipenv shell
    ```
    or using virtualenv
    ```shell script
    python3 -m virtualenv venv && source venv/bin/activate && pip install -r requirements.txt
    ```
4. Set environment variables   
    - REDIS_HOST=127.0.0.1   
    - REDIS_PORT=6379
    - REDIS_DB=1
    - DEBUG=False
    - PORT=8000  

5. Run   
    
   ```shell script
    python server.py
    ```
   

## deploy using docker-compose
1. Clone the repo
    ```shell script
    git clone https://github.com/nabakirov/rest-todo.git
    ```
2. Install and run
    ```shell script
    docker-compose up -d
    ```

## API
- [Get Flights](#flights)


### flights
#### GET */flights*
##### access - *public*
query params   
 - ?fly_from=CODE&fly_to=CODE   
 
response
```json5
{
  "15-04-2021": {
    "price": 15,
    "id": "",
    "booking_token": "",
    "count": 9,
    "prices": [
      15,
    ],
    "fly_from": "ALA",
    "city_from": "Almaty",
    "fly_to": "CIT",
    "city_to": "Shymkent",
    "checked": {
      "flights_checked": true,
      "flights_to_check": false,
      "flights_real_checked": true,
      "flights_invalid": false,
      "flights_price": 12.44
    }
  }
}
```