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
---

---

<!-- _class: divider -->

# 우리가 만든 것들

---

<!-- === 발표자: Arin === -->

# Arin

> 배경) 로켓런칭 팀 내에서 매주 미팅을 진행하는데, 미팅 전 노션에 작업 현황을 업데이트해야 하는 작업이 필요했음.

**문제** 배경) 로켓런칭 팀 내에서 매주 미팅을 진행하는데, 미팅 전 노션에 작업 현황을 업데이트해야 하는 작업이 필요했음.

**해결 방향** 파편화된 커뮤니케이션 내용을 취합해 1) 디자인 진행 상황 리스트업 & 정리, 2) 디자인 타임라인을 짜주는 자동화를 만들자!

**현재 구현** 디자인 진행 상황 리스트업 & 정리

---

<!-- _class: toc -->

<div class="toc-l"><span class="badge">Contents</span><div class="toc-big">Arin</div></div>
<div class="toc-r">
<div class="toc-item"><div class="t-num">01</div><div><div class="t-title">① 해결하고 싶은 문제</div><div class="t-desc">배경) 로켓런칭 팀 내에서 매주 미팅을 진행하는데, 미팅 전 노션에 작업 현황을 업데이트해야 하는…</div></div></div>
<div class="toc-item"><div class="t-num">02</div><div><div class="t-title">② 기존 방식의 병목</div><div class="t-desc">요청 경로 파편화: Slack 2개 채널 + 개인 DM + Notion 등 4개 채널에서 각각 수…</div></div></div>
<div class="toc-item"><div class="t-num">03</div><div><div class="t-title">③ 지향했던 방향성</div><div class="t-desc">파편화된 커뮤니케이션 내용을 취합해 1) 디자인 진행 상황 리스트업 & 정리, 2) 디자인 타임라…</div></div></div>
<div class="toc-item"><div class="t-num">04</div><div><div class="t-title">④ 현재 구현 단계</div><div class="t-desc">디자인 진행 상황 리스트업 & 정리</div></div></div>
<div class="toc-item"><div class="t-num">05</div><div><div class="t-title">⑤ 추후 과제</div><div class="t-desc">추가적인 디자인 피드백 사항도 자동 취합해서 정리되도록 구현</div></div></div>
<div class="toc-item"><div class="t-num">06</div><div><div class="t-title">⑥ 소감</div><div class="t-desc">아직도 기본적인 개념에 대한 확립이 미흡하다고는 생각하지만, 그럼에도 불구하고 이런 나도 자동화 …</div></div></div>
</div>

---

<div class="s-top"><span class="badge">문제 &amp; 해결 방향</span><h1>Arin</h1></div>
<p class="slide-sub">배경) 로켓런칭 팀 내에서 매주 미팅을 진행하는데, 미팅 전 노션에 작업 현황을 업데이트해야 하는 작업이 필요했음.</p>
<div class="two-panel">
  <div class="panel-l"><div class="panel-header left">② 기존 방식의 병목</div><ol><li>요청 경로 파편화: Slack 2개 채널 + 개인 DM + Notion 등 4개 채널에서 각각 수동 확인</li><li>요청 형식의 다양성: 요청자마다 요청 형식이 달라 필요한 정보를 다시 확인하거나 정리해야 했음</li><li>수동 복제 관리: 전주 Task list를 복제 → 차주 Task list로 이름, 내용 수정 → 공유하는 반복적인 수동 관리가 필요했음</li><li>정보 누락: 피그마, 기획안, 고객사 클래스 링크 등의 정보를 누락해서 작성</li></ol></div>
  <div class="panel-r"><div class="panel-header right">③ 지향했던 방향성</div><p>파편화된 커뮤니케이션 내용을 취합해 1) 디자인 진행 상황 리스트업 & 정리, 2) 디자인 타임라인을 짜주는 자동화를 만들자!</p></div>
</div>

---

<div class="s-top"><span class="badge">현재 구현 단계</span><h1>Arin</h1></div>
<div class="proc-heads"><div class="ph">수집</div><div class="ph">필터</div><div class="ph">Human</div><div class="ph last">Figma 플러그인</div></div>
<div class="cmp-wrap"><table class="cmp-table"><thead><tr><th class="l">② 기존 방식</th><th class="m">구분</th><th class="r">④ 자동화 후</th></tr></thead><tbody><tr><td>요청 경로 파편화: Slack 2개 채널 + 개인 DM + Notion 등 4개 채널에서 각각 수동 확인</td><td class="m">비교</td><td>디자인 진행 상황 리스트업 & 정리</td></tr><tr><td>요청 형식의 다양성: 요청자마다 요청 형식이 달라 필요한 정보를 다시 확인하거나 정리해야 했음</td><td class="m">비교</td><td>수집 스케줄: 월~금 9, 10, 11, 13, 14, 15, 16, 17, 18, 19시 정각 (오후 12시, 아린 연차 날 제외)</td></tr><tr><td>수동 복제 관리: 전주 Task list를 복제 → 차주 Task list로 이름, 내용 수정 → 공유하는 반복적인 수동 관리가 필요했…</td><td class="m">수동 복제 관리</td><td>1차, 2차 시안 공유와 같은 Work Flow 날짜 자동 계산해서 작성</td></tr><tr><td>정보 누락: 피그마, 기획안, 고객사 클래스 링크 등의 정보를 누락해서 작성</td><td class="m">정보 누락</td><td>미완료 Task 자동 이월 로직</td></tr><tr><td>—</td><td class="m">비교</td><td>디자인 타임라인 정리</td></tr></tbody></table></div>

---

<div class="s-top"><span class="badge">추후 과제 &amp; 소감</span><h1>Arin</h1></div>
<div class="prose-panel">
<p class="sec-label">⑤ 추후 과제</p>
<div class="prose-body"><p>추가적인 디자인 피드백 사항도 자동 취합해서 정리되도록 구현</p></div>
<hr class="sec-divider">
<p class="sec-label">⑥ 소감</p>
<div class="prose-body"><p>아직도 기본적인 개념에 대한 확립이 미흡하다고는 생각하지만, 그럼에도 불구하고 이런 나도 자동화 도구를 만들 수 있다는 뿌듯한 경험을 했습니다. 클로드는 내가 만들고자 하는 뚜렷한 작업 플로우와 디테일한 조건만 잘 제시해준다면 누구나 쉽게 만들 수 있겠다는 가능성도 체감할 수 있었습니다.</p></div>
</div>

<!-- === /발표자: Arin === -->
