from datetime import datetime
import httpx
import pytz
from collections import defaultdict


class KiwiParser:
    base_search_url = 'https://api.skypicker.com/flights'
    base_check_url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'

    search_extra_params = {
        'partner': 'picky',
        'curr': 'EUR'
    }
    check_extra_params = {
        'v': 2,
        'bnum': 1,
        'pnum': 1,
        'currency': 'EUR'
    }

    async def search_flights(self, *, fly_from: str, fly_to: str, date_from: datetime, date_to: datetime) -> dict:
        params = {
            'fly_from': fly_from,
            'fly_to': fly_to,
            'date_from': date_from.strftime('%d/%m/%Y'),
            'date_to': date_to.strftime('%d/%m/%Y')
        }
        params.update(self.search_extra_params)
        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_search_url, params=params, timeout=10)
        return await self.find_cheapest_by_date(r.json())

    @staticmethod
    async def find_cheapest_by_date(data: dict):
        date_flights = defaultdict(dict)
        for flight in data['data']:
            date = datetime.fromtimestamp(flight['dTimeUTC'], tz=pytz.UTC)
            key = date.strftime('%d-%m-%Y')
            if key in date_flights:
                date_flights[key]['count'] += 1
                date_flights[key]['prices'].append(flight['price'])
                if date_flights[key]['price'] > flight['price']:
                    date_flights[key]['price'] = flight['price']
                    date_flights[key]['id'] = flight['id']
                    date_flights[key]['booking_token'] = flight['booking_token']
                    date_flights[key]['dump'] = flight
            else:
                date_flights[key]['price'] = flight['price']
                date_flights[key]['id'] = flight['id']
                date_flights[key]['booking_token'] = flight['booking_token']
                date_flights[key]['count'] = 1
                date_flights[key]['prices'] = [flight['price']]
                date_flights[key]['fly_from'] = flight['flyFrom']
                date_flights[key]['fly_from'] = flight['flyFrom']
                date_flights[key]['city_from'] = flight['cityFrom']
                date_flights[key]['fly_to'] = flight['flyTo']
                date_flights[key]['city_to'] = flight['cityTo']
                date_flights[key]['dump'] = flight
        return date_flights

    async def check_flight(self, booking_token: str) -> dict:
        params = {
            'booking_token': booking_token
        }
        params.update(self.check_extra_params)
        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_check_url, params=params, timeout=10)
        data = r.json()
        cleaned = {
            'flights_checked': data['flights_checked'],
            'flights_to_check': data['flights_to_check'],
            'flights_real_checked': data['flights_real_checked'],
            'flights_invalid': data['flights_invalid'],
            'flights_price': data['flights_price'],
            'dump': data
        }
        return cleaned


kiwi_parser = KiwiParser()

