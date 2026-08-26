---
name: reference-lookup
description: Look up a paper's DOI, year, and authors from its title (or partial citation) using the free, keyless OpenAlex API, then cross-check the DOI against Crossref. Use when the user gives a paper title and needs its DOI or metadata, asks to build a reading list from titles, or asks to find or verify a citation.
---

# Reference Lookup (OpenAlex + Crossref)

Resolve a paper title to real metadata using OpenAlex — a free, keyless scholarly
API covering 240M+ works. No API key or account is required. Never rely on your
own memory for a DOI: report only what the API returns, and cross-check it before
you trust it.

## Look up a paper by title

Run this (Python 3, standard library only — nothing to install). Replace the title:

```bash
uv run --no-project python - <<'PY'
import json, urllib.parse, urllib.request
title = "PUT THE PAPER TITLE HERE"
url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
    "search": title, "per-page": 3, "mailto": "you@example.com"})
with urllib.request.urlopen(url, timeout=20) as r:
    data = json.load(r)
for w in data["results"]:
    authors = ", ".join(a["author"]["display_name"] for a in w["authorships"][:3])
    print(f"- {w['title']}\n  {authors} ({w.get('publication_year')})\n  DOI: {w.get('doi')}")
PY
```

Set `mailto` to the user's real email to join OpenAlex's faster "polite pool" (optional).

## Verify before you trust (do not skip)

A returned DOI is a *candidate*, not proof. For each result:

1. **Cross-check the DOI against Crossref** — a second, independent source. If
   OpenAlex and Crossref agree on the title for that DOI, trust it; if they
   disagree, flag it as suspicious.

   ```bash
   uv run --no-project python - <<'PY'
   import json, urllib.request
   doi = "10.XXXX/XXXXX"   # the DOI to check, no https:// prefix
   try:
       with urllib.request.urlopen(f"https://api.crossref.org/works/{doi}", timeout=20) as r:
           m = json.load(r)["message"]
       print("Crossref title:", (m.get("title") or ["?"])[0])
       print("Crossref year :", m.get("issued", {}).get("date-parts", [[None]])[0][0])
   except Exception as e:
       print("DOI did NOT resolve at Crossref:", e)
   PY
   ```

2. **Tell the user to open** `https://doi.org/<DOI>` and confirm the landing page
   matches the title, authors, and year. The final check is human.

## Rules

- **Never invent or guess a DOI.** Report only a DOI the API returned. If OpenAlex
  finds no match, say so plainly — do not substitute a plausible-looking DOI.
- If a lookup by ID 404s, re-run the plain title search before concluding the
  work does not exist.
- Present results as a **short list** (title, authors, year, DOI, verified or
  unverified) — not a rewrite of any file. The user decides what enters their
  reading list.
