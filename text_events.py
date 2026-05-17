import discord
import random

import media
import config

async def event_random_gif(ctx):
    file_path = media.get_random_media_file()

    if file_path:
        await ctx["channel"].send(file=discord.File(file_path))

async def event_random_reaction(ctx):
    msg = ctx.get("msg")
    if not msg:
        return

    server_emojis = list(msg.guild.emojis) if msg.guild else []

    unicode_ranges = [(0x1F600, 0x1F64F),]
    unicode_emojis = []
    for start, end in unicode_ranges:
        for codepoint in range(start, end + 1):
            try:
                unicode_emojis.append(chr(codepoint))
            except:
                continue

    use_server_emoji = random.choice([True, False])
    if use_server_emoji and server_emojis:
        chosen_emoji = random.choice(server_emojis)
    else:
        chosen_emoji = random.choice(unicode_emojis)

    await msg.add_reaction(chosen_emoji)

async def thanos_replace(ctx):
    global message
    file1 = discord.File("media/thanos_1.png")
    file2 = discord.File("media/thanos_2.png")
    await ctx["last_bot_msg"].edit(content="", attachments=[file1])
    await ctx["channel"].send(content="", file=file2)

async def scary_zuck(ctx):
    member = ctx.get("member")
    if member is None:
        return
    await member.send(discord.File("media/scary_zuck.png"))
