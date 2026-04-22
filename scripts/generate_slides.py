#!/usr/bin/env python3
"""
submissions/*/SHOWCASE.md 를 읽어 Marp 슬라이드 마크다운을 생성합니다.

실행:
    python3 scripts/generate_slides.py              # 전체 재생성
    python3 scripts/generate_slides.py --update-css # CSS만 최신화

HTML 빌드:
    bash scripts/build_slides.sh          # 전체
    bash scripts/build_slides.sh --html-only

<!--
<slide-design-guidelines>

  <color-chip confirmed="true">
    <background>#f0e8d8</background>      <!-- Orchid White -->
    <dark-primary>#252422</dark-primary>  <!-- Warm Black -->
    <dark-secondary>#403D39</dark-secondary>
    <accent>#e07a5f</accent>              <!-- Main — 구조 요소에만 -->
    <sub>#CCC5B9</sub>                    <!-- Chrome White -->
    <panel>#e5ddd0</panel>               <!-- 콘텐츠 패널 배경 -->
  </color-chip>

  <layout>
    <rule>TOC: 좌 이름 + 우 6섹션 목록</rule>
    <rule>문제/해결: 2-panel (② 병목 | ③ 방향)</rule>
    <rule>구현: 화살표 플로우 + 비교표 (② vs ④)</rule>
    <rule>추후/소감: prose panel (⑤⑥)</rule>
  </layout>

</slide-design-guidelines>
-->
"""

import re
import subprocess
import sys
from pathlib import Path

# ── 경로 설정 ─────────────────────────────────────────────────

REPO_ROOT      = Path(__file__).parent.parent
SUBMISSIONS_DIR = REPO_ROOT / "submissions"
SLIDES_DIR     = REPO_ROOT / "slides"
OUTPUT_MD      = SLIDES_DIR / "showcase.md"
OUTPUT_PDF     = SLIDES_DIR / "showcase.pdf"

# ── 템플릿 기본 텍스트 감지 ───────────────────────────────────

TEMPLATE_HINTS = [
    "어떤 업무에서 불편함이나 비효율을",
    "반복적으로 하던 작업, 시간이 오래 걸리던",
    "AI를 쓰기 전에는 어떻게 하고 있었나요",
    "어디서 막히거나, 어디에 시간이",
    "AI로 어떤 변화를 만들고 싶었나요",
    "이렇게 되면 좋겠다",
    "지금까지 무엇을 만들었는지, 어느 정도 완성됐는지",
    "완성이 아니어도 괜찮아요. 시도한 것 자체가",
    "아직 해결하지 못한 것, 더 발전시키고 싶은 것",
    "이번 캠프를 통해 느낀 점, 달라진 것",
    "SHOWCASE.md 제출 후 채움",
]

# ── Marp 헤더 + CSS ───────────────────────────────────────────

MARP_HEADER = """\
---
marp: true
paginate: true
html: true
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

  /* ─── 기본 섹션 ────────────────────────────── */
  section {
    background: #f0e8d8;
    color: #252422;
    font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', sans-serif;
    padding: 44px 72px 50px;
    font-size: 20px;
    line-height: 1.65;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }
  section.dark {
    background: #3d3d3d;
    color: #ffffff;
  }
  section.divider {
    background: #3d3d3d;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  /* h1 — 이름/제목 */
  h1 {
    font-size: 1.75em;
    font-weight: 900;
    border-bottom: 4px solid #e07a5f;
    padding-bottom: 0.1em;
    display: inline-block;
    margin: 0 0 0.45em;
    line-height: 1.2;
  }
  section.dark h1, section.divider h1 {
    color: #fff;
    border-bottom-color: #e07a5f;
  }

  /* h2 — 소제목 */
  h2 {
    font-size: 0.95em;
    font-weight: 700;
    color: #252422;
    margin: 0.8em 0 0.2em;
    letter-spacing: -0.01em;
  }
  h2:first-of-type { margin-top: 0; }

  /* blockquote */
  blockquote {
    background: rgba(224,122,95,0.12);
    border-left: 5px solid #e07a5f;
    padding: 12px 18px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.88em;
    color: #555;
    font-style: normal;
  }
  blockquote p { margin: 0; }

  /* 표 */
  table { width: 100%; border-collapse: collapse; font-size: 0.82em; margin-top: 0.4em; }
  th { background: #252422; color: #fff; padding: 9px 13px; text-align: left; font-weight: 700; }
  th:last-child { background: #e07a5f; }
  td { padding: 8px 13px; border-bottom: 1px solid #ddd; vertical-align: top; }
  tr:nth-child(even) td { background: rgba(0,0,0,0.03); }

  /* 목록 */
  ul, ol { padding-left: 1.3em; margin: 0.25em 0; }
  li { margin-bottom: 0.28em; }

  /* 강조 */
  strong { color: #252422; font-weight: 900; }

  /* 페이지 번호 */
  section::after { font-size: 0.7em; color: #e07a5f; font-weight: 700; }

  /* ══════════════════════════════════════════════
     공통 컴포넌트
  ══════════════════════════════════════════════ */

  /* 배지 */
  .badge {
    display: inline-block;
    background: #252422;
    color: #fff;
    font-size: 0.46em;
    font-weight: 700;
    padding: 3px 12px;
    letter-spacing: 0.09em;
  }

  /* 슬라이드 상단 영역 (배지 + 제목) */
  .s-top { text-align: center; margin-bottom: 0.45em; }
  .s-top .badge { display: block; width: fit-content; margin: 0 auto 0.4em; }
  .s-top h1 {
    border-bottom: none;
    display: block;
    font-size: 1.35em;
    text-align: center;
    margin: 0;
  }

  /* 서브타이틀 */
  .slide-sub {
    font-size: 0.7em;
    color: #888;
    text-align: center;
    margin: -0.2em 0 0.55em;
  }

  /* ══════════════════════════════════════════════
     Layout 1 — 목차 (TOC)
  ══════════════════════════════════════════════ */
  section.toc {
    flex-direction: row !important;
    padding: 0 !important;
  }
  .toc-l {
    width: 272px;
    padding: 0 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 14px;
    flex-shrink: 0;
  }
  .toc-big {
    font-size: 2.5em;
    font-weight: 900;
    color: #252422;
    line-height: 1.0;
  }
  .toc-r {
    flex: 1;
    background: #e5ddd0;
    padding: 32px 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .toc-item {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    padding: 10px 0;
    border-bottom: 1px solid #CCC5B9;
  }
  .toc-item:first-child { border-top: 1px solid #CCC5B9; }
  .t-num  { font-size: 1.05em; font-weight: 900; color: #CCC5B9; min-width: 28px; padding-top: 1px; }
  .t-title { font-size: 0.76em; font-weight: 700; color: #252422; margin-bottom: 2px; }
  .t-desc  { font-size: 0.6em;  color: #999; line-height: 1.4; }

  /* ══════════════════════════════════════════════
     Layout 2 — 문제/해결 방향 (2-panel)
  ══════════════════════════════════════════════ */
  .two-panel {
    display: flex;
    gap: 4px;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }
  .panel-l, .panel-r {
    flex: 1;
    background: #e5ddd0;
    padding: 0.85em 1.05em;
    font-size: 0.79em;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .panel-header {
    font-size: 0.82em;
    font-weight: 700;
    padding: 0.33em 0.85em;
    margin: -0.85em -1.05em 0.65em;
    text-align: center;
    flex-shrink: 0;
    color: #fff;
  }
  .panel-header.left  { background: #7a7570; }
  .panel-header.right { background: #252422; }
  .panel-l p, .panel-r p { margin: 0 0 0.45em; line-height: 1.55; }
  .panel-l ul, .panel-r ul { padding-left: 1.05em; margin: 0.15em 0; }
  .panel-l ol, .panel-r ol { padding-left: 1.05em; margin: 0.15em 0; }
  .panel-l li, .panel-r li { margin-bottom: 0.32em; line-height: 1.5; }

  /* ══════════════════════════════════════════════
     Layout 3 — 순서 (프로세스 플로우)
  ══════════════════════════════════════════════ */
  .proc-wrap {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
  }
  .proc-heads {
    display: flex;
    height: 38px;
    margin-bottom: 4px;
    flex-shrink: 0;
  }
  .ph {
    flex: 1;
    background: #8a8478;
    color: #fff;
    font-size: 0.6em;
    font-weight: 700;
    line-height: 38px;
    text-align: center;
    position: relative;
    margin-right: -12px;
    padding: 0 6px 0 18px;
    z-index: 5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ph:nth-child(2) { z-index: 4; }
  .ph:nth-child(3) { z-index: 3; }
  .ph:nth-child(4) { z-index: 2; }
  .ph:nth-child(5), .ph:nth-child(6) { z-index: 1; }
  .ph::after {
    content: '';
    position: absolute;
    right: -12px; top: 0;
    width: 0; height: 0;
    border-top: 19px solid transparent;
    border-bottom: 19px solid transparent;
    border-left: 12px solid #8a8478;
  }
  .ph.last { background: #252422; margin-right: 0; padding-left: 20px; }
  .ph.last::after { display: none; }
  .proc-rows { flex: 1; display: flex; flex-direction: column; gap: 2px; overflow: hidden; }
  .pr { display: grid; gap: 2px; }
  .pc { font-size: 0.63em; line-height: 1.5; color: #403D39; padding: 0.55em 0.75em; }
  .pr:nth-child(odd)  .pc { background: rgba(255,255,255,0.88); }
  .pr:nth-child(even) .pc { background: #e5ddd0; }

  /* ══════════════════════════════════════════════
     Layout 4 — 비교표 (Comparison)
  ══════════════════════════════════════════════ */
  .cmp-wrap { flex: 1; min-height: 0; overflow: hidden; }
  .cmp-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
  .cmp-table th { padding: 0.5em 0.75em; text-align: center; font-size: 0.7em; font-weight: 700; }
  .cmp-table th.l { background: #7a7570; color: #fff; }
  .cmp-table th.m { background: #CCC5B9; color: #252422; font-size: 0.6em; width: 14%; }
  .cmp-table th.r { background: #252422; color: #fff; }
  .cmp-table td {
    padding: 0.45em 0.75em;
    font-size: 0.68em;
    text-align: center;
    color: #403D39;
    border-bottom: 1px solid #CCC5B9;
    vertical-align: middle;
  }
  .cmp-table tr:nth-child(even) td { background: rgba(0,0,0,0.025); }
  .cmp-table td.m { background: #ddd7cc; color: #888; font-size: 0.6em; }
  .cmp-table td strong { font-weight: 900; }

  /* ══════════════════════════════════════════════
     Layout 5 — 줄글 (Prose)
  ══════════════════════════════════════════════ */
  .prose-panel {
    flex: 1;
    background: #e5ddd0;
    padding: 1em 1.35em;
    min-height: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 0.55em;
  }
  .prose-sub {
    font-size: 0.8em;
    font-weight: 700;
    text-align: center;
    color: #252422;
    flex-shrink: 0;
  }
  .prose-body { font-size: 0.76em; line-height: 1.88; color: #403D39; }
  .prose-body strong { font-weight: 900; }
  .prose-body mark  { background: #252422; color: #fff; padding: 0 3px; }

  /* ⑤⑥ 라벨 */
  .sec-label {
    color: #e07a5f;
    font-size: 0.68em;
    font-weight: 700;
    margin: 0.65em 0 0.15em;
    flex-shrink: 0;
  }
  .sec-label:first-child { margin-top: 0; }
  .sec-divider {
    border: none;
    border-top: 1px solid #CCC5B9;
    margin: 0.75em 0;
    flex-shrink: 0;
  }
---"""

# ── 파싱 유틸 ─────────────────────────────────────────────────

def is_template(text: str) -> bool:
    return not text or any(hint in text for hint in TEMPLATE_HINTS)


def parse_showcase(path: Path) -> tuple[str, dict]:
    content = path.read_text(encoding="utf-8")

    title_m = re.search(r"^#\s+(.+)", content, re.MULTILINE)
    raw = title_m.group(1).strip() if title_m else ""
    name_m = re.match(r"\[(.+?)\]", raw)
    name = name_m.group(1) if name_m else (raw.replace("AI Camp2 Showcase", "").strip() or path.parent.name)

    sections: dict[str, str] = {}
    for num in "①②③④⑤⑥":
        pat = rf"## {re.escape(num)}\s+[^\n]+\n(.*?)(?=\n## [①②③④⑤⑥]|$)"
        m = re.search(pat, content, re.DOTALL)
        text = m.group(1).strip() if m else ""
        text = re.sub(r"\n---\s*$", "", text).strip()
        sections[num] = "" if is_template(text) else text

    return name, sections


def first_sentence(text: str) -> str:
    for line in text.splitlines():
        line = line.strip().lstrip("#").lstrip("-").lstrip("*").strip()
        line = re.sub(r'^\d+[.)]\s*', '', line).strip()
        if line and not line.startswith(">"):
            return line[:120] + ("…" if len(line) > 120 else "")
    return ""


def fallback(text: str, placeholder: str = "(작성 중)") -> str:
    return text if text else placeholder


# ── 콘텐츠 파싱 헬퍼 ─────────────────────────────────────────

def parse_list_items(text: str) -> list[str]:
    """번호/불릿 항목 추출."""
    items = []
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r'^\d+[.)]\s+(.+)', line)
        if m:
            items.append(m.group(1).strip())
            continue
        m = re.match(r'^[-*]\s+(.+)', line)
        if m:
            items.append(m.group(1).strip())
    return items


def extract_flow_steps(text: str) -> list[str]:
    """'(A → B → C)' 패턴에서 단계 추출."""
    m = re.search(r'[（(]([^）)\n]+(?:→[^）)\n]+)+)[）)]', text)
    if not m:
        return []
    raw = [s.strip() for s in m.group(1).split('→') if s.strip()]
    steps = []
    for step in raw[:6]:
        step = re.sub(r'\s*[（(][^）)]*[）)]\s*', '', step).strip()
        if len(step) > 11:
            words = step.split()
            step = ' '.join(words[:2]) if len(' '.join(words[:2])) <= 11 else words[0][:11]
        steps.append(step)
    return steps


# ── HTML 생성 헬퍼 ────────────────────────────────────────────

def md_to_html(text: str) -> str:
    """기본 마크다운 → HTML (bold, list, paragraph)."""
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        ln = lines[i].strip()
        if re.match(r'^[-*]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^[-*]\s+', lines[i].strip()):
                items.append(re.sub(r'^[-*]\s+', '', lines[i].strip()))
                i += 1
            out.append('<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>')
            continue
        if re.match(r'^\d+[.)]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\d+[.)]\s+', lines[i].strip()):
                items.append(re.sub(r'^\d+[.)]\s+', '', lines[i].strip()))
                i += 1
            out.append('<ol>' + ''.join(f'<li>{it}</li>' for it in items) + '</ol>')
            continue
        if ln:
            out.append(f'<p>{ln}</p>')
        i += 1
    return '\n'.join(out)


def gen_flow_html(steps: list[str]) -> str:
    """화살표 플로우 헤더 HTML 생성."""
    if not steps:
        return ""
    n = len(steps)
    items = []
    for i, step in enumerate(steps):
        cls = "ph last" if i == n - 1 else "ph"
        items.append(f'<div class="{cls}">{step}</div>')
    return f'<div class="proc-heads">{"".join(items)}</div>'


def gen_compare_table(old_items: list[str], new_items: list[str],
                      left_label: str = "② 기존 방식",
                      right_label: str = "④ 자동화 후") -> str:
    """비교표 HTML 생성."""
    n = max(len(old_items), len(new_items))
    while len(old_items) < n:
        old_items.append("—")
    while len(new_items) < n:
        new_items.append("—")

    rows = []
    for old, new in zip(old_items, new_items):
        lbl_m = re.match(r'^([^:：]{2,8})[：:]\s*', old)
        lbl = lbl_m.group(1).strip() if lbl_m else "비교"
        old_s = old[:75] + ("…" if len(old) > 75 else "")
        new_s = new[:75] + ("…" if len(new) > 75 else "")
        rows.append(
            f'<tr><td>{old_s}</td><td class="m">{lbl}</td><td>{new_s}</td></tr>'
        )

    return (
        f'<div class="cmp-wrap">'
        f'<table class="cmp-table">'
        f'<thead><tr>'
        f'<th class="l">{left_label}</th>'
        f'<th class="m">구분</th>'
        f'<th class="r">{right_label}</th>'
        f'</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        f'</table></div>'
    )


# ── 슬라이드 생성 함수 ────────────────────────────────────────

def slide_cover(name: str, s: dict) -> str:
    """1장: 커버 (이름 + 요약)"""
    s1, s3, s4 = s.get("①", ""), s.get("③", ""), s.get("④", "")
    return (
        f"# {name}\n\n"
        f"> {first_sentence(s1) or '(작성 중)'}\n\n"
        f"**문제** {first_sentence(s1) or '(작성 중)'}\n\n"
        f"**해결 방향** {first_sentence(s3) or '(작성 중)'}\n\n"
        f"**현재 구현** {first_sentence(s4) or '(작성 중)'}"
    )


def slide_toc(name: str, s: dict) -> str:
    """2장: 목차 — TOC layout"""
    sec_info = [
        ("01", "① 해결하고 싶은 문제",  s.get("①", "")),
        ("02", "② 기존 방식의 병목",    s.get("②", "")),
        ("03", "③ 지향했던 방향성",     s.get("③", "")),
        ("04", "④ 현재 구현 단계",      s.get("④", "")),
        ("05", "⑤ 추후 과제",           s.get("⑤", "")),
        ("06", "⑥ 소감",                s.get("⑥", "")),
    ]
    items_html = ""
    for num, title, content in sec_info:
        desc = first_sentence(content) or "작성 중"
        desc_s = desc[:54] + ("…" if len(desc) > 54 else "")
        items_html += (
            f'<div class="toc-item">'
            f'<div class="t-num">{num}</div>'
            f'<div><div class="t-title">{title}</div>'
            f'<div class="t-desc">{desc_s}</div></div>'
            f'</div>\n'
        )
    return (
        "<!-- _class: toc -->\n\n"
        f'<div class="toc-l">'
        f'<span class="badge">Contents</span>'
        f'<div class="toc-big">{name}</div>'
        f'</div>\n'
        f'<div class="toc-r">\n{items_html}</div>'
    )


def slide_problem(name: str, s: dict) -> str:
    """3장: 문제/해결 방향 — 2-panel (② 병목 | ③ 방향)"""
    s1, s2, s3 = s.get("①", ""), s.get("②", ""), s.get("③", "")
    s2_html = md_to_html(fallback(s2))
    s3_html = md_to_html(fallback(s3))
    subtitle = (first_sentence(s1) or "")[:90]

    return (
        f'<div class="s-top">'
        f'<span class="badge">문제 &amp; 해결 방향</span>'
        f'<h1>{name}</h1>'
        f'</div>\n'
        + (f'<p class="slide-sub">{subtitle}</p>\n' if subtitle else "")
        + f'<div class="two-panel">\n'
        f'  <div class="panel-l">'
        f'<div class="panel-header left">② 기존 방식의 병목</div>'
        f'{s2_html}'
        f'</div>\n'
        f'  <div class="panel-r">'
        f'<div class="panel-header right">③ 지향했던 방향성</div>'
        f'{s3_html}'
        f'</div>\n'
        f'</div>'
    )


def slide_impl(name: str, s: dict) -> str:
    """4장: 현재 구현 단계 — 플로우 + 비교표"""
    s2, s4 = s.get("②", ""), s.get("④", "")

    flow_steps = extract_flow_steps(s4)
    old_items  = parse_list_items(s2)
    # ④ 에서 화살표 포함 항목(플로우 설명)은 제외한 실제 구현 내용만 추출
    new_items  = [it for it in parse_list_items(s4) if '→' not in it]

    flow_html  = gen_flow_html(flow_steps)

    if old_items and new_items:
        body_html = (flow_html + "\n" if flow_html else "") + gen_compare_table(old_items, new_items)
    elif flow_html:
        body_html = flow_html + f'\n<div class="prose-panel">{md_to_html(fallback(s4))}</div>'
    else:
        body_html = f'<div class="prose-panel">{md_to_html(fallback(s4))}</div>'

    return (
        f'<div class="s-top">'
        f'<span class="badge">현재 구현 단계</span>'
        f'<h1>{name}</h1>'
        f'</div>\n'
        f'{body_html}'
    )


def slide_reflection(name: str, s: dict) -> str:
    """5장: 추후 과제 & 소감 — prose panel"""
    s5, s6 = s.get("⑤", ""), s.get("⑥", "")
    s5_html = md_to_html(fallback(s5))
    s6_html = md_to_html(fallback(s6))

    return (
        f'<div class="s-top">'
        f'<span class="badge">추후 과제 &amp; 소감</span>'
        f'<h1>{name}</h1>'
        f'</div>\n'
        f'<div class="prose-panel">\n'
        f'<p class="sec-label">⑤ 추후 과제</p>\n'
        f'<div class="prose-body">{s5_html}</div>\n'
        f'<hr class="sec-divider">\n'
        f'<p class="sec-label">⑥ 소감</p>\n'
        f'<div class="prose-body">{s6_html}</div>\n'
        f'</div>'
    )


# ── 발표자별 슬라이드 조합 ────────────────────────────────────

def slides_for_person(name: str, s: dict) -> list[str]:
    slides = [
        slide_cover(name, s),
        slide_toc(name, s),
        slide_problem(name, s),
        slide_impl(name, s),
        slide_reflection(name, s),
    ]
    return slides


# ── 전체 발표 마크다운 조합 ───────────────────────────────────

def build_presentation(persons: list[tuple[str, dict]]) -> str:
    chunks = [MARP_HEADER]
    chunks.append("<!-- _class: divider -->\n\n# 우리가 만든 것들")

    for name, sections in persons:
        slides = slides_for_person(name, sections)
        slides[0]  = f"<!-- === 발표자: {name} === -->\n\n{slides[0]}"
        slides[-1] = f"{slides[-1]}\n\n<!-- === /발표자: {name} === -->"
        chunks.extend(slides)

    return "\n\n---\n\n".join(chunks) + "\n"


# ── CSS 최신화 ────────────────────────────────────────────────

def update_css():
    """showcase.md 의 YAML 프런트매터(CSS)만 MARP_HEADER로 교체."""
    if not OUTPUT_MD.exists():
        print(f"오류: {OUTPUT_MD} 파일이 없습니다.")
        sys.exit(1)

    content = OUTPUT_MD.read_text(encoding="utf-8")
    pattern = re.compile(r"^---\n.*?^---", re.DOTALL | re.MULTILINE)
    m = pattern.search(content)
    if not m:
        print("오류: showcase.md에서 YAML 프런트매터를 찾을 수 없습니다.")
        sys.exit(1)

    updated = content[: m.start()] + MARP_HEADER + content[m.end():]
    OUTPUT_MD.write_text(updated, encoding="utf-8")
    print(f"CSS 최신화 완료: {OUTPUT_MD}")


# ── 메인 ─────────────────────────────────────────────────────

def main():
    if "--update-css" in sys.argv:
        update_css()
        return

    print("SHOWCASE.md 파일 수집 중...\n")

    if not SUBMISSIONS_DIR.exists():
        print(f"오류: {SUBMISSIONS_DIR} 폴더가 없습니다.")
        sys.exit(1)

    persons = []
    for person_dir in sorted(SUBMISSIONS_DIR.iterdir()):
        if not person_dir.is_dir():
            continue
        f = person_dir / "SHOWCASE.md"
        if not f.exists():
            continue
        name, sections = parse_showcase(f)
        filled = sum(1 for v in sections.values() if v)
        persons.append((name, sections))
        print(f"  ✓ {person_dir.name:<15} ({name})  — {filled}/6 항목 작성됨")

    if not persons:
        print("\n제출된 SHOWCASE.md 파일이 없습니다.")
        sys.exit(1)

    print(f"\n총 {len(persons)}명 파싱 완료. 슬라이드 생성 중...")

    SLIDES_DIR.mkdir(exist_ok=True)
    md = build_presentation(persons)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"마크다운 생성: {OUTPUT_MD}")

    try:
        subprocess.run(
            ["marp", str(OUTPUT_MD), "--pdf", "--allow-local-files", "-o", str(OUTPUT_PDF)],
            check=True, capture_output=True,
        )
        print(f"PDF 생성 완료: {OUTPUT_PDF}")
    except FileNotFoundError:
        print(
            "\n⚠️  marp CLI가 없습니다. HTML 빌드는 build_slides.sh를 사용하세요:\n"
            "    bash scripts/build_slides.sh"
        )
    except subprocess.CalledProcessError as e:
        print(f"\n오류: {e.stderr.decode()}")


if __name__ == "__main__":
    main()
