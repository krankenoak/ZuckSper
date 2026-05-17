import discord

async def play_pipe(ctx):
    vc = ctx.get("vc")
    if vc is None:
        return

    if not vc.is_playing():
        vc.play(discord.FFmpegPCMAudio("media/pipe.mp3"))

