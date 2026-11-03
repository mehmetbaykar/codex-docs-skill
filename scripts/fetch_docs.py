#!/usr/bin/env python3
"""Mirror the OpenAI Codex documentation into the codex-docs skill.

Product-specific settings only; the shared engine lives in docs_mirror.py.
"""

from __future__ import annotations

import html
import re
from email.utils import parsedate_to_datetime

import requests

from docs_mirror import Page, Product, Section, fetch_text, parse_xml, run


BASE_URL = "https://learn.chatgpt.com"
LEGACY_PREFIX = "/codex"
CHANGELOG_RSS_URL = f"{BASE_URL}/docs/changelog/rss.xml"

# learn.chatgpt.com hosts the combined ChatGPT and Codex docs. These sections
# cover ChatGPT-only features and stay out of the Codex mirror. Shared pages,
# such as the desktop app Codex runs in, stay in.
CHATGPT_ONLY_PATHS = (
    "/docs/appshots",
    "/docs/artifacts-viewer",
    "/docs/dots",
    "/docs/get-started-with-work",
    "/docs/image-generation",
    "/docs/personalize",
    "/docs/pets",
    "/docs/sites",
    "/docs/space",
    "/docs/use-chatgpt",
    "/docs/visualizations",
    "/docs/web",
)
CHATGPT_ONLY_PREFIXES = (
    "/docs/dots/",
    "/docs/sites/",
    "/docs/space/",
    "/docs/whats-new/dots-",
)

INDEX_POINTER = re.compile(
    r"^> For the complete documentation index, see \[llms\.txt\]\([^)]*\)\.[^\n]*\n+",
    re.MULTILINE,
)
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)


def map_legacy_path(path: str) -> str:
    """Map legacy /codex/* paths, still linked from pages and llms.txt, onto /docs/*."""

    if path == LEGACY_PREFIX or path.startswith(f"{LEGACY_PREFIX}/"):
        suffix = path.removeprefix(LEGACY_PREFIX).strip("/")
        return f"/docs/{suffix}" if suffix else "/docs"
    return path


def recipe_fields(raw: str) -> dict[str, str]:
    """Read the name, tagline, and summary scalars from a recipe's frontmatter."""

    match = FRONTMATTER.match(raw)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for found in re.finditer(
        r"^(name|tagline|summary):[ \t]*(.*(?:\n[ \t]+.*)*)", match.group(1), flags=re.MULTILINE
    ):
        value = re.sub(r"^[>|][-+]?", "", found.group(2).strip())
        value = " ".join(part.strip() for part in value.splitlines() if part.strip())
        fields[found.group(1)] = value.strip("\"'")
    return fields


def exclude(page: Page, raw: str) -> str | None:
    """Keep only Codex recipes; the recipe gallery also lists ChatGPT-only ones.

    A recipe whose name, tagline, or summary mentions Codex stays. One that
    mentions only ChatGPT goes. When neither is named, the body decides.
    """

    if page.section.key != "use-cases":
        return None
    headline = " ".join(recipe_fields(raw).values())
    if re.search(r"\bCodex\b", headline):
        return None
    if re.search(r"\bChatGPT\b", headline):
        return "ChatGPT-only recipe"
    body = FRONTMATTER.sub("", raw, count=1)
    if len(re.findall(r"\bCodex\b", body)) > len(re.findall(r"\bChatGPT\b", body)):
        return None
    return "Recipe is not about Codex"


def render_recipe(content: str) -> str:
    """Lift a recipe's frontmatter into the page so its skills and prompt survive."""

    match = FRONTMATTER.match(content)
    if not match:
        return content
    fields = recipe_fields(content)
    details = re.sub(
        r"^(\s*url:\s*)(/\S*)",
        lambda found: found.group(1) + BASE_URL + map_legacy_path(found.group(2)),
        match.group(1),
        flags=re.MULTILINE,
    )
    header = [f"# {fields.get('name', 'Recipe')}", ""]
    for key in ("tagline", "summary"):
        if fields.get(key):
            header.extend([fields[key], ""])
    header.extend(["## Recipe details", "", "```yaml", details, "```", ""])
    return "\n".join(header) + content[match.end() :]


def clean(page: Page, content: str) -> str:
    if page.section.key == "use-cases":
        content = render_recipe(content)
    return INDEX_POINTER.sub("", content, count=1)


def render_changelog(session: requests.Session, product: Product, page: Page) -> tuple[str, str]:
    """Render the changelog from its RSS feed; the page has no .md twin."""

    channel = parse_xml(fetch_text(session, product, CHANGELOG_RSS_URL) or "").find("channel")
    items = channel.findall("item") if channel is not None else []
    if not items:
        raise RuntimeError("Codex changelog RSS returned no entries")

    lines = ["# Codex Changelog", "", f"> Rendered from the changelog RSS feed: {CHANGELOG_RSS_URL}", ""]
    for item in items:
        title = html.unescape(item.findtext("title") or "Untitled").strip()
        link = (item.findtext("link") or page.url).strip()
        published = (item.findtext("pubDate") or "").strip()
        date = ""
        if published:
            try:
                date = parsedate_to_datetime(published).date().isoformat()
            except (TypeError, ValueError, IndexError):
                date = published
        summary = re.sub(r"<[^>]+>", "", html.unescape(item.findtext("description") or "")).strip()
        lines.extend([f"## {title} ({date})" if date else f"## {title}", "", f"- Source: {link}"])
        if summary:
            lines.extend(["", summary])
        lines.append("")
    return "\n".join(lines), CHANGELOG_RSS_URL


PRODUCT = Product(
    name="Codex",
    skill="codex-docs",
    repository="mehmetbaykar/codex-docs-skill",
    docs_url=f"{BASE_URL}/docs",
    base_url=BASE_URL,
    sitemap_urls=(f"{BASE_URL}/sitemap-index.xml",),
    llms_txt_url=f"{BASE_URL}/docs/llms.txt",
    sections=(
        Section(
            key="docs",
            label="Documentation",
            path_prefix="/docs",
            fetch="markdown",
            mdx=True,
            root_filename="codex",
        ),
        Section(
            key="use-cases",
            label="Recipes",
            path_prefix="/use-cases",
            fetch="markdown",
            mdx=True,
            keep_prefix=True,
        ),
        Section(
            key="guides",
            label="Guides",
            path_prefix="/guides",
            fetch="html",
            keep_prefix=True,
            html_selector="article#mainContent",
        ),
    ),
    # llms.txt still links some pages on the previous docs host.
    alternate_hosts=("developers.openai.com",),
    excluded_prefixes=("/docs/enterprise/", *CHATGPT_ONLY_PREFIXES),
    excluded_paths=(
        # Aggregate exports rather than individual documentation pages.
        "/docs/codex-manual",
        "/docs/llms-full",
        "/docs/videos",
        *CHATGPT_ONLY_PATHS,
    ),
    map_path=map_legacy_path,
    clean=clean,
    exclude=exclude,
    special={"/docs/changelog": render_changelog},
    source_extra={"changelog_rss_url": CHANGELOG_RSS_URL},
)


if __name__ == "__main__":
    raise SystemExit(run(PRODUCT))
