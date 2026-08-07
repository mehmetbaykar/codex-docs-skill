#!/usr/bin/env python3
"""Fetch and clean OpenAI Codex documentation for the codex-docs skill."""

from __future__ import annotations

import hashlib
import html
import json
import logging
import random
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import feedparser
import requests


ROOT_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT_DIR / "skills" / "codex-docs"
REFERENCES_DIR = SKILL_DIR / "references"
RAW_DIR = REFERENCES_DIR / "_raw"
MANIFEST_FILE = "docs_manifest.json"

# Codex docs moved from developers.openai.com/codex to learn.chatgpt.com/docs
# around 2026-07-09; the legacy host now redirects here.
DOCS_BASE_URL = "https://learn.chatgpt.com"
DOCS_PATH_PREFIX = "/docs"
LEGACY_DOCS_PATH_PREFIX = "/codex"
SITEMAP_INDEX_URL = f"{DOCS_BASE_URL}/sitemap-index.xml"
LLMS_TXT_URL = f"{DOCS_BASE_URL}{DOCS_PATH_PREFIX}/llms.txt"
CODEX_CHANGELOG_RSS_URL = f"{DOCS_BASE_URL}{DOCS_PATH_PREFIX}/changelog/rss.xml"

HEADERS = {
    "User-Agent": "codex-docs-skill-fetcher/1.0 (+https://learn.chatgpt.com/docs)",
    "Accept": "text/plain, text/markdown, application/xml, text/xml, */*",
    "Cache-Control": "no-cache",
}

MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
RATE_LIMIT_SECONDS = 0.2
RETRY_BASE_DELAY_SECONDS = 1
RETRY_MAX_DELAY_SECONDS = 10
MAX_THROTTLE_RETRIES = 5

# Coverage guards. A documentation mirror that silently keeps serving old
# content is worse than one that fails loudly, so the run fails when live
# coverage collapses.
MAX_STALE_RATIO = 0.2
MAX_SKIPPED_RATIO = 0.2
MIN_DISCOVERY_RATIO = 0.8
FETCH_TOOL_VERSION = "2.0"

EXCLUDED_PREFIXES = (f"{DOCS_PATH_PREFIX}/enterprise/",)
EXCLUDED_EXACT_PATHS = {
    f"{DOCS_PATH_PREFIX}/videos",
    # Aggregate exports rather than individual documentation pages.
    f"{DOCS_PATH_PREFIX}/codex-manual",
    f"{DOCS_PATH_PREFIX}/llms-full",
}
SPECIAL_RSS_PATHS = {
    f"{DOCS_PATH_PREFIX}/changelog": CODEX_CHANGELOG_RSS_URL,
}
PAGE_PROCESSING_ERRORS = (
    RuntimeError,
    requests.RequestException,
    OSError,
    ValueError,
    KeyError,
    TypeError,
    ET.ParseError,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("codex-docs")


@dataclass(frozen=True)
class CodexPage:
    """A Codex documentation page discovered from the sitemap."""

    url: str
    path: str
    filename: str
    title: str

    @property
    def markdown_url(self) -> str:
        path = self.path.rstrip("/")
        return f"{DOCS_BASE_URL}{path}.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    manifest_path = REFERENCES_DIR / MANIFEST_FILE
    if not manifest_path.exists():
        return {"files": {}}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        logger.warning("Ignoring invalid manifest JSON: %s", error)
        return {"files": {}}

    if "files" not in manifest or not isinstance(manifest["files"], dict):
        manifest["files"] = {}
    return manifest


def write_text_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def fetch_text(
    session: requests.Session, url: str, *, allow_404: bool = False
) -> str | None:
    """Fetch a URL as text. Returns None only when ``allow_404`` is set and the
    server replied 404. Other 4xx responses raise immediately because they are
    not transient. 5xx, connection, and timeout errors retry with backoff and
    jitter; 429 honors ``Retry-After`` (or 30s) and does not consume an attempt.
    """

    last_error: Exception | None = None
    attempt = 0
    throttle_count = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        try:
            response = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        except (
            requests.ConnectionError,
            requests.Timeout,
            requests.exceptions.ChunkedEncodingError,
        ) as error:
            last_error = error
            _sleep_backoff(url, attempt, error)
            continue

        if response.status_code == 404 and allow_404:
            return None
        if response.status_code == 429:
            if throttle_count >= MAX_THROTTLE_RETRIES:
                raise RuntimeError(
                    f"Rate limited fetching {url} after "
                    f"{MAX_THROTTLE_RETRIES} cooperative retries"
                )
            throttle_count += 1
            wait_seconds = int(response.headers.get("Retry-After", "30"))
            logger.warning(
                "Rate limited fetching %s; waiting %ss (cooperative retry %s/%s)",
                url,
                wait_seconds,
                throttle_count,
                MAX_THROTTLE_RETRIES,
            )
            time.sleep(wait_seconds)
            attempt -= 1
            continue
        if 500 <= response.status_code < 600:
            error = requests.HTTPError(
                f"{response.status_code} {response.reason}", response=response
            )
            last_error = error
            _sleep_backoff(url, attempt, error)
            continue

        response.raise_for_status()
        return response.text

    raise RuntimeError(
        f"Failed to fetch {url} after {MAX_RETRIES} attempts: {last_error}"
    )


def _sleep_backoff(url: str, attempt: int, error: Exception) -> None:
    delay = min(
        RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1)), RETRY_MAX_DELAY_SECONDS
    )
    delay *= random.uniform(0.5, 1.0)
    logger.warning(
        "Fetch failed for %s (%s/%s): %s; retrying in %.1fs",
        url,
        attempt,
        MAX_RETRIES,
        error,
        delay,
    )
    time.sleep(delay)


def _parse_xml(xml_text: str) -> ET.Element:
    """Parse XML defensively against XXE / external-entity attacks, with a
    fallback for older Python builds that do not accept the safety parameters.
    """

    try:
        parser = ET.XMLParser(
            forbid_dtd=True, forbid_entities=True, forbid_external=True
        )
        return ET.fromstring(xml_text, parser=parser)
    except TypeError:
        logger.warning("XMLParser safety parameters unavailable; using default parser")
        return ET.fromstring(xml_text)


def xml_locs(xml_text: str) -> list[str]:
    try:
        root = _parse_xml(xml_text)
    except ET.ParseError as error:
        raise RuntimeError(f"Failed to parse XML: {error}") from error

    locs: list[str] = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            locs.append(element.text.strip())
    return locs


def normalize_path(path: str) -> str:
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    if path.endswith(".md"):
        path = path.removesuffix(".md")
    # llms.txt links legacy /codex/* paths that now redirect to /docs/*.
    if path == LEGACY_DOCS_PATH_PREFIX or path.startswith(
        f"{LEGACY_DOCS_PATH_PREFIX}/"
    ):
        suffix = path.removeprefix(LEGACY_DOCS_PATH_PREFIX).strip("/")
        path = f"{DOCS_PATH_PREFIX}/{suffix}" if suffix else DOCS_PATH_PREFIX
    return path


def is_codex_doc_url(url: str) -> bool:
    """Return True for mirrored Codex doc pages on the current docs host."""

    parsed = urlparse(url)
    path = normalize_path(parsed.path)

    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.netloc != urlparse(DOCS_BASE_URL).netloc:
        return False
    if parsed.query:
        return False
    if not (path == DOCS_PATH_PREFIX or path.startswith(f"{DOCS_PATH_PREFIX}/")):
        return False
    if path in EXCLUDED_EXACT_PATHS:
        return False
    if any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return True


def path_to_filename(path: str) -> str:
    slug = path.removeprefix(DOCS_PATH_PREFIX).strip("/")
    if not slug:
        # Keep the overview filename stable for installed skill consumers.
        slug = "codex"

    slug = slug.replace("/", "__")
    slug = re.sub(r"[^a-zA-Z0-9_.-]+", "-", slug)
    slug = slug.strip("-._") or "codex"
    return f"{slug}.md"


def title_from_path(path: str) -> str:
    slug = path.removeprefix(DOCS_PATH_PREFIX).strip("/") or "codex"
    return " ".join(part.capitalize() for part in re.split(r"[/_-]+", slug) if part)


def pages_from_paths(paths: set[str]) -> list[CodexPage]:
    pages: list[CodexPage] = []
    filename_to_path: dict[str, str] = {}
    for path in sorted(paths):
        filename = path_to_filename(path)
        prior_path = filename_to_path.get(filename)
        if prior_path is not None and prior_path != path:
            raise RuntimeError(
                f"Slug collision: {prior_path!r} and {path!r} both map to "
                f"{filename!r}; adjust path_to_filename"
            )
        filename_to_path[filename] = path
        pages.append(
            CodexPage(
                url=f"{DOCS_BASE_URL}{path}",
                path=path,
                filename=filename,
                title=title_from_path(path),
            )
        )
    return pages


def paths_from_sitemaps(session: requests.Session) -> set[str]:
    """Collect documentation paths from the sitemap index."""

    logger.info("Fetching sitemap index: %s", SITEMAP_INDEX_URL)
    try:
        sitemap_index = fetch_text(session, SITEMAP_INDEX_URL)
    except PAGE_PROCESSING_ERRORS as error:
        logger.warning("Sitemap index fetch failed: %s", error)
        return set()

    if not sitemap_index:
        return set()

    sitemap_urls = xml_locs(sitemap_index)
    if not sitemap_urls:
        logger.warning("No sitemap URLs found in sitemap index")
        return set()

    paths: set[str] = set()
    for sitemap_url in sitemap_urls:
        logger.info("Fetching sitemap: %s", sitemap_url)
        try:
            sitemap_text = fetch_text(session, sitemap_url)
        except PAGE_PROCESSING_ERRORS as error:
            logger.warning("Failed to fetch sitemap %s: %s", sitemap_url, error)
            continue
        if sitemap_text is None:
            continue
        paths.update(
            normalize_path(urlparse(url).path)
            for url in xml_locs(sitemap_text)
            if is_codex_doc_url(url)
        )

    logger.info("Discovered %s documentation paths from the sitemap", len(paths))
    return paths


def paths_from_llms_txt(session: requests.Session) -> set[str]:
    """Collect documentation paths from the llms.txt index.

    llms.txt links some pages only as query variants of a shared base page
    (for example `developer-commands.md?surface=cli` and `?surface=ide`), so
    the query is stripped and the base path is mirrored once.
    """

    logger.info("Fetching llms.txt: %s", LLMS_TXT_URL)
    try:
        llms_text = fetch_text(session, LLMS_TXT_URL, allow_404=True)
    except PAGE_PROCESSING_ERRORS as error:
        logger.warning("Failed to fetch %s: %s", LLMS_TXT_URL, error)
        return set()
    if not llms_text:
        return set()

    paths: set[str] = set()
    for match in re.finditer(r"\((https?://[^)\s]+?\.md)(?:\?[^)\s]*)?\)", llms_text):
        parsed = urlparse(match.group(1))
        if parsed.netloc not in {
            urlparse(DOCS_BASE_URL).netloc,
            "developers.openai.com",
        }:
            continue
        path = normalize_path(parsed.path)
        if is_codex_doc_url(f"{DOCS_BASE_URL}{path}"):
            paths.add(path)

    logger.info("Discovered %s documentation paths from llms.txt", len(paths))
    return paths


def discover_codex_pages(session: requests.Session) -> list[CodexPage]:
    """Discover pages from the sitemap and llms.txt, then merge both sets.

    Neither index is complete on its own: the sitemap omits pages that
    llms.txt links only as query variants, and llms.txt omits the changelog.
    """

    paths = paths_from_sitemaps(session) | paths_from_llms_txt(session)
    pages = pages_from_paths(paths)
    logger.info("Discovered %s Codex documentation URLs after filtering", len(pages))
    return pages


def strip_inline_markdown_noise(content: str) -> str:
    content = content.replace('{" "}', " ")
    content = content.replace("{' '}", " ")
    content = re.sub(r"\{`([^`]+)`\}", r"`\1`", content)
    return content


def convert_html_links(content: str) -> str:
    def replace_anchor(match: re.Match[str]) -> str:
        href = html.unescape(match.group("href"))
        label = re.sub(r"<[^>]+>", "", match.group("label")).strip()
        label = html.unescape(label)
        if href.startswith("/"):
            href = urljoin(DOCS_BASE_URL, href)
        return f"[{label}]({href})"

    return re.sub(
        r"<a\b[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<label>.*?)</a>",
        replace_anchor,
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )


def convert_keyboard_tags(content: str) -> str:
    return re.sub(
        r"<kbd>(.*?)</kbd>",
        lambda match: f"`{html.unescape(match.group(1).strip())}`",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )


def remove_component_tags(content: str) -> str:
    lines = content.splitlines()
    cleaned: list[str] = []
    in_fence = False
    skipping_tag = False
    skipping_script = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            cleaned.append(line)
            continue

        if in_fence:
            cleaned.append(line)
            continue

        if skipping_script:
            if "</script>" in stripped.lower():
                skipping_script = False
            continue

        if skipping_tag:
            if ">" in stripped:
                skipping_tag = False
            continue

        if stripped.lower().startswith("<script"):
            if "</script>" not in stripped.lower():
                skipping_script = True
            continue

        if re.match(r"^</?[A-Z][A-Za-z0-9_.-]*\b", stripped):
            if stripped.startswith("</"):
                continue
            if ">" not in stripped:
                skipping_tag = True
            continue

        if re.match(
            r"^</?(div|span|br|section|aside)\b", stripped, flags=re.IGNORECASE
        ):
            if stripped.startswith("</"):
                continue
            if stripped.endswith("/>") or stripped in {"<br>", "<br/>", "<br />"}:
                continue
            if ">" not in stripped:
                skipping_tag = True
                continue
            line = re.sub(
                r"</?(div|span|section|aside)\b[^>]*>", "", line, flags=re.IGNORECASE
            )
            if not line.strip():
                continue

        line = re.sub(r"</?[A-Z][A-Za-z0-9_.-]*\b[^>]*>", "", line)
        line = re.sub(r"<br\s*/?>", "", line, flags=re.IGNORECASE)
        cleaned.append(line)

    return "\n".join(cleaned)


def _split_by_fences(text: str) -> list[tuple[bool, str]]:
    """Return (in_fence, chunk) segments split on triple-backtick fence lines.

    Fence delimiter lines themselves are returned as ``in_fence=False`` so
    outside-of-fence transforms leave them verbatim while still toggling the
    fenced-state for following chunks.
    """

    segments: list[tuple[bool, str]] = []
    buffer: list[str] = []
    in_fence = False

    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            if buffer:
                segments.append((in_fence, "".join(buffer)))
                buffer = []
            segments.append((False, line))
            in_fence = not in_fence
            continue
        buffer.append(line)

    if buffer:
        segments.append((in_fence, "".join(buffer)))

    return segments


def _apply_outside_fences(text: str, transform) -> str:
    return "".join(
        chunk if in_fence else transform(chunk)
        for in_fence, chunk in _split_by_fences(text)
    )


def absolutize_links(content: str) -> str:
    """Rewrite root-relative Markdown links to absolute documentation URLs.

    Legacy `/codex/...` targets are mapped onto their current `/docs/...`
    location so mirrored pages do not link to redirect-only paths.
    """

    def replace(match: re.Match[str]) -> str:
        target = match.group("target")
        path, separator, tail = target.partition("#")
        if path == LEGACY_DOCS_PATH_PREFIX or path.startswith(
            f"{LEGACY_DOCS_PATH_PREFIX}/"
        ):
            suffix = path.removeprefix(LEGACY_DOCS_PATH_PREFIX).strip("/")
            path = f"{DOCS_PATH_PREFIX}/{suffix}" if suffix else DOCS_PATH_PREFIX
        return f"]({DOCS_BASE_URL}{path}{separator}{tail})"

    # Anchored on the link target rather than the label, because labels can
    # themselves contain brackets (for example `` `[auto_review].policy` ``).
    return re.sub(r"\]\((?P<target>/(?!/)[^)\s]*)\)", replace, content)


def clean_mdx(raw_content: str) -> str:
    content = raw_content.replace("\r\n", "\n")

    def outside_fences(text: str) -> str:
        text = re.sub(r"(?ms)^import\s+.*?(?=^\S|\Z)", "", text)
        text = re.sub(r"(?ms)^export\s+.*?(?=^\S|\Z)", "", text)
        text = re.sub(r"(?is)<script\b[^>]*>.*?</script>", "", text)
        text = convert_html_links(text)
        text = convert_keyboard_tags(text)
        text = strip_inline_markdown_noise(text)
        text = absolutize_links(text)
        return text

    content = _apply_outside_fences(content, outside_fences)
    content = remove_component_tags(content)
    content = html.unescape(content)

    content = re.sub(r"\n{3,}", "\n\n", content)
    content = re.sub(r"[ \t]+\n", "\n", content)
    return content.strip() + "\n"


def content_looks_like_markdown(content: str) -> bool:
    stripped = content.strip()
    if len(stripped) < 50:
        return False
    indicators = (
        "# ",
        "## ",
        "### ",
        "- ",
        "1. ",
        "```",
        "[",
        "|",
    )
    return (
        sum(1 for line in stripped.splitlines() if line.lstrip().startswith(indicators))
        >= 2
    )


def extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return fallback


def yaml_quoted(value: str) -> str:
    """Quote a YAML scalar without escaping non-ASCII characters."""

    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def frontmatter_for(page: CodexPage, *, source_url: str) -> str:
    return (
        "---\n"
        f"title: {yaml_quoted(page.title)}\n"
        f"source: {source_url}\n"
        f"path: {page.path}\n"
        "---\n\n"
    )


def render_changelog_from_rss(session: requests.Session, page: CodexPage) -> str:
    rss_text = fetch_text(session, CODEX_CHANGELOG_RSS_URL)
    if rss_text is None:
        raise RuntimeError("Changelog RSS returned no content")

    parsed = feedparser.parse(rss_text)
    entries = list(parsed.entries)
    if getattr(parsed, "bozo", 0) and getattr(parsed, "bozo_exception", None):
        logger.warning("RSS feed flagged as bozo: %s", parsed.bozo_exception)
    if not entries:
        logger.warning(
            "Codex changelog RSS returned zero entries (%s)",
            CODEX_CHANGELOG_RSS_URL,
        )

    lines = [
        "# Codex Changelog",
        "",
        f"> Source: {page.url}",
        f"> RSS: {CODEX_CHANGELOG_RSS_URL}",
        "",
    ]

    for entry in entries:
        title = html.unescape(entry.get("title", "Untitled")).strip()
        link = entry.get("link", page.url)
        published = entry.get("published") or entry.get("updated") or ""
        date_label = ""
        if published:
            try:
                date_label = parsedate_to_datetime(published).date().isoformat()
            except (TypeError, ValueError, IndexError):
                date_label = str(published)

        summary = html.unescape(entry.get("summary", "") or "")
        summary = re.sub(r"<[^>]+>", "", summary).strip()

        heading = f"## {title}"
        if date_label:
            heading += f" ({date_label})"
        lines.extend([heading, "", f"- Source: {link}"])
        if summary:
            lines.extend(["", summary])
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_index(entries: dict[str, dict], skipped: list[dict]) -> str:
    lines = [
        "# Codex Docs Index",
        "",
        "Local mirror of OpenAI Codex documentation from https://learn.chatgpt.com/docs.",
        "",
        "Invoke this skill with a topic, for example `$codex-docs hooks` in Codex or `/codex-docs hooks` in Claude Code.",
        "",
        "## Topics",
        "",
    ]

    for filename, metadata in sorted(entries.items(), key=lambda item: item[0]):
        title = metadata.get("title") or filename.removesuffix(".md")
        source = metadata.get("original_url", "")
        lines.append(f"- `{filename.removesuffix('.md')}` - [{title}]({source})")

    if skipped:
        lines.extend(["", "## Skipped Sitemap Pages", ""])
        for item in skipped:
            lines.append(f"- `{item['path']}` - {item['reason']}")

    return "\n".join(lines).strip() + "\n"


def cleanup_old_files(manifest: dict, current_files: set[str]) -> None:
    previous_files = set(manifest.get("files", {}).keys())
    for filename in sorted(previous_files - current_files):
        if filename == MANIFEST_FILE:
            continue
        path = REFERENCES_DIR / filename
        if path.exists():
            logger.info("Removing obsolete file: %s", filename)
            path.unlink()


def save_page(
    page: CodexPage,
    content: str,
    source_url: str,
    manifest: dict,
    new_files: dict[str, dict],
    current_files: set[str],
    *,
    raw_content: str | None = None,
    status: str = "live",
    preserve_raw: bool = False,
) -> None:
    content_hash = sha256(content)
    old_entry = manifest.get("files", {}).get(page.filename, {})
    old_hash = old_entry.get("hash")
    last_updated = old_entry.get("last_updated", now_iso())

    if old_hash != content_hash:
        last_updated = now_iso()
        write_text_if_changed(REFERENCES_DIR / page.filename, content)
        logger.info("Updated: %s", page.filename)
    else:
        logger.info("Unchanged: %s", page.filename)

    raw_path = RAW_DIR / page.filename
    if raw_content is not None:
        write_text_if_changed(raw_path, raw_content)
    elif not preserve_raw and raw_path.exists():
        # The cleaner recovered for this page, so the raw copy is now stale.
        logger.info("Removing stale raw copy: %s", page.filename)
        raw_path.unlink()

    new_files[page.filename] = {
        "title": extract_title(content, page.title),
        "path": page.path,
        "original_url": page.url,
        "source_url": source_url,
        "hash": content_hash,
        "last_updated": last_updated,
        "status": status,
    }
    current_files.add(page.filename)


def load_previous_reference(page: CodexPage, manifest: dict) -> tuple[str, str] | None:
    """Return ``(content, source_url)`` for a previously mirrored page."""

    entry = manifest.get("files", {}).get(page.filename)
    reference_path = REFERENCES_DIR / page.filename
    if not isinstance(entry, dict) or not reference_path.exists():
        return None
    return reference_path.read_text(encoding="utf-8"), entry.get("source_url", page.url)


def check_coverage_guards(
    *,
    discovered: int,
    live: int,
    stale: int,
    skipped: int,
    previous_file_count: int,
) -> list[str]:
    """Return the reasons this run must fail instead of committing."""

    problems: list[str] = []
    if discovered == 0:
        problems.append("Discovery returned no documentation pages")
        return problems

    if live == 0:
        problems.append("No page was fetched live; the mirror would be frozen")

    if previous_file_count and discovered < previous_file_count * MIN_DISCOVERY_RATIO:
        problems.append(
            f"Discovered {discovered} pages, below {MIN_DISCOVERY_RATIO:.0%} of the "
            f"previous {previous_file_count}; refusing to delete references"
        )

    if stale > discovered * MAX_STALE_RATIO:
        problems.append(
            f"{stale}/{discovered} pages served stale content, above the "
            f"{MAX_STALE_RATIO:.0%} threshold"
        )

    if skipped > discovered * MAX_SKIPPED_RATIO:
        problems.append(
            f"{skipped}/{discovered} pages had no usable Markdown, above the "
            f"{MAX_SKIPPED_RATIO:.0%} threshold"
        )

    return problems


def fetch_and_save_pages(
    session: requests.Session, pages: list[CodexPage], manifest: dict
) -> dict:
    new_files: dict[str, dict] = {}
    current_files: set[str] = set()
    skipped: list[dict] = []
    failed: list[dict] = []
    stale: list[dict] = []
    successful = 0

    for index, page in enumerate(pages, start=1):
        logger.info("Processing %s/%s: %s", index, len(pages), page.path)
        try:
            if page.path in SPECIAL_RSS_PATHS:
                content = render_changelog_from_rss(session, page)
                save_page(
                    page,
                    content,
                    SPECIAL_RSS_PATHS[page.path],
                    manifest,
                    new_files,
                    current_files,
                )
                successful += 1
                continue

            raw_content = fetch_text(session, page.markdown_url, allow_404=True)
            if raw_content is None:
                skipped.append(
                    {
                        "path": page.path,
                        "url": page.url,
                        "reason": "No .md endpoint and no special fetcher",
                    }
                )
                logger.info("Skipped (no markdown endpoint): %s", page.path)
                continue

            cleaned_content = clean_mdx(raw_content)
            page_with_title = CodexPage(
                page.url,
                page.path,
                page.filename,
                extract_title(cleaned_content, page.title),
            )

            if not content_looks_like_markdown(cleaned_content):
                logger.warning(
                    "Cleaned content failed markdown sanity check: %s", page.path
                )
                raw_header = (
                    f"# {page_with_title.title}\n\n"
                    f"> Source: {page.url}\n"
                    "> Note: MDX cleaning failed for this page, so this file contains raw source.\n\n"
                )
                content = raw_header + raw_content.strip() + "\n"
                save_page(
                    page_with_title,
                    content,
                    page.markdown_url,
                    manifest,
                    new_files,
                    current_files,
                    raw_content=raw_content,
                )
            else:
                content = (
                    frontmatter_for(page_with_title, source_url=page.url)
                    + cleaned_content
                )
                save_page(
                    page_with_title,
                    content,
                    page.markdown_url,
                    manifest,
                    new_files,
                    current_files,
                )

            successful += 1
            time.sleep(RATE_LIMIT_SECONDS)
        except PAGE_PROCESSING_ERRORS as error:
            previous = load_previous_reference(page, manifest)
            if previous is None:
                logger.error("Failed to process %s: %s", page.path, error)
                failed.append(
                    {"path": page.path, "url": page.url, "error": str(error)}
                )
                continue

            previous_content, previous_source = previous
            logger.warning(
                "Serving stale content for %s after fetch failure: %s",
                page.path,
                error,
            )
            stale.append({"path": page.path, "url": page.url, "error": str(error)})
            save_page(
                page,
                previous_content,
                previous_source,
                manifest,
                new_files,
                current_files,
                status="stale",
                preserve_raw=True,
            )

    cleanup_old_files(manifest, current_files)

    index_content = build_index(new_files, skipped)
    write_text_if_changed(REFERENCES_DIR / "INDEX.md", index_content)

    new_manifest = {
        "description": "Codex documentation mirror manifest. Files live beside this manifest in references/.",
        "source": {
            "sitemap_index_url": SITEMAP_INDEX_URL,
            "llms_txt_url": LLMS_TXT_URL,
            "base_url": DOCS_BASE_URL,
        },
        "filters": {
            "include": [f"{DOCS_PATH_PREFIX}/*"],
            "exclude_prefixes": list(EXCLUDED_PREFIXES),
            "exclude_exact_paths": sorted(EXCLUDED_EXACT_PATHS),
            "exclude_cross_domain": True,
        },
        "files": new_files,
        "skipped": skipped,
        "fetch_metadata": {
            "total_pages_discovered": len(pages),
            "pages_fetched_successfully": successful,
            "pages_stale": len(stale),
            "pages_skipped": len(skipped),
            "pages_failed": len(failed),
            "failed_pages": failed,
            "stale_pages": stale,
            "fetch_tool_version": FETCH_TOOL_VERSION,
        },
    }
    if _manifest_projection(manifest) == _manifest_projection(new_manifest):
        new_manifest["last_updated"] = manifest.get("last_updated", now_iso())
    else:
        new_manifest["last_updated"] = now_iso()
    write_text_if_changed(
        REFERENCES_DIR / MANIFEST_FILE,
        json.dumps(new_manifest, indent=2, sort_keys=True) + "\n",
    )

    problems = check_coverage_guards(
        discovered=len(pages),
        live=successful,
        stale=len(stale),
        skipped=len(skipped),
        previous_file_count=len(manifest.get("files", {})),
    )
    if failed:
        problems.append(f"{len(failed)} page(s) failed; see {MANIFEST_FILE}")
    if problems:
        raise RuntimeError("; ".join(problems))

    return new_manifest


def _manifest_projection(manifest: dict) -> dict:
    projection = dict(manifest)
    projection.pop("last_updated", None)
    projection.pop("fetch_metadata", None)
    return projection


def main() -> int:
    start = time.monotonic()
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()
    with requests.Session() as session:
        pages = discover_codex_pages(session)
        if not pages:
            raise RuntimeError("No Codex pages discovered")
        new_manifest = fetch_and_save_pages(session, pages, manifest)

    elapsed = time.monotonic() - start
    metadata = new_manifest["fetch_metadata"]
    logger.info(
        "Fetch complete in %.1fs: %s live, %s stale, %s skipped, %s failed",
        elapsed,
        metadata["pages_fetched_successfully"],
        metadata["pages_stale"],
        metadata["pages_skipped"],
        metadata["pages_failed"],
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        logger.error("%s", error)
        raise SystemExit(1) from error
