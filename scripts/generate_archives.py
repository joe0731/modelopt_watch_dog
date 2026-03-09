#!/usr/bin/env python3
"""
generate archive reports from data/changelog.json.

two types of archives:
  1. monthly:  archives/YYYY-MM/report.md       (grouped by month)
  2. per-tag:  tags_archives/<tag>/README.md     (grouped by tag)

rows containing high-priority tags (eval, vllm, vlm, onnx) are visually
highlighted with emoji markers and bold text in monthly archives.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
CHANGELOG_PATH = ROOT_DIR / "data" / "changelog.json"
ARCHIVES_DIR = ROOT_DIR / "archives"
TAG_ARCHIVES_DIR = ROOT_DIR / "tags_archives"
CONFIG_PATH = ROOT_DIR / "config" / "directory_tags.json"

HIGHLIGHT_TAGS = {
    "eval":  "🟡",
    "vllm":  "🔵",
    "vlm":   "🟣",
    "onnx":  "🟠",
}


def load_changelog():
    """load structured changelog entries."""
    if not CHANGELOG_PATH.exists():
        print("[error] data/changelog.json not found; run classify_mr.py first", file=sys.stderr)
        sys.exit(1)
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config():
    """read config including watched_repo and tag_definitions."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_month(entries):
    """group entries into {YYYY-MM: [entries...]} buckets."""
    buckets = defaultdict(list)
    for entry in entries:
        month_key = entry["date"][:7]  # "YYYY-MM"
        buckets[month_key].append(entry)
    return buckets


def get_highlight_markers(tags):
    """return emoji markers for any high-priority tags present."""
    markers = []
    for tag, emoji in HIGHLIGHT_TAGS.items():
        if tag in tags:
            markers.append(emoji)
    return markers


def sanitize_title(title):
    """escape markdown-sensitive characters in external text."""
    for ch in ("\\", "|", "[", "]", "<", ">", "`"):
        title = title.replace(ch, f"\\{ch}")
    return title


def generate_report(month_key, entries, repo):
    """generate a markdown report for one month."""
    lines = []
    lines.append(f"# Model-Optimizer Changelog — {month_key}\n")
    lines.append(f"> Auto-generated from [{repo}](https://github.com/{repo}) merged PRs.\n")
    lines.append("> Rows marked with color emoji contain **high-priority** tags:\n")
    lines.append("> 🟡 `eval`  🔵 `vllm`  🟣 `vlm`  🟠 `onnx`\n")

    lines.append("| Focus | Date | Commit | PR | Author | Tags | Description |")
    lines.append("|:-----:|------|--------|-------|--------|------|-------------|")

    sorted_entries = sorted(entries, key=lambda x: x["date"], reverse=True)

    for entry in sorted_entries:
        tags = entry["tags"]
        markers = get_highlight_markers(tags)
        focus_col = "".join(markers) if markers else ""
        is_highlighted = len(markers) > 0

        commit_short = entry["commit"][:8]
        commit_url = f"https://github.com/{repo}/commit/{entry['commit']}"
        pr_url = f"https://github.com/{repo}/pull/{entry['pr_number']}"
        author_url = f"https://github.com/{entry['author']}"

        tags_str = " ".join(f"`{t}`" for t in tags)
        title = sanitize_title(entry["title"])

        if is_highlighted:
            # bold the key columns for visual weight
            date_col = f"**{entry['date']}**"
            commit_col = f"**[{commit_short}]({commit_url})**"
            pr_col = f"**[#{entry['pr_number']}]({pr_url})**"
            author_col = f"**[@{entry['author']}]({author_url})**"
            title_col = f"**{title}**"
        else:
            date_col = entry["date"]
            commit_col = f"[{commit_short}]({commit_url})"
            pr_col = f"[#{entry['pr_number']}]({pr_url})"
            author_col = f"[@{entry['author']}]({author_url})"
            title_col = title

        row = (
            f"| {focus_col} "
            f"| {date_col} "
            f"| {commit_col} "
            f"| {pr_col} "
            f"| {author_col} "
            f"| {tags_str} "
            f"| {title_col} |"
        )
        lines.append(row)

    # summary footer
    total = len(sorted_entries)
    highlighted = sum(1 for e in sorted_entries if get_highlight_markers(e["tags"]))
    lines.append("")
    lines.append(f"---\n**Total: {total} PRs** | **Highlighted: {highlighted}**")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# per-tag archives
# ---------------------------------------------------------------------------

def group_by_tag(entries):
    """group entries by tag. each entry appears in every tag it carries."""
    buckets = defaultdict(list)
    for entry in entries:
        for tag in entry["tags"]:
            buckets[tag].append(entry)
    return buckets


def generate_tag_report(tag, description, entries, repo):
    """generate a markdown report for a single tag."""
    lines = []
    lines.append(f"# `{tag}` — {description}\n")
    lines.append(
        f"> All merged PRs in [{repo}](https://github.com/{repo}) "
        f"that touched **{tag}** related code.\n"
    )

    lines.append("| Date | Commit | PR | Author | All Tags | Description |")
    lines.append("|------|--------|-------|--------|----------|-------------|")

    sorted_entries = sorted(entries, key=lambda x: x["date"], reverse=True)

    for entry in sorted_entries:
        commit_short = entry["commit"][:8]
        commit_url = f"https://github.com/{repo}/commit/{entry['commit']}"
        pr_url = f"https://github.com/{repo}/pull/{entry['pr_number']}"
        author_url = f"https://github.com/{entry['author']}"
        tags_str = " ".join(f"`{t}`" for t in entry["tags"])
        title = sanitize_title(entry["title"])

        row = (
            f"| {entry['date']} "
            f"| [{commit_short}]({commit_url}) "
            f"| [#{entry['pr_number']}]({pr_url}) "
            f"| [@{entry['author']}]({author_url}) "
            f"| {tags_str} "
            f"| {title} |"
        )
        lines.append(row)

    lines.append("")
    lines.append(f"---\n**Total: {len(sorted_entries)} PRs**")
    lines.append("")

    return "\n".join(lines)


def generate_tag_index(tag_counts, tag_definitions):
    """generate tags_archives/README.md as a directory index."""
    lines = []
    lines.append("# Tag Archives\n")
    lines.append(
        "Each directory below contains all commits related to that tag.\n"
        "Click a tag to see its full history.\n"
    )

    lines.append("| Tag | Description | PRs |")
    lines.append("|-----|-------------|:---:|")

    for tag in sorted(tag_counts.keys()):
        desc = tag_definitions.get(tag, "")
        count = tag_counts[tag]
        lines.append(f"| [`{tag}`]({tag}/) | {desc} | {count} |")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def generate_monthly_archives(entries, repo):
    """generate archives/YYYY-MM/report.md for each month."""
    buckets = group_by_month(entries)
    generated = 0

    for month_key in sorted(buckets.keys(), reverse=True):
        month_entries = buckets[month_key]
        report = generate_report(month_key, month_entries, repo)

        out_dir = ARCHIVES_DIR / month_key
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "report.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"[ok] {out_path.relative_to(ROOT_DIR)}  ({len(month_entries)} PRs)")
        generated += 1

    print(f"[done] generated {generated} monthly archives")


def generate_all_tag_archives(entries, repo, tag_definitions):
    """generate tags_archives/<tag>/README.md for each tag."""
    buckets = group_by_tag(entries)
    generated = 0
    tag_counts = {}

    for tag in sorted(buckets.keys()):
        tag_entries = buckets[tag]
        description = tag_definitions.get(tag, "")
        report = generate_tag_report(tag, description, tag_entries, repo)

        out_dir = TAG_ARCHIVES_DIR / tag
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "README.md"
        out_path.write_text(report, encoding="utf-8")
        print(f"[ok] {out_path.relative_to(ROOT_DIR)}  ({len(tag_entries)} PRs)")
        tag_counts[tag] = len(tag_entries)
        generated += 1

    # generate index page
    index = generate_tag_index(tag_counts, tag_definitions)
    index_path = TAG_ARCHIVES_DIR / "README.md"
    TAG_ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index, encoding="utf-8")

    print(f"[done] generated {generated} tag archives + index")


def main():
    config = load_config()
    repo = config["watched_repo"]
    tag_definitions = config.get("tag_definitions", {})
    entries = load_changelog()

    if not entries:
        print("[info] no entries in changelog.json")
        return 0

    generate_monthly_archives(entries, repo)
    generate_all_tag_archives(entries, repo, tag_definitions)
    return 0


if __name__ == "__main__":
    sys.exit(main())
