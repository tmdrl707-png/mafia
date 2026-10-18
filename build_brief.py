#!/usr/bin/env python3
import json, sys, html, datetime, pathlib

src = sys.argv[1] if len(sys.argv) > 1 else "news.json"
data = json.loads(pathlib.Path(src).read_text(encoding="utf-8"))

date = data.get("date") or datetime.date.today().isoformat()
items = data.get("items", [])
if not (6 <= len(items) <= 10):
    print(f"주의: 기사 {len(items)}건 — 권장 범위(6~10건)를 벗어남. 그대로 진행합니다.")

try:
    d = datetime.date.fromisoformat(date)
    WD = "월화수목금토일"[d.weekday()]
    date_ko = f"{d.year}년 {d.month}월 {d.day}일 {WD}요일"
    date_tag = d.isoformat()
except Exception:
    date_ko = date
    date_tag = date

E = lambda s: html.escape(str(s or ""))

CAT_COLOR = {
    "정치": "#7C3AED", "경제": "#0F766E", "사회": "#DC2626",
    "교육": "#2563EB", "문화": "#D97706", "국제": "#4338CA",
    "IT·산업": "#0891B2", "IT·문화": "#0891B2", "생활": "#65A30D",
}
DEFAULT_COLOR = "#6B7280"

cover_rows = "".join(
    f"""<div class="h-row">
          <div class="h-num">{i+1:02d}</div>
          <div class="h-body">
            <div class="h-title">{E(it.get('title'))}</div>
            <div class="h-meta">{E(it.get('press'))}{' · ' + E(it.get('category')) if it.get('category') else ''}</div>
          </div>
        </div>"""
    for i, it in enumerate(items))

def card(i, it):
    cat = it.get("category") or "뉴스"
    col = CAT_COLOR.get(cat, DEFAULT_COLOR)
    pts = "".join(f"<li>{E(p)}</li>" for p in (it.get("points") or [])[:3])
    ctx = it.get("context")
    return f"""
<div class="card" style="border-left-color:{col}">
  <div class="c-head">
    <span class="c-num" style="color:{col}">{i+1:02d}</span>
    <span class="c-cat" style="background:{col}">{E(cat)}</span>
    <span class="c-press">{E(it.get('press'))}</span>
  </div>
  <div class="c-title">{E(it.get('title'))}</div>
  <div class="c-lead">{E(it.get('summary'))}</div>
  {f'<ul class="c-points">{pts}</ul>' if pts else ''}
  {f'<div class="c-ctx"><span>배경</span> {E(ctx)}</div>' if ctx else ''}
</div>"""

def card_pages():
    out = []
    for s in range(0, len(items), 2):
        pair = items[s:s + 2]
        body = "".join(card(s + j, it) for j, it in enumerate(pair))
        if len(pair) == 1:
            body += '<div class="card empty"></div>'
        out.append(f'<section class="page cards">{body}</section>')
    return "".join(out)

CSS = """
@page { size: A4; margin: 18mm 15mm 14mm 15mm; }
* { box-sizing: border-box; }
body { font-family: "Pretendard", "맑은 고딕", "Noto Sans CJK KR", sans-serif;
       color: #111827; margin: 0; line-height: 1.6; }
.cover { page-break-after: always; }
.c-kicker { font-size: 11pt; font-weight: 800; color: #1D4ED8; letter-spacing: 2px; }
.c-big { font-size: 34pt; font-weight: 900; letter-spacing: -1px; margin: 10px 0 6px; }
.c-date { font-size: 13pt; color: #6B7280; margin-bottom: 20px; }
.c-rule { height: 3px; background: #111827; margin-bottom: 16px; }
.h-row { display: flex; gap: 14px; padding: 10px 0; border-bottom: 1px solid #E5E7EB; }
.h-num { font-size: 14pt; font-weight: 800; color: #1D4ED8; min-width: 32px; }
.h-title { font-size: 12.5pt; font-weight: 700; line-height: 1.45; }
.h-meta { font-size: 9pt; color: #9CA3AF; margin-top: 2px; }
.page.cards { page-break-before: always; padding-top: 4mm; }
.card { height: 118mm; margin-bottom: 10mm; background: #FFFFFF;
        border: 1px solid #E5E7EB; border-left: 6px solid #999; border-radius: 8px;
        padding: 11mm 10mm 11mm 12mm; page-break-inside: avoid; }
.card:last-child { margin-bottom: 0; }
.card.empty { border-color: transparent; background: transparent; }
.c-head { display: flex; align-items: center; gap: 9px; margin-bottom: 10px; }
.c-num { font-size: 14pt; font-weight: 900; }
.c-cat { font-size: 9pt; font-weight: 700; color: #FFFFFF; padding: 3px 10px; border-radius: 20px; }
.c-press { font-size: 9.5pt; color: #9CA3AF; margin-left: auto; }
.c-title { font-size: 20pt; font-weight: 900; line-height: 1.32; letter-spacing: -0.4px;
           margin-bottom: 10px; }
.c-lead { font-size: 12pt; line-height: 1.75; color: #1F2937; }
.c-points { margin: 14px 0 0; padding-left: 18px; }
.c-points li { font-size: 11pt; line-height: 1.65; color: #4B5563; margin-bottom: 6px; }
.c-ctx { margin-top: 12px; padding-top: 10px; border-top: 1px solid #E5E7EB;
         font-size: 10.5pt; line-height: 1.65; color: #6B7280; }
.c-ctx span { font-weight: 800; color: #1D4ED8; margin-right: 4px; }
"""

DOC = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="cover">
  <div class="c-kicker">MORNING BRIEF</div>
  <div class="c-big">오늘의 뉴스 {len(items)}</div>
  <div class="c-date">{E(date_ko)}</div>
  <div class="c-rule"></div>
  {cover_rows}
</div>
{card_pages()}
</body></html>"""

out = f"브리핑_{date_tag}.pdf"

from weasyprint import HTML as WHTML
WHTML(string=DOC).write_pdf(out)
npages = 1 + (len(items) + 1) // 2
print(f"완성: {out}  ({len(items)}건 · 총 {npages}쪽)")
