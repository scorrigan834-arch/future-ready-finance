#!/usr/bin/env python3
"""
Future Ready Finance — Match the calculator pages to the homepage's navy scheme.

Run from your repo root (where index.html lives):
    python3 restyle_calculators.py

Applies the navy-frame look (approved on the Net Worth calculator) to the 16
standard calculators in simulations/:
  - body background: light gradient -> navy #0B1929
  - nav: opacity .92 -> .85, height 58px -> 62px  (matches homepage)
  - footer: padding 2rem -> 3.5rem 2rem 2rem       (matches homepage)

The white input cards then float on navy, and the already-navy result/projection
sections fit right in.

DELIBERATELY SKIPS two files:
  - kids-money-adventure.html  (its own bright kid-friendly palette)
  - debt-payoff.html           (the redirect page)

Reports exactly what changed per file, and flags anything that didn't get the
full set so nothing is silently missed. Safe to run once.
"""
import os, glob

CALC_DIR = 'simulations'

# Files to leave untouched (each for a good reason)
SKIP = {'kids-money-adventure.html', 'debt-payoff.html'}

# The uniform body background all 16 standard calculators share
OLD_BODY = 'body{font-family:"DM Sans",sans-serif;background:linear-gradient(180deg,#F5F7F6 0%,#ECF1F0 100%);background-attachment:fixed;color:#0B1929;line-height:1.6}'
NEW_BODY = 'body{font-family:"DM Sans",sans-serif;background:#0B1929;background-attachment:fixed;color:#0B1929;line-height:1.6}'

# Nav (matches homepage). Only replace the leading portion so any trailing
# border/props stay intact — we match the exact prefix through height.
OLD_NAV = '.nav{position:sticky;top:0;z-index:200;background:rgba(11,25,41,.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:58px'
NEW_NAV = '.nav{position:sticky;top:0;z-index:200;background:rgba(11,25,41,.85);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:62px'

# Footer (matches homepage). Two variants: with and without margin-top.
FOOTER_VARIANTS = [
    ('.footer{background:#0B1929;padding:2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center}',
     '.footer{background:#0B1929;padding:3.5rem 2rem 2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center}'),
    ('.footer{background:#0B1929;padding:2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center;margin-top:1rem}',
     '.footer{background:#0B1929;padding:3.5rem 2rem 2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center;margin-top:1rem}'),
]

CORE = {'body', 'nav', 'footer'}

files = sorted(glob.glob(os.path.join(CALC_DIR, '*.html')))
print(f"Found {len(files)} files in {CALC_DIR}/  (will skip {len(SKIP)})\n")

changed_count = 0
incomplete = []

for path in files:
    fn = os.path.basename(path)
    if fn in SKIP:
        print(f"  {fn:34s} SKIPPED (intentional)")
        continue
    try:
        content = open(path, encoding='utf-8').read()
    except Exception as e:
        print(f"  {fn:34s} ERROR: {e}")
        continue
    orig = content
    applied = set()

    if OLD_BODY in content:
        content = content.replace(OLD_BODY, NEW_BODY); applied.add('body')
    if OLD_NAV in content:
        content = content.replace(OLD_NAV, NEW_NAV); applied.add('nav')
    for old_ft, new_ft in FOOTER_VARIANTS:
        if old_ft in content:
            content = content.replace(old_ft, new_ft); applied.add('footer'); break

    if content != orig:
        open(path, 'w', encoding='utf-8').write(content)
        changed_count += 1
        missing = CORE - applied
        status = "OK" if not missing else f"MISSING: {', '.join(sorted(missing))}"
        flag = "" if not missing else "  <-- CHECK THIS FILE"
        print(f"  {fn:34s} {status}{flag}")
        if missing:
            incomplete.append((fn, missing))
    else:
        print(f"  {fn:34s} no change (already styled or different CSS?)")

print(f"\nUpdated {changed_count} calculators.")
if incomplete:
    print(f"\n⚠️  {len(incomplete)} file(s) did NOT get all core changes.")
    print("    Copy this list and tell Claude — those need a quick manual touch:")
    for fn, missing in incomplete:
        print(f"      {fn}: missing {', '.join(sorted(missing))}")
else:
    print("✓ All updated calculators received the full set of changes.")

print("\nNext:  git add -A  &&  git commit -m 'restyle calculators to navy homepage look'  &&  git pull --no-edit  &&  git push")
