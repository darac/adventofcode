from datetime import UTC, datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).parent.parent / "src" / "aoc"
if not BASE_DIR.is_dir():
    print(f"Error: {BASE_DIR} does not exist or is not a directory.")
    exit(1)
START_YEAR = 2015

NOW = datetime.now(UTC)
CURRENT_YEAR = NOW.year
TODAY = NOW.day if NOW.month == 12 else None

IMG_PATH = Path(__file__).parent / "aoc_progress.png"

CELL = 18
GAP = 4
LEFT_PAD = 70
TOP_PAD = 30


def get_years() -> list[int]:
    years = []
    for year_dir in BASE_DIR.iterdir():
        if (
            year_dir.is_dir()
            and year_dir.name.startswith("year")
            and len(year_dir.name) == 8
        ):
            print(f"Found year directory: {year_dir.name}")
            year = year_dir.name[4:]
            years.append(int(year))
    return sorted(years, reverse=True)


def get_days(year: int) -> list[int]:
    year_dir = BASE_DIR / f"year{year}"
    days = [0] * 25

    if not year_dir.is_dir():
        return days

    for d in range(1, 26):
        day_file = year_dir / f"day{d:02}.py"
        if not day_file.is_file():
            continue

        days[d - 1] = 1  # file exists → at least started

    return days


def build_data() -> list[dict]:
    data = []

    for year in get_years():
        days = get_days(year)
        total = sum(days)

        if total > 0:
            data.append(
                {
                    "year": year,
                    "stars": total,
                    "days": days,
                }
            )

    return data


def colors(is_current: bool) -> dict[int, tuple[int, int, int]]:
    if is_current:
        return {
            0: (235, 237, 240),
            1: (155, 233, 168),
            2: (33, 110, 57),
        }
    return {
        0: (245, 245, 245),
        1: (210, 210, 210),
        2: (160, 160, 160),
    }


years = build_data()

width = LEFT_PAD + (CELL + GAP) * 25 + 20
height = TOP_PAD + (CELL + GAP) * len(years) + 20

img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

for row, ydata in enumerate(years):
    year = ydata["year"]
    days = ydata["days"]
    total = ydata["stars"]

    y = TOP_PAD + row * (CELL + GAP)
    is_current = year == CURRENT_YEAR

    palette = colors(is_current)

    label = f"{year}  * {total}"
    draw.text((10, y + 2), label, fill=(0, 0, 0), font=font)

    for i, stars in enumerate(days):
        x = LEFT_PAD + i * (CELL + GAP)
        fill = palette[stars]

        draw.rectangle([x, y, x + CELL, y + CELL], fill=fill)

        if is_current and TODAY and (i + 1) == TODAY:
            draw.rectangle(
                [x - 2, y - 2, x + CELL + 2, y + CELL + 2],
                outline=(255, 0, 0),
                width=2,
            )

img.save(IMG_PATH)
print(f"Saved {IMG_PATH} ({width}x{height})")
