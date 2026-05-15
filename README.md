# Codex Docs Skill

Local Agent Skill mirror of the OpenAI Codex documentation from
[https://developers.openai.com/codex](https://developers.openai.com/codex).

The repository is the skill: `SKILL.md` is the entry point, cleaned Markdown
copies of every relevant Codex page live under `references/`, and a 3-hour
GitHub Action keeps them in sync with upstream.

## Install

```bash
npx skills add mehmetbaykar/codex-docs-skill
```

The `npx skills` CLI handles install, update, and removal across Codex CLI,
Codex IDE/App, Claude Code, Cursor, and other agents that follow the
[agentskills.io](https://agentskills.io) standard.

## Usage

Once installed, invoke the skill with a topic from your agent (`$codex-docs-skill hooks` in Codex, `/codex-docs-skill hooks` in Claude Code) or with no argument to
list topics. The full agent-facing usage contract lives in `[SKILL.md](SKILL.md)`.

## What's mirrored

The fetcher reads `https://developers.openai.com/sitemap-index.xml`, keeps
every URL whose path starts with `/codex/`, and excludes:

- `/codex/enterprise/*`
- `/codex/videos`
- non-doc cross-domain URLs (blog, cookbook, community, resources, showcase)
- query-string variants of the same page

The current mirror contains 129 cleaned Markdown files plus
`references/INDEX.md` and `references/docs_manifest.json`. The Codex changelog
is rendered from `https://developers.openai.com/codex/changelog/rss.xml`
because the changelog page does not expose an `.md` endpoint. Any sitemap
entries we intentionally skip are recorded in `docs_manifest.json` under
`skipped`.

## Update

```bash
npx skills update codex-docs-skill   # update an installed local copy
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
rewrites `references/INDEX.md` and `references/docs_manifest.json`. Files
whose content hash is unchanged are not rewritten.

## Repository layout

```
.
├── SKILL.md                   # agent-facing instructions and routing
├── agents/openai.yaml         # Codex App UI metadata + invocation policy
├── references/                # mirrored Codex docs + INDEX + manifest
├── scripts/
│   ├── fetch_codex_docs.py    # sitemap -> fetch -> clean -> write
│   └── requirements.txt
└── .github/workflows/
    └── update-docs.yml        # cron every 3 hours
```

## Troubleshooting

- If docs look stale, check the latest run of [Update Codex Documentation](actions/workflows/update-docs.yml) on this repository
and reproduce locally with the steps in "Refresh locally" above.
- If the scheduled fetch fails, the workflow opens an issue automatically.
- If a single page renders poorly, the upstream MDX is preserved under
`references/_raw/` whenever the cleaner falls back, so the source of truth
is never lost.

## Notes

This repository is an unofficial local mirror packaged as an Agent Skill. It is
not affiliated with, endorsed by, or sponsored by OpenAI.

Documentation content belongs to OpenAI and is subject to OpenAI's applicable
terms and policies. The MIT license in this repository applies only to the
mirroring tool, scripts, skill metadata, and repository-specific code.
