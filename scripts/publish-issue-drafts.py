#!/usr/bin/env python3
"""Publish the ordered issue drafts to the ContentPilot GitHub repository."""

import argparse
import json
import re
import subprocess
from pathlib import Path


REPOSITORY = "Basharkhan/contentpilot"
DRAFTS = Path(__file__).resolve().parents[1] / "docs" / "issue-drafts.md"
HEADING = re.compile(r"^## (\d{2}) — (.+)$", re.MULTILINE)


def run_gh(*args: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args], input=input_text, text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"gh failed with code {result.returncode}")
    return result.stdout.strip()


def drafts() -> list[tuple[str, str]]:
    content = DRAFTS.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(content))
    return [
        (
            f"[{match.group(1)}] {match.group(2)}",
            content[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(content)].strip(),
        )
        for index, match in enumerate(matches)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List titles without contacting GitHub")
    args = parser.parse_args()

    issues = drafts()
    if len(issues) != 14:
        raise SystemExit(f"Expected 14 issue drafts, found {len(issues)}")

    if args.dry_run:
        for title, _ in issues:
            print(title)
        return

    existing = {
        issue["title"]
        for issue in json.loads(
            run_gh("issue", "list", "--repo", REPOSITORY, "--state", "all", "--limit", "1000", "--json", "title")
        )
    }
    for title, body in issues:
        if title in existing:
            print(f"Already exists: {title}")
            continue
        url = run_gh(
            "issue", "create", "--repo", REPOSITORY, "--title", title, "--body-file", "-", input_text=body
        )
        print(f"Created: {url}")


if __name__ == "__main__":
    main()
