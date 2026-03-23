import random
class Mood:
    def __init__(self):
        self.value = random.randint(-100, 100)

    def get(self):
        return self.value

    def inc(self, amount):
        self.value += amount
        if self.value > 127:
            self.value = 127

    def dec(self, amount):
        self.value -= amount
        if self.value < -128:
            self.value = -128

    def get_emoji(self):
        v = self.value
        if v <= -128:
            return "💀"   # extremely bad
        elif v <= -100:
            return "😢"   # very sad
        elif v < -50:
            return "😞"   # sad
        elif v == 0:
            return "😐"   # neutral
        elif v < 1:
            return "🙂"   # slightly happy
        elif v < 50:
            return "😃"   # happy
        else:
            return "🤩"   # extremely happy

COMMON = 1
UNCOMMON = 2
RARE = 3
EPIC = 4
LEGENDARY = 5
MYTHIC = 6

BASE_RARITY = {
    COMMON: 0.50,
    UNCOMMON: 0.25,
    RARE: 0.15,
    EPIC: 0.07,
    LEGENDARY: 0.03,
    MYTHIC: 0.01
}

def apply_mood(weights, mood):
    factor = 1 + (mood / 1000.0)
    for r in weights:
        weights[r] = round(weights[r] * factor, 5)
    return weights

from datetime import datetime, timezone
from immanuel import charts

def astrology_new_chart():
    now = datetime.now(timezone.utc)
    latitude = 50.25
    longitude = 19.02
  
    subject = charts.Subject(
        date_time=now,
        latitude=latitude,
        longitude=longitude
    )

    natal = charts.Natal(subject)
    return natal


# def astrology_modifier(weights: Dict[Rarity, float], chart immanuel.chart)
     
