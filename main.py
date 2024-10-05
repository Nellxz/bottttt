import os
from logging import getLogger, DEBUG, FileHandler, Formatter
from nextcord import Intents, Status, Streaming
from nextcord.ext import commands
from os import listdir
from asyncio import run
from typing import Dict, Optional
from myserver import server_on

# Set up logger
logger = getLogger("nextcord")
logger.setLevel(DEBUG)
handler = FileHandler(filename="log\discord.log", encoding="utf-8", mode="w")
handler.setFormatter(Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# prefix
Bot_prefix = "!"

# Set up intents
intent = Intents.default()
intent.members = True
intent.message_content = True  # Enable message content intent

# Create bot instance
React = commands.Bot(
    command_prefix=Bot_prefix,
    case_insensitive=True,
    help_command=None,
    intents=intent,
    strip_after_prefix=True,
)

async def loadcogs():
    import os
    cogs_directory = os.path.join(os.path.dirname(__file__), "cogs")
    for file in listdir(cogs_directory):
        if file.endswith(".py") and not file.startswith("__COMING__SOON"):
            try:
                React.load_extension(f"cogs.{file[:-3]}")
                print(f"Successfully loaded {file[:-3]}")
            except Exception as e:
                print(f"Unable to load {file[:-3]}: {e}")

@React.event
async def on_connect():
    # Use the new methods for deploying application commands
    try:
      React.add_all_application_commands()
      print("Connected to discord API")
    except Exception as e:
      print(f"Failed to connect to discord API: {e}")

@React.event
async def on_ready():
    print(f"{React.user} is online")
    await React.change_presence(
        status=Status.idle,
        activity=Streaming(
            name="Moomohfh",
            url="https://discord.gg/CAphTpFS",
        ),
    )

@React.event
async def on_message(message):
     # ตรวจสอบว่าเป็นข้อความที่มาจาก DM (ไม่มี guild)
     if message.guild is None:
         # ส่งข้อความแจ้งเตือนว่าบอทไม่รับคำสั่งจาก DM
         if message.content.startswith(Bot_prefix):
             await message.channel.send("อยากใช้ทักดิส awoskck อย่าแอบใช้อิอิ")
             await message.channel.send("อยากใช้ทักดิส awoskck อย่าแอบใช้อิอิ")
         return

     # ส่งต่อข้อความไปยังคำสั่งอื่น ๆ ถ้าไม่ใช่ DM
     await React.process_commands(message)

server_on()

if __name__ == "__main__":
    React.loop.run_until_complete(loadcogs())
    React.run(os.getenv('Bot_token'), reconnect=True)
