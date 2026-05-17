import discord

import media
import config

async def event_random_gif(ctx):
    file_path = media.get_random_media_file()

    if file_path:
        await ctx["channel"].send(file=discord.File(file_path))

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
