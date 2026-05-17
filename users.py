import random

import discord

import config

guild_users = {}

async def get_user_creation_date(ctx):
    author_id = ctx.get("author_id")
    channel = ctx.get("channel")

    if author_id is None or channel is None:
        return None

    guild = getattr(channel, "guild", None)
    if guild:
        member = guild.get_member(author_id)
        if member:
            return member.created_at

    return None

async def update_guild_users(guild: discord.Guild):
    guild_data = {}

    async for member in guild.fetch_members(limit=None):
        guild_data[member.id] = {
            "name": member.name,
            "display_name": member.display_name,
            "id": member.id,
            "chance_modifier": 1.0
        }

    guild_users[guild.id] = guild_data

def get_guild_users(guild: discord.Guild):
    return guild_users.get(guild.id, {})

def change_chance_modifiers():
    for guild_id, users in guild_users.items():
        for user_id, user_data in users.items():
            if user_id == config.HAU_ID:
                user_data["chance_modifier"] = 1.3
            else:
                user_data["chance_modifier"] = random.uniform(0.9, 1.1)

def print_chances(guild: discord.Guild):
    users = guild_users.get(guild.id, {})

    msg = f"Current chance modifiers ({guild.name}):\n"
    for user in users.values():
        msg += f"{user['display_name']}: {user['chance_modifier']:.4f}\n"

    return msg
