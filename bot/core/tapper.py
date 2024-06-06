import asyncio
import hmac
import hashlib
from urllib.parse import unquote, quote

import aiohttp
import json
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestWebView
from .agents import generate_random_user_agent
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


class Tapper:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.user_id = 0
        self.username = None

    async def get_secret(self, userid):
        key_hash = str("adwawdasfajfklasjglrejnoierjboivrevioreboidwa").encode('utf-8')
        message = str(userid).encode('utf-8')
        hmac_obj = hmac.new(key_hash, message, hashlib.sha256)
        secret = str(hmac_obj.hexdigest())
        return secret

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            with_tg = True

            if not self.tg_client.is_connected:
                with_tg = False
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('pixelversexyzbot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                url='https://sexyzbot.pxlvrs.io/'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            self.user_id = (await self.tg_client.get_me()).id
            if (await self.tg_client.get_me()).username:
                self.username = (await self.tg_client.get_me()).username
            else:
                self.username = ''

            if with_tg is False:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def get_progress(self, http_client: aiohttp.ClientSession):
        try:
            async with http_client.get(url='https://api-clicker.pixelverse.xyz/api/mining/progress') as response:
                response_text = await response.text()
                data = json.loads(response_text)
                current_available = data.get('currentlyAvailable')
                min_amount_for_claim = data.get('minAmountForClaim')
                next_full = data.get('nextFullRestorationDate')
                if current_available and min_amount_for_claim and next_full:
                    return (current_available,
                            min_amount_for_claim,
                            next_full)
                return None, None, None
        except Exception as error:
            logger.error(f"Error happened: {error}")
            return None, None, None

    async def get_stats(self, http_client: aiohttp.ClientSession):
        try:
            async with http_client.get(url='https://api-clicker.pixelverse.xyz/api/users') as response:
                response_text = await response.text()
                data = json.loads(response_text)
                points = data.get('clicksCount')
                if points:
                    return points
                return None
        except Exception as error:
            logger.error(f"Error happened: {error}")
            return None

    async def claim_mining(self, http_client: aiohttp.ClientSession):
        try:
            async with http_client.post(url='https://api-clicker.pixelverse.xyz/api/mining/claim') as response:
                response_text = await response.text()
                data = json.loads(response_text)
                claimed_amount = data.get('claimedAmount')
                if claimed_amount:
                    return claimed_amount
                else:
                    return None
        except Exception as error:
            logger.error(f"Error happened: {error}")
            return None

    async def get_pet_id(self, http_client: aiohttp.ClientSession, name_pet):
        try:
            if name_pet is not None:
                async with http_client.get(url='https://api-clicker.pixelverse.xyz/api/pets') as response:
                    response_text = await response.text()
                    data = json.loads(response_text)
                    for pet in data.get('data'):
                        if pet.get('name') == name_pet:
                            return (pet.get('userPet').get('id'),
                                    pet.get('userPet').get('levelUpPrice'),
                                    data.get('buyPrice'))
            else:
                async with http_client.get(url='https://api-clicker.pixelverse.xyz/api/pets') as response:
                    response_text = await response.text()
                    data = json.loads(response_text)
                    return data.get('buyPrice')
            return None, None, None
        except Exception as error:
            logger.error(f"Error happened: {error}")
            return None, None, None

    async def buy_pet(self, http_client: aiohttp.ClientSession):
        async with http_client.post(url=f'https://api-clicker.pixelverse.xyz/api/pets/buy?'
                                        f'tg-id={self.user_id}&secret=adwawdasfajfklasjglrejnoierjb'
                                        f'oivrevioreboidwa', json={}) as response:
            response_text = await response.text()
            data = json.loads(response_text)
            if data.get('pet'):
                return data.get('pet').get('name')
            elif data.get('message'):
                return data.get('message')
            else:
                return None

    async def level_up_pet(self, http_client: aiohttp.ClientSession, pet_id):
        try:
            async with http_client.post(url=f'https://api-clicker.pixelverse.xyz/api/pets/'
                                            f'user-pets/{pet_id}/level-up') as response:
                response_text = await response.text()
                data = json.loads(response_text)
                level = data.get('level')
                cost = data.get('levelUpPrice')
                if level and cost:
                    return (level,
                            cost)
                else:
                    return None, None
        except Exception as error:
            logger.error(f"Error happened: {error}")
            return None, None

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        if proxy:
            await self.check_proxy(http_client=http_client, proxy=proxy)

        while True:
            try:
                tg_web_data = await self.get_tg_web_data(proxy=proxy)
                access_secret = await self.get_secret(userid=self.user_id)

                if not access_secret or not tg_web_data:
                    continue

                tg_web_data_parts = tg_web_data.split('&')
                query_id = tg_web_data_parts[0].split('=')[1]
                user_data = tg_web_data_parts[1].split('=')[1]
                auth_date = tg_web_data_parts[2].split('=')[1]
                hash_value = tg_web_data_parts[3].split('=')[1]

                # Кодируем user_data
                user_data_encoded = quote(user_data)

                # Формируем init_data
                init_data = f"query_id={query_id}&user={user_data_encoded}&auth_date={auth_date}&hash={hash_value}"

                http_client.headers["secret"] = f"{access_secret}"
                http_client.headers["initData"] = f"{init_data}"
                http_client.headers["tg-id"] = f"{self.user_id}"
                http_client.headers["username"] = f"{self.username}"
                (http_client.headers
                    ["User-Agent"]) = generate_random_user_agent(device_type='android', browser_type='chrome')

                current_available, min_amount, next_full = await self.get_progress(http_client=http_client)

                if ((current_available is not None and min_amount is not None) and (current_available > min_amount)
                        and settings.AUTO_CLAIM):
                    amount = await self.claim_mining(http_client=http_client)
                    if amount is not None:
                        balance = await self.get_stats(http_client=http_client)
                        logger.success(f"<light-yellow>{self.session_name}</light-yellow> | "
                                       f"<light-cyan>Claimed mining</light-cyan>, amount: "
                                       f"<green>{int(amount)}</green>. "
                                       f"Balance now: <green>{int(balance)}</green>")
                    else:
                        continue

                if settings.AUTO_UPGRADE:
                    name = settings.PET_NAME
                    id, cost, new_pet_cost = await self.get_pet_id(http_client=http_client, name_pet=name)
                    if cost is not None and id is not None:
                        while True:
                            balance = await self.get_stats(http_client=http_client)
                            if int(balance) >= int(cost):
                                level, cost = await self.level_up_pet(http_client=http_client, pet_id=id)
                                if level is not None and cost is not None:
                                    logger.success(f"<light-yellow>{self.session_name}</light-yellow> | "
                                                   f"Successfully upgraded pet: {name}. Level "
                                                   f"now: <green>{level}</green>, next level cost: "
                                                   f"<green>{cost}</green>")
                                await asyncio.sleep(delay=3)
                            else:
                                logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | "
                                               f"Not enough money to upgrade pet. "
                                               f"Balance: <green>{int(balance)}</green>, level up "
                                               f"pet cost: <green>{cost}</green>")
                                break
                    else:
                        logger.critical(
                            f"<light-yellow>{self.session_name}</light-yellow> | <red>Not found pet with that "
                            f"name in .env file</red>")

                if settings.AUTO_BUY:
                    balance = await self.get_stats(http_client=http_client)
                    new_pet_cost = await self.get_pet_id(http_client=http_client, name_pet=None)
                    if (balance is not None and new_pet_cost is not None) and int(balance) >= int(new_pet_cost):
                        pet_name = await self.buy_pet(http_client=http_client)
                        if (pet_name is not None) and str(pet_name) != "You can buy only 1 pet in 24 hours":
                            logger.success(f"<light-yellow>{self.session_name}</light-yellow> | Bought new pet, "
                                           f"you got <cyan>{pet_name}</cyan>")
                        else:
                            logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | Error while buying: "
                                           f"You can buy only 1 pet in 24 hours")

                logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Going sleep 1 hour")

                await asyncio.sleep(3600)

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
