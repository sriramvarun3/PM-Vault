#!/usr/bin/env python3
"""vault-lint — deterministic health checks for the PM vault.

The agent does the judgment half (contradictions worth revisiting, stale claims,
missing topic pages). This script does the mechanical half, cheaply, so the agent
doesn't burn context globbing the vault. Python 3 standard library only.

Usage:
    python3 _bin/vault-lint.py            # human-readable report
    python3 _bin/vault-lint.py --json     # machine-readable
    python3 _bin/vault-lint.py --vault /path/to/vault

Checks:
  broken-links      [[wiki-links]] with no matching file
  orphans           semantic pages with no inbound links
  unsourced-topics  Topics/ pages with an empty or missing sources:
  missing-stamps    semantic pages missing status: or updated:
  review-due        pages explicitly marked status: review-due
  stale             semantic pages not updated in STALE_DAYS
  cold-contacts     People with a cadence: but no interaction in the window
  old-followups     unchecked boxes in notes untouched for OLD_TASK_DAYS
  past-dates        YYYY-MM-DD mentions in the past on open checkbox lines
  competency-gaps   competencies (from _reference/competencies.md) with little
                    or no Journal evidence
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

DEFAULT_VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMANTIC = ("Topics", "People", "Projects", "Accounts", "Decisions")
EPISODIC = ("Interactions", "Journal")
# Folders that are tooling, templates, raw material, or documentation — not vault content.
SKIP = {".git", "_web", "_templates", "_bin", "_meta", "_inbox", "Sources", "Tasks",
        "_archive", "workflows", "skills", "docs", "examples", ".claude", ".obsidian",
        ".trash", "node_modules"}
# These use [[wiki-links]] illustratively in prose, so "broken" links are examples.
DOC_FILES = {"AGENTS.md", "README.md", "CLAUDE.md"}

STALE_DAYS = 45
OLD_TASK_DAYS = 30
CADENCE_DAYS = {"1:1": 21, "weekly": 14, "monthly": 45, "as-needed": 90}

LINK_RE = re.compile(r"\[\[([^\]|#]+)")
TASK_RE = re.compile(r"^\s*-\s+\[ \]\s+(.*)$", re.M)
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def today():
    return dt.date.today()


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n"):
        if line.startswith(" ") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.split("#")[0].strip().strip('"').strip("'")
    return out


def load_competencies(vault):
    """Competency labels are the `## ` headings in _reference/competencies.md."""
    path = os.path.join(vault, "_reference", "competencies.md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return []
    text = COMMENT_RE.sub("", text)
    return [h for h in HEADING_RE.findall(text) if not h.lower().startswith("level")]


def load(vault):
    """Return {relpath: {name, folder, text, fm}}."""
    pages = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, vault)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            pages[rel] = {
                "name": fn[:-3],
                "folder": rel.split(os.sep)[0] if os.sep in rel else "",
                # HTML comments hold template guidance and placeholder links; ignore them.
                "text": COMMENT_RE.sub("", text),
                "fm": parse_frontmatter(text),
            }
    return pages


def date_of(vault, page, rel):
    """Best available date for a page: updated:, then date:, then mtime."""
    for key in ("updated", "date", "decided"):
        v = page["fm"].get(key)
        if v:
            try:
                return dt.date.fromisoformat(v)
            except ValueError:
                pass
    try:
        return dt.date.fromtimestamp(os.path.getmtime(os.path.join(vault, rel)))
    except OSError:
        return None


def run(vault):
    pages = load(vault)
    competencies = load_competencies(vault)
    by_name = {p["name"]: rel for rel, p in pages.items()}
    findings = defaultdict(list)

    inbound = defaultdict(set)
    broken = set()
    for rel, page in pages.items():
        for target in LINK_RE.findall(page["text"]):
            target = target.strip()
            if target in by_name:
                if by_name[target] != rel:
                    inbound[by_name[target]].add(rel)
            elif rel not in DOC_FILES:
                broken.add(f"{rel} → [[{target}]]")
    findings["broken-links"].extend(sorted(broken))

    for rel, page in pages.items():
        folder, fm = page["folder"], page["fm"]
        d = date_of(vault, page, rel)
        age = (today() - d).days if d else None

        if folder in SEMANTIC:
            if not inbound[rel]:
                findings["orphans"].append(rel)
            if not fm.get("status"):
                findings["missing-stamps"].append(f"{rel} (no status:)")
            if not fm.get("updated"):
                findings["missing-stamps"].append(f"{rel} (no updated:)")
            if fm.get("status") == "review-due":
                findings["review-due"].append(rel)
            if age is not None and age > STALE_DAYS:
                findings["stale"].append(f"{rel} ({age}d)")

        if folder == "Topics":
            src = fm.get("sources", "")
            if src in ("", "[]"):
                findings["unsourced-topics"].append(rel)

        open_tasks = TASK_RE.findall(page["text"])
        open_tasks = [t for t in open_tasks if t.strip()]
        if open_tasks and age is not None and age > OLD_TASK_DAYS:
            findings["old-followups"].append(
                f"{rel}: {len(open_tasks)} open, untouched {age}d")
        for t in open_tasks:
            for ds in DATE_RE.findall(t):
                try:
                    if dt.date.fromisoformat(ds) < today():
                        findings["past-dates"].append(f"{rel}: {t.strip()[:90]}")
                except ValueError:
                    pass

    # cold contacts: last episodic note mentioning the person
    last_seen = {}
    for rel, page in pages.items():
        if page["folder"] not in EPISODIC:
            continue
        d = date_of(vault, page, rel)
        if not d:
            continue
        for target in set(LINK_RE.findall(page["text"])):
            target = target.strip()
            if by_name.get(target, "").startswith("People" + os.sep):
                if target not in last_seen or d > last_seen[target]:
                    last_seen[target] = d
    for rel, page in pages.items():
        if page["folder"] != "People":
            continue
        cadence = (page["fm"].get("cadence") or "").lower()
        window = next((v for k, v in CADENCE_DAYS.items() if k in cadence), None)
        if not window:
            continue
        seen = last_seen.get(page["name"])
        if seen is None:
            findings["cold-contacts"].append(
                f"{page['name']} (cadence '{cadence}', no interaction note)")
        else:
            gap = (today() - seen).days
            if gap > window:
                findings["cold-contacts"].append(
                    f"{page['name']} (cadence '{cadence}', last seen {seen}, {gap}d ago)")

    # competency coverage across Journal entries
    counts = {c: 0 for c in competencies}
    unknown = set()
    for rel, page in pages.items():
        if page["folder"] != "Journal":
            continue
        raw = page["fm"].get("competency", "")
        for label in re.findall(r'"([^"]+)"', raw) or re.findall(r"\[?([^,\[\]]+)", raw):
            label = label.strip()
            if not label:
                continue
            if label in counts:
                counts[label] += 1
            elif competencies:
                unknown.add(f"{rel}: '{label}'")
    for c, n in counts.items():
        if n <= 1:
            findings["competency-gaps"].append(
                f"{c}: {n} journal entr{'y' if n == 1 else 'ies'}")
    findings["competency-gaps"].extend(
        sorted(f"off-vocabulary label — {u}" for u in unknown))

    return pages, findings, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--vault", default=DEFAULT_VAULT,
                    help="vault root (default: the folder above _bin/)")
    args = ap.parse_args()
    vault = os.path.abspath(args.vault)

    pages, findings, counts = run(vault)

    if args.json:
        print(json.dumps({"pages": len(pages), "findings": findings,
                          "competency_counts": counts}, indent=2, sort_keys=True))
        return 0

    order = ["broken-links", "unsourced-topics", "missing-stamps", "review-due",
             "stale", "orphans", "cold-contacts", "old-followups", "past-dates",
             "competency-gaps"]
    total = sum(len(findings[k]) for k in order)
    print(f"vault-lint — {len(pages)} pages scanned, {total} findings, {today()}")
    for key in order:
        items = findings.get(key) or []
        print(f"\n## {key} ({len(items)})")
        if not items:
            print("  clean")
        for i in sorted(items):
            print(f"  - {i}")
    print("\nJudgment checks the agent still has to do: contradictions worth revisiting,")
    print("claims superseded by newer sources, concepts mentioned 3+ times with no Topic")
    print("page, and gaps a workplace or web search could close.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
