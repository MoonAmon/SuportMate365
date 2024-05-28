import discord
from src.database import *
from src.client import *

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
