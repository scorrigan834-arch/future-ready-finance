#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Adds the "What if you invested this payment instead?" feature to car-affordability.html.
# Surgical: only inserts the new pieces, preserves everything else (nav fix, search, etc). Idempotent.
import os

F = 'simulations/car-affordability.html'

HTML_BLOCK = '\n\n    <div class="invest-instead" id="investInstead" style="display:none">\n      <div class="ii-head">\n        <div class="ii-icon">📈</div>\n        <div>\n          <div class="ii-title">What if you invested this payment instead?</div>\n          <div class="ii-sub">If you drove a cheaper (or paid-off) car and invested this <b id="ii-amount">$0</b>/mo at a 7% average return:</div>\n        </div>\n      </div>\n      <div class="ii-grid">\n        <div class="ii-card ii-highlight">\n          <div class="ii-years" id="ii-term-label">Over your loan</div>\n          <div class="ii-value" id="ii-term">$0</div>\n          <div class="ii-contrib" id="ii-term-c">vs $0 in payments</div>\n        </div>\n        <div class="ii-card">\n          <div class="ii-years">In 20 years</div>\n          <div class="ii-value" id="ii-20">$0</div>\n          <div class="ii-contrib" id="ii-20c">you\'d put in $0</div>\n        </div>\n        <div class="ii-card">\n          <div class="ii-years">In 30 years</div>\n          <div class="ii-value" id="ii-30">$0</div>\n          <div class="ii-contrib" id="ii-30c">you\'d put in $0</div>\n        </div>\n      </div>\n      <div class="ii-foot">Cars lose value every year; invested money grows. This isn\'t saying never buy a nice car — it\'s showing the real long-term tradeoff so you can decide what\'s worth it.</div>\n    </div>'

CSS_BLOCK = '\n/* ---- Invested Instead feature ---- */\n.invest-instead{background:linear-gradient(135deg,#0B1929,#0f2236);border-radius:16px;padding:1.5rem 1.6rem;margin-top:1.4rem;box-shadow:0 14px 40px rgba(11,25,41,.25)}\n.ii-head{display:flex;align-items:flex-start;gap:.9rem;margin-bottom:1.2rem}\n.ii-icon{flex-shrink:0;width:2.6rem;height:2.6rem;border-radius:50%;background:rgba(14,165,160,.18);display:flex;align-items:center;justify-content:center;font-size:1.3rem}\n.ii-title{font-family:"Playfair Display",serif;font-size:1.12rem;font-weight:700;color:#fff;margin-bottom:.25rem;line-height:1.2}\n.ii-sub{font-size:.85rem;color:rgba(255,255,255,.62);line-height:1.5}\n.ii-sub b{color:#3fd0c9}\n.ii-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin-bottom:1rem}\n.ii-card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:1.1rem .9rem;text-align:center}\n.ii-card.ii-highlight{background:rgba(14,165,160,.12);border-color:rgba(14,165,160,.4)}\n.ii-years{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#94a3b8;margin-bottom:.5rem}\n.ii-card.ii-highlight .ii-years{color:#6ee7b7}\n.ii-value{font-family:"Playfair Display",serif;font-size:1.55rem;font-weight:900;color:#3fd0c9;line-height:1;margin-bottom:.4rem}\n.ii-card.ii-highlight .ii-value{color:#6ee7b7}\n.ii-contrib{font-size:.7rem;color:rgba(255,255,255,.45);line-height:1.3}\n.ii-foot{font-size:.78rem;color:rgba(255,255,255,.5);line-height:1.55;border-top:1px solid rgba(255,255,255,.08);padding-top:.85rem}\n@media(max-width:560px){.ii-grid{grid-template-columns:1fr;gap:.6rem}.ii-value{font-size:1.7rem}}'

JS_FUNC = 'function renderInvestInstead(monthly, term){\n  var box=document.getElementById(\'investInstead\');\n  if(!monthly || monthly<=0){ box.style.display=\'none\'; return; }\n  function fv(months){ var r=0.07/12; return monthly*((Math.pow(1+r,months)-1)/r); }\n  // Card 1: invested over the loan term\n  var termYears=Math.round(term/12*10)/10;\n  var termGrown=fv(term);\n  var termContrib=monthly*term;\n  document.getElementById(\'ii-term-label\').textContent=\'Over \'+(term%12===0?(term/12)+\' yrs\':term+\' mos\');\n  document.getElementById(\'ii-term\').textContent=money(Math.round(termGrown));\n  document.getElementById(\'ii-term-c\').textContent=\'vs \'+money(Math.round(termContrib))+\' in payments\';\n  // Cards 2 & 3: 20 and 30 years\n  document.getElementById(\'ii-20\').textContent=money(Math.round(fv(240)));\n  document.getElementById(\'ii-20c\').textContent="you\'d put in "+money(monthly*240);\n  document.getElementById(\'ii-30\').textContent=money(Math.round(fv(360)));\n  document.getElementById(\'ii-30c\').textContent="you\'d put in "+money(monthly*360);\n  document.getElementById(\'ii-amount\').textContent=money(Math.round(monthly));\n  box.style.display=\'block\';\n}'

if not os.path.exists(F):
    print('ERROR: ' + F + ' not found. Run from repo root.'); raise SystemExit(1)

h = open(F, encoding='utf-8').read()

if 'investInstead' in h:
    print('Feature already present — nothing to do.'); raise SystemExit(0)

changes = 0

# 1. Insert HTML after the insightBox div
anchor1 = '<div class="insight-box" id="insightBox"></div>'
if anchor1 in h:
    h = h.replace(anchor1, anchor1 + HTML_BLOCK, 1)
    changes += 1
else:
    print('WARN: insightBox anchor not found')

# 2. Insert CSS before </style>
if '</style>' in h:
    h = h.replace('</style>', CSS_BLOCK + '\n</style>', 1)
    changes += 1
else:
    print('WARN: </style> not found')

# 3. Insert JS function before "function calculate(){"
if 'function calculate(){' in h:
    h = h.replace('function calculate(){', JS_FUNC + '\n\nfunction calculate(){', 1)
    changes += 1
else:
    print('WARN: calculate() not found')

# 4. Insert the call before result is shown
call_anchor = "document.getElementById('result').classList.add('show');"
call_code = "renderInvestInstead(payment, term);\n  " + call_anchor
if call_anchor in h:
    h = h.replace(call_anchor, call_code, 1)
    changes += 1
else:
    print('WARN: result-show anchor not found')

open(F, 'w', encoding='utf-8').write(h)
print('')
print('Done — applied ' + str(changes) + ' of 4 insertions to car-affordability.html')
print('(If all 4 applied, the feature is fully wired.)')
