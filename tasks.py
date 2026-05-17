import random
from datetime import time
import pytz

import discord
from discord.ext import tasks

import config
import users
import astrology

@tasks.loop(time=time(hour=0, minute=0, tzinfo=pytz.timezone("Europe/Warsaw")))
async def periodic_update():
    config.logging.info(f"[TASK] periodic_update")
    users.change_chance_modifiers()
    astrology.generate_daily_horoscopes()
    for user in users.guild_users.values():
        config.logging.info(f"{ user }")

@tasks.loop(minutes=15)
async def mood_decay():
    mood_obj = config.STATE["mood"]

    delta = random.randint(-5, 5)

    if delta > 0:
        mood_obj.inc(delta)
    else:
        mood_obj.dec(abs(delta))

    config.logging.info(
        f"[MOOD] {mood_obj.get()} "
        f"{mood_obj.get_emoji()}"
    )


@tasks.loop(time=time(hour=3, minute=0, tzinfo=pytz.timezone("Europe/Warsaw")))
async def zucky_3am_reminder():
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        return

    await guild.fetch_members().flatten()

    for member in guild.members:
        if member.bot:
            continue
        if member.status != discord.Status.online:
            continue

        ctx = {
            "type": "zuckzkzk",
            "member": member,
            "author_id": member.id,
            "guild": guild,
        }

        await events.trigger_random_event("scary_zuck_3am", ctx)
