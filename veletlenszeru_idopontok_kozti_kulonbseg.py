import random
import datetime

# véletlenszerű időgenerálás
def random_time() -> datetime.datetime:

    hour = random.randint(0, 23)      # 0‑23 óra
    minute = random.randint(0, 59)    # 0‑59 perc
    return datetime.datetime(2025, 1, 1, hour, minute)

def human_readable_delta(t1: datetime.datetime,
                         t2: datetime.datetime) -> str:

    delta: datetime.timedelta = abs(t2 - t1)

    total_seconds = delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60

    # formázott sztring
    return f"{int(hours)} óra {int(minutes)} perc"

# ----- példa futtatás -----
t1 = random_time()
t2 = random_time()

print(f"Első időpont: {t1.strftime('%H:%M')}")
print(f"Második időpont: {t2.strftime('%H:%M')}")
print(f"A két időpont közti eltérés: {human_readable_delta(t1, t2)}")