import json
from datetime import datetime, timedelta
import asyncio

from sanic_scheduler import task

from app import redis
from parsers import kiwi_parser
from settings import DIRECTIONS


async def pull_flights(fly_from: str, fly_to: str, date_from: datetime, date_to: datetime):
    data = await kiwi_parser.search_flights(fly_from=fly_from, fly_to=fly_to, date_from=date_from, date_to=date_to)
    with await redis.conn as r:
        final_book = {}
        updated_keys = set()
        for date, flight_info in data.items():
            flight_key = f'{fly_from}-{fly_to}-{flight_info["id"]}'
            await r.set(flight_key, json.dumps(flight_info))
            updated_keys.add(flight_key)
            final_book[date] = flight_key
        await r.set(f"{fly_from}-{fly_to}", json.dumps(final_book))
        keys_to_delete = []
        async for key in r.iscan(match=f'{fly_from}-{fly_to}-*'):
            print(key)
            key = key.decode()
            if key not in updated_keys:
                keys_to_delete.append(key)
        await r.delete(*keys_to_delete)


async def check_flights(fly_from: str, fly_to: str):
    with await redis.conn as r:
        async for key in r.iscan(match=f'{fly_from}-{fly_to}-*'):
            print(key)
            flight = json.loads(await r.get(key))
            checked = await kiwi_parser.check_flight(flight['booking_token'])
            flight['checked'] = checked
            await r.set(key, json.dumps(flight))


@task(timedelta(hours=24))
async def scheduled_pull_flights(_):
    date_from = datetime.now()
    date_to = date_from + timedelta(days=30)
    tasks = []
    for fly_from, fly_to in DIRECTIONS:
        tasks.append(pull_flights(fly_from=fly_from, fly_to=fly_to, date_from=date_from, date_to=date_to))
    await asyncio.gather(*tasks, return_exceptions=True)


@task(timedelta(minutes=10), timedelta(minutes=1))
async def scheduled_check_flights(_):
    tasks = []
    for fly_from, fly_to in DIRECTIONS:
        tasks.append(check_flights(fly_from=fly_from, fly_to=fly_to))
    await asyncio.gather(*tasks, return_exceptions=True)
