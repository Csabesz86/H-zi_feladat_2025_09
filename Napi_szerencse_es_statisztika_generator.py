
import random
import math
import datetime
import statistics

def is_prime(n: int) -> bool:
    """Egyszerű primalitás‑ellenőrzés – csak pozitív egész számokra."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    # 1 Dátum‑információk
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    day_name = today.strftime("%A")
    day_of_year = today.timetuple().tm_yday

    print(f"Mai dátum: {date_str}")
    print(f"Hét napja: {day_name}")
    print(f"Év hányadik napja: {day_of_year}\n")

    # 2 10 véletlen szám 1–100 között
    numbers = [random.randint(1, 100) for _ in range(10)]
    print("Generált számok:", numbers)

    # 3 Szerencseszám kiválasztása
    lucky = random.choice(numbers)
    print(f"Szerencseszám: {lucky}")

    # 4 Statisztikai elemzés
    avg = statistics.mean(numbers)
    std_dev = statistics.stdev(numbers)
    maximum = max(numbers)
    minimum = min(numbers)
    total = sum(numbers)
    sqrt_total = math.sqrt(total)

    print("\nStatisztikai elemzés:")
    print(f"Átlag: {avg:.2f}")
    print(f"Szórás: {std_dev:.2f}")
    print(f"Maximum: {maximum}")
    print(f"Minimum: {minimum}")
    print(f"Összeg gyöke: {sqrt_total:.2f}")

    # 5 Prímszám‑ellenőrzés a szerencseszámra
    if is_prime(lucky):
        print("\nÜdv! Ez a szerencseszámod! 🎉")
    else:
        print("\nSzerencsétlen vagy!")

if __name__ == "__main__":
    main()