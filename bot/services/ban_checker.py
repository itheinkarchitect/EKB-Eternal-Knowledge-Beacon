import discord
from datetime import datetime, timedelta
from discord.ext import tasks

from bot.database.ban import get_expired_bans, clear_ban


@tasks.loop(minutes=1)
async def check_bans(bot):
    await bot.wait_until_ready()

    expired_bans = get_expired_bans()

    for ban in expired_bans:
        for guild in bot.guilds:
            try:
                await guild.unban(
                    discord.Object(id=ban.user_id),
                    reason="Срок 7-дневного бана истёк"
                )

            except discord.NotFound:
                pass

            except discord.Forbidden:
                print(
                    f"Не удалось снять бан с {ban.user_id}: "
                    f"недостаточно прав."
                )

        clear_ban(ban.id)