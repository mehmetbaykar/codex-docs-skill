# Codex Docs Skill

Local Agent Skill mirror of the OpenAI Codex documentation from
[https://learn.chatgpt.com/docs](https://learn.chatgpt.com/docs).

The installable skill lives in `skills/codex-docs/`: `SKILL.md` is the entry
point, cleaned Markdown copies live under `skills/codex-docs/references/`, and
a 3-hour GitHub Action keeps them in sync with upstream.

## Install

```bash
npx skills add mehmetbaykar/codex-docs-skill
```

The `npx skills` CLI discovers the nested skill automatically. Installing the
repo exposes only the skill directory (`SKILL.md` plus `references/`) to the
target agent while repository maintenance files stay at the repo root.

The repository slug is `codex-docs-skill`; the installed skill name is
`codex-docs`.

## Usage

Once installed, invoke the skill with a topic from your agent
(`$codex-docs hooks` in Codex, `/codex-docs hooks` in Claude Code) or with no
argument to list topics. The full agent-facing usage contract lives in
[skills/codex-docs/SKILL.md](skills/codex-docs/SKILL.md).

## What's mirrored

The fetcher reads `https://learn.chatgpt.com/sitemap-index.xml` and mirrors
Codex pages under `/docs` and `/docs/*` when they expose a `.md` source or
have a special fetcher. If the sitemap yields no docs pages, it falls back to
`https://learn.chatgpt.com/docs/llms.txt`. It excludes:

- `/docs/enterprise/*`
- `/docs/videos`
- non-doc site sections (use-cases, guides, videos, resources, community)
- query-string variants of the same page

Current counts, fetched files, skipped entries, and failed pages are recorded in
`skills/codex-docs/references/docs_manifest.json`; the generated topic list
lives in `skills/codex-docs/references/INDEX.md`. The Codex changelog is
rendered from `https://learn.chatgpt.com/docs/changelog/rss.xml` because
the changelog page does not expose an `.md` endpoint.

## Update

```bash
npx skills update codex-docs   # update an installed local copy
```

Upstream refreshes happen automatically every 3 hours; there is nothing to
configure on the consumer side.

## Refresh locally (maintainers only)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/fetch_codex_docs.py
```

The fetcher reads the sitemap, downloads each page's `.md` source, cleans MDX
and JSX wrappers into plain Markdown, renders the changelog from RSS, and
rewrites `skills/codex-docs/references/INDEX.md` and
`skills/codex-docs/references/docs_manifest.json`. Files whose content hash is
unchanged are not rewritten.

## Repository layout

```text
.
├── agents/openai.yaml         # Codex App UI metadata + invocation policy
├── skills/
│   └── codex-docs/
│       ├── SKILL.md           # installed skill instructions and routing
│       └── references/        # mirrored Codex docs + INDEX + manifest
├── scripts/
│   ├── fetch_codex_docs.py    # sitemap -> fetch -> clean -> write
│   └── requirements.txt
└── .github/workflows/
    └── update-docs.yml        # cron every 3 hours
```

## Troubleshooting

- If docs look stale, check the latest run of
  [Update Codex Documentation](../../actions/workflows/update-docs.yml) on this
  repository and reproduce locally with the steps in "Refresh locally" above.
- If the scheduled fetch fails, the workflow opens or updates a
`docs-fetch-failure` issue automatically.
- If a single page renders poorly and the cleaner fell back, the upstream MDX is
preserved under `skills/codex-docs/references/_raw/`, so the source of truth is
never lost.

## Notes

This repository is an unofficial local mirror packaged as an Agent Skill. It is
not affiliated with, endorsed by, or sponsored by OpenAI.

Documentation content belongs to OpenAI and is subject to OpenAI's applicable
terms and policies. The MIT license in this repository applies only to the
mirroring tool, scripts, skill metadata, and repository-specific code.
