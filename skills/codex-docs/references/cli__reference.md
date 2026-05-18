---
title: Command line options
source: https://developers.openai.com/codex/cli/reference
path: /codex/cli/reference
---

# Command line options

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

];

## How to read this reference

This page catalogs every documented Codex CLI command and flag. Use the interactive tables to search by key or description. Each section indicates whether the option is stable or experimental and calls out risky combinations.

The CLI inherits most defaults from <code>~/.codex/config.toml</code>. Any
  <code>-c key=value</code> overrides you pass at the command line take
  precedence for that invocation. See [Config
  basics](https://developers.openai.com/codex/config-basic#configuration-precedence) for more information.

## Global flags

These options apply to the base `codex` command and propagate to each subcommand unless a section below specifies otherwise.
When you run a subcommand, place global flags after it (for example, `codex exec --oss ...`) so Codex applies them as intended.

## Command overview

The Maturity column uses feature maturity labels such as Experimental, Beta,
  and Stable. See [Feature Maturity](https://developers.openai.com/codex/feature-maturity) for how to
  interpret these labels.

## Command details

### `codex` (interactive)

Running `codex` with no subcommand launches the interactive terminal UI (TUI). The agent accepts the global flags above plus image attachments. Web search defaults to cached mode; use `--search` to switch to live browsing. For low-friction local work, use `--sandbox workspace-write --ask-for-approval on-request`.

Use `--remote ws://host:port` or `--remote wss://host:port` to connect the TUI to an app server started with `codex app-server --listen ws://IP:PORT`. Add `--remote-auth-token-env ` when the server requires a bearer token for WebSocket authentication.

### `codex app-server`

Launch the Codex app server locally. This is primarily for development and debugging and may change without notice.

`codex app-server --listen stdio://` keeps the default JSONL-over-stdio behavior. `--listen ws://IP:PORT` enables WebSocket transport for app-server clients. The server accepts `ws://` listen URLs; use TLS termination or a secure proxy when clients connect with `wss://`. Use `--listen unix://` to accept WebSocket handshakes on Codex's default Unix socket, or `--listen unix:///absolute/path.sock` to choose a socket path. If you generate schemas for client bindings, add `--experimental` to include gated fields and methods.

### `codex remote-control`

Ensure the app-server daemon is running with remote-control support enabled.
Managed remote-control clients and SSH remote workflows use this command; it's
not a replacement for `codex app-server --listen` when you are building a local
protocol client.

### `codex app`

Launch Codex Desktop from the terminal on macOS or Windows. On macOS, Codex can open a specific workspace path; on Windows, Codex prints the path to open.

`codex app` opens an installed Codex Desktop app, or starts the installer when
the app is missing. On macOS, Codex opens the provided workspace path; on
Windows, it prints the path to open after installation.

### `codex debug app-server send-message-v2`

Send one message through app-server's V2 thread/turn flow using the built-in app-server test client.

This debug flow initializes with `experimentalApi: true`, starts a thread, sends a turn, and streams server notifications. Use it to reproduce and inspect app-server protocol behavior locally.

### `codex debug models`

Print the raw model catalog Codex sees as JSON.

Use `--bundled` when you want to inspect only the catalog bundled with the current binary, without refreshing from the remote models endpoint.

### `codex apply`

Apply the most recent diff from a Codex cloud task to your local repository. You must authenticate and have access to the task.

Codex prints the patched files and exits non-zero if `git apply` fails (for example, due to conflicts).

### `codex cloud`

Interact with Codex cloud tasks from the terminal. The default command opens an interactive picker; `codex cloud exec` submits a task directly, and `codex cloud list` returns recent tasks for scripting or quick inspection.

Authentication follows the same credentials as the main CLI. Codex exits non-zero if the task submission fails.

#### `codex cloud list`

List recent cloud tasks with optional filtering and pagination.

Plain-text output prints a task URL followed by status details. Use `--json` for automation. The JSON payload contains a `tasks` array plus an optional `cursor` value. Each task includes `id`, `url`, `title`, `status`, `updated_at`, `environment_id`, `environment_label`, `summary`, `is_review`, and `attempt_total`.

### `codex completion`

Generate shell completion scripts and redirect the output to the appropriate location, for example `codex completion zsh > "${fpath[1]}/_codex"`.

### `codex features`

Manage feature flags stored in `~/.codex/config.toml`. The `enable` and `disable` commands persist changes so they apply to future sessions. When you launch with `--profile`, Codex writes to that profile instead of the root configuration.

### `codex exec`

Use `codex exec` (or the short form `codex e`) for scripted or CI-style runs that should finish without human interaction.

Codex writes formatted output by default. Add `--json` to receive newline-delimited JSON events (one per state change). The optional `resume` subcommand lets you continue non-interactive tasks. Use `--last` to pick the most recent session from the current working directory, or add `--all` to search across all sessions:

### `codex execpolicy`

Check `execpolicy` rule files before you save them. `codex execpolicy check` accepts one or more `--rules` flags (for example, files under `~/.codex/rules`) and emits JSON showing the strictest decision and any matching rules. Add `--pretty` to format the output. The `execpolicy` command is currently in preview.

### `codex login`

Authenticate the CLI with a ChatGPT account, API key, or access token. With no flags, Codex opens a browser for the ChatGPT OAuth flow.

`codex login status` exits with `0` when credentials are present, which is helpful in automation scripts.

### `codex logout`

Remove saved credentials for both API key and ChatGPT authentication. This command has no flags.

### `codex mcp`

Manage Model Context Protocol server entries stored in `~/.codex/config.toml`.

The `add` subcommand supports both stdio and streamable HTTP transports:

OAuth actions (`login`, `logout`) only work with streamable HTTP servers (and only when the server supports OAuth).

### `codex plugin marketplace`

Manage plugin marketplace sources that Codex can browse and install from.

`codex plugin marketplace add` accepts GitHub shorthand such as `owner/repo` or
`owner/repo@ref`, HTTP or HTTPS Git URLs, SSH Git URLs, and local marketplace
root directories. Use `--ref` to pin a Git ref, and repeat `--sparse PATH` to
use a sparse checkout for Git-backed marketplace repositories.

### `codex mcp-server`

Run Codex as an MCP server over stdio so that other tools can connect. This command inherits global configuration overrides and exits when the downstream client closes the connection.

### `codex resume`

Continue an interactive session by ID or resume the most recent conversation. `codex resume` scopes `--last` to the current working directory unless you pass `--all`. It accepts the same global flags as `codex`, including model and sandbox overrides.

### `codex fork`

Fork a previous interactive session into a new thread. By default, `codex fork` opens the session picker; add `--last` to fork your most recent session instead.

### `codex sandbox`

Use the sandbox helper to run a command under the same policies Codex uses internally.

#### macOS seatbelt

#### Linux Landlock

#### Windows

### `codex update`

Check for and apply a Codex CLI update when the installed release supports self-update. Debug builds print a message telling you to install a release build instead.

## Flag combinations and safety tips

- Use `--sandbox workspace-write` for unattended local work that can stay inside the workspace, and avoid `--dangerously-bypass-approvals-and-sandbox` unless you are inside a dedicated sandbox VM.
- When you need to grant Codex write access to more directories, prefer `--add-dir` rather than forcing `--sandbox danger-full-access`.
- Pair `--json` with `--output-last-message` in CI to capture machine-readable progress and a final natural-language summary.

## Related resources

- [Codex CLI overview](https://developers.openai.com/codex/cli): installation, upgrades, and quick tips.
- [Config basics](https://developers.openai.com/codex/config-basic): persist defaults like the model and provider.
- [Advanced Config](https://developers.openai.com/codex/config-advanced): profiles, providers, sandbox tuning, and integrations.
- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md): conceptual overview of Codex agent capabilities and best practices.
