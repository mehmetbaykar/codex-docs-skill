---
title: "Configuration Reference"
source: https://learn.chatgpt.com/docs/config-file/config-reference
path: /docs/config-file/config-reference
---

# Configuration Reference

Use this page as a searchable reference for Codex configuration files. For conceptual guidance and examples, start with [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) and [Advanced Config](https://learn.chatgpt.com/docs/config-file/config-advanced).

<a id="settings-for-synced-chatgpt-work"></a>

## Settings for Local computer access with Work Cloud

With Local computer access with Work Cloud enabled, OpenAI's cloud coordinates the task while supported tools run in the cloud or on a connected computer. Requirements set limits; configuration values provide defaults.

Use the policy API to manage Global settings. To manage Local or Codex Cloud settings, use the Agent Security UI. Existing Global API workflows remain available after migration. Test your scripts and Terraform integrations, and confirm that policy assignments and ordering are unchanged. Support for a `requirements.toml` field does not by itself establish API compatibility.

| Setting or setting family                                           | Scope in Local computer access with Work Cloud                                                                                   | Guidance                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Approval policies and review requirements                           | Global orchestrator policy when managed policy is enabled                                                                        | Keep approval and review controls in Global. Environment overrides cannot change orchestrator controls. Local execution and cloud-container execution have separate policy scopes.                                                                                                                                                                                                                                                                  |
| Managed apps, MCP servers, plugins, marketplaces, and command rules | Global policy                                                                                                                    | Keep these controls global. Do not treat the field's presence in a schema as proof that the field can be edited per environment.                                                                                                                                                                                                                                                                                                                    |
| File, sandbox, and portable network requirements                    | Local execution                                                                                                                  | For local execution, MDM and legacy managed-device requirements rank above Agent Security. The device's system requirements file ranks below Agent Security. The new enterprise `requirements.toml` configuration does not apply to Work cloud containers, which retain existing Work Cloud policies.                                                                                                                                               |
| Platform-specific executor controls                                 | Computer running the step                                                                                                        | Support depends on the executor and platform.                                                                                                                                                                                                                                                                                                                                                                                                       |
| Managed hooks                                                       | Where enabled, admin-defined MCP hooks that run on the cloud coordinator (orchestrator) for supported lifecycle and tool events. | Before relying on these hooks, test the callback connection, confirm the events it receives, and check how failures affect the task. MCP hooks do not provide a complete Compliance API audit trail. Command, local-config, and plugin hooks are unsupported with cloud orchestration, even when tools execute locally. Existing supported hooks still apply to local-only Work and Codex threads where orchestration and execution are both local. |
| Proxy listener addresses, ports, and process settings               | Not portable environment policy                                                                                                  | Managed HTTP/SOCKS listener ports and non-loopback proxy listeners are unsupported by the cloud runtime; socket-rule support depends on the execution path. Custom proxy configuration is separate from supported destination restrictions.                                                                                                                                                                                                         |
| App-only settings and ordinary local defaults                       | Not necessarily consumed by cloud coordination                                                                                   | App-enforced controls can remain effective even when Local computer access with Work Cloud does not consume them. Cloud delivery and cloud-browser behavior need separate validation.                                                                                                                                                                                                                                                               |

<a id="agent-security-requirements-used-by-work-cloud"></a>

<a id="agent-security-requirements-for-synced-work"></a>

### Agent Security requirements for Local computer access with Work Cloud

For Work with local access and dots, supported Global policy applies to the shared cloud orchestrator when managed policy is enabled. Local execution requirements govern the connected computer. Work cloud containers and dots cloud computers use their own execution configuration and requirements. Test local and cloud controls separately.

#### Exposed in the Agent Security UI

- Allowed approval policies
- Allowed web search modes

#### Configured through TOML

- `allowed_approvals_reviewers`
- `auto_review`
- `guardian_policy_config`
- `apps`
- `mcp_servers`
- `plugins`
- `rules`

These orchestrator requirements stay in Global. They do not configure shared cloud capability permissions or make local execution settings portable to Work cloud containers or dots cloud computers.

<a id="work-sync-compatibility-limits"></a>

<a id="local-computer-access-compatibility-limits"></a>

### Local computer access with Work Cloud compatibility limits

Support depends on the field, how the policy is delivered, and where the task runs. Check the member's effective policy before enabling sync. Some controls need to be tested in your deployment, as noted in the table.

Within a policy, the order from highest to lowest is OS-specific environment override → all-OS environment override → Global. A higher-priority policy wins even when a lower-priority policy is more specific.

For local execution, MDM and legacy managed-device requirements take precedence over Agent Security, which takes precedence over the device's system requirements file. Some requirements, including network requirements, have field-specific merge rules and runtime limits. See [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) for examples.

| **Setting or family**                                                                              | **Local computer access with Work Cloud compatibility**                                                               | **Admin guidance**                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sqlite_home`, `log_dir`, `model_catalog_json`                                                     | Not supported as managed cloud overrides.                                                                             | Local paths cannot move cloud storage or logs. A local model catalog does not carry over.                                                                                                                                                                                             |
| `model_provider`, `model_providers`                                                                | Not supported in managed Local computer access with Work Cloud requirements or configuration.                         | Custom inference gateways and provider connections do not carry over through these fields. This is separate from model selection.                                                                                                                                                     |
| `enforce_residency`                                                                                | Blocks Local computer access with Work Cloud when enabled in any cloud policy.                                        | If `enforce_residency` is enabled in any cloud policy, **Allow local computer access** is disabled for both Work and dots. This safeguard does not configure workspace residency or, by itself, disable Work Cloud or dots.                                                           |
| `application.network.enabled` and `application.network.domains`                                    | Not supported by Local computer access with Work Cloud.                                                               | Do not use these application-destination restrictions as Local computer access with Work Cloud command-networking controls.                                                                                                                                                           |
| `allow_browser_and_computer_use`, `in_app_browser`, `additional_developer_instructions`            | Cloud policy delivery needs validation. Local computer access with Work Cloud rejects these managed requirement keys. | Browser restrictions have app-side checks. That does not prove cloud delivery or cloud-browser enforcement. `additional_developer_instructions` requires orchestrator support.                                                                                                        |
| `experimental_network` and `permissions.<profile>.network`                                         | Partial. Supported destination and executor restrictions differ from custom proxy configuration.                      | Managed HTTP/SOCKS listener ports and non-loopback proxy listeners are unsupported by the cloud runtime; socket-rule support depends on the execution path. Local-execution merge behavior is separate. Command-network restrictions do not disable hosted search, MCP, or app tools. |
| features / `feature_requirements`, models, `computer_use`                                          | Partial.                                                                                                              | Retired switches such as `tool_search` = false, `tool_search_always_defer_mcp_tools` = false, `js_repl` = true, and `remote_control` = true are rejected. Some computer-use settings still need end-to-end validation.                                                                |
| `browser_use`, `allow_appshots`, feedback, `allow_remote_control`, marketplace source restrictions | The app or app-server enforces these controls on some policy delivery paths.                                          | App controls can still apply when Local computer access with Work Cloud ignores a field. Desktop browser site rules do not apply to Work cloud containers. Validate the actual surface and policy delivery path.                                                                      |

The configuration schema includes keys that may not work with Local computer access with Work Cloud or support environment overrides. See [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration) for the global baseline and precedence.

## `config.toml`

User-level configuration lives in `~/.codex/config.toml`. You can also add project-scoped overrides in `.codex/config.toml` files. Codex loads project-scoped config files only when you trust the project.

Project-scoped config can't override machine-local provider, auth,
host-owned app request metadata, notification, configuration profile selection,
or telemetry routing keys. Codex ignores `openai_base_url`,
`chatgpt_base_url`, `apps_mcp_product_sku`, `model_provider`,
`model_providers`, `notify`, `profile`, `profiles`,
`experimental_realtime_ws_base_url`, and `otel` when they appear in a
project-local `.codex/config.toml`; put provider, notification, and telemetry
keys in user-level config instead. Config [profile files](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles) live next to
`config.toml` as `$CODEX_HOME/profile-name.config.toml`; select one with
`--profile profile-name`.

For sandbox and approval keys (`approval_policy`, `sandbox_mode`, and `sandbox_workspace_write.*`), pair this reference with [Sandbox and approvals](https://learn.chatgpt.com/docs/agent-approvals-security#sandbox-and-approvals), [Protected paths in writable roots](https://learn.chatgpt.com/docs/agent-approvals-security#protected-paths-in-writable-roots), and [Network access](https://learn.chatgpt.com/docs/agent-approvals-security#network-access). For beta permission profiles, see [Permissions](https://learn.chatgpt.com/docs/permissions).

Codex and ChatGPT Work no longer support `approval_policy = "untrusted"`.
Remove the setting or choose a supported policy. Project entries with
`trust_level = "untrusted"` in user-level `~/.codex/config.toml` remain supported. See
[Migrate from the retired `untrusted` approval policy](https://learn.chatgpt.com/docs/agent-approvals-security#migrate-from-the-retired-untrusted-approval-policy)
for examples and approval tradeoffs.

Set `model` to one available to your signed-in account or workspace. See
[GPT-6.1 Sol availability](https://learn.chatgpt.com/docs/models#gpt-6.1-sol) before using the example value.

- model: Model to use (e.g., `gpt-6.1-sol`). (Type: string)
- review_model: Optional model override used by `/review` (defaults to the current session model). (Type: string)
- model_provider: Provider id from `model_providers` (default: `openai`). (Type: string)
- openai_base_url: Base URL override for the built-in `openai` model provider. (Type: string)
- model_context_window: Context window tokens available to the active model. (Type: number)
- model_auto_compact_token_limit: Token threshold that triggers automatic history compaction (unset uses model defaults). (Type: number)
- model_auto_compact_token_limit_scope: Controls whether the auto-compaction threshold counts the full active context (`total`, the default) or only growth after the carried compaction-window prefix (`body_after_prefix`). (Type: total | body_after_prefix)
- model_post_turn_compact_threshold_percent: Compact history after a final response when active context reaches this percentage of the usable context window. Omit or set to `0` to disable turn-end compaction. The usual auto-compaction limits still apply. (Type: integer (0–100))
- model_catalog_json: Optional path to a JSON model catalog loaded on startup. A selected `$CODEX_HOME/profile-name.config.toml` profile file can override this per profile. (Type: string (path))
- oss_provider: Default local provider used when running with `--oss` (defaults to prompting if unset). (Type: lmstudio | ollama)
- approval_policy: Controls when Codex pauses for approval before executing commands. You can also use `approval_policy = { granular = { ... } }` to allow or auto-reject specific prompt categories while keeping other prompts interactive. `untrusted` is unsupported, and `on-failure` is deprecated; use `on-request` for interactive runs or `never` for non-interactive runs. (Type: on-request | never | { granular = { sandbox_approval = bool, rules = bool, mcp_elicitations = bool, request_permissions = bool, skill_approval = bool } })
- approval_policy.granular.sandbox_approval: When `true`, sandbox escalation approval prompts are allowed to surface. (Type: boolean)
- approval_policy.granular.rules: When `true`, approvals triggered by execpolicy `prompt` rules are allowed to surface. (Type: boolean)
- approval_policy.granular.mcp_elicitations: When `true`, MCP elicitation prompts are allowed to surface instead of being auto-rejected. (Type: boolean)
- approval_policy.granular.request_permissions: When `true`, prompts from the `request_permissions` tool are allowed to surface. (Type: boolean)
- approval_policy.granular.skill_approval: When `true`, skill-script approval prompts are allowed to surface. (Type: boolean)
- approvals_reviewer: Who reviews eligible approval prompts under `on-request` or granular approval policies. Defaults to `user`; `auto_review` uses the reviewer subagent. This setting doesn't change sandboxing or review actions already allowed inside the sandbox. (Type: user | auto_review)
- auto_review.policy: Local Markdown policy instructions for automatic review. Managed `guardian_policy_config` takes precedence. Blank values are ignored. (Type: string)
- auto_review.extra_policy: Additional local Markdown policy for automatic review, included alongside the main policy. Managed `guardian_extra_policy` takes precedence. Blank values are ignored. (Type: string)
- allow_login_shell: Allow shell-based tools to use login-shell semantics. Defaults to `true`; when `false`, `login = true` requests are rejected and omitted `login` defaults to non-login shells. (Type: boolean)
- allow_symlinked_codex_home: On macOS, allow writable sandbox roots at or under `$CODEX_HOME` to follow symlinks. Codex reads this only from the execution host's `$CODEX_HOME/config.toml` at startup. Enabling it trusts targets outside that directory and targets that change between commands. It grants no additional writable roots. Defaults to `false`. (Type: boolean)
- sandbox_mode: Sandbox policy for filesystem and network access during command execution. (Type: read-only | workspace-write | danger-full-access)
- sandbox_workspace_write.writable_roots: Additional writable roots when `sandbox_mode = "workspace-write"`. (Type: array<string>)
- sandbox_workspace_write.network_access: Allow outbound network access inside the workspace-write sandbox. (Type: boolean)
- sandbox_workspace_write.exclude_tmpdir_env_var: Exclude `$TMPDIR` from writable roots in workspace-write mode. (Type: boolean)
- sandbox_workspace_write.exclude_slash_tmp: Exclude `/tmp` from writable roots in workspace-write mode. (Type: boolean)
- windows.sandbox: Native Windows sandbox implementation. Explicit `mxc` selection fails when MXC is unavailable or prohibited by managed requirements. Use `features.prefer_mxc` with a legacy selection for automatic MXC selection with fallback. (Type: mxc | elevated | unelevated)
- browser_use.allow_history_access: Set to `false` to restrict browser-history access. Managed requirements can enforce this restriction. (Type: boolean)
- browser_use.default_origin_policy: Fallback browser-origin restrictions. Supports `access`, `uploads`, `downloads`, and `full_cdp_access`, each set to `allow` or `deny`. (Type: table)
- browser_use.origins.<origin>: Per-origin browser restrictions with the same fields as `browser_use.default_origin_policy`. Include an HTTP or HTTPS scheme and optional port; omit paths, queries, and fragments. Local values cannot relax managed denies. (Type: table)
- computer_use.default_app_access: Fallback native-app access policy for Computer Use. App-specific entries can supply a policy; local configuration cannot relax managed restrictions. (Type: allow | deny)
- computer_use.macos.bundle_ids: Native macOS app access keyed by bundle identifier. (Type: map<string, allow | deny>)
- computer_use.windows.aumids: Packaged Windows app access keyed by Application User Model ID (AUMID). (Type: map<string, allow | deny>)
- computer_use.windows.exes: Windows executable access rules. Each rule requires `publisher_name`, `product_name`, and `access` (`allow` or `deny`); `binary_name` is optional. (Type: array<table>)
- computer_use.windows.always_allowed_app_ids: Windows app identifiers that Computer Use can open without prompting. Apps not in the list require approval; remove saved entries from the ChatGPT desktop app's Computer Use settings. (Type: array<string>)
- notify: Command invoked for notifications; receives a JSON payload from Codex. (Type: array<string>)
- check_for_update_on_startup: Check for Codex updates on startup (set to false only when updates are centrally managed). (Type: boolean)
- feedback.enabled: Enable feedback submission via `/feedback` across local clients (default: true). (Type: boolean)
- analytics.enabled: Enable or disable analytics for this machine or profile. Setting this to `false` disables the built-in Statsig metrics exporter. Explicit OTLP metrics exporters remain active. When unset, the client default applies. (Type: boolean)
- instructions: Reserved for future use; prefer `model_instructions_file` or `AGENTS.md`. (Type: string)
- developer_instructions: Additional developer instructions injected into the session (optional). (Type: string)
- log_dir: Directory where Codex writes log files; defaults to `$CODEX_HOME/log`. Setting this explicitly also enables the opt-in plaintext TUI log, `codex-tui.log`, in that directory. (Type: string (path))
- sqlite_home: Directory where Codex stores the SQLite-backed state DB used by agent jobs and other resumable runtime state. (Type: string (path))
- compact_prompt: Inline override for the history compaction prompt. (Type: string)
- model_instructions_file: Replacement for built-in instructions instead of `AGENTS.md`. (Type: string (path))
- personality: Deprecated compatibility setting. `friendly` and `pragmatic` no longer select a style. `none` omits the built-in Personality section from model instructions; explicit instruction overrides are unchanged. (Type: none | friendly | pragmatic)
- service_tier: Preferred service tier for new turns. Use `fast` or another tier advertised by the active model; `fast` maps to the request value `priority`. (Type: string)
- experimental_compact_prompt_file: Load the compaction prompt override from a file (experimental). (Type: string (path))
- skills.bundled.enabled: Load the system skills bundled with Codex. Defaults to `true`. Set to `false` in a trusted project configuration to disable bundled skills for that project. (Type: boolean)
- skills.include_instructions: Include the automatic skills instructions in the model context. Defaults to `true`. (Type: boolean)
- skills.max_context_tokens: Token budget for the available-skills catalog. Defaults to 2% of the model's context window. Explicit values are capped at `10000` tokens. (Type: integer (positive))
- skills.config: Enable or disable skills by name or path. If several rules match a skill, the last one wins. (Type: array<object>)
- skills.config.<index>.path: Absolute path to one `SKILL.md` file. (Type: string (path))
- skills.config.<index>.name: Match every skill with this exact name. Specify either `name` or `path` for each entry. (Type: string)
- skills.config.<index>.enabled: Enable or disable the referenced skill. (Type: boolean)
- apps.<id>.enabled: Enable or disable a specific app/connector by id (default: true). (Type: boolean)
- apps._default.enabled: Default app enabled state for all apps unless overridden per app. (Type: boolean)
- apps._default.destructive_enabled: Default allow/deny for app tools with `destructive_hint = true`. (Type: boolean)
- apps._default.open_world_enabled: Default allow/deny for app tools with `open_world_hint = true`. (Type: boolean)
- apps._default.approvals_reviewer: Default reviewer for app tool approval prompts unless overridden per app. When omitted, apps inherit the top-level `approvals_reviewer` value. (Type: user | auto_review)
- apps._default.default_tools_approval_mode: Default approval behavior for app tools without per-app or per-tool overrides. (Type: auto | prompt | writes | approve)
- apps.<id>.destructive_enabled: Allow or block tools in this app that advertise `destructive_hint = true`. (Type: boolean)
- apps.<id>.open_world_enabled: Allow or block tools in this app that advertise `open_world_hint = true`. (Type: boolean)
- apps.<id>.default_tools_enabled: Default enabled state for tools in this app unless a per-tool override exists. (Type: boolean)
- apps.<id>.approvals_reviewer: Reviewer for this app's tool approval prompts. Overrides `apps._default.approvals_reviewer`. (Type: user | auto_review)
- apps.<id>.default_tools_approval_mode: Default approval behavior for tools in this app unless a per-tool override exists. (Type: auto | prompt | writes | approve)
- apps.<id>.omit_tools_from: Omit this app's tools from the `direct`, `deferred`, or `code_mode` surfaces. App and MCP server omissions apply together. (Type: array<string>)
- apps.<id>.tools.<tool>.enabled: Per-tool enabled override for an app tool (for example `repos/list`). (Type: boolean)
- apps.<id>.tools.<tool>.approval_mode: Per-tool approval behavior override for a single app tool. (Type: auto | prompt | writes | approve)
- tool_suggest.discoverables: Allow tool suggestions for additional discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`. (Type: array<table>)
- tool_suggest.disabled_tools: Disable suggestions for specific discoverable connectors or plugins. Each entry uses `type = "connector"` or `"plugin"` and an `id`. (Type: array<table>)
- features.apps: Enable app (connector) integrations (stable; on by default). App and connector traffic is not controlled by the sandboxed-command network proxy or its domain allowlist. (Type: boolean)
- features.hooks: Enable lifecycle hooks loaded from `hooks.json` or inline `[hooks]` config. `features.codex_hooks` is a deprecated alias. (Type: boolean)
- features.code_mode.enabled: Enable code mode feature configuration. This feature is under development and off by default. (Type: boolean)
- features.code_mode.excluded_tool_namespaces: Tool namespaces code mode excludes from nested code-mode tool guidance and executor exposure. (Type: array<string>)
- features.code_mode.direct_only_tool_namespaces: Tool namespaces code mode can use only through direct tool calls. (Type: array<string>)
- features.context_management.experimental_mode: Experimental context-management setting. The feature is not currently available. (Type: boolean)
- features.rollout_budget.enabled: Enable rollout budget tracking. This feature is under development and off by default. When enabled, set both `limit_tokens` and `reminder_at_remaining_tokens`. (Type: boolean)
- features.rollout_budget.limit_tokens: Positive token limit for rollout budget tracking. Required when rollout budget is enabled. (Type: integer)
- features.rollout_budget.reminder_at_remaining_tokens: Send a reminder as the remaining weighted token budget crosses each threshold. Supply the list when rollout budget tracking is enabled. Each value must be positive and below `limit_tokens`. (Type: array<integer>)
- features.rollout_budget.sampling_token_weight: Finite non-negative multiplier for sampled tokens in rollout budget accounting. Defaults to `1.0`. (Type: number)
- features.rollout_budget.prefill_token_weight: Finite non-negative multiplier for prefill tokens in rollout budget accounting. Defaults to `1.0`. (Type: number)
- hooks: Lifecycle hooks configured inline in `config.toml`. Uses the same event schema as `hooks.json`; see the Hooks guide for examples and supported events. (Type: table)
- hooks.<Event>: Matcher groups for hook events such as `PreModelRequest`, `PostModelRequest`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`, or `Interrupt`. (Type: array<table>)
- hooks.<Event>[].hooks: Hook handlers for a matcher group. Command and MCP tool hooks are supported while prompt and agent hook handlers are parsed but skipped. (Type: array<table>)
- hooks.<Event>[].hooks[].async: Run a command hook in the background without delaying the triggering operation. Defaults to `false`; `SessionEnd` always runs synchronously. See [Run hooks in the background](https://learn.chatgpt.com/docs/hooks#run-hooks-in-the-background). (Type: boolean)
- hooks.<Event>[].hooks[].additionalContextLimit: Approximate per-handler token threshold for saving oversized `additionalContext` to disk and showing the model a shorter preview. Defaults to `2500`; `0` passes the full context directly to the model. See [Large hook output](https://learn.chatgpt.com/docs/hooks#large-hook-output). (Type: integer)
- hooks.<Event>[].hooks[].commandWindows: Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. (Type: string)
- features.memories: Enable [Memories](https://learn.chatgpt.com/docs/customization/memories) (off by default). (Type: boolean)
- mcp_optional_startup_grace_ms: Shared wait for optional MCP servers when building the initial tool catalog. Defaults to `1000`. Set to `0` to wait for each server's `startup_timeout_sec` instead. (Type: integer (milliseconds))
- mcp_servers.<id>.command: Launcher command for an MCP stdio server. (Type: string)
- mcp_servers.<id>.args: Arguments passed to the MCP stdio server command. (Type: array<string>)
- mcp_servers.<id>.env: Environment variables forwarded to the MCP stdio server. (Type: map<string,string>)
- mcp_servers.<id>.env_vars: Additional environment variables to whitelist for an MCP stdio server. String entries default to `source = "local"`; use `source = "remote"` only with executor-backed remote stdio. (Type: array<string | { name = string, source = "local" | "remote" }>)
- mcp_servers.<id>.cwd: Working directory for the MCP stdio server process. (Type: string)
- mcp_servers.<id>.url: Endpoint for an MCP streamable HTTP server. (Type: string)
- mcp_servers.<id>.auth: Authentication fallback for an MCP HTTP server after configured bearer tokens and authorization headers. `oauth` (default) uses stored MCP OAuth credentials when available. `chatgpt` uses the current ChatGPT session for the trusted first-party ChatGPT origin, then falls back to stored OAuth. Both modes can connect without authentication if no credential source resolves. (Type: oauth | chatgpt)
- mcp_servers.<id>.oauth.client_id: Pre-registered OAuth client ID used for authorization and token exchange with this MCP server. (Type: string)
- mcp_servers.<id>.oauth.client_secret: OAuth client secret for token exchange with a pre-registered client. Requires a nonempty `oauth.client_id`; the secret must also be nonempty. Stored in configuration. (Type: string)
- mcp_servers.<id>.oauth.callback_url: Server-specific OAuth callback. Pre-registered clients reuse it when issuer identification is supported or the URL already ends in the server-specific callback ID. Otherwise, Codex uses the global or default callback with that ID appended. Clients without a pre-registered ID use this callback during client registration. (Type: string)
- mcp_servers.<id>.oauth.callback_port: Fixed OAuth callback listener port for this MCP server. Overrides `mcp_oauth_callback_port`. For a direct loopback callback with an explicit URL port, configure the same listener port. (Type: integer)
- mcp_servers.<id>.bearer_token_env_var: Environment variable sourcing the bearer token for an MCP HTTP server. (Type: string)
- mcp_servers.<id>.http_headers: Static HTTP headers included with each MCP HTTP request. (Type: map<string,string>)
- mcp_servers.<id>.http_headers_helper: Local command that prints a JSON object of HTTP header names and values. Supported only for locally connected HTTP MCP servers. Explicit bearer tokens and OAuth credentials take precedence over helper-provided Authorization headers. (Type: string (command))
- mcp_servers.<id>.env_http_headers: HTTP headers populated from environment variables for an MCP HTTP server. (Type: map<string,string>)
- mcp_servers.<id>.enabled: Disable an MCP server without removing its configuration. (Type: boolean)
- mcp_servers.<id>.required: Require this enabled server to be ready at startup. With `startup_readiness = "catalog"`, a valid cached catalog can satisfy that requirement. (Type: boolean)
- mcp_servers.<id>.startup_readiness: Use a live connection to establish startup readiness (`connection`, the default), or let a valid cached tool catalog satisfy startup while the connection opens (`catalog`). Calling a tool still requires a live connection. (Type: connection | catalog)
- mcp_servers.<id>.startup_timeout_sec: Override the default 10s startup timeout for an MCP server. (Type: number)
- mcp_servers.<id>.startup_timeout_ms: Alias for `startup_timeout_sec` in milliseconds. (Type: number)
- mcp_servers.<id>.tool_timeout_sec: Override the default 60s per-tool timeout for an MCP server. (Type: number)
- mcp_servers.<id>.enabled_tools: Allow list of tool names exposed by the MCP server. (Type: array<string>)
- mcp_servers.<id>.disabled_tools: Deny list applied after `enabled_tools` for the MCP server. (Type: array<string>)
- mcp_servers.<id>.supports_parallel_tool_calls: Mark every tool on this server as safe to run in parallel. Enable only when the server can handle concurrent calls to all its tools. Defaults to `false`. (Type: boolean)
- mcp_servers.<id>.tool_input_schema_max_bytes: Compact each ordinary MCP tool's input schema when it exceeds this many UTF-8 bytes. The default is 5,000 bytes. Code Mode also uses an explicit value when rendering tool input types. (Type: integer (positive))
- mcp_servers.<id>.omit_tools_from: Omit this server’s tools from selected model-facing surfaces. Choose `direct` (initial tools), `deferred` (tool search), or `code_mode` (Code Mode scripts). Use `disabled_tools` to block a tool. An empty list clears inherited omissions. (Type: array<string>)
- mcp_servers.<id>.default_tools_approval_mode: Default approval behavior for MCP tools on this server unless a per-tool override exists. (Type: auto | prompt | writes | approve)
- mcp_servers.<id>.tools.<tool>.approval_mode: Per-tool approval behavior override for one MCP tool on this server. (Type: auto | prompt | writes | approve)
- mcp_servers.<id>.tools.<tool>.output_token_limit: Token budget for one MCP tool's output, before the standard 20% serialization allowance. Overrides the model's default output truncation budget for that tool. (Type: integer (positive))
- mcp_servers.<id>.scopes: OAuth scopes to request at login. If omitted, Codex uses the initial authentication challenge's scopes, falling back to the protected resource's metadata. (Type: array<string>)
- mcp_servers.<id>.oauth_resource: Optional RFC 8707 OAuth resource parameter to include during MCP login. (Type: string)
- mcp_servers.<id>.environment_id: Execution environment for the MCP server. Defaults to `local`. Use the ID of a configured executor to run a stdio server or connect to a streamable HTTP server there. (Type: string)
- agents: Multi-agent settings and custom role declarations. Scalar setting names are reserved and can't be used as custom role names. (Type: table)
- agents.enabled: Enable or disable multi-agent tools (default: true). (Type: boolean)
- agents.max_concurrent_threads_per_session: Maximum number of spawned-agent threads that can be open concurrently, excluding the primary thread. When unset, Codex chooses the default. (Type: number)
- agents.max_threads: Legacy alias for `agents.max_concurrent_threads_per_session`. (Type: number)
- agents.default_subagent_model: Default model for spawned agents. An explicit spawn model takes precedence. (Type: string)
- agents.default_subagent_reasoning_effort: Default reasoning effort for spawned agents. An explicit spawn effort takes precedence. (Type: string)
- agents.interrupt_message: Record a model-visible message when an agent turn is interrupted (default: true). (Type: boolean)
- agents.<name>.description: Role guidance shown to Codex when choosing and spawning that agent type. (Type: string)
- agents.<name>.config_file: Path to a TOML config layer for that role; relative paths resolve from the config file that declares the role. (Type: string (path))
- memories.version: Select the local memory store. With memories enabled, Codex defaults to `v2` for a fresh home and `v1` if `$CODEX_HOME/memories/` exists. Explicitly setting `dual_write = false` keeps the default at `v1`. (Type: v1 | v2)
- memories.dual_write: With `v1` selected, set to `true` to generate both stores while continuing to read `v1`. With `v2` selected, Codex writes only `v2`. (Type: boolean)
- memories.generate_memories: When `false`, newly created threads are not stored as memory-generation inputs. Defaults to `true`. (Type: boolean)
- memories.use_memories: When `false`, Codex skips injecting existing memories into future sessions. Defaults to `true`. (Type: boolean)
- memories.disable_on_external_context: When `true`, threads that use external context such as MCP tool calls, web search, or tool search are kept out of memory generation. Defaults to `false`. Legacy alias: `memories.no_memories_if_mcp_or_web_search`. (Type: boolean)
- memories.max_raw_memories_for_consolidation: Maximum recent raw memories retained for global consolidation. Defaults to `256` and is capped at `4096`. (Type: number)
- memories.max_unused_days: Maximum days since a memory was last used before it becomes ineligible for consolidation. Defaults to `30` and is clamped to `0`-`365`. (Type: number)
- memories.max_rollout_age_days: Maximum age of threads considered for memory generation. Defaults to `30` and is clamped to `0`-`90`. (Type: number)
- memories.max_rollouts_per_startup: Maximum rollout candidates processed per startup pass. Defaults to `16` and is capped at `128`. (Type: number)
- memories.min_rollout_idle_hours: Minimum idle time before a thread is considered for memory generation. Defaults to `6` and is clamped to `1`-`48`. (Type: number)
- memories.min_rate_limit_remaining_percent: Minimum remaining percentage required in Codex rate-limit windows before memory generation starts. Defaults to `25` and is clamped to `0`-`100`. (Type: number)
- memories.extract_model: Optional model override for per-thread memory extraction. (Type: string)
- memories.consolidation_model: Optional model override for global memory consolidation. (Type: string)
- memories.consolidation_service_tier: Service tier for global memory consolidation. Defaults to `default` (Standard). (Type: string)
- features.prefer_mxc: Prefer MXC for local Windows execution when native capabilities and policy allow it; otherwise retain the configured legacy sandbox and setup. Disabled by default in the standalone CLI; the desktop app can enable it through rollout configuration. Command failures don't trigger fallback. (Type: boolean)
- features.unified_exec: Use resumable command execution (stable; enabled on all platforms). User opt-outs are ignored. Managed requirements can disable resumable processes and `write_stdin`, leaving one-shot `exec_command` available. (Type: boolean)
- features.view_image: Enable the built-in `view_image` tool for opening local images. Defaults to `true`. (Type: boolean)
- features.shell_snapshot: Snapshot shell environment to speed up repeated commands (stable; on by default). (Type: boolean)
- features.multi_agent: Enable multi-agent collaboration tools (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, and `close_agent`) (stable; on by default). (Type: boolean)
- features.goals: Enable persisted goals and automatic continuation (stable; on by default). (Type: boolean)
- goals.max_goal_token_budget: Set the default token budget for new goals and the largest budget a goal can request. Omit to leave goals without a configured limit. (Type: integer (positive))
- features.remote_plugin: Enable the remote plugin catalog (stable; on by default). (Type: boolean)
- features.personality: Removed feature flag. Accepted for compatibility and ignored. (Type: boolean)
- features.network_proxy: Start the network proxy for sandboxed commands (experimental; off by default). Required to enforce permission-profile domain rules unless enabled administrator-managed `network_proxy` requirements start the proxy. Use a table when setting feature-level policy options such as `domains`. Does not filter web search, apps, MCP, or other hosted tools. (Type: boolean | table)
- features.network_proxy.enabled: Start the sandboxed-command network proxy when command network access is enabled. Defaults to `false`; permission-profile domain rules are not enforced while the proxy is off. (Type: boolean)
- features.network_proxy.domains: Domain policy for sandboxed networking. Unset by default, which means no external destinations are allowed until you add `allow` rules. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules. Prefer scoped rules because `*` broadly opens public outbound access. Add `deny` rules for blocked destinations; `deny` wins on conflicts. (Type: map<string, allow | deny>)
- features.network_proxy.unix_sockets: Unix socket policy for sandboxed networking. Unset by default; add `allow` entries for permitted sockets. (Type: map<string, allow | deny>)
- features.network_proxy.allow_local_binding: Allow broader local/private-network access. Defaults to `false`; exact local IP literal or `localhost` allow rules can still permit specific local targets. (Type: boolean)
- features.network_proxy.enable_socks5: Expose SOCKS5 support. Defaults to `true`. (Type: boolean)
- features.network_proxy.enable_socks5_udp: Allow UDP over SOCKS5. Defaults to `true`. (Type: boolean)
- features.network_proxy.allow_upstream_proxy: Allow chaining through an upstream proxy from the environment. Defaults to `true`. (Type: boolean)
- features.network_proxy.dangerously_allow_non_loopback_proxy: Permit non-loopback listener addresses. Defaults to `false`; enabling it can expose proxy listeners beyond localhost. (Type: boolean)
- features.network_proxy.dangerously_allow_all_unix_sockets: Permit arbitrary Unix socket destinations instead of allowlist-only access. Defaults to `false`; use only in tightly controlled environments. (Type: boolean)
- features.network_proxy.proxy_url: HTTP listener URL for sandboxed networking. Defaults to `"http://127.0.0.1:3128"`. (Type: string)
- features.network_proxy.socks_url: SOCKS5 listener URL. Defaults to `"http://127.0.0.1:8081"`. (Type: string)
- features.web_search: Deprecated legacy toggle; prefer the top-level `web_search` setting. (Type: boolean)
- features.web_search_cached: Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "cached"`. (Type: boolean)
- features.web_search_request: Deprecated legacy toggle. When `web_search` is unset, true maps to `web_search = "live"`. (Type: boolean)
- features.shell_tool: Enable command execution tools (stable; on by default). (Type: boolean)
- features.enable_request_compression: Compress streaming request bodies with zstd when supported (stable; on by default). (Type: boolean)
- features.skill_mcp_dependency_install: Allow prompting and installing missing MCP dependencies for skills (stable; on by default). (Type: boolean)
- features.fast_mode: Enable Fast mode controls advertised by the active model (stable; on by default), independently of `features.ultrafast_mode`. Availability still depends on the model and account. (Type: boolean)
- features.ultrafast_mode: Enable Ultrafast mode controls (stable; on by default), independently of `features.fast_mode`. Availability still depends on the model and account. (Type: boolean)
- features.prevent_idle_sleep: Prevent the machine from sleeping while a turn is actively running (experimental; off by default). (Type: boolean)
- suppress_unstable_features_warning: Suppress the warning that appears when under-development feature flags are enabled. (Type: boolean)
- model_providers.<id>: Custom provider definition. Built-in provider IDs (`openai`, `ollama`, and `lmstudio`) are reserved and cannot be overridden. (Type: table)
- model_providers.<id>.name: Display name for a custom model provider. (Type: string)
- model_providers.<id>.base_url: API base URL for the model provider. (Type: string)
- model_providers.<id>.model_catalog_url: Full URL for a Codex-native model catalog. Omit to keep the provider's default model discovery. (Type: string)
- model_providers.<id>.capabilities.external_web_access: Whether the provider's hosted web search can access the live web. Omit to keep provider defaults; model and turn settings may restrict access further. (Type: boolean)
- model_providers.<id>.capabilities.remote_compaction: Provider compaction protocol. `unsupported` uses local compaction; `v2` sends compaction triggers through Responses. Omit to keep provider defaults; model and turn settings may restrict support further. (Type: unsupported | v2)
- model_providers.<id>.env_key: Environment variable supplying the provider API key. (Type: string)
- model_providers.<id>.env_key_instructions: Optional setup guidance for the provider API key. (Type: string)
- model_providers.<id>.experimental_bearer_token: Direct bearer token for the provider (discouraged; use `env_key`). (Type: string)
- model_providers.<id>.requires_openai_auth: The provider uses OpenAI authentication (defaults to false). (Type: boolean)
- model_providers.<id>.wire_api: Protocol used by the provider. `responses` is the only supported value, and it is the default when omitted. (Type: responses)
- model_providers.<id>.query_params: Extra query parameters appended to provider requests. (Type: map<string,string>)
- model_providers.<id>.http_headers: Static HTTP headers added to provider requests. (Type: map<string,string>)
- model_providers.<id>.env_http_headers: HTTP headers populated from environment variables when present. (Type: map<string,string>)
- model_providers.<id>.request_max_retries: Retry count for HTTP requests to the provider (default: 4). (Type: number)
- model_providers.<id>.stream_max_retries: Retry count for SSE streaming interruptions (default: 5). (Type: number)
- model_providers.<id>.stream_idle_timeout_ms: Idle timeout for SSE streams in milliseconds (default: 300000). (Type: number)
- model_providers.<id>.supports_websockets: Whether that provider supports the Responses API WebSocket transport. (Type: boolean)
- model_providers.<id>.supports_standalone_web_search: Advertise support for a compatible standalone web search endpoint (default: false). Standalone search remains under development and off by default; provider compatibility alone doesn't enable it. (Type: boolean)
- model_providers.<id>.auth: Command-backed bearer token configuration for a custom provider. Do not combine with `env_key`, `experimental_bearer_token`, or `requires_openai_auth`. (Type: table)
- model_providers.<id>.auth.command: Command to run when Codex needs a bearer token. The command must print the token to stdout. (Type: string)
- model_providers.<id>.auth.args: Arguments passed to the token command. (Type: array<string>)
- model_providers.<id>.auth.timeout_ms: Maximum token command runtime in milliseconds (default: 5000). (Type: number)
- model_providers.<id>.auth.refresh_interval_ms: How often Codex proactively refreshes the token in milliseconds (default: 300000). Set to `0` to refresh only after an authentication retry. (Type: number)
- model_providers.<id>.auth.cwd: Working directory for the token command. (Type: string (path))
- model_providers.gcp.base_url: Override the built-in Google Cloud Vertex AI endpoint. Otherwise, Codex builds it from the project ID and location. (Type: string)
- model_providers.gcp.project_id: Google Cloud project ID for the Vertex AI endpoint. Takes precedence over `GOOGLE_CLOUD_PROJECT`. (Type: string)
- model_providers.gcp.location: Google Cloud location for the Vertex AI endpoint. Takes precedence over `GOOGLE_CLOUD_LOCATION`. Defaults to `global`. (Type: string)
- model_providers.gcp.credential_file: Path to a Google Application Default Credentials (ADC) file. Overrides `GOOGLE_APPLICATION_CREDENTIALS` only for the provider’s authentication command. (Type: string (absolute path))
- model_providers.amazon-bedrock.aws.profile: AWS profile name used by the built-in `amazon-bedrock` provider. (Type: string)
- model_providers.amazon-bedrock.aws.region: AWS region used by the built-in `amazon-bedrock` provider. (Type: string)
- model_reasoning_effort: Reasoning effort advertised by the selected model, such as `low`, `medium`, `high`, `xhigh`, `max`, or `ultra`. Available levels depend on the model and client. (Type: string)
- plan_mode_reasoning_effort: Plan-mode-specific reasoning override using a level supported by the selected model. When unset, Plan mode uses its built-in preset default. (Type: string)
- model_reasoning_summary: Select reasoning summary detail or disable summaries entirely. (Type: auto | concise | detailed | none)
- model_verbosity: Optional GPT-5 Responses API verbosity override; when unset, the selected model/preset default is used. (Type: low | medium | high)
- shell_environment_policy.inherit: Baseline environment inheritance when spawning subprocesses. (Type: all | core | none)
- shell_environment_policy.ignore_default_excludes: Keep variables containing KEY, SECRET, or TOKEN before other filters run (default: true). Set to false to apply automatic secret-name exclusions. (Type: boolean)
- shell_environment_policy.filters: Canonical case-insensitive environment-variable pattern filters. Include entries create an allowlist and can't restore excluded values. Explicit `set` values apply after exclusions. Don't combine filters with legacy `exclude` or `include_only` arrays in the same layer. (Type: map<string, include | exclude>)
- shell_environment_policy.exclude: Legacy environment-variable exclusion patterns. Use `shell_environment_policy.filters` for new configuration; don't combine both forms in the same layer. (Type: array<string>)
- shell_environment_policy.include_only: Legacy allowlist of environment-variable patterns. Use `shell_environment_policy.filters` for new configuration; don't combine both forms in the same layer. (Type: array<string>)
- shell_environment_policy.set: Explicit environment values injected after exclusions; include filters can still remove them. (Type: map<string,string>)
- shell_environment_policy.experimental_use_profile: Use the user shell profile when spawning subprocesses. (Type: boolean)
- project_root_markers: List of project root marker filenames; used when searching parent directories for the project root. (Type: array<string>)
- project_doc_max_bytes: Maximum bytes read from `AGENTS.md` when building project instructions. (Type: number)
- project_doc_fallback_filenames: Additional filenames to try when `AGENTS.md` is missing. (Type: array<string>)
- history.persistence: Control whether Codex saves session transcripts to history.jsonl. (Type: save-all | none)
- tool_output_token_limit: Token budget for storing individual tool/function outputs in history. (Type: number)
- thread_unload_delay_secs: Seconds the app server waits before unloading an inactive thread with no subscribers. Set to `0` to unload it as soon as it meets both conditions. Defaults to `60` seconds. (Type: integer (nonnegative))
- background_terminal_max_timeout: Maximum poll window in milliseconds for empty `write_stdin` polls (background terminal polling). Default: `300000` (5 minutes). Replaces the older `background_terminal_timeout` key. (Type: number)
- history.max_bytes: If set, caps the history file size in bytes by dropping oldest entries. (Type: number)
- file_opener: URI scheme used to open citations from Codex output (default: `vscode`). (Type: vscode | vscode-insiders | windsurf | cursor | none)
- otel.environment: Environment tag applied to emitted OpenTelemetry events (default: `dev`). (Type: string)
- otel.exporter: Select the OpenTelemetry exporter and provide any endpoint metadata. (Type: none | otlp-http | otlp-grpc)
- otel.trace_exporter: Select the OpenTelemetry trace exporter and provide any endpoint metadata. (Type: none | otlp-http | otlp-grpc)
- otel.metrics_exporter: Select the OpenTelemetry metrics exporter. The default, `statsig`, follows `analytics.enabled`. Explicit OTLP exporters work independently of that setting. Set to `none` to disable metrics export. (Type: none | statsig | otlp-http | otlp-grpc)
- otel.log_user_prompt: Opt in to exporting raw user prompts with OpenTelemetry logs. (Type: boolean)
- otel.log_agent_responses: Export final response text from the main agent and spawned subagents to the configured OTLP log exporter. Defaults to `false`. Response text can contain sensitive data and is capped at 64 KiB per response. (Type: boolean)
- otel.log_guardian_assessments: Export completed automatic approval reviews to the configured OTLP log exporter. Defaults to `false`. Review rationales can contain sensitive data and are capped at 64 KiB each. (Type: boolean)
- otel.span_attributes: Add string attributes to every exported trace span. (Type: map<string,string>)
- otel.tracestate: Set fields on W3C tracestate members when propagating trace context. Each member maps field names to string values. (Type: map<string,map<string,string>>)
- otel.tool_result.max_bytes: Maximum number of UTF-8 bytes from each tool result to include in logs, before the truncation notice. Defaults to `2048`. This setting affects only logged output. (Type: integer (nonnegative))
- otel.exporter.<id>.endpoint: Exporter endpoint for OTEL logs. (Type: string)
- otel.exporter.<id>.protocol: Protocol used by the OTLP/HTTP exporter. (Type: binary | json)
- otel.exporter.<id>.headers: Static headers included with OTEL exporter requests. (Type: map<string,string>)
- otel.trace_exporter.<id>.endpoint: Trace exporter endpoint for OTEL logs. (Type: string)
- otel.trace_exporter.<id>.protocol: Protocol used by the OTLP/HTTP trace exporter. (Type: binary | json)
- otel.trace_exporter.<id>.headers: Static headers included with OTEL trace exporter requests. (Type: map<string,string>)
- otel.exporter.<id>.tls.ca-certificate: CA certificate path for OTEL exporter TLS. (Type: string)
- otel.exporter.<id>.tls.client-certificate: Client certificate path for OTEL exporter TLS. (Type: string)
- otel.exporter.<id>.tls.client-private-key: Client private key path for OTEL exporter TLS. (Type: string)
- otel.trace_exporter.<id>.tls.ca-certificate: CA certificate path for OTEL trace exporter TLS. (Type: string)
- otel.trace_exporter.<id>.tls.client-certificate: Client certificate path for OTEL trace exporter TLS. (Type: string)
- otel.trace_exporter.<id>.tls.client-private-key: Client private key path for OTEL trace exporter TLS. (Type: string)
- desktop.custom_file_handlers.<id>: User-level only. Defines an additional **Open in** target for the ChatGPT desktop app. See [Add custom file handlers](https://learn.chatgpt.com/docs/config-file/config-advanced#add-custom-file-handlers) for examples and handler ID constraints. (Type: table)
- desktop.custom_file_handlers.<id>.label: Display name shown in **Open in** menus. Required. (Type: string)
- desktop.custom_file_handlers.<id>.icon: Bundled asset path, Base64-encoded `data:image/...` URL, file URI, or absolute local path for the handler icon. Required; unsupported sources use the default VS Code icon. (Type: string)
- desktop.custom_file_handlers.<id>.command: Executable path or command name to detect and launch. Required. (Type: string)
- desktop.custom_file_handlers.<id>.args: Arguments inserted between the command and file input (default: `[]`). (Type: array<string>)
- desktop.custom_file_handlers.<id>.input: How the app sends file input to the handler (default: `path`). (Type: path | json_argument | json_stdin)
- desktop.custom_file_handlers.<id>.supports_ssh: Offer the handler for files in SSH workspaces (default: `false`). (Type: boolean)
- tui: TUI-specific options such as enabling inline desktop notifications. (Type: table)
- tui.notifications: Enable TUI notifications; optionally restrict to specific event types. (Type: boolean | array<string>)
- tui.notification_method: Notification method for terminal notifications (default: auto). (Type: auto | osc9 | bel)
- tui.notification_condition: Control whether TUI notifications fire only when the terminal is unfocused or regardless of focus. Defaults to `unfocused`. (Type: unfocused | always)
- tui.animations: Enable terminal animations (welcome screen, shimmer, spinner) (default: true). (Type: boolean)
- tui.disable_paste_burst: Disable burst-paste detection in the TUI (default: false). Takes precedence over the legacy top-level `disable_paste_burst` setting. (Type: boolean)
- tui.alternate_screen: Control alternate screen usage for the TUI (default: auto; auto skips it in Zellij to preserve scrollback). (Type: auto | always | never)
- tui.resume_cwd: Working directory to use when resuming or forking a session. When unset, Codex asks you to choose if your current directory differs from the session's saved directory. (Type: current | session)
- tui.vim_mode_default: Start the composer in Vim normal mode instead of insert mode (default: false). You can still toggle it per session with `/vim`. (Type: boolean)
- tui.raw_output_mode: Start the TUI in raw scrollback mode for copy-friendly terminal selection (default: false). You can toggle it with `/raw` or the default `alt-r` key binding. (Type: boolean)
- tui.show_tooltips: Show onboarding tooltips in the TUI welcome screen (default: true). (Type: boolean)
- tui.auto_recap: Generate automatic conversation recaps while the terminal is unfocused (default: true). Set to `false` to disable automatic recaps; `/recap` remains available. (Type: boolean)
- tui.show_server_version_notice: Show informational notices about connected app-server version differences (default: true). Does not hide compatibility errors or version status. (Type: boolean)
- tui.status_line: Ordered list of TUI footer status-line item identifiers. `null` disables the status line. (Type: array<string> | null)
- tui.terminal_title: Ordered list of terminal window/tab title item identifiers. Defaults to `["spinner", "project"]`; `null` disables title updates. (Type: array<string> | null)
- tui.theme: Syntax-highlighting theme override (kebab-case theme name). (Type: string)
- tui.keymap.<context>.<action>: Keyboard shortcut binding for a TUI action. Supported contexts include `global`, `chat`, `composer`, `editor`, `vim_normal`, `vim_operator`, `vim_text_object`, `pager`, `list`, and `approval`. Selected composer actions fall back to matching `tui.keymap.global` bindings; context-specific bindings take precedence when supported. (Type: string | array<string>)
- tui.keymap.<context>.<action> = []: Unbind the action in that keymap context. Key names use normalized strings such as `ctrl-a`, `shift-enter`, `page-down`, or `minus`. (Type: empty array)
- marketplaces.<name>.source_type: Source kind for a configured plugin marketplace. Marketplaces can be defined in system, cloud-managed, user, or trusted-project config.toml. (Type: git | local)
- marketplaces.<name>.source: Git repository location or local marketplace root directory. Use an absolute path for a local source; the directory contains .agents/plugins/marketplace.json. (Type: string)
- marketplaces.<name>.ref: Optional Git branch, tag, or commit for the marketplace. (Type: string)
- marketplaces.<name>.sparse_paths: Optional sparse checkout paths for a Git marketplace. Include the marketplace catalog and any local plugin directories it references. (Type: array<string>)
- plugins._default.enabled: Set the default activation state for installed plugins. An explicit `plugins.<plugin>.enabled` overrides this default for plugins their source enables. Omit the table to keep the source or account activation settings. (Type: boolean)
- plugins.<plugin>.enabled: Enable or disable a local-marketplace plugin using a `plugin-name@marketplace-name` key. Read from the effective merged config; trusted-project settings can override user, cloud-managed, and system defaults. Marketplace refresh can install or refresh configured plugins even when disabled. This does not override workspace-managed enabled states. (Type: boolean)
- plugins.<plugin>.mcp_servers.<server>.enabled: Enable or disable an MCP server bundled by an installed plugin without changing the plugin manifest. (Type: boolean)
- plugins.<plugin>.mcp_servers.<server>.default_tools_approval_mode: Default approval behavior for tools on a plugin-provided MCP server. (Type: auto | prompt | writes | approve)
- plugins.<plugin>.mcp_servers.<server>.enabled_tools: Allow list of tools exposed from a plugin-provided MCP server. (Type: array<string>)
- plugins.<plugin>.mcp_servers.<server>.disabled_tools: Deny list applied after `enabled_tools` for a plugin-provided MCP server. (Type: array<string>)
- plugins.<plugin>.mcp_servers.<server>.tools.<tool>.approval_mode: Per-tool approval behavior override for a plugin-provided MCP tool. (Type: auto | prompt | writes | approve)
- tui.presets.<digit>.input: Save a prompt or slash command in one of the ten slots (`0`–`9`) shown by `/presets`. Use up to 8,000 UTF-8 bytes of nonempty text. Shell commands beginning with `!` are unsupported. (Type: string)
- tui.presets.<digit>.label: Optional name for the preset in the picker and shortcut hints. (Type: string)
- tui.model_availability_nux.<model>: Internal startup-tooltip state keyed by model slug. (Type: integer)
- hide_agent_reasoning: Suppress reasoning events in both the TUI and `codex exec` output. (Type: boolean)
- show_raw_agent_reasoning: Surface raw reasoning content when the active model emits it. (Type: boolean)
- disable_paste_burst: Legacy fallback for `tui.disable_paste_burst`. Prefer the setting under `[tui]`. (Type: boolean)
- chatgpt_base_url: Override the base URL used during the ChatGPT login flow. (Type: string)
- cli_auth_credentials_store: Control where the CLI stores cached credentials. (Type: file | keyring | auto | ephemeral)
- mcp_oauth_credentials_store: Preferred store for MCP OAuth credentials. (Type: auto | file | keyring)
- mcp_oauth_callback_port: Optional global fixed port for the local HTTP callback server used during MCP OAuth login. A server-specific `oauth.callback_port` takes precedence. When neither is set, Codex binds to an ephemeral port chosen by the OS. (Type: integer)
- mcp_oauth_callback_url: Optional base callback URL for MCP OAuth login, such as a devbox ingress URL. Newly added pre-registered clients use this URL unchanged when the authorization server supports issuer identification; existing clients without a saved callback append a server-specific callback ID. Without issuer support, any pre-registered MCP server whose configured callback lacks the required ID falls back to this URL with the ID appended. Callback URL ports don't select the listener port. (Type: string)
- experimental_use_unified_exec_tool: Legacy name for enabling unified exec; prefer `[features].unified_exec` or `codex --enable unified_exec`. (Type: boolean)
- tools.web_search: Optional web search tool configuration. The object form can set search context size, allowed search domains, and approximate user location. These search-domain filters are separate from sandboxed-command network domain rules and do not restrict connectors or MCP servers. (Type: boolean | { context_size = "low|medium|high", allowed_domains = [string], location = { country, region, city, timezone } })
- web_search: Web search mode (default: `"cached"`; cached uses an OpenAI-maintained index without external web access; indexed permits external access only when gated by the search index; if you use `--yolo` or another full access sandbox setting, it defaults to `"live"`). Use `"live"` for unrestricted live retrieval, or `"disabled"` to remove the tool. (Type: disabled | cached | indexed | live)
- default_permissions: Name of the default permissions profile to apply to sandboxed tool calls. Built-ins are `:read-only`, `:workspace`, and `:danger-full-access`; custom profile names require matching `[permissions.<name>]` tables. Don't combine with `sandbox_mode` or `[sandbox_workspace_write]`. (Type: string)
- permissions.<name>.description: Human-readable description for this named profile. A profile does not inherit its parent's description through `extends`. (Type: string)
- permissions.<name>.extends: Optional parent profile applied before this named profile. Set it to another named profile, `:read-only`, or `:workspace`; `:danger-full-access`, undefined parents, and cycles are rejected. (Type: string)
- permissions.<name>.workspace_roots: Profile-defined workspace roots that receive `:workspace_roots` filesystem rules alongside the session's runtime workspace roots. (Type: table)
- permissions.<name>.workspace_roots.<path>: Opt a path into the profile's workspace root set when `true`. Disabled entries remain inactive. (Type: boolean)
- permissions.<name>.filesystem: Named filesystem permission profile. Each key is an absolute path or special token such as `:minimal` or `:workspace_roots`. (Type: table)
- permissions.<name>.filesystem.glob_scan_max_depth: Maximum depth for expanding deny-read glob patterns on platforms that snapshot matches before sandbox startup. Must be at least `1` when set. (Type: number)
- permissions.<name>.filesystem.<path-or-glob>: Grant direct access for a path, glob pattern, or special token, or scope nested entries under that root. Use `"deny"` to deny reads for matching paths. (Type: "read" | "write" | "deny" | table)
- permissions.<name>.filesystem.":workspace_roots".<subpath-or-glob>: Scoped filesystem access relative to each effective workspace root. Use `"."` for the root itself; glob subpaths such as `"**/*.env"` can deny reads with `"deny"`. (Type: "read" | "write" | "deny")
- permissions.<name>.network.enabled: Enable network access for commands in this permission profile. This does not start the network proxy. Without `features.network_proxy` or enabled administrator-managed networking requirements, command network access is direct and profile domain rules are not enforced. (Type: boolean)
- permissions.<name>.network.proxy_url: HTTP listener URL used when this permissions profile enables sandboxed networking. (Type: string)
- permissions.<name>.network.enable_socks5: Expose SOCKS5 support when this permissions profile enables sandboxed networking. (Type: boolean)
- permissions.<name>.network.socks_url: SOCKS5 proxy endpoint used by this permissions profile. (Type: string)
- permissions.<name>.network.enable_socks5_udp: Allow UDP over the SOCKS5 listener when enabled. (Type: boolean)
- permissions.<name>.network.allow_upstream_proxy: Allow sandboxed networking to chain through another upstream proxy. (Type: boolean)
- permissions.<name>.network.dangerously_allow_non_loopback_proxy: Permit non-loopback bind addresses for sandboxed networking listeners. Enabling it can expose listeners beyond localhost. (Type: boolean)
- permissions.<name>.network.dangerously_allow_all_unix_sockets: Allow arbitrary Unix socket destinations instead of the default restricted set. Use only in tightly controlled environments. (Type: boolean)
- permissions.<name>.network.mode: Network proxy mode used for subprocess traffic. (Type: limited | full)
- permissions.<name>.network.domains: Domain rules for sandboxed commands. Enforced only when `features.network_proxy` or enabled administrator-managed networking requirements activate the proxy. Supports exact hosts, `*.example.com`, `**.example.com`, and global `*` allow rules; `deny` wins. Does not restrict web search, apps, or MCP servers. (Type: table)
- permissions.<name>.network.domains.<pattern>: Allow or deny an exact host or scoped wildcard pattern such as `*.example.com` or `**.example.com`. (Type: allow | deny)
- permissions.<name>.network.unix_sockets: Unix socket allowlist overrides for sandboxed networking. Use socket paths as keys; `allow` adds a path, and `deny` rejects it. (Type: table)
- permissions.<name>.network.unix_sockets.<path>: Add an absolute Unix socket path to the effective allowlist with `allow`, or reject it with `deny`. Denied entries are omitted from the effective allowlist. (Type: allow | deny)
- permissions.<name>.network.allow_local_binding: Permit broader local/private-network access through sandboxed networking. Exact local IP literal or `localhost` allow rules can still permit specific local targets when this stays `false`. (Type: boolean)
- projects.<path>.trust_level: Mark a project or worktree as trusted or untrusted (`"trusted"` | `"untrusted"`). Untrusted projects skip project-scoped `.codex/` layers, including project-local config, hooks, and rules. (Type: string)
- notice.hide_full_access_warning: Track acknowledgement of the full access warning prompt. (Type: boolean)
- notice.hide_world_writable_warning: Track acknowledgement of the Windows world-writable directories warning. (Type: boolean)
- notice.hide_rate_limit_model_nudge: Track opt-out of the rate limit model switch reminder. (Type: boolean)
- notice.hide_gpt5_1_migration_prompt: Track acknowledgement of the GPT-5.1 migration prompt. (Type: boolean)
- notice.hide_gpt-5.1-codex-max_migration_prompt: Track acknowledgement of the gpt-5.1-codex-max migration prompt. (Type: boolean)
- notice.model_migrations: Track acknowledged model migrations as old->new mappings. (Type: map<string,string>)
- forced_login_method: Restrict Codex to a specific authentication method. (Type: chatgpt | api)
- forced_chatgpt_workspace_id: Limit ChatGPT logins to a specific workspace identifier. (Type: string (uuid))

You can find the latest JSON schema for `config.toml` [here](https://learn.chatgpt.com/docs/config-schema.json).

To get autocompletion and diagnostics when editing `config.toml` in VS Code or Cursor, you can install the [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) extension and add this line to the top of your `config.toml`:

```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

Note: Rename `experimental_instructions_file` to `model_instructions_file`. Codex deprecates the old key; update existing configs to the new name.

## `requirements.toml`

`requirements.toml` is an admin-enforced configuration file that constrains security-sensitive settings users can't override. For details, locations, and examples, see [Admin-enforced requirements](https://learn.chatgpt.com/docs/enterprise/managed-configuration#admin-enforced-requirements-requirementstoml).

For ChatGPT Business and Enterprise users, Codex can also apply cloud-fetched
requirements. See the security page for precedence details. To serve CLI policy from your own HTTPS endpoint, see [Self-host Codex configuration for your team](https://learn.chatgpt.com/docs/enterprise/configuration-server).

Use `[features]` in `requirements.toml` to pin runtime feature flags by the same
canonical keys that `config.toml` uses. Requirements can also include documented
app-only keys that don't belong in `config.toml`. Omitted keys remain
unconstrained.

Some managed requirements enforce an exact configuration value instead of an
allowlist. Users can't override an enforced path, update preference, login-shell
policy, or feedback setting.

Managed permission-profile allowlists require Codex 0.138.0 or later. Codex
0.137.0 and earlier ignore `allowed_permission_profiles` and managed
`default_permissions`.

Use `allowed_sandbox_modes` with `sandbox_mode`. For permission-profile
deployments, use `allowed_permission_profiles` with managed
`default_permissions`.

An `untrusted` entry in `allowed_approval_policies` is still valid for the
stricter approval behavior Codex derives when a project uses
`trust_level = "untrusted"`. It does not permit explicitly setting
`approval_policy = "untrusted"`.

The `[models.new_thread]` table supplies managed defaults, not enforcement.
If you explicitly override the model or reasoning effort with `--model`,
`--config`, or `--profile`, Codex ignores both `model` and
`model_reasoning_effort` in `[models.new_thread]`. `service_tier` is independent.

The browser requirements cover three separate surfaces. `in_app_browser`
controls the browser pane that a person opens and uses directly. `browser_use`
controls agent-driven work in a browser. `computer_use` controls agent-driven
work in native desktop apps.

The nested Browser Use and Computer Use policy values do not grant access by
themselves. An origin- or app-specific `allow` can override the fallback for
the same policy source, but normal feature, approval, and other policy checks
still apply. Where managed requirements and `config.toml` both apply, a `deny`
from either one wins.

- config_server: Enroll Codex with a configuration server. Set this in local administrator-controlled requirements. (Type: table)
- config_server.base_url: Base URL of the configuration server enrolled by the administrator. Codex appends /codex/config/bundle to this URL. (Type: string (HTTPS URL))
- config_server.oauth: Optional company sign-in settings. Omit this table to fetch the bundle without credentials. (Type: table)
- config_server.oauth.authorization_url: Authorization endpoint for company browser sign-in. Required when OAuth is configured. (Type: string (HTTPS URL))
- config_server.oauth.token_url: Token endpoint for company sign-in and refresh. Required when OAuth is configured. (Type: string (HTTPS URL))
- config_server.oauth.client_id: Public OAuth client ID registered for Codex. Required when OAuth is configured. (Type: string)
- config_server.oauth.scopes: Optional OAuth permissions to request from the identity provider. (Type: array<string>)
- config_server.oauth.resource: Optional OAuth resource identifier required by the identity provider. (Type: string)
- config_server.oauth.redirect_port: Optional port for the browser callback on 127.0.0.1. By default, Codex chooses an available port. (Type: number)
- sqlite_home: Enforce the directory where Codex stores SQLite-backed runtime state. (Type: string (path))
- unsafe_enforce_sqlite_journal_mode: On Linux, set to `true` to migrate existing SQLite databases on NFS from WAL to DELETE journaling before opening them for writes. Defaults to `false`. The mount must support POSIX locks across hosts. Keep every other SQLite client that uses the databases stopped on every host until migration succeeds. Replacements preserve file mode bits but belong to the user running the migration and do not copy the original owner, group, or extended ACLs. (Type: boolean)
- log_dir: Enforce the directory where Codex writes local log files. (Type: string (path))
- model_catalog_json: Enforce the JSON model catalog Codex uses at startup. (Type: string (path))
- check_for_update_on_startup: Enforce whether Codex checks for updates when it starts. (Type: boolean)
- allow_login_shell: Enforce whether shell tools can start a login shell. (Type: boolean)
- config_server: Enroll Codex with a configuration server through local managed requirements. Codex retrieves its policy bundle from this server. A cloud policy cannot configure its own server. (Type: table)
- config_server.base_url: Required HTTPS base URL. Codex appends `/codex/config/bundle`. Omit credentials, query parameters, and fragments from the base URL. (Type: string)
- config_server.oauth: OAuth settings for configuration server sign-in. Requires `authorization_url`, `token_url`, and a nonempty `client_id`. Optional fields are `device_authorization_url`, `resource`, `scopes` (defaults to an empty list), and `redirect_port` (nonzero). All endpoint URLs must use HTTPS. (Type: table)
- allowed_login_methods: Allow `chatgpt`, `api`, or both. If omitted, this setting doesn't restrict login methods. If set, the list must contain at least one method. `api` permits API authentication, including Amazon Bedrock. Set through the local system requirements file or macOS MDM. Cloud-managed values are ignored. (Type: array<string>)
- allowed_chatgpt_workspaces: Restrict ChatGPT login, including Codex access tokens, to the listed workspace IDs. An empty list disables ChatGPT login; API authentication remains available when permitted. Set through the local system requirements file or macOS MDM; cloud-managed values are ignored. (Type: array<string>)
- cli_auth_credentials_store: Enforce the CLI credential store before authentication loads. `file` uses `CODEX_HOME/auth.json`; `keyring` requires the OS credential store; `auto` falls back to a file if the credential store is unavailable; `ephemeral` keeps credentials in memory for the current process. Set through the local system requirements file or macOS MDM; cloud-managed values are ignored. (Type: file | keyring | auto | ephemeral)
- chatgpt_base_url: Enforce the ChatGPT service base URL before authentication and cloud-policy retrieval. This doesn't configure every Codex network destination. Set through the local system requirements file or macOS MDM; cloud-managed values are ignored. (Type: string)
- feedback: Managed feedback settings. (Type: table)
- feedback.enabled: Enforce whether users can submit feedback across Codex clients. (Type: boolean)
- allowed_approval_policies: Allowed approval policies, such as `on-request`, `never`, and `granular`. Include `untrusted` to permit the stricter policy derived from an untrusted project; it cannot be selected directly with `approval_policy`. (Type: array<string>)
- allowed_approvals_reviewers: Allowed values for `approvals_reviewer`, such as `user` and `auto_review`. (Type: array<string>)
- guardian_policy_config: Managed Markdown policy instructions for automatic review. This takes precedence over local `[auto_review].policy`. Blank values are ignored. (Type: string)
- guardian_extra_policy: Additional managed Markdown policy for automatic review, included alongside the main policy. This takes precedence over local `[auto_review].extra_policy`. Blank values are ignored. (Type: string)
- additional_developer_instructions: Managed developer instructions added as a separate developer message. Codex rejects instructions that exceed a limit of 10,000 estimated tokens, including context markers. (Type: string)
- auto_review: Managed automatic-review requirements. (Type: table)
- auto_review.required_on_models: Model slugs that must use automatic review. Slugs must be non-empty, omit provider namespaces, and have no surrounding whitespace. Lists from multiple requirements sources are combined. (Type: array<string>)
- auto_review.ignore_rules: Full model slugs for which Codex ignores `allow` prefix rules in command execution policy. Match the slug exactly, including its provider namespace when present; unlike `required_on_models`, this does not accept a namespace-free alias. Deny and network rules still apply. (Type: array<string>)
- allowed_permission_profiles: Complete list of allowed permission profiles. Profiles set to `true` are allowed. Profiles that are omitted or set to `false` are denied, including profiles added in future versions. When requirements sources are combined, entries are matched by profile name. (Type: table<boolean>)
- allowed_permission_profiles.<name>: Allow or deny a built-in or custom permission profile defined in a loaded config or requirements source. A later, higher-precedence requirements source can use `false` to turn off a profile allowed by an earlier, lower-precedence source. (Type: boolean)
- default_permissions: Managed default permission profile. The profile must be allowed by `allowed_permission_profiles`. Set this explicitly for predictable behavior; if omitted, Codex defaults to `:workspace` only when both `:workspace` and `:read-only` are explicitly allowed. (Type: string)
- enforce_residency: Require Codex service traffic to use a supported data residency. Currently accepts `us`. (Type: string)
- model_provider: Enforce the model provider ID, overriding local and session configuration. (Type: string)
- model_providers: Managed model provider definitions. Each entry replaces the complete configured provider with the same ID; fields aren't merged with the user's definition. Providers with other IDs remain available. (Type: map<string, table>)
- model_providers.<id>: Complete managed provider definition. Uses the same provider fields as `config.toml`, including `name`, `base_url`, authentication, and transport settings. (Type: table)
- models: Contains the `[models.new_thread]` table. (Type: table)
- models.new_thread: Optional defaults to apply when a new local thread starts. They take priority over user and project defaults, but can be superseded by explicit overrides. (Type: table)
- models.new_thread.model: Default model for new threads. An explicit override of either the model or reasoning effort causes both fields to be ignored. (Type: string)
- models.new_thread.model_reasoning_effort: Default reasoning effort for new threads. An explicit override of either the model or reasoning effort causes both fields to be ignored. (Type: string)
- models.new_thread.service_tier: Default service tier for new threads. An explicit service-tier override causes this field to be ignored. (Type: string)
- permissions: Admin-defined permission profiles keyed by profile name. Uses the same profile fields as `config.toml`. (Type: table)
- permissions.<name>: Admin-defined permission profile. The name can't start with `:`, use the reserved name `filesystem`, or duplicate a profile from a loaded config. Uses the same profile fields as `config.toml`; see the Permissions guide for the complete profile schema. (Type: table)
- allowed_sandbox_modes: Allowed values for `sandbox_mode`. (Type: array<string>)
- windows: Native Windows sandbox requirements. (Type: table)
- windows.allowed_sandbox_implementations: Allowed legacy native Windows sandbox implementations (`elevated` and `unelevated`). The list must not be empty. When both are allowed and no mode is selected, Codex prefers `elevated`. This list does not restrict the `mxc` sandbox when it is available. (Type: array<string>)
- windows.allow_mxc: Set to `false` to prohibit both explicit MXC selection and automatic selection through `features.prefer_mxc`. Omitting this requirement or setting it to `true` permits MXC but doesn't enable it or require it. Legacy implementation restrictions still apply to fallback. (Type: boolean)
- windows.require_mxc: On Windows, set to `true` to reject any effective sandbox implementation other than MXC. Select MXC separately. If Codex cannot use it, configuration fails instead of falling back to a legacy sandbox. (Type: boolean)
- remote_sandbox_config: Host-specific sandbox requirements. The first entry whose `hostname_patterns` match the resolved host name overrides top-level `allowed_sandbox_modes` for that requirements source. Host-specific entries currently override sandbox modes only. (Type: array<table>)
- remote_sandbox_config[].hostname_patterns: Case-insensitive host name patterns. Supports `*` for any sequence of characters and `?` for one character. (Type: array<string>)
- remote_sandbox_config[].allowed_sandbox_modes: Allowed sandbox modes to apply when this host-specific entry matches. (Type: array<string>)
- allowed_web_search_modes: Allowed values for `web_search` (`disabled`, `cached`, `indexed`, `live`). `disabled` is always allowed; an empty list effectively allows only `disabled`. (Type: array<string>)
- allow_managed_hooks_only: When `true`, Codex skips user, project, session, and plugin hooks while still allowing managed hooks from `requirements.toml` and other managed config layers. (Type: boolean)
- allow_appshots: Set to `false` to disable Appshots for managed users. If omitted, Appshots remain unconstrained by requirements and follow normal product availability. (Type: boolean)
- allow_remote_control: Set to `false` to disable device remote control for managed users. If omitted, device remote control remains unconstrained by requirements and follows normal product availability. (Type: boolean)
- allow_browser_and_computer_use: Set to `false` to block both agent-driven Browser Use and native-app Computer Use. Setting it to `true` or omitting it does not enable either feature; the remaining feature, policy, and approval checks still apply. (Type: boolean)
- features.plugin_sharing: Set to `false` in cloud-managed `requirements.toml` to disable workspace sharing for locally built plugins. (Type: boolean)
- features: Pinned feature values. Use canonical names from `config.toml` for runtime features; documented app-only requirement keys are also supported here. (Type: table)
- features.<name>: Require a documented runtime or app feature to stay enabled or disabled. (Type: boolean)
- features.apps: Pin Apps integration availability on or off for managed users. (Type: boolean)
- features.api_key_cyber_access_programs: Allow Codex to send an explicitly selected cyber access program with requests to the built-in OpenAI provider when using API key authentication. The account and model must already have access to the program. (Type: boolean)
- features.in_app_updates: Set to `false` in `requirements.toml` to disable in-app updates. Updates remain enabled by default when this requirement is omitted. (Type: boolean)
- features.in_app_browser: Set to `false` in `requirements.toml` to disable the built-in browser pane that users open and control directly. (Type: boolean)
- features.browser_annotation_api: Set to `false` to block website-provided annotation customizations in the built-in browser. Users can still annotate pages themselves. Set to `true` to allow customizations when the app and account support them. (Type: boolean)
- features.in_app_chat: Set to `false` to hide ChatGPT and ChatGPT Work conversation screens and related cloud automation UI in the ChatGPT desktop app. This setting does not block ChatGPT Voice or stop existing cloud tasks. Setting it to `true` does not bypass account, workspace-permission, or rollout checks. (Type: boolean)
- features.in_app_dictation: Set to `false` to disable in-app dictation in the desktop app. Setting it to `true` does not bypass other availability checks. (Type: boolean)
- features.in_app_voice: Set to `false` to disable real-time Codex voice in the desktop app. Use `features.in_app_dictation` to manage dictation separately. (Type: boolean)
- features.in_app_local_automation: Set to `false` to disable local scheduled tasks in the desktop app. Setting it to `true` does not bypass other availability checks. (Type: boolean)
- features.browser_use: Set to `false` in `requirements.toml` to disable agent-driven Browser Use. (Type: boolean)
- features.browser_use_external: Set to `false` in `requirements.toml` to prevent Codex from operating supported browsers through the ChatGPT browser extension, including existing tabs and signed-in sessions. (Type: boolean)
- features.browser_use_full_cdp_access: Set to `false` in `requirements.toml` to disable full Chrome DevTools Protocol access in the local runtime, including Browser Developer mode, and prevent the ChatGPT desktop app from enabling the corresponding setting. If omitted, normal product availability applies. (Type: boolean)
- features.fast_mode: Allow or block Fast mode for managed users. Older app servers also use this setting to control Ultrafast mode. (Type: boolean)
- features.ultrafast_mode: Allow or block Ultrafast mode for managed users. On app servers that support independent speed settings, this applies even when Fast mode is disabled. Availability depends on the model and account. (Type: boolean)
- features.standalone_web_search: Experimental. Set to `true` to keep the desktop app's native web search configuration when hosted search through MCP would otherwise be available. (Type: boolean)
- features.guardian_approval: Pin Guardian approval availability on or off for managed users. (Type: boolean)
- features.memories: Pin Memories availability on or off for managed users. (Type: boolean)
- features.multi_agent: Pin multi-agent availability on or off for managed users. (Type: boolean)
- features.plugins: Pin plugin availability on or off for managed users. (Type: boolean)
- features.remote_plugin: Pin remote plugin catalog availability on or off for managed users. (Type: boolean)
- features.realtime_conversation: Set to `false` to disable the experimental `/voice` command in the Codex CLI. Do not rely on this setting to block [ChatGPT Voice](https://learn.chatgpt.com/docs/features/voice) in the desktop app or app-server voice sessions. Setting it to `true` does not bypass client or rollout checks. (Type: boolean)
- features.computer_use: Set to `false` in `requirements.toml` to disable Computer Use, Record & Replay, and related install or enablement flows. (Type: boolean)
- features.workspace_dependencies: Pin bundled workspace-dependency runtime availability on or off for managed users. (Type: boolean)
- in_app_browser: Requirements for the built-in browser pane. These settings do not control agent-driven Browser Use. (Type: table)
- in_app_browser.allow_external_browser_settings_import: Set to `false` to prevent users from importing settings or browsing data from an external browser into the built-in browser. Setting it to `true` or omitting it leaves the import available when other product checks allow it. This is a managed-only setting with no `config.toml` override. (Type: boolean)
- browser_use: Managed requirements for agent-driven Browser Use. (Type: table)
- browser_use.extension: Managed settings for Browser Use in supported Chromium browser extensions. (Type: table)
- browser_use.extension.request_headers: Add up to 16 HTTP headers to requests from agent-controlled tabs in supported Chromium extensions. Use an empty list to send no managed headers. (Type: array<table>)
- browser_use.extension.request_headers[].name: Header name. Reserved names, including `Authorization` and `Cookie`, are prohibited. Names and values support `{{session_id}}` as their only substitution. (Type: string)
- browser_use.extension.request_headers[].value: Header value to send with matching browser requests. (Type: string)
- browser_use.allow_webmcp: Allow site tools (WebMCP) through workspace policy on eligible managed plans. Both `true` and an unset value allow access through this policy. Setting `false` turns off this path. Users can still have access through their account rollout. Browser settings and site permissions apply. (Type: boolean)
- browser_use.allow_history_access: Set to `false` to prevent Browser Use from reading browser history. Setting it to `true` or omitting it leaves normal history settings and availability checks in place. (Type: boolean)
- browser_use.disable_auto_review: Set to `true` to skip automatic review for Browser Use and ask the user for approval instead. Setting it to `false` or omitting it leaves automatic review available when other settings allow it. (Type: boolean)
- browser_use.allow_global_persistent_approval: Set to `false` to prevent Browser Use from creating or honoring `Always allow` approvals that cover every site, such as allowing downloads from any site. Existing saved approvals are ignored, not deleted. Setting it to `true` or omitting it does not create an approval. (Type: boolean)
- browser_use.default_origin_policy: Fallback for each Browser Use setting when no matching entry under `browser_use.origins` defines it. A matching origin rule replaces the fallback for that source. Codex then applies the stricter result from managed requirements and user configuration. (Type: table)
- browser_use.default_origin_policy.access: Use `deny` to block Browser Use on origins that use the fallback. A denied origin also blocks uploads, downloads, full browser debugging access, and automatic review there. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.default_origin_policy.downloads: Use `deny` to block Browser Use downloads on origins that use the fallback. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.default_origin_policy.uploads: Use `deny` to block Browser Use uploads on origins that use the fallback. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.default_origin_policy.full_cdp_access: Use `deny` to block full Chrome DevTools Protocol (CDP) access on origins that use the fallback. `allow` only lets normal opt-in and approval checks continue. (Type: allow | deny)
- browser_use.default_origin_policy.auto_review: Use `deny` to skip automatic review on origins that use the fallback and ask the user for approval instead. `allow` leaves automatic review available when other settings allow it. (Type: allow | deny)
- browser_use.default_origin_policy.persistent_approval: Set to `false` to prevent Browser Use from saving or honoring an `Always allow` approval on origins that use the fallback. Approvals for the current turn or thread can still apply. `true` makes `Always allow` available when otherwise permitted but does not create an approval. (Type: boolean)
- browser_use.default_origin_policy.access_approval_lifetime: Set how long a non-persistent site-access approval lasts: `turn` limits it to the current turn, and `thread` keeps it for the rest of the current thread. `persistent_approval` separately controls whether `Always allow` is available. The product default is `thread`. (Type: turn | thread)
- browser_use.origins: Origin-specific Browser Use policies. Keys use `<scheme>://<host-pattern>[:<port>]` with `http` or `https`. Use an exact host, `*.example.com` for subdomains only, or `**.example.com` for the base domain and its subdomains. Other `*` wildcards can span dots, so `region*.example.com` also matches `region.api.example.com`; a host of `*` matches every host for that scheme. Schemes and nondefault ports are significant; explicit default ports are normalized away. Paths, queries, embedded usernames or passwords, and wildcard schemes or ports are invalid. Quote the pattern in TOML, for example `[browser_use.origins."https://**.example.com"]`. (Type: map<string, table>)
- browser_use.origins.<pattern>: Policy for origins matching this pattern. If several patterns match, Codex uses the most restrictive value for each capability: `deny` over `allow`, `false` over `true`, and `turn` over `thread`. (Type: table)
- browser_use.origins.<pattern>.access: Use `deny` to block Browser Use on matching origins. Denial also blocks uploads, downloads, full browser debugging access, and automatic review there. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.origins.<pattern>.downloads: Use `deny` to block Browser Use downloads on matching origins. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.origins.<pattern>.uploads: Use `deny` to block Browser Use uploads on matching origins. `allow` only lets normal approval and policy checks continue. (Type: allow | deny)
- browser_use.origins.<pattern>.full_cdp_access: Use `deny` to block full Chrome DevTools Protocol (CDP) access on matching origins. `allow` only lets normal opt-in and approval checks continue. (Type: allow | deny)
- browser_use.origins.<pattern>.auto_review: Use `deny` to skip automatic review on matching origins and ask the user for approval instead. `allow` leaves automatic review available when other settings allow it. (Type: allow | deny)
- browser_use.origins.<pattern>.persistent_approval: Set to `false` to prevent Browser Use from saving or honoring an `Always allow` approval on matching origins. Approvals for the current turn or thread can still apply. `true` makes `Always allow` available when otherwise permitted but does not create an approval. (Type: boolean)
- browser_use.origins.<pattern>.access_approval_lifetime: Set how long a non-persistent site-access approval for matching origins lasts: `turn` limits it to the current turn, and `thread` keeps it for the rest of the current thread. `persistent_approval` separately controls whether `Always allow` is available. (Type: turn | thread)
- computer_use: Managed requirements for agent-driven work in native desktop apps. Managed app rules and `config.toml` app rules are both enforced; an app must be allowed by each policy source. (Type: table)
- computer_use.allow_locked_computer_use: Set to `false` to prevent users from enabling Locked Use on a managed macOS device. This requirement removes the enablement controls; it does not turn off Locked Use if it is already enabled. If omitted, normal product availability applies. (Type: boolean)
- computer_use.allow_persistent_approval: Set to `false` to remove the option to save app approvals across sessions. Approvals for the current session remain available. Setting it to `true` or omitting it does not approve an app. (Type: boolean)
- computer_use.default_app_access: Fallback access for native apps that do not match a platform-specific rule. `deny` blocks access. `allow` only lets normal approval and policy checks continue. The product default is `allow`. (Type: allow | deny)
- computer_use.macos: Computer Use app rules for macOS. (Type: table)
- computer_use.macos.bundle_ids: Map exact macOS bundle identifiers to `allow` or `deny`. A matching rule replaces `computer_use.default_app_access` within the same policy source. A deny from either managed requirements or user configuration still blocks access. (Type: map<string, allow | deny>)
- computer_use.macos.bundle_ids.<bundle-id>: Use `deny` to block the exact bundle identifier. `allow` overrides only this policy source's default and still requires any other policy source and the normal approval flow to allow the app. (Type: allow | deny)
- computer_use.windows: Computer Use app rules for packaged and unpackaged Windows apps. (Type: table)
- computer_use.windows.aumids: Map exact, registered Application User Model IDs (AUMIDs) for signed packaged apps to `allow` or `deny`. A matching rule replaces `computer_use.default_app_access` within the same policy source. (Type: map<string, allow | deny>)
- computer_use.windows.aumids.<aumid>: Use `deny` to block the exact packaged-app identity. `allow` overrides only this policy source's default and still requires any other policy source and the normal approval flow to allow the app. (Type: allow | deny)
- computer_use.windows.exes: Rules for signed, unpackaged Windows executables. Rules match the executable's verified publisher and signed version information, not its path or current file name. A matching deny takes precedence over matching allows. Unsigned executables use `computer_use.default_app_access`; executables whose signed identity cannot be verified unambiguously are blocked. (Type: array<table>)
- computer_use.windows.exes[].publisher_name: Required exact publisher name from the executable's trusted signing certificate, formatted as a Windows X.500 distinguished name. (Type: string)
- computer_use.windows.exes[].product_name: Required exact `ProductName` from the executable's signed version information. (Type: string)
- computer_use.windows.exes[].binary_name: Optional `OriginalFilename` from the executable's signed version information. Matching is case-insensitive. If a matching publisher and product rule requires this value but the executable does not provide it, Computer Use blocks the executable. (Type: string)
- computer_use.windows.exes[].access: Required access decision for matching executables. `deny` blocks access. `allow` overrides only this policy source's default and still requires any other policy source and the normal approval flow to allow the app. (Type: allow | deny)
- application: Managed desktop application requirements. (Type: table)
- application.storage: Pin storage locations for newly created work on desktop builds that support managed storage. Each path independently overrides the local preference. Storage settings do not restrict filesystem access. (Type: table)
- application.storage.default_project_parent: Parent directory for new local projects created with Start from scratch. (Type: string (absolute path))
- application.storage.projectless_workspace_root: Root directory for new chats created without a project. (Type: string (absolute path))
- application.network: Destination restrictions for desktop app network requests, separate from command networking and browser origin rules. This doesn't impose destination restrictions on native modules or spawned processes. (Type: table)
- application.network.enabled: Defaults to true when the table is present. When true, external desktop app requests require an explicitly allowed domain. An empty domain map allows no external destinations. An absent application network policy or false value doesn't restrict destinations through this policy. (Type: boolean)
- application.network.domains: Exact domain rules for desktop app requests. Enabled policies allow HTTPS and WSS requests only to explicitly allowed domains; subdomains aren't implicitly allowed. (Type: table<allow | deny>)
- application.network.domains.<domain>: Allow or deny an exact domain. Use domain names without URL schemes, ports, or wildcards. (Type: allow | deny)
- otel: Enforce the specified OpenTelemetry settings. Each exporter replaces the entire corresponding exporter definition. Span attributes and tracestate fields override only matching entries. (Type: table)
- otel.environment: Enforce the environment label on telemetry. (Type: string)
- otel.exporter: Enforce the log exporter, including its endpoint, headers, and TLS settings. (Type: none | otlp-http | otlp-grpc)
- otel.trace_exporter: Enforce the trace exporter, including its endpoint, headers, and TLS settings. (Type: none | otlp-http | otlp-grpc)
- otel.metrics_exporter: Enforce the metrics exporter. The Statsig exporter follows `analytics.enabled`. Explicit OTLP metrics exporters run independently of that setting. (Type: none | statsig | otlp-http | otlp-grpc)
- otel.log_user_prompt: Control whether exported logs include user prompt text. (Type: boolean)
- otel.log_agent_responses: Control whether OTLP logs include final response text from the main agent and spawned subagents. (Type: boolean)
- otel.log_guardian_assessments: Control whether OTLP logs include completed automatic approval assessments and their rationales. (Type: boolean)
- otel.tool_result: Enforce the tool-result log settings as a unit. An empty table enforces the default byte limit. (Type: table)
- otel.tool_result.max_bytes: Maximum UTF-8 bytes of tool-result text before the truncation notice in logs. Defaults to `2048` when the managed table is present. (Type: integer (nonnegative))
- otel.span_attributes: Enforce individual string attributes on exported spans. Higher-priority requirements win for the same attribute. (Type: map<string,string>)
- otel.tracestate: Enforce individual fields within W3C tracestate members. Higher-priority requirements win for the same member and field. (Type: map<string,map<string,string>>)
- network_proxy: Administrator-managed network requirements for sandboxed local commands. Codex 0.166.0 accepts `[network_proxy]` and its alias `[experimental_network]`. Use one name per requirements layer. Keep the alias in published policies until every client and policy validator supports the new name. When enabled, these requirements can start the command network proxy without `features.network_proxy`. Browser tools separately check managed network denies and exclusive allowlists. These requirements do not route browser traffic through the proxy or control web search, apps, MCP servers, native-app traffic, or other capability-specific traffic. On supported managed Codex Cloud paths, these requirements constrain command networking alongside separate Cloud environment internet settings. Approved full sandbox escalation can bypass the command proxy where policy permits it. Work Cloud does not inherit these requirements. (Type: table)
- network_proxy.enabled: Enable sandboxed networking requirements. This does not grant network access when the active sandbox keeps command networking off. (Type: boolean)
- network_proxy.http_port: Loopback HTTP listener port to use for `[network_proxy]` requirements. (Type: integer)
- network_proxy.socks_port: Loopback SOCKS5 listener port to use for `[network_proxy]` requirements. (Type: integer)
- network_proxy.allow_upstream_proxy: Allow sandboxed networking to chain through an upstream proxy from the environment. (Type: boolean)
- network_proxy.dangerously_allow_non_loopback_proxy: Permit non-loopback listener addresses for `[network_proxy]` requirements. Enabling it can expose listeners beyond localhost. (Type: boolean)
- network_proxy.dangerously_allow_all_unix_sockets: Permit arbitrary Unix socket destinations instead of allowlist-only access. Use only in tightly controlled environments. (Type: boolean)
- network_proxy.domains: Map-shaped administrator domain policy for sandboxed networking. Supports exact hosts, `*.example.com` for subdomains only, `**.example.com` for apex plus subdomains, and global `*` allow rules. Prefer scoped rules because `*` broadly opens public outbound access. Environment rules can replace the same Global domain key within a policy. Higher-priority values replace the same key, while other inherited keys remain. After composition, a different matching `deny`, including an inherited wildcard, still blocks a request. Empty environment maps do not clear Global rules. Verify executor support. Do not combine this with `network_proxy.allowed_domains` or `network_proxy.denied_domains`. (Type: map<string, allow | deny>)
- network_proxy.domains.<pattern>: Allow or deny sandboxed network access for the matching domain pattern. A deny rule wins when several patterns match. (Type: allow | deny)
- network_proxy.review_domains: Route matching hosts through network approval even if an allow rule matches. An explicit deny takes precedence. Approved requests still undergo DNS and private-address checks. Defaults to an empty list. (Type: array<string>)
- network_proxy.allowed_domains: Administrator allow rules for sandboxed-command networking while the managed network proxy is enabled. These rules do not apply to web search, apps, or MCP servers. Do not combine this with `network_proxy.domains`. (Type: array<string>)
- network_proxy.denied_domains: List-shaped administrator deny rules for sandboxed networking. Do not combine this with `network_proxy.domains`. (Type: array<string>)
- network_proxy.managed_allowed_domains_only: When networking requirements are enabled and this is true, ordinary user configuration and per-domain approvals cannot expand the managed proxy allowlist. With no effective configured or inherited Allow entries, ordinary managed commands have no allowed destinations. A deny-only policy does not allow the rest of the internet. This does not cover every tool or approved full sandbox escalation. (Type: boolean)
- network_proxy.unix_sockets: Administrator-managed Unix socket allowlist for sandboxed networking on macOS. Paths must be absolute. (Type: map<string, allow | deny>)
- network_proxy.unix_sockets.<path>: On macOS, `allow` adds an absolute Unix socket path to the allowlist; `deny` leaves it out. A `deny` entry cannot block a socket when allow-all Unix sockets is enabled. (Type: allow | deny)
- network_proxy.allow_local_binding: Permit broader local/private-network access for sandboxed networking. On the supported Codex Cloud proxy path, an explicit false can prevent upstream-proxy access even if a domain is allowed. It defaults to true only if no applicable requirement, selected network profile, or proxy feature setting provides a value. Inherited false remains explicit. A supported higher-priority Cloud override can change it without broadening Global for Local or adding domain Allow entries. Verify executor support. Do not apply this Cloud default to Local. (Type: boolean)
- hooks: Admin-enforced managed lifecycle hooks. Requires a managed hook directory and uses the same event schema as inline `[hooks]` in `config.toml`. (Type: table)
- hooks.managed_dir: Directory containing managed hook scripts on macOS and Linux. Codex validates that it is absolute and exists before loading managed hooks. (Type: string (absolute path))
- hooks.windows_managed_dir: Directory containing managed hook scripts on Windows. Codex validates that it is absolute and exists before loading managed hooks. (Type: string (absolute path))
- hooks.<Event>: Matcher groups for a hook event such as `PreModelRequest`, `PostModelRequest`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, or `Stop`. (Type: array<table>)
- hooks.<Event>[].hooks: Hook handlers for a matcher group. Command and MCP tool hooks are supported while prompt and agent hook handlers are parsed but skipped. (Type: array<table>)
- hooks.<Event>[].hooks[].async: Run a command hook in the background without delaying the triggering operation. Defaults to `false`; `SessionEnd` always runs synchronously. See [Run hooks in the background](https://learn.chatgpt.com/docs/hooks#run-hooks-in-the-background). (Type: boolean)
- hooks.<Event>[].hooks[].additionalContextLimit: Approximate per-handler token threshold for saving oversized `additionalContext` to disk and showing the model a shorter preview. Defaults to `2500`; `0` passes the full context directly to the model. See [Large hook output](https://learn.chatgpt.com/docs/hooks#large-hook-output). (Type: integer)
- hooks.<Event>[].hooks[].commandWindows: Windows-only command override for command hooks. The TOML alias `command_windows` is also accepted. (Type: string)
- permissions.filesystem.deny_read: Admin-enforced filesystem read denials. Entries can be paths or glob patterns, and users cannot weaken them with local config. (Type: array<string>)
- mcp_servers: Allowlist of MCP servers that may be enabled. Both the server name (`<id>`) and its identity must match for the MCP server to be enabled. Any configured MCP server not in the allowlist (or with a mismatched identity) is disabled. (Type: table)
- mcp_servers.<id>.identity: Identity rule for a single MCP server. Set either `command` (stdio) or `url` (streamable HTTP). (Type: table)
- mcp_servers.<id>.identity.command: Allow an MCP stdio server by exact command string, or use a matcher table to require an exact executable and ordered argument matchers. The string form doesn't inspect arguments, `cwd`, `env`, or `env_vars`. (Type: string | table)
- mcp_servers.<id>.identity.command.executable: Executable that the stdio server's configured `command` must match exactly. (Type: string)
- mcp_servers.<id>.identity.command.args: Ordered argument matchers for a stdio server. The configured argument list must have the same length, and every position must match. Command matchers don't inspect `cwd`, `env`, or `env_vars`. (Type: array<table>)
- mcp_servers.<id>.identity.command.args[].match: Match operation for this argument position. (Type: exact | prefix | regex)
- mcp_servers.<id>.identity.command.args[].value: Value used by an `exact` or `prefix` argument matcher. (Type: string)
- mcp_servers.<id>.identity.command.args[].expression: Regular expression used by a `regex` argument matcher. The expression must be valid and match the complete argument value. (Type: string)
- mcp_servers.<id>.identity.url: Allow an MCP streamable HTTP server by exact URL string, or use an `exact`, `prefix`, or `regex` value matcher table. (Type: string | table)
- mcp_servers.<id>.identity.url.match: Match operation for the configured MCP server URL. (Type: exact | prefix | regex)
- mcp_servers.<id>.identity.url.value: Value used by an `exact` or `prefix` URL matcher. (Type: string)
- mcp_servers.<id>.identity.url.expression: Regular expression used by a `regex` URL matcher. The expression must be valid and match the complete URL value. (Type: string)
- plugins: Plugin-specific MCP server allowlists keyed by plugin identifier. When this table is present, plugin-bundled servers without a matching plugin and server entry are disabled. (Type: table)
- plugins.<plugin>.mcp_servers: Allowlist for MCP servers bundled with one plugin. Plugin server requirements use the same exact identity and matcher forms as top-level `mcp_servers` requirements. (Type: table)
- plugins.<plugin>.mcp_servers.<server>.identity: Identity rule for one plugin-bundled MCP server. Set either `command` (stdio) or `url` (streamable HTTP). (Type: table)
- plugins.<plugin>.mcp_servers.<server>.identity.command: Allow a plugin's stdio MCP server by exact command string, or use a matcher table to require an exact executable and ordered argument matchers. (Type: string | table)
- plugins.<plugin>.mcp_servers.<server>.identity.command.executable: Executable that the plugin-bundled stdio server's configured command must match exactly. (Type: string)
- plugins.<plugin>.mcp_servers.<server>.identity.command.args: Ordered argument matchers for a plugin-bundled stdio server. The configured argument list must have the same length, and every position must match. (Type: array<table>)
- plugins.<plugin>.mcp_servers.<server>.identity.command.args[].match: Match operation for this argument position. (Type: exact | prefix | regex)
- plugins.<plugin>.mcp_servers.<server>.identity.command.args[].value: Value used by an `exact` or `prefix` argument matcher. (Type: string)
- plugins.<plugin>.mcp_servers.<server>.identity.command.args[].expression: Regular expression used by a `regex` argument matcher. The expression must match the complete argument value. (Type: string)
- plugins.<plugin>.mcp_servers.<server>.identity.url: Allow a plugin's streamable HTTP MCP server by exact URL string, or use an `exact`, `prefix`, or `regex` value matcher table. (Type: string | table)
- plugins.<plugin>.mcp_servers.<server>.identity.url.match: Match operation for the plugin-bundled MCP server URL. (Type: exact | prefix | regex)
- plugins.<plugin>.mcp_servers.<server>.identity.url.value: Value used by an `exact` or `prefix` URL matcher. (Type: string)
- plugins.<plugin>.mcp_servers.<server>.identity.url.expression: Regular expression used by a `regex` URL matcher. The expression must match the complete URL value. (Type: string)
- marketplaces: Admin requirements for plugin marketplace sources. Rules take effect when `restrict_to_allowed_sources` is `true`. (Type: table)
- marketplaces.restrict_to_allowed_sources: When `true`, require configured marketplace sources to match `allowed_sources` for marketplace add, plugin install, refresh, and runtime loading. OpenAI-curated Git catalogs, including the API-key catalog, must also match the allowlist. Bundled and remotely installed workspace plugins are separate from this curated Git source policy. (Type: boolean)
- marketplaces.allowed_sources: Allowed marketplace sources keyed by administrator-chosen rule name. Distinct names accumulate across requirements layers; fields under the same name use normal layer precedence. (Type: table)
- marketplaces.allowed_sources.<name>: One allowed source rule. The final `source` value after requirements merge determines which sibling fields Codex interprets. (Type: table)
- marketplaces.allowed_sources.<name>.source: Marketplace source matcher type. Use `git` for one repository, `host_pattern` for Git hosts matched by regular expression, or `local` for one directory. (Type: git | host_pattern | local)
- marketplaces.allowed_sources.<name>.url: Git repository URL required when `source = "git"`. Codex normalizes the configured and allowed URLs before requiring an exact repository match. (Type: string)
- marketplaces.allowed_sources.<name>.ref: Optional exact Git ref for a `git` rule. When omitted, the rule allows any ref for the matching repository. (Type: string)
- marketplaces.allowed_sources.<name>.host_pattern: Regular expression required when `source = "host_pattern"`. Codex matches it against the lowercase hostname parsed from an HTTPS, SSH, or SCP-style Git source. Use `^` and `$` to require a whole-host match. (Type: string)
- marketplaces.allowed_sources.<name>.path: Local marketplace directory required when `source = "local"`. Codex requires an absolute path and compares paths after normalization. (Type: string (absolute path))
- apps: Managed app requirements keyed by app identifier. Requirements can disable an app or constrain approval behavior for individual tools. (Type: table)
- apps.<id>.enabled: Set to `false` to disable an app. A disabled requirement remains restrictive when multiple requirements sources are merged. (Type: boolean)
- apps.<id>.tools.<tool>.approval_mode: Set the managed approval mode for one app tool. (Type: auto | prompt | writes | approve)
- rules: Admin-enforced command rules merged with `.rules` files. Requirements rules must be restrictive. (Type: table)
- rules.prefix_rules: List of enforced prefix rules. Each rule must include `pattern` and `decision`. (Type: array<table>)
- rules.prefix_rules[].pattern: Command prefix expressed as pattern tokens. Each token sets either `token` or `any_of`. (Type: array<table>)
- rules.prefix_rules[].pattern[].token: A single literal token at this position. (Type: string)
- rules.prefix_rules[].pattern[].any_of: A list of allowed alternative tokens at this position. (Type: array<string>)
- rules.prefix_rules[].decision: Required. Requirements rules can only prompt or forbid (not allow). (Type: prompt | forbidden)
- rules.prefix_rules[].justification: Optional non-empty rationale surfaced in approval prompts or rejection messages. (Type: string)
