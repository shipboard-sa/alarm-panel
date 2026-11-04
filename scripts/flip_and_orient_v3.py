"""Flip non-LED SMD to bottom layer and check connector orientations.

Runs on the placed PCB file from place_v3.py.
- LEDs stay on top (faceplate)
- U1, U2, U4 (amber LED packages) stay on top
- Buzzer stays as-is (through-hole)
- CN, H stay as-is (through-hole)
- Everything else SMD -> bottom layer
- Check connector orientations (CN1-7 vertical, CN8 horizontal)
"""
import json, re, sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PCB_PATH = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_Alarm-v2.1-placed-v3.json'

with open(PCB_PATH, 'r', encoding='utf-8') as f:
    pcb = json.load(f)

SEP = '#@$'
MM = 3.937
BOX = 4047.559
BOY = 3046.528

LAYER_MAP = {'1':'2', '2':'1', '3':'4', '4':'3', '5':'6', '6':'5', '100':'101', '101':'100'}

def mirror_x(val, cx): return 2*cx - val

def mirror_path(s, cx):
    tokens = re.sub(r'([MLCZmlcz])', r' \1 ', s).split()
    out, cmd, i = [], 'M', 0
    while i < len(tokens):
        t = tokens[i]
        if t in 'MLCSmlcs': cmd=t; out.append(t); i+=1; continue
        if t in 'Zz': out.append(t); i+=1; continue
        try:
            x = float(t)
            if i+1 < len(tokens):
                try:
                    y = float(tokens[i+1])
                    out.append(f'{mirror_x(x,cx):.4f}' if cmd in 'MLCS' else f'{x:.4f}')
                    out.append(f'{y:.4f}'); i+=2; continue
                except ValueError: pass
            out.append(t); i+=1
        except ValueError: out.append(t); i+=1
    return ' '.join(out)

def mirror_pairs(s, cx):
    parts = s.strip().split(); r = []
    for i in range(0, len(parts)-1, 2):
        try: r.append(f'{mirror_x(float(parts[i]),cx):.4f}'); r.append(parts[i+1])
        except: r.append(parts[i]); r.append(parts[i+1])
    if len(parts)%2: r.append(parts[-1])
    return ' '.join(r)

def flip_component(shape, target_layer):
    """Flip a component to top (1) or bottom (2)."""
    subs = shape.split(SEP)
    lf = subs[0].split('~')
    current_layer = lf[7] if len(lf) > 7 else '1'

    if current_layer == str(target_layer):
        return shape  # already on target layer

    cx = float(lf[1])
    lf[7] = str(target_layer)
    subs[0] = '~'.join(lf)

    out = [subs[0]]
    for sub in subs[1:]:
        if sub.startswith('PAD~'):
            p = sub.split('~')
            if len(p)>2:
                try: p[2] = str(mirror_x(float(p[2]),cx))
                except: pass
            if len(p)>6 and p[6] in LAYER_MAP: p[6] = LAYER_MAP[p[6]]
            if len(p)>10 and p[10] and ' ' in p[10]: p[10] = mirror_pairs(p[10],cx)
            if len(p)>17 and ',' in p[17]:
                parts = p[17].split(',')
                if len(parts)==2:
                    try: p[17] = f'{mirror_x(float(parts[0]),cx)},{parts[1]}'
                    except: pass
            out.append('~'.join(p))
        elif sub.startswith('TEXT~'):
            p = sub.split('~')
            if len(p)>2:
                try: p[2] = str(mirror_x(float(p[2]),cx))
                except: pass
            if len(p)>11 and p[11] and 'M' in p[11]: p[11] = mirror_path(p[11],cx)
            out.append('~'.join(p))
        elif sub.startswith('TRACK~'):
            p = sub.split('~')
            if len(p)>2 and p[2] in LAYER_MAP: p[2] = LAYER_MAP[p[2]]
            if len(p)>4 and ' ' in p[4]: p[4] = mirror_pairs(p[4],cx)
            out.append('~'.join(p))
        elif sub.startswith('SOLIDREGION~'):
            p = sub.split('~')
            if len(p)>1 and p[1] in LAYER_MAP: p[1] = LAYER_MAP[p[1]]
            if len(p)>3 and p[3] and 'M' in p[3]: p[3] = mirror_path(p[3],cx)
            out.append('~'.join(p))
        elif sub.startswith('CIRCLE~'):
            p = sub.split('~')
            if len(p)>1:
                try: p[1] = str(mirror_x(float(p[1]),cx))
                except: pass
            if len(p)>5 and p[5] in LAYER_MAP: p[5] = LAYER_MAP[p[5]]
            out.append('~'.join(p))
        else:
            out.append(sub)
    return SEP.join(out)

# ── Build index ──────────────────────────────────────────────────────
desig_data = {}
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'): continue
    subs = shape.split(SEP)
    desig = '??'
    for sub in subs:
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = subs[0].split('~')
    is_th = any(sub.startswith('PAD~') and len(sub.split('~'))>6 and sub.split('~')[6]=='11'
               for sub in subs)
    layer = lf[7] if len(lf)>7 else '1'
    desig_data[desig] = {'idx': i, 'layer': layer, 'th': is_th,
                         'x': float(lf[1]), 'y': float(lf[2])}

# ── Flip SMD to bottom ──────────────────────────────────────────────
KEEP_TOP = {'U1', 'U2', 'U4'}  # amber LED packages on faceplate
flipped = 0
kept_top = 0

for desig, info in desig_data.items():
    prefix = ''.join(c for c in desig if c.isalpha())

    if info['th']: continue  # through-hole, skip
    if prefix in ('LED',): kept_top += 1; continue  # LEDs stay top
    if desig in KEEP_TOP: kept_top += 1; continue  # amber LEDs stay top

    if prefix in ('Q', 'R', 'D', 'C', 'U'):
        if info['layer'] != '2':  # not already on bottom
            pcb['shape'][info['idx']] = flip_component(pcb['shape'][info['idx']], 2)
            flipped += 1

print(f'Flipped to bottom: {flipped}')
print(f'Kept on top: {kept_top}')

# ── Verify U1, U2, U4 on top ────────────────────────────────────────
print('\n=== U1/U2/U4 layer check ===')
for d in ['U1', 'U2', 'U4']:
    if d in desig_data:
        shape = pcb['shape'][desig_data[d]['idx']]
        lf = shape.split(SEP)[0].split('~')
        layer = lf[7] if len(lf)>7 else '?'
        print(f'  {d}: layer={layer} (should be 1)')
        if layer != '1':
            pcb['shape'][desig_data[d]['idx']] = flip_component(shape, 1)
            print(f'    FIXED -> layer 1')

# ── Check connector orientations ────────────────────────────────────
print('\n=== CONNECTOR ORIENTATION CHECK ===')
for cn_num in range(1, 9):
    d = f'CN{cn_num}'
    if d not in desig_data: continue
    shape = pcb['shape'][desig_data[d]['idx']]
    subs = shape.split(SEP)

    # Get all pad positions to determine orientation
    pads = []
    for sub in subs:
        if sub.startswith('PAD~'):
            p = sub.split('~')
            if len(p) > 3:
                try: pads.append((float(p[2]), float(p[3])))
                except: pass

    if len(pads) < 2:
        print(f'  {d}: only {len(pads)} pads, skip')
        continue

    # Check if pads run primarily vertical (top-to-bottom) or horizontal (left-to-right)
    xs = [p[0] for p in pads]
    ys = [p[1] for p in pads]
    x_spread = max(xs) - min(xs)
    y_spread = max(ys) - min(ys)

    if y_spread > x_spread:
        orient = 'vertical (top-to-bottom)'
    else:
        orient = 'horizontal (left-to-right)'

    expected = 'horizontal' if cn_num == 8 else 'vertical'
    actual = 'vertical' if y_spread > x_spread else 'horizontal'
    status = 'OK' if actual == expected else 'NEEDS ROTATION'

    x_mm = (desig_data[d]['x'] - BOX) / MM
    y_mm = (desig_data[d]['y'] - BOY) / MM
    print(f'  {d}: {orient} at ({x_mm:.0f},{y_mm:.0f})mm  spread X={x_spread/MM:.1f}mm Y={y_spread/MM:.1f}mm [{status}]')

# ── Save ─────────────────────────────────────────────────────────────
with open(PCB_PATH, 'w', encoding='utf-8') as f:
    json.dump(pcb, f, separators=(',', ':'))
print(f'\nSaved to {PCB_PATH}')
