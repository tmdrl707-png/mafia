#!/usr/bin/env python3
import json, sys, html, datetime, pathlib

src = sys.argv[1] if len(sys.argv) > 1 else "news.json"
data = json.loads(pathlib.Path(src).read_text(encoding="utf-8"))
items = data.get("items", [])
try:
    d = datetime.date.fromisoformat(data["date"])
    date_ko = f"{d.year}년 {d.month}월 {d.day}일 {'월화수목금토일'[d.weekday()]}요일"
    tag = d.isoformat()
except Exception:
    date_ko = tag = str(data.get("date", ""))

E = lambda s: html.escape(str(s or ""))
COL = {"정치": "#7C3AED", "경제": "#0F766E", "사회": "#DC2626", "교육": "#2563EB",
       "문화": "#D97706", "국제": "#4338CA", "IT·산업": "#0891B2", "IT·문화": "#0891B2",
       "생활": "#65A30D"}

def card(i, it):
    c = COL.get(it.get("category"), "#6B7280")
    pts = "".join(f"<li>{E(p)}</li>" for p in (it.get("points") or [])[:3])
    url = it.get("url")
    link = f'<a class="src" href="{E(url)}" target="_blank" rel="noopener">원문 보기</a>' if url else ""
    ctx = it.get("context")
    return f"""<article class="card" style="--c:{c}">
<div class="head"><span class="num">{i+1:02d}</span><span class="cat">{E(it.get('category') or '뉴스')}</span><span class="press">{E(it.get('press'))}</span></div>
<h2>{E(it.get('title'))}</h2>
<p class="lead">{E(it.get('summary'))}</p>
{f'<ul>{pts}</ul>' if pts else ''}
{f'<p class="ctx"><b>배경</b> {E(ctx)}</p>' if ctx else ''}
{link}
</article>"""

toc = "".join(f'<li><a href="#n{i+1}"><span>{i+1:02d}</span>{E(it.get("title"))}</a></li>' for i, it in enumerate(items))
cards = "".join(f'<div id="n{i+1}">{card(i, it)}</div>' for i, it in enumerate(items))

PAGE = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>아침 뉴스 브리핑</title>
<style>
:root{{--bg:#F4F5F7;--card:#fff;--ink:#111827;--sub:#4B5563;--mute:#9CA3AF;--line:#E5E7EB;--acc:#1D4ED8}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0F1115;--card:#181B21;--ink:#F3F4F6;--sub:#C4C9D2;--mute:#7C8594;--line:#2A2F38;--acc:#7AA2FF}}}}
:root[data-theme="dark"]{{--bg:#0F1115;--card:#181B21;--ink:#F3F4F6;--sub:#C4C9D2;--mute:#7C8594;--line:#2A2F38;--acc:#7AA2FF}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:Pretendard,-apple-system,"Noto Sans KR","맑은 고딕",sans-serif;line-height:1.65;-webkit-text-size-adjust:100%}}
main{{max-width:680px;margin:0 auto;padding:24px 16px 56px}}
.kicker{{font-size:12px;font-weight:800;letter-spacing:2px;color:var(--acc)}}
h1{{font-size:30px;line-height:1.2;margin:6px 0 4px;letter-spacing:-.5px}}
.date{{color:var(--mute);font-size:14px;margin-bottom:16px}}
.pdf{{display:inline-block;margin:0 0 18px;padding:10px 16px;border-radius:10px;background:var(--acc);color:#fff;font-weight:700;font-size:14px;text-decoration:none}}
.toc{{list-style:none;margin:0 0 22px;padding:0;background:var(--card);border:1px solid var(--line);border-radius:12px}}
.toc li+li{{border-top:1px solid var(--line)}}
.toc a{{display:flex;gap:12px;padding:12px 14px;color:var(--ink);text-decoration:none;font-weight:600;font-size:15px}}
.toc span{{color:var(--acc);font-weight:800;min-width:24px}}
.card{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--c);border-radius:12px;padding:18px 16px;margin-bottom:14px}}
.head{{display:flex;align-items:center;gap:8px;margin-bottom:8px}}
.num{{font-weight:900;color:var(--c)}}
.cat{{background:var(--c);color:#fff;font-size:12px;font-weight:700;padding:2px 10px;border-radius:20px}}
.press{{margin-left:auto;color:var(--mute);font-size:12px}}
h2{{font-size:20px;line-height:1.35;margin:0 0 8px;letter-spacing:-.3px}}
.lead{{margin:0;color:var(--sub);font-size:15.5px}}
ul{{margin:12px 0 0;padding-left:20px;color:var(--sub);font-size:15px}}
li{{margin-bottom:4px}}
.ctx{{margin:12px 0 0;padding-top:10px;border-top:1px solid var(--line);color:var(--mute);font-size:14px}}
.ctx b{{color:var(--acc);margin-right:4px}}
.src{{display:inline-block;margin-top:10px;color:var(--acc);font-size:14px;font-weight:600}}
</style></head><body><main>
<div class="kicker">MORNING BRIEF</div>
<h1>오늘의 뉴스 {len(items)}</h1>
<div class="date">{E(date_ko)}</div>
<a class="pdf" href="브리핑_{E(tag)}.pdf">PDF 내려받기</a>
<ol class="toc">{toc}</ol>
{cards}
</main></body></html>"""

pathlib.Path("brief.html").write_text(PAGE, encoding="utf-8")
print(f"완성: brief.html ({len(items)}건)")
