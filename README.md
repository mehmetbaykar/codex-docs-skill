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

The fetcher discovers pages from `https://learn.chatgpt.com/sitemap-index.xml`
and the machine-readable index at `https://learn.chatgpt.com/docs/llms.txt`,
then merges both sets. Neither index is complete on its own: the sitemap omits
pages that llms.txt links only as `?surface=` query variants (such as
`developer-commands` and `developer-settings`), and llms.txt omits the
changelog. It mirrors pages under `/docs` and `/docs/*` that expose a `.md`
source or have a special fetcher, and excludes:

- `/docs/enterprise/*`
- `/docs/videos`
- aggregate exports (`/docs/codex-manual`, `/docs/llms-full`)
- cross-domain URLs

Query-string variants collapse onto the single page they represent, and legacy
`/codex/*` links inside page bodies are rewritten to their current `/docs/*`
location.

Current counts, fetched files, skipped entries, stale pages, and failed pages
are recorded in `skills/codex-docs/references/docs_manifest.json`; the generated
topic list lives in `skills/codex-docs/references/INDEX.md`. The Codex changelog
is rendered from `https://learn.chatgpt.com/docs/changelog/rss.xml` because the
changelog page does not expose an `.md` endpoint.

## Update

```bash
npx skills update codex-docs   # update an installed local copy
```

Upstream refreshes happen automatically every 3 hours; there is nothing to
configure on the consumer side.

## Refresh locally (maintainers only)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-dev.txt
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/fetch_codex_docs.py
```

The fetcher discovers pages, downloads each page's `.md` source, cleans MDX
and JSX wrappers into plain Markdown, renders the changelog from RSS, and
rewrites `skills/codex-docs/references/INDEX.md` and
`skills/codex-docs/references/docs_manifest.json`. Files whose content hash is
unchanged are not rewritten.

## Freshness guarantees

The mirror fails loudly rather than serving frozen content. A run aborts
without committing when:

- discovery returns no pages
- no page could be fetched live
- discovery drops below 80% of the previously mirrored page count
- more than 20% of pages served stale content or exposed no usable Markdown
- any page failed outright

Every entry in `docs_manifest.json` records a `status` of `live` or `stale`,
and `fetch_metadata` reports live, stale, skipped, and failed counts for the
run.

## Repository layout

```text
.
├── skills/
│   └── codex-docs/
│       ├── agents/
│       │   └── openai.yaml       # Agent UI metadata + invocation policy
│       ├── SKILL.md              # installed skill instructions and routing
│       └── references/           # mirrored Codex docs + INDEX + manifest
├── scripts/
│   ├── fetch_codex_docs.py       # discover -> fetch -> clean -> write
│   ├── requirements.txt
│   └── requirements-dev.txt
├── tests/
│   └── test_fetch_codex_docs.py  # offline tests for the fetcher
└── .github/workflows/
    └── update-docs.yml           # tests on PRs, cron refresh every 3 hours
```

## Troubleshooting

- If docs look stale, check the latest run of
  [Update Codex Documentation](../../actions/workflows/update-docs.yml) on this
  repository and reproduce locally with the steps in "Refresh locally" above.
- If the scheduled fetch fails, the workflow opens or updates a failure issue
  automatically and closes it after the next successful run.
- If a page reports `stale` in `docs_manifest.json`, the previous content is
  still served but upstream could not be reached on the last run.
- If a single page renders poorly and the cleaner fell back, the upstream MDX is
  preserved under `skills/codex-docs/references/_raw/`, so the source of truth is
  never lost.

## Notes

This repository is an unofficial local mirror packaged as an Agent Skill. It is
not affiliated with, endorsed by, or sponsored by OpenAI.

Documentation content belongs to OpenAI and is subject to OpenAI's applicable
terms and policies. The MIT license in this repository applies only to the
mirroring tool, scripts, skill metadata, and repository-specific code.
