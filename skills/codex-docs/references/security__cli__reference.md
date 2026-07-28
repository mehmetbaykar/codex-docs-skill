---
title: Codex Security CLI reference
source: https://learn.chatgpt.com/docs/security/cli/reference
path: /docs/security/cli/reference
---

# Codex Security CLI reference

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

Use this reference to check the supported `codex-security` commands, flags,
output formats, and exit behavior. For a guided first scan, start with the
[CLI quickstart](https://learn.chatgpt.com/docs/security/cli).

The Codex Security CLI is in beta and requires access. Follow the installation
  instructions provided with your access.

When you install the package in a local project, invoke the executable as
`npx codex-security`. Use `codex-security` directly when the executable is
available on your `PATH`.

## Command overview

```text
usage: codex-security [--version] <command> [options]
```

The CLI provides these commands:

| Command                       | Purpose                                               |
| ----------------------------- | ----------------------------------------------------- |
| `codex-security scan`         | Run a Codex Security scan.                            |
| `codex-security install-hook` | Install a Git pre-commit security scan.               |
| `codex-security bulk-scan`    | Discover repositories and run resumable bulk scans.   |
| `codex-security scans`        | List, inspect, match, rerun, and compare saved scans. |
| `codex-security export`       | Export completed findings as CSV, JSON, or SARIF.     |
| `codex-security validate`     | Check one or more candidate security findings.        |
| `codex-security patch`        | Patch one or more security issues.                    |
| `codex-security login`        | Sign in, store credentials, or check sign-in status.  |
| `codex-security logout`       | Remove the stored sign-in.                            |
| `codex-security info`         | Show read-only SDK and bundled-plugin metadata.       |

The CLI also provides these integration commands:

| Command                      | Purpose                               |
| ---------------------------- | ------------------------------------- |
| `codex-security completions` | Generate shell completion scripts.    |
| `codex-security mcp`         | Register the CLI as an MCP server.    |
| `codex-security skills`      | Sync Codex Security skills to agents. |

Run `codex-security --help` for root help, or place `--help` after a command for
its full options:

```bash
npx codex-security --help
npx codex-security scan --help
npx codex-security install-hook --help
npx codex-security bulk-scan --help
npx codex-security scans --help
npx codex-security export --help
npx codex-security info --json
```

`codex-security --version` prints the installed version and exits.
`codex-security info --json` reports the SDK and bundled-plugin versions.
Neither command requires Python.

### Discover commands and connect agents

Inspect the agent-readable command manifest, scan argument schema, and shell
completion scripts:

```bash
npx codex-security --llms
npx codex-security scan --schema --format json
npx codex-security completions bash
npx codex-security completions zsh
npx codex-security completions fish
```

Scan results support `--format toon|json|yaml|jsonl` and `--full-output`. This
framework-level `--format` is separate from `--export-format`, which selects
the format of an artifact exported from a completed scan. Global command help
also lists `md`, but scan results don't support Markdown output.

Register the CLI as an MCP server or sync its agent skills:

```bash
npx codex-security mcp add
npx codex-security skills add
```

MCP exposes only the read-only `info` metadata command. Scans, exports,
authentication, validation, and patching remain CLI-only.

## `codex-security scan`

Run a scan against a repository, selected paths, committed changes, or the
working tree.

```text
usage: codex-security scan [-h] [--path PATH | --diff BASE | --working-tree]
                           [--head HEAD] [--base BASE]
                           [--knowledge-base PATH]
                           [--mode {standard,deep}] [--model MODEL]
                           [--output-dir DIR]
                           [--archive-existing]
                           [--plugin-path PATH] [--python PATH]
                           [--codex KEY=VALUE] [--fail-on-severity LEVEL]
                           [--max-cost USD] [--dry-run] [--json] [repository]
```

`repository` defaults to the current directory.

### Select the scan target

Choose one target type for each scan.

| Argument                 | Description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| `--path PATH`            | Scan a path relative to the repository. Repeat the flag for more paths.         |
| `--diff BASE`            | Scan committed changes from `BASE` to `--head`. The head defaults to `HEAD`.    |
| `--head HEAD`            | Set the head revision for `--diff`.                                             |
| `--working-tree`         | Scan staged and unstaged changes against `--base`. The base defaults to `HEAD`. |
| `--base BASE`            | Set the base revision for `--working-tree`.                                     |
| `--mode {standard,deep}` | Select the scan mode. The default is `standard`.                                |

`--path`, `--diff`, and `--working-tree` are mutually exclusive. `--head`
requires `--diff`, and `--base` requires `--working-tree`. Deep mode supports
repository and path targets.

Diff and working-tree scans require the repository argument to be the Git
worktree root. The selected refs must exist in that checkout.

Examples:

```bash
npx codex-security scan .
npx codex-security scan . --path src --path tests
npx codex-security scan . --diff origin/main --head HEAD
npx codex-security scan . --working-tree --base HEAD
npx codex-security scan . --mode deep
```

### Add security context

Use `--knowledge-base PATH` to provide architecture documents, threat models,
or security policies. Repeat the option for more files or directories:

```bash
npx codex-security scan . \
  --knowledge-base /path/to/architecture.md \
  --knowledge-base /path/to/security-policies
```

Supported documents include `.md`, `.markdown`, `.txt`, `.pdf`, and `.docx`
files. The CLI searches directories recursively, rejects linked input paths,
skips linked directory entries, and keeps extracted document content
outside the saved scan results.

### Set output and policy options

Use these options to keep artifacts, preserve earlier results, or create a
machine-readable result.

| Argument                   | Description                                                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `--output-dir DIR`         | Write scan artifacts to a private directory outside the enclosing Git worktree. Defaults to persistent Codex Security state. |
| `--archive-existing`       | Move existing results to `DIR.previous-<timestamp>-<id>` and start with an empty output directory. Requires `--output-dir`.  |
| `--fail-on-severity LEVEL` | Return exit `1` when a completed scan reports a finding at or above `critical`, `high`, `medium`, or `low`.                  |
| `--max-cost USD`           | Stop a scan when its estimated model cost exceeds the specified USD amount.                                                  |
| `--dry-run`                | Check the repository, target, output directory, and Codex configuration without starting a scan.                             |
| `--json`                   | Print manifest, findings, coverage, paths, and turn metadata as one JSON document.                                           |

The cost limit is an estimate, not a hard spending cap. Requests already in
progress can finish above the limit, and partial scan results remain available.

When you omit `--output-dir`, results persist under
`$CODEX_HOME/state/plugins/codex-security/scans/<repository>`. `CODEX_HOME`
defaults to `~/.codex`. Set `CODEX_SECURITY_STATE_DIR` to keep results under
`$CODEX_SECURITY_STATE_DIR/scans/<repository>` instead. These directories can
contain source excerpts and vulnerability details, so manage their permissions
and retention accordingly.

The output directory can be new or empty. On macOS and Linux, an existing
directory must be private to the current user. A scan can replace an existing
result directory with `--archive-existing`.

```bash
npx codex-security scan . \
  --output-dir /path/outside/repository/results \
  --archive-existing
```

Scans are report-only by default. Add `--fail-on-severity` to evaluate a
severity policy in CI:

```bash
npx codex-security scan . \
  --diff origin/main \
  --output-dir /path/outside/repository/results \
  --json \
  --fail-on-severity high \
  > /path/outside/repository/codex-security.json
```

A dry run checks local inputs without loading credentials, starting Codex, or
probing the plugin's Python interpreter:

```bash
npx codex-security scan . --output-dir /path/outside/repository/results --dry-run
```

### Configure the runtime

Use runtime options when you need an explicit model, interpreter, plugin, or
Codex configuration value.

| Argument             | Description                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| `--model MODEL`      | Select the model for the scan.                                                                           |
| `--plugin-path PATH` | Use a Codex Security plugin directory or ZIP to override the bundled plugin.                             |
| `--python PATH`      | Select the Python interpreter for the plugin runtime.                                                    |
| `--codex KEY=VALUE`  | Override an isolated Codex configuration value. Values use TOML syntax. Repeat the flag for more values. |

Quote string values passed through `--codex` so the TOML parser receives a
string:

```bash
npx codex-security scan . --codex 'model="<model>"'
```

Codex Security owns plugin-loading configuration and rejects conflicting
overrides. Use `--plugin-path` to select a plugin.

## `codex-security install-hook`

Install a Git pre-commit security check for the current repository:

```bash
npx codex-security install-hook
```

The check scans staged and unstaged changes before each commit and blocks
high-severity findings or scan errors. It respects `core.hooksPath` and does
not replace an existing pre-commit script. Set a different severity threshold
when needed:

```bash
npx codex-security install-hook . --fail-on-severity medium
```

## `codex-security bulk-scan`

Discover and scan GitHub repositories, or run a resumable scan from a
repository CSV:

```text
usage: codex-security bulk-scan [input] [--output-dir DIR]
                                [--workers N] [--mode {standard,deep}]
                                [--max-attempts N] [--plugin-path PATH]
                                [--python PATH] [--codex KEY=VALUE]
```

Run `codex-security bulk-scan` without arguments or options to select
repositories interactively. This flow requires a GitHub CLI sign-in.

For a prepared repository list, provide a CSV and `--output-dir`:

```bash
npx codex-security bulk-scan repositories.csv \
  --output-dir /path/outside/repositories/security-scans \
  --workers 4
```

The CSV requires `id`, `repository`, and `revision` columns. Revisions must be
full commit hashes. Optional `scope` and `mode` columns configure individual
repositories:

```csv
id,repository,revision,scope,mode
service,https://github.com/example/service.git,0123456789abcdef0123456789abcdef01234567,src,standard
```

`--workers` limits simultaneous scans and defaults to `4`. `--mode` defaults to
`standard`, and `--max-attempts` defaults to `1`. Run the same command again to
resume a bulk scan from its existing output directory.

For containerized campaigns, see [Run bulk scans in
Docker](https://learn.chatgpt.com/docs/security/cli#run-bulk-scans-in-docker).

## `codex-security scans`

List, inspect, rerun, match, and compare saved scans:

```bash
npx codex-security scans
npx codex-security scans list /path/to/repository
npx codex-security scans list --scan-root /path/outside/repository/results
npx codex-security scans show SCAN_ID
npx codex-security scans rerun SCAN_ID
npx codex-security scans match PREVIOUS_SCAN_ID CURRENT_SCAN_ID
npx codex-security scans match --all
npx codex-security scans compare PREVIOUS_SCAN_ID CURRENT_SCAN_ID
```

`scans` defaults to `scans list` for the current directory. Pass a repository
path or `--scan-root` to select a different checkout or scan-output root.

`show` includes saved results and configuration. `rerun` applies the original
configuration to the current checkout. `match` links findings with the same
root cause, and `match --all` matches completed scans of the same repository
across checkouts. `compare` uses saved matches to classify findings as new,
persisting, reopened, resolved, or unknown. It reports a missing finding as
unknown when the later scan has incomplete coverage or doesn't cover the
finding's original location.

## `codex-security export`

Export CSV, JSON, or SARIF from a completed, sealed scan. Export validates the
scan artifacts before writing output and leaves the Codex runtime and
credentials untouched.

```text
usage: codex-security export [--export-format {csv,json,sarif}]
                             [--output FILE|-] [--source-root PATH]
                             [--python PATH] scan_dir
```

`scan_dir` is the completed scan directory.

| Argument                           | Description                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| `--export-format {csv,json,sarif}` | Select the export format. The default is `sarif`.                                           |
| `--output FILE\|-`                 | Write the selected format to a file or stdout. Defaults to a file in the current directory. |
| `--source-root PATH`               | Add source-line fingerprints to SARIF using a repository checkout.                          |
| `--python PATH`                    | Select the Python interpreter for the bundled exporter.                                     |

`--source-root` works only with `--export-format sarif`. JSON preserves
the sealed findings document. CSV contains portable finding columns and does
not include local workbench triage state.

Without `--output`, the CLI writes SARIF to `results.sarif`, JSON to
`findings.json`, and CSV to `findings.csv` in the current working directory.
Exports can contain source excerpts and vulnerability details. Run the command
outside the repository or pass `--output` with a private path outside the
scanned checkout.

Write SARIF to a file:

```bash
npx codex-security export /path/to/scan \
  --export-format sarif \
  --source-root /path/to/repository \
  --output /path/outside/repository/exports/results.sarif
```

Write SARIF to stdout:

```bash
npx codex-security export /path/to/scan --export-format sarif --source-root . --output -
```

Export JSON or CSV:

```bash
npx codex-security export /path/to/scan \
  --export-format json \
  --output /path/outside/repository/exports/findings.json
npx codex-security export /path/to/scan \
  --export-format csv \
  --output /path/outside/repository/exports/findings.csv
```

## `codex-security validate` and `codex-security patch`

Use `validate` to run the bundled validation skill on candidate findings. Use
`patch` to run the bundled remediation skill on security issues:

```bash
npx codex-security validate findings.json "Possible SQL injection in src/query.ts:42"
npx codex-security patch findings.json "Missing authorization check in src/routes.ts:18"
```

Each argument can contain literal text or point to a file. Both commands work
against the current directory. External tools can use these commands without
rebuilding the scanner.

## `codex-security login`, `logout`, and `info`

Sign in interactively or use device authentication on a remote or headless
machine:

```bash
npx codex-security login
npx codex-security login --device-auth
npx codex-security login status
npx codex-security logout
```

Store an API key or enterprise access token by passing it on stdin:

```bash
printenv OPENAI_API_KEY | npx codex-security login --with-api-key
printenv CODEX_ACCESS_TOKEN | npx codex-security login --with-access-token
```

Use `codex-security info --json` for read-only SDK and bundled-plugin metadata.
When you expose the CLI as an MCP server, `info` is the only available command;
scans, exports, sign-in, validation, and patching remain CLI-only.

## Read scan output

The CLI writes structured command results to stdout and sends progress,
completion summaries, and errors to stderr. This lets terminal users read a
summary while automation captures a clean JSON or SARIF document.

### Completion summary

A completed scan writes its finding count, severity breakdown, coverage,
elapsed time, result directory, and next step to stderr. It includes worker
counts and token usage when available:

```text
codex-security: Findings: 4 (1 critical, 2 high, 1 informational). Coverage: complete.
codex-security: Elapsed: 1s. Workers: 3/6.
codex-security: Tokens: 1,250 input, 200 cached, 30 output.
codex-security: Results: /path/to/scan
codex-security: Next: codex-security export /path/to/scan --export-format sarif
```

Informational findings count toward the summary total. Severity policies
evaluate only `critical`, `high`, `medium`, and `low` findings.

### JSON output

`scan --json` writes one complete JSON document to stdout. Its top-level shape
is:

```text
manifest
findings
coverage
scanDir
threadId
reportPath
artifactsDir
sarifPath
turn
  id
  status
  durationMs
  finalResponse
  usage
```

Progress, completion summaries, archive notices, and errors remain on stderr.
A completed scan still prints the full JSON result when a severity policy
returns exit `1` or incomplete coverage returns exit `2`.

`codex-security scan --json` emits one JSON document. `codex exec --json`
  emits a JSON Lines event stream. Use the output format that matches the
  command you run.

## Scan artifacts

A completed scan keeps the readable report and structured artifacts together:

```text
<scan-directory>/
├── scan-manifest.json
├── findings.json
├── coverage.json
├── report.md
├── artifacts/
└── exports/
    └── results.sarif       # when produced
```

The structured files serve different jobs:

| File                    | Contents                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `scan-manifest.json`    | Scan identity, status, target, scope, producer, and sealed artifact records.                                                    |
| `findings.json`         | Finding identifiers, severity, confidence, taxonomy, locations, evidence, validation, data flow, reachability, and remediation. |
| `coverage.json`         | Reviewed surfaces, exclusions, deferred work, open questions, and coverage completeness.                                        |
| `report.md`             | Readable scan report.                                                                                                           |
| `artifacts/`            | Supporting scan artifacts.                                                                                                      |
| `exports/results.sarif` | SARIF generated during the scan, when present.                                                                                  |

Coverage completeness has three values:

- `complete`: The scan records complete coverage for its selected scope.
- `partial`: The scan records deferred work or other coverage limits.
- `unknown`: The scan reports coverage completeness as unknown.

Review deferred surfaces, explicit exclusions, and open questions before using
coverage as evidence for a security decision.

## Exit codes and signals

The CLI uses these exit codes:

| Exit  | Condition                                                                                                                                     |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`   | A scan completed with complete coverage and passed its severity policy, a bulk scan completed without failures, or another command succeeded. |
| `1`   | A completed scan reports a finding at or above the configured severity.                                                                       |
| `2`   | The CLI found an input, runtime, or export error, a scan has incomplete coverage, or a bulk scan has repositories with errors.                |
| `130` | Ctrl-C interrupted a scan.                                                                                                                    |
| `143` | SIGTERM terminated a scan.                                                                                                                    |

Any scan with `partial` or `unknown` coverage returns `2`, even without a
severity policy. Completed scans still write the available results to stdout.
The CLI prints the location of any partial output after an interruption or
runtime error.

## Authentication and prerequisites

Set `OPENAI_API_KEY` or `CODEX_API_KEY`, sign in with `codex-security login`, or
use an existing file-backed Codex sign-in. Environment API keys take precedence
over stored credentials. For CI, keep the API key scoped to the scan step and
use a trusted workflow.

The CLI requires Node.js 22 or later. Running a scan or exporting findings also
requires Python 3.10 or later. Python 3.10 also requires `tomli`. Use `--python`
or `PYTHON` to select an interpreter when automatic discovery is unsuitable.

Continue with the [CLI quickstart](https://learn.chatgpt.com/docs/security/cli), [CI
guide](https://learn.chatgpt.com/docs/security/cli/ci), or [TypeScript SDK
guide](https://learn.chatgpt.com/docs/security/sdk).

### Plain-text aliases

- --output FILE|-
