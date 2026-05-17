import asyncio
import random

import discord
from discord.ext import commands

import config
import events
import tasks

import astrology
import mood
import users
import vc

# DISCORD
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# DISCORD EVENTS
@bot.event
async def on_ready():
    config.logging.info(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        await users.update_guild_users(guild)

    tasks.periodic_update.start()
    await tasks.periodic_update()

    tasks.mood_decay.start()
    tasks.zucky_3am_reminder.start()
    vc.vc_event_loop.start(bot)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.author == bot.user:
        increase = random.randint(1, 10)
        config.STATE["mood"].inc(increase)
        config.logging.info(f"[MOOD+] +{increase}")

@bot.event
async def on_message(msg):
    ctx = {
        "type": "message",
        "msg": msg,
        "author_id": msg.author.id,
        "channel": msg.channel,
        "member": msg.author,
    }

    if msg.author.bot:
        config.LAST_BOT_MESSAGE[msg.channel.id] = msg
        return
    
    last_bot_msg = config.LAST_BOT_MESSAGE.get(msg.channel.id)
    if last_bot_msg:
        ctx["last_bot_msg"] = last_bot_msg
        await events.trigger_event("thanos_replace", ctx)
        config.LAST_BOT_MESSAGE.pop(msg.channel.id, None)

    if bot.user in msg.mentions:
        content = msg.content.lower()

        if "cicho" in content:
            config.STATE["active"] = False
            config.STATE["mood"].dec(50)
            await bot.change_presence(status=discord.Status.invisible)
            await msg.add_reaction(discord.utils.get(bot.emojis, name="brain1"))
            return

        if "siat" in content:
            await msg.channel.send(file=discord.File("me.jpg"))
            return

    await events.process_random_events(ctx)
    await bot.process_commands(msg)

# COMMANDS
@bot.command()
async def info(ctx):
    mood_obj = config.STATE["mood"]

    lines = []
    lines.append(
        f"Mood: "
        f"{mood_obj.get()} "
        f"{mood_obj.get_emoji()}"
        f""
    )

    lines.append(f"\nRANDOM EVENTS")
    for event in events.RANDOM_EVENTS:
        lines.append(
            f"{event['name']} :: "
            f"{events.apply_global_modifiers(event['base_chance']):.4f}"
        )

    lines.append(f"\nTRIGGER EVENTS")
    for name, event in events.TRIGGER_EVENTS.items():
        lines.append(
        f"{name} :: "
        f"{events.apply_global_modifiers(event['base_chance']):.4f}"
    )

    await ctx.send(
        "```" + "\n".join(lines) + "```"
    )

@bot.command()
async def users_modifiers(ctx):
    msg = users.print_chances(ctx.guild)
    await ctx.send(f"```\n{msg}\n```")

@bot.command()
async def my_sign(ctx):
    member = ctx.author
    sign = astrology.get_user_sign(member.created_at)
    horoscope = astrology.get_sign_horoscope(sign)

    await ctx.send(f"🌌 **Your zodiac sign:** {sign}\n")

@bot.command()
async def my_horoscope(ctx):
    member = ctx.author

    sign = astrology.get_user_sign(member.created_at)
    horoscope = astrology.get_sign_horoscope(sign)

    await ctx.send(
        f"🔮 Horoscope for **{member.display_name}**\n"
        f"🌌 Sign: **{sign}**\n\n"
        f"{horoscope['message']}\n"
        f"Cosmic modifier: `{horoscope['modifier']:.4f}`"
    )

@bot.command()
async def all_signs(ctx):
    lines = []

    for member in ctx.guild.members:
        sign = astrology.get_user_sign(member.created_at)
        lines.append(f"{member.display_name}: {sign}")

    output = "\n".join(lines)

    if len(output) > 1900:
        output = output[:1900] + "\n... (truncated)"

    await ctx.send("🌌 **Zodiac Signs of Members**\n```" + output + "```")

@bot.command()
async def all_horoscopes(ctx):
    lines = []

    for sign in astrology.sign_horoscopes.keys():
        horoscope = astrology.get_sign_horoscope(sign)
        lines.append(
            f"🌌 **{sign}**\n"
            f"{horoscope["message"]}\n"
            f"modifier: `{horoscope["modifier"]:.3f}`\n"
        )

    output = "\n".join(lines)
    if len(output) > 1900:
        output = output[:1900] + "\n... (truncated)"

    await ctx.send(output)

message = None

@bot.command()
async def test(ctx):
    global message
    file1 = discord.File("media/me.jpg")
    message = await ctx.channel.send("Here is the image:", file=file1)

@bot.command()
async def replace(ctx):
    global message
    file1 = discord.File("media/thanos_1.png")
    file2 = discord.File("media/thanos_2.png")
    await message.edit(content="", attachments=[file1])
    await ctx.channel.send(content="", file=file2)

# MAIN
async def main():
    async with bot:
        await bot.load_extension("vc")
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
