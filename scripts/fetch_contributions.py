"""Scrape the public contribution calendar (no token) -> data/contributions.json"""
import json, re, sys, datetime as dt
import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else "Shubhamx18"
r = requests.get(f"https://github.com/users/{USER}/contributions",
                 headers={"User-Agent": "Mozilla/5.0 profile-art"}, timeout=30)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

counts = {}
for tip in soup.find_all("tool-tip"):
    m = re.match(r"(\d+|No) contributions?", tip.get_text(strip=True))
    if m and tip.get("for"):
        counts[tip["for"]] = 0 if m.group(1) == "No" else int(m.group(1))

days = []
for td in soup.select("td.ContributionCalendar-day"):
    if not td.get("data-date"):
        continue
    days.append({"date": td["data-date"], "level": int(td.get("data-level", 0)),
                 "count": counts.get(td.get("id"), 0)})
days.sort(key=lambda d: d["date"])
if not days:
    sys.exit("no contribution cells found - GitHub markup may have changed")

total = sum(d["count"] for d in days)
longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
cur = 0
for d in reversed(days):
    if d["count"]:
        cur += 1
    elif d["date"] == dt.date.today().isoformat():
        continue              # today may still be empty
    else:
        break
best = max(days, key=lambda d: d["count"])
months = {}
for d in days:
    months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]

json.dump({"user": USER, "total": total, "current_streak": cur, "longest_streak": longest,
           "best_day": best, "months": months, "days": days},
          open("data/contributions.json", "w"), indent=1)
print(f"{USER}: {total} contributions, streak {cur}, longest {longest}")
