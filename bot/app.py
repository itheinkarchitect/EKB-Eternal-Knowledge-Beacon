import discord
from bot.handlers.messages import on_message
from bot.services.ban_checker import check_bans

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Client(intents=intents)

    async def on_ready():
        if not check_bans.is_running():
            check_bans.start(bot)

    bot.event(on_ready)

    bot.event(on_message)

    return bot

