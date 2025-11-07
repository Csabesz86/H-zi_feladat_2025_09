import os
import sys
import random
import datetime
from typing import Dict, Any


def generate_random_data(
        filename: str,
        start: datetime.date = datetime.date(2024, 10, 1),
        end: datetime.date = datetime.date(2025, 11, 30),
) -> None:

    weather_options = ["szeles", "napos", "esős", "ködös", "semmilyen"]

    delta = datetime.timedelta(days=1)
    cur = start

    with open(filename, "w", encoding="utf-8") as fp:
        while cur <= end:
            temp = round(random.uniform(0, 20), 1)
            fp.write(f"Dátum: {cur}\n")
            fp.write(f"Időjárás: {random.choice(weather_options)}\n")
            fp.write(f"Hőmérséklet: {temp}C\n")
            fp.write(f"Várható eső: {random.randint(0, 100)}%\n")
            cur += delta


def load_data(filename: str) -> Dict[str, Dict[str, Any]]:

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Fájl nem található: {filename}")

    data: Dict[str, Dict[str, Any]] = {}
    with open(filename, encoding="utf-8") as fp:
        current_date = None
        for line in fp:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Dátum:"):
                current_date = line.split("Dátum:")[1].strip()
                data[current_date] = {}
                continue

            if current_date is None:
                raise ValueError("Hibás fájlformátum – „Dátum:” előtt más mező van")

            if line.startswith("Időjárás:"):
                data[current_date]["Időjárás"] = line.split("Időjárás:")[1].strip()
                continue

            if line.startswith("Hőmérséklet:"):
                temp_text = line.split("Hőmérséklet:")[1].strip()
                if temp_text.endswith("C"):
                    temp_text = temp_text[:-1]
                data[current_date]["Hőmérséklet"] = float(temp_text)
                continue

            if line.startswith("Várható eső:"):
                rain_text = line.split("Várható eső:")[1].strip()
                if rain_text.endswith("%"):
                    rain_text = rain_text[:-1]
                data[current_date]["Várható eső"] = int(rain_text)
                continue

            key, _, val = line.partition(":")
            data[current_date][key.strip()] = val.strip()

    return data


def print_daily_report(data: Dict[str, Dict[str, Any]], date: datetime.date) -> None:

    key = date.isoformat()
    if key not in data:
        print(f"Adat nem található a(z) {key} napra.")
        return

    rec = data[key]
    print(f"\nNapi jelentés – {key}")
    print(f"  Időjárás: {rec['Időjárás']}")
    print(f"  Hőmérséklet: {rec['Hőmérséklet']:.1f} °C")
    print(f"  Várható eső: {rec['Várható eső']}%")


def print_monthly_report(data: Dict[str, Dict[str, Any]], year: int, month: int) -> None:

    start = datetime.date(year, month, 1)
    if month == 12:
        end = datetime.date(year, 12, 31)
    else:
        end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    temps = []
    rain_days = 0
    no_weather = 0

    for key in data:
        if start <= datetime.date.fromisoformat(key) <= end:
            rec = data[key]
            temps.append(rec["Hőmérséklet"])
            if rec["Várható eső"] > 0:
                rain_days += 1
            if rec["Időjárás"] == "semmilyen":
                no_weather += 1

    if not temps:
        print(f"Nem található adat a(z) {year}-{month:02d} hónapra.")
        return

    avg_temp = sum(temps) / len(temps)
    max_temp = max(temps)
    print(f"\nHavi összegzés – {year}-{month:02d}")
    print(f"  Átlaghőmérséklet: {avg_temp:.1f} °C")
    print(f"  Maximális hőmérséklet: {max_temp:.1f} °C")
    print(f"  Esős napok: {rain_days}")
    print(f"  Semmilyen napok: {no_weather}")


def print_interval_report(
        data: Dict[str, Dict[str, Any]],
        start: datetime.date,
        end: datetime.date,
) -> None:

    if start > end:
        start, end = end, start

    temps = []
    rain_days = 0
    no_weather = 0

    for key in data:
        d = datetime.date.fromisoformat(key)
        if start <= d <= end:
            rec = data[key]
            temps.append(rec["Hőmérséklet"])
            if rec["Várható eső"] > 0:
                rain_days += 1
            if rec["Időjárás"] == "semmilyen":
                no_weather += 1

    if not temps:
        print(f"Nem található adat a(z) {start}–{end} időszakra.")
        return

    avg_temp = sum(temps) / len(temps)
    max_temp = max(temps)
    print(f"\nIdőszak – {start} – {end}")
    print(f"  Átlaghőmérséklet: {avg_temp:.1f} °C")
    print(f"  Maximális hőmérséklet: {max_temp:.1f} °C")
    print(f"  Esős napok: {rain_days}")
    print(f"  Semmilyen napok: {no_weather}")


def menu_loop(data: Dict[str, Dict[str, Any]]) -> None:
    while True:
        print("\n--- Menü ---")
        print("1. Adott napi / havi jelentés")
        print("2. Két időpont közötti adatok")
        print("3. Kilépés (q / quit / end)")

        choice = input("Választás: ").strip().lower()
        if choice == "1":
            t = input("Nap (nap) vagy hónap (hónap)? ").strip().lower()
            if t == "nap":
                try:
                    d = datetime.datetime.strptime(
                        input("Dátum (YYYY-MM-DD): ").strip(), "%Y-%m-%d"
                    ).date()
                except ValueError:
                    print("Érvénytelen dátumformátum.")
                    continue
                print_daily_report(data, d)
            elif t == "hónap":
                try:
                    year, month = map(int, input("Hónap (YYYY-MM): ").split("-"))
                except ValueError:
                    print("Érvénytelen hónapformátum.")
                    continue
                print_monthly_report(data, year, month)
            else:
                print("Érvénytelen opció.")
        elif choice == "2":
            try:
                start = datetime.datetime.strptime(
                    input("Kezdő dátum (YYYY-MM-DD): ").strip(), "%Y-%m-%d"
                ).date()
                end = datetime.datetime.strptime(
                    input("Záró dátum (YYYY-MM-DD): ").strip(), "%Y-%m-%d"
                ).date()
            except ValueError:
                print("Érvénytelen dátumformátum.")
                continue
            print_interval_report(data, start, end)
        elif choice in ("3", "q", "quit", "end"):
            print("Viszlát!")
            break
        else:
            print("Ismeretlen választás, kérlek újra próbáld.")


def main() -> None:
    filename = "weather_data.txt"

    if not os.path.exists(filename):
        load_start = datetime.date(2024, 1, 1)
        load_end = datetime.date(2025, 12, 31)
        print(
            f"Fájl létrehozása: {filename} "
            f"({load_start.isoformat()} – {load_end.isoformat()})"
        )
        generate_random_data(filename, load_start, load_end)

    data = load_data(filename)
    menu_loop(data)


if __name__ == "__main__":
    main()