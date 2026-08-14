from datetime import UTC, datetime  # noqa: INP001
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent / "src" / "aoc"
if not BASE_DIR.is_dir():
    print(f"Error: {BASE_DIR} does not exist or is not a directory.")
    exit(1)
START_YEAR = 2015

NOW = datetime.now(UTC)
CURRENT_YEAR = NOW.year
TODAY = NOW.day if NOW.month == 12 else None

IMG_PATH = Path(__file__).parent / "aoc_progress.svg"

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
    """Return the list of days for which we have solutions"""
    days = [0] * 25

    for day in range(1, 26):
        test_file = (
            BASE_DIR.parent.parent
            / "tests"
            / f"year{year}"
            / f"day{day:02}.yml"
        )

        if not test_file.is_file():
            continue

        solved = 0

        with test_file.open() as fh:
            for doc in yaml.safe_load_all(fh):
                if not isinstance(doc, dict):
                    continue

                if doc.get("b") is not None:
                    solved = 2
                    break

                if doc.get("a") is not None:
                    solved = 1

        days[day - 1] = solved

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
                    "solved": total,
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
        0: (22, 27, 34),
        1: (0, 153, 0),
        2: (255, 255, 102),
    }


years = build_data()

width = LEFT_PAD + (CELL + GAP) * 25 + 20
height = TOP_PAD + (CELL + GAP) * len(years) + 20


def svg_cell(x: int, y: int, state: int) -> str:
    classes = {
        0: "unsolved",
        1: "one-star",
        2: "two-star",
    }

    return (
        f'<rect class="{classes[state]}" '
        f'x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" rx="3" />'
    )


def svg_label(x: int, y: int, text: str) -> str:
    return (
        f'<text class="label" x="{x}" y="{y}" '
        f'dominant-baseline="middle" text-anchor="start">'
        f"{text}</text>"
    )


STYLESHEET = """
    <style>
        .label    {
            fill: #24292f;
            font-family: DejaVu Sans Mono, monospace;
            font-size: 13px;
        }
        .unsolved { fill: #ebedf0 }
        .one-star { fill: #009900 }
        .two-star { fill: #999900 }

        @media (prefers-color-scheme: dark) {
            .label    {
                fill: #24292f;
                font-family: DejaVu Sans Mono, monospace;
                font-size: 13px;
            }
            .unsolved { fill: #161b22 }
            .one-star { fill: #00cc00 }
            .two-star { fill: #ffff66 }
        }
    </style>
"""

svg_elements = []
for row, ydata in enumerate(years):
    y = TOP_PAD + row * (CELL + GAP)
    is_current = ydata["year"] == CURRENT_YEAR

    svg_elements.append(
        svg_label(
            10, y + CELL // 2, f"{ydata['year']}: ★ {ydata['solved']}"
        )
    )

    for day, solved in enumerate(ydata["days"]):
        x = LEFT_PAD + day * (CELL + GAP)
        svg_elements.append(svg_cell(x, y, solved))

svf = f"""\
<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}"
    viewBox="0 0 {width} {height}">
{STYLESHEET}
    {"\n    ".join(svg_elements)}
</svg>
"""
Path(IMG_PATH).write_text(svf, encoding="utf-8")

print(f"Saved {IMG_PATH} ({width}x{height})")
