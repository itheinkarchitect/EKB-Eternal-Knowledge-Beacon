from bot.services.moderation import handle_message


async def on_message(message):
    if message.author.bot:
        return

    print(f"{message.author}: {message.content}")

    await handle_message(message)