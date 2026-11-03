"""Offline tests for the Codex product settings in fetch_docs.py."""

from __future__ import annotations

import pytest

import docs_mirror as dm
import fetch_docs


PRODUCT = fetch_docs.PRODUCT
BASE = fetch_docs.BASE_URL


def page_for(path: str) -> dm.Page:
    return dm.pages_from_paths(PRODUCT, {path})[0]


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (f"{BASE}/docs", "/docs"),
        (f"{BASE}/docs/hooks", "/docs/hooks"),
        (f"{BASE}/docs/cli/features", "/docs/cli/features"),
        (f"{BASE}/docs/app", "/docs/app"),
        (f"{BASE}/use-cases/agent-friendly-clis", "/use-cases/agent-friendly-clis"),
        (f"{BASE}/guides/best-practices", "/guides/best-practices"),
        ("https://developers.openai.com/codex/prompting.md", "/docs/prompting"),
        (f"{BASE}/codex/config-file/config-basic", "/docs/config-file/config-basic"),
    ],
)
def test_keeps_codex_pages(url: str, expected: str) -> None:
    assert dm.page_path(PRODUCT, url, strip_query=True) == expected


@pytest.mark.parametrize(
    "url",
    [
        f"{BASE}/docs/enterprise/admin",
        f"{BASE}/docs/videos",
        f"{BASE}/docs/codex-manual",
        f"{BASE}/docs/llms-full.txt",
        f"{BASE}/use-cases",
        f"{BASE}/pricing",
        "https://example.com/docs/hooks",
        f"{BASE}/docs/hooks?surface=cli",
    ],
)
def test_drops_out_of_scope_urls(url: str) -> None:
    assert dm.page_path(PRODUCT, url) is None


@pytest.mark.parametrize(
    "path",
    [
        "/docs/dots",
        "/docs/dots/channels",
        "/docs/space/pages",
        "/docs/sites/creating-a-site",
        "/docs/pets",
        "/docs/image-generation",
        "/docs/whats-new/dots-october-28-2026",
    ],
)
def test_drops_chatgpt_only_sections(path: str) -> None:
    assert dm.page_path(PRODUCT, f"{BASE}{path}") is None


def test_llms_query_variants_collapse_to_one_page() -> None:
    paths = {
        dm.page_path(PRODUCT, f"{BASE}/docs/developer-commands.md?surface={surface}", strip_query=True)
        for surface in ("cli", "ide")
    }
    assert paths == {"/docs/developer-commands"}


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/docs/hooks", "hooks.md"),
        ("/docs/cli/features", "cli__features.md"),
        ("/docs", "codex.md"),
        ("/use-cases/agent-friendly-clis", "use-cases__agent-friendly-clis.md"),
        ("/guides/best-practices", "guides__best-practices.md"),
    ],
)
def test_filenames(path: str, expected: str) -> None:
    assert page_for(path).filename == expected


def test_legacy_links_are_mapped_onto_docs() -> None:
    resolve = dm.link_resolver(PRODUCT)
    rewritten = dm.absolutize_links("[old](/codex/config-file/config-advanced#auto) [root](/codex)", resolve)
    assert f"({BASE}/docs/config-file/config-advanced#auto)" in rewritten
    assert f"({BASE}/docs)" in rewritten


def test_clean_drops_the_llms_pointer() -> None:
    raw = (
        "# Hooks\n\n> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). "
        "Markdown versions of documentation pages are available by appending `.md` to the page URL.\n\nBody.\n"
    )
    assert fetch_docs.clean(page_for("/docs/hooks"), raw) == "# Hooks\n\nBody.\n"


RECIPE = """---
name: Create a CLI Codex can use
tagline: Give Codex a composable command.
summary: Ask Codex to create a composable CLI it can run
  from any folder.
skills:
  - token: $cli-creator
    url: https://github.com/openai/skills/tree/main/skills/.curated/cli-creator
relatedLinks:
  - label: Plugins
    url: /codex/plugins
---

> For the complete documentation index, see [llms.txt](/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

## Introduction

Body text.
"""


def recipe(name: str, summary: str, body: str = "Body.") -> str:
    return f"---\nname: {name}\ntagline: A tagline.\nsummary: {summary}\n---\n\n{body}\n"


@pytest.mark.parametrize(
    ("raw", "reason"),
    [
        (RECIPE, None),
        (recipe("Slack coding tasks", "Use ChatGPT in Slack to hand work to Codex."), None),
        (recipe("Audit a course", "Use ChatGPT to compare syllabi."), "ChatGPT-only recipe"),
        (recipe("Web development", "Ship faster.", "Codex builds it. Codex tests it. ChatGPT reviews."), None),
        (recipe("Sales", "Close deals.", "ChatGPT drafts. ChatGPT summarizes. Codex helps."), "Recipe is not about Codex"),
    ],
)
def test_recipes_are_limited_to_codex(raw: str, reason: str | None) -> None:
    assert fetch_docs.exclude(page_for("/use-cases/example"), raw) == reason


def test_exclusion_only_applies_to_recipes() -> None:
    assert fetch_docs.exclude(page_for("/docs/hooks"), recipe("Audit", "Use ChatGPT.")) is None


def test_recipe_frontmatter_becomes_a_page_header() -> None:
    rendered = fetch_docs.clean(page_for("/use-cases/agent-friendly-clis"), RECIPE)
    assert rendered.startswith(
        "# Create a CLI Codex can use\n\nGive Codex a composable command.\n\n"
        "Ask Codex to create a composable CLI it can run from any folder.\n\n## Recipe details\n\n```yaml\n"
    )
    assert f"url: {BASE}/docs/plugins" in rendered
    assert "For the complete documentation index" not in rendered
    assert rendered.rstrip().endswith("Body text.")


RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Codex</title>
<item><title>Codex CLI 0.147.0</title><link>https://learn.chatgpt.com/docs/changelog#0147</link>
<pubDate>Mon, 02 Nov 2026 10:00:00 GMT</pubDate><description>&lt;p&gt;Adds &lt;b&gt;Agent Plugins&lt;/b&gt;.&lt;/p&gt;</description></item>
</channel></rss>"""


class FakeResponse:
    status_code = 200
    headers: dict = {}
    reason = "OK"

    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self) -> None:
        pass


class FakeSession:
    def __init__(self, text: str):
        self.text = text

    def get(self, url: str, headers: dict | None = None, timeout: float | None = None) -> FakeResponse:
        assert url == fetch_docs.CHANGELOG_RSS_URL
        return FakeResponse(self.text)


def test_changelog_is_rendered_from_rss() -> None:
    markdown, source = fetch_docs.render_changelog(FakeSession(RSS), PRODUCT, page_for("/docs/changelog"))
    assert source == fetch_docs.CHANGELOG_RSS_URL
    assert "## Codex CLI 0.147.0 (2026-11-02)" in markdown
    assert "- Source: https://learn.chatgpt.com/docs/changelog#0147" in markdown
    assert "Adds Agent Plugins." in markdown


def test_an_empty_changelog_fails_instead_of_publishing() -> None:
    empty = '<?xml version="1.0"?><rss version="2.0"><channel><title>Codex</title></channel></rss>'
    with pytest.raises(RuntimeError, match="no entries"):
        fetch_docs.render_changelog(FakeSession(empty), PRODUCT, page_for("/docs/changelog"))
