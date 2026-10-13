# tzmeet

Find the UTC time windows when every given time zone is within working hours.

Why: scheduling a meeting across zones is mental arithmetic made worse by DST
(US and Europe change clocks on different weeks). tzmeet uses the IANA tz
database via `zoneinfo`, evaluated on the date you give, so DST is handled.

## Install

Python 3.9+, standard library only (on systems without tz data, `pip install tzdata`).

    git clone <repo> && cd tzmeet
    python -m tzmeet --help

## Usage

    python -m tzmeet ZONE [ZONE ...] [--start H] [--end H] [--date YYYY-MM-DD] [--json]

Defaults: 9-17 local, today. Hours may be fractional (`--start 8.5`).
The date is the local date in the first zone; other zones may contribute their
working day from the adjacent date.

    $ python -m tzmeet America/New_York Europe/Berlin --date 2026-10-20
    2026-10-20 13:00 - 2026-10-20 15:00 UTC
      America/New_York       2026-10-20 09:00 - 2026-10-20 11:00
      Europe/Berlin          2026-10-20 15:00 - 2026-10-20 17:00

    $ python -m tzmeet America/New_York Europe/Berlin Asia/Tokyo --date 2026-10-20
    no overlap

`--json` prints `{"date": ..., "windows": [{"utc_start", "utc_end", "local": {zone: {start, end}}}]}`.

Exit codes: 0 overlap found, 1 no overlap, 2 bad timezone/date/hours.

## Tests

    pip install pytest && python -m pytest

## License

MIT
