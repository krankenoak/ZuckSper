import discord
from discord.ext import commands, tasks

import random
from datetime import time
import pytz

import vc
import gifs_local
import mood

hau_id = 577560664730501140

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot_active = True
bot_mood = mood.Mood()
bot_weights = mood.apply_mood(mood.BASE_RARITY, bot_mood.get())
bot_chart = mood.astrology_new_chart()

zuckprosiny_id = 1462139529480638699
me_file = discord.File("me.jpg")
scary_file = discord.File("scary_zuck.png")

async def random_event(msg, rarity): 
    chance = bot_weights[rarity]

    if msg.author.id == hau_id:
        chance *= 1.1
        if chance > 1.0:  # cap at 100%
            chance = 1.0

    if random.random() < chance:
        file_path = gifs_local.get_random_media_file()
        if file_path:
            await msg.channel.send(file=discord.File(file_path))

async def send_dm(user_id: int, text: str):
    user = await bot.fetch_user(user_id)
    await user.send(text)

@tasks.loop(seconds=5)
async def przepros():
    if bot_active:
        przepros.stop()
        return
    await bot.get_channel(zuckprosiny_id).send("przepraszam 🥺, znalazłeś backdoora... witam, jestem tutaj, w czym mogę pomóc?")

@bot.event
async def on_ready():
    print(f"DzZIASjgasdk {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.author == bot.user:
        bot_mood.inc(random.randint(1, 10))

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
            await msg.channel.send(me_file)
            bot_active = True
            await msg.add_reaction(discord.utils.get(bot.emojis, name="deep_hard_butt_sux_elf"));
            await bot.change_presence(status=discord.Status.online)
        return
    
    if bot.user in msg.mentions:
        if "cicho" in msg.content.lower():
            bot_active = False
            await msg.add_reaction(discord.utils.get(bot.emojis, name="brain1"))
            await bot.change_presence(status=discord.Status.invisible)
            bot_mood.dec(-999)
            przepros.start()
            return
        if "siat" in msg.content.lower():
            await msg.channel.send(file=discord.File("me.jpg"))
            return
        if "czy to prawda" in msg.content.lower() or "is it true" in msg.content.lower():
            odpowiedz = random.choice(["tak", "nie"])
            await msg.reply(odpowiedz)
            return
    await random_event(msg, mood.RARE)
    await bot.process_commands(msg)

@bot.command()
async def test(ctx):
    await random_event(ctx.message, mood.COMMON)

@bot.command()
async def info(ctx):
    weights_str = "\n".join(f"({v})" for v in bot_weights.items())
    response = (
        f"{bot_mood.get_emoji()} ({bot_mood.get()})\n"
        f"{weights_str}\n"
    )
    await ctx.send(response)

@tasks.loop(hours=1)
async def change_chart():
    bot_mood.value = random.randint(-128, 127)
    bot_weights = mood.apply_mood(mood.BASE_RARITY, bot_mood.get())
    bot_chart = astrology_new_chart()


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
            file=discord.File(scary_file)
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
