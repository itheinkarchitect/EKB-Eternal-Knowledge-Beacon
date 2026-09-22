import os

from dotenv import load_dotenv

from bot.app import create_bot
from bot.database.database import init_database

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

init_database()

bot = create_bot()

bot.run(TOKEN)