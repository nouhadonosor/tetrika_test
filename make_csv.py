import csv, random, string


ROWS = 10000


def make_random_ints(vocabulary_magnitude=100):
    while True:
        yield random.choice(range(vocabulary_magnitude))


def make_random_strs(str_len=7, str_count=5, separator=" "):
    rand_str = lambda: "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase)
        for i in range(str_len)
    )
    while True:
        yield separator.join(rand_str() for _ in range(str_count))


id_generator = make_random_ints(10)
title_generator = make_random_strs(str_count=3)
body_generator = make_random_strs(str_count=20, str_len=10)

row_generator = zip(id_generator, title_generator, body_generator)

with open("example.csv", "w", newline="") as file:
    writer = csv.writer(file, dialect="excel")
    writer.writerow(["userId", "title", "body"])
    for i in range(ROWS):
        print(f"Progress {i+1}/{ROWS}", end="\r")
        row = next(row_generator)
        writer.writerow(row)
    print("\nDone")
