from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc


def working_window(tz, day, start, end):
    """Working hours on local date `day` in zone `tz`, as (start_utc, end_utc).

    Wall-clock arithmetic is used, so DST shifts on that date are respected.
    """
    midnight = datetime(day.year, day.month, day.day, tzinfo=tz)
    s = (midnight + timedelta(hours=start)).astimezone(UTC)
    e = (midnight + timedelta(hours=end)).astimezone(UTC)
    return s, e


def overlap_windows(zones, day, start=9, end=17):
    """UTC windows when every zone is within [start, end) local time.

    The window is anchored on `day` in the first zone; other zones may
    contribute their working day from the day before or after.
    Returns a list of (start_utc, end_utc) tuples.
    """
    if not 0 <= start < end <= 24:
        raise ValueError("need 0 <= start < end <= 24")
    tzs = [ZoneInfo(z) for z in zones]
    cur = [working_window(tzs[0], day, start, end)]
    for tz in tzs[1:]:
        cands = [working_window(tz, day + timedelta(days=d), start, end)
                 for d in (-1, 0, 1)]
        nxt = []
        for a, b in cur:
            for c, d in cands:
                lo, hi = max(a, c), min(b, d)
                if lo < hi:
                    nxt.append((lo, hi))
        cur = nxt
    return sorted(cur)
