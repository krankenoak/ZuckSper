import datetime
import random

# Planet	    Astrological Significance
# Sun	        Core identity, ego, willpower, vitality. Where you shine.
# Moon	        Emotions, instincts, habits, subconscious. Inner world.
# Mercury	    Communication, intellect, thinking style, learning.
# Venus	        Love, relationships, values, aesthetics, pleasure.
# Mars	        Drive, energy, ambition, aggression, sexual energy.
# Jupiter	    Expansion, luck, growth, optimism, learning.
# Saturn	    Discipline, challenges, responsibility, structure.
# Uranus	    Innovation, sudden change, rebellion, individuality.
# Neptune	    Dreams, intuition, illusions, spirituality, creativity.
# Pluto	        Transformation, power, regeneration, hidden forces.

ZODIAC_SIGNS = [
    ("Koziorożec",   (12, 22), (1, 19)),
    ("Wodnik",       (1, 20),  (2, 18)),
    ("Ryby",         (2, 19),  (3, 20)),
    ("Baran",        (3, 21),  (4, 19)),
    ("Byk",          (4, 20),  (5, 20)),
    ("Bliźnięta",    (5, 21),  (6, 20)),
    ("Rak",          (6, 21),  (7, 22)),
    ("Lew",          (7, 23),  (8, 22)),
    ("Panna",        (8, 23),  (9, 22)),
    ("Waga",         (9, 23),  (10, 22)),
    ("Skorpion",     (10, 23), (11, 21)),
    ("Strzelec",     (11, 22), (12, 21)),
]

sign_horoscopes = {}
CURRENT_DAY = None

def generate_daily_horoscopes():
    global sign_horoscopes, CURRENT_DAY
    today = datetime.date.today()
    
    if CURRENT_DAY == today:
        return
    
    CURRENT_DAY = today
    sign_horoscopes = {}
    
    for sign, _, _ in ZODIAC_SIGNS:
        seed = f"{sign}-{today.isoformat()}"
        rng = random.Random(seed)
    
        modifier = rng.uniform(-0.3, 0.3)
    
        if modifier < -0.15:
            messages = [
                "Cosmic alignment strongly favors your sign.",
                "Energy flows effortlessly today.",
                "A powerful surge of positive fate surrounds you."
            ]
        elif modifier < 0:
            messages = [
                "Stable cosmic flow supports your actions.",
                "Small opportunities may emerge today.",
                "Balanced energies guide your path."
            ]
        elif modifier < 0.15:
            messages = [
                "Cosmic instability may slow progress.",
                "Proceed with patience today.",
                "Energy feels slightly blocked."
            ]
        else:
            messages = [
                "Chaotic cosmic forces dominate your sign.",
                "Expect turbulence in decisions today.",
                "Fate feels unusually unpredictable."
            ]
    
        sign_horoscopes[sign] = {
            "modifier": modifier,
            "message": rng.choice(messages)
        }

def get_sign_horoscope(sign: str) -> dict:
    return sign_horoscopes.get(sign, {"modifier": 0.0, "message": "Cosmic silence surrounds your sign."})

def get_user_sign(user_creation_date: datetime.datetime) -> str:
    month = user_creation_date.month
    day = user_creation_date.day

    for sign, (start_month, start_day), (end_month, end_day) in ZODIAC_SIGNS:
        if start_month == end_month:
            if month == start_month and start_day <= day <= end_day:
                return sign
        else:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return sign
    return "Koziorożec"

def get_astrology_modifier(user_creation_date: datetime.datetime) -> float:
    sign = get_user_sign(user_creation_date)
    horoscope = get_sign_horoscope(sign)
    return horoscope["modifier"]
