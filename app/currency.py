import aiohttp
import asyncio

from app.enum.currency import CurrencyEnum


async def get_rates(base_currency: str):
    async with aiohttp.ClientSession(base_url="https://v6.exchangerate-api.com/") as session:
        async with session.get(f"v6/fe9a3b30b461c965f4467270/latest/{base_currency}") as response:
            data = await response.json()
            currencies = data["conversion_rates"]
            print(currencies)
            return currencies

if __name__ == '__main__':
    asyncio.run(get_rates("RUB"))