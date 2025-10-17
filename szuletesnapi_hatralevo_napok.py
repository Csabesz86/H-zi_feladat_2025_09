import datetime
import sys

def current_date() -> datetime.date:
    """Visszaadja a mai nap dátumát."""
    return datetime.date.today()

def parse_month_day(user_input: str) -> tuple[int, int]:

    try:
        month_str, day_str = user_input.strip().split()
        month = int(month_str)
        day = int(day_str)
    except ValueError:
        raise ValueError("Kérjük, ad meg a hónapot és a napot, szóközzel elválasztva: például '12 25'")

    if not (1 <= month <= 12):
        raise ValueError("A hónap 1 és 12 között kell, hogy legyen.")
    if not (1 <= day <= 31):
        raise ValueError("A nap 1 és 31 között kell, hogy legyen.")

    return month, day

def next_birthday(month: int, day: int, today: datetime.date) -> datetime.date:

    # Alapértelmezett év: a mai év
    year = today.year
    try:
        birthday_this_year = datetime.date(year, month, day)
    except ValueError:
        # Például 2/29, amely nem minden évben létezik
        # Ebben az esetben a következő létező napra (pl. 3/1) álljunk
        if month == 2 and day == 29:
            # Ha a mai év nem szökőév, állítsuk a 3/1-gyel
            birthday_this_year = datetime.date(year, 3, 1)
        else:
            raise

    if birthday_this_year < today or birthday_this_year == today:
        # már elmúlt a születésnap a mai évben, tehát a következő évben
        year += 1
        try:
            return datetime.date(year, month, day)
        except ValueError:
            # ugyanező 2/29 esetén 3/1
            if month == 2 and day == 29:
                return datetime.date(year, 3, 1)
            raise

    return birthday_this_year

def days_until_next_birthday(birthday: datetime.date, today: datetime.date) -> int:
    """
    Visszaadja a mai nap és a következő születésnap közötti napok számát.
    """
    delta = birthday - today
    return delta.days

def main() -> None:
    today = current_date()
    print(f"Ma: {today.strftime('%Y-%m-%d')}")

    user_input = input("Add meg a születésnapod (hónap nap), pl. '12 25': ")
    try:
        month, day = parse_month_day(user_input)
    except ValueError as e:
        print(f"Hiba: {e}")
        sys.exit(1)

    try:
        next_bday = next_birthday(month, day, today)
    except ValueError as e:
        print(f"Hiba: {e}")
        sys.exit(1)

    days_left = days_until_next_birthday(next_bday, today)

    if days_left == 0:
        print("Ma van a születésnapod! 🎉")
    else:
        print(f"Ön {next_bday.strftime('%Y-%m-%d')} van születésnapja. "
              f"Ennyi nap van hátra: {days_left}")

if __name__ == "__main__":
    main()