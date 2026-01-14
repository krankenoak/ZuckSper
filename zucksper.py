import discord
from discord.ext import commands, tasks

import random
import gifs
async def random_event(msg, chance): 
    if random.random() < chance:
        await msg.channel.send(random.choice(gifs.tenor_urls))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"DzZIASjgasdk {bot.user}")

bot_active = True

@bot.event
async def on_message(msg):
    global bot_active
    if msg.author.bot:
        return

    if not bot_active:
        if bot.user in msg.mentions and "do nogi" in msg.content.lower():
            bot_active = True
            await msg.add_reaction(discord.utils.get(bot.emojis, name="deep_hard_butt_sex_elf"));
            await bot.change_presence(status=discord.Status.online)
        return
    
    if bot.user in msg.mentions:
        if "cicho" in msg.content.lower():
            bot_active = False
            await msg.add_reaction(discord.utils.get(bot.emojis, name="brain1"))
            await bot.change_presence(status=discord.Status.invisible)
            return
        if "siat" in msg.content.lower():
            await msg.channel.send(file=discord.File("me.jpg"))
            return

    await random_event(msg, 0.02)
    await bot.process_commands(msg)

@bot.command()
async def test(ctx):
    await random_event(ctx.message, 1.0)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        play_audio_loop.start(ctx.voice_client)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@tasks.loop(seconds=120)
async def play_audio_loop(vc: discord.VoiceClient):
    if not vc.is_connected():
        play_audio_loop.stop()
        return
    if random.randint(1, 4) == 1:
        if not vc.is_playing():
            vc.play(discord.FFmpegPCMAudio("metal.mp3"))

with open("token", "r") as file:
    token = file.read().strip()
bot.run(token)
