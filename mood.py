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
            return "💀"
        elif v <= -100:
            return "😢"
        elif v < -50:
            return "😞"
        elif v == 0:
            return "😐"
        elif v < 1:
            return "🙂"
        elif v < 50:
            return "😃"
        else:
            return "🤩"
