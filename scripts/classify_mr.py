#!/usr/bin/env python3
"""
classify merged PRs from NVIDIA/Model-Optimizer by directory tags.

workflow:
  1. load directory-to-tag mapping from config/directory_tags.json
  2. fetch merged PRs from GitHub API since last processed date
  3. classify each PR based on changed files (longest-prefix match)
  4. prepend new entries to README.md changelog table
  5. persist state in data/state.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

MAX_RETRIES = 3
RETRY_BASE_DELAY = 5  # seconds

GITHUB_API = "https://api.github.com"

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = ROOT_DIR / "config" / "directory_tags.json"
STATE_PATH = ROOT_DIR / "data" / "state.json"
README_PATH = ROOT_DIR / "README.md"


# ---------------------------------------------------------------------------
# github api helpers
# ---------------------------------------------------------------------------

def github_get(url, params=None):
    """make a GET request to the GitHub REST API with retry on rate limit."""
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{url}?{query}"
    else:
        full_url = url

    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    for attempt in range(MAX_RETRIES):
        req = Request(full_url, headers=headers)
        try:
            with urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 403 and attempt < MAX_RETRIES - 1:
                delay = RETRY_BASE_DELAY * (2 ** attempt)
                print(f"[warn] rate limited, retrying in {delay}s ... ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(delay)
                continue
            print(f"[error] GitHub API {e.code} {e.reason}: {full_url}", file=sys.stderr)
            if e.code == 403:
                print("[hint] rate limit exceeded; set GITHUB_TOKEN env var", file=sys.stderr)
            return None

    return None


def fetch_merged_prs(repo, since_date):
    """return merged PRs (newest first) updated after *since_date* (ISO 8601)."""
    collected = []
    page = 1
    per_page = 100

    while True:
        data = github_get(
            f"{GITHUB_API}/repos/{repo}/pulls",
            params={
                "state": "closed",
                "sort": "updated",
                "direction": "desc",
                "per_page": str(per_page),
                "page": str(page),
            },
        )
        if not data:
            break

        for pr in data:
            merged_at = pr.get("merged_at")
            if not merged_at:
                continue
            if merged_at < since_date:
                return collected
            collected.append(pr)

        if len(data) < per_page:
            break
        page += 1

    return collected


def fetch_pr_files(repo, pr_number):
    """return the list of changed file paths for a given PR.

    returns None when the API call fails (e.g. rate limit) so callers
    can distinguish "no files changed" from "failed to fetch".
    """
    files = []
    page = 1
    per_page = 100

    while True:
        data = github_get(
            f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/files",
            params={"per_page": str(per_page), "page": str(page)},
        )
        if data is None:
            return None
        files.extend(item["filename"] for item in data)
        if len(data) < per_page:
            break
        page += 1

    return files


# ---------------------------------------------------------------------------
# classification logic
# ---------------------------------------------------------------------------

def load_config():
    """load directory_tags.json and return the parsed dict."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def classify_files(changed_files, directory_to_tag):
    """classify *changed_files* into tags via longest-prefix matching.

    for each file, the longest key in *directory_to_tag* that is a prefix of
    the file path wins.  each directory can map to a single tag (str) or
    multiple tags (list).  root-level files fall back to ``infra``.
    """
    sorted_prefixes = sorted(directory_to_tag.keys(), key=len, reverse=True)

    tags = set()
    for filepath in changed_files:
        matched = False
        for prefix in sorted_prefixes:
            if filepath.startswith(prefix + "/") or filepath == prefix:
                value = directory_to_tag[prefix]
                if isinstance(value, list):
                    tags.update(value)
                else:
                    tags.add(value)
                matched = True
                break
        if not matched:
            tags.add("infra")

    return sorted(tags)


# ---------------------------------------------------------------------------
# state management
# ---------------------------------------------------------------------------

def load_state(lookback_days):
    """load persisted state or create a default one."""
    if STATE_PATH.exists():
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    default_since = (
        datetime.now(timezone.utc) - timedelta(days=lookback_days)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"last_processed_date": default_since, "processed_prs": []}


def save_state(state):
    """persist state to disk."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# readme update
# ---------------------------------------------------------------------------

TABLE_START = "<!-- CHANGELOG_TABLE -->"
TABLE_END = "<!-- CHANGELOG_TABLE_END -->"

TABLE_HEADER = (
    "| Date | Commit | PR | Author | Tags | Description |\n"
    "|------|--------|-------|--------|------|-------------|"
)


def update_readme(repo, new_entries):
    """prepend *new_entries* into the changelog table inside README.md."""
    if not new_entries:
        return

    content = README_PATH.read_text(encoding="utf-8")

    if TABLE_START not in content or TABLE_END not in content:
        print("[error] changelog markers not found in README.md", file=sys.stderr)
        sys.exit(1)

    start_idx = content.index(TABLE_START) + len(TABLE_START)
    end_idx = content.index(TABLE_END)

    existing_block = content[start_idx:end_idx].strip()
    existing_lines = existing_block.split("\n") if existing_block else []

    # separate header lines from data lines
    if len(existing_lines) >= 2 and existing_lines[1].startswith("|---"):
        data_lines = existing_lines[2:]
    else:
        data_lines = []

    new_rows = []
    for entry in new_entries:
        commit_short = entry["commit"][:8]
        commit_url = f"https://github.com/{repo}/commit/{entry['commit']}"
        pr_url = f"https://github.com/{repo}/pull/{entry['pr_number']}"
        author_url = f"https://github.com/{entry['author']}"
        tags_str = " ".join(f"`{t}`" for t in entry["tags"])
        title = entry["title"].replace("|", "\\|")

        row = (
            f"| {entry['date']} "
            f"| [{commit_short}]({commit_url}) "
            f"| [#{entry['pr_number']}]({pr_url}) "
            f"| [@{entry['author']}]({author_url}) "
            f"| {tags_str} "
            f"| {title} |"
        )
        new_rows.append(row)

    all_data = new_rows + data_lines
    table_block = TABLE_HEADER + "\n" + "\n".join(all_data)

    before = content[: content.index(TABLE_START) + len(TABLE_START)]
    after = content[end_idx:]
    README_PATH.write_text(f"{before}\n{table_block}\n{after}", encoding="utf-8")
    print(f"[ok] appended {len(new_entries)} entries to README.md")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="classify Model-Optimizer merged PRs")
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=7,
        help="how many days to look back on first run (default: 7)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print results without writing files",
    )
    args = parser.parse_args()

    config = load_config()
    repo = config["watched_repo"]
    directory_to_tag = config["directory_to_tag"]

    print(f"[info] watching repo: {repo}")

    state = load_state(args.lookback_days)
    since_date = state["last_processed_date"]
    processed_set = set(state.get("processed_prs", []))

    print(f"[info] fetching merged PRs since {since_date} ...")
    merged_prs = fetch_merged_prs(repo, since_date)
    print(f"[info] found {len(merged_prs)} merged PRs")

    new_entries = []
    newly_processed = []

    skipped = 0

    # process oldest first so the table stays chronological (newest on top)
    for pr in reversed(merged_prs):
        pr_number = pr["number"]
        if pr_number in processed_set:
            continue

        print(f"  -> PR #{pr_number}: {pr['title']}")
        files = fetch_pr_files(repo, pr_number)

        if files is None:
            print(f"     [skip] could not fetch files for PR #{pr_number}, will retry next run")
            skipped += 1
            continue

        tags = classify_files(files, directory_to_tag)

        new_entries.append({
            "date": pr["merged_at"][:10],
            "commit": pr.get("merge_commit_sha", "unknown"),
            "pr_number": pr_number,
            "author": pr["user"]["login"],
            "title": pr["title"],
            "tags": tags,
        })
        newly_processed.append(pr_number)

    if skipped > 0:
        print(f"[warn] skipped {skipped} PRs due to API errors (will retry next run)")

    if not new_entries:
        print("[info] no new PRs to process")
        return 0

    # newest first in table
    new_entries.sort(key=lambda x: x["date"], reverse=True)

    if args.dry_run:
        print("[dry-run] would add the following entries:")
        for e in new_entries:
            print(f"  {e['date']}  PR#{e['pr_number']}  @{e['author']}  {e['tags']}")
        return 0

    update_readme(repo, new_entries)

    if skipped == 0:
        latest_date = max(pr["merged_at"] for pr in merged_prs)
        state["last_processed_date"] = latest_date
    # when skipped > 0, keep old last_processed_date so skipped PRs
    # appear again on the next run; processed_prs handles dedup.

    all_processed = sorted(processed_set | set(newly_processed))
    # cap to prevent unbounded growth; 500 most recent are sufficient
    # because older PRs fall behind last_processed_date anyway
    if len(all_processed) > 500:
        all_processed = all_processed[-500:]
    state["processed_prs"] = all_processed
    save_state(state)

    print(f"[done] processed {len(new_entries)} new PRs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
