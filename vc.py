import discord
from discord.ext import commands, tasks
import random

import yt_dlp
import asyncio

YTDL_OPTIONS = {
    "format": "bestaudio",
    "quiet": True,
    "noplaylist": True,
    "no_warnings": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

def get_audio_url(url):
    info = ytdl.extract_info(url, download=False)
    return info["url"]

@tasks.loop(seconds=120)
async def play_audio_loop(vc: discord.VoiceClient):
    if not vc.is_connected():
        play_audio_loop.stop()
        return
    if random.random() < 0.02:
        if not vc.is_playing():
            vc.play(discord.FFmpegPCMAudio("metal.mp3"))

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
            play_audio_loop.start(ctx.voice_client)
    
    @bot.command()
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
    
    @bot.command()
    async def play(ctx, url: str):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        
        if ctx.voice_client.is_playing():
            return
        
        audio_url = await asyncio.to_thread(get_audio_url, url)
        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
