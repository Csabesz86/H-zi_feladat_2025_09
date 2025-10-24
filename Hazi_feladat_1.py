import sys

FILENAME = "kiserlet.txt"   # a feladatban megadott állomány

def main():
    total_dobs = 0          # összes dobás
    heads = 0               # fej szám
    exact_pair_of_heads = 0

    current_head_run = 0

    with open(FILENAME, "r") as f:
        for block in iter(lambda: f.read(8192), ""):
            for ch in block:
                if ch not in ("F", "I"):
                    continue

                total_dobs += 1

                if ch == "F":
                    heads += 1
                    current_head_run += 1
                else:  # ch == "I"
                    if current_head_run == 2:
                        exact_pair_of_heads += 1
                    current_head_run = 0


    if current_head_run == 2:
        exact_pair_of_heads += 1

    if total_dobs > 0:
        percent_heads = (heads / total_dobs) * 100
    else:
        percent_heads = 0.0

    # Eredmények kiírása
    print(total_dobs)
    print(f"{percent_heads:.2f}")
    print(exact_pair_of_heads)


if __name__ == "__main__":
    main()