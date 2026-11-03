---
name: codex-docs
description: >-
  Answers questions about OpenAI Codex from a local mirror of its official
  documentation, recipes, and guides (learn.chatgpt.com). Use when someone
  asks how Codex behaves or how to set it up: the CLI, IDE extension, desktop
  app, cloud tasks, config.toml, AGENTS.md, hooks, skills, plugins, MCP,
  subagents, sandboxing and approvals, models and pricing, the SDK, Codex
  Security, the changelog, or a Codex recipe for a task. Read the mirror
  before searching the web. Not for Claude Code, Cursor, the OpenAI API, or
  ChatGPT-only features such as dots, Space, or Sites.
license: MIT for the mirroring tooling; the mirrored documentation belongs to OpenAI.
compatibility: Any agent that reads Agent Skills, such as Claude Code, Codex, or Cursor. Needs read access to this skill's files and no network access.
allowed-tools: Read Grep Glob
metadata:
  upstream: https://learn.chatgpt.com/docs
  repository: https://github.com/mehmetbaykar/codex-docs-skill
---

# Codex Docs

A local mirror of the Codex documentation, recipes, and guides, refreshed from learn.chatgpt.com every 3 hours. Start at `references/INDEX.md`. Each page is a file `references/<topic>.md` whose frontmatter holds its `title`, `source` URL, and `path`; `references/docs_manifest.json` records every page's upstream URL and status.

learn.chatgpt.com also documents ChatGPT. Pages about ChatGPT-only features are left out; pages about the ChatGPT desktop app that Codex runs in stay in.

## Find the page

1. Turn the topic into a slug: lowercase, drop a leading `/docs/`, and join nested segments with `__` (for example `cli features` becomes `cli__features`). Recipes are `use-cases__<name>` and guides are `guides__<name>`.
2. If `references/<slug>.md` exists, read it.
3. Otherwise read `references/INDEX.md`, pick the closest topics, and read those files. Search the `references/` tree only when the index has no match; the index is faster and keeps context small.
4. With no topic, show the topic groups in `references/INDEX.md`.

## Answer

- Lead with a direct answer grounded in the files you read.
- Quote commands, flags, and `config.toml` keys exactly as the page writes them.
- End with `Source: <url>`, using the `source` value from the page's frontmatter.

## When the mirror looks stale or wrong

1. Check the page's `status` in `references/docs_manifest.json`: `stale` means the last refresh could not reach upstream, so the previous copy is still served.
2. Suggest updating the skill with `npx skills update codex-docs`, or the `codex-docs` plugin from the agent's plugin manager.
3. Offer the page's `source` URL so the user can check the live page.
4. A page whose cleaning failed keeps its raw upstream source in `references/_raw/<slug>.md`.

## Examples

| Request | Read |
| --- | --- |
| `$codex-docs hooks` in Codex, `/codex-docs hooks` in Claude Code or Cursor | `references/hooks.md` |
| "What CLI flags and slash commands exist?" | `references/developer-commands.md` |
| "What can I set in config.toml?" | `references/config-file__config-reference.md` |
| "How should I write AGENTS.md?" | `references/agent-configuration__agents-md.md` |
| "Is there a recipe for building a CLI Codex can use?" | `references/use-cases__agent-friendly-clis.md` |
| "What are the Codex best practices?" | `references/guides__best-practices.md` |
| No topic, or no matching file | `references/INDEX.md` |
