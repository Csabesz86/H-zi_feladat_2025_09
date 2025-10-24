import os
import sys
from collections import defaultdict, Counter

LOG_FILE = "webstat.txt"

# betöltés
entries = []

if not os.path.isfile(LOG_FILE):
    print(f"Hiba: a '{LOG_FILE}' fájl nem található.")
    sys.exit(1)

with open(LOG_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 4:
            print(f"Figyelem: a következő sor nem a várt formátumban van: {line}")
            continue
        browser, date, ip, referer = parts
        entries.append({
            "browser": browser,
            "date": date,
            "ip": ip,
            "referer": referer,
        })


print("1. feladat:")
print(f"Napló sorainak száma: {len(entries)}\n")


print("2. feladat:")
# napi megszámlálás
day_counts = defaultdict(int)
for e in entries:
    day_counts[e["date"]] += 1

# rendezés dátum szerint
for day in sorted(day_counts.keys()):
    print(f"{day}\t{day_counts[day]}")
print()


print("3. feladat:")
browsers = sorted({e["browser"] for e in entries})
print(", ".join(browsers))
print()


print("4. feladat:")
chrome_entries = [e for e in entries if e["browser"].lower() == "chrome"]
total_chrome = len(chrome_entries)

if total_chrome > 0:
    honlap_cnt = sum(1 for e in chrome_entries if e["referer"] == "honlap")
    others_cnt = total_chrome - honlap_cnt
    honlap_pct = honlap_cnt / total_chrome * 100
    others_pct = others_cnt / total_chrome * 100
    print(f"Honlap referer: {honlap_pct:.1f}%")
    print(f"Másik forrás: {others_pct:.1f}%")
else:
    print("Nincs Chrome böngészőből származó adat.")
print()


print("5. feladat:")
# napi IP‑k megszámlálása
repeated_ips_per_day = defaultdict(set)

for day, group in defaultdict(list).items():  # csak a struktúra meghatározásához
    pass  # a szánalmat csak a következő sorban használjuk

# napi szerkesztés
ips_per_day = defaultdict(list)
for e in entries:
    ips_per_day[e["date"]].append(e["ip"])

for day, ips in ips_per_day.items():
    cnt = Counter(ips)
    repeated = [ip for ip, c in cnt.items() if c > 1]
    if repeated:
        repeated_ips_per_day[day] = set(repeated)

# kiírás
for day in sorted(repeated_ips_per_day.keys()):
    print(f"{day}: {', '.join(sorted(repeated_ips_per_day[day]))}")
print()


print("6. feladat:")
ip_query = input("Kérek egy IP-címet: ").strip()
if not ip_query:
    print("Nincs megadva IP.")
    sys.exit(0)

# első két bájt kinyerése
octets = ip_query.split('.')
if len(octets) < 2:
    print("Érvénytelen IP‑cím formátum.")
    sys.exit(1)

prefix = '.'.join(octets[:2])
output_file = ip_query.replace('.', '_') + ".txt"

with open(output_file, "w", encoding="utf-8") as outf:
    for e in entries:
        if e["ip"].startswith(prefix + '.'):
            outf.write(f"{e['date']}\t{e['ip']}\n")

print(f"Kimeneti fájl: {output_file}")