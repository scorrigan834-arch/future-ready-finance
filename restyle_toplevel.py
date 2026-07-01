#!/usr/bin/env python3
"""Restyle top-level pages: navy body + floating white content card = 'more navy' homepage match.
Handles two families (.wrap and .section/.section-inner) and both DM Sans quote variants.
Reports OK/MISSING per file."""
import sys, re

def restyle(html, fname):
    notes = []
    orig = html

    # Idempotency guard: if already restyled, skip entirely
    if 'More-navy: floating white content cards' in html:
        return html, True, ['already restyled — skipped (safe)']

    # --- 1. BODY → navy (handle both quote variants of DM Sans) ---
    # Match: body{font-family:"DM Sans",sans-serif;background:#F5F7F6;color:#0B1929;line-height:1.6}
    #    or: body{font-family:'DM Sans',sans-serif;background:#F5F7F6;...}
    body_pat = re.compile(r'(body\{font-family:(?:"DM Sans"|\'DM Sans\'),sans-serif;background:)#F5F7F6(;color:#0B1929;line-height:1\.6\})')
    if body_pat.search(html):
        html = body_pat.sub(r'\g<1>#0B1929\g<2>', html)
        notes.append('body→navy OK')
    else:
        notes.append('MISSING: body background pattern')

    # --- 2. Inject the floating-card CSS before </style> ---
    # This restyles .wrap AND .section-inner as floating white cards on the navy body,
    # and adds a navy accent band style. Works for both families.
    card_css = '''
/* ===== More-navy: floating white content cards on navy body ===== */
.wrap{background:#fff;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.28);padding:2.75rem 2.75rem;margin-top:-1.5rem;margin-bottom:3rem;position:relative;z-index:5}
.section{padding:0}
.section-inner{background:#fff;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.28);padding:2.75rem 2.75rem;margin:2rem auto;max-width:1000px;position:relative;z-index:5}
/* first content card tucks up under the hero for a smooth navy→card transition */
.page-hero{padding-bottom:3.5rem}
/* navy accent callout that can break up long white content */
.navy-accent{background:linear-gradient(135deg,#0B1929,#0f2338);border-radius:18px;padding:2rem 2.25rem;margin:2rem 0;color:#fff;box-shadow:0 12px 34px rgba(11,25,41,.25)}
.navy-accent h2,.navy-accent h3{color:#fff !important}
.navy-accent p{color:rgba(255,255,255,.8) !important}
/* buttons match homepage */
.btn-primary{background:#0EA5A0;color:#fff;box-shadow:0 6px 20px rgba(14,165,160,.32)}
.btn-ghost{background:transparent;color:#0B1929;border:1.5px solid #cbd5e1}
@media(max-width:768px){.wrap{padding:1.75rem 1.4rem;margin-top:-1rem}.section-inner{padding:1.75rem 1.4rem}}
'''
    if '</style>' in html:
        html = html.replace('</style>', card_css + '</style>', 1)
        notes.append('card CSS injected')
    else:
        notes.append('MISSING: </style>')

    changed = (html != orig)
    ok = 'MISSING' not in ' '.join(notes)
    return html, ok, notes

if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else ['about.html','resources.html','start-here.html','big-decisions.html','guides.html','life-stages.html']
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh: html = fh.read()
        except FileNotFoundError:
            print(f'  {f}: SKIP (not found)'); continue
        new, ok, notes = restyle(html, f)
        if ok:
            with open(f, 'w', encoding='utf-8') as fh: fh.write(new)
            print(f'  {f}: OK — {"; ".join(notes)}')
        else:
            print(f'  {f}: ⚠️  {"; ".join(notes)} (NOT written)')
