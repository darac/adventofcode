# noqa: INP001
# Copyright (c) 2026 Paul Saunders
from datetime import UTC, datetime
from html import escape
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
GRID_X = 120
LABEL_GAP = 10
LABEL_X = GRID_X - LABEL_GAP
TOP_PAD = 30
DAYS_PER_ROW = 25

STYLESHEET = """
    <style>
        :root {
            --label: #59636e;
            --unsolved: #ebedf0;
            --one-star: #009900;
            --two-star: #999900;
            --today: #cf222e;

            --unsolved-text: #59636e;
            --one-star-text: #ffffff;
            --two-star-text: #24292f;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --label: #9198a1;
                --unsolved: #161b22;
                --one-star: #00cc00;
                --two-star: #ffff66;
                --today: #ff7b72;

                --unsolved-text: #9198a1;
                --one-star-text: #0d1117;
                --two-star-text: #0d1117;
            }
        }

        .label {
            fill: var(--label);
            font-family: "DejaVu Sans Mono", monospace;
            font-size: 13px;
        }

        .day {
            font-family: "DejaVu Sans Mono", monospace;
            font-size: 9px;
            text-anchor: middle;
            dominant-baseline: middle;
            pointer-events: none;
        }

        .unsolved { fill: var(--unsolved); }
        .one-star { fill: var(--one-star); }
        .two-star { fill: var(--two-star); }

        .unsolved-text { fill: var(--unsolved-text); }
        .one-star-text { fill: var(--one-star-text); }
        .two-star-text { fill: var(--two-star-text); }

        .today {
            stroke: var(--today);
            stroke-width: 2px;
        }
    </style>
"""


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


def get_days_in_year(year: int) -> int:
    return 25 if year < 2025 else 12


def get_days(year: int) -> list[int]:
    """Return the list of days for which we have solutions"""
    days = [0] * get_days_in_year(year)

    for day in range(1, len(days) + 1):
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


years = build_data()

width = GRID_X + (CELL + GAP) * DAYS_PER_ROW + 20
height = TOP_PAD + (CELL + GAP) * len(years) + 20


def svg_cell(
    x: int,
    y: int,
    state: int,
    year: int,
    day: int,
    today: bool = False,
) -> str:
    state_class = {
        0: "unsolved",
        1: "one-star",
        2: "two-star",
    }[state]

    text_class = {
        0: "unsolved-text",
        1: "one-star-text",
        2: "two-star-text",
    }[state]

    classes = state_class
    if today:
        classes += " today"

    status = {
        0: "Unsolved",
        1: "Part A solved",
        2: "Both parts solved",
    }[state]

    return (
        f'    <rect class="{classes}" '
        f'x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" rx="3">'
        f"\n        <title>{year} Day {day}: {status}</title>\n"
        "    </rect>\n"
        f'    <text class="day {text_class}" '
        f'x="{x + CELL / 2}" y="{y + CELL / 2}">{day}</text>'
    )


def svg_label(x: int, y: int, text: str) -> str:
    return (
        f'    <text class="label" x="{x}" y="{y}" '
        f'dominant-baseline="middle" text-anchor="end" '
        'xml:space="preserve">'
        f"{escape(text)}</text>"
    )


svg_elements = []
for row, ydata in enumerate(years):
    y = TOP_PAD + row * (CELL + GAP)
    is_current = ydata["year"] == CURRENT_YEAR

    svg_elements.append(
        svg_label(
            LABEL_X,
            y + CELL // 2,
            f"{ydata['year']}: ★ "
            f"{ydata['solved']:2d}/{len(ydata['days']) * 2}",
        )
    )

    for day, solved in enumerate(ydata["days"], start=1):
        x = GRID_X + (day - 1) * (CELL + GAP)

        is_today = ydata["year"] == CURRENT_YEAR and day == TODAY

        svg_elements.append(
            svg_cell(x, y, solved, ydata["year"], day, is_today)
        )

svf = f"""\
<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}" height="{height}"
    viewBox="0 0 {width} {height}">
{STYLESHEET}
{"\n".join(svg_elements)}
</svg>
"""
Path(IMG_PATH).write_text(svf, encoding="utf-8")

print(f"Saved {IMG_PATH} ({width}x{height})")
