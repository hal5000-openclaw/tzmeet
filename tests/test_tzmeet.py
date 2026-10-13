import json
from datetime import date

import pytest

from tzmeet.cli import main
from tzmeet.core import overlap_windows


def test_ny_berlin_summer():
    w = overlap_windows(["America/New_York", "Europe/Berlin"], date(2026, 10, 20))
    assert [(a.hour, b.hour) for a, b in w] == [(13, 15)]


def test_dst_gap_differs():
    # 2026-10-28: US still on DST, Europe back to standard time
    w = overlap_windows(["America/New_York", "Europe/Berlin"], date(2026, 10, 28))
    assert [(a.hour, b.hour) for a, b in w] == [(13, 16)]


def test_no_overlap(capsys):
    rc = main(["America/New_York", "Asia/Tokyo", "Europe/Berlin", "--date", "2026-10-20"])
    assert rc == 1
    assert capsys.readouterr().out.strip() == "no overlap"


def test_bad_zone(capsys):
    assert main(["Mars/Base"]) == 2


def test_json(capsys):
    rc = main(["UTC", "Europe/London", "--date", "2026-01-15", "--json"])
    data = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert data["windows"][0]["utc_start"] == "2026-01-15 09:00"


def test_bad_hours():
    assert main(["UTC", "--start", "17", "--end", "9"]) == 2
