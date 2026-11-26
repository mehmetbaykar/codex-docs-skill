---
title: "Turn an issue into a tested pull request"
source: https://learn.chatgpt.com/use-cases/issue-to-tested-pr
path: /use-cases/issue-to-tested-pr
---

# Turn an issue into a tested pull request

Hand off a small feature with acceptance criteria and review the evidence.

Give Codex a scoped issue, a prepared cloud environment, and explicit checks. Get an implementation, tests, documentation, and a reviewable change with evidence for each acceptance criterion.

## Recipe details

```yaml
name: Turn an issue into a tested pull request
tagline: Hand off a small feature with acceptance criteria and review the evidence.
summary: Give Codex a scoped issue, a prepared cloud environment, and explicit
  checks. Get an implementation, tests, documentation, and a reviewable change
  with evidence for each acceptance criterion.
bestFor:
  - Startup engineers implementing a scoped API issue.
  - Reviewers who need implementation and validation evidence together.
  - Teams with acceptance criteria and a working test environment.
starterPrompt:
  title: Implement a scoped issue
  body: >-
    Implement [issue ID and title] in [repository] at [base branch and commit],

    using the prepared cloud environment I selected for this task.

    Input packet: [paste or attach the issue, acceptance criteria, relevant

    files, public success/error schemas, authorization and pagination contract,

    test fixtures, and approved validation commands].

    Repository instructions: [AGENTS.md and any relevant nested instructions].

    Scope: [files or component boundaries].

    Out of scope: [explicit exclusions].

    Required checks: [focused tests, relevant regression tests, type check,

    lint, and any required CI checks].

    Output: [create a draft PR in this repository if the available integration

    supports it and I authorize it here / return a diff and draft PR
    description].

    First read the instructions and relevant code. Confirm the starting commit

    and run the existing baseline checks using the execution tools available

    in this environment. Record any new test files as still to be created.

    If the baseline fails, access is missing, or a

    required check cannot run, report the exact blocker before implementing.

    State a short plan, then implement the smallest change that meets the

    acceptance criteria. Follow existing auth, error, pagination, and testing

    patterns. Add tests that distinguish the required behavior from the old

    behavior. For this pagination example, require tied timestamps across a

    page boundary, bounded traversal and replay on fixed fixtures, partial and

    exact-full final pages, authorization before cursor validation, invalid

    cursor cases, and success/error schema checks. Update the affected API

    documentation to match the implemented public response exactly.

    After implementation, run the required checks again. For every acceptance

    criterion, point to the test or other evidence that verifies it. Record

    commands, results, the tested commit or working-tree state, and any checks

    that were not run. Separate pre-existing failures from new failures.

    Never describe an unrun check as passing.

    Deliver the diff or authorized draft PR, a concise change summary, the

    acceptance-criteria evidence table, remaining risks, and reviewer actions.

    Do not merge, deploy, use production data, change permissions, add new

    dependencies, or expand the agreed scope. Stop for a decision if the

    contract conflicts with the repository or the work needs a schema change.
relatedLinks:
  - label: Download the runnable sample
    url: https://learn.chatgpt.com/docs/use-cases/issue-to-tested-pr/sample.zip
  - label: Cloud environments
    url: https://learn.chatgpt.com/docs/environments/cloud-environments
  - label: Keep documentation up-to-date
    url: https://learn.chatgpt.com/use-cases/update-documentation
```

Hand Codex a small, well-defined issue and ask for a change a teammate can review: implementation, tests, documentation, and evidence that the requested behavior works. Keep the task in one prepared cloud environment so the code and validation use the same repository setup.

1. In the web or desktop app, choose **Work in** > **Cloud** and select a published environment.

2. To create one, select **Create environment**, choose the GitHub repositories, and ask Codex to prepare the runtime, dependencies, and isolated test services.

3. Review the setup report, resolve failed checks, and **Publish** before starting a new task.

- Follow the [current Cloud environment guide](https://learn.chatgpt.com/docs/environments/cloud-environments).
- Keep repository guidance in [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

If dependencies change or service setup changes, edit the reusable environment, test it, and **Republish**, then verify the changes in a new task.

Repository refresh does not rerun install/start commands, and existing tasks keep their own state.

Configure required network destinations and test credentials separately; allowing a destination does not grant service access.

If required checks cannot run, finish setup before using this workflow.

## When to use it

Choose a feature with a written contract and a clear stopping point: a new API endpoint, a validation rule, or a small addition to an existing service. The issue should fit in one pull request and have checks that can run without production access.

The example adds pagination to a project's activity feed. The runnable TypeScript sample includes authentication, project access, signed cursors, and an existing project-detail route. It uses fixed test records in memory, so you can check the pagination contract without a database or external service.

## Try the runnable sample

[Download the sample](https://developers.openai.com/codex/use-cases/issue-to-tested-pr/sample.zip), extract it, and open its `issue-to-tested-pr` folder. Use **Node 22.6 or later**. The sample uses the standard library and needs no package installation or API key.

```bash
node --version
node --experimental-strip-types api.ts
node --experimental-strip-types test.ts --seeded
node --experimental-strip-types test.ts
node --experimental-strip-types reproduce.ts ./evidence
```

`node --experimental-strip-types api.ts` starts a local HTTP server, requests the first page, prints its public IDs, and closes the server.

The `--seeded` test run deliberately exits nonzero: its timestamp-only continuation skips two events tied at the first page boundary. The same tests pass with the corrected timestamp-and-ID tuple continuation.

The reproduction command succeeds only if the seeded state fails and the corrected state passes.

The corrected traversal with `limit=2` returns these pages in three requests:

```text
[evt_105, evt_104]
[evt_103, evt_102]
[evt_101]
```

The first two pages have a continuation cursor; the final page has `next_cursor: null`.

The seeded state returns `[evt_105, evt_104]`, then `[evt_101]`, losing `evt_103` and `evt_102`.

A successful run passes all 36 tests in the corrected state. The seeded state fails three assertions that expose the pagination defect.

To verify your environment, put the files in your selected repository, prepare and publish an environment with a supported Node runtime, then run the commands in a new Cloud task and record its results.

`reproduce.ts` saves `red.log`, `green.log`, `observed-http.json`, and `run-manifest.json` in the requested evidence directory. The manifest identifies the runtime, commands, exit codes, seeded defect, correction, and SHA-256 source hashes.

It does not record session tokens or the signing key. Read `README.md` and `openapi.json` for the sample's setup and public contract.

**Java setup**

Use Java 17 or later and Maven with a complete `developers-website` checkout, including the [Java sample project](https://github.com/openai/developers-website/tree/main/src/content/platform/java-examples), its `pom.xml`, and `src/main/java/codex-cloud` files intact.

Start at the repository checkout root in a POSIX shell. The tests require the sibling `../typescript-examples/codex-cloud/issue-to-tested-pr/openapi.json` contract, relative to the Java project directory, from the same checkout.

```bash
cd src/content/platform/java-examples
mvn -q -DskipTests compile dependency:build-classpath -Dmdep.outputFile=target/live-classpath
java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudApi
java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudTest --seeded
java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudTest
java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudReproduce ./evidence
```

**Expected results**

- The seeded test fails on the deliberate timestamp-only defect.
- The corrected test passes.
- `CodexCloudReproduce` saves logs for the failing seeded run and passing corrected run in `./evidence`.

Use these commands in place of the Node commands for the Java tab.

For Ruby, use the complete [Ruby sample project](https://github.com/openai/developers-website/tree/main/src/content/platform/ruby-examples) with its `Gemfile`, lockfile, and `codex-cloud` directory intact. Install its dependencies using Ruby 3.3. From the Ruby project directory, run `bundle exec ruby codex-cloud/api/main.rb`, `bundle exec ruby codex-cloud/test.rb --seeded`, `bundle exec ruby codex-cloud/test.rb`, and `bundle exec ruby codex-cloud/reproduce/main.rb ./evidence`. The seeded test deliberately fails; the corrected test passes. These Ruby commands replace the TypeScript commands above.

Use Go 1.26 or later with a full [repository checkout](https://github.com/openai/developers-website). Keep the `src/content/platform/go-examples/` module (`go.mod` and `go.sum`) and the sibling `typescript-examples/codex-cloud` files intact. Start the commands below at the repository root.

```bash
cd src/content/platform/go-examples/codex-cloud/issue-to-tested-pr
go run . api
go run . fixtures
go run . --seeded -test.v test
go run . -test.v test
go run . reproduce ./evidence
```

The Go tests read the canonical `../../../typescript-examples/codex-cloud/issue-to-tested-pr/openapi.json` from this example directory. The ZIP and Node commands above target TypeScript.

Expected results

- The seeded test exits with a nonzero status.
- The corrected test exits successfully.
- The reproduction writes red and green logs to a new `./evidence` directory.

### Inspect the runnable sample

The TypeScript excerpts come from the ZIP.

The Ruby examples come from the linked Ruby sample project.

**Full programs**

Use the selected language's project, supporting files, and launch commands above. The excerpts below highlight the implementation.

<details>
<summary>Cursor and ordering implementation</summary>
Create the example API

```typescript
import { createFixtures } from "./fixtures.ts";
type Fixtures = ReturnType<typeof createFixtures>;
type EventKey = { created_at: string; id: string };

export function createApi({
  sessions,
  projects,
  events,
  signingKey,
  seededBug = false,
}: Fixtures & { seededBug?: boolean }) {
  return createServer((request, response) => {
    const send = (status: number, body: unknown) => {
      response.writeHead(status, { "content-type": "application/json" });
      response.end(JSON.stringify(body));
    };
    const fail = (code: string) => {
      const [status, message] = errors[code];
      send(status, { error: { code, message } });
    };
    // Authenticate, then authorize. Malformed parameters must not change these results.
    const authorization = request.headers.authorization ?? "";
    const bearer = /^Bearer ([A-Za-z0-9_-]+)$/.exec(authorization);
    const tenantId = bearer ? sessions.get(bearer[1]) : undefined;
    if (!tenantId) return fail("unauthenticated");

    const url = new URL(request.url ?? "/", "http://127.0.0.1");
    const route = /^\/v1\/projects\/([^/]+)(\/events)?$/.exec(url.pathname);
    let projectId;
    try {
      projectId = route ? decodeURIComponent(route[1]) : undefined;
    } catch {
      return fail("not_found");
    }
    const project = projectId ? projects.get(projectId) : undefined;
    if (
      request.method !== "GET" ||
      !route ||
      !project ||
      project.tenant_id !== tenantId
    ) {
      return fail("not_found");
    }
    // Existing project-detail behavior remains independent of pagination parameters.
    if (!route[2]) return send(200, { id: projectId, name: project.name });

    const rawLimit = url.searchParams.get("limit");
    const limit = rawLimit === null ? 25 : Number(rawLimit);
    if (
      url.searchParams.getAll("limit").length > 1 ||
      (rawLimit !== null && !/^\d+$/.test(rawLimit)) ||
      !Number.isInteger(limit) ||
      limit < 1 ||
      limit > 100
    ) {
      return fail("invalid_limit");
    }
    let cursor: EventKey | undefined;
    if (url.searchParams.has("cursor")) {
      try {
        if (url.searchParams.getAll("cursor").length !== 1)
          throw new Error("Invalid cursor");
        cursor = decodeCursor(
          url.searchParams.get("cursor"),
          tenantId,
          projectId,
          signingKey
        );
      } catch {
        return fail("invalid_cursor");
      }
    }

    const matching = events
      .filter(
        (event) =>
          event.tenant_id === tenantId && event.project_id === projectId
      )
      .sort(compareEvents)
      .filter((event) => {
        if (!cursor) return true;
        // Deliberate baseline defect: timestamp-only continuation loses tied rows.
        if (seededBug)
          return (
            timestampValue(event.created_at) < timestampValue(cursor.created_at)
          );
        return compareEvents(event, cursor) > 0;
      });
    const selected = matching.slice(0, limit);
    const items = selected.map(({ id, created_at, type, summary }) => ({
      id,
      created_at,
      type,
      summary,
    }));
    const nextCursor =
      matching.length > limit
        ? encodeCursor(
            selected[selected.length - 1],
            tenantId,
            projectId,
            signingKey
          )
        : null;
    return send(200, { items, next_cursor: nextCursor });
  });
}

export async function startApi(
  fixtures: Fixtures,
  options: { seededBug?: boolean } = {}
) {
  const server = createApi({ ...fixtures, ...options });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve(undefined));
  });
  const address = server.address();
  if (!address || typeof address === "string")
    throw new Error("No listening address");
  return {
    baseUrl: `http://127.0.0.1:${address.port}`,
    close: () =>
      new Promise((resolve, reject) =>
        server.close((error) => (error ? reject(error) : resolve(undefined)))
      ),
  };
}
```

```go
type page struct {
	Items      []event `json:"items"`
	NextCursor *string `json:"next_cursor"`
}
type cursor struct {
	Version   int    `json:"version"`
	Tenant    string `json:"tenant_id"`
	Project   string `json:"project_id"`
	CreatedAt string `json:"created_at"`
	ID        string `json:"id"`
}

var timestampPattern = regexp.MustCompile(`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$`)

func timestamp(value string) (time.Time, error) {
	if !timestampPattern.MatchString(value) {
		return time.Time{}, errors.New("invalid timestamp")
	}
	return time.Parse(time.RFC3339Nano, value)
}

// Compare parsed instants, without truncating submillisecond fractions.
func compare(left, right event) int {
	a, err := timestamp(left.CreatedAt)
	if err != nil {
		panic(err)
	}
	b, err := timestamp(right.CreatedAt)
	if err != nil {
		panic(err)
	}
	if a.After(b) {
		return -1
	}
	if a.Before(b) {
		return 1
	}
	return -strings.Compare(left.ID, right.ID)
}
func sign(payload string, key []byte) string {
	mac := hmac.New(sha256.New, key)
	_, _ = mac.Write([]byte(payload))
	return payload + "." + base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
}
func encodeCursor(e event, tenant, project string, key []byte) string {
	data, err := json.Marshal(cursor{1, tenant, project, e.CreatedAt, e.ID})
	if err != nil {
		panic(err)
	}
	return sign(base64.RawURLEncoding.EncodeToString(data), key)
}
func decodeCursor(token, tenant, project string, key []byte) (event, error) {
	bad := errors.New("invalid cursor")
	parts := strings.Split(token, ".")
	if len(token) > 2048 || len(parts) != 2 {
		return event{}, bad
	}
	decode := func(s string) ([]byte, error) {
		b, err := base64.RawURLEncoding.Strict().DecodeString(s)
		if err != nil || len(s) == 0 || base64.RawURLEncoding.EncodeToString(b) != s {
			return nil, bad
		}
		return b, nil
	}
	data, err := decode(parts[0])
	if err != nil {
		return event{}, bad
	}
	signature, err := decode(parts[1])
	if err != nil {
		return event{}, bad
	}
	mac := hmac.New(sha256.New, key)
	_, _ = mac.Write([]byte(parts[0]))
	if !hmac.Equal(signature, mac.Sum(nil)) {
		return event{}, bad
	}
	// Reject missing, duplicate, unknown and null fields, including signed payloads.
	decoder := json.NewDecoder(bytes.NewReader(data))
	opening, err := decoder.Token()
	if err != nil || opening != json.Delim('{') {
		return event{}, bad
	}
	fields := map[string]json.RawMessage{}
	for decoder.More() {
		name, err := decoder.Token()
		if err != nil {
			return event{}, bad
		}
		field, ok := name.(string)
		if !ok {
			return event{}, bad
		}
		if _, exists := fields[field]; exists {
			return event{}, bad
		}
		var value json.RawMessage
		if decoder.Decode(&value) != nil {
			return event{}, bad
		}
		fields[field] = value
	}
	if _, err := decoder.Token(); err != nil {
		return event{}, bad
	}
	var trailing any
	if decoder.Decode(&trailing) != io.EOF || len(fields) != 5 {
		return event{}, bad
	}
	for _, name := range []string{"version", "tenant_id", "project_id", "created_at", "id"} {
		value, ok := fields[name]
		if !ok || bytes.Equal(value, []byte("null")) {
			return event{}, bad
		}
	}
	var c cursor
	strict := json.NewDecoder(bytes.NewReader(data))
	strict.DisallowUnknownFields()
	if strict.Decode(&c) != nil || c.Version != 1 || c.Tenant != tenant || c.Project != project || c.ID == "" {
		return event{}, bad
	}
	if _, err := timestamp(c.CreatedAt); err != nil {
		return event{}, bad
	}
	return event{ID: c.ID, CreatedAt: c.CreatedAt}, nil
}

type publicError struct {
	Error struct {
		Code    string `json:"code"`
		Message string `json:"message"`
	} `json:"error"`
}

func failure(code string) (int, publicError) {
	status, message := 400, "Invalid cursor."
	switch code {
	case "invalid_limit":
		message = "Limit must be an integer from 1 through 100."
	case "unauthenticated":
		status, message = 401, "Authentication required."
	case "not_found":
		status, message = 404, "Project not found."
	}
	var body publicError
	body.Error.Code = code
	body.Error.Message = message
	return status, body
}

// Decode each query field independently, preserving invalid escapes for validation.
// Unlike url.ParseQuery, URLSearchParams does not treat a semicolon as a separator.
func parameters(raw string) url.Values {
	result := url.Values{}
	decode := func(value string) string {
		decoded, err := url.QueryUnescape(value)
		if err != nil {
			return value
		}
		return decoded
	}
	for _, field := range strings.Split(raw, "&") {
		if field == "" {
			continue
		}
		name, value, _ := strings.Cut(field, "=")
		result.Add(decode(name), decode(value))
	}
	return result
}

// createAPI keeps authentication and project authorization ahead of pagination.
func createAPI(f fixtures, seededBug bool) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		send := func(status int, body any) {
			data, err := json.Marshal(body)
			if err != nil {
				http.Error(w, "encoding failure", 500)
				return
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(status)
			if _, err := w.Write(data); err != nil {
				fmt.Fprintln(os.Stderr, "write response:", err)
			}
		}
		fail := func(code string) { status, body := failure(code); send(status, body) }
		auth := r.Header.Get("Authorization")
		token, ok := strings.CutPrefix(auth, "Bearer ")
		tenant := f.Sessions[token]
		if !ok || tenant == "" {
			fail("unauthenticated")
			return
		}
		path := strings.Split(strings.TrimPrefix(r.URL.EscapedPath(), "/"), "/")
		if r.Method != "GET" || (len(path) != 3 && len(path) != 4) || path[0] != "v1" || path[1] != "projects" || (len(path) == 4 && path[3] != "events") {
			fail("not_found")
			return
		}
		projectID, err := url.PathUnescape(path[2])
		p, exists := f.Projects[projectID]
		if err != nil || !exists || p.Tenant != tenant {
			fail("not_found")
			return
		}
		if len(path) == 3 {
			send(200, map[string]string{"id": projectID, "name": p.Name})
			return
		}
		parameters := parameters(r.URL.RawQuery)
		limit := 25
		if values, present := parameters["limit"]; present {
			if len(values) != 1 || !regexp.MustCompile(`^[0-9]+$`).MatchString(values[0]) {
				fail("invalid_limit")
				return
			}
			limit, err = strconv.Atoi(values[0])
			if err != nil || limit < 1 || limit > 100 {
				fail("invalid_limit")
				return
			}
		}
		var after *event
		if values, present := parameters["cursor"]; present {
			if len(values) != 1 {
				fail("invalid_cursor")
				return
			}
			value, err := decodeCursor(values[0], tenant, projectID, f.SigningKey)
			if err != nil {
				fail("invalid_cursor")
				return
			}
			after = &value
		}
		matching := make([]event, 0)
		for _, stored := range f.Events {
			if stored.Tenant != tenant || stored.Project != projectID {
				continue
			}
			e := stored.event
			if after != nil {
				if seededBug {
					a, _ := timestamp(e.CreatedAt)
					b, _ := timestamp(after.CreatedAt)
					if !a.Before(b) {
						continue
					}
				} else if compare(e, *after) <= 0 {
					continue
				}
			}
			matching = append(matching, e)
		}
		sort.Slice(matching, func(i, j int) bool { return compare(matching[i], matching[j]) < 0 })
		result := page{Items: matching}
		if len(matching) > limit {
			result.Items = matching[:limit]
			value := encodeCursor(result.Items[limit-1], tenant, projectID, f.SigningKey)
			result.NextCursor = &value
		}
		send(200, result)
	})
}

type runningAPI struct {
	BaseURL string
	server  *http.Server
	done    chan error
}

func startAPI(f fixtures, seededBug bool) (*runningAPI, error) {
	listener, err := net.Listen("tcp4", "127.0.0.1:0")
	if err != nil {
		return nil, err
	}
	server := &http.Server{
		Handler:           createAPI(f, seededBug),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       10 * time.Second,
	}
	api := &runningAPI{BaseURL: "http://" + listener.Addr().String(), server: server, done: make(chan error, 1)}
	go func() { api.done <- server.Serve(listener) }()
	return api, nil
}
func (a *runningAPI) Close() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err := a.server.Shutdown(ctx)
	if err != nil {
		_ = a.server.Close()
	}
	serveErr := <-a.done
	if err != nil {
		return err
	}
	if !errors.Is(serveErr, http.ErrServerClosed) {
		return serveErr
	}
	return nil
}

type observation struct {
	Status int             `json:"status"`
	Body   json.RawMessage `json:"body"`
}

func request(api *runningAPI, projectID, query, token string, detail bool) (observation, error) {
	path := "/v1/projects/" + url.PathEscape(projectID)
	if !detail {
		path += "/events"
	}
	req, err := http.NewRequest("GET", api.BaseURL+path+"?"+query, nil)
	if err != nil {
		return observation{}, err
	}
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	// Fixture requests never follow redirects or use a process-configured proxy.
	transport := &http.Transport{Proxy: nil}
	defer transport.CloseIdleConnections()
	client := http.Client{Timeout: 5 * time.Second, Transport: transport, CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }}
	response, err := client.Do(req)
	if err != nil {
		return observation{}, err
	}
	defer response.Body.Close()
	if response.Header.Get("Content-Type") != "application/json" {
		return observation{}, errors.New("non-JSON response")
	}
	data, err := io.ReadAll(io.LimitReader(response.Body, 1<<20))
	if err != nil {
		return observation{}, err
	}
	if !json.Valid(data) {
		return observation{}, errors.New("invalid JSON response")
	}
	return observation{response.StatusCode, data}, nil
}
func ids(p page) []string {
	result := make([]string, 0, len(p.Items))
	for _, e := range p.Items {
		result = append(result, e.ID)
	}
	return result
}
func showAPI() error {
	f := createFixtures()
	api, err := startAPI(f, false)
	if err != nil {
		return err
	}
	result, requestErr := request(api, "feed", "limit=2", f.TokenA, false)
	closeErr := api.Close()
	if requestErr != nil {
		return requestErr
	}
	if closeErr != nil {
		return closeErr
	}
	var p page
	if err := json.Unmarshal(result.Body, &p); err != nil {
		return err
	}
	return printJSON(map[string]any{"status": result.Status, "ids": ids(p), "has_next_page": p.NextCursor != nil})
}
```

```java
package com.openai.docs.codexcloud;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLDecoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/** A synthetic application HTTP API, not a Codex or OpenAI service client. */
public final class CodexCloudApi implements AutoCloseable {
  public static final ObjectMapper JSON =
      new ObjectMapper()
          .enable(JsonParser.Feature.STRICT_DUPLICATE_DETECTION)
          .enable(DeserializationFeature.FAIL_ON_TRAILING_TOKENS);
  private static final Base64.Encoder ENCODER = Base64.getUrlEncoder().withoutPadding();
  private static final Base64.Decoder DECODER = Base64.getUrlDecoder();
  private final CodexCloudFixtures.Fixtures fixtures;
  private final boolean seededBug;
  private final HttpServer server;
  private final ExecutorService executor = Executors.newFixedThreadPool(4);

  public record Key(String createdAt, String id) {}

  public record Result(int status, Object body) {}

  public static Instant timestamp(String value) {
    if (value == null
        || !value.matches("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,9})?Z")) {
      throw new IllegalArgumentException("Invalid timestamp");
    }
    Instant parsed = Instant.parse(value);
    // Instant permits 24:00 and leap-second normalization; the fixture contract does not.
    if (!parsed.toString().substring(0, 19).equals(value.substring(0, 19))) {
      throw new IllegalArgumentException("Invalid timestamp");
    }
    return parsed;
  }

  public static final Comparator<Key> ORDER =
      Comparator.comparing((Key key) -> timestamp(key.createdAt()))
          .reversed()
          .thenComparing(Key::id, Comparator.reverseOrder());

  public static String signPayload(byte[] payload, byte[] signingKey) throws Exception {
    String encoded = ENCODER.encodeToString(payload);
    Mac mac = Mac.getInstance("HmacSHA256");
    mac.init(new SecretKeySpec(signingKey, "HmacSHA256"));
    return encoded
        + "."
        + ENCODER.encodeToString(mac.doFinal(encoded.getBytes(StandardCharsets.US_ASCII)));
  }

  public static String encodeCursor(Key key, String tenant, String project, byte[] signingKey)
      throws Exception {
    return signPayload(
        JSON.writeValueAsBytes(
            Map.of(
                "version",
                1,
                "tenant_id",
                tenant,
                "project_id",
                project,
                "created_at",
                key.createdAt(),
                "id",
                key.id())),
        signingKey);
  }

  public static Key decodeCursor(String token, String tenant, String project, byte[] signingKey)
      throws Exception {
    if (token == null || token.length() > 2048)
      throw new IllegalArgumentException("Invalid cursor");
    String[] parts = token.split("\\.", -1);
    if (parts.length != 2
        || !parts[0].matches("[A-Za-z0-9_-]+")
        || !parts[1].matches("[A-Za-z0-9_-]+"))
      throw new IllegalArgumentException("Invalid cursor");
    byte[] decoded = DECODER.decode(parts[0]);
    byte[] signature = DECODER.decode(parts[1]);
    String expected = signPayload(decoded, signingKey).split("\\.")[1];
    if (!ENCODER.encodeToString(decoded).equals(parts[0])
        || !ENCODER.encodeToString(signature).equals(parts[1])
        || !MessageDigest.isEqual(signature, DECODER.decode(expected))) {
      throw new IllegalArgumentException("Invalid cursor");
    }
    JsonNode node = JSON.readTree(decoded);
    Set<String> fields = Set.of("version", "tenant_id", "project_id", "created_at", "id");
    if (node == null || !node.isObject() || node.size() != fields.size()) {
      throw new IllegalArgumentException("Invalid cursor");
    }
    for (String field : fields)
      if (!node.has(field)) throw new IllegalArgumentException("Invalid cursor");
    if (!node.get("version").isIntegralNumber()
        || !node.get("version").canConvertToInt()
        || node.get("version").intValue() != 1
        || !node.get("tenant_id").isTextual()
        || !node.get("tenant_id").textValue().equals(tenant)
        || !node.get("project_id").isTextual()
        || !node.get("project_id").textValue().equals(project)
        || !node.get("id").isTextual()
        || node.get("id").textValue().isEmpty()
        || !node.get("created_at").isTextual())
      throw new IllegalArgumentException("Invalid cursor");
    timestamp(node.get("created_at").textValue());
    return new Key(node.get("created_at").textValue(), node.get("id").textValue());
  }

  private static Result error(String code) {
    int status;
    String message;
    switch (code) {
      case "invalid_cursor" -> {
        status = 400;
        message = "Invalid cursor.";
      }
      case "invalid_limit" -> {
        status = 400;
        message = "Limit must be an integer from 1 through 100.";
      }
      case "unauthenticated" -> {
        status = 401;
        message = "Authentication required.";
      }
      case "not_found" -> {
        status = 404;
        message = "Project not found.";
      }
      default -> throw new IllegalArgumentException("Unknown error code");
    }
    return new Result(status, Map.of("error", Map.of("code", code, "message", message)));
  }

  private static Map<String, List<String>> parameters(String raw) {
    Map<String, List<String>> values = new LinkedHashMap<>();
    if (raw != null && !raw.isEmpty()) {
      for (String part : raw.split("&", -1)) {
        String[] pair = part.split("=", 2);
        String name = URLDecoder.decode(pair[0], StandardCharsets.UTF_8);
        String value = URLDecoder.decode(pair.length == 2 ? pair[1] : "", StandardCharsets.UTF_8);
        values.computeIfAbsent(name, ignored -> new ArrayList<>()).add(value);
      }
    }
    return values;
  }

  /** Authenticate and authorize before interpreting pagination input. */
  public Result respond(String method, URI uri, String authorization) throws Exception {
    String tenant =
        authorization != null && authorization.matches("Bearer [A-Za-z0-9_-]+")
            ? fixtures.sessions().get(authorization.substring(7))
            : null;
    if (tenant == null) return error("unauthenticated");
    String[] route = uri.getRawPath().split("/", -1);
    if (!method.equals("GET")
        || (route.length != 4 && route.length != 5)
        || !route[1].equals("v1")
        || !route[2].equals("projects")
        || (route.length == 5 && !route[4].equals("events"))) return error("not_found");
    String project;
    try {
      // URLDecoder treats '+' as space; a path component must preserve literal '+'.
      project = URLDecoder.decode(route[3].replace("+", "%2B"), StandardCharsets.UTF_8);
    } catch (IllegalArgumentException invalid) {
      return error("not_found");
    }
    CodexCloudFixtures.Project owner = fixtures.projects().get(project);
    if (owner == null || !owner.tenantId().equals(tenant)) return error("not_found");
    if (route.length == 4) return new Result(200, Map.of("id", project, "name", owner.name()));

    Map<String, List<String>> query;
    try {
      query = parameters(uri.getRawQuery());
    } catch (IllegalArgumentException invalid) {
      return error("invalid_cursor");
    }
    List<String> limits = query.getOrDefault("limit", List.of("25"));
    int limit;
    try {
      if (limits.size() != 1 || !limits.get(0).matches("[0-9]+")) return error("invalid_limit");
      limit = Integer.parseInt(limits.get(0));
      if (limit < 1 || limit > 100) return error("invalid_limit");
    } catch (NumberFormatException invalid) {
      return error("invalid_limit");
    }
    Key cursor = null;
    if (query.containsKey("cursor")) {
      try {
        if (query.get("cursor").size() != 1) return error("invalid_cursor");
        cursor = decodeCursor(query.get("cursor").get(0), tenant, project, fixtures.signingKey());
      } catch (Exception invalid) {
        return error("invalid_cursor");
      }
    }
    List<CodexCloudFixtures.Event> matching = new ArrayList<>();
    for (CodexCloudFixtures.Event event : fixtures.events()) {
      if (!event.tenantId().equals(tenant) || !event.projectId().equals(project)) continue;
      Key key = new Key(event.createdAt(), event.id());
      if (cursor == null
          || (seededBug
              ? timestamp(key.createdAt()).isBefore(timestamp(cursor.createdAt()))
              : ORDER.compare(key, cursor) > 0)) matching.add(event);
    }
    matching.sort(
        (left, right) ->
            ORDER.compare(
                new Key(left.createdAt(), left.id()), new Key(right.createdAt(), right.id())));
    List<CodexCloudFixtures.Event> selected = matching.subList(0, Math.min(limit, matching.size()));
    String next = null;
    if (matching.size() > limit) {
      CodexCloudFixtures.Event last = selected.get(selected.size() - 1);
      next =
          encodeCursor(
              new Key(last.createdAt(), last.id()), tenant, project, fixtures.signingKey());
    }
    Map<String, Object> page = new LinkedHashMap<>();
    page.put("items", selected.stream().map(CodexCloudFixtures.Event::publicFields).toList());
    page.put("next_cursor", next);
    return new Result(200, page);
  }

  public CodexCloudApi(CodexCloudFixtures.Fixtures fixtures, boolean seededBug) throws IOException {
    this.fixtures = fixtures;
    this.seededBug = seededBug;
    server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
    server.setExecutor(executor);
    server.createContext("/", this::handle);
    server.start();
  }

  public String baseUrl() {
    return "http://127.0.0.1:" + server.getAddress().getPort();
  }

  @Override
  public void close() {
    server.stop(0);
    executor.shutdownNow();
  }

  private void handle(HttpExchange exchange) throws IOException {
    try {
      Result result;
      try {
        result =
            respond(
                exchange.getRequestMethod(),
                exchange.getRequestURI(),
                exchange.getRequestHeaders().getFirst("Authorization"));
      } catch (Exception failure) {
        failure.printStackTrace(System.err);
        result =
            new Result(
                500,
                Map.of(
                    "error",
                    Map.of("code", "internal_error", "message", "Internal server error.")));
      }
      byte[] bytes = JSON.writeValueAsBytes(result.body());
      exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
      exchange.sendResponseHeaders(result.status(), bytes.length);
      exchange.getResponseBody().write(bytes);
    } finally {
      exchange.close();
    }
  }

  public static void main(String[] args) throws Exception {
    CodexCloudFixtures.Fixtures fixtures = CodexCloudFixtures.create();
    try (CodexCloudApi api = new CodexCloudApi(fixtures, false)) {
      HttpClient client =
          HttpClient.newBuilder().connectTimeout(java.time.Duration.ofSeconds(5)).build();
      HttpResponse<String> response =
          client.send(
              HttpRequest.newBuilder(URI.create(api.baseUrl() + "/v1/projects/feed/events?limit=2"))
                  .timeout(java.time.Duration.ofSeconds(5))
                  .header("Authorization", "Bearer " + fixtures.tokenA())
                  .build(),
              HttpResponse.BodyHandlers.ofString());
      JsonNode body = JSON.readTree(response.body());
      List<String> ids = new ArrayList<>();
      body.path("items").forEach(item -> ids.add(item.path("id").asText()));
      if (response.statusCode() != 200) throw new IllegalStateException(response.body());
      System.out.println(
          JSON.writeValueAsString(
              Map.of(
                  "status",
                  response.statusCode(),
                  "ids",
                  ids,
                  "has_next_page",
                  !body.path("next_cursor").isNull())));
    }
  }
}
```

```ruby
require "base64"
require "json"
require "net/http"
require "openssl"
require "time"
require "timeout"
require "uri"
require "webrick"
require_relative "../fixtures/main"

module PaginationAPI
  ERRORS = {
    "invalid_cursor" => [400, "Invalid cursor."],
    "invalid_limit" => [400, "Limit must be an integer from 1 through 100."],
    "unauthenticated" => [401, "Authentication required."],
    "not_found" => [404, "Project not found."]
  }.freeze

  def self.timestamp(value)
    match = value.is_a?(String) && value.match(/\A(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z\z/)
    raise ArgumentError, "Invalid timestamp" unless match

    parsed = Time.iso8601(value)
    raise ArgumentError, "Invalid timestamp" unless parsed.utc.strftime("%Y-%m-%dT%H:%M:%S") == match[1]

    (parsed.to_r * 1_000_000_000).to_i
  end

  def self.compare(left, right)
    [timestamp(right.fetch("created_at")), right.fetch("id")] <=> [timestamp(left.fetch("created_at")), left.fetch("id")]
  end

  def self.encode_cursor(event, tenant, project, key)
    payload = Base64.urlsafe_encode64(
      JSON.generate(
        version: 1, tenant_id: tenant, project_id: project,
        created_at: event.fetch("created_at"), id: event.fetch("id")
      ), padding: false
    )
    signature = Base64.urlsafe_encode64(OpenSSL::HMAC.digest("SHA256", key, payload), padding: false)
    "#{payload}.#{signature}"
  end

  def self.decode_cursor(token, tenant, project, key)
    raise ArgumentError, "Invalid cursor" unless token.is_a?(String) && token.bytesize <= 2048

    parts = token.split(".", -1)
    raise ArgumentError, "Invalid cursor" unless parts.length == 2 && parts.all? { |part| part.match?(/\A[A-Za-z0-9_-]+\z/) }

    payload, signature = parts
    decoded, actual = Base64.urlsafe_decode64(payload), Base64.urlsafe_decode64(signature)
    expected = OpenSSL::HMAC.digest("SHA256", key, payload)
    unless Base64.urlsafe_encode64(decoded, padding: false) == payload && Base64.urlsafe_encode64(actual, padding: false) == signature &&
           actual.bytesize == expected.bytesize && OpenSSL.fixed_length_secure_compare(actual, expected)
      raise ArgumentError, "Invalid cursor"
    end

    cursor = JSON.parse(decoded, allow_duplicate_key: false)
    fields = %w[version tenant_id project_id created_at id]
    unless cursor.is_a?(Hash) && cursor.keys.sort == fields.sort && cursor["version"].is_a?(Integer) && cursor["version"] == 1 &&
           cursor["tenant_id"] == tenant && cursor["project_id"] == project && cursor["id"].is_a?(String) && !cursor["id"].empty?
      raise ArgumentError, "Invalid cursor"
    end

    timestamp(cursor["created_at"])
    cursor
  end

  def self.failure(code)
    status, message = ERRORS.fetch(code)
    [
      status, {
        error: {
          code: code,
          message: message
        }
      }
    ]
  end

  def self.handle(request, fixtures, seeded_bug)
    bearer = request["authorization"].to_s.match(/\ABearer ([A-Za-z0-9_-]+)\z/)
    tenant = bearer && fixtures[:sessions][bearer[1]]
    return failure("unauthenticated") unless tenant

    begin
      url = URI.parse(request.unparsed_uri)
      route = url.path.to_s.match(%r{\A/v1/projects/([^/]+)(/events)?\z})
      project_id = route && URI.decode_www_form_component(route[1])
    rescue ArgumentError, URI::InvalidURIError
      return failure("not_found")
    end
    project = project_id && fixtures[:projects][project_id]
    return failure("not_found") unless request.request_method == "GET" && route && project && project["tenant_id"] == tenant
    unless route[2]
      return [
        200, {
          id: project_id,
          name: project["name"]
        }
      ]
    end

    begin
      parameters = URI.decode_www_form(url.query.to_s)
    rescue ArgumentError
      return failure("invalid_cursor")
    end
    limits = parameters.filter_map { |key, value| value if key == "limit" }
    return failure("invalid_limit") if limits.length > 1 || (!limits.empty? && !limits.fetch(0).match?(/\A\d+\z/))

    limit = limits.empty? ? 25 : limits.fetch(0).to_i
    return failure("invalid_limit") unless (1..100).cover?(limit)

    cursors = parameters.filter_map { |key, value| value if key == "cursor" }
    cursor = nil
    unless cursors.empty?
      begin
        raise ArgumentError, "Repeated cursor" unless cursors.length == 1

        cursor = decode_cursor(cursors.first, tenant, project_id, fixtures[:signing_key])
      rescue ArgumentError, JSON::ParserError
        return failure("invalid_cursor")
      end
    end
    matching = fixtures[:events].select { |event| event["tenant_id"] == tenant && event["project_id"] == project_id }
                                .sort { |left, right| compare(left, right) }.select do |event|
      !cursor || (seeded_bug ? timestamp(event["created_at"]) < timestamp(cursor["created_at"]) : compare(event, cursor).positive?)
    end
    selected = matching.take(limit)
    items = selected.map { |event| event.slice("id", "created_at", "type", "summary") }
    next_cursor = (matching.length > limit) ? encode_cursor(selected.last, tenant, project_id, fixtures[:signing_key]) : nil
    [
      200, {
        items: items,
        next_cursor: next_cursor
      }
    ]
  end

  def self.start(fixtures, seeded_bug: false)
    ready = Queue.new
    server = WEBrick::HTTPServer.new(
      Port: 0, BindAddress: "127.0.0.1", AccessLog: [],
      Logger: WEBrick::Log.new(File::NULL), StartCallback: -> { ready << true }
    )
    server.mount_proc("/") do |request, response|
      status, body = handle(request, fixtures, seeded_bug)
      response.status = status
      response["content-type"] = "application/json"
      response.body = JSON.generate(body)
    end
    worker = Thread.new { server.start }
    Timeout.timeout(5) { ready.pop }
    {
      url: "http://127.0.0.1:#{server.config[:Port]}",

      close: -> {
        server.shutdown
        worker.join
      }
    }
  # Always close the owned listener if startup is interrupted.
  rescue Exception # standard:disable Lint/RescueException
    server&.shutdown
    worker&.join
    raise
  end

  def self.fetch(base, path, token)
    request = Net::HTTP::Get.new(URI("#{base}#{path}"))
    request["Authorization"] = "Bearer #{token}" if token
    response = Net::HTTP.start(request.uri.host, request.uri.port, open_timeout: 5, read_timeout: 5) { |http| http.request(request) }
    [response.code.to_i, JSON.parse(response.body)]
  end
end

if $PROGRAM_NAME == __FILE__
  fixtures = PaginationFixtures.create
  api = PaginationAPI.start(fixtures)
  begin
    status, body = PaginationAPI.fetch(api[:url], "/v1/projects/feed/events?limit=2", fixtures[:token_a])
    puts JSON.generate(status: status, ids: body.fetch("items").map { |item| item.fetch("id") }, has_next_page: !body["next_cursor"].nil?)
  ensure
    api[:close].call
  end
end
```

</details>

<details>
<summary>Seeded records and project access fixtures</summary>
Create test fixtures

```typescript
export function createFixtures() {
  const tokenA = randomBytes(24).toString("base64url");
  const tokenB = randomBytes(24).toString("base64url");
  const sessions = new Map([
    [tokenA, "tenant_a"],
    [tokenB, "tenant_b"],
  ]);
  const projects = new Map([
    ["feed", { tenant_id: "tenant_a", name: "Activity feed" }],
    ["empty", { tenant_id: "tenant_a", name: "Empty feed" }],
    ["exact", { tenant_id: "tenant_a", name: "Four events" }],
    ["large", { tenant_id: "tenant_a", name: "Large feed" }],
    ["precision", { tenant_id: "tenant_a", name: "Precise timestamps" }],
    ["other", { tenant_id: "tenant_a", name: "Another project" }],
    ["private", { tenant_id: "tenant_b", name: "Private project" }],
  ]);
  const event = (
    id: string,
    created_at: string,
    project_id: string,
    tenant_id = "tenant_a"
  ) => ({
    id,
    created_at,
    project_id,
    tenant_id,
    type: "deployment",
    summary: `Synthetic event ${id}`,
    internal_note: "This field must never enter the HTTP response.",
    raw_payload: { synthetic: true },
  });
  const feed = [
    event("evt_105", "2026-01-15T12:00:03.123456Z", "feed"),
    event("evt_104", "2026-01-15T12:00:02.123456Z", "feed"),
    event("evt_103", "2026-01-15T12:00:02.123456Z", "feed"),
    event("evt_102", "2026-01-15T12:00:02.123456Z", "feed"),
    event("evt_101", "2026-01-15T12:00:01.123456Z", "feed"),
  ];
  const events = [
    ...feed,
    ...feed.slice(0, 4).map((item) => ({ ...item, project_id: "exact" })),
    ...Array.from({ length: 105 }, (_, index) =>
      event(
        `large_${String(index).padStart(3, "0")}`,
        new Date(Date.UTC(2026, 0, 15, 12, 0, index))
          .toISOString()
          .replace(".000Z", ".123456Z"),
        "large"
      )
    ),
    // Reverse ID order makes timestamp precision observable in the tests.
    event("precise_a", "2026-01-15T12:00:00.123999Z", "precision"),
    event("precise_z", "2026-01-15T12:00:00.123001Z", "precision"),
    event("other_1", "2026-01-15T12:00:00.123456Z", "other"),
    event("other_2", "2026-01-15T11:59:59.123456Z", "other"),
    event("private_1", "2026-01-15T12:00:00.123456Z", "private", "tenant_b"),
    event("private_2", "2026-01-15T11:59:59.123456Z", "private", "tenant_b"),
  ];
  return {
    sessions,
    projects,
    events,
    signingKey: randomBytes(32),
    tokenA,
    tokenB,
  };
}
```

```go
type event struct {
	ID        string `json:"id"`
	CreatedAt string `json:"created_at"`
	Type      string `json:"type"`
	Summary   string `json:"summary"`
}
type storedEvent struct {
	event
	Tenant, Project, InternalNote string
	RawPayload                    map[string]bool
}
type project struct{ Tenant, Name string }
type fixtures struct {
	Sessions       map[string]string
	Projects       map[string]project
	Events         []storedEvent
	SigningKey     []byte
	TokenA, TokenB string
}

func randomToken(size int) string {
	data := make([]byte, size)
	if _, err := rand.Read(data); err != nil {
		panic(err)
	}
	return base64.RawURLEncoding.EncodeToString(data)
}

func createFixtures() fixtures {
	a, b := randomToken(24), randomToken(24)
	f := fixtures{
		Sessions: map[string]string{a: "tenant_a", b: "tenant_b"},
		Projects: map[string]project{
			"feed":      {"tenant_a", "Activity feed"},
			"empty":     {"tenant_a", "Empty feed"},
			"exact":     {"tenant_a", "Four events"},
			"large":     {"tenant_a", "Large feed"},
			"precision": {"tenant_a", "Precise timestamps"},
			"other":     {"tenant_a", "Another project"},
			"private":   {"tenant_b", "Private project"},
		},
		TokenA:     a,
		TokenB:     b,
		SigningKey: []byte(randomToken(32)),
	}
	add := func(id, stamp, projectID, tenant string) {
		f.Events = append(f.Events, storedEvent{event: event{id, stamp, "deployment", "Synthetic event " + id},
			Tenant: tenant, Project: projectID, InternalNote: "This field must never enter the HTTP response.", RawPayload: map[string]bool{"synthetic": true}})
	}
	stamps := []string{"03", "02", "02", "02", "01"}
	for i, seconds := range stamps {
		id := fmt.Sprintf("evt_%d", 105-i)
		stamp := "2026-01-15T12:00:" + seconds + ".123456Z"
		add(id, stamp, "feed", "tenant_a")
		if i < 4 {
			add(id, stamp, "exact", "tenant_a")
		}
	}
	start := time.Date(2026, 1, 15, 12, 0, 0, 123456000, time.UTC)
	for i := 0; i < 105; i++ {
		add(fmt.Sprintf("large_%03d", i), start.Add(time.Duration(i)*time.Second).Format(time.RFC3339Nano), "large", "tenant_a")
	}
	add("precise_a", "2026-01-15T12:00:00.123999Z", "precision", "tenant_a")
	add("precise_z", "2026-01-15T12:00:00.123001Z", "precision", "tenant_a")
	for _, p := range []string{"other", "private"} {
		tenant := "tenant_a"
		if p == "private" {
			tenant = "tenant_b"
		}
		add(p+"_1", "2026-01-15T12:00:00.123456Z", p, tenant)
		add(p+"_2", "2026-01-15T11:59:59.123456Z", p, tenant)
	}
	return f
}
```

```java
package com.openai.docs.codexcloud;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.security.SecureRandom;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeFormatterBuilder;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Map;

/** Owned synthetic fixtures. Every construction generates fresh session and cursor secrets. */
public final class CodexCloudFixtures {
  public record Project(String tenantId, String name) {}

  public record Event(
      String id,
      String createdAt,
      String projectId,
      String tenantId,
      String type,
      String summary,
      String internalNote,
      Map<String, Object> rawPayload) {
    public Map<String, String> publicFields() {
      return Map.of("id", id, "created_at", createdAt, "type", type, "summary", summary);
    }
  }

  public record Fixtures(
      Map<String, String> sessions,
      Map<String, Project> projects,
      List<Event> events,
      byte[] signingKey,
      String tokenA,
      String tokenB) {
    public Fixtures {
      sessions = Map.copyOf(sessions);
      projects = Map.copyOf(projects);
      events = List.copyOf(events);
      signingKey = signingKey.clone();
    }

    @Override
    public byte[] signingKey() {
      return signingKey.clone();
    }
  }

  private static final SecureRandom RANDOM = new SecureRandom();

  private static byte[] randomBytes(int length) {
    byte[] bytes = new byte[length];
    RANDOM.nextBytes(bytes);
    return bytes;
  }

  private static String token() {
    return Base64.getUrlEncoder().withoutPadding().encodeToString(randomBytes(24));
  }

  private static Event event(String id, String time, String project, String tenant) {
    return new Event(
        id,
        time,
        project,
        tenant,
        "deployment",
        "Synthetic event " + id,
        "This field must never enter the HTTP response.",
        Map.of("synthetic", true));
  }

  public static Fixtures create() {
    String tokenA = token();
    String tokenB = token();
    Map<String, Project> projects =
        Map.of(
            "feed", new Project("tenant_a", "Activity feed"),
            "empty", new Project("tenant_a", "Empty feed"),
            "exact", new Project("tenant_a", "Four events"),
            "large", new Project("tenant_a", "Large feed"),
            "precision", new Project("tenant_a", "Precise timestamps"),
            "other", new Project("tenant_a", "Another project"),
            "private", new Project("tenant_b", "Private project"));
    List<Event> events = new ArrayList<>();
    String[] times = {"03", "02", "02", "02", "01"};
    for (int index = 0; index < times.length; index++) {
      Event item =
          event(
              "evt_" + (105 - index),
              "2026-01-15T12:00:" + times[index] + ".123456Z",
              "feed",
              "tenant_a");
      events.add(item);
      if (index < 4) {
        events.add(event(item.id(), item.createdAt(), "exact", "tenant_a"));
      }
    }
    DateTimeFormatter microseconds = new DateTimeFormatterBuilder().appendInstant(6).toFormatter();
    for (int index = 0; index < 105; index++) {
      events.add(
          event(
              String.format(java.util.Locale.ROOT, "large_%03d", index),
              microseconds.format(Instant.parse("2026-01-15T12:00:00.123456Z").plusSeconds(index)),
              "large",
              "tenant_a"));
    }
    events.add(event("precise_a", "2026-01-15T12:00:00.123999Z", "precision", "tenant_a"));
    events.add(event("precise_z", "2026-01-15T12:00:00.123001Z", "precision", "tenant_a"));
    for (String project : List.of("other", "private")) {
      String tenant = project.equals("private") ? "tenant_b" : "tenant_a";
      events.add(event(project + "_1", "2026-01-15T12:00:00.123456Z", project, tenant));
      events.add(event(project + "_2", "2026-01-15T11:59:59.123456Z", project, tenant));
    }
    return new Fixtures(
        Map.of(tokenA, "tenant_a", tokenB, "tenant_b"),
        projects,
        events,
        randomBytes(32),
        tokenA,
        tokenB);
  }

  public static void main(String[] args) throws Exception {
    Fixtures fixtures = create();
    System.out.println(
        new ObjectMapper()
            .writeValueAsString(
                Map.of(
                    "projects", fixtures.projects().size(), "events", fixtures.events().size())));
  }
}
```

```ruby
require "json"
require "securerandom"
require "time"

module PaginationFixtures
  def self.event(id, created_at, project_id, tenant_id = "tenant_a")
    {
      "id" => id,

      "created_at" => created_at,

      "project_id" => project_id,
      "tenant_id" => tenant_id,

      "type" => "deployment",

      "summary" => "Synthetic event #{id}",
      "internal_note" => "This field must never enter the HTTP response.",

      "raw_payload" => { "synthetic" => true }
    }
  end

  def self.create
    token_a, token_b = SecureRandom.urlsafe_base64(24), SecureRandom.urlsafe_base64(24)
    projects = {
      "feed" => "Activity feed",

      "empty" => "Empty feed",

      "exact" => "Four events",
      "large" => "Large feed",

      "precision" => "Precise timestamps",

      "other" => "Another project",
      "private" => "Private project"
    }.to_h do |id, name|
      [
        id, {
          "tenant_id" => (id == "private") ? "tenant_b" : "tenant_a",
          "name" => name
        }
      ]
    end
    feed = [["evt_105", "03"], ["evt_104", "02"], ["evt_103", "02"], ["evt_102", "02"], ["evt_101", "01"]].map do |id, second|
      event(id, "2026-01-15T12:00:#{second}.123456Z", "feed")
    end
    events = feed + feed.take(4).map { |item| item.merge("project_id" => "exact") }
    105.times do |index|
      events << event(format("large_%03d", index), (Time.utc(2026, 1, 15, 12) + index).strftime("%Y-%m-%dT%H:%M:%S.123456Z"), "large")
    end
    events.concat(
      [
        event("precise_a", "2026-01-15T12:00:00.123999Z", "precision"),
        event("precise_z", "2026-01-15T12:00:00.123001Z", "precision"),
        event("other_1", "2026-01-15T12:00:00.123456Z", "other"),
        event("other_2", "2026-01-15T11:59:59.123456Z", "other"),
        event("private_1", "2026-01-15T12:00:00.123456Z", "private", "tenant_b"),
        event("private_2", "2026-01-15T11:59:59.123456Z", "private", "tenant_b")
      ]
    )
    {
      sessions: {
        token_a => "tenant_a",
        token_b => "tenant_b"
      },

      projects: projects,
      events: events,

      signing_key: SecureRandom.random_bytes(32),

      token_a: token_a,

      token_b: token_b
    }
  end
end

if $PROGRAM_NAME == __FILE__
  fixtures = PaginationFixtures.create
  puts JSON.generate(projects: fixtures[:projects].length, events: fixtures[:events].length)
end
```

</details>

<details>
<summary>HTTP contract and regression tests</summary>
Test the example API

```typescript
test("five-event traversal crosses a timestamp tie and replays the same continuation", async () => {
  const expected = ["evt_105", "evt_104", "evt_103", "evt_102", "evt_101"];
  const pages = await traverse("feed", 2, expected);
  assert.deepEqual(pages.map(ids), [
    ["evt_105", "evt_104"],
    ["evt_103", "evt_102"],
    ["evt_101"],
  ]);
  assert.equal(pages.length, 3);
  assert.ok(pages[0].next_cursor);
  assert.ok(pages[1].next_cursor);
  assert.equal(pages[2].next_cursor, null);
  const replay = await request("feed", {
    limit: "2",
    cursor: pages[0].next_cursor,
  });
  assert.deepEqual(replay.body.items, pages[1].items);
  const next = await request("feed", {
    limit: "2",
    cursor: replay.body.next_cursor,
  });
  assert.deepEqual(next.body.items, pages[2].items);
  assert.equal(next.body.next_cursor, null);
  console.log(
    JSON.stringify({
      fixture: "five-event-tie",
      pages: pages.map(ids),
      requests: pages.length,
      replay: ids(replay.body),
    })
  );
});

test("the same tie group traverses correctly with limit three", async () => {
  const pages = await traverse("feed", 3, [
    "evt_105",
    "evt_104",
    "evt_103",
    "evt_102",
    "evt_101",
  ]);
  assert.deepEqual(pages.map(ids), [
    ["evt_105", "evt_104", "evt_103"],
    ["evt_102", "evt_101"],
  ]);
});

test("timestamp ordering and continuation preserve submillisecond precision", async () => {
  const pages = await traverse("precision", 1, ["precise_a", "precise_z"]);
  assert.equal(pages[0].items[0].created_at, "2026-01-15T12:00:00.123999Z");
  assert.equal(pages[1].items[0].created_at, "2026-01-15T12:00:00.123001Z");
});

test("omitted, minimum, and maximum limits return 25, 1, and 100 of 105 events", async () => {
  for (const [parameters, expected] of [
    [{}, 25],
    [{ limit: "1" }, 1],
    [{ limit: "100" }, 100],
  ] as [Record<string, string>, number][]) {
    const result = await request("large", parameters);
    assert.equal(result.status, 200);
    assert.equal(result.body.items.length, expected);
    assert.ok(result.body.next_cursor);
  }
  const pages = await traverse(
    "large",
    100,
    Array.from(
      { length: 105 },
      (_, index) => `large_${String(104 - index).padStart(3, "0")}`
    )
  );
  assert.deepEqual(
    pages.map((page) => page.items.length),
    [100, 5]
  );
});

test("invalid and repeated limits return the documented generic error", async (context) => {
  for (const limit of [
    "0",
    "101",
    "-1",
    "1.5",
    "many",
    "",
    "1e2",
    "Infinity",
  ]) {
    await context.test(`limit ${JSON.stringify(limit)}`, async () => {
      const result = await request("feed", { limit });
      assert.equal(result.status, 400);
      assert.deepEqual(
        result.body,
        expectedError(
          "invalid_limit",
          "Limit must be an integer from 1 through 100."
        )
      );
    });
  }
  const repeated = await request("feed", [
    ["limit", "1"],
    ["limit", "2"],
  ]);
  assert.equal(repeated.status, 400);
});

test("empty, partial, and exactly full final pages have no continuation", async () => {
  assert.deepEqual((await request("empty")).body, {
    items: [],
    next_cursor: null,
  });
  const partial = await traverse("feed", 2, [
    "evt_105",
    "evt_104",
    "evt_103",
    "evt_102",
    "evt_101",
  ]);
  assert.equal(partial.at(-1).items.length, 1);
  const exact = await traverse("exact", 2, [
    "evt_105",
    "evt_104",
    "evt_103",
    "evt_102",
  ]);
  assert.deepEqual(
    exact.map((page) => page.items.length),
    [2, 2]
  );
  assert.equal(exact[1].next_cursor, null);
});

test("authentication precedes malformed and wrong-scope cursor or limit validation", async () => {
  const privateCursor = (
    await request("private", { limit: "1" }, fixtures.tokenB)
  ).body.next_cursor;
  for (const token of [null, "invalid_session"]) {
    for (const parameters of [
      { cursor: "broken" },
      { cursor: privateCursor },
      { limit: "0", cursor: "broken" },
    ] as Record<string, string>[]) {
      const result = await request("feed", parameters, token);
      assert.equal(result.status, 401);
      assert.deepEqual(result.body, unauthenticated);
    }
  }
});

test("inaccessible and nonexistent projects return identical 404 before cursor validation", async () => {
  const ownCursor = (await request("feed", { limit: "1" })).body.next_cursor;
  for (const project of ["private", "missing"]) {
    for (const parameters of [
      {},
      { cursor: "broken" },
      { cursor: ownCursor },
      { limit: "0", cursor: "broken" },
    ] as Record<string, string>[]) {
      const result = await request(project, parameters);
      assert.equal(result.status, 404);
      assert.deepEqual(result.body, notFound);
    }
  }
});

test("a valid cursor from another project in the same tenant is invalid on an authorized feed", async () => {
  const cursor = (await request("other", { limit: "1" })).body.next_cursor;
  assert.ok(cursor);
  const result = await request("feed", { cursor });
  assert.equal(result.status, 400);
  assert.deepEqual(result.body, invalidCursor);
});

test("a valid cursor from another tenant is invalid on an authorized feed", async () => {
  const cursor = (await request("private", { limit: "1" }, fixtures.tokenB))
    .body.next_cursor;
  assert.ok(cursor);
  const result = await request("feed", { cursor });
  assert.equal(result.status, 400);
  assert.deepEqual(result.body, invalidCursor);
});

test("undecodable, empty, tampered, and repeated cursor tokens return the same closed error", async () => {
  const cursor = (await request("feed", { limit: "1" })).body.next_cursor;
  const [payload, signature] = cursor.split(".");
  const tampered = `${payload}.${signature[0] === "A" ? "B" : "A"}${signature.slice(1)}`;
  for (const token of [
    "broken",
    "",
    "%%%.___",
    "a.b.c",
    "x".repeat(2049),
    tampered,
  ]) {
    const result = await request("feed", { cursor: token });
    assert.equal(result.status, 400);
    assert.deepEqual(result.body, invalidCursor);
  }
  const result = await request("feed", [
    ["cursor", cursor],
    ["cursor", cursor],
  ]);
  assert.equal(result.status, 400);
  assert.deepEqual(result.body, invalidCursor);
});

test("signed structurally invalid payloads and unsupported versions are rejected", async (context) => {
  const valid = {
    version: 1,
    tenant_id: "tenant_a",
    project_id: "feed",
    created_at: "2026-01-15T12:00:02.123456Z",
    id: "evt_104",
  };
  const missing: Partial<typeof valid> = { ...valid };
  delete missing.id;
  const cases: [string, unknown][] = [
    ["missing ID", missing],
    ["number ID", { ...valid, id: 104 }],
    ["empty ID", { ...valid, id: "" }],
    ["number timestamp", { ...valid, created_at: 0 }],
    ["invalid date", { ...valid, created_at: "2026-02-30T12:00:00Z" }],
    ["unsupported version", { ...valid, version: 2 }],
    ["extra field", { ...valid, extra: true }],
    ["wrong tenant type", { ...valid, tenant_id: 1 }],
    ["wrong project type", { ...valid, project_id: null }],
    ["null payload", null],
    ["array payload", []],
    ["invalid JSON", "not-json"],
  ];
  for (const [name, payload] of cases) {
    await context.test(name, async () => {
      const result = await request("feed", { cursor: signFixture(payload) });
      assert.equal(result.status, 400);
      assert.deepEqual(result.body, invalidCursor);
    });
  }
});

test("every serialized event omits stored tenant, project, and raw payload fields", async () => {
  const result = await request("feed", { limit: "100" });
  assert.equal(result.status, 200);
  for (const item of result.body.items) {
    assert.deepEqual(Object.keys(item).sort(), [
      "created_at",
      "id",
      "summary",
      "type",
    ]);
  }
  assert.ok(
    fixtures.events.some((event) => event.internal_note && event.raw_payload)
  );
});

test("the schema oracle rejects extra, missing, incorrectly typed, and malformed public fields", () => {
  const schema = specification.components.schemas.EventPage;
  const page = {
    items: [
      {
        id: "evt_1",
        created_at: "2026-01-15T12:00:00.123456Z",
        type: "deployment",
        summary: "Synthetic",
      },
    ],
    next_cursor: null,
  };
  assert.ok(conforms(page, schema));
  assert.equal(conforms({ ...page, tenant_id: "tenant_a" }, schema), false);
  assert.equal(
    conforms(
      { ...page, items: [{ ...page.items[0], raw_payload: {} }] },
      schema
    ),
    false
  );
  assert.equal(conforms({ items: page.items }, schema), false);
  assert.equal(conforms({ ...page, next_cursor: "" }, schema), false);
  assert.equal(
    conforms({ ...page, items: [{ ...page.items[0], id: 1 }] }, schema),
    false
  );
  assert.equal(
    conforms(
      { ...page, items: [{ ...page.items[0], created_at: "yesterday" }] },
      schema
    ),
    false
  );
  const errorSchema = specification.components.schemas.InvalidCursor;
  assert.equal(
    conforms(
      { error: { ...invalidCursor.error, stack: "internal" } },
      errorSchema
    ),
    false
  );
  assert.equal(
    conforms(
      { error: { ...invalidCursor.error, message: "tenant_a" } },
      errorSchema
    ),
    false
  );
});

test("the existing project-detail route preserves access and ignores pagination parameters", async () => {
  const own = await request(
    "feed",
    { cursor: "broken", limit: "0" },
    fixtures.tokenA,
    true
  );
  assert.equal(own.status, 200);
  assert.deepEqual(own.body, { id: "feed", name: "Activity feed" });
  const inaccessible = await request("private", {}, fixtures.tokenA, true);
  assert.equal(inaccessible.status, 404);
  assert.deepEqual(inaccessible.body, notFound);
  const unauthenticatedResult = await request("feed", {}, null, true);
  assert.equal(unauthenticatedResult.status, 401);
  assert.deepEqual(unauthenticatedResult.body, unauthenticated);
});

test("OpenAPI declares operation, limit boundaries, signed cursor, and response statuses", () => {
  assert.equal(specification.openapi, "3.1.0");
  const operation = specification.paths["/v1/projects/{project_id}/events"].get;
  assert.equal(operation.operationId, "listProjectEvents");
  const limit = operation.parameters.find(
    (parameter: { name: string }) => parameter.name === "limit"
  ).schema;
  assert.deepEqual(limit, {
    type: "integer",
    minimum: 1,
    maximum: 100,
    default: 25,
  });
  assert.deepEqual(Object.keys(operation.responses).sort(), [
    "200",
    "400",
    "401",
    "404",
  ]);
  assert.equal(
    specification.components.securitySchemes.session.scheme,
    "bearer"
  );
});
```

```go
// validatePage is a closed response oracle for this sample's public contract.
// It rejects missing fields, extra storage fields, null items and invalid dates.
func validatePage(data []byte) error {
	var object map[string]json.RawMessage
	if json.Unmarshal(data, &object) != nil || len(object) != 2 || object["items"] == nil || object["next_cursor"] == nil {
		return errors.New("invalid page fields")
	}
	var items []map[string]json.RawMessage
	if json.Unmarshal(object["items"], &items) != nil || items == nil {
		return errors.New("invalid items")
	}
	for _, item := range items {
		if len(item) != 4 {
			return errors.New("invalid event fields")
		}
		for _, name := range []string{"id", "created_at", "type", "summary"} {
			var value string
			if item[name] == nil || bytes.Equal(item[name], []byte("null")) || json.Unmarshal(item[name], &value) != nil {
				return errors.New("invalid event field")
			}
			if (name == "id" || name == "type") && value == "" {
				return errors.New("empty ID or event type")
			}
			if name == "created_at" {
				if _, err := timestamp(value); err != nil {
					return err
				}
			}
		}
	}
	if !bytes.Equal(object["next_cursor"], []byte("null")) {
		var value string
		if json.Unmarshal(object["next_cursor"], &value) != nil || value == "" {
			return errors.New("invalid continuation")
		}
	}
	return nil
}

// Canonical shared schema in the public source checkout. The harness copies
// that same file into its owned directory before compiling this program.
const openAPIFile = "../../../typescript-examples/codex-cloud/issue-to-tested-pr/openapi.json"

func validateOpenAPI(data []byte) error {
	var specification struct {
		OpenAPI string `json:"openapi"`
		Paths   map[string]struct {
			Get struct {
				OperationID string `json:"operationId"`
				Parameters  []struct {
					Name   string         `json:"name"`
					Schema map[string]any `json:"schema"`
				} `json:"parameters"`
				Responses map[string]json.RawMessage `json:"responses"`
			} `json:"get"`
		} `json:"paths"`
		Components struct {
			SecuritySchemes map[string]struct {
				Scheme string `json:"scheme"`
			} `json:"securitySchemes"`
			Schemas map[string]struct {
				AdditionalProperties *bool                     `json:"additionalProperties"`
				Required             []string                  `json:"required"`
				Properties           map[string]map[string]any `json:"properties"`
			} `json:"schemas"`
		} `json:"components"`
	}
	if err := json.Unmarshal(data, &specification); err != nil {
		return err
	}
	operation := specification.Paths["/v1/projects/{project_id}/events"].Get
	if specification.OpenAPI != "3.1.0" || operation.OperationID != "listProjectEvents" || specification.Components.SecuritySchemes["session"].Scheme != "bearer" {
		return errors.New("OpenAPI operation or session authentication changed")
	}
	var limit, continuation map[string]any
	for _, parameter := range operation.Parameters {
		if parameter.Name == "limit" {
			limit = parameter.Schema
		}
		if parameter.Name == "cursor" {
			continuation = parameter.Schema
		}
	}
	if !reflect.DeepEqual(limit, map[string]any{"type": "integer", "minimum": float64(1), "maximum": float64(100), "default": float64(25)}) {
		return errors.New("OpenAPI limit contract changed")
	}
	if !reflect.DeepEqual(continuation, map[string]any{"type": "string", "minLength": float64(1), "maxLength": float64(2048)}) {
		return errors.New("OpenAPI cursor bounds changed")
	}
	statuses := []string{}
	for status := range operation.Responses {
		statuses = append(statuses, status)
	}
	sort.Strings(statuses)
	if !reflect.DeepEqual(statuses, []string{"200", "400", "401", "404"}) {
		return errors.New("OpenAPI response statuses changed")
	}
	event := specification.Components.Schemas["Event"]
	required := append([]string(nil), event.Required...)
	sort.Strings(required)
	if event.AdditionalProperties == nil ||
		*event.AdditionalProperties ||
		!reflect.DeepEqual(required, []string{"created_at", "id", "summary", "type"}) ||
		len(event.Properties) != 4 ||
		event.Properties["id"]["minLength"] != float64(1) ||
		event.Properties["type"]["minLength"] != float64(1) {
		return errors.New("OpenAPI public event projection changed")
	}
	return nil
}

func equal(t *testing.T, actual, expected any) {
	t.Helper()
	if !reflect.DeepEqual(actual, expected) {
		t.Fatalf("got %#v; want %#v", actual, expected)
	}
}
func setup(t *testing.T, seeded bool) (fixtures, *runningAPI) {
	t.Helper()
	f := createFixtures()
	api, err := startAPI(f, seeded)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := api.Close(); err != nil {
			t.Error(err)
		}
	})
	return f, api
}
func get(t *testing.T, api *runningAPI, f fixtures, projectID, query, token string, detail bool) observation {
	t.Helper()
	result, err := request(api, projectID, query, token, detail)
	if err != nil {
		t.Fatal(err)
	}
	if result.Status != 200 {
		var actual publicError
		decoder := json.NewDecoder(bytes.NewReader(result.Body))
		decoder.DisallowUnknownFields()
		if err := decoder.Decode(&actual); err != nil {
			t.Fatal(err)
		}
		status, expected := failure(actual.Error.Code)
		if actual.Error.Code != "invalid_cursor" && actual.Error.Code != "invalid_limit" && actual.Error.Code != "not_found" && actual.Error.Code != "unauthenticated" {
			t.Fatal("undocumented error code")
		}
		equal(t, result.Status, status)
		equal(t, actual, expected)
	} else if !detail {
		if err := validatePage(result.Body); err != nil {
			t.Fatal(err)
		}
	}
	return result
}
func getPage(t *testing.T, api *runningAPI, f fixtures, p, q string) page {
	t.Helper()
	result := get(t, api, f, p, q, f.TokenA, false)
	equal(t, result.Status, 200)
	var body page
	if err := json.Unmarshal(result.Body, &body); err != nil {
		t.Fatal(err)
	}
	return body
}
func traverse(t *testing.T, api *runningAPI, f fixtures, p string, limit int, expected []string) []page {
	t.Helper()
	pages := []page{}
	all := []string{}
	query := "limit=" + strconv.Itoa(limit)
	for {
		if len(pages) > len(expected)+1 {
			t.Fatal("unbounded traversal")
		}
		body := getPage(t, api, f, p, query)
		pages = append(pages, body)
		all = append(all, ids(body)...)
		if body.NextCursor == nil {
			break
		}
		query = "limit=" + strconv.Itoa(limit) + "&cursor=" + url.QueryEscape(*body.NextCursor)
	}
	equal(t, all, expected)
	seen := map[string]bool{}
	for _, id := range all {
		if seen[id] {
			t.Fatal("duplicate event")
		}
		seen[id] = true
	}
	return pages
}
func signedFixture(payload any, f fixtures) string {
	data, err := json.Marshal(payload)
	if err != nil {
		panic(err)
	}
	return sign(base64.RawURLEncoding.EncodeToString(data), f.SigningKey)
}

func regressionTests(seeded bool) []testing.InternalTest {
	return []testing.InternalTest{
		{Name: "TestTuplePaginationAndReplay", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			equal(t, len(f.Projects), 7)
			equal(t, len(f.Events), 120)
			pages := traverse(t, api, f, "feed", 2, []string{"evt_105", "evt_104", "evt_103", "evt_102", "evt_101"})
			equal(t, len(pages), 3)
			equal(t, ids(pages[0]), []string{"evt_105", "evt_104"})
			equal(t, ids(pages[1]), []string{"evt_103", "evt_102"})
			equal(t, ids(pages[2]), []string{"evt_101"})
			if pages[0].NextCursor == nil || pages[1].NextCursor == nil || pages[2].NextCursor != nil {
				t.Fatal("incorrect continuation")
			}
			replay := getPage(t, api, f, "feed", "limit=2&cursor="+url.QueryEscape(*pages[0].NextCursor))
			equal(t, replay, pages[1])
			equal(t, getPage(t, api, f, "feed", "limit=2&cursor="+url.QueryEscape(*replay.NextCursor)), pages[2])
		}},
		{Name: "TestTiesWithLimitThree", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			pages := traverse(t, api, f, "feed", 3, []string{"evt_105", "evt_104", "evt_103", "evt_102", "evt_101"})
			equal(t, len(pages), 2)
		}},
		{Name: "TestSubmillisecondPrecision", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			pages := traverse(t, api, f, "precision", 1, []string{"precise_a", "precise_z"})
			equal(t, pages[0].Items[0].CreatedAt, "2026-01-15T12:00:00.123999Z")
			equal(t, pages[1].Items[0].CreatedAt, "2026-01-15T12:00:00.123001Z")
		}},
		{Name: "TestLimitBoundaries", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			for _, test := range []struct {
				query string
				count int
			}{{"", 25}, {"limit=1", 1}, {"limit=100", 100}} {
				p := getPage(t, api, f, "large", test.query)
				equal(t, len(p.Items), test.count)
				if p.NextCursor == nil {
					t.Fatal("missing continuation")
				}
			}
			expected := []string{}
			for i := 104; i >= 0; i-- {
				expected = append(expected, fmt.Sprintf("large_%03d", i))
			}
			pages := traverse(t, api, f, "large", 100, expected)
			equal(t, len(pages[0].Items), 100)
			equal(t, len(pages[1].Items), 5)
		}},
		{Name: "TestInvalidLimits", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			for _, value := range []string{"0", "101", "-1", "1.5", "many", "", "1e2", "Infinity"} {
				r := get(t, api, f, "feed", "limit="+url.QueryEscape(value), f.TokenA, false)
				equal(t, r.Status, 400)
			}
			equal(t, get(t, api, f, "feed", "limit=1&limit=2", f.TokenA, false).Status, 400)
		}},
		{Name: "TestFinalPages", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			p := getPage(t, api, f, "empty", "")
			equal(t, len(p.Items), 0)
			equal(t, p.NextCursor, (*string)(nil))
			pages := traverse(t, api, f, "exact", 2, []string{"evt_105", "evt_104", "evt_103", "evt_102"})
			equal(t, len(pages), 2)
			equal(t, pages[1].NextCursor, (*string)(nil))
		}},
		{Name: "TestAuthenticationPrecedence", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			for _, token := range []string{"", "invalid_session"} {
				for _, q := range []string{"cursor=broken", "limit=0&cursor=broken"} {
					equal(t, get(t, api, f, "feed", q, token, false).Status, 401)
				}
			}
		}},
		{Name: "TestAuthorizationPrecedence", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			own := getPage(t, api, f, "feed", "limit=1")
			for _, p := range []string{"private", "missing"} {
				for _, q := range []string{"", "cursor=broken", "limit=0&cursor=broken", "cursor=" + url.QueryEscape(*own.NextCursor)} {
					equal(t, get(t, api, f, p, q, f.TokenA, false).Status, 404)
				}
			}
		}},
		{Name: "TestProjectCursorScope", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			other := getPage(t, api, f, "other", "limit=1")
			equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(*other.NextCursor), f.TokenA, false).Status, 400)
		}},
		{Name: "TestTenantCursorScope", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			r := get(t, api, f, "private", "limit=1", f.TokenB, false)
			equal(t, r.Status, 200)
			var p page
			if err := json.Unmarshal(r.Body, &p); err != nil {
				t.Fatal(err)
			}
			equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(*p.NextCursor), f.TokenA, false).Status, 400)
			equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(*p.NextCursor), "", false).Status, 401)
		}},
		{Name: "TestMalformedCursors", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			p := getPage(t, api, f, "feed", "limit=1")
			parts := strings.Split(*p.NextCursor, ".")
			first := "A"
			if parts[1][0] == 'A' {
				first = "B"
			}
			tampered := parts[0] + "." + first + parts[1][1:]
			for _, token := range []string{"broken", "", "%%%.___", "a.b.c", strings.Repeat("x", 2049), tampered} {
				equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(token), f.TokenA, false).Status, 400)
			}
			q := "cursor=" + url.QueryEscape(*p.NextCursor)
			equal(t, get(t, api, f, "feed", q+"&"+q, f.TokenA, false).Status, 400)
		}},
		{Name: "TestSignedInvalidCursors", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			valid := map[string]any{"version": 1, "tenant_id": "tenant_a", "project_id": "feed", "created_at": "2026-01-15T12:00:02.123456Z", "id": "evt_104"}
			for _, change := range []struct {
				name  string
				value any
			}{{"id", nil}, {"id", 104}, {"id", ""}, {"created_at", 0}, {"created_at", "2026-02-30T12:00:00Z"}, {"version", 2}, {"extra", true}, {"tenant_id", 1}, {"project_id", nil}} {
				input := map[string]any{}
				for k, v := range valid {
					input[k] = v
				}
				input[change.name] = change.value
				equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(signedFixture(input, f)), f.TokenA, false).Status, 400)
			}
			delete(valid, "id")
			for _, input := range []any{valid, nil, []string{}, "not-json"} {
				equal(t, get(t, api, f, "feed", "cursor="+url.QueryEscape(signedFixture(input, f)), f.TokenA, false).Status, 400)
			}
		}},
		{Name: "TestPublicEventFields", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			r := get(t, api, f, "feed", "limit=100", f.TokenA, false)
			equal(t, r.Status, 200)
			for _, secret := range []string{"tenant_id", "project_id", "internal_note", "raw_payload"} {
				if bytes.Contains(r.Body, []byte(secret)) {
					t.Fatal("private field leaked:", secret)
				}
			}
			if f.Events[0].InternalNote == "" || f.Events[0].RawPayload == nil {
				t.Fatal("missing negative control")
			}
		}},
		{Name: "TestSchemaOracle", F: func(t *testing.T) {
			valid := []byte(`{"items":[{"id":"evt_1","created_at":"2026-01-15T12:00:00.123456Z","type":"deployment","summary":"Synthetic"}],"next_cursor":null}`)
			if err := validatePage(valid); err != nil {
				t.Fatal(err)
			}
			for _, invalid := range []string{
				`{"items":[],"next_cursor":null,"tenant_id":"tenant_a"}`, `{"items":[]}`, `{"items":[],"next_cursor":""}`,
				strings.Replace(string(valid), `"evt_1"`, `1`, 1), strings.Replace(string(valid), `2026-01-15T12:00:00.123456Z`, `yesterday`, 1),
				strings.Replace(string(valid), `"summary":"Synthetic"`, `"summary":"Synthetic","raw_payload":{}`, 1),
				strings.Replace(string(valid), `"type":"deployment"`, `"type":""`, 1),
			} {
				if validatePage([]byte(invalid)) == nil {
					t.Fatal("oracle accepted invalid page", invalid)
				}
			}
		}},
		{Name: "TestProjectDetail", F: func(t *testing.T) {
			f, api := setup(t, seeded)
			r := get(t, api, f, "feed", "cursor=broken&limit=0", f.TokenA, true)
			equal(t, r.Status, 200)
			var body map[string]string
			if err := json.Unmarshal(r.Body, &body); err != nil {
				t.Fatal(err)
			}
			equal(t, body, map[string]string{"id": "feed", "name": "Activity feed"})
			equal(t, get(t, api, f, "private", "", f.TokenA, true).Status, 404)
			equal(t, get(t, api, f, "feed", "", "", true).Status, 401)
		}},
		{Name: "TestOpenAPIContract", F: func(t *testing.T) {
			data, err := os.ReadFile(openAPIFile)
			if err != nil {
				t.Fatal(err)
			}
			if err := validateOpenAPI(data); err != nil {
				t.Fatal(err)
			}
		}},
	}
}

func matchTest(pattern, name string) (bool, error) { return regexp.MatchString(pattern, name) }
func nativeSuite(seeded bool)                      { testing.Main(matchTest, regressionTests(seeded), nil, nil) }
```

```java
package com.openai.docs.codexcloud;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Native behavioral suite. Run with --seeded to expose the timestamp-only defect. */
public final class CodexCloudTest {
  @FunctionalInterface
  public interface Checked {
    void run() throws Exception;
  }

  public record Response(int status, JsonNode body) {}

  public record SuiteResult(int tests, int failures, List<List<String>> pages) {}

  private final CodexCloudFixtures.Fixtures fixtures;
  private final CodexCloudApi api;
  private final HttpClient client =
      HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
  private int assertions;
  private JsonNode specification;

  private CodexCloudTest(CodexCloudFixtures.Fixtures fixtures, CodexCloudApi api) {
    this.fixtures = fixtures;
    this.api = api;
  }

  private void equal(Object actual, Object expected) {
    assertions++;
    if (!Objects.equals(actual, expected)) {
      throw new AssertionError("Expected " + expected + ", got " + actual);
    }
  }

  private void require(boolean condition, String message) {
    assertions++;
    if (!condition) throw new AssertionError(message);
  }

  public static String query(Map<String, String> values) {
    return values.entrySet().stream()
        .map(entry -> encode(entry.getKey()) + "=" + encode(entry.getValue()))
        .collect(java.util.stream.Collectors.joining("&"));
  }

  private static String encode(String value) {
    return URLEncoder.encode(value, StandardCharsets.UTF_8);
  }

  private Response request(String project, String query, String token, boolean detail)
      throws Exception {
    HttpRequest.Builder request =
        HttpRequest.newBuilder(
                URI.create(
                    api.baseUrl()
                        + "/v1/projects/"
                        + project
                        + (detail ? "" : "/events")
                        + "?"
                        + query))
            .timeout(Duration.ofSeconds(5));
    if (token != null) request.header("Authorization", "Bearer " + token);
    HttpResponse<String> response =
        client.send(request.build(), HttpResponse.BodyHandlers.ofString());
    require(
        response.headers().firstValue("content-type").orElse("").startsWith("application/json"),
        "JSON content type");
    JsonNode body = CodexCloudApi.JSON.readTree(response.body());
    require(
        conforms(body, response.statusCode(), detail), "Closed public response schema: " + body);
    JsonNode spec = specification();
    JsonNode operation =
        spec.path("paths")
            .path(detail ? "/v1/projects/{project_id}" : "/v1/projects/{project_id}/events")
            .path("get");
    JsonNode schema =
        operation
            .path("responses")
            .path(Integer.toString(response.statusCode()))
            .path("content")
            .path("application/json")
            .path("schema");
    require(
        !schema.isMissingNode() && schemaConforms(body, schema, spec), "OpenAPI response schema");
    return new Response(response.statusCode(), body);
  }

  private Response request(String project, Map<String, String> query) throws Exception {
    return request(project, query(query), fixtures.tokenA(), false);
  }

  static java.nio.file.Path openApiFile() throws java.nio.file.NoSuchFileException {
    var canonical =
        java.nio.file.Path.of("../typescript-examples/codex-cloud/issue-to-tested-pr/openapi.json");
    if (java.nio.file.Files.isRegularFile(canonical)) return canonical;
    var isolated = java.nio.file.Path.of("codex-cloud/issue-to-tested-pr/openapi.json");
    if (java.nio.file.Files.isRegularFile(isolated)) return isolated;
    throw new java.nio.file.NoSuchFileException(
        canonical.toString(), isolated.toString(), "Missing shared OpenAPI fixture");
  }

  private JsonNode specification() throws Exception {
    if (specification == null) {
      specification = CodexCloudApi.JSON.readTree(java.nio.file.Files.readString(openApiFile()));
    }
    return specification;
  }

  // Only the schema keywords used by the peer's owned OpenAPI fixture are supported.
  private static boolean schemaConforms(JsonNode value, JsonNode schema, JsonNode spec) {
    if (schema.has("$ref")) {
      String reference = schema.path("$ref").asText();
      if (!reference.startsWith("#/"))
        throw new IllegalArgumentException("Only local schema references are supported");
      JsonNode resolved = spec.at(reference.substring(1));
      if (resolved.isMissingNode())
        throw new IllegalArgumentException("Unresolved schema reference");
      return schemaConforms(value, resolved, spec);
    }
    if (schema.has("oneOf")) {
      int matches = 0;
      for (JsonNode choice : schema.path("oneOf"))
        if (schemaConforms(value, choice, spec)) matches++;
      return matches == 1;
    }
    String type = schema.path("type").asText();
    switch (type) {
      case "null":
        if (!value.isNull()) return false;
        break;
      case "array":
        if (!value.isArray()) return false;
        for (JsonNode item : value)
          if (!schemaConforms(item, schema.path("items"), spec)) return false;
        break;
      case "object":
        if (!value.isObject()) return false;
        for (JsonNode key : schema.path("required")) if (!value.has(key.asText())) return false;
        if (schema.path("additionalProperties").isBoolean()
            && !schema.path("additionalProperties").asBoolean()) {
          for (String key : fields(value)) if (!schema.path("properties").has(key)) return false;
        }
        for (String key : fields(schema.path("properties"))) {
          if (value.has(key)
              && !schemaConforms(value.get(key), schema.path("properties").get(key), spec))
            return false;
        }
        break;
      case "string":
        if (!value.isTextual()) return false;
        String text = value.textValue();
        if (schema.has("minLength")
            && text.codePointCount(0, text.length()) < schema.path("minLength").asInt())
          return false;
        if (schema.has("pattern")
            && !java.util.regex.Pattern.compile(schema.path("pattern").asText())
                .matcher(text)
                .find()) return false;
        if (schema.path("format").asText().equals("date-time")) {
          try {
            java.time.OffsetDateTime.parse(text);
          } catch (RuntimeException invalid) {
            return false;
          }
        }
        break;
      case "":
        break;
      default:
        throw new IllegalArgumentException("Unsupported fixture schema type: " + type);
    }
    if (schema.has("enum")) {
      for (JsonNode choice : schema.path("enum")) if (choice.equals(value)) return true;
      return false;
    }
    return true;
  }

  private static Set<String> fields(JsonNode object) {
    Set<String> keys = new HashSet<>();
    object.fieldNames().forEachRemaining(keys::add);
    return keys;
  }

  /** Closed schema oracle for this application's public responses, not a general validator. */
  public static boolean conforms(JsonNode body, int status, boolean detail) {
    if (body == null || !body.isObject()) return false;
    if (status != 200) {
      if (!fields(body).equals(Set.of("error"))) return false;
      JsonNode error = body.path("error");
      if (!error.isObject() || !fields(error).equals(Set.of("code", "message"))) return false;
      Map<String, String> messages =
          Map.of(
              "invalid_cursor",
              "Invalid cursor.",
              "invalid_limit",
              "Limit must be an integer from 1 through 100.",
              "unauthenticated",
              "Authentication required.",
              "not_found",
              "Project not found.");
      Map<String, Integer> statuses =
          Map.of(
              "invalid_cursor",
              400,
              "invalid_limit",
              400,
              "unauthenticated",
              401,
              "not_found",
              404);
      String code = error.path("code").asText();
      return error.path("code").isTextual()
          && error.path("message").isTextual()
          && Objects.equals(statuses.get(code), status)
          && Objects.equals(messages.get(code), error.path("message").textValue());
    }
    if (detail)
      return fields(body).equals(Set.of("id", "name"))
          && body.path("id").isTextual()
          && !body.path("id").textValue().isEmpty()
          && body.path("name").isTextual();
    if (!fields(body).equals(Set.of("items", "next_cursor")) || !body.path("items").isArray())
      return false;
    JsonNode cursor = body.path("next_cursor");
    if (!cursor.isNull()
        && (!cursor.isTextual() || !cursor.textValue().matches("[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+")))
      return false;
    for (JsonNode item : body.path("items")) {
      if (!item.isObject() || !fields(item).equals(Set.of("id", "created_at", "type", "summary")))
        return false;
      for (String key : List.of("id", "created_at", "type", "summary")) {
        if (!item.path(key).isTextual() || item.path(key).textValue().isEmpty()) return false;
      }
      try {
        CodexCloudApi.timestamp(item.path("created_at").textValue());
      } catch (RuntimeException invalid) {
        return false;
      }
    }
    return true;
  }

  public static List<String> ids(JsonNode page) {
    List<String> ids = new ArrayList<>();
    page.path("items").forEach(item -> ids.add(item.path("id").asText()));
    return ids;
  }

  private List<JsonNode> traverse(String project, int limit, List<String> expected)
      throws Exception {
    List<JsonNode> pages = new ArrayList<>();
    List<String> observed = new ArrayList<>();
    String cursor = null;
    do {
      require(
          pages.size() < Math.max(1, (expected.size() + limit - 1) / limit), "Bounded traversal");
      Map<String, String> query = new LinkedHashMap<>();
      query.put("limit", Integer.toString(limit));
      if (cursor != null) query.put("cursor", cursor);
      Response result = request(project, query);
      equal(result.status(), 200);
      pages.add(result.body());
      observed.addAll(ids(result.body()));
      cursor =
          result.body().path("next_cursor").isNull()
              ? null
              : result.body().path("next_cursor").asText();
    } while (cursor != null);
    equal(observed, expected);
    equal(new HashSet<>(observed).size(), expected.size());
    return pages;
  }

  private void error(Response response, int status, String code, String message) {
    equal(response.status(), status);
    equal(
        response.body(),
        CodexCloudApi.JSON.valueToTree(Map.of("error", Map.of("code", code, "message", message))));
  }

  private void invalidCursor(String cursor) throws Exception {
    error(request("feed", Map.of("cursor", cursor)), 400, "invalid_cursor", "Invalid cursor.");
  }

  public static SuiteResult runSuite(boolean seeded) throws Exception {
    CodexCloudFixtures.Fixtures fixtures = CodexCloudFixtures.create();
    try (CodexCloudApi api = new CodexCloudApi(fixtures, seeded)) {
      CodexCloudTest suite = new CodexCloudTest(fixtures, api);
      return suite.run();
    }
  }

  private SuiteResult run() throws Exception {
    List<String> expected = List.of("evt_105", "evt_104", "evt_103", "evt_102", "evt_101");
    Map<String, Checked> tests = new LinkedHashMap<>();
    List<List<String>> observedPages = new ArrayList<>();
    tests.put(
        "five-event traversal crosses a timestamp tie and replays the same continuation",
        () -> {
          List<JsonNode> pages = traverse("feed", 2, expected);
          for (JsonNode page : pages) observedPages.add(ids(page));
          equal(pages.size(), 3);
          Response replay =
              request(
                  "feed",
                  Map.of("limit", "2", "cursor", pages.get(0).path("next_cursor").asText()));
          equal(replay.body(), pages.get(1));
          Response last =
              request(
                  "feed",
                  Map.of("limit", "2", "cursor", replay.body().path("next_cursor").asText()));
          equal(last.body(), pages.get(2));
          System.out.println(
              CodexCloudApi.JSON.writeValueAsString(
                  Map.of(
                      "fixture",
                      "five-event-tie",
                      "pages",
                      observedPages,
                      "requests",
                      pages.size(),
                      "replay",
                      ids(replay.body()))));
        });
    tests.put(
        "the same tie group traverses correctly with limit three",
        () -> {
          List<JsonNode> pages = traverse("feed", 3, expected);
          equal(
              pages.stream().map(CodexCloudTest::ids).toList(),
              List.of(expected.subList(0, 3), expected.subList(3, 5)));
        });
    tests.put(
        "timestamp ordering and continuation preserve submillisecond precision",
        () -> {
          List<JsonNode> pages = traverse("precision", 1, List.of("precise_a", "precise_z"));
          equal(
              pages.get(0).path("items").get(0).path("created_at").asText(),
              "2026-01-15T12:00:00.123999Z");
          equal(
              pages.get(1).path("items").get(0).path("created_at").asText(),
              "2026-01-15T12:00:00.123001Z");
        });
    tests.put(
        "omitted, minimum, and maximum limits return 25, 1, and 100 of 105 events",
        () -> {
          for (int limit : List.of(25, 1, 100)) {
            Response page = request("large", limit == 25 ? Map.of() : Map.of("limit", "" + limit));
            equal(page.body().path("items").size(), limit);
            require(page.body().path("next_cursor").isTextual(), "Continuation");
          }
          List<String> large = new ArrayList<>();
          for (int index = 104; index >= 0; index--)
            large.add(String.format(java.util.Locale.ROOT, "large_%03d", index));
          equal(
              traverse("large", 100, large).stream()
                  .map(page -> page.path("items").size())
                  .toList(),
              List.of(100, 5));
        });
    tests.put(
        "invalid and repeated limits return the documented generic error",
        () -> {
          for (String limit :
              List.of(
                  "0",
                  "101",
                  "-1",
                  "1.5",
                  "many",
                  "",
                  "1e2",
                  "Infinity",
                  "999999999999999999999")) {
            error(
                request("feed", Map.of("limit", limit)),
                400,
                "invalid_limit",
                "Limit must be an integer from 1 through 100.");
          }
          error(
              request("feed", "limit=1&limit=2", fixtures.tokenA(), false),
              400,
              "invalid_limit",
              "Limit must be an integer from 1 through 100.");
        });
    tests.put(
        "empty, partial, and exactly full final pages have no continuation",
        () -> {
          equal(ids(request("empty", Map.of()).body()), List.of());
          require(request("empty", Map.of()).body().path("next_cursor").isNull(), "Empty terminal");
          equal(traverse("feed", 2, expected).get(2).path("items").size(), 1);
          List<JsonNode> pages = traverse("exact", 2, expected.subList(0, 4));
          equal(pages.stream().map(page -> page.path("items").size()).toList(), List.of(2, 2));
          require(pages.get(1).path("next_cursor").isNull(), "Exact terminal");
        });
    tests.put(
        "authentication precedes malformed and wrong-scope cursor or limit validation",
        () -> {
          String privateCursor =
              request("private", "limit=1", fixtures.tokenB(), false)
                  .body()
                  .path("next_cursor")
                  .asText();
          for (String token : new String[] {null, "invalid_session"}) {
            for (String query :
                List.of("cursor=broken", "limit=0&cursor=broken", "cursor=" + privateCursor)) {
              error(
                  request("feed", query, token, false),
                  401,
                  "unauthenticated",
                  "Authentication required.");
            }
          }
        });
    tests.put(
        "inaccessible and nonexistent projects return identical 404 before cursor validation",
        () -> {
          String cursor = request("feed", Map.of("limit", "1")).body().path("next_cursor").asText();
          for (String project : List.of("private", "missing")) {
            for (String query :
                List.of("", "cursor=broken", "limit=0&cursor=broken", "cursor=" + cursor)) {
              error(
                  request(project, query, fixtures.tokenA(), false),
                  404,
                  "not_found",
                  "Project not found.");
            }
          }
        });
    tests.put(
        "a valid cursor from another project is invalid on an authorized feed",
        () ->
            invalidCursor(
                request("other", Map.of("limit", "1")).body().path("next_cursor").asText()));
    tests.put(
        "a valid cursor from another tenant is invalid on an authorized feed",
        () ->
            invalidCursor(
                request("private", "limit=1", fixtures.tokenB(), false)
                    .body()
                    .path("next_cursor")
                    .asText()));
    tests.put(
        "undecodable, empty, tampered, and repeated cursor tokens return the same closed error",
        () -> {
          String cursor = request("feed", Map.of("limit", "1")).body().path("next_cursor").asText();
          String[] parts = cursor.split("\\.");
          String tampered =
              parts[0] + "." + (parts[1].startsWith("A") ? "B" : "A") + parts[1].substring(1);
          for (String value :
              List.of("broken", "", "%%%.___", "a.b.c", "x".repeat(2049), tampered, cursor + "="))
            invalidCursor(value);
          error(
              request("feed", "cursor=" + cursor + "&cursor=" + cursor, fixtures.tokenA(), false),
              400,
              "invalid_cursor",
              "Invalid cursor.");
        });
    tests.put(
        "signed structurally invalid payloads and unsupported versions are rejected",
        () -> {
          ObjectNode valid =
              CodexCloudApi.JSON.valueToTree(
                  Map.of(
                      "version",
                      1,
                      "tenant_id",
                      "tenant_a",
                      "project_id",
                      "feed",
                      "created_at",
                      "2026-01-15T12:00:02.123456Z",
                      "id",
                      "evt_104"));
          List<JsonNode> bad = new ArrayList<>();
          ObjectNode missing = valid.deepCopy();
          missing.remove("id");
          bad.add(missing);
          bad.add(valid.deepCopy().put("id", 104));
          bad.add(valid.deepCopy().put("id", ""));
          bad.add(valid.deepCopy().put("created_at", 0));
          bad.add(valid.deepCopy().put("created_at", "2026-02-30T12:00:00Z"));
          bad.add(valid.deepCopy().put("created_at", "2026-01-15T24:00:00Z"));
          bad.add(valid.deepCopy().put("version", 2));
          bad.add(valid.deepCopy().put("version", 1.0));
          bad.add(valid.deepCopy().put("extra", true));
          bad.add(valid.deepCopy().put("tenant_id", 1));
          bad.add(valid.deepCopy().putNull("project_id"));
          bad.add(CodexCloudApi.JSON.getNodeFactory().nullNode());
          bad.add(CodexCloudApi.JSON.createArrayNode());
          for (JsonNode value : bad)
            invalidCursor(
                CodexCloudApi.signPayload(
                    CodexCloudApi.JSON.writeValueAsBytes(value), fixtures.signingKey()));
          for (String value : List.of("not-json", valid + " {}", "{\"version\":1,\"version\":1}")) {
            invalidCursor(
                CodexCloudApi.signPayload(
                    value.getBytes(StandardCharsets.UTF_8), fixtures.signingKey()));
          }
        });
    tests.put(
        "every serialized event omits stored tenant, project, and raw payload fields",
        () -> {
          for (JsonNode item : request("feed", Map.of("limit", "100")).body().path("items")) {
            equal(fields(item), Set.of("id", "created_at", "type", "summary"));
          }
          require(
              fixtures.events().stream()
                  .allMatch(
                      event -> !event.internalNote().isEmpty() && !event.rawPayload().isEmpty()),
              "Sensitive fixture fields exist");
        });
    tests.put(
        "the schema oracle rejects extra, missing, incorrectly typed, and malformed public fields",
        () -> {
          ObjectNode page = (ObjectNode) request("feed", Map.of("limit", "1")).body();
          require(!conforms(page.deepCopy().put("extra", true), 200, false), "Extra field");
          ObjectNode missing = page.deepCopy();
          missing.remove("items");
          require(!conforms(missing, 200, false), "Missing field");
          require(!conforms(page.deepCopy().put("items", "bad"), 200, false), "Wrong type");
          require(
              !conforms(page.deepCopy().put("next_cursor", "broken"), 200, false),
              "Invalid cursor schema");
          ObjectNode time = page.deepCopy();
          ((ObjectNode) time.path("items").get(0)).put("created_at", "bad");
          require(!conforms(time, 200, false), "Invalid timestamp schema");
          require(
              !conforms(
                  CodexCloudApi.JSON.valueToTree(
                      Map.of("error", Map.of("code", "invalid_cursor", "message", "tenant_a"))),
                  400,
                  false),
              "Generic error only");
        });
    tests.put(
        "the existing project-detail route preserves access and ignores pagination parameters",
        () -> {
          Response detail = request("feed", "limit=0&cursor=broken", fixtures.tokenA(), true);
          equal(detail.status(), 200);
          equal(
              detail.body(),
              CodexCloudApi.JSON.valueToTree(Map.of("id", "feed", "name", "Activity feed")));
          error(
              request("private", "", fixtures.tokenA(), true),
              404,
              "not_found",
              "Project not found.");
          error(
              request("feed", "", null, true), 401, "unauthenticated", "Authentication required.");
        });
    tests.put(
        "OpenAPI declares operation, limit boundaries, signed cursor, and response statuses",
        () -> {
          // Authoritative shared OpenAPI fixture for this local application.
          JsonNode specification =
              CodexCloudApi.JSON.readTree(java.nio.file.Files.readString(openApiFile()));
          equal(specification.path("openapi").asText(), "3.1.0");
          JsonNode operation =
              specification.path("paths").path("/v1/projects/{project_id}/events").path("get");
          equal(operation.path("operationId").asText(), "listProjectEvents");
          JsonNode limit = null;
          for (JsonNode parameter : operation.path("parameters"))
            if (parameter.path("name").asText().equals("limit")) limit = parameter.path("schema");
          equal(
              limit,
              CodexCloudApi.JSON.valueToTree(
                  Map.of("type", "integer", "minimum", 1, "maximum", 100, "default", 25)));
          equal(fields(operation.path("responses")), Set.of("200", "400", "401", "404"));
          equal(
              specification
                  .path("components")
                  .path("securitySchemes")
                  .path("session")
                  .path("scheme")
                  .asText(),
              "bearer");
        });
    int failures = 0;
    int index = 0;
    for (Map.Entry<String, Checked> test : tests.entrySet()) {
      index++;
      try {
        test.getValue().run();
        System.out.println("ok " + index + " - " + test.getKey());
      } catch (Exception | AssertionError failure) {
        failures++;
        System.out.println("not ok " + index + " - " + test.getKey());
        failure.printStackTrace(System.err);
      }
    }
    System.out.printf(
        "# tests %d%n# assertions %d%n# fail %d%n# cancelled 0%n# skipped 0%n# todo 0%n",
        tests.size(), assertions, failures);
    return new SuiteResult(tests.size(), failures, observedPages);
  }

  public static void main(String[] args) throws Exception {
    boolean seeded = List.of(args).contains("--seeded");
    if (runSuite(seeded).failures() != 0) System.exit(1);
  }
}
```

```ruby
require "minitest/autorun"
require_relative "api/main"

SEEDED_PAGINATION_BUG = !!ARGV.delete("--seeded")
ARGV << "--verbose"

class PaginationTest < Minitest::Test
  def setup
    @fixtures = PaginationFixtures.create
    @spec = JSON.parse(File.read(File.expand_path("support/openapi.json", __dir__)))
    @api = PaginationAPI.start(@fixtures, seeded_bug: SEEDED_PAGINATION_BUG)
  end

  def teardown
    @api&.fetch(:close)&.call
  end

  # This oracle implements only the keywords in this fixture's closed schemas.
  def conforms?(value, schema)
    if schema["$ref"]
      resolved = schema["$ref"].delete_prefix("#/").split("/").reduce(@spec) { |item, key| item.fetch(key) }
      return conforms?(value, resolved)
    end
    return schema["oneOf"].count { |choice| conforms?(value, choice) } == 1 if schema["oneOf"]

    case schema["type"]
    when "null"
      return value.nil?
    when "array"
      return value.is_a?(Array) && value.all? { |item| conforms?(item, schema.fetch("items", {})) }
    when "object"
      return false unless value.is_a?(Hash)

      properties = schema.fetch("properties", {})
      return false unless schema.fetch("required", []).all? { |key| value.key?(key) }
      return false if schema["additionalProperties"] == false && (value.keys - properties.keys).any?

      return properties.all? { |key, child| !value.key?(key) || conforms?(value[key], child) }
    when "string"
      return false unless value.is_a?(String)
      return false if value.length < schema.fetch("minLength", 0)
      return false if schema["pattern"] && !Regexp.new(schema["pattern"]).match?(value)

      if schema["format"] == "date-time"
        begin
          Time.iso8601(value)
        rescue ArgumentError
          return false
        end
      end
    end
    !schema["enum"] || schema["enum"].include?(value)
  end

  def request(project = "feed", parameters = {}, token: @fixtures[:token_a], detail: false)
    path = "/v1/projects/#{project}#{"/events" unless detail}?#{URI.encode_www_form(parameters)}"
    status, body = PaginationAPI.fetch(@api[:url], path, token)
    route = detail ? "/v1/projects/{project_id}" : "/v1/projects/{project_id}/events"
    schema = @spec.fetch("paths").fetch(route).fetch("get").fetch("responses").fetch(status.to_s).fetch("content").fetch("application/json").fetch("schema")
    assert conforms?(body, schema), "HTTP #{status} must match its closed public schema"
    [status, body]
  end

  def ids(body)
    body.fetch("items").map { |item| item.fetch("id") }
  end

  def page(project = "feed", parameters = {})
    status, body = request(project, parameters)
    assert_equal 200, status
    body
  end

  def error(code, project = "feed", parameters = {}, token: @fixtures[:token_a], detail: false, **query)
    parameters = parameters.merge(query) unless query.empty?
    status, body = request(project, parameters, token: token, detail: detail)
    expected_status, expected_body = PaginationAPI.failure(code)
    assert_equal expected_status, status
    assert_equal JSON.parse(JSON.generate(expected_body)), body
    body
  end

  def test_tuple_pagination_and_replay
    first = page("feed", limit: 2)
    assert_equal %w[evt_105 evt_104], ids(first)
    second = page("feed", limit: 2, cursor: first.fetch("next_cursor"))
    assert_equal %w[evt_103 evt_102], ids(second)
    assert_equal second, page("feed", limit: 2, cursor: first.fetch("next_cursor"))
    third = page("feed", limit: 2, cursor: second.fetch("next_cursor"))
    assert_equal ["evt_101"], ids(third)
    assert_nil third["next_cursor"]
  end

  def test_ties_with_limit_three
    first = page("feed", limit: 3)
    assert_equal %w[evt_105 evt_104 evt_103], ids(first)
    last = page("feed", limit: 3, cursor: first.fetch("next_cursor"))
    assert_equal %w[evt_102 evt_101], ids(last)
    assert_nil last["next_cursor"]
  end

  def test_submillisecond_precision
    first = page("precision", limit: 1)
    assert_equal ["precise_a"], ids(first)
    assert_equal ["precise_z"], ids(page("precision", limit: 1, cursor: first.fetch("next_cursor")))
  end

  def test_limit_boundaries
    assert_equal 25, ids(page("large")).length
    assert_equal 1, ids(page("large", limit: 1)).length
    assert_equal 100, ids(page("large", limit: 100)).length
  end

  def test_invalid_limits
    ["", "0", "101", "-1", "1.5", "1e2", " 2", "NaN", "Infinity"].each do |limit|
      error("invalid_limit", "feed", limit: limit)
    end
    error("invalid_limit", "feed", [["limit", "2"], ["limit", "3"]])
  end

  def test_final_pages
    assert_empty ids(page("empty"))
    assert_nil page("empty")["next_cursor"]
    assert_nil page("feed", limit: 100)["next_cursor"]
    first = page("exact", limit: 2)
    last = page("exact", limit: 2, cursor: first.fetch("next_cursor"))
    assert_equal 2, ids(last).length
    assert_nil last["next_cursor"]
  end

  def test_authentication_precedence
    [nil, "wrong", "invalid token"].each do |token|
      error(
        "unauthenticated", "feed", {
          cursor: "broken",
          limit: "0"
        }, token: token
      )
    end
  end

  def test_authorization_precedence
    private_error = error("not_found", "private", cursor: "broken", limit: "0")
    assert_equal private_error, error("not_found", "missing", cursor: "broken", limit: "0")
  end

  def test_project_cursor_scope
    cursor = page("other", limit: 1).fetch("next_cursor")
    error("invalid_cursor", "feed", cursor: cursor)
  end

  def test_tenant_cursor_scope
    _, body = request("private", { limit: 1 }, token: @fixtures[:token_b])
    error("invalid_cursor", "feed", cursor: body.fetch("next_cursor"))
  end

  def test_malformed_cursors
    cursor = page("feed", limit: 2).fetch("next_cursor")
    ["", "broken", "a.b.c", cursor + "=", "!" + cursor, cursor.sub(/.$/, cursor.end_with?("A") ? "B" : "A")].each do |token|
      error("invalid_cursor", "feed", cursor: token)
    end
    error("invalid_cursor", "feed", [["cursor", cursor], ["cursor", cursor]])
  end

  def test_signed_invalid_cursors
    valid = {
      "version" => 1,
      "tenant_id" => "tenant_a",
      "project_id" => "feed",
      "created_at" => "2026-01-15T12:00:02.123456Z",
      "id" => "evt_104"
    }
    [
      valid.merge("version" => 2), valid.merge("version" => 1.0), valid.merge("extra" => true), valid.except("id"),
      valid.merge("id" => ""), valid.merge("id" => 5), valid.merge("created_at" => "2026-02-30T00:00:00Z"), nil, []
    ].each do |value|
      payload = Base64.urlsafe_encode64(JSON.generate(value), padding: false)
      signature = Base64.urlsafe_encode64(OpenSSL::HMAC.digest("SHA256", @fixtures[:signing_key], payload), padding: false)
      error("invalid_cursor", "feed", cursor: "#{payload}.#{signature}")
    end
  end

  def test_public_event_fields
    page("large", limit: 100).fetch("items").each do |event|
      assert_equal %w[created_at id summary type], event.keys.sort
    end
  end

  def test_schema_oracle
    schema = @spec.fetch("components").fetch("schemas").fetch("Event")
    valid = page.fetch("items").first
    assert conforms?(valid, schema)
    [valid.merge("tenant_id" => "secret"), valid.except("id"), valid.merge("id" => 1), valid.merge("created_at" => "bad-date")].each do |event|
      refute conforms?(event, schema)
    end
  end

  def test_project_detail
    status, body = request(
      "feed", {
        cursor: "broken",
        limit: "0"
      }, detail: true
    )
    assert_equal 200, status
    assert_equal(
      {
        "id" => "feed",
        "name" => "Activity feed"
      }, body
    )
    error("not_found", "private", {}, detail: true)
    error("unauthenticated", "feed", {}, token: nil, detail: true)
  end

  def test_openapi_contract
    assert_equal "3.1.0", @spec["openapi"]
    operation = @spec.fetch("paths").fetch("/v1/projects/{project_id}/events").fetch("get")
    assert_equal "listProjectEvents", operation["operationId"]
    limit = operation.fetch("parameters").find { |parameter| parameter["name"] == "limit" }.fetch("schema")
    assert_equal(
      {
        "type" => "integer",
        "minimum" => 1,
        "maximum" => 100,
        "default" => 25
      }, limit
    )
    assert_equal %w[200 400 401 404], operation.fetch("responses").keys.sort
    assert_equal "bearer", @spec.dig("components", "securitySchemes", "session", "scheme")
  end
end
```

</details>

<details>
<summary>Evidence capture</summary>
Reproduce the issue

```typescript
mkdirSync(output, { recursive: true });
const states = [];
for (const [name, arguments_] of [
  ["red", ["--seeded"]],
  ["green", []],
]) {
  const result = spawnSync(
    process.execPath,
    [
      "--experimental-strip-types",
      resolve(directory, "test.ts"),
      ...arguments_,
    ],
    {
      cwd: directory,
      encoding: "utf8",
      timeout: 30_000,
    }
  );
  writeFileSync(
    resolve(output, `${name}.log`),
    `${result.stdout ?? ""}${result.stderr ?? ""}`
  );
  states.push({
    name,
    command: `node --experimental-strip-types test.ts${arguments_.length ? " --seeded" : ""}`,
    exit_code: result.status,
    signal: result.signal,
    error: result.error?.message ?? null,
  });
}
const sources = Object.fromEntries(
  readdirSync(directory, { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => [
      entry.name,
      createHash("sha256")
        .update(readFileSync(resolve(directory, entry.name)))
        .digest("hex"),
    ])
);
const observed = { red: await observe(true), green: await observe(false) };
writeJson("observed-http.json", observed);
writeJson("run-manifest.json", {
  execution: "Synthetic loopback HTTP fixture; no external service",
  recorded_at: new Date().toISOString(),
  node: process.version,
  minimum_node: "22.6.0",
  dependencies: "Node standard library only; no install step",
  baseline:
    "Deliberately seeded timestamp-only continuation; not a historical customer defect",
  correction:
    "Descending timestamp-and-ID tuple continuation using full fractional precision",
  source_sha256: sources,
  states,
});
if (
  states[0].exit_code === null ||
  states[0].exit_code === 0 ||
  states[1].exit_code !== 0
) {
  throw new Error(
    "Expected the unchanged tests to fail on the seeded baseline and pass on the corrected implementation. Inspect red.log and green.log."
  );
}
console.log(
  JSON.stringify(
    {
      execution: "synthetic-loopback-http",
      red_exit: states[0].exit_code,
      green_exit: states[1].exit_code,
      green_pages: observed.green.pages.map((page) =>
        page.body.items.map((item: { id: string }) => item.id)
      ),
      evidence_directory: output,
    },
    null,
    2
  )
);
```

```go
func observe(seeded bool) (map[string]any, error) {
	f := createFixtures()
	api, err := startAPI(f, seeded)
	if err != nil {
		return nil, err
	}
	pages := []observation{}
	problems := []observation{}
	query := "limit=2"
	observeErr := func() error {
		for {
			if len(pages) >= 3 {
				return errors.New("traversal exceeded fixture request bound")
			}
			result, err := request(api, "feed", query, f.TokenA, false)
			if err != nil {
				return err
			}
			if result.Status != 200 {
				return fmt.Errorf("unexpected page status %d", result.Status)
			}
			pages = append(pages, result)
			var p page
			if err := json.Unmarshal(result.Body, &p); err != nil {
				return err
			}
			if p.NextCursor == nil {
				break
			}
			query = "limit=2&cursor=" + url.QueryEscape(*p.NextCursor)
		}
		for _, input := range []struct{ project, token string }{{"feed", f.TokenA}, {"feed", ""}, {"private", f.TokenA}} {
			result, err := request(api, input.project, "cursor=broken", input.token, false)
			if err != nil {
				return err
			}
			problems = append(problems, result)
		}
		return nil
	}()
	closeErr := api.Close()
	if observeErr != nil {
		return nil, observeErr
	}
	if closeErr != nil {
		return nil, closeErr
	}
	return map[string]any{"pages": pages, "errors": problems}, nil
}
func writeJSON(path string, value any) error {
	data, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(path, append(data, '\n'), 0600)
}

func reproduce(output string) error {
	if err := os.Mkdir(output, 0700); err != nil {
		return fmt.Errorf("create new owned evidence directory: %w", err)
	}
	executable, err := os.Executable()
	if err != nil {
		return err
	}
	states := []map[string]any{}
	exits := []int{}
	for _, mode := range []struct {
		name string
		args []string
	}{{"red", []string{"--seeded", "-test.v", "test"}}, {"green", []string{"-test.v", "test"}}} {
		ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		command := exec.CommandContext(ctx, executable, mode.args...)
		log, runErr := command.CombinedOutput()
		cancel()
		exit := 0
		if runErr != nil {
			var exitErr *exec.ExitError
			if !errors.As(runErr, &exitErr) {
				return runErr
			}
			exit = exitErr.ExitCode()
			if exit < 0 {
				return fmt.Errorf("%s interrupted: %w", mode.name, runErr)
			}
		}
		if err := os.WriteFile(filepath.Join(output, mode.name+".log"), log, 0600); err != nil {
			return err
		}
		states = append(states, map[string]any{"name": mode.name, "command": append([]string{executable}, mode.args...), "exit_code": exit})
		exits = append(exits, exit)
	}
	red, err := observe(true)
	if err != nil {
		return err
	}
	green, err := observe(false)
	if err != nil {
		return err
	}
	if err := writeJSON(filepath.Join(output, "observed-http.json"), map[string]any{"red": red, "green": green}); err != nil {
		return err
	}
	_, sourcePath, _, ok := runtime.Caller(0)
	if !ok {
		return errors.New("source location unavailable")
	}
	source, err := os.ReadFile(sourcePath)
	if err != nil {
		return err
	}
	digest := sha256.Sum256(source)
	if err := writeJSON(filepath.Join(output, "run-manifest.json"), map[string]any{
		"execution": "Synthetic loopback HTTP fixture; no external service", "recorded_at": time.Now().UTC().Format(time.RFC3339Nano),
		"go": runtime.Version(), "dependencies": "Go standard library only", "source_sha256": map[string]string{"main.go": fmt.Sprintf("%x", digest)},
		"baseline":   "Deliberately seeded timestamp-only continuation; not a historical customer defect",
		"correction": "Descending timestamp-and-ID tuple continuation using full fractional precision", "states": states,
	}); err != nil {
		return err
	}
	if exits[0] != 1 || exits[1] != 0 {
		return fmt.Errorf("expected red exit 1 and green exit 0; got %v", exits)
	}
	pages := [][]string{}
	for _, result := range green["pages"].([]observation) {
		var p page
		if err := json.Unmarshal(result.Body, &p); err != nil {
			return err
		}
		pages = append(pages, ids(p))
	}
	return printJSON(map[string]any{
		"execution":          "synthetic-loopback-http",
		"red_exit":           exits[0],
		"green_exit":         exits[1],
		"green_pages":        pages,
		"evidence_directory": output,
	})
}
```

```java
package com.openai.docs.codexcloud;

import com.fasterxml.jackson.databind.JsonNode;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/** Run from the Java example project after compilation, with dependencies on the classpath. */
public final class CodexCloudReproduce {
  private static void write(Path output, String name, Object value) throws Exception {
    Files.writeString(
        output.resolve(name),
        CodexCloudApi.JSON.writerWithDefaultPrettyPrinter().writeValueAsString(value) + "\n");
  }

  public static Map<String, Object> observe(boolean seeded) throws Exception {
    CodexCloudFixtures.Fixtures fixtures = CodexCloudFixtures.create();
    HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
    try (CodexCloudApi api = new CodexCloudApi(fixtures, seeded)) {
      List<Map<String, Object>> pages = new ArrayList<>();
      String cursor = null;
      do {
        if (pages.size() >= 3)
          throw new IllegalStateException("Traversal exceeded the fixed-fixture bound");
        Map<String, String> query = new LinkedHashMap<>();
        query.put("limit", "2");
        if (cursor != null) query.put("cursor", cursor);
        HttpResponse<String> response =
            client.send(
                HttpRequest.newBuilder(
                        URI.create(
                            api.baseUrl()
                                + "/v1/projects/feed/events?"
                                + CodexCloudTest.query(query)))
                    .header("Authorization", "Bearer " + fixtures.tokenA())
                    .timeout(Duration.ofSeconds(5))
                    .build(),
                HttpResponse.BodyHandlers.ofString());
        JsonNode body = CodexCloudApi.JSON.readTree(response.body());
        if (response.statusCode() != 200 || !CodexCloudTest.conforms(body, 200, false)) {
          throw new IllegalStateException("Unexpected pagination response: " + response.body());
        }
        pages.add(Map.of("status", response.statusCode(), "body", body));
        cursor = body.path("next_cursor").isNull() ? null : body.path("next_cursor").asText();
      } while (cursor != null);
      List<Map<String, Object>> errors = new ArrayList<>();
      for (int index = 0; index < 3; index++) {
        String project = index == 2 ? "private" : "feed";
        HttpRequest.Builder request =
            HttpRequest.newBuilder(
                    URI.create(api.baseUrl() + "/v1/projects/" + project + "/events?cursor=broken"))
                .timeout(Duration.ofSeconds(5));
        if (index != 1) request.header("Authorization", "Bearer " + fixtures.tokenA());
        HttpResponse<String> response =
            client.send(request.build(), HttpResponse.BodyHandlers.ofString());
        JsonNode body = CodexCloudApi.JSON.readTree(response.body());
        int expectedStatus = List.of(400, 401, 404).get(index);
        if (response.statusCode() != expectedStatus
            || !CodexCloudTest.conforms(body, expectedStatus, false)) {
          throw new IllegalStateException("Unexpected error response: " + response.body());
        }
        errors.add(Map.of("status", response.statusCode(), "body", body));
      }
      return Map.of("pages", pages, "errors", errors);
    }
  }

  public static void main(String[] args) throws Exception {
    if (args.length > 2)
      throw new IllegalArgumentException("Usage: [evidence-directory] [native-source-root]");
    Path output = Path.of(args.length > 0 ? args[0] : "evidence").toAbsolutePath();
    Path sourceRoot = Path.of(args.length > 1 ? args[1] : "src/main/java/codex-cloud");
    Files.createDirectories(output);
    List<Map<String, Object>> states = new ArrayList<>();
    String java = Path.of(System.getProperty("java.home"), "bin", "java").toString();
    for (String name : List.of("red", "green")) {
      List<String> command =
          new ArrayList<>(
              List.of(
                  java,
                  "-cp",
                  System.getProperty("java.class.path"),
                  CodexCloudTest.class.getName()));
      if (name.equals("red")) command.add("--seeded");
      Path log = output.resolve(name + ".log");
      Process process =
          new ProcessBuilder(command)
              .redirectErrorStream(true)
              .redirectOutput(log.toFile())
              .start();
      boolean completed = process.waitFor(30, TimeUnit.SECONDS);
      if (!completed) {
        process.destroyForcibly();
        if (!process.waitFor(5, TimeUnit.SECONDS))
          throw new IllegalStateException("Native suite did not terminate");
      }
      states.add(
          Map.of(
              "name",
              name,
              "command",
              command,
              "exit_code",
              process.exitValue(),
              "timed_out",
              !completed));
    }
    Map<String, String> hashes = new LinkedHashMap<>();
    try (var paths = Files.walk(sourceRoot)) {
      for (Path path : paths.filter(Files::isRegularFile).sorted().toList()) {
        hashes.put(
            sourceRoot.relativize(path).toString(),
            HexFormat.of()
                .formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(path))));
      }
    }
    if (hashes.isEmpty()) throw new IllegalStateException("No authored sources found to hash");
    Path contract = CodexCloudTest.openApiFile();
    hashes.put(
        "runtime/codex-cloud/issue-to-tested-pr/openapi.json",
        HexFormat.of()
            .formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(contract))));
    Map<String, Object> observed = Map.of("red", observe(true), "green", observe(false));
    write(output, "observed-http.json", observed);
    write(
        output,
        "run-manifest.json",
        Map.of(
            "execution",
            "Synthetic loopback HTTP fixture; no external service",
            "recorded_at",
            Instant.now().toString(),
            "java",
            System.getProperty("java.version"),
            "minimum_java",
            "17",
            "dependencies",
            "Jackson databind 2.18.11; Java standard library",
            "baseline",
            "Deliberately seeded timestamp-only continuation; not a historical customer defect",
            "correction",
            "Descending timestamp-and-ID tuple continuation using full fractional precision",
            "source_sha256",
            hashes,
            "states",
            states));
    if (!states.get(0).get("exit_code").equals(1)
        || !states.get(1).get("exit_code").equals(0)
        || states.stream().anyMatch(state -> state.get("timed_out").equals(true))) {
      throw new IllegalStateException(
          "Expected failing baseline and passing correction; inspect red.log and green.log");
    }
    JsonNode green = CodexCloudApi.JSON.valueToTree(observed.get("green"));
    List<List<String>> pages = new ArrayList<>();
    for (JsonNode page : green.path("pages")) pages.add(CodexCloudTest.ids(page.path("body")));
    if (!pages.equals(
        List.of(
            List.of("evt_105", "evt_104"), List.of("evt_103", "evt_102"), List.of("evt_101")))) {
      throw new IllegalStateException("Corrected page traversal did not preserve every fixture ID");
    }
    System.out.println(
        CodexCloudApi.JSON.writeValueAsString(
            Map.of(
                "execution",
                "synthetic-loopback-http",
                "red_exit",
                states.get(0).get("exit_code"),
                "green_exit",
                states.get(1).get("exit_code"),
                "green_pages",
                pages,
                "evidence_directory",
                output.toString())));
  }
}
```

```ruby
require "digest"
require "fileutils"
require "rbconfig"
require "timeout"
require_relative "../api/main"

output = File.expand_path(ARGV.fetch(0, "evidence"))
FileUtils.mkdir_p(output)
test_path = File.expand_path("../test.rb", __dir__)
states = [["red", ["--seeded"]], ["green", []]].map do |name, arguments|
  log_path = File.join(output, "#{name}.log")
  pid = if arguments.empty?
          Process.spawn(RbConfig.ruby, test_path, out: log_path, err: [:child, :out])
        else
          Process.spawn(RbConfig.ruby, test_path, "--seeded", out: log_path, err: [:child, :out])
        end
  begin
    status = Timeout.timeout(30) { (Process.wait2(pid) or raise "Child process was not reaped").last }
  rescue Timeout::Error
    Process.kill("KILL", pid)
    Process.wait(pid)
    raise
  end
  {
    name: name,
    command: [RbConfig.ruby, test_path, *arguments],
    exit_code: status.exitstatus,
    signal: status.termsig
  }
end

observed = [true, false].to_h do |seeded|
  fixtures = PaginationFixtures.create
  api = PaginationAPI.start(fixtures, seeded_bug: seeded)
  begin
    pages = []
    state = { cursor: nil }
    loop do
      raise "Traversal exceeded fixture bound" if pages.length >= 3

      parameters = { limit: 2 }
      parameters[:cursor] = state[:cursor] if state[:cursor]
      status, body = PaginationAPI.fetch(api[:url], "/v1/projects/feed/events?#{URI.encode_www_form(parameters)}", fixtures[:token_a])
      pages << {
        status: status,
        body: body
      }
      state[:cursor] = body.fetch("next_cursor")
      break unless state[:cursor]
    end
    errors = [["feed", fixtures[:token_a]], ["feed", nil], ["private", fixtures[:token_a]]].map do |project, token|
      status, body = PaginationAPI.fetch(api[:url], "/v1/projects/#{project}/events?cursor=broken", token)
      {
        status: status,
        body: body
      }
    end
    [
      seeded ? :red : :green, {
        pages: pages,
        errors: errors
      }
    ]
  ensure
    api[:close].call
  end
end
sources = %w[api/main.rb fixtures/main.rb test.rb reproduce/main.rb support/openapi.json].to_h do |name|
  [name, Digest::SHA256.file(File.expand_path("../#{name}", __dir__)).hexdigest]
end
File.write(File.join(output, "observed-http.json"), JSON.pretty_generate(observed))
File.write(
  File.join(output, "run-manifest.json"),
  JSON.pretty_generate(
    execution: "Synthetic loopback HTTP fixture; no external service", recorded_at: Time.now.utc.iso8601,
    ruby: RUBY_VERSION, source_sha256: sources, states: states,
    baseline: "Deliberately seeded timestamp-only continuation; not a historical customer defect",
    correction: "Descending timestamp-and-ID continuation retaining fractional precision"
  )
)
unless states.fetch(0)[:exit_code] == 1 && states.fetch(1)[:exit_code] == 0
  raise "Expected seeded failure and corrected success; inspect red.log and green.log"
end

puts JSON.generate(
  execution: "synthetic-loopback-http", red_exit: states.fetch(0)[:exit_code], green_exit: states.fetch(1)[:exit_code],
  green_pages: observed.fetch(:green)[:pages].map { |page| page[:body].fetch("items").map { |item| item.fetch("id") } }, evidence_directory: output
)
```

</details>

## Prepare the input packet

An issue link is useful only if Codex can read it. Paste or attach the relevant content when the source is unavailable. Include the following information with the starter prompt.

| Input               | Sample issue                                                                                                                                                                                                                                                                     |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Issue and outcome   | `API-142`: Add `GET /v1/projects/{project_id}/events` so customers can page through an activity feed.                                                                                                                                                                            |
| Repository and base | Put the sample folder in your chosen repository, then record the branch and exact commit selected for the task.                                                                                                                                                                  |
| Relevant code       | The sample's `api.ts`, `fixtures.ts`, `test.ts`, and `openapi.json`, plus your repository's `AGENTS.md`.                                                                                                                                                                         |
| Existing patterns   | Keep authentication and project authorization before pagination validation. Use signed cursors and the documented public error envelope. When adapting the issue, follow your repository's existing helpers.                                                                     |
| Test setup          | Fixed in-memory test projects for two tenants, six tenant-A projects, a timestamp tie split across a page boundary, timestamps with fractional precision, empty and exactly full final pages, and 105 events for limit checks.                                                   |
| Validation          | `node --experimental-strip-types test.ts --seeded` (expected failure), `node --experimental-strip-types test.ts` (corrected state), and `node --experimental-strip-types reproduce.ts ./evidence`. For your own service, add its actual type, lint, regression, and CI commands. |
| Scope               | Endpoint, focused tests, and its OpenAPI documentation. No new dependencies, database migration, frontend, deployment, or auth redesign.                                                                                                                                         |
| Handoff             | A draft PR when the available repository integration supports it and you have authorized creation; otherwise a diff and draft PR description.                                                                                                                                    |

For the sample, prepare Node 22.6 or later; the tests create their own test sessions and cursor-signing key and bind a temporary HTTP server to the loopback interface. For your own service, also prepare its dependencies, test configuration, and isolated services. Verify that its cursor helper can bind a cursor to the authenticated tenant and requested project before assigning this issue.

### Define the API contract

Confirm the sample contract below matches your repository before implementation. A successful response is HTTP 200 with exactly `{ items, next_cursor }`.

Each item has exactly four required public fields: `id` (nonempty string), `created_at` (UTC RFC 3339 timestamp string), `type` (nonempty string), and `summary` (string). `items` is an array of these objects; `next_cursor` is an opaque nonempty string or `null`.

Internal tenant/project keys, database metadata, raw event payloads, and credentials are not response fields. Describe response field types, required fields, whether fields allow `null`, and closed object shapes in OpenAPI. Verify the serialized HTTP bodies against that schema.

Events sort by `created_at DESC, id DESC`, preserving the timestamp's fractional precision and using descending lexical ID order. The cursor resumes strictly after the last returned tuple in that order.

The default page size is 25; valid limits are decimal integers from 1 through 100. Repeated limit or cursor parameters are invalid. Return a non-null cursor only when another matching event exists.

Both a partial final page and an exactly full final page return `next_cursor: null`; an empty authorized project returns `items: []` and `next_cursor: null`.

The sample signs each cursor and binds it to the authenticated tenant and requested project. Authenticate and authorize the requested project before validating its limit or cursor, so parameter errors cannot reveal whether another tenant's project exists.

A missing or invalid session returns 401; an inaccessible or nonexistent project returns the same generic 404. After confirming access, check the limit before the cursor.

A malformed, tampered, structurally invalid, or tenant/project-mismatched cursor returns HTTP 400 with code `invalid_cursor`. A valid cursor for another project in the same tenant, or for another tenant, is invalid when supplied to an authorized project.

A supplied cursor must not change the authorization result for an inaccessible project. The sample's version-1 cursor does not expire; unsupported versions are invalid.

In the sample, every error body has exactly `{ error: { code, message } }`, with both fields required strings and no extra fields.

Use these generic error responses:

- 400 `invalid_cursor` / `Invalid cursor.`
- 400 `invalid_limit` / `Limit must be an integer from 1 through 100.`
- 401 `unauthenticated` / `Authentication required.`
- 404 `not_found` / `Project not found.`

Keep decoded cursor contents, tenant/project identifiers, raw errors, and stack traces out of every error body. Use the real repository's approved envelope and codes if they differ; resolve that contract difference before changing shared helpers.

Traversal and replay assertions use fixed fixtures with no concurrent writes: following cursors returns every event once in the agreed order and terminates within `ceil(event_count / limit)` requests for a nonempty feed, or one request for an empty feed.

Replaying a valid cursor with the same request parameters returns the same items and continuation position while those fixtures stay unchanged; it need not produce byte-identical signed tokens.

This contract does not promise single-use cursors, snapshot pagination, or identical results after feed changes. Document the repository's existing feed consistency policy; stop for a product decision if no policy exists and the issue requires snapshot behavior.

## How to use

1. **Choose the issue and prepare the environment.** Confirm that the contract above matches the actual repository. Select the prepared cloud environment and the intended base commit. Supply the issue packet directly in the task; starting this recipe does not depend on an automatic issue-tracker trigger.
2. **Run the starter prompt.** Replace its bracketed inputs with your repository, issue packet, boundaries, and checks. Choose whether Codex should return a diff or create an authorized draft PR. The starter prompt on this page contains the full handoff instructions.
3. **Establish the baseline.** Codex should read repository instructions and run the approved baseline checks before editing.

   For the sample, run `node --experimental-strip-types test.ts`; `--seeded` is a separate deliberate failure demonstration.

   For your own service, run its existing regression, type, and lint checks. A new endpoint's focused test file may not exist yet; record that as a test to create. Resolve failing existing checks or unavailable test services before attributing later results to the feature.

4. **Implement and verify the contract.** Ask Codex to use the existing access and cursor helpers, implement the endpoint, add the acceptance tests below, and update its API documentation. Where practical, the new tests should fail against the original code and pass after the change. Keep those results with the final verification record. In the downloadable sample, `--seeded` selects a deliberate defect for this comparison; this comparison is separate from a failing baseline in your repository.
5. **Review the change and its evidence.** Read the diff, acceptance checks, check outputs, and remaining risks together. If Codex creates an authorized draft PR, verify that its base and head are correct. If PR tooling is unavailable, use the returned diff and description to prepare the PR through your normal process. List any unresolved checks in the draft PR and keep it unready for merge.
6. **Resolve review feedback and merge through your normal process.** Give Codex the specific comments to address in the same task, then rerun the affected checks. A reviewer confirms required CI and approves the final commit before merging.

## Acceptance tests to require

These tests make the issue small enough to delegate and specific enough to review. Adapt the names to your test runner, while preserving the behavior each test proves.

### Stable traversal

Seed five fixed events: `evt_105` has the newest timestamp, `evt_104`, `evt_103`, and `evt_102` share the middle timestamp, and `evt_101` has the oldest.

With `limit=2`, require exactly these pages: `[evt_105, evt_104]`, `[evt_103, evt_102]`, `[evt_101]`. The tie group must cross the first boundary.

Assert exact order, no duplicate or missing IDs, non-null cursors on the first two pages, and a null cursor on the third; fail if traversal exceeds three requests.

Replay the first continuation cursor with the same limit against unchanged fixtures and assert the same second-page items and continuation position.

### Default and boundary sizes

Seed more than 100 events. Assert 25 items without a `limit` parameter, one with `limit=1`, and 100 with `limit=100`.

### Invalid limits

Assert HTTP 400 for `0`, `101`, `-1`, a fractional value, and a string such as `many`, using the existing validation error shape.

### Empty and final pages

Assert an empty authorized project returns `items: []` and `next_cursor: null`. With `limit=2`, assert that five events produce a one-item third page with a null cursor and that four events produce a two-item second page with a null cursor. The full final page must not require an extra empty request.

### Authentication

Assert missing and invalid sessions return the agreed 401 schema, including requests with a malformed cursor or a cursor from another scope. Cursor validation must not override authentication.

### Tenant isolation

Authenticate as tenant A and request tenant B's project or a nonexistent project. Assert the same agreed generic 404 body with no event data, including when the request carries a malformed or mismatched cursor. Authorization must precede cursor validation.

### Cursor scope

Request an authorized tenant-A project with (1) a valid signed cursor from another tenant-A project and (2) a valid signed cursor issued under tenant B.

Assert both return the same HTTP 400 `invalid_cursor` body with no event data or scope details. Test these separately from requests to an inaccessible project, which must return 404.

### Malformed and tampered cursors

On an authorized project, assert HTTP 400 `invalid_cursor` for tokens the helper cannot decode, tokens with modified signatures, and signed tokens that omit required cursor fields or give those fields the wrong type. Use isolated test signing fixtures.

Cover unsupported versions or expired tokens if the shared helper supports those features. Assert that responses match the agreed generic error schema and contain no decoded contents, identifiers, raw errors, or stack traces.

### Existing behavior

The sample checks the existing project-detail route with authorized, unauthorized, and inaccessible-project requests. In your service, run its established regression suite, type check, and lint.

### Public response schema

Validate actual HTTP 200, 400, 401, and 404 response bodies against the agreed OpenAPI schemas. Assert required keys, item field types, timestamp format, whether the cursor allows `null`, and no extra properties at any object level.

Seed internal fields in stored events and verify they are absent from serialized items; verify every error response contains only its approved generic code and message.

### Documentation

Verify the OpenAPI operation and examples match the implemented parameters, exact success/error schemas, authorization precedence, ordering, final-page rules, and fixed-fixture replay/consistency limits. Run the repository's API specification validation if one exists.

## What good output looks like

### Shared evidence record

Use this evidence format for each acceptance criterion. Populate it from observed output. For a new test that does not exist at baseline, distinguish “not yet present” from a failed existing check.

```text
Criterion / test: [specific behavior and test location]
Environment: [published setup reference; runtime, database and dependency versions]
Before: [revision + test-only diff ID; command; exit code; observed assertion; log path]
After: [final revision or base + diff ID; command; exit code; observed assertion; log path]
Status: [pass / fail / blocked / not run]
Limits / reviewer action: [untested behavior, blocker, or decision required]
```

Keep red and green runs tied to their actual tested states, including test-only changes on the original revision. Keep the logs, response fixtures, and final diff with the handoff; file and test names alone do not prove execution. Update the evidence when the tested revision changes. Checks that are blocked or have not run cannot count as passing.

A useful PR description links each claim to its evidence. Use this handoff template and replace every bracketed field with observed results.

```text
Title: Add cursor pagination for project events
Issue: API-142
Base: [branch and commit]
Tested state: [head commit, or base commit plus attached diff identifier]

Changes
- Add the project-events endpoint using the existing project access helper.
- Reuse signed cursors scoped to tenant and project.
- Add contract tests and update the OpenAPI operation.

Acceptance evidence
- [One row per criterion above: test, observed result, and log reference.]

Validation
- Before edits: [command, result, and log reference for each baseline check].
- New tests against original code: [result, or not run with reason].
- After edits: [command, result, and log reference for each required check].
- CI: [check links and actual states, or not available].
- Remaining checks: [specific checks and blockers, or none with supporting evidence].

Reviewer focus
- [Highest-risk behavior and unresolved criteria.]

Remaining risk and rollback
- [Observed limitations; distinguish them from untested assumptions.]
- [How this change can be reverted and whether any callers depend on it.]
```

## Iterate from review comments

Use a focused follow-up for a specific review finding. For example:

```text
Address this review comment in the current change:
"Repeat the five-event traversal with limit=3; assert pages
[evt_105, evt_104, evt_103] and [evt_102, evt_101], then a null cursor."

Add the regression test and change the implementation only if it exposes a
failure. Rerun the focused endpoint tests and any other required checks affected
by the edit. Update the evidence table with the tested state and actual results.
Keep the same scope. Do not merge or deploy.
```

Provide the text of the comment if Codex cannot access the review directly. A reviewer should check that the response resolves the behavior in question, rather than only satisfying the wording of the comment.

## When to stop

- **The baseline is red or cannot run.** Return the failing check and setup details. Fix the environment or agree on a documented baseline before continuing.
- **The contract conflicts with existing behavior.** Identify the conflict, affected callers, and the smallest decision needed. Do not silently change the contract.
- **The change needs a migration, new dependency, or auth redesign.** Explain why and split or re-scope the issue before expanding it.
- **Tests fail after implementation.** Do not treat the change as ready to merge. Report the failing cases. Do not remove assertions or weaken authorization to make checks pass.
- **Repository write integration is unavailable.** Return the diff, draft PR description, and validation evidence. A teammate can complete the repository handoff.

## Reuse the workflow

After a reviewer accepts the first result, save the issue packet and acceptance checklist in your team's issue template. Record stable repository guidance, such as test commands and where API contracts live, in `AGENTS.md` or the existing contributor guide.
