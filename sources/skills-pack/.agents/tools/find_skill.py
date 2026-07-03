#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

STOP = {"the","a","an","and","or","to","for","of","in","on","with","use","create","make","do","my","this","that","please","need","want"}
SYN = {
  "frontend": {"ui","react","web","design","accessibility"}, "database": {"postgres","drizzle","sql","schema","migration"},
  "deploy": {"deployment","launch","ship","vercel","netlify","render","cloudflare","rollback"},
  "security": {"threat","vulnerability","audit","hardening","auth","secrets","ownership"}, "mobile": {"react-native","winui","app"},
  "docs": {"documentation","adr","openai","writing","pdf"}, "image": {"imagegen","banner","design","screenshot"},
  "test": {"tdd","debug","review","validator","pitfalls","playwright","coverage"}, "crypto": {"defi","blockchain","mev","liquidity","hft"},
  "plan": {"spec","tasks","breakdown","incremental","lifecycle"}, "api": {"interface","rest","graphql","contract"},
  "performance": {"latency","profiling","web-vitals","lighthouse","optimize"}, "observability": {"logging","metrics","tracing","alerts"},
  "idea": {"refine","interview","requirements","clarify"}, "context": {"agents","instructions","source","documentation"},
  "brief": {"caveman","concise","tokens","compress"}, "delegate": {"cavecrew","subagent","investigator","builder","reviewer"},
  "landing": {"design","taste","frontend","marketing","brand"}, "portfolio": {"design","taste","frontend","marketing"},
  "dashboard": {"impeccable","product","ui","audit"}, "prototype": {"huashu","design","html","interactive"},
  "slides": {"huashu","deck","presentation","design"}, "motion": {"huashu","animation","video","design"},
  "marketing": {"marketing","copywriting","cro","ads","growth","launch","pricing"}, "seo": {"seo","search","schema","sitemap","hreflang","geo"},
  "content": {"content","editorial","blog","social","repurpose","calendar"}, "translate": {"translation","transcreation","localization","russian","english"},
  "humanize": {"humanizer","voice","editing","natural","anti-slop"},
}

RU = {
  "ошибка": {"debug","error","failure"}, "ошибку": {"debug","error","failure"}, "баг": {"debug","bug","test"},
  "исправить": {"debug","test","reproducing","regression"}, "починить": {"debug","test","reproducing","regression"}, "сломано": {"debug","failure"},
  "тест": {"test","tdd","coverage"}, "тесты": {"test","tdd","coverage"}, "нестабильный": {"flaky","debug","reproducing","regression"},
  "причина": {"localizing","root","cause","debug"}, "причину": {"localizing","root","cause","debug"},
  "доказать": {"verify","evidence","regression"}, "проверить": {"review","verify","test"},
  "ревью": {"review","quality"}, "безопасность": {"security","audit"},
  "производительность": {"performance","profiling","latency"}, "ускорить": {"performance","optimize"},
  "интерфейс": {"frontend","ui","design"}, "дизайн": {"design","ui"}, "апи": {"api","interface","rest"},
  "деплой": {"deploy","launch","ship"}, "релиз": {"launch","ship","rollback"}, "миграция": {"migration","deprecation"},
  "документация": {"docs","documentation","adr"}, "логирование": {"observability","logging"},
  "план": {"plan","tasks","breakdown"}, "спецификация": {"spec","requirements"}, "идея": {"idea","refine"},
  "контекст": {"context","agents","instructions"}, "кодекс": {"codex","workflow","skills"},
  "кратко": {"caveman","concise","tokens"}, "сжать": {"caveman","compress","tokens"}, "делегировать": {"cavecrew","subagent","investigator","builder","reviewer"},
  "лендинг": {"design","taste","frontend","marketing","brand"}, "портфолио": {"design","taste","frontend","marketing"},
  "дашборд": {"impeccable","product","ui","audit"}, "дашборда": {"impeccable","product","ui","audit"},
  "аудит": {"impeccable","audit","product","ui"}, "прототип": {"huashu","design","html","interactive"},
  "презентация": {"huashu","deck","slides","design"}, "анимация": {"huashu","motion","video","design"},
  "маркетинг": {"marketing","copywriting","cro","ads","growth"}, "сео": {"seo","search","schema","sitemap","geo"},
  "контент": {"content","editorial","blog","social","calendar"}, "перевод": {"translation","transcreation","localization","russian","english"},
  "оживить": {"humanizer","voice","editing","natural"}, "живой": {"humanizer","voice","natural"},
  "живым": {"humanizer","voice","natural"}, "человечным": {"humanizer","voice","natural"},
  "нейросеть": {"humanizer","anti-slop","editing"}, "нейросети": {"humanizer","anti-slop","editing"},
  "русский": {"russian","ru-text","humanizer-ru"}, "русского": {"russian","translation","transcreation"},
  "английский": {"english","translation","transcreation"}, "английского": {"english","translation","transcreation"},
  "локализация": {"localization","transcreation","translation"}, "адаптировать": {"transcreation","localization"},
  "стратегия": {"strategy","plan","marketing"}, "запуск": {"launch","marketing","plan"},
  "линкедин": {"linkedin","social","content"}, "голос": {"voice","brand","humanizer"},
  "бренда": {"brand","voice","marketing"}, "текст": {"copywriting","editing","content","ru-text"},
}

def toks(s): return {x for x in re.findall(r"[^\W_]+(?:-[^\W_]+)*", s.lower(), re.UNICODE) if len(x)>1 and x not in STOP}

def intent_bonus(raw: str, name: str) -> int:
  """High-precision routing for common RU/EN workflows with overlapping vocabularies."""
  score = 0
  ru_to_en = any(x in raw for x in ("с русского на англий", "ru to en", "ru→en", "ru-en", "на английский"))
  en_to_ru = any(x in raw for x in ("с английского на рус", "en to ru", "en→ru", "en-ru", "на русский"))
  transcreation = any(x in raw for x in ("transcreation", "транскреац", "локализ", "адаптируй", "адаптировать"))
  human = any(x in raw for x in ("живой текст", "живым", "человеч", "убери ии", "ии-шност", "ai текст", "нейросетев"))
  russian = any(x in raw for x in ("русск", "russian"))

  if (ru_to_en or transcreation) and name == "bilingual-transcreator": score += 90
  if en_to_ru and name == "en-ru-translator-adv": score += 85
  if human and russian and name in {"humanizer-ru", "ru-editor", "ru-text"}: score += {"humanizer-ru":80,"ru-editor":70,"ru-text":55}[name]
  if human and not russian and name == "humanizer": score += 70

  if any(x in raw for x in ("seo аудит", "сео аудит", "полный seo", "полный сео", "full seo audit")):
    if name == "seo-audit": score += 90
    elif name == "seo": score += 55
    elif name == "marketing-seo-audit": score += 25
  if "linkedin" in raw or "линкедин" in raw:
    if name == "content-linkedin": score += 85
    elif name == "social": score += 30
  if any(x in raw for x in ("голос бренда", "brand voice")):
    if name == "content-linkedin" and ("linkedin" in raw or "линкедин" in raw): score += 30
    if name == "content-setup": score += 20
  if any(x in raw for x in ("маркетинговая стратегия", "маркетинговую стратег", "marketing strategy", "маркетинговый план", "go-to-market", "gtm")):
    if name == "marketing-plan": score += 90
    elif name == "content-strategy": score += 25
    elif name == "marketing-ideas": score += 20
  if any(x in raw for x in ("запуск", "launch")) and name == "launch": score += 55

  # A landing-page translation is a language task, not primarily visual design.
  if (ru_to_en or en_to_ru or transcreation) and name == "design-taste-frontend": score -= 40
  return score

def main():
 p=argparse.ArgumentParser(); p.add_argument('query'); p.add_argument('--top',type=int,default=8); a=p.parse_args()
 root=Path(__file__).resolve().parents[1]
 rows=json.loads((root/'SKILLS_INDEX.json').read_text('utf-8'))
 q=toks(a.query); expanded=set(q)
 for token in list(q):
  expanded |= SYN.get(token,set())
  expanded |= RU.get(token,set())
 scored=[]
 for r in rows:
  n=toks(r['name'].replace('-',' ')); d=toks(r['description']); c=toks(r['category'])
  score=5*len(expanded&n)+2*len(expanded&d)+len(expanded&c)
  raw=a.query.lower()
  if r['name']=='impeccable' and any(x in raw for x in ('dashboard','дашборд','аудит интерфейс','product ui')): score += 20
  if r['name']=='design-taste-frontend' and any(x in raw for x in ('landing','лендинг','portfolio','портфолио','marketing site')): score += 20
  if r['name']=='huashu-design' and any(x in raw for x in ('prototype','прототип','presentation','презентац','slide deck','анимац','narrat')): score += 20
  score += intent_bonus(raw, r['name'])
  if r['name'] in a.query.lower(): score += 20
  if score: scored.append((score,r))
 scored.sort(key=lambda x:(-x[0],x[1]['name']))
 if not scored:
  print('No strong match. Inspect .agents/SKILLS_INDEX.md or use $skill-router.'); return
 for score,r in scored[:a.top]:
  print(f"{score:>3}  ${r['name']}: {r['description']}")
if __name__=='__main__': main()
