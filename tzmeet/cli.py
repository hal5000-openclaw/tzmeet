import argparse
import json
import sys
from datetime import date, datetime
from zoneinfo import ZoneInfo

from .core import UTC, overlap_windows


def _fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


def _hour(s):
    v = float(s)
    return int(v) if v == int(v) else v


def build_parser():
    p = argparse.ArgumentParser(
        prog="tzmeet",
        description="Find UTC windows when all time zones are in working hours.")
    p.add_argument("zones", nargs="+", help="IANA zones, e.g. Europe/Berlin")
    p.add_argument("--start", type=_hour, default=9, help="start hour (default 9)")
    p.add_argument("--end", type=_hour, default=17, help="end hour (default 17)")
    p.add_argument("--date", default=None,
                   help="YYYY-MM-DD, anchored on the first zone (default today)")
    p.add_argument("--json", action="store_true", help="JSON output")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        day = date.fromisoformat(args.date) if args.date else date.today()
    except ValueError:
        print("tzmeet: bad date %r (use YYYY-MM-DD)" % args.date, file=sys.stderr)
        return 2
    for z in args.zones:
        try:
            ZoneInfo(z)
        except Exception:
            print("tzmeet: unknown timezone %r" % z, file=sys.stderr)
            return 2
    try:
        wins = overlap_windows(args.zones, day, args.start, args.end)
    except ValueError as e:
        print("tzmeet: %s" % e, file=sys.stderr)
        return 2

    out = []
    for s, e in wins:
        out.append({
            "utc_start": _fmt(s), "utc_end": _fmt(e),
            "local": {z: {"start": _fmt(s.astimezone(ZoneInfo(z))),
                          "end": _fmt(e.astimezone(ZoneInfo(z)))}
                      for z in args.zones}})
    if args.json:
        print(json.dumps({"date": day.isoformat(), "windows": out}, indent=2))
    elif not out:
        print("no overlap")
    else:
        for w in out:
            print("%s - %s UTC" % (w["utc_start"], w["utc_end"]))
            for z, l in w["local"].items():
                print("  %-22s %s - %s" % (z, l["start"], l["end"]))
    return 0 if out else 1
