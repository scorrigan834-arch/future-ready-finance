#!/usr/bin/env python3
"""
Future Ready Finance — Match all 37 guide pages to the homepage's navy color scheme.

Run from your repo root (where index.html lives):
    python3 restyle_guides.py

Transforms every guide in decisions/ to the navy-framed look:
  navy body + taller navy hero + floating white reading card + navy callout
  boxes + homepage-matched nav/buttons/footer.

Handles both quote variants ("DM Sans" and 'DM Sans'). Reports exactly what it
changes in each file, and flags any guide that doesn't receive the full set so
nothing is silently skipped. Safe to run once.
"""
import os, glob

GUIDES_DIR = 'decisions'

# Each rule: (label, old_string, new_string). Applied if `old` is present.
# Quote-variant rules are generated for both " and ' where relevant.
def build_rules():
    rules = []

    # 1. BODY: light -> navy (both quote variants)
    for q in ['"', "'"]:
        rules.append((
            f'body-navy({q})',
            f'body{{font-family:{q}DM Sans{q},sans-serif;background:#F5F7F6;color:#0B1929;line-height:1.6}}',
            f'body{{font-family:{q}DM Sans{q},sans-serif;background:#0B1929;color:#0B1929;line-height:1.6}}',
        ))

    # 2. NAV: opacity .92 -> .85, height 58 -> 62
    rules.append((
        'nav',
        '.nav{position:sticky;top:0;z-index:200;background:rgba(11,25,41,.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:58px;border-bottom:1px solid rgba(255,255,255,.07)}',
        '.nav{position:sticky;top:0;z-index:200;background:rgba(11,25,41,.85);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;justify-content:space-between;padding:0 2rem;height:62px;border-bottom:1px solid rgba(255,255,255,.07)}',
    ))

    # 3. PAGE-HERO: simple navy -> taller gradient + teal glow
    rules.append((
        'hero',
        '.page-hero{background:#0B1929;padding:3.5rem 2rem 2.75rem}',
        '.page-hero{background:linear-gradient(180deg,#0B1929 0%,#0d1e30 100%);padding:4rem 2rem 5.5rem;position:relative;overflow:hidden}\n.page-hero::after{content:"";position:absolute;width:480px;height:480px;border-radius:50%;background:radial-gradient(circle,rgba(14,165,160,.14),transparent 68%);top:-180px;right:-120px;pointer-events:none;z-index:0}',
    ))

    # 4. CONTENT: plain centered column -> floating white card on navy
    rules.append((
        'content',
        '.content{max-width:760px;margin:0 auto;padding:3rem 2rem}',
        '.content{max-width:800px;margin:-3rem auto 4.5rem;padding:3rem 3.25rem;background:#fff;border:1px solid #E2E8F0;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.35);position:relative;z-index:2;overflow:hidden}',
    ))

    # 4b. CONTENT mobile override
    rules.append((
        'content-mobile',
        '.content{padding:2rem 1.25rem}',
        '.content{padding:1.9rem 1.4rem;margin:-2rem 1rem 3rem;border-radius:16px}',
    ))

    # 5. CALLOUT: light teal -> navy gradient
    rules.append((
        'callout',
        '.callout{background:rgba(14,165,160,.07);border:1px solid rgba(14,165,160,.22);border-left:4px solid #0EA5A0;border-radius:8px;padding:1.1rem 1.25rem;margin:1.5rem 0;font-size:.925rem;line-height:1.7;color:#0B1929}',
        '.callout{background:linear-gradient(135deg,#0B1929,#12293f);border:1px solid rgba(14,165,160,.3);border-left:4px solid #0EA5A0;border-radius:12px;padding:1.25rem 1.4rem;margin:1.5rem 0;font-size:.925rem;line-height:1.7;color:#cdd9e3}',
    ))

    # 5b. Callout strong color (only if present)
    rules.append((
        'callout-strong',
        '.callout strong{color:#0EA5A0}',
        '.callout strong{color:#5eead4}',
    ))

    # 6. BUTTON: match homepage padding/radius + shadow
    rules.append((
        'button',
        '.btn{display:inline-block;background:#0EA5A0;color:#fff;padding:.6rem 1.4rem;border-radius:7px;font-weight:700;font-size:.875rem;text-decoration:none}',
        '.btn{display:inline-block;background:#0EA5A0;color:#fff;padding:.8rem 1.7rem;border-radius:9px;font-weight:700;font-size:.9rem;text-decoration:none;box-shadow:0 6px 20px rgba(14,165,160,.32)}',
    ))

    # 7. FOOTER: cramped -> generous
    rules.append((
        'footer',
        '.footer{background:#0B1929;padding:2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center}',
        '.footer{background:#0B1929;padding:3.5rem 2rem 2rem;color:rgba(255,255,255,.55);font-size:.8rem;text-align:center}',
    ))

    return rules

RULES = build_rules()

# Rules that are quote-variant pairs — only ONE of each pair needs to apply per file.
# For reporting "core" changes, we treat body-navy(") and body-navy(') as one logical change.
CORE_LABELS = {'body-navy', 'nav', 'hero', 'content', 'callout', 'button', 'footer'}

def logical(label):
    # strip quote-variant suffix e.g. body-navy(") -> body-navy
    return label.split('(')[0]

files = sorted(glob.glob(os.path.join(GUIDES_DIR, '*.html')))
print(f"Found {len(files)} guide files in {GUIDES_DIR}/\n")

changed_count = 0
incomplete = []

for path in files:
    try:
        content = open(path, encoding='utf-8').read()
    except Exception as e:
        print(f"  SKIP {path}: {e}")
        continue
    orig = content
    applied = set()
    for label, old, new in RULES:
        if old in content:
            content = content.replace(old, new)
            applied.add(logical(label))
    if content != orig:
        open(path, 'w', encoding='utf-8').write(content)
        changed_count += 1
        # Check the CORE changes all landed
        missing = CORE_LABELS - applied
        # callout-strong is optional; ignore if only that
        status = "OK" if not missing else f"MISSING: {', '.join(sorted(missing))}"
        flag = "" if not missing else "  <-- CHECK THIS FILE"
        print(f"  {os.path.basename(path):40s} {status}{flag}")
        if missing:
            incomplete.append((path, missing))
    else:
        print(f"  {os.path.basename(path):40s} no change (already styled?)")

print(f"\nUpdated {changed_count} of {len(files)} guides.")
if incomplete:
    print(f"\n⚠️  {len(incomplete)} file(s) did NOT get all core changes — they may have")
    print("    slightly different CSS. Tell Claude which files + what's missing:")
    for path, missing in incomplete:
        print(f"      {path}: missing {', '.join(sorted(missing))}")
else:
    print("✓ All updated guides received the full set of changes.")

print("\nNext:  git add -A  &&  git commit -m 'restyle guides to navy homepage look'  &&  git pull --no-edit  &&  git push")
