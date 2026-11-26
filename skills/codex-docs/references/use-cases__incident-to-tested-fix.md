---
title: "Investigate an incident and test a fix"
source: https://learn.chatgpt.com/use-cases/incident-to-tested-fix
path: /use-cases/incident-to-tested-fix
---

# Investigate an incident and test a fix

Turn an incident packet into a reproduced bug, a focused patch, and a reviewable handoff.

Give Codex Cloud a sanitized incident packet and a working test environment. Investigate the evidence, reproduce a supported code defect, and return a focused patch with regression-test evidence and a deployment and rollback handoff.

## Recipe details

```yaml
name: Investigate an incident and test a fix
tagline: Turn an incident packet into a reproduced bug, a focused patch, and a
  reviewable handoff.
summary: Give Codex Cloud a sanitized incident packet and a working test
  environment. Investigate the evidence, reproduce a supported code defect, and
  return a focused patch with regression-test evidence and a deployment and
  rollback handoff.
bestFor:
  - Small engineering teams investigating a stabilized incident.
  - Application defects with sanitized evidence and safe reproduction inputs.
  - Teams reviewing a focused fix in a working, isolated test environment.
starterPrompt:
  title: Investigate an incident
  body: >-
    Investigate [incident ID] in [repository/service] using [path to sanitized
    incident packet]. Work in the published cloud environment selected for this
    task.

    The packet identifies the incident time window, affected release SHA,
    expected behavior, observed behavior, relevant log and trace excerpts, and
    safe reproduction inputs. Read AGENTS.md and the repository's setup and
    testing instructions first. Check that the checkout matches the affected
    release, or explain the difference before drawing conclusions.

    Build a short timeline with file and line references to the packet and
    source code. Separate observations, hypotheses, and evidence gaps. Test the
    strongest hypothesis in the isolated test environment. If you cannot
    reproduce the failure or lack decisive evidence, return an investigation
    with the next diagnostic step; do not claim a confirmed root cause or make a
    speculative fix.

    If the evidence supports a code defect, add a regression test and run it
    against the original code to demonstrate the failure. Make the smallest fix,
    rerun that test, then run the relevant broader tests, lint, and type checks
    available in this repository. Record the commands, exit codes, and any
    checks you could not run.

    Prepare a branch diff, a draft pull-request description, test-evidence.md,
    and a deployment and rollback handoff. Include the supported cause,
    unresolved uncertainty, and behavior changed. Use one evidence row per
    criterion: revision and environment versions, baseline command/exit/log,
    final command/exit/log, actual result, and pass/fail/blocked/not-run status
    with limitations. Keep the PR description as a local draft for review.

    For this duplicate-webhook example, name the before-commit and after-commit
    failure points, prove duplicate contention with independent database
    connections, and state isolation, receipt-retention, and mixed-version
    rollout assumptions.

    For this duplicate-webhook example, before proposing that retained
    deliveries resume, identify legacy orders without matching receipts after
    old consumers have drained. Hold affected event keys using the existing
    queue or quarantine procedure. Add a seeded orphan-with-pending-retry test
    that proves no second order or success acknowledgment occurs while held.
    Reconcile only from trusted immutable event identity, canonical payload, and
    committed-order evidence; keep missing or conflicting evidence quarantined
    for owner review. Do not invent fingerprints, delete receipts, or replay an
    unresolved legacy event.

    Use only the supplied packet and repository unless I identify another
    approved source. Access only the explicitly approved read-only monitoring
    source, if supplied. Write code and task artifacts only in this repository;
    use only its isolated test database. Do not connect directly to production
    application or database hosts, or modify production systems. Do not replay
    production events, modify live data or monitoring, create or post external
    updates, merge, or deploy.
relatedLinks:
  - label: Cloud environments
    url: https://learn.chatgpt.com/docs/environments/cloud-environments
```

Give Codex one bounded incident to investigate in a prepared cloud environment. The goal is a result an engineer can review: a supported explanation, a regression test that fails before the fix, a focused patch, and evidence from the tests that ran.

This works well after the immediate incident has been stabilized and the remaining job is to understand and fix an application defect. If the available evidence cannot establish the cause, a useful result is a clear account of the investigation and the next diagnostic step.

## Prepare the environment and incident packet

1. In the web or desktop app, choose **Work in** > **Cloud** and select a published environment.

2. To create one, select **Create environment**, choose the GitHub repositories, and ask Codex to prepare the runtime, dependencies, and isolated test services.

3. Review the setup report, resolve failed checks, and **Publish** before starting a new task.

- Follow the [current Cloud environment guide](https://learn.chatgpt.com/docs/environments/cloud-environments).
- Keep repository guidance in [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

If dependencies change or service setup changes, edit the reusable environment, test it, and **Republish**; then validate the updated environment in a new task.

Repository refresh does not rerun install/start commands, and existing tasks retain their own state.

Configure required network destinations and test credentials separately; allowing a destination does not grant service access.

Confirm that the affected checkout, dependencies, checks, and disposable test database work in the new task. Record the starting commit and test baseline.

Keep the initial investigation self-contained. Place a sanitized packet in the repository or make its files available to the task. An engineer should assemble and check it before starting:

| Input               | What to include                                                                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Incident summary    | Incident ID, UTC time window, expected and observed behavior, known impact, and current status. Distinguish confirmed counts from estimates.       |
| Release identity    | The deployed commit SHA, deployment time, relevant configuration values without secrets, and the last known good release if available.             |
| Correlated evidence | Log and trace excerpts with timestamps, event IDs, request IDs, trace IDs, and file references. Preserve identifiers consistently when sanitizing. |
| Safe reproduction   | Test request bodies, relevant fixtures, and instructions for exercising the suspected path without calling live services.                          |
| Repository guidance | Relevant paths, database engine, test commands, permitted changes, and the engineer who will review the result.                                    |

Do not include access tokens, customer payloads, or personal data in the packet.

A monitoring integration is optional. If you use one, grant read-only access to the relevant project and time window; the file-based workflow does not require it. Repository instructions should keep test credentials separate from production configuration.

## Run the starter prompt

Use the starter prompt on this page and replace its placeholders with your incident ID, repository, and packet path. The first result should connect the evidence to the affected code, explain what can be reproduced, and identify missing information.

Ask Codex to continue through implementation only when the evidence supports a code defect. Otherwise, review the investigation and provide the missing input. A plausible explanation, a recent code change, or a successful test on a different release is not enough to establish the cause.

## Example: A retried webhook creates a duplicate order

Use the [runnable incident sample](https://developers.openai.com/codex/use-cases/incident-to-tested-fix/sample.zip) to practice the investigation. It includes a prepared incident packet, a handler with a reproducible defect, the corrected handler, and PostgreSQL tests.

The service receives an `order.created` webhook, writes an order, and records that the event has been processed. During an incident, a retry appears to create a second order. The team has already stabilized the service and wants a patch for review.

The sample uses TypeScript, Node.js's test runner, and PostgreSQL. Its disposable fixture has an `event_receipts` table with non-null identity columns and a non-deferrable unique key on `(provider, account_id, event_id)`.

The schema permits a receipt claim before the order exists and retains the canonical payload fingerprint needed to detect conflicting reuse of the same event key.

If your application instead requires an order foreign key at claim time or lacks this conflict evidence, stop for a separate schema/design decision.

Record the exact runtime, dependency lock, PostgreSQL version, transaction isolation level, and receipt schema in the evidence. The downloadable fixture pins Node.js 24.19.0, PostgreSQL 17.6, and `pg` 8.23.1.

For the supplied Compose setup, prepare an environment with a working Docker daemon and verify `docker info` before publishing it. Its database accepts only public test credentials and is bound to the local loopback interface. Use your application's database engine and relevant settings when adapting the test.

This example assumes PostgreSQL READ COMMITTED, stable provider event IDs, and receipt retention covering the provider's retry/replay window.

The fixed handler places receipt and order writes in one database transaction. The fixture provisions a disposable database and a `delivery_holds` table to model an existing queue's quarantine procedure; that table is test infrastructure, not a proposed application migration.

The application fix adds no queue, database service, schema migration, or monitoring integration. If those assumptions do not hold, stop and revise the scope.

### Run the sample

Extract the ZIP, open its directory, and use Docker with Compose:

```bash
docker compose -p codex-incident-rehearsal up -d --wait postgres
docker compose -p codex-incident-rehearsal run --rm runner node --experimental-strip-types main.ts baseline
docker compose -p codex-incident-rehearsal run --rm runner node --experimental-strip-types main.ts regression
docker compose -p codex-incident-rehearsal run --rm runner
docker compose -p codex-incident-rehearsal down --volumes
```

The baseline command must exit with code `1`: the retry assertion observes two orders and one receipt instead of one of each. The regression command runs the same assertion against the corrected handler and must exit with code `0`.

The final test command exercises the full matrix, including independent connections, database lock contention, and legacy-orphan quarantine.

If your installation provides `docker-compose`, use that spelling in place of `docker compose`. Run these commands sequentially; the suite resets only its marked test schema.

Use the [complete Python incident program](https://github.com/openai/developers-website/blob/main/src/content/platform/python-examples/codex-cloud/incident-to-tested-fix.py) from a complete [Python sample project](https://github.com/openai/developers-website/tree/main/src/content/platform/python-examples) checkout. The excerpt below shows `fixed()`; use the linked full program for its supporting helpers and test runner. Keep `codex-cloud/incidents/`, `pyproject.toml`, and `uv.lock` intact. The ZIP above contains only TypeScript.

Install Python 3.11 or later, uv, and Docker Compose. The locked Python dependencies include `psycopg[binary]==3.3.9`; `uv sync --locked` installs Psycopg and its binary package. Start at the repository checkout root in a POSIX shell. Keep the sibling `typescript-examples/codex-cloud/incident-to-tested-fix/compose.yaml` and `init.sql` together; the commands below start the shared PostgreSQL 17.6 fixture on `127.0.0.1:55432`.

Reserve this fixture for the rehearsal and keep application data out of it. Run the following Python commands instead of the Node runner commands above. Expect the deliberately failing baseline to exit with `1`, then continue with regression and fixed:

```bash
incident_fixture_dir="$PWD/src/content/platform/typescript-examples/codex-cloud/incident-to-tested-fix"
docker compose -f "$incident_fixture_dir/compose.yaml" -p codex-incident-rehearsal up -d --wait postgres
cd src/content/platform/python-examples
uv sync --locked
CODEX_INCIDENT_TEST_PASSWORD=synthetic-incident-fixture-only .venv/bin/python codex-cloud/incident-to-tested-fix.py baseline
CODEX_INCIDENT_TEST_PASSWORD=synthetic-incident-fixture-only .venv/bin/python codex-cloud/incident-to-tested-fix.py regression
CODEX_INCIDENT_TEST_PASSWORD=synthetic-incident-fixture-only .venv/bin/python codex-cloud/incident-to-tested-fix.py fixed
docker compose -f "$incident_fixture_dir/compose.yaml" -p codex-incident-rehearsal down --volumes
```

Use only the public synthetic fixture password shown above. Each Python command supplies it through `CODEX_INCIDENT_TEST_PASSWORD` for that child process; no production credential is needed. The runner connects to the fixture's `codex_incident_test` database and user. Expect regression and fixed to exit with `0`.

Run the final Compose command after the checks, including after a failure, to remove the disposable fixture. The absolute Compose path keeps cleanup valid after changing to the Python directory. Do not run this fixture alongside another rehearsal using the same project or port.

**Java setup**

Use Java 17 or later and Maven with a complete `developers-website` checkout, including the [Java sample project](https://github.com/openai/developers-website/tree/main/src/content/platform/java-examples).

Start at the checkout root in a POSIX shell. The fixture loader requires the sibling `../typescript-examples/codex-cloud/incident-to-tested-fix/incidents/INC-DEMO-014/order-created.sanitized.json` file, relative to the Java project directory, from the same checkout.

The commands use the same Compose project, PostgreSQL service, and cleanup as above. The explicit Compose file path keeps startup and cleanup independent of the Java working directory.

```bash
incident_fixture_dir="$PWD/src/content/platform/typescript-examples/codex-cloud/incident-to-tested-fix"
docker compose -f "$incident_fixture_dir/compose.yaml" -p codex-incident-rehearsal up -d --wait postgres
cd src/content/platform/java-examples
mvn -q -DskipTests compile dependency:build-classpath -Dmdep.outputFile=target/live-classpath
PGPASSWORD=synthetic-incident-fixture-only java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudIncidentToTestedFix baseline
PGPASSWORD=synthetic-incident-fixture-only java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudIncidentToTestedFix regression
PGPASSWORD=synthetic-incident-fixture-only java -cp "target/classes:$(cat target/live-classpath)" com.openai.docs.codexcloud.CodexCloudIncidentToTestedFix fixed
docker compose -f "$incident_fixture_dir/compose.yaml" -p codex-incident-rehearsal down --volumes
```

**Expected results**

Each Java command supplies the existing public Compose fixture password through `PGPASSWORD` only for that child process. Expect the baseline failure, regression success, and complete fixed suite described above.

For Ruby, use the complete [Ruby sample project](https://github.com/openai/developers-website/tree/main/src/content/platform/ruby-examples) and install its dependencies using Ruby 3.3. Start PostgreSQL with the Compose setup in the ZIP archive. From the Ruby project directory, run `bundle exec ruby codex-cloud/incident-to-tested-fix/main.rb baseline`, then repeat with `regression` and `fixed`. These commands use the same disposable database and produce the expected failing and passing results; use them in place of the Node runner commands.

Use Go 1.26 or later with a full [repository checkout](https://github.com/openai/developers-website). Keep the `src/content/platform/go-examples/` module (`go.mod` and `go.sum`) and the sibling TypeScript incident fixture intact. Start the commands below at the repository root.

The Go runner uses the same marked PostgreSQL 17.6 fixture on `127.0.0.1:55432`. Use a temporary password file containing only the fixture's public synthetic password, with mode `0600`. Set `PGPASSFILE` for each command and exclude any inherited `PGPASSWORD`.

```bash
incident_fixture_dir="$PWD/src/content/platform/typescript-examples/codex-cloud/incident-to-tested-fix"
docker compose -p codex-incident-rehearsal -f "$incident_fixture_dir/compose.yaml" up -d --wait postgres
codex_pgpass_file=$(mktemp)
chmod 600 "$codex_pgpass_file"
printf '%s\n' '127.0.0.1:55432:codex_incident_test:codex_incident_test:synthetic-incident-fixture-only' > "$codex_pgpass_file"
cd src/content/platform/go-examples/codex-cloud/incident-to-tested-fix
env -u PGPASSWORD PGPASSFILE="$codex_pgpass_file" go run . -test.v baseline
env -u PGPASSWORD PGPASSFILE="$codex_pgpass_file" go run . -test.v regression
env -u PGPASSWORD PGPASSFILE="$codex_pgpass_file" go run . -test.v fixed
rm -f "$codex_pgpass_file"
docker compose -p codex-incident-rehearsal -f "$incident_fixture_dir/compose.yaml" down --volumes
```

The Go runner reads the sibling `typescript-examples/codex-cloud/incident-to-tested-fix/incidents/INC-DEMO-014/order-created.sanitized.json`. Expect exit status `1` from the deliberately failing baseline and `0` from regression and fixed. Use these Go commands in place of the Node runner commands above.

### Inspect the transaction handler

The TypeScript excerpt comes from `main.ts` in the ZIP.

The Ruby examples come from the linked Ruby sample project.

Run the complete files for the selected language with the supplied database fixture.

<details>
<summary>Receipt claim and order transaction</summary>
Claim a receipt and write an order

```typescript
import type { Client } from "pg";

type IncidentEvent = {
  provider: string;
  accountId: string;
  eventId: string;
  payload: { type: string; orderId: string; amountCents: number };
};

async function fixed(
  client: Client,
  input: IncidentEvent,
  hook = async (_boundary: string) => {}
) {
  await assertNotHeld(client, input);
  await hook("beforeClaim");
  await client.query("BEGIN ISOLATION LEVEL READ COMMITTED");
  let committed = false;
  try {
    const claimed = await client.query(
      `INSERT INTO event_receipts(provider, account_id, event_id, payload_fingerprint)
       VALUES ($1,$2,$3,$4)
       ON CONFLICT (provider, account_id, event_id) DO NOTHING RETURNING event_id`,
      [...key(input), fingerprint(input)]
    );
    trace("receipt-claim-result", client, input, {
      inserted: claimed.rowCount === 1,
    });
    if (claimed.rowCount === 1) {
      await hook("afterClaim");
      await writeOrder(client, input);
      await hook("afterOrder");
    } else {
      // A new READ COMMITTED statement sees the winner after its commit.
      await checkReceipt(client, input);
    }
    await client.query("COMMIT");
    committed = true;
    trace("transaction-committed", client, input);
    await hook("afterCommit");
    trace("acknowledged", client, input, acknowledgment);
    return acknowledgment;
  } catch (error) {
    if (!committed) {
      await client.query("ROLLBACK");
      trace("transaction-rolled-back-no-ack", client, input);
    } else {
      trace("committed-response-lost-no-ack", client, input);
    }
    throw error;
  }
}
```

```python
# Requires an autocommit Psycopg connection dedicated to this delivery, with the
# fixture's immediate UNIQUE(provider,account_id,event_id) receipt constraint.
# Existing legacy orphans must be held before consumers resume ingestion.
def fixed(client, input_event, hook=no_failure):
    assert_not_held(client, input_event)
    hook("beforeClaim")
    client.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
    committed = False
    try:
        claim = client.execute(
            """INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint)
               VALUES (%s,%s,%s,%s)
               ON CONFLICT (provider,account_id,event_id) DO NOTHING RETURNING event_id""",
            [*key(input_event), fingerprint(input_event)],
        ).fetchone()
        trace("receipt-claim-result", client, input_event, inserted=claim is not None)
        if claim is not None:
            hook("afterClaim")
            write_order(client, input_event)
            hook("afterOrder")
        else:
            # A new READ COMMITTED statement sees the winner after its commit.
            check_receipt(client, input_event)
        client.execute("COMMIT")
        committed = True
        trace("transaction-committed", client, input_event)
        hook("afterCommit")
        trace("acknowledged", client, input_event, **ACKNOWLEDGMENT)
        return copy.deepcopy(ACKNOWLEDGMENT)
    except BaseException:
        if not committed:
            client.execute("ROLLBACK")
            trace("transaction-rolled-back-no-ack", client, input_event)
        else:
            trace("committed-response-lost-no-ack", client, input_event)
        raise
```

```go
// A nondeferrable database identity constraint serializes competing deliveries.
// Acknowledgment follows commit; losing the response remains safe to retry.
func fixed(c *client, input incidentEvent, h hook) (result acknowledgment, err error) {
	if err = assertNotHeld(c, input); err != nil {
		return result, err
	}
	if err = call(h, "beforeClaim"); err != nil {
		return result, err
	}
	tx, err := c.conn.BeginTx(c.ctx, &sql.TxOptions{Isolation: sql.LevelReadCommitted})
	if err != nil {
		return result, err
	}
	committed, commitAttempted := false, false
	defer func() {
		if !committed && !commitAttempted {
			if rollback(tx, &err) {
				trace("transaction-rolled-back-no-ack", c, input, nil)
			} else {
				trace("rollback-unconfirmed-no-ack", c, input, nil)
			}
		}
	}()
	var claimedID string
	err = tx.QueryRowContext(
		c.ctx,
		`INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint)
         VALUES ($1,$2,$3,$4)
         ON CONFLICT (provider,account_id,event_id) DO NOTHING
         RETURNING event_id`,
		values(input)...,
	).Scan(&claimedID)
	claimed := err == nil
	if err != nil && !errors.Is(err, sql.ErrNoRows) {
		return result, err
	}
	err = nil
	trace("receipt-claim-result", c, input, map[string]any{"inserted": claimed})
	if claimed {
		if err = call(h, "afterClaim"); err != nil {
			return result, err
		}
		if err = writeOrder(c, tx, input); err != nil {
			return result, err
		}
		if err = call(h, "afterOrder"); err != nil {
			return result, err
		}
	} else {
		// READ COMMITTED gives this statement a fresh snapshot after the winner commits.
		if err = checkReceipt(c, tx, input); err != nil {
			return result, err
		}
	}
	commitAttempted = true
	if err = tx.Commit(); err != nil {
		return result, fmt.Errorf("commit outcome unknown; no acknowledgment; reconcile durable state: %w", err)
	}
	committed = true
	trace("transaction-committed", c, input, nil)
	if err = call(h, "afterCommit"); err != nil {
		trace("committed-response-lost-no-ack", c, input, nil)
		return result, err
	}
	trace("acknowledged", c, input, map[string]any{"status": ack.Status, "body": ack.Body})
	return ack, nil
}
```

```java
package com.openai.docs.codexcloud;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Properties;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Synthetic PostgreSQL transaction rehearsal. Requires the owned, marked PostgreSQL 17.6 fixture,
 * exclusive fixture use, org.postgresql:postgresql, and secret PGPASSWORD. Run baseline (expected
 * exit 1), regression, then fixed. No provider delivery or unknown-COMMIT transport failure is
 * being simulated. Never point this program at an application database.
 */
public final class CodexCloudIncidentToTestedFix {
  private static final ObjectMapper JSON = new ObjectMapper();
  private static final String URL = "jdbc:postgresql://127.0.0.1:55432/codex_incident_test";
  private static final Map<String, Object> ACK =
      Map.of("status", 200, "body", Map.of("received", true));

  // Canonical sanitized input from the peer's fictional incident packet.
  private static final String INCIDENT_EVENT_FILE =
      "../typescript-examples/codex-cloud/incident-to-tested-fix/incidents/INC-DEMO-014/order-created.sanitized.json";
  private static IncidentEvent EVENT;

  static IncidentEvent parseIncidentEvent(String data) throws Exception {
    IncidentEvent input = JSON.readValue(data, IncidentEvent.class);
    if (input == null
        || input.provider() == null
        || input.provider().isBlank()
        || input.accountId() == null
        || input.accountId().isBlank()
        || input.eventId() == null
        || input.eventId().isBlank()
        || input.payload() == null
        || input.payload().type() == null
        || input.payload().type().isBlank()
        || input.payload().orderId() == null
        || input.payload().orderId().isBlank()
        || input.payload().amountCents() <= 0) {
      throw new IllegalArgumentException("Incomplete sanitized incident fixture");
    }
    return input;
  }

  public record Payload(String type, String orderId, long amountCents) {}

  public record IncidentEvent(String provider, String accountId, String eventId, Payload payload) {}

  private record Counts(long orders, long receipts) {}

  private record Outcome(Map<String, Object> acknowledgment, Exception failure) {}

  @FunctionalInterface
  private interface Hook {
    void at(String boundary) throws Exception;
  }

  @FunctionalInterface
  private interface Checked {
    void run() throws Exception;
  }

  private static final Hook NO_FAILURE = boundary -> {};
  private final Connection observer;
  private final String mode;
  private int assertions;

  private CodexCloudIncidentToTestedFix(Connection observer, String mode) {
    this.observer = observer;
    this.mode = mode;
  }

  private static Connection connect(String name) throws SQLException {
    String password = System.getenv("PGPASSWORD");
    if (password == null || password.isBlank())
      throw new IllegalArgumentException("Set the disposable fixture's PGPASSWORD secret");
    Properties properties = new Properties();
    properties.setProperty("user", "codex_incident_test");
    properties.setProperty("password", password);
    properties.setProperty("ApplicationName", "fixture-" + name);
    properties.setProperty("connectTimeout", "5");
    properties.setProperty("socketTimeout", "12");
    Connection connection = DriverManager.getConnection(URL, properties);
    try {
      connection.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
      execute(connection, "SET search_path TO incident_rehearsal, public");
      execute(connection, "SET statement_timeout = '8s'");
      return connection;
    } catch (SQLException failure) {
      try {
        connection.close();
      } catch (SQLException cleanup) {
        failure.addSuppressed(cleanup);
      }
      throw failure;
    }
  }

  private static void execute(Connection client, String sql) throws SQLException {
    try (Statement statement = client.createStatement()) {
      statement.execute(sql);
    }
  }

  private static PreparedStatement keyed(
      Connection client, String sql, IncidentEvent input, boolean fingerprint) throws Exception {
    PreparedStatement statement = client.prepareStatement(sql);
    try {
      statement.setString(1, input.provider());
      statement.setString(2, input.accountId());
      statement.setString(3, input.eventId());
      if (fingerprint) statement.setString(4, fingerprint(input));
      return statement;
    } catch (Exception failure) {
      try {
        statement.close();
      } catch (SQLException cleanup) {
        failure.addSuppressed(cleanup);
      }
      throw failure;
    }
  }

  private static String fingerprint(IncidentEvent input) throws Exception {
    // Explicit canonical field order, exclusively for this trusted fixture.
    return HexFormat.of()
        .formatHex(
            MessageDigest.getInstance("SHA-256")
                .digest(
                    JSON.writeValueAsBytes(
                        List.of(
                            input.payload().type(),
                            input.payload().orderId(),
                            input.payload().amountCents()))));
  }

  private static int pid(Connection client) throws SQLException {
    try (Statement statement = client.createStatement();
        ResultSet result = statement.executeQuery("SELECT pg_backend_pid()")) {
      if (!result.next()) throw new SQLException("Missing backend PID");
      return result.getInt(1);
    }
  }

  // The shared evidence reader recognizes JSON trace records with action first.
  private static void emit(String action, Map<String, Object> detail) throws Exception {
    Map<String, Object> record = new LinkedHashMap<>();
    record.put("action", action);
    record.putAll(detail);
    System.out.println(JSON.writeValueAsString(record));
  }

  private static void trace(
      String action, Connection client, IncidentEvent input, Map<String, Object> detail)
      throws Exception {
    Map<String, Object> record = new LinkedHashMap<>();
    record.put("action", action);
    record.put("pid", pid(client));
    record.put("key", List.of(input.provider(), input.accountId(), input.eventId()));
    record.putAll(detail);
    System.out.println(JSON.writeValueAsString(record));
  }

  private void equal(Object actual, Object expected) {
    assertions++;
    if (!Objects.equals(actual, expected))
      throw new AssertionError("Expected " + expected + ", got " + actual);
  }

  private void require(boolean condition, String message) {
    assertions++;
    if (!condition) throw new AssertionError(message);
  }

  private static Hook failAt(String point) {
    return boundary -> {
      if (boundary.equals(point)) throw new IllegalStateException("injected:" + point);
    };
  }

  private void rejects(Checked action, String message) throws Exception {
    try {
      action.run();
    } catch (Exception failure) {
      require(
          failure.getMessage() != null && failure.getMessage().contains(message),
          "Expected " + message + ", got " + failure);
      return;
    }
    throw new AssertionError("Expected failure " + message);
  }

  private Counts counts(IncidentEvent input) throws Exception {
    try (PreparedStatement statement =
        keyed(
            observer,
            "SELECT (SELECT count(*) FROM orders WHERE provider=? AND account_id=? AND event_id=?)"
                + " AS orders, (SELECT count(*) FROM event_receipts WHERE provider=? AND"
                + " account_id=? AND event_id=?) AS receipts",
            input,
            false)) {
      statement.setString(4, input.provider());
      statement.setString(5, input.accountId());
      statement.setString(6, input.eventId());
      try (ResultSet result = statement.executeQuery()) {
        if (!result.next()) throw new SQLException("Missing counts");
        Counts counts = new Counts(result.getLong("orders"), result.getLong("receipts"));
        trace(
            "committed-state",
            observer,
            input,
            Map.of("orders", counts.orders(), "receipts", counts.receipts()));
        return counts;
      }
    }
  }

  private void assertCounts(long orders, long receipts, IncidentEvent input) throws Exception {
    equal(counts(input), new Counts(orders, receipts));
  }

  private static void writeOrder(Connection client, IncidentEvent input) throws Exception {
    try (PreparedStatement statement =
        keyed(
            client,
            "INSERT INTO orders(provider,account_id,event_id,payload_fingerprint) VALUES (?,?,?,?)",
            input,
            true)) {
      statement.executeUpdate();
    }
    trace("order-written", client, input, Map.of());
  }

  private static void checkReceipt(Connection client, IncidentEvent input) throws Exception {
    try (PreparedStatement statement =
            keyed(
                client,
                "SELECT payload_fingerprint FROM event_receipts WHERE provider=? AND account_id=?"
                    + " AND event_id=?",
                input,
                false);
        ResultSet result = statement.executeQuery()) {
      if (!result.next()) throw new IllegalStateException("missing-receipt-after-skipped-claim");
      String stored = result.getString(1);
      if (!fingerprint(input).equals(stored)) throw new IllegalStateException("payload-conflict");
      if (result.next()) throw new IllegalStateException("multiple-receipts");
    }
  }

  private static void assertNotHeld(Connection client, IncidentEvent input) throws Exception {
    try (PreparedStatement statement =
            keyed(
                client,
                "SELECT 1 FROM delivery_holds WHERE provider=? AND account_id=? AND event_id=?",
                input,
                false);
        ResultSet result = statement.executeQuery()) {
      if (result.next()) {
        trace("legacy-retry-held-no-ack", client, input, Map.of());
        throw new IllegalStateException("legacy-retry-held");
      }
    }
  }

  /** Legacy defect: the order survives failure before receipt creation. */
  private static Map<String, Object> baseline(Connection client, IncidentEvent input, Hook hook)
      throws Exception {
    try (PreparedStatement statement =
            keyed(
                client,
                "SELECT 1 FROM event_receipts WHERE provider=? AND account_id=? AND event_id=?",
                input,
                false);
        ResultSet result = statement.executeQuery()) {
      if (result.next()) {
        checkReceipt(client, input);
        return ACK;
      }
    }
    client.setAutoCommit(false);
    boolean restore = true;
    try {
      writeOrder(client, input);
      client.commit();
    } catch (Exception failure) {
      restore = rollback(client, failure);
      throw failure;
    } finally {
      if (restore) client.setAutoCommit(true);
    }
    trace("legacy-order-committed-without-receipt", client, input, Map.of());
    hook.at("afterOrder");
    try (PreparedStatement statement =
        keyed(
            client,
            "INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint) VALUES"
                + " (?,?,?,?)",
            input,
            true)) {
      statement.executeUpdate();
    }
    trace("legacy-receipt-committed", client, input, Map.of());
    return ACK;
  }

  private static boolean rollback(Connection client, Exception failure) {
    try {
      client.rollback();
      return true;
    } catch (SQLException cleanup) {
      failure.addSuppressed(cleanup);
      try {
        client.close();
      } catch (SQLException closing) {
        failure.addSuppressed(closing);
      }
      return false; // Never restore autocommit after an unsuccessful rollback.
    }
  }

  /** Claim and business write commit together, with READ COMMITTED duplicate visibility. */
  private static Map<String, Object> fixed(Connection client, IncidentEvent input, Hook hook)
      throws Exception {
    assertNotHeld(client, input);
    hook.at("beforeClaim");
    client.setAutoCommit(false);
    boolean committed = false;
    boolean commitAttempted = false;
    boolean restore = true;
    try {
      boolean inserted;
      try (PreparedStatement statement =
              keyed(
                  client,
                  "INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint)"
                      + " VALUES (?,?,?,?) ON CONFLICT (provider,account_id,event_id) DO NOTHING"
                      + " RETURNING event_id",
                  input,
                  true);
          ResultSet result = statement.executeQuery()) {
        inserted = result.next();
      }
      trace("receipt-claim-result", client, input, Map.of("inserted", inserted));
      if (inserted) {
        hook.at("afterClaim");
        writeOrder(client, input);
        hook.at("afterOrder");
      } else {
        // A new statement sees the winner's commit after a blocked claim returns.
        checkReceipt(client, input);
      }
      commitAttempted = true;
      client.commit();
      committed = true;
      trace("transaction-committed", client, input, Map.of());
      hook.at("afterCommit");
      trace("acknowledged", client, input, ACK);
      return ACK;
    } catch (Exception failure) {
      if (!committed && commitAttempted) {
        // A transport error during COMMIT does not establish whether the commit happened.
        // This branch is not exercised by the post-commit response-loss rehearsal.
        restore = false;
        try {
          client.close();
        } catch (SQLException closing) {
          failure.addSuppressed(closing);
        }
        throw new IllegalStateException(
            "commit-outcome-unknown; discard connection and inspect durable state", failure);
      } else if (!committed) {
        restore = rollback(client, failure);
        if (restore) trace("transaction-rolled-back-no-ack", client, input, Map.of());
      } else {
        trace("committed-response-lost-no-ack", client, input, Map.of());
      }
      throw failure;
    } finally {
      if (restore) client.setAutoCommit(true);
    }
  }

  /** Only after ingestion is paused and all legacy consumers have drained. */
  private static int identifyAndHoldLegacyOrphans(Connection client) throws Exception {
    int count;
    try (Statement statement = client.createStatement()) {
      count =
          statement.executeUpdate(
              "INSERT INTO delivery_holds(provider,account_id,event_id) SELECT DISTINCT"
                  + " o.provider,o.account_id,o.event_id FROM orders o WHERE NOT EXISTS (SELECT 1"
                  + " FROM event_receipts r WHERE r.provider=o.provider AND"
                  + " r.account_id=o.account_id AND r.event_id=o.event_id) ON CONFLICT DO NOTHING");
    }
    emit("pre-resume-orphans-held", Map.of("keys", count));
    return count;
  }

  private void reconcileHeldOrphan(Connection client, IncidentEvent input) throws Exception {
    client.setAutoCommit(false);
    boolean restore = true;
    try {
      try (PreparedStatement statement =
              keyed(
                  client,
                  "SELECT 1 FROM delivery_holds WHERE provider=? AND account_id=? AND event_id=?"
                      + " FOR UPDATE",
                  input,
                  false);
          ResultSet result = statement.executeQuery()) {
        require(result.next(), "Reconciliation requires a durable hold");
      }
      try (PreparedStatement statement =
              keyed(
                  client,
                  "SELECT payload_fingerprint FROM orders WHERE provider=? AND account_id=? AND"
                      + " event_id=? FOR UPDATE",
                  input,
                  false);
          ResultSet result = statement.executeQuery()) {
        if (!result.next() || !fingerprint(input).equals(result.getString(1)) || result.next()) {
          throw new IllegalStateException("legacy-evidence-insufficient-keep-held");
        }
      }
      try (PreparedStatement statement =
          keyed(
              client,
              "INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint) VALUES"
                  + " (?,?,?,?) ON CONFLICT DO NOTHING",
              input,
              true)) {
        statement.executeUpdate();
      }
      checkReceipt(client, input);
      try (PreparedStatement statement =
          keyed(
              client,
              "DELETE FROM delivery_holds WHERE provider=? AND account_id=? AND event_id=?",
              input,
              false)) {
        equal(statement.executeUpdate(), 1);
      }
      client.commit();
      trace("trusted-orphan-reconciled-hold-released", client, input, Map.of());
    } catch (Exception failure) {
      restore = rollback(client, failure);
      throw failure;
    } finally {
      if (restore) client.setAutoCommit(true);
    }
  }

  private void waitForContention(int waiter, int winner) throws Exception {
    long deadline = System.nanoTime() + Duration.ofSeconds(5).toNanos();
    while (System.nanoTime() < deadline) {
      try (PreparedStatement statement =
          observer.prepareStatement(
              "SELECT wait_event_type, wait_event, pg_blocking_pids(pid) AS blockers FROM"
                  + " pg_stat_activity WHERE pid=?")) {
        statement.setInt(1, waiter);
        try (ResultSet result = statement.executeQuery()) {
          if (result.next()) {
            java.sql.Array array = result.getArray("blockers");
            List<Integer> blockers = new ArrayList<>();
            try {
              Object values = array.getArray();
              for (int index = 0; index < java.lang.reflect.Array.getLength(values); index++) {
                blockers.add(((Number) java.lang.reflect.Array.get(values, index)).intValue());
              }
            } finally {
              array.free();
            }
            if ("Lock".equals(result.getString("wait_event_type")) && blockers.contains(winner)) {
              Map<String, Object> record = new LinkedHashMap<>();
              record.put("action", "real-database-contention");
              record.put("pid", waiter);
              record.put("winner", winner);
              record.put("wait_event_type", "Lock");
              record.put("wait_event", result.getString("wait_event"));
              record.put("blockers", blockers);
              System.out.println(JSON.writeValueAsString(record));
              return;
            }
          }
        }
      }
      Thread.sleep(10);
    }
    throw new IllegalStateException("competitor-never-observed-blocking-on-winner");
  }

  private static void await(CountDownLatch latch) throws Exception {
    if (!latch.await(7, TimeUnit.SECONDS))
      throw new IllegalStateException("Timed out awaiting transaction boundary");
  }

  private static Outcome outcome(Connection client, Hook hook) {
    try {
      return new Outcome(fixed(client, EVENT, hook), null);
    } catch (Exception failure) {
      return new Outcome(null, failure);
    }
  }

  private void overlap(boolean winnerRollsBack) throws Exception {
    ExecutorService workers = Executors.newFixedThreadPool(2);
    CountDownLatch claimed = new CountDownLatch(1);
    CountDownLatch release = new CountDownLatch(1);
    try (Connection winner = connect("winner");
        Connection waiter = connect("waiter")) {
      int winnerPid = pid(winner), waiterPid = pid(waiter);
      require(winnerPid != waiterPid, "Independent database backends");
      CompletableFuture<Outcome> first =
          CompletableFuture.supplyAsync(
              () ->
                  outcome(
                      winner,
                      boundary -> {
                        if (!boundary.equals("afterClaim")) return;
                        claimed.countDown();
                        await(release);
                        if (winnerRollsBack)
                          throw new IllegalStateException("injected:winner-rollback");
                      }),
              workers);
      CompletableFuture<Outcome> second = null;
      try {
        await(claimed);
        assertCounts(0, 0, EVENT);
        second = CompletableFuture.supplyAsync(() -> outcome(waiter, NO_FAILURE), workers);
        waitForContention(waiterPid, winnerPid);
      } finally {
        release.countDown();
        // Join while connections remain open, including failure paths.
        Outcome a = first.get(12, TimeUnit.SECONDS);
        Outcome b = second == null ? null : second.get(12, TimeUnit.SECONDS);
        if (winnerRollsBack)
          require(
              a.failure() != null && a.failure().getMessage().contains("winner-rollback"),
              "Winner rollback");
        else {
          equal(a.failure(), null);
          equal(a.acknowledgment(), ACK);
        }
        require(b != null, "Waiter started");
        equal(b.failure(), null);
        equal(b.acknowledgment(), ACK);
      }
      assertCounts(1, 1, EVENT);
    } finally {
      release.countDown();
      workers.shutdownNow();
      if (!workers.awaitTermination(15, TimeUnit.SECONDS))
        throw new IllegalStateException("Transaction workers did not stop");
    }
  }

  private void verifyFixture() throws Exception {
    try (Statement statement = observer.createStatement();
        ResultSet result =
            statement.executeQuery(
                "SELECT current_database(), current_user, shobj_description(oid,'pg_database') FROM"
                    + " pg_database WHERE datname=current_database()")) {
      require(result.next(), "Database identity");
      equal(result.getString(1), "codex_incident_test");
      equal(result.getString(2), "codex_incident_test");
      equal(result.getString(3), "codex-synthetic-incident-fixture-v1");
    }
    String version;
    try (Statement statement = observer.createStatement();
        ResultSet result = statement.executeQuery("SHOW server_version")) {
      require(result.next(), "Database version");
      version = result.getString(1);
      equal(version, "17.6 (Debian 17.6-2.pgdg12+1)");
    }
    try (Statement statement = observer.createStatement();
        ResultSet result = statement.executeQuery("SELECT pg_try_advisory_lock(14014)")) {
      require(result.next() && result.getBoolean(1), "Exclusive synthetic fixture lease");
    }
    emit(
        "fixture-environment",
        Map.of(
            "java",
            System.getProperty("java.version"),
            "pg",
            version,
            "mode",
            mode,
            "event_source",
            "canonical-sanitized-incident-record"));
  }

  private void createSchema() throws Exception {
    execute(observer, "DROP SCHEMA IF EXISTS incident_rehearsal CASCADE");
    execute(observer, "CREATE SCHEMA incident_rehearsal");
    execute(observer, "SET search_path TO incident_rehearsal, public");
    execute(
        observer,
        "CREATE TABLE event_receipts(provider text NOT NULL,account_id text NOT NULL,event_id text"
            + " NOT NULL,payload_fingerprint text NOT NULL,CONSTRAINT event_receipts_identity"
            + " UNIQUE(provider,account_id,event_id) NOT DEFERRABLE)");
    execute(
        observer,
        "CREATE TABLE orders(id bigserial PRIMARY KEY,provider text NOT NULL,account_id text NOT"
            + " NULL,event_id text NOT NULL,payload_fingerprint text)");
    execute(
        observer,
        "CREATE TABLE delivery_holds(provider text NOT NULL,account_id text NOT NULL,event_id text"
            + " NOT NULL,PRIMARY KEY(provider,account_id,event_id))");
    try (Statement statement = observer.createStatement();
        ResultSet result =
            statement.executeQuery(
                "SELECT condeferrable,pg_get_constraintdef(oid) FROM pg_constraint WHERE"
                    + " conrelid='incident_rehearsal.event_receipts'::regclass AND"
                    + " conname='event_receipts_identity'")) {
      require(result.next(), "Receipt uniqueness");
      equal(result.getBoolean(1), false);
      emit(
          "receipt-schema",
          Map.of(
              "conname",
              "event_receipts_identity",
              "condeferrable",
              result.getBoolean(1),
              "definition",
              result.getString(2)));
    }
  }

  private int run() throws Exception {
    Map<String, Checked> tests = new LinkedHashMap<>();
    tests.put(
        "retry after the order boundary leaves exactly one order and one receipt",
        () -> {
          try (Connection client = connect("regression")) {
            rejects(
                () -> {
                  if (mode.equals("baseline")) baseline(client, EVENT, failAt("afterOrder"));
                  else fixed(client, EVENT, failAt("afterOrder"));
                },
                "injected:afterOrder");
            assertCounts(mode.equals("baseline") ? 1 : 0, 0, EVENT);
            equal(
                mode.equals("baseline")
                    ? baseline(client, EVENT, NO_FAILURE)
                    : fixed(client, EVENT, NO_FAILURE),
                ACK);
            assertCounts(
                1, 1, EVENT); // Baseline deliberately fails here, after exposing two orders.
          }
        });
    if (mode.equals("fixed")) {
      tests.put(
          "first delivery and committed duplicate return the exact acknowledgment",
          () -> {
            try (Connection client = connect("duplicate")) {
              equal(fixed(client, EVENT, NO_FAILURE), ACK);
              equal(fixed(client, EVENT, NO_FAILURE), ACK);
              assertCounts(1, 1, EVENT);
            }
          });
      for (String boundary : List.of("beforeClaim", "afterClaim", "afterOrder")) {
        tests.put(
            "failure " + boundary + " rolls back and remains retryable",
            () -> {
              try (Connection client = connect("failure-" + boundary)) {
                rejects(() -> fixed(client, EVENT, failAt(boundary)), "injected:" + boundary);
                assertCounts(0, 0, EVENT);
                equal(fixed(client, EVENT, NO_FAILURE), ACK);
                assertCounts(1, 1, EVENT);
              }
            });
      }
      tests.put(
          "lost acknowledgment after commit does not duplicate the order",
          () -> {
            try (Connection client = connect("lost-ack")) {
              rejects(() -> fixed(client, EVENT, failAt("afterCommit")), "injected:afterCommit");
              assertCounts(1, 1, EVENT);
              equal(fixed(client, EVENT, NO_FAILURE), ACK);
              assertCounts(1, 1, EVENT);
            }
          });
      tests.put("real overlapping duplicate contention: winner commit", () -> overlap(false));
      tests.put("real overlapping duplicate contention: winner rollback", () -> overlap(true));
      tests.put(
          "event, account, and provider scope remain independent; conflicting payload is rejected",
          () -> {
            try (Connection client = connect("identity")) {
              for (IncidentEvent input :
                  List.of(
                      EVENT,
                      new IncidentEvent(
                          EVENT.provider(), EVENT.accountId(), "evt_demo_043", EVENT.payload()),
                      new IncidentEvent(
                          EVENT.provider(), "acct_demo_02", EVENT.eventId(), EVENT.payload()),
                      new IncidentEvent(
                          "synthetic-other",
                          EVENT.accountId(),
                          EVENT.eventId(),
                          EVENT.payload()))) {
                equal(fixed(client, input, NO_FAILURE), ACK);
                assertCounts(1, 1, input);
              }
              rejects(() -> fixed(client, changedPayload(), NO_FAILURE), "payload-conflict");
              assertCounts(1, 1, EVENT);
            }
          });
      tests.put(
          "legacy orphan is held before retry and reconciled only from trusted evidence",
          () -> {
            try (Connection client = connect("legacy-orphan")) {
              writeOrder(client, EVENT);
              assertCounts(1, 0, EVENT);
              equal(identifyAndHoldLegacyOrphans(client), 1);
              rejects(() -> fixed(client, EVENT, NO_FAILURE), "legacy-retry-held");
              assertCounts(1, 0, EVENT);
              rejects(() -> reconcileHeldOrphan(client, changedPayload()), "evidence-insufficient");
              rejects(() -> fixed(client, EVENT, NO_FAILURE), "legacy-retry-held");
              reconcileHeldOrphan(client, EVENT);
              equal(fixed(client, EVENT, NO_FAILURE), ACK);
              assertCounts(1, 1, EVENT);
            }
          });
      tests.put(
          "missing legacy payload evidence stays quarantined without a fabricated receipt",
          () -> {
            try (Connection client = connect("legacy-missing-evidence")) {
              try (PreparedStatement statement =
                  keyed(
                      client,
                      "INSERT INTO orders(provider,account_id,event_id) VALUES (?,?,?)",
                      EVENT,
                      false)) {
                statement.executeUpdate();
              }
              equal(identifyAndHoldLegacyOrphans(client), 1);
              rejects(() -> reconcileHeldOrphan(client, EVENT), "evidence-insufficient");
              rejects(() -> fixed(client, EVENT, NO_FAILURE), "legacy-retry-held");
              assertCounts(1, 0, EVENT);
            }
          });
    }
    int failures = 0, index = 0;
    for (Map.Entry<String, Checked> test : tests.entrySet()) {
      index++;
      try {
        execute(observer, "TRUNCATE orders,event_receipts,delivery_holds RESTART IDENTITY");
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
    return failures;
  }

  private static IncidentEvent changedPayload() {
    return new IncidentEvent(
        EVENT.provider(),
        EVENT.accountId(),
        EVENT.eventId(),
        new Payload(EVENT.payload().type(), EVENT.payload().orderId(), 9999));
  }

  public static void main(String[] args) throws Exception {
    if (args.length > 1) throw new IllegalArgumentException("Usage: baseline|regression|fixed");
    String mode = args.length == 0 ? "fixed" : args[0];
    if (!List.of("baseline", "regression", "fixed").contains(mode))
      throw new IllegalArgumentException("Unknown incident mode");
    EVENT =
        parseIncidentEvent(
            java.nio.file.Files.readString(java.nio.file.Path.of(INCIDENT_EVENT_FILE)));
    int failures;
    try (Connection observer = connect("observer")) {
      CodexCloudIncidentToTestedFix suite = new CodexCloudIncidentToTestedFix(observer, mode);
      suite.verifyFixture(); // No schema mutation before all identity and lease checks pass.
      try {
        suite.createSchema();
        failures = suite.run();
      } finally {
        execute(observer, "DROP SCHEMA IF EXISTS incident_rehearsal CASCADE");
        execute(observer, "SELECT pg_advisory_unlock(14014)");
      }
    }
    if (failures != 0) System.exit(1);
  }
}
```

```csharp
using System.Data;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;
using Npgsql;

namespace OpenAI.Docs.Examples.CodexCloud.IncidentToTestedFix;

internal static class IncidentToTestedFixSample
{
    // The entry point targets only a marked disposable PostgreSQL fixture.
    // A native scenario adapter can call RunModeAsync("baseline"|"regression"|"fixed").
    internal static Task RunAsync() => RunModeAsync("fixed");

    internal static string ParseMode(string[] arguments) => arguments.Length == 1 &&
        arguments[0] is "baseline" or "regression" or "fixed"
            ? arguments[0]
            : throw new ArgumentException("Expected exactly one mode: baseline, regression, or fixed.", nameof(arguments));

    internal sealed record Payload(string type, string orderId, [property: JsonRequired] int amountCents);
    internal sealed record Incident(string provider, string accountId, string eventId, Payload payload);
    private sealed record Acknowledgment(int status, object body);
    private const string FixtureRelativePath = "../../typescript-examples/codex-cloud/incident-to-tested-fix/incidents/INC-DEMO-014/order-created.sanitized.json";

    internal static string ResolveInputPath(string sourceFile, string relativePath) =>
        Path.GetFullPath(Path.Combine(Path.GetDirectoryName(sourceFile)!, relativePath));

    internal static Incident LoadInput([System.Runtime.CompilerServices.CallerFilePath] string sourceFile = "")
    {
        string owned = Path.Combine("codex-cloud", "incident-to-tested-fix", "incidents", "INC-DEMO-014", "order-created.sanitized.json");
        return ParseInput(File.ReadAllText(File.Exists(owned) ? owned : ResolveInputPath(sourceFile, FixtureRelativePath)));
    }

    private static readonly JsonSerializerOptions InputJsonOptions = new()
    { UnmappedMemberHandling = JsonUnmappedMemberHandling.Disallow };

    internal static Incident ParseInput(string json)
    {
        Incident? input = JsonSerializer.Deserialize<Incident>(json, InputJsonOptions);
        if (input is null || string.IsNullOrWhiteSpace(input.provider) ||
            string.IsNullOrWhiteSpace(input.accountId) || string.IsNullOrWhiteSpace(input.eventId) ||
            input.payload is null || string.IsNullOrWhiteSpace(input.payload.type) ||
            string.IsNullOrWhiteSpace(input.payload.orderId) || input.payload.amountCents < 0)
            throw new FormatException("Invalid sanitized incident fixture.");
        return input;
    }
    private static readonly Acknowledgment Ack = new(200, new { received = true });
    internal static string Fingerprint(Incident input) => Convert.ToHexStringLower(SHA256.HashData(
        JsonSerializer.SerializeToUtf8Bytes(new object[] { input.payload.type, input.payload.orderId, input.payload.amountCents })));
    internal static object[] Key(Incident input) => [input.provider, input.accountId, input.eventId];
    internal static object[] Values(Incident input) => [.. Key(input), Fingerprint(input)];

    private static void Trace(string action, NpgsqlConnection client, Incident input, object? details = null)
    {
        Dictionary<string, object?> value = new(StringComparer.Ordinal)
        { ["action"] = action, ["pid"] = client.ProcessID, ["key"] = Key(input) };
        if (details is not null)
            foreach (var property in JsonSerializer.SerializeToElement(details).EnumerateObject())
                value.Add(property.Name, property.Value.Clone());
        Console.WriteLine(JsonSerializer.Serialize(value));
    }

    private static NpgsqlCommand Command(NpgsqlConnection client, string sql, object[]? values = null,
        NpgsqlTransaction? transaction = null)
    {
        NpgsqlCommand command = new(sql, client, transaction) { CommandTimeout = 8 };
        // Empty parameter names select Npgsql's positional $1, $2, ... binding.
        foreach (object value in values ?? []) command.Parameters.Add(new NpgsqlParameter { Value = value });
        return command;
    }
    private static async Task<int> Execute(NpgsqlConnection client, string sql, object[]? values = null,
        NpgsqlTransaction? transaction = null)
    {
        await using NpgsqlCommand command = Command(client, sql, values, transaction);
        return await command.ExecuteNonQueryAsync();
    }
    private static async Task<object?> Scalar(NpgsqlConnection client, string sql, object[]? values = null,
        NpgsqlTransaction? transaction = null)
    {
        await using NpgsqlCommand command = Command(client, sql, values, transaction);
        return await command.ExecuteScalarAsync();
    }
    private static void Require(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
    private static async Task Reject(Func<Task> action, string message)
    {
        try { await action(); }
        catch (InvalidOperationException error) when (error.Message == message) { return; }
        throw new InvalidOperationException("Expected failure: " + message);
    }
    private static Func<string, Task> FailAt(string point) => boundary =>
        boundary == point ? Task.FromException(new InvalidOperationException("injected:" + point)) : Task.CompletedTask;

    private static async Task WriteOrder(NpgsqlConnection client, Incident input, NpgsqlTransaction? transaction = null)
    {
        await Execute(client,
            "INSERT INTO orders(provider,account_id,event_id,payload_fingerprint) VALUES ($1,$2,$3,$4)", Values(input), transaction);
        Trace("order-written", client, input);
    }
    private static async Task CheckReceipt(NpgsqlConnection client, Incident input, NpgsqlTransaction? transaction = null)
    {
        object? value = await Scalar(client,
            "SELECT payload_fingerprint FROM event_receipts WHERE provider=$1 AND account_id=$2 AND event_id=$3", Key(input), transaction);
        Require(value is string, "missing-receipt-after-skipped-claim");
        Require((string)value! == Fingerprint(input), "payload-conflict");
    }

    // Deliberate legacy defect: its first commit survives the injected failure.
    private static async Task<Acknowledgment> Baseline(NpgsqlConnection client, Incident input, Func<string, Task>? hook = null)
    {
        hook ??= _ => Task.CompletedTask;
        if (await Scalar(client, "SELECT 1 FROM event_receipts WHERE provider=$1 AND account_id=$2 AND event_id=$3", Key(input)) is not null)
        {
            await CheckReceipt(client, input);
            return Ack;
        }
        await using (NpgsqlTransaction transaction = await client.BeginTransactionAsync(IsolationLevel.ReadCommitted))
        {
            await WriteOrder(client, input, transaction);
            await transaction.CommitAsync();
        }
        Trace("legacy-order-committed-without-receipt", client, input);
        await hook("afterOrder");
        await Execute(client, "INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint) VALUES ($1,$2,$3,$4)", Values(input));
        Trace("legacy-receipt-committed", client, input);
        return Ack;
    }

    private static async Task<Acknowledgment> Fixed(NpgsqlConnection client, Incident input, Func<string, Task>? hook = null)
    {
        hook ??= _ => Task.CompletedTask;
        if (await Scalar(client, "SELECT 1 FROM delivery_holds WHERE provider=$1 AND account_id=$2 AND event_id=$3", Key(input)) is not null)
        {
            Trace("legacy-retry-held-no-ack", client, input);
            throw new InvalidOperationException("legacy-retry-held");
        }
        await hook("beforeClaim");
        await using NpgsqlTransaction transaction = await client.BeginTransactionAsync(IsolationLevel.ReadCommitted);
        bool committed = false;
        try
        {
            object? claimed = await Scalar(client, """
                INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint)
                VALUES ($1,$2,$3,$4) ON CONFLICT (provider,account_id,event_id)
                DO NOTHING RETURNING event_id
                """, Values(input), transaction);
            Trace("receipt-claim-result", client, input, new { inserted = claimed is not null });
            if (claimed is not null)
            {
                await hook("afterClaim");
                await WriteOrder(client, input, transaction);
                await hook("afterOrder");
            }
            else
            {
                // A new READ COMMITTED statement sees the committed winner.
                await CheckReceipt(client, input, transaction);
            }
            await transaction.CommitAsync();
            committed = true;
            Trace("transaction-committed", client, input);
            await hook("afterCommit");
            Trace("acknowledged", client, input, Ack);
            return Ack;
        }
        catch (Exception failure)
        {
            if (!committed)
            {
                try { await transaction.RollbackAsync(); }
                catch (Exception rollbackFailure)
                { throw new AggregateException("Transaction failed and rollback could not be confirmed", failure, rollbackFailure); }
                Trace("transaction-rolled-back-no-ack", client, input);
            }
            else Trace("committed-response-lost-no-ack", client, input);
            throw;
        }
    }

    // Run with ingestion paused and legacy consumers drained. This durable hold
    // models an operator-controlled quarantine, not a production migration.
    private static async Task<int> HoldOrphans(NpgsqlConnection client)
    {
        int held = await Execute(client, """
            INSERT INTO delivery_holds(provider,account_id,event_id)
            SELECT DISTINCT o.provider,o.account_id,o.event_id FROM orders o
            WHERE NOT EXISTS (SELECT 1 FROM event_receipts r
                WHERE r.provider=o.provider AND r.account_id=o.account_id AND r.event_id=o.event_id)
            ON CONFLICT DO NOTHING
            """);
        Console.WriteLine(JsonSerializer.Serialize(new { action = "pre-resume-orphans-held", keys = held }));
        return held;
    }
    private static async Task Reconcile(NpgsqlConnection client, Incident input)
    {
        await using NpgsqlTransaction transaction = await client.BeginTransactionAsync(IsolationLevel.ReadCommitted);
        try
        {
            Require(await Scalar(client, "SELECT 1 FROM delivery_holds WHERE provider=$1 AND account_id=$2 AND event_id=$3 FOR UPDATE",
                Key(input), transaction) is not null, "reconciliation-requires-hold");
            List<string?> fingerprints = [];
            await using (NpgsqlCommand command = Command(client,
                "SELECT payload_fingerprint FROM orders WHERE provider=$1 AND account_id=$2 AND event_id=$3 FOR UPDATE", Key(input), transaction))
            await using (NpgsqlDataReader reader = await command.ExecuteReaderAsync())
                while (await reader.ReadAsync()) fingerprints.Add(reader.IsDBNull(0) ? null : reader.GetString(0));
            Require(fingerprints.Count == 1 && fingerprints[0] == Fingerprint(input), "legacy-evidence-insufficient-keep-held");
            await Execute(client, """
                INSERT INTO event_receipts(provider,account_id,event_id,payload_fingerprint) VALUES ($1,$2,$3,$4)
                ON CONFLICT DO NOTHING
                """, Values(input), transaction);
            await CheckReceipt(client, input, transaction);
            await Execute(client, "DELETE FROM delivery_holds WHERE provider=$1 AND account_id=$2 AND event_id=$3", Key(input), transaction);
            await transaction.CommitAsync();
            Trace("trusted-orphan-reconciled-hold-released", client, input);
        }
        catch (Exception failure)
        {
            try { await transaction.RollbackAsync(); }
            catch (Exception rollbackFailure)
            { throw new AggregateException("Reconciliation failed and rollback could not be confirmed", failure, rollbackFailure); }
            throw;
        }
    }
    private static async Task Counts(NpgsqlConnection observer, int orders, int receipts, Incident input)
    {
        await using NpgsqlCommand command = Command(observer, """
            SELECT (SELECT count(*)::integer FROM orders WHERE provider=$1 AND account_id=$2 AND event_id=$3),
                (SELECT count(*)::integer FROM event_receipts WHERE provider=$1 AND account_id=$2 AND event_id=$3)
            """, Key(input));
        await using NpgsqlDataReader reader = await command.ExecuteReaderAsync();
        Require(await reader.ReadAsync(), "Missing committed-state counts");
        int actualOrders = reader.GetInt32(0), actualReceipts = reader.GetInt32(1);
        Trace("committed-state", observer, input, new { orders = actualOrders, receipts = actualReceipts });
        Require(actualOrders == orders && actualReceipts == receipts,
            $"Expected {orders} order(s)/{receipts} receipt(s); got {actualOrders}/{actualReceipts}");
    }
    private static void Acknowledged(Acknowledgment value) => Require(
        JsonSerializer.Serialize(value) == "{\"status\":200,\"body\":{\"received\":true}}", "Exact delivery acknowledgment");

    internal static async Task RunModeAsync(string mode)
    {
        if (mode is not ("baseline" or "regression" or "fixed")) throw new ArgumentException("Expected baseline, regression, or fixed", nameof(mode));
        Incident original = LoadInput();
        string password = Environment.GetEnvironmentVariable("CODEX_INCIDENT_DB_PASSWORD")
            ?? throw new InvalidOperationException("Set CODEX_INCIDENT_DB_PASSWORD to the disposable fixture password");
        NpgsqlConnectionStringBuilder configuration = new()
        {
            Host = "127.0.0.1",
            Port = 55432,
            Username = "codex_incident_test",
            Database = "codex_incident_test",
            Password = password,
            Timeout = 5,
            CommandTimeout = 8,
            Pooling = false,
            ApplicationName = "csharp-incident-rehearsal"
        };
        await using NpgsqlConnection observer = new(configuration.ConnectionString);
        await observer.OpenAsync();
        // Verify all fixture identity evidence before creating or changing any DB object.
        await using (NpgsqlCommand identity = Command(observer, """
            SELECT current_database(),current_user,shobj_description(oid,'pg_database'),current_setting('server_version')
            FROM pg_database WHERE datname=current_database()
            """))
        await using (NpgsqlDataReader reader = await identity.ExecuteReaderAsync())
        {
            Require(await reader.ReadAsync() && reader.GetString(0) == "codex_incident_test" &&
                reader.GetString(1) == "codex_incident_test" && !reader.IsDBNull(2) &&
                reader.GetString(2) == "codex-synthetic-incident-fixture-v1" &&
                reader.GetString(3) == "17.6 (Debian 17.6-2.pgdg12+1)", "Refusing an unmarked or unexpected database fixture");
            Console.WriteLine(JsonSerializer.Serialize(new
            {
                action = "fixture-environment",
                mode,
                runtime = System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription,
                pg = reader.GetString(3)
            }));
        }
        string schema = "incident_rehearsal_" + Guid.NewGuid().ToString("N");
        // The generated identifier is hex only; external input never enters this SQL.
        await Execute(observer, $"CREATE SCHEMA {schema}");
        List<NpgsqlConnection> clients = [];
        int tests = 0, failures = 0;
        try
        {
            await Execute(observer, $"SET search_path TO {schema},public");
            await Execute(observer, """
                CREATE TABLE event_receipts (
                    provider text NOT NULL, account_id text NOT NULL, event_id text NOT NULL,
                    payload_fingerprint text NOT NULL,
                    CONSTRAINT event_receipts_identity UNIQUE(provider,account_id,event_id) NOT DEFERRABLE);
                CREATE TABLE orders (id bigserial PRIMARY KEY, provider text NOT NULL,
                    account_id text NOT NULL, event_id text NOT NULL, payload_fingerprint text);
                CREATE TABLE delivery_holds (provider text NOT NULL, account_id text NOT NULL,
                    event_id text NOT NULL, PRIMARY KEY(provider,account_id,event_id));
                """);
            Require(await Scalar(observer, """
                SELECT NOT condeferrable FROM pg_constraint
                WHERE conname='event_receipts_identity' AND conrelid='event_receipts'::regclass
                """) is true, "Receipt uniqueness must be nondeferrable");
            async Task<NpgsqlConnection> Connect()
            {
                NpgsqlConnection client = new(configuration.ConnectionString);
                clients.Add(client);
                await client.OpenAsync();
                await Execute(client, $"SET search_path TO {schema},public");
                await Execute(client, "SET statement_timeout = '8s'");
                return client;
            }
            async Task Case(string name, Func<NpgsqlConnection, Task> test)
            {
                tests++;
                try
                {
                    await Execute(observer, "TRUNCATE orders,event_receipts,delivery_holds RESTART IDENTITY");
                    NpgsqlConnection client = await Connect();
                    try { await test(client); }
                    finally { await client.DisposeAsync(); clients.Remove(client); }
                    Console.WriteLine($"ok {tests} - {name}");
                }
                catch (Exception error)
                {
                    failures++;
                    Console.WriteLine($"not ok {tests} - {name}");
                    Console.WriteLine("# " + error.ToString().Replace("\r", "").Replace("\n", "\n# "));
                }
            }
            await Case("retry after the order boundary leaves exactly one order and one receipt", async client =>
            {
                async Task<Acknowledgment> Handle(Func<string, Task>? hook = null) => mode == "baseline"
                    ? await Baseline(client, original, hook) : await Fixed(client, original, hook);
                await Reject(async () => { await Handle(FailAt("afterOrder")); }, "injected:afterOrder");
                await Counts(observer, mode == "baseline" ? 1 : 0, 0, original);
                Acknowledged(await Handle());
                await Counts(observer, 1, 1, original);
            });
            if (mode == "fixed")
            {
                await Case("first delivery and committed duplicate return the exact acknowledgment", async client =>
                {
                    Acknowledged(await Fixed(client, original));
                    Acknowledged(await Fixed(client, original));
                    await Counts(observer, 1, 1, original);
                });
                foreach (string boundary in new[] { "beforeClaim", "afterClaim", "afterOrder" })
                    await Case("failure " + boundary + " rolls back and remains retryable", async client =>
                    {
                        await Reject(async () => { await Fixed(client, original, FailAt(boundary)); }, "injected:" + boundary);
                        await Counts(observer, 0, 0, original);
                        Acknowledged(await Fixed(client, original));
                        await Counts(observer, 1, 1, original);
                    });
                await Case("lost acknowledgment after commit does not duplicate the order", async client =>
                {
                    await Reject(async () => { await Fixed(client, original, FailAt("afterCommit")); }, "injected:afterCommit");
                    await Counts(observer, 1, 1, original);
                    Acknowledged(await Fixed(client, original));
                    await Counts(observer, 1, 1, original);
                });
                foreach (bool rollback in new[] { false, true })
                    await Case("real overlapping duplicate contention: winner " + (rollback ? "rollback" : "commit"), async winner =>
                    {
                        NpgsqlConnection waiter = await Connect();
                        try
                        {
                            Require(winner.ProcessID != waiter.ProcessID, "Contention requires independent backends");
                            TaskCompletionSource claimed = new(TaskCreationOptions.RunContinuationsAsynchronously);
                            TaskCompletionSource release = new(TaskCreationOptions.RunContinuationsAsynchronously);
                            Task<Acknowledgment> winnerTask = Fixed(winner, original, async boundary =>
                            {
                                if (boundary != "afterClaim") return;
                                claimed.TrySetResult();
                                await release.Task.WaitAsync(TimeSpan.FromSeconds(7));
                                if (rollback) throw new InvalidOperationException("injected:winner-rollback");
                            });
                            Task<Acknowledgment>? waiterTask = null;
                            try
                            {
                                await Task.WhenAny(claimed.Task, winnerTask).WaitAsync(TimeSpan.FromSeconds(5));
                                if (!claimed.Task.IsCompleted) { await winnerTask; throw new InvalidOperationException("Winner did not claim receipt"); }
                                await Counts(observer, 0, 0, original);
                                waiterTask = Fixed(waiter, original);
                                await WaitForContention(observer, waiter, winner, original);
                            }
                            finally
                            {
                                release.TrySetResult();
                                // Observe both outcomes even when the first assertion fails.
                                await Task.WhenAll(
                                    ObserveWinner(winnerTask, rollback),
                                    waiterTask is null ? Task.CompletedTask : ObserveWaiter(waiterTask));
                            }
                            await Counts(observer, 1, 1, original);
                        }
                        finally { await waiter.DisposeAsync(); clients.Remove(waiter); }
                    });
                await Case("event, account, and provider identity; conflicting payload rejected", async client =>
                {
                    foreach (Incident input in new[] { original, original with { eventId = "evt_demo_043" },
                        original with { accountId = "acct_demo_02" }, original with { provider = "synthetic-other" } })
                    {
                        Acknowledged(await Fixed(client, input));
                        await Counts(observer, 1, 1, input);
                    }
                    await Reject(async () => { await Fixed(client, original with { payload = original.payload with { amountCents = 9999 } }); }, "payload-conflict");
                    await Counts(observer, 1, 1, original);
                });
                await Case("legacy orphan held before retry and reconciled only from trusted evidence", async client =>
                {
                    await WriteOrder(client, original);
                    await Counts(observer, 1, 0, original);
                    Require(await HoldOrphans(client) == 1, "Hold the orphan before resuming ingestion");
                    await Reject(async () => { await Fixed(client, original); }, "legacy-retry-held");
                    await Reject(
            () => Reconcile(client, original with
            {
                payload = original.payload with { amountCents = 9999 },
            }),
            "legacy-evidence-insufficient-keep-held");
                    await Reject(async () => { await Fixed(client, original); }, "legacy-retry-held");
                    await Reconcile(client, original);
                    Acknowledged(await Fixed(client, original));
                    await Counts(observer, 1, 1, original);
                });
                await Case("missing legacy payload evidence stays quarantined", async client =>
                {
                    await Execute(client, "INSERT INTO orders(provider,account_id,event_id) VALUES ($1,$2,$3)", Key(original));
                    Require(await HoldOrphans(client) == 1, "Hold missing-evidence orphan");
                    await Reject(() => Reconcile(client, original), "legacy-evidence-insufficient-keep-held");
                    await Reject(async () => { await Fixed(client, original); }, "legacy-retry-held");
                    await Counts(observer, 1, 0, original);
                });
            }
            Require(tests == (mode == "fixed" ? 11 : 1), "All native incident scenarios must execute");
            Console.WriteLine($"1..{tests}\n# tests {tests}\n# pass {tests - failures}\n# fail {failures}\n# cancelled 0\n# skipped 0\n# todo 0");
        }
        finally
        {
            try
            {
                foreach (NpgsqlConnection client in clients) await client.DisposeAsync();
            }
            finally { await Execute(observer, $"DROP SCHEMA {schema} CASCADE"); }
        }
        if (failures != 0) throw new InvalidOperationException($"{failures} native incident regression(s) failed");
    }

    private static async Task ObserveWinner(Task<Acknowledgment> task, bool rollback)
    {
        if (rollback) await Reject(async () => { await task; }, "injected:winner-rollback");
        else Acknowledged(await task);
    }
    private static async Task ObserveWaiter(Task<Acknowledgment> task) => Acknowledged(await task);
    private static async Task WaitForContention(NpgsqlConnection observer, NpgsqlConnection waiter, NpgsqlConnection winner, Incident input)
    {
        Stopwatch elapsed = Stopwatch.StartNew();
        while (elapsed.Elapsed < TimeSpan.FromSeconds(5))
        {
            await using (NpgsqlCommand command = Command(observer, """
                SELECT wait_event_type,wait_event,pg_blocking_pids(pid)
                FROM pg_stat_activity WHERE pid=$1
                """, [waiter.ProcessID]))
            await using (NpgsqlDataReader reader = await command.ExecuteReaderAsync())
            {
                if (await reader.ReadAsync() && !reader.IsDBNull(0) && reader.GetString(0) == "Lock")
                {
                    int[] blockers = reader.GetFieldValue<int[]>(2);
                    if (blockers.Contains(winner.ProcessID))
                    {
                        Trace("real-database-contention", waiter, input, new
                        { winner = winner.ProcessID, wait_event_type = reader.GetString(0), wait_event = reader.GetString(1), blockers });
                        return;
                    }
                }
            }
            await Task.Delay(10);
        }
        throw new InvalidOperationException("competitor-never-observed-blocking-on-winner");
    }
}
```

```ruby
def self.fixed(client, input, hook = ->(_boundary) {})
  assert_not_held(client, input)
  hook.call("beforeClaim")
  client.exec("BEGIN ISOLATION LEVEL READ COMMITTED")
  committed = false
  begin
    claimed = client.exec_params(<<~SQL, key(input) + [fingerprint(input)])
      INSERT INTO event_receipts(provider, account_id, event_id, payload_fingerprint)
      VALUES ($1,$2,$3,$4)
      ON CONFLICT (provider, account_id, event_id) DO NOTHING RETURNING event_id
    SQL
    trace("receipt-claim-result", client, input, inserted: claimed.ntuples == 1)
    if claimed.ntuples == 1
      hook.call("afterClaim")
      write_order(client, input)
      hook.call("afterOrder")
    else
      # A new READ COMMITTED statement sees the winner after its commit.
      check_receipt(client, input)
    end
    client.exec("COMMIT")
    committed = true
    trace("transaction-committed", client, input)
    hook.call("afterCommit")
    trace("acknowledged", client, input, **ACK)
    ACK
  rescue
    if committed
      trace("committed-response-lost-no-ack", client, input)
    else
      client.exec("ROLLBACK")
      trace("transaction-rolled-back-no-ack", client, input)
    end
    raise
  end
end
```

</details>

### 1. Provide a compact packet

Use these files as the packet outline:

```text
incidents/INC-DEMO-014/incident.md
incidents/INC-DEMO-014/logs.ndjson
incidents/INC-DEMO-014/release.json
incidents/INC-DEMO-014/order-created.sanitized.json
```

In this scenario, `release.json` identifies the example release SHA `4a1c9e7d2b6f8a0c3d5e7f9012a4b6c8d0e2f413`, deployed at `2026-09-22T11:58:00Z`. The incident window is `12:03:00Z–12:05:00Z` on the same day. The packet reports two internal orders associated with one provider event. When preparing your own packet, include confirmed impact counts and identify any estimates.

The sanitized logs contain these correlated observations:

| UTC time     | Correlation                                                                              | Observation                                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 12:03:04.110 | Event `evt_demo_042`, account `acct_demo_01`, request `req_demo_a`, trace `trace_demo_a` | First delivery enters the webhook handler.                                                                                   |
| 12:03:04.145 | Same event and first trace                                                               | Order `ord_demo_101` is committed.                                                                                           |
| 12:03:04.150 | Same worker                                                                              | Worker exits before a receipt-write success or response is recorded. The excerpt alone does not prove the receipt is absent. |
| 12:03:14.203 | Same provider/account/event, request `req_demo_b`, trace `trace_demo_b`                  | A retry enters the handler. The handler logs that no matching receipt was found.                                             |
| 12:03:14.241 | Same event and second trace                                                              | Order `ord_demo_102` is committed and a receipt is recorded.                                                                 |

Keep a stable event ID across deliveries and distinct request and trace IDs per delivery. A per-request identifier would hide the relationship between the retry and the original event.

### 2. Trace the evidence and test the hypothesis

The incident report proposes that a retry storm caused the duplicate. Codex should treat that as a hypothesis. Two observed deliveries do not establish a storm, and retries are a normal condition a webhook handler must tolerate.

In the sample’s affected implementation, source inspection reveals this sequence: look up a receipt, commit the order, then write the receipt in a separate transaction. The gap between the two commits is a stronger explanation. A worker failure in that gap can leave an order without a receipt, so a retry can create another order. Concurrent deliveries can also both pass a separate check before either writes its receipt.

Have Codex trace the actual handler and transaction boundaries and cite the relevant lines. It should confirm the packet's release matches the code under test, or explain why testing a different commit limits the conclusion.

### 3. Reproduce before changing the handler

Add a regression test using the sample webhook and the isolated PostgreSQL database. Put a test-only failure hook immediately after the order write and before the receipt-write step in the original handler.

Confirm from the real transaction boundaries that the original order has committed at that point. Retry the same provider/account/event and assert exactly one order and one matching receipt; the seeded implementation should fail with two orders.

After the fix, exercise the corresponding hook after the order statement but before the shared transaction commits; the failed attempt must leave zero orders and zero receipts.

Retry and assert one of each. Keep the same business assertion across revisions and record the hook location on each revision.

Run the new test on the original implementation first. For the seeded defect in this sample, the expected failure is two orders instead of one. Save the command, starting commit, exit code, and assertion output. If that failure does not occur, investigate the mismatch before editing the handler.

An injected exception exercises the application's transaction behavior. Record that it does not reproduce every possible host, network, or database failure.

### 4. Make the smallest supported fix

For this specific defect, claim the event receipt and write the order within one transaction on one database connection. Use the existing unique key with `INSERT ... ON CONFLICT (provider, account_id, event_id) DO NOTHING RETURNING ...`.

Only the delivery that inserts the receipt may write the order; acknowledge success only after commit. A failed transaction rolls back both writes. Do not catch a uniqueness error and continue using an aborted transaction.

A competing delivery may wait for the first transaction. If the first commits, the second claim inserts nothing: issue a fresh SELECT under READ COMMITTED, verify the stored event identity/payload policy, and return the existing duplicate acknowledgment without writing an order.

If the first transaction rolls back, the competitor can claim and process the event. A missing receipt after a skipped insert, an identity conflict, or a transient database error must follow the documented retry/error path, not a fabricated success.

Under stricter isolation, serialization failures require the repository's bounded whole-transaction retry policy. See PostgreSQL's [INSERT conflict behavior](https://www.postgresql.org/docs/current/sql-insert.html) and [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

Neither an in-memory set nor a separate “check then insert” protects against concurrent workers or restarts. Scope the key to the provider's event-identity contract. If a supposedly identical event carries conflicting identity or payload information, surface that inconsistency rather than silently treating it as a valid duplicate.

The demo's business mutation is entirely within the same database. If the real handler also sends email, charges a card, or calls another service, this transaction alone does not make those external effects idempotent. Identify that boundary and the system's existing delivery or idempotency mechanism before expanding the fix.

### 5. Verify the changed behavior

Ask for both the original failure and the post-fix result. Use test-only hooks at named transaction boundaries and inspect committed state from a separate connection. The sample passes eleven local PostgreSQL tests; `test-evidence.md` in the download records those results and the checks still needed for Cloud execution and deployment. Run the suite in your published environment and test actual connection loss during commit before relying on that recovery path.

| Check / failure point                              | Required behavior                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| First delivery and committed duplicate             | The first creates one order and one receipt; a repeated event returns the agreed acknowledgment and leaves counts unchanged. Record exact status/body.                                                                                                                                                                              |
| Before receipt claim                               | Failure creates neither row and returns no success acknowledgment. A retry creates one of each.                                                                                                                                                                                                                                     |
| After claim, before order write                    | Failure rolls back the receipt; no order exists. A retry can claim and process normally.                                                                                                                                                                                                                                            |
| After order write, before commit                   | Failure rolls back both rows. This is the fixed-code counterpart of the original committed-order/missing-receipt defect; a retry leaves one of each.                                                                                                                                                                                |
| After commit, before acknowledgment                | Simulate a lost response. Both rows remain committed. A retry returns the duplicate acknowledgment without another order.                                                                                                                                                                                                           |
| Commit outcome unknown                             | Model a connection loss around commit separately from an ordinary exception. Return no unsupported success claim; a retry with the same stable event key must be safe whether the first transaction committed or rolled back. If this transport case was not exercised, mark it not run.                                            |
| Concurrent duplicate: first transaction commits    | Two independent connections/workers contend on the same event key. Hold the winner after claim; start the competitor before releasing it. Verify the competitor actually contends, then release the winner. Both complete through the expected acknowledgment path; exactly one order and one receipt exist.                        |
| Concurrent duplicate: first transaction rolls back | Repeat the controlled overlap, but fail the claimant before commit. The competitor claims after rollback and creates one order and one receipt. Check both responses and final state.                                                                                                                                               |
| Event identity and payload conflict                | Different events and the same event ID under different accounts/providers remain independent. For an event with the same scoped ID but a conflicting canonical payload, follow the agreed conflict path; do not create a second order or silently acknowledge different work.                                                       |
| Legacy order without receipt and pending retry     | Seed a committed legacy order without a receipt. Identify and hold its event key before retries resume. A held retry returns no success acknowledgment and creates no row. Trusted reconciliation permits the duplicate acknowledgment with one existing order and one receipt; missing or conflicting evidence keeps the key held. |
| Broader service checks                             | Run relevant integration tests, lint, and type checking. Separate new failures, pre-existing failures, and checks that could not run.                                                                                                                                                                                               |

Coordinate concurrency with barriers/latches and bounded timeouts, not sleeps or a bare pair of promises. Release blocked workers in test cleanup and use disposable fixtures. An exception test alone does not prove abrupt process death, transport loss, or production concurrency behavior.

The sample uses `node --experimental-strip-types main.ts baseline`, `node --experimental-strip-types main.ts regression`, and `node --experimental-strip-types main.ts` inside the pinned runner. Its structured output records transaction boundaries, committed row counts, acknowledgment status/body, and observed blocking backend IDs.

When adapting the workflow, use the commands actually defined by your repository and report their real results. A skipped check or unavailable dependency belongs in the handoff, with its impact on confidence.

## Review the handoff

### Shared evidence record

Use the incident workflow's evidence format for each acceptance criterion. Populate it from observed output; the fields below are a template, not passing results. For a new test that does not exist at baseline, distinguish “not yet present” from a failed existing check.

```text
Criterion / test: [specific behavior and test location]
Environment: [published setup reference; runtime, database and dependency versions]
Before: [revision + test-only diff ID; command; exit code; observed assertion; log path]
After: [final revision or base + diff ID; command; exit code; observed assertion; log path]
Status: [pass / fail / blocked / not run]
Limits / reviewer action: [untested behavior, blocker, or decision required]
```

Keep red and green runs tied to their actual tested states, including test-only changes on the original revision. Keep the logs, response fixtures, and final diff with the handoff. A changed final revision needs updated evidence; checks that were not run or were blocked cannot count as passing.

Ask Codex to leave the code diff and these review artifacts in the repository:

- `incident-investigation.md`: timeline, evidence references, hypotheses tested, supported cause, and remaining uncertainty.
- `test-evidence.md`: baseline commit, failing regression output, fix commit or diff, passing targeted checks, broader checks, and limitations.
- `pr-draft.md`: a concise explanation of the defect, changed behavior, test evidence, and remaining risk.
- `deployment-handoff.md`: verified schema/isolation/receipt-retention assumptions, named rollout owner, pre-deployment checks, duplicate-order and acknowledgment/error metrics, and the rollout/rollback gates below.

Before accepting the patch, verify that the original code fails the new test, the fix passes it, and the diff addresses the demonstrated defect. In the webhook example, inspect event-key scope, transaction boundaries, concurrency coverage, and any effects outside the transaction. Review existing duplicate orders separately; preventing new duplicates does not repair historical records.

### Plan deployment and rollback

A code patch protects only workers running the corrected handler. Old workers can still write an order before claiming a receipt, so a mixed-version canary is not evidence that the defect is eliminated.

The deployment owner must choose either a tested mixed-version strategy or an existing runbook that pauses ingestion, drains in-flight old workers, updates every consumer, and resumes retained deliveries without loss.

Confirm the provider/queue retry and retention behavior before choosing the latter; do not assume pausing is lossless.

Before resuming retained deliveries, identify committed legacy orders with no matching receipt. Pausing and draining old consumers prevents new legacy writes; it does not repair those existing orders. Hold every affected event key with the existing queue or quarantine procedure. If legacy records cannot establish a complete event identity, keep the affected deliveries or those from the affected time window paused for owner review rather than declaring the scan complete.

Reconcile a held key only when trusted immutable provider/account/event identity, canonical payload evidence, and the committed business record establish what already happened.

Under the approved reconciliation procedure, record the matching receipt without repeating the business mutation, then release that key's hold.

Keep affected keys quarantined for owner review when evidence is missing, payloads conflict, or multiple business records exist. A retry payload cannot substitute for trusted evidence of the original event when reconstructing its fingerprint.

The pre-resume gate passes only when each affected key is reconciled or its hold remains enforced across all consumers.

Seed a legacy order and its pending retry in staging. Verify the hold prevents another order and any success acknowledgment; after trusted reconciliation, the retry may receive the duplicate acknowledgment while the existing order count stays at one. Rehearse an unresolved case too: it must remain held without a fabricated receipt. Keep this gate in the deployment handoff alongside pause/drain, consumer-version, retention, and rollback checks.

Before rollout, verify the existing unique constraint is present and valid, the receipt key/payload policy is consistent across all consumers, receipt cleanup cannot reopen the replay window, and external effects remain outside this patch.

In staging, rehearse the selected sequence and failed-worker retry. Record the owner's observation window and stop thresholds for duplicate orders, webhook errors, acknowledgment latency, lock waits, and retry backlog; do not invent production thresholds.

Reverting to the old handler can reintroduce duplicate orders. The rollback handoff must name the containment step (for example, the approved pause/drain procedure), the safe revision, and the owner who decides when processing can resume. Preserve receipts; do not delete them to unblock retries. Historical duplicate orders require a separately reviewed remediation.

The engineer owns the deployment decision and any production remediation. A passing isolated test is evidence for review, not proof that production is healthy. Create the pull request, run your normal CI and review process, and deploy through your team's established controls after reviewing the draft.

## Continue in the same task

Use a focused follow-up to resolve uncertainty or improve the handoff:

```text
Review the patch against two concurrent deliveries and a retry after a worker failure. Show which behaviors the tests establish and which remain untested. Keep the change limited to this handler and its regression tests; update the handoff with any remaining risk.
```

If the first run could not reproduce the incident:

```text
Stop implementation. List the hypotheses the evidence rules out, the strongest remaining hypothesis, and the smallest additional sanitized input or isolated experiment needed to distinguish it. Keep the root cause unconfirmed.
```
