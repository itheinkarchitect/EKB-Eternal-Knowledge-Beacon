from datetime import timedelta

from bot.services.profanity import count_profanity
from bot.database.profanity_logs import save_profanity, get_profanity_count
from bot.database.warning import add_warning, get_warning_count, clear_warnings
from bot.database.mute import add_mute, get_mute_count
from bot.database.ban import add_ban


async def handle_message(message):
    count = count_profanity(message.content)

    if count == 0:
        return

    save_profanity(message.author.id, count)

    total = get_profanity_count(message.author.id)

    if total <= 30:
        return

    await handle_warning(message)

async def handle_warning(message):
    add_warning(message.author.id)

    warning_count = get_warning_count(message.author.id)

    if warning_count < 5:
        return

    await handle_mute(message)

async def handle_mute(message):
    await message.author.timeout(
        timedelta(hours=24),
        reason="5 предупреждений за нарушение правил"
    )

    add_mute(message.author.id)

    mute_count = get_mute_count(message.author.id)

    clear_warnings(message.author.id)

    if mute_count < 3:
        return

    await handle_ban(message)

async def handle_ban(message):
    await message.author.ban(
        reason="3 мута за последние 30 дней"
    )

    add_ban(message.author.id)