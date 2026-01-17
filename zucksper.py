import discord
from discord.ext import commands, tasks

import random
from datetime import time
import pytz

import vc

import random
import gifs

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot_active = True
zuckprosiny_id = 1462139529480638699

async def random_event(msg, chance): 
    if random.random() < chance:
        await msg.channel.send(random.choice(gifs.tenor_urls))

async def send_dm(user_id: int, text: str):
    user = await bot.fetch_user(user_id)
    await user.send(text)

@tasks.loop(seconds=5)
async def przepros():
    if bot_active:
        przepros.stop()
        return
    await bot.get_channel(zuckprosiny_id).send("przepraszam 🥺")

@bot.event
async def on_ready():
    print(f"DzZIASjgasdk {bot.user}")

@bot.event
async def on_message(msg):
    global bot_active
    if msg.author.bot:
        return

    if isinstance(msg.channel, discord.DMChannel):
        print(  f"[MSG] {msg.author} ({msg.author.id}) "
                f"in #{msg.channel} ({msg.guild}): {msg.content}" )

    if not bot_active:
        if msg.channel.id == zuckprosiny_id and "wybaczam" in msg.content.lower():
            await msg.channel.send(file=discord.File("me.jpg"))
            bot_active = True
            await msg.add_reaction(discord.utils.get(bot.emojis, name="deep_hard_butt_sux_elf"));
            await bot.change_presence(status=discord.Status.online)
        return
    
    if bot.user in msg.mentions:
        if "cicho" in msg.content.lower():
            bot_active = False
            await msg.add_reaction(discord.utils.get(bot.emojis, name="brain1"))
            await bot.change_presence(status=discord.Status.invisible)
            przepros.start()
            return
        if "siat" in msg.content.lower():
            await msg.channel.send(file=discord.File("me.jpg"))
            return

    await random_event(msg, 0.02)
    await bot.process_commands(msg)

@bot.command()
async def test(ctx):
    await random_event(ctx.message, 1.0)

@tasks.loop(time=time(hour=3, minute=0, tzinfo=pytz.timezone("Europe/Warsaw")))
async def zucky_3am_reminder():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    await guild.members.fetch()

    online = []

    for member in guild.members:
        if member.bot:
            continue

        if member.status == discord.Status.online:
            online.append(member)
    for member in online:
        if random.randint(0, 10) >= 4:
            continue
        await member.send(
            "📷 Twoje zdjęcie:",
            file=discord.File("scary_zuck.png")
        )

###############################################

with open("token", "r") as file:
    token = file.read().strip()

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

async def main():
    async with bot:
        await bot.load_extension("vc")
        await bot.start(token)

import asyncio
asyncio.run(main())
