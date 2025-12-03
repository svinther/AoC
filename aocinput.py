#!/usr/bin/env python3

from pathlib import Path

from datetime import datetime
import requests
import typer


def getinput(year: int = None, day: int = None):
    year = year or datetime.today().year
    day = day or datetime.today().day

    path = Path(f"{day}.txt")
    sessionid = Path(".secret").read_text().strip()
    if sessionid.startswith("session="):
        sessionid = sessionid.split("=", 1)
    res = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": sessionid},
    )
    path.write_text(res.text)


if __name__ == "__main__":
    typer.run(getinput)
