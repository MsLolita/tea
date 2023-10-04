import random
from random import choice

from fake_useragent import UserAgent  # pip install fake-useragent

from core.utils import str_to_file, logger
from string import ascii_lowercase, digits
from aiohttp import ClientSession

from inputs.config import (
    MOBILE_PROXY,
    MOBILE_PROXY_CHANGE_IP_LINK
)


class TeaXyz(ClientSession):
    referral = None

    def __init__(self, email: str):
        headers = {
            'authority': 'teaxyz.activehosted.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://tea.xyz',
            'referer': 'https://tea.xyz/',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random,
        }

        ClientSession.__init__(self, headers=headers, trust_env=True)

        self.email = email

        self.proxy = None

    async def define_proxy(self, proxy: str):
        if MOBILE_PROXY:
            await TeaXyz.change_ip()
            self.proxy = MOBILE_PROXY

        if proxy is not None:
            self.proxy = f"http://{proxy}"

    @staticmethod
    async def change_ip():
        async with ClientSession() as session:
            await session.get(MOBILE_PROXY_CHANGE_IP_LINK)

    async def enter_beta(self):
        url = 'https://teaxyz.activehosted.com/proc.php'

        data = {
            'u': '7',
            'f': '7',
            's': '',
            'c': '0',
            'm': '0',
            'act': 'sub',
            'v': '2',
            'or': 'da7da7643f23fec57e826a8a989fb54a',
            'email': self.email,
            'field[5]': random.choice(["Yes", "No"]),
        }

        async with self.post(url, data=data, proxy=self.proxy, allow_redirects=False, ssl=False) as resp:
            return await resp.text(), resp.status

    def logs(self, file_name: str, msg_result: str = ""):
        file_msg = f"{self.email}|{self.proxy}"
        str_to_file(f"./logs/{file_name}.txt", file_msg)
        msg_result = msg_result and " | " + str(msg_result)

        if file_name == "success":
            logger.success(f"{self.email}{msg_result}")
        else:
            logger.error(f"{self.email}{msg_result}")

    @staticmethod
    def generate_password(k=10):
        return ''.join([choice(ascii_lowercase + digits) for _ in range(k)])
