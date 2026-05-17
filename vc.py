import asyncio

import discord
from discord.ext import commands, tasks

import events
import vc_events

def get_all_active_vcs(bot: commands.Bot):
    return [
        vc for vc in bot.voice_clients
        if vc.is_connected()
    ]

@tasks.loop(seconds=240)
async def vc_event_loop(bot: commands.Bot):
    for vc in get_all_active_vcs(bot):
        if not vc or not vc.is_connected():
            continue

        ctx = {
            "type": "vc",
            "vc": vc,
            "guild": vc.guild,
        }

        await events.process_random_events(ctx)

async def setup(bot: commands.Bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None:
            return
    
        voice_client = member.guild.voice_client
        if not voice_client:
            return
    
        if voice_client.channel != before.channel:
            return
    
        if len(before.channel.members) == 1:
            await voice_client.disconnect()

    @bot.command()
    async def join(ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
    
    @bot.command()
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
