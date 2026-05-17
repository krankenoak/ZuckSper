import random

import config
import text_events
import vc_events
import users

import astrology

# RANDOM EVENTS
RANDOM_EVENTS = [
    {
        "name": "random_gif",
        "type": "message",
        "base_chance": 0.05,
        "func": text_events.event_random_gif,
    },
    {
        "name": "pipe",
        "type": "vc",
        "base_chance": 0.02,
        "func": vc_events.play_pipe
    },
]

# TRIGGERED EVENTS
TRIGGER_EVENTS = {
    "scary_zuck": {
        "base_chance": 0.333,
        "func": text_events.scary_zuck
    },
    "thanos_replace": {
        "base_chance": 0.04,
        "func": text_events.thanos_replace
    },
}

# EVENT PROCESSING
def apply_global_modifiers(base_chance):
    state = config.STATE
    chance = base_chance

    mood_value = state["mood"].get()
    chance *= 1 + (mood_value / 300)

    return chance

def apply_context_modifiers(ctx, chance):
    author_id = ctx.get("author_id")
    if author_id is None:
        return chance

    user = users.guild_users.get(author_id)
    if user is None:
        return chance

    chance *= user.get("chance_modifier", 1.0)
    return chance

def apply_astrology_modifier(ctx, chance):
    member = ctx.get("member")
    if not member:
        return chance

    sign = astrology.get_user_sign(member.created_at)
    horoscope = astrology.get_sign_horoscope(sign)

    chance *= (1 + horoscope["modifier"])
    config.logging.info(f"Applying astrological modifiers {horoscope['modifier']} ")

    return chance

async def compute_chance(event, ctx=None):
    chance = event["base_chance"]

    chance = apply_global_modifiers(chance)
    chance = apply_context_modifiers(ctx, chance)
    chance = apply_astrology_modifier(ctx, chance)

    if chance < 0.0:
        return 0.0
    if chance > 1.0:
        return 1.0

    return chance

async def process_random_events(ctx):
    if not config.STATE["active"]:
        return

    for event in RANDOM_EVENTS:
        if event["type"] != ctx["type"]:
            continue

        chance = await compute_chance(event, ctx)
        roll = random.random()

        config.logging.info(
            f"[EVENT] {event['name']} "
            f"chance={chance:.4f} "
            f"roll={roll:.4f}"
        )

        if roll >= chance:
            continue

        config.logging.info(
            f"[TRIGGER] {event['name']}"
        )

        try:
            await event["func"](ctx)
        except Exception as e:
            config.logging.exception(
                f"Random event failed: "
                f"{event['name']} :: {e}"
            )


async def trigger_event(name, ctx=None):
    event = TRIGGER_EVENTS.get(name)

    if event is None:
        config.logging.warning(f"[TRIGGER] Unknown event: {name}")
        return
    
    chance = await compute_chance(event, ctx)
    roll = random.random()

    config.logging.info(
        f"[TRIGGER] {name} "
        f"chance={chance:.4f} "
        f"roll={roll:.4f}"
    )

    if roll >= chance:
        return

    try:
        await event["func"](ctx)
    except Exception as e:
        config.logging.exception(
            f"Trigger event failed: "
            f"{name} :: {e}"
        )
