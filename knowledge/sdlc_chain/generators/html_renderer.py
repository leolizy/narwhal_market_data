"""Convert Markdown content to a styled, self-contained HTML document.

Uses only the Python standard library — no external packages required.
Handles the Markdown elements produced by md_renderer.py:
  ATX headings, horizontal rules, fenced code blocks, blockquotes,
  pipe tables, unordered/ordered lists, bold, italic, inline code,
  and plain paragraphs.
"""
import html as _html
import re
from pathlib import Path
from typing import List


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def render_markdown_to_html(md_content: str, title: str = "SDLC Document") -> str:
    """Convert a Markdown string to a complete, styled HTML document."""
    body = _convert(md_content)
    return _wrap_html(title, body)


def render_md_file_to_html(md_path: str, title: str = "") -> str:
    """Read a Markdown file and return a full HTML document string."""
    text = Path(md_path).read_text(encoding="utf-8")
    doc_title = title or Path(md_path).stem.replace("_", " ").replace("-", " ")
    return render_markdown_to_html(text, doc_title)


# ---------------------------------------------------------------------------
# HTML wrapper
# ---------------------------------------------------------------------------

def _wrap_html(title: str, body: str) -> str:
    escaped_title = _html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped_title}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.65;
      color: #2d3748;
      background: #f7f8fa;
      margin: 0;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 1100px;
      margin: 0 auto;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 12px rgba(0,0,0,.08);
      padding: 2.5rem 3rem;
    }}
    h1 {{
      font-size: 2em;
      color: #1a3d5c;
      border-bottom: 3px solid #2c5f8a;
      padding-bottom: .4em;
      margin-top: 0;
    }}
    h2 {{
      font-size: 1.45em;
      color: #2c5f8a;
      border-bottom: 1px solid #d0dce8;
      padding-bottom: .25em;
      margin-top: 2.2em;
    }}
    h3 {{ font-size: 1.15em; color: #3a6ea8; margin-top: 1.5em; }}
    h4, h5, h6 {{ color: #4a5568; margin-top: 1.2em; }}
    p {{ margin: .8em 0; }}
    a {{ color: #2c5f8a; }}
    hr {{
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 2em 0;
    }}
    code {{
      background: #eef2f7;
      padding: .15em .4em;
      border-radius: 4px;
      font-size: .88em;
      font-family: 'SFMono-Regular', Consolas, monospace;
    }}
    pre {{
      background: #1e2433;
      color: #cdd5e0;
      padding: 1.1em 1.4em;
      border-radius: 6px;
      overflow-x: auto;
      margin: 1em 0;
    }}
    pre code {{
      background: none;
      color: inherit;
      padding: 0;
      font-size: .9em;
    }}
    blockquote {{
      border-left: 4px solid #2c5f8a;
      margin: 1em 0;
      padding: .6em 1.1em;
      background: #f0f5fb;
      color: #4a5568;
      border-radius: 0 4px 4px 0;
    }}
    blockquote p {{ margin: 0; }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1.2em 0;
      font-size: .9em;
    }}
    th {{
      background: #2c5f8a;
      color: #fff;
      padding: .55em .9em;
      text-align: left;
      font-weight: 600;
    }}
    td {{
      padding: .45em .9em;
      border: 1px solid #d0dce8;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f7f9fc; }}
    ul, ol {{ padding-left: 1.8em; margin: .6em 0; }}
    li {{ margin: .3em 0; }}
    strong {{ color: #1a3d5c; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="container">
{body}
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Block-level converter
# ---------------------------------------------------------------------------

def _convert(md: str) -> str:
    """Convert Markdown to HTML body content (block-level pass)."""
    lines = md.split("\n")
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # ── Fenced code block ─────────────────────────────────────────────
        if line.rstrip().startswith("```"):
            lang = line.strip()[3:].strip()
            code_lines: List[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(_html.escape(lines[i]))
                i += 1
            lang_attr = f' class="language-{_html.escape(lang)}"' if lang else ""
            result.append(f'<pre><code{lang_attr}>{chr(10).join(code_lines)}</code></pre>')
            i += 1  # skip closing ```
            continue

        # ── ATX heading ───────────────────────────────────────────────────
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            text = _inline(m.group(2).rstrip("#").strip())
            result.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # ── Horizontal rule ───────────────────────────────────────────────
        if re.match(r"^[-*_]{3,}\s*$", line.strip()) and line.strip():
            result.append("<hr>")
            i += 1
            continue

        # ── Blockquote ────────────────────────────────────────────────────
        if line.startswith(">"):
            bq_lines: List[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                bq_lines.append(lines[i][1:].lstrip(" "))
                i += 1
            inner = _convert("\n".join(bq_lines)).strip()
            result.append(f"<blockquote>\n  <p>{inner}</p>\n</blockquote>")
            continue

        # ── Pipe table ────────────────────────────────────────────────────
        if "|" in line and i + 1 < len(lines) and _is_table_sep(lines[i + 1]):
            tbl: List[str] = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                tbl.append(lines[i])
                i += 1
            result.append(_render_table(tbl))
            continue

        # ── Unordered list ────────────────────────────────────────────────
        if re.match(r"^(\s*)[-*+]\s+", line):
            items: List[str] = []
            while i < len(lines) and re.match(r"^(\s*)[-*+]\s+", lines[i]):
                items.append(_inline(re.sub(r"^(\s*)[-*+]\s+", "", lines[i])))
                i += 1
            lis = "\n".join(f"  <li>{item}</li>" for item in items)
            result.append(f"<ul>\n{lis}\n</ul>")
            continue

        # ── Ordered list ──────────────────────────────────────────────────
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(_inline(re.sub(r"^\s*\d+\.\s+", "", lines[i])))
                i += 1
            lis = "\n".join(f"  <li>{item}</li>" for item in items)
            result.append(f"<ol>\n{lis}\n</ol>")
            continue

        # ── Blank line ────────────────────────────────────────────────────
        if not line.strip():
            i += 1
            continue

        # ── Paragraph ─────────────────────────────────────────────────────
        para: List[str] = []
        while i < len(lines) and _is_para_line(lines, i):
            para.append(lines[i])
            i += 1
        if para:
            result.append(f"<p>{_inline(' '.join(para))}</p>")
        else:
            i += 1  # safety: advance past unrecognised line

    return "\n".join(result)


def _is_table_sep(line: str) -> bool:
    """True if the line looks like a Markdown table separator (|---|---|)."""
    stripped = line.strip()
    return bool(stripped) and bool(re.match(r"^[\s|:\-]+$", stripped)) and "|" in stripped


def _is_para_line(lines: List[str], i: int) -> bool:
    """True if lines[i] should be consumed as part of a paragraph."""
    line = lines[i]
    if not line.strip():
        return False
    if re.match(r"^#{1,6}\s", line):
        return False
    if re.match(r"^[-*_]{3,}\s*$", line.strip()):
        return False
    if line.startswith(">"):
        return False
    if line.rstrip().startswith("```"):
        return False
    if re.match(r"^(\s*)[-*+]\s+", line):
        return False
    if re.match(r"^\s*\d+\.\s+", line):
        return False
    # Start of a table
    if "|" in line and i + 1 < len(lines) and _is_table_sep(lines[i + 1]):
        return False
    return True


# ---------------------------------------------------------------------------
# Inline formatting
# ---------------------------------------------------------------------------

def _inline(text: str) -> str:
    """Apply inline Markdown formatting to a text fragment."""
    text = _html.escape(text)
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic: *text* or _text_ (not inside words)
    text = re.sub(r"(?<!\w)\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    return text


# ---------------------------------------------------------------------------
# Table renderer
# ---------------------------------------------------------------------------

def _render_table(lines: List[str]) -> str:
    """Convert a list of pipe-table Markdown lines to an HTML table."""
    if not lines:
        return ""

    def split_cells(row: str) -> List[str]:
        cells = row.strip().split("|")
        # Strip outer empty strings from leading/trailing |
        if cells and not cells[0].strip():
            cells = cells[1:]
        if cells and not cells[-1].strip():
            cells = cells[:-1]
        return [c.strip() for c in cells]

    headers = split_cells(lines[0])
    col_count = len(headers)
    # lines[1] is the separator row — skip it
    data_lines = lines[2:] if len(lines) > 2 else []

    out: List[str] = ["<table>", "  <thead>", "    <tr>"]
    for h in headers:
        out.append(f"      <th>{_inline(h)}</th>")
    out += ["    </tr>", "  </thead>", "  <tbody>"]

    for dline in data_lines:
        cells = split_cells(dline)
        out.append("    <tr>")
        for j in range(col_count):
            cell = cells[j] if j < len(cells) else ""
            out.append(f"      <td>{_inline(cell)}</td>")
        out.append("    </tr>")

    out += ["  </tbody>", "</table>"]
    return "\n".join(out)
