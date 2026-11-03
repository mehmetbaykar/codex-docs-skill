# Codex Docs Skill

An unofficial mirror of the [OpenAI Codex documentation](https://learn.chatgpt.com/docs), recipes, and guides, packaged as an [Agent Skill](https://agentskills.io) so coding agents read the docs locally instead of searching the web. A GitHub Action refreshes the mirror every 3 hours.

The skill lives in `skills/codex-docs/`. The repository is also a plugin, `codex-docs`, for Claude Code, Codex, and Cursor.

## Install

| Agent | Install |
| --- | --- |
| Any agent that reads Agent Skills | `npx skills add mehmetbaykar/codex-docs-skill` |
| Claude Code | `/plugin marketplace add mehmetbaykar/codex-docs-skill`, then `/plugin install codex-docs@codex-docs-skill` |
| Codex | `codex plugin marketplace add mehmetbaykar/codex-docs-skill`, then `codex plugin add codex-docs@codex-docs-skill` |
| Cursor | In **Customize**, choose **From GitHub Repository** and enter `https://github.com/mehmetbaykar/codex-docs-skill`, then install `codex-docs` |

## Use

Ask a Codex question and the agent picks up the skill on its own, or call it with a topic:

- Codex: `$codex-docs hooks`
- Claude Code and Cursor: `/codex-docs hooks` (as a Claude Code plugin, also `/codex-docs:codex-docs hooks`)

With no topic, the skill shows what the mirror covers. [`skills/codex-docs/SKILL.md`](skills/codex-docs/SKILL.md) holds the instructions the agent follows.

## Update

| Installed with | Update |
| --- | --- |
| `npx skills` | `npx skills update codex-docs` |
| Claude Code plugin | `claude plugin marketplace update codex-docs-skill`, then `claude plugin update codex-docs@codex-docs-skill` |
| Codex plugin | `codex plugin marketplace upgrade` |
| Cursor plugin | Import the repository again from **Customize**; team marketplaces can turn on **Enable Auto Refresh** |

Every refresh sets the plugin version to the time of the mirror's last change (`2026.1103.1534` is November 3, 15:34 UTC), so plugin managers see each update.

## What's mirrored

The fetcher reads https://learn.chatgpt.com/sitemap-index.xml and https://learn.chatgpt.com/docs/llms.txt and merges both lists, because neither is complete on its own: the sitemap omits pages that llms.txt links only as `?surface=` variants, and llms.txt omits the changelog. It mirrors three sections:

- **Documentation** under `/docs`. The changelog is rendered from https://learn.chatgpt.com/docs/changelog/rss.xml because that page has no `.md` version.
- **Recipes** under `/use-cases`. The gallery mixes ChatGPT and Codex recipes; a recipe stays when its name, tagline, or summary mentions Codex, or, when neither product is named there, when its body mentions Codex more than ChatGPT.
- **Guides** under `/guides`, converted from HTML.

learn.chatgpt.com hosts the combined ChatGPT and Codex docs, so pages about ChatGPT-only features (dots, Space, Sites, pets, image generation, visualizations, personalization, appshots, file artifacts, ChatGPT Work, and ChatGPT on the web) are left out. Pages about the ChatGPT desktop app that Codex runs in stay in. `/docs/enterprise/*`, `/docs/videos`, and the aggregate exports (`/docs/codex-manual`, `/docs/llms-full`) are left out too. Legacy `/codex/*` links are rewritten to their current `/docs/*` location.

[`references/INDEX.md`](skills/codex-docs/references/INDEX.md) lists every page by section. [`references/docs_manifest.json`](skills/codex-docs/references/docs_manifest.json) records each page's upstream URL, content hash, and `live` or `stale` status, plus the recipes that were left out and why.

## Freshness guarantees

A refresh builds the whole mirror in memory and publishes it only when every check passes, so a failed run never leaves a half-written mirror. The run fails without publishing when:

- discovery finds no pages, or fewer than 80% of the pages already mirrored
- no page could be fetched live
- more than 20% of pages are stale, have no usable Markdown, or fail cleaning
- a page fails and has no earlier copy to fall back on

A page that fails while an earlier copy exists keeps that copy and is marked `stale`. When cleaning fails, the raw upstream source is kept under `references/_raw/`.

## For maintainers

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/fetch_docs.py
```

[`scripts/fetch_docs.py`](scripts/fetch_docs.py) holds the Codex settings. Everything else in `scripts/`, `tests/`, and `.github/` is shared, byte for byte, with [claude-code-docs-skill](https://github.com/mehmetbaykar/claude-code-docs-skill) and [cursor-docs-skill](https://github.com/mehmetbaykar/cursor-docs-skill); `SHARED_FILES` in [`scripts/docs_mirror.py`](scripts/docs_mirror.py) lists the files. Change shared files in all three repositories on branches with the same name: CI's drift check (`python scripts/fetch_docs.py --check-drift`) compares against that branch in the other repositories, or their `main`, and fails while the files differ.

```text
.
├── plugin.json                          # Agent Plugins manifest (Codex, Cursor)
├── .claude-plugin/                      # Claude Code plugin and marketplace (Codex and npx skills read these too)
├── .cursor-plugin/                      # Cursor plugin and marketplace
├── skills/codex-docs/
│   ├── SKILL.md                         # instructions the agent follows
│   ├── agents/openai.yaml               # Codex and ChatGPT app metadata
│   └── references/                      # mirrored pages, INDEX.md, docs_manifest.json
├── scripts/
│   ├── fetch_docs.py                    # Codex settings
│   └── docs_mirror.py                   # shared engine
├── tests/                               # offline tests
└── .github/workflows/update-docs.yml    # tests, refresh every 3 hours, drift check, failure alerts
```

## Troubleshooting

- **Docs look stale:** check the latest run of [Update docs mirror](../../actions/workflows/update-docs.yml).
- **A scheduled refresh failed:** the workflow opens or updates an issue titled "Docs mirror update failures" and closes it after the next successful run.
- **A page shows `stale`:** upstream could not be reached on the last run, so the previous copy is still served.

## Notes

This is an unofficial mirror, not affiliated with, endorsed by, or sponsored by OpenAI. The documentation belongs to OpenAI and is subject to OpenAI's terms. The MIT license in this repository covers only the mirroring tooling, scripts, and packaging.
