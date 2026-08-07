"""Offline tests for the codex-docs fetcher."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import fetch_codex_docs as fetcher  # noqa: E402


LLMS_SAMPLE = """# Codex

## Reference

- [ChatGPT desktop app commands](https://learn.chatgpt.com/docs/reference/commands.md): Reference
- [Command line options](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli): Options
- [Codex IDE extension commands](https://learn.chatgpt.com/docs/developer-commands.md?surface=ide): Reference
- [Codex IDE extension settings](https://learn.chatgpt.com/docs/developer-settings.md?surface=ide): Reference
- [Full manual](https://learn.chatgpt.com/docs/codex-manual.md): Aggregate export
- [Enterprise admin](https://learn.chatgpt.com/docs/enterprise/admin.md): Out of scope
- [Legacy host](https://developers.openai.com/codex/prompting.md): Redirects to /docs
- [Other product](https://example.com/docs/other.md): Different site
"""


def llms_paths(text: str) -> set[str]:
    """Mirror the fetcher's llms.txt parsing without performing any network I/O."""

    paths: set[str] = set()
    for match in re.finditer(r"\((https?://[^)\s]+?\.md)(?:\?[^)\s]*)?\)", text):
        from urllib.parse import urlparse

        parsed = urlparse(match.group(1))
        if parsed.netloc not in {"learn.chatgpt.com", "developers.openai.com"}:
            continue
        path = fetcher.normalize_path(parsed.path)
        if fetcher.is_codex_doc_url(f"{fetcher.DOCS_BASE_URL}{path}"):
            paths.add(path)
    return paths


def test_llms_parsing_keeps_query_variant_pages() -> None:
    """These pages are linked only as `?surface=` variants and are not in the sitemap."""

    paths = llms_paths(LLMS_SAMPLE)

    assert "/docs/developer-commands" in paths
    assert "/docs/developer-settings" in paths
    assert "/docs/reference/commands" in paths


def test_llms_parsing_collapses_surface_variants_to_one_page() -> None:
    assert len([path for path in llms_paths(LLMS_SAMPLE) if path.endswith("developer-commands")]) == 1


def test_llms_parsing_drops_aggregates_enterprise_and_other_sites() -> None:
    paths = llms_paths(LLMS_SAMPLE)

    assert "/docs/codex-manual" not in paths
    assert not any(path.startswith("/docs/enterprise") for path in paths)
    assert not any("other" in path for path in paths)


def test_legacy_host_links_are_mapped_onto_the_current_docs_path() -> None:
    assert "/docs/prompting" in llms_paths(LLMS_SAMPLE)


@pytest.mark.parametrize(
    "url",
    [
        "https://learn.chatgpt.com/docs",
        "https://learn.chatgpt.com/docs/hooks",
        "https://learn.chatgpt.com/docs/cli/features",
    ],
)
def test_keeps_documentation_urls(url: str) -> None:
    assert fetcher.is_codex_doc_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "https://learn.chatgpt.com/docs/enterprise/admin",
        "https://learn.chatgpt.com/docs/videos",
        "https://learn.chatgpt.com/docs/codex-manual",
        "https://learn.chatgpt.com/docs/llms-full",
        "https://learn.chatgpt.com/pricing",
        "https://example.com/docs/hooks",
        "https://learn.chatgpt.com/docs/hooks?surface=cli",
    ],
)
def test_drops_out_of_scope_urls(url: str) -> None:
    assert fetcher.is_codex_doc_url(url) is False


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/docs/hooks", "hooks.md"),
        ("/docs/cli/features", "cli__features.md"),
        ("/docs", "codex.md"),
        ("/docs/developer-commands", "developer-commands.md"),
    ],
)
def test_path_to_filename(path: str, expected: str) -> None:
    assert fetcher.path_to_filename(path) == expected


def test_normalize_path_strips_markdown_suffix_and_maps_legacy_prefix() -> None:
    assert fetcher.normalize_path("/docs/hooks.md") == "/docs/hooks"
    assert fetcher.normalize_path("/codex/prompting") == "/docs/prompting"
    assert fetcher.normalize_path("/codex") == "/docs"


def test_pages_from_paths_detects_slug_collisions() -> None:
    with pytest.raises(RuntimeError, match="Slug collision"):
        fetcher.pages_from_paths({"/docs/cli/features", "/docs/cli__features"})


def test_absolutize_links_rewrites_root_relative_and_legacy_targets() -> None:
    content = "See [config](/docs/config-basic) and [old](/codex/config-file/config-advanced#auto)."
    rewritten = fetcher.absolutize_links(content)

    assert "(https://learn.chatgpt.com/docs/config-basic)" in rewritten
    assert "(https://learn.chatgpt.com/docs/config-file/config-advanced#auto)" in rewritten


def test_absolutize_links_leaves_absolute_links_alone() -> None:
    content = "[docs](https://learn.chatgpt.com/docs/hooks)"
    assert fetcher.absolutize_links(content) == content


def test_absolutize_links_handles_labels_containing_brackets() -> None:
    content = "[`[auto_review].policy`](/codex/config-file/config-advanced#policy)"
    rewritten = fetcher.absolutize_links(content)

    assert (
        "(https://learn.chatgpt.com/docs/config-file/config-advanced#policy)"
        in rewritten
    )


def test_absolutize_links_leaves_protocol_relative_urls_alone() -> None:
    content = "[cdn](//cdn.example.com/asset.png)"
    assert fetcher.absolutize_links(content) == content


def test_clean_mdx_preserves_code_fences() -> None:
    raw = "# Hooks\n\n```bash\ncodex --help /docs/x\n```\n"
    cleaned = fetcher.clean_mdx(raw)

    assert "codex --help /docs/x" in cleaned


def test_yaml_quoted_preserves_non_ascii() -> None:
    assert fetcher.yaml_quoted("Semaine 26 · juin") == '"Semaine 26 · juin"'


def test_frontmatter_quotes_titles_with_colons() -> None:
    page = fetcher.CodexPage(
        url="https://learn.chatgpt.com/docs/hooks",
        path="/docs/hooks",
        filename="hooks.md",
        title="Hooks: lifecycle",
    )
    assert 'title: "Hooks: lifecycle"' in fetcher.frontmatter_for(page, source_url=page.url)


def test_guards_pass_on_a_healthy_run() -> None:
    assert (
        fetcher.check_coverage_guards(
            discovered=116, live=115, stale=0, skipped=1, previous_file_count=112
        )
        == []
    )


def test_guards_fail_when_nothing_is_live() -> None:
    problems = fetcher.check_coverage_guards(
        discovered=116, live=0, stale=116, skipped=0, previous_file_count=112
    )
    assert any("No page was fetched live" in problem for problem in problems)


def test_guards_fail_when_discovery_collapses() -> None:
    problems = fetcher.check_coverage_guards(
        discovered=10, live=10, stale=0, skipped=0, previous_file_count=112
    )
    assert any("refusing to delete references" in problem for problem in problems)


def test_guards_fail_on_empty_discovery() -> None:
    assert fetcher.check_coverage_guards(
        discovered=0, live=0, stale=0, skipped=0, previous_file_count=112
    ) == ["Discovery returned no documentation pages"]


def test_sanitize_error_strips_local_paths() -> None:
    """Error text is committed to the manifest, so it must not carry a home path."""

    error = OSError(
        "[Errno 2] No such file or directory: '/Users/someone/Desktop/repo/x.md'"
    )
    message = fetcher.sanitize_error(error)

    assert "/Users/someone" not in message
    assert "/Users/<user>" in message
    assert message.startswith("OSError: ")


def test_sanitize_error_redacts_proxy_credentials() -> None:
    error = fetcher.requests.ConnectionError(
        "Failed to connect to https://alice:hunter2@proxy.corp.example/"
    )
    message = fetcher.sanitize_error(error)

    assert "hunter2" not in message
    assert "<redacted>@proxy.corp.example" in message


def test_sanitize_error_replaces_the_repository_root() -> None:
    error = OSError(f"cannot write {fetcher.ROOT_DIR}/skills/x/references/y.md")
    message = fetcher.sanitize_error(error)

    assert str(fetcher.ROOT_DIR) not in message
    assert "<repo>" in message


def test_sanitize_error_is_bounded() -> None:
    assert len(fetcher.sanitize_error(RuntimeError("x" * 5000))) == 300
