import discord
import os
from discord.ext import commands
from discord import app_commands, Intents
from log.log import logger
from dotenv import load_dotenv
from modal import *
from database import *
from commmands import *

# Define the guild ID for the Discord server
GUILD = discord.Object(897839630852952114)


# Define bot
class SupportClient(commands.Bot):
    def __init__(self, *args: object, **kwargs: object) -> object:
        super().__init__(*args, **kwargs)
        logger.warning('Bot is initializing.')

    async def setup_hook(self) -> None:
        await self.tree.sync()
        logger.warning('Bot setup completed.')


# Initialize the app
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.integrations = True
intents.messages = True
intents.message_content = True

Database.initialise()
bot = SupportClient(command_prefix='!', intents=intents)

bot.tree.sync()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Connected to the following guilds:")
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    print('---------------')

    await bot.loop.create_task(bot.tree.sync())

bot.run(TOKEN)


