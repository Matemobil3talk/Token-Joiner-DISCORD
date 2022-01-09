import os
import sys
import logging
import asyncio
import pymongo
from tasksio import TaskPool
from aiohttp import ClientSession

if sys.platform == "linux":
    clear = lambda: os.system("clear")
else:
    clear = lambda: os.system("cls")

reset = "\x1b[0m"
red = "\x1b[38;5;203m"

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;203m[\x1b[0m%(asctime)s\x1b[38;5;203m]\x1b[0m -> \x1b[38;5;203m%(message)s",
    datefmt="%H:%M:%S",
)

class Authentication:

    def __init__(self):
        self.client = pymongo.MongoClient("")
        self.db = self.client.get_database("astroid").get_collection("servers")

class Main:

    def __init__(self):
        self.tokens = []
        for line in open("data/tokens.txt"):
            self.tokens.append(line.replace("\n", ""))

    async def join_server(self, token, invite):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US", 
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        try:
            token = token[:25] + "*"*34
        except:
            token = "*"*len(token)
        async with ClientSession(headers=headers) as session:
            async with session.post("https://discord.com/api/v9/invites/%s" % (invite)) as r:
                text = await r.text()
                if "vanity_url_code" in text:
                    logging.info("%s successfully joined" % (token))
                elif "You need to verify your account" in text:
                    logging.error("%s is not verified" % (token))
                elif "Unauthorized" in text:
                    logging.error("%s is invalid" % (token))
                elif "banned from this guild" in text:
                    logging.error("%s is banned" % (token))
                elif "Maximum number of guilds reached" in text:
                    logging.error("%s is in 100 guilds already" % (token))
                else:
                    logging.error("%s failed to join" % (token))
                    await self.join_server(token, invite)

    async def leave_server(self, token, id):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US", 
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        try:
            token = token[:25] + "*"*34
        except:
            token = "*"*len(token)
        async with ClientSession(headers=headers) as session:
            async with session.delete("https://discord.com/api/v9/users/@me/guilds/%s" % (id)) as r:
                text = await r.text()
                if r.status == 204:
                    logging.info("%s successfully left" % (token))
                elif "You need to verify your account" in text:
                    logging.error("%s is not verified" % (token))
                elif "Unauthorized" in text:
                    logging.error("%s is invalid" % (token))
                else:
                    logging.error("%s failed to leave" % (token))
                    await self.leave_server(token, id)

    async def send_message(self, token, id, message):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        try:
            token = token[:25] + "*"*34
        except:
            token = "*"*len(token)
        async with ClientSession(headers=headers) as session:
            async with session.post("https://discord.com/api/v9/channels/%s/messages" % (id), json={"content": "%s | %s" % (message, os.urandom(5).hex())}) as r:
                text = await r.text()
                if "content" in text:
                    logging.info("%s successfully sent message" % (token))
                elif "You need to verify your account" in text:
                    logging.error("%s is not verified" % (token))
                elif "Unauthorized" in text:
                    logging.error("%s is invalid" % (token))
                else:
                    json = await r.json()
                    logging.error("%s failed to send message, %s" % (token, json["message"]))
                    await self.send_message(token, id, message)

    async def nickname(self, token, id, name):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        try:
            token = token[:25] + "*"*34
        except:
            token = "*"*len(token)
        async with ClientSession(headers=headers) as session:
            async with session.patch("https://discord.com/api/v9/guilds/%s/members/@me/nick" % (id), json={"nick": name}) as r:
                text = await r.text()
                if name in text:
                    logging.info("%s successfully changed nick" % (token))
                elif "You need to verify your account" in text:
                    logging.error("%s is not verified" % (token))
                elif "Unauthorized" in text:
                    logging.error("%s is invalid" % (token))
                else:
                    json = await r.json()
                    logging.error("%s failed to change nick, %s" % (token, json["message"]))
                    await self.nickname(token, id, name)

    async def direct_message(self, token, id, message):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        try:
            token = token[:25] + "*"*34
        except:
            token = "*"*len(token)
        async with ClientSession(headers=headers) as session:
            async with session.post("https://discord.com/api/v9/users/@me/channels", json={"recipient_id": id}) as r:
                if r.status == 200:
                    json = await r.json()
                    id = json["id"]
                    async with session.post("https://discord.com/api/v9/channels/%s/messages" % (id), json={"content": message}) as r:
                        text = await r.text()
                        if "content" in text:
                            logging.info("%s successfully sent message" % (token))
                        elif "You need to verify your account" in text:
                            logging.error("%s is not verified" % (token))
                        elif "Unauthorized" in text:
                            logging.error("%s is invalid" % (token))
                        else:
                            json = await r.json()
                            logging.error("%s failed to send message, %s" % (token, json["message"]))
                            await self.direct_message(token, id, message)
                else:
                    json = await r.json()
                    logging.error("%s failed to send message, %s" % (token, json["message"]))
                    await self.direct_message(token, id, message)

    async def start(self):
        clear()
        logging.info("%s[%s1%s]%s Join" % (reset, red, reset, red))
        logging.info("%s[%s2%s]%s Leave" % (reset, red, reset, red))
        logging.info("%s[%s3%s]%s Send Message" % (reset, red, reset, red))
        logging.info("%s[%s4%s]%s Change Nickname" % (reset, red, reset, red))
        logging.info("%s[%s5%s]%s Send Direct Message" % (reset, red, reset, red))
        print()
        option = input("%s[%s~%s] %sOption%s:%s " % (red, reset, red, reset, red, reset)).lower()
        print()
        if option == "1":
            invite = input("%s[%s~%s] %sInvite%s:%s discord.gg/" % (red, reset, red, reset, red, reset))
            print()
            async with TaskPool(5_000) as pool:
                for token in self.tokens:
                    await pool.put(self.join_server(token, invite))
            await asyncio.sleep(5)
            await self.start()
        elif option == "2":
            id = input("%s[%s~%s] %sGuild ID%s:%s " % (red, reset, red, reset, red, reset))
            print()
            async with TaskPool(5_000) as pool:
                for token in self.tokens:
                    await pool.put(self.leave_server(token, id))
            await asyncio.sleep(5)
            await self.start()
        elif option == "3":
            message = input("%s[%s~%s] %sMessage%s:%s " % (red, reset, red, reset, red, reset))
            channel = input("%s[%s~%s] %sChannel%s:%s " % (red, reset, red, reset, red, reset))
            amount = int(input("%s[%s~%s] %sAmount%s:%s " % (red, reset, red, reset, red, reset)))
            print()
            async with TaskPool(5_000) as pool:
                for x in range(amount):
                    for token in self.tokens:
                        await pool.put(self.send_message(token, channel, message))
            await asyncio.sleep(5)
            await self.start()
        elif option == "4":
            nick = input("%s[%s~%s] %sNickname%s:%s " % (red, reset, red, reset, red, reset))
            id = input("%s[%s~%s] %sGuild ID%s:%s " % (red, reset, red, reset, red, reset))
            print()
            async with TaskPool(5_000) as pool:
                for token in self.tokens:
                    await pool.put(self.nickname(token, id, nick))
            await asyncio.sleep(5)
            await self.start()
        elif option == "5":
            message = input("%s[%s~%s] %sMessage%s:%s " % (red, reset, red, reset, red, reset))
            id = input("%s[%s~%s] %sUser ID%s:%s " % (red, reset, red, reset, red, reset))
            amount = int(input("%s[%s~%s] %sAmount%s:%s " % (red, reset, red, reset, red, reset)))
            print()
            async with TaskPool(5_000) as pool:
                for x in range(amount):
                    for token in self.tokens:
                        await pool.put(self.direct_message(token, id, message))
            await asyncio.sleep(5)
            await self.start()
        else:
            await self.start()

if __name__ == '__main__':
    client = Main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start()) 