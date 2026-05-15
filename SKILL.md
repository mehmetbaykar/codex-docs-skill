---
name: codex-docs
description: >-
  Local mirror of OpenAI Codex product documentation
  (developers.openai.com/codex): CLI, Cloud, web app, IDE extension, hooks,
  skills, plugins, MCP, subagents, AGENTS.md, prompts, rules, sandboxing,
  models, pricing, security, and configuration. Use whenever the user asks
  how Codex behaves, how to install or configure Codex, or what a Codex
  flag, slash command, or feature does (including informal phrasing such as
  "hooks", "--resume", "sandbox modes", "cloud environments"). Read this
  skill's references/ before generic web search for Codex product questions.
  Do NOT use for Claude Code, Cursor, or other agents -- in particular, do
  not use for "Claude Code hooks" or general OpenAI API, ChatGPT, Realtime,
  or non-Codex coding help.
disable-model-invocation: false
---

# Codex Docs

Local mirror of OpenAI Codex documentation, kept fresh by a 3-hour GitHub Action. The cleaned Markdown lives in `references/`; the auto-generated topic list lives in `references/INDEX.md`; the per-file manifest with upstream URLs lives in `references/docs_manifest.json`.

## Scope

Use this skill for Codex-specific product and configuration questions, including CLI behavior, `codex.toml`, slash commands, Codex hooks, skills, MCP, subagents, AGENTS.md, prompts, sandboxing, cloud environments, models, pricing, security, migrations, and use-case recipes. If the question is about Claude Code hooks, Cursor, general OpenAI APIs, ChatGPT, GPT models, or another non-Codex product, this skill does not apply.

## Workflow

1. If the user supplied a topic, normalize it to a slug:
   - lowercase, strip leading `/codex/`, strip surrounding slashes
   - join nested segments with `__` (e.g. `cli features` -> `cli__features`, `guides agents-md` -> `guides__agents-md`)
2. If `references/<slug>.md` exists, read that file directly. Do NOT grep the whole `references/` tree first - the index plus targeted reads is faster and uses less context.
3. If no exact match, read `references/INDEX.md` and pick the closest topic. If still ambiguous, list the candidates and ask.
4. If the user supplied no topic, read `references/INDEX.md` and present the available topics.

## Answer format

- Lead with a direct answer to the user's question grounded in the file you read.
- Quote short snippets (commands, config keys) when they appear verbatim in the doc.
- End with `Source: <upstream URL>` using the `original_url` from the file frontmatter or `references/docs_manifest.json`.

## Freshness and fallback

The mirror is refreshed every 3 hours by upstream CI. If the local content looks stale, contradicted by the user, or empty:

1. Suggest the user run `npx skills update codex-docs`.
2. Cross-check the canonical URL via `original_url` in `references/docs_manifest.json` and offer it as a follow-up source.
3. If a specific page failed MDX cleaning, the unmodified source is preserved at `references/_raw/<slug>.md` -- read that as a fallback.

## Examples

| Invocation | Reads |
| --- | --- |
| `$codex-docs hooks` / `/codex-docs hooks` | `references/hooks.md` |
| `$codex-docs cli features` | `references/cli__features.md` |
| `$codex-docs cloud environments` | `references/cloud__environments.md` |
| `$codex-docs agents md` | `references/guides__agents-md.md` |
| `$codex-docs` (no argument) | `references/INDEX.md` |
