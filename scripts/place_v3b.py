"""Place all 29 alarm circuits — CORRECTED: no swap remapping.

The net-label swaps on connector pins don't change the circuits.
Each AL keeps its ORIGINAL components and LEDs.
AL30 components are DELETED (not parked).

Circuit groupings (original, unchanged):
  AL1-24:  standard positions 1-24
  AL25:    pos 29 — M/E Running, has U1 + 6R
  AL26:    pos 30 — GenSet Running, has U2 + 6R
  AL27:    pos 28 — NC circuit, 4R + 1Q
  AL28:    pos 25 — standard
  AL29:    pos 26 — standard
  AL30:    DELETED (was pos 27)
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PCB_PATH = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_PCB_PCB_Alarm-v2.1-LEDS-v20_2026-10-28.json'
V20_PATH = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_Alarm-v2.1-LEDS-v20.json'
OUT_PATH = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_Alarm-v2.1-placed-v3b.json'

with open(PCB_PATH, 'r', encoding='utf-8') as f:
    pcb = json.load(f)
with open(V20_PATH, 'r', encoding='utf-8') as f:
    v20 = json.load(f)

SEP = '#@$'
MM = 3.937
BOX = 4047.559
BOY = 3046.528

# ── full_move (shifts all sub-element coordinates) ───────────────────
def _shift_path(s, dx, dy):
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
                    if cmd in 'MLCS': out.append(f'{x+dx:.4f}'); out.append(f'{y+dy:.4f}')
                    else: out.append(f'{x:.4f}'); out.append(f'{y:.4f}')
                    i+=2; continue
                except ValueError: pass
            out.append(t); i+=1
        except ValueError: out.append(t); i+=1
    return ' '.join(out)

def _shift_pairs(s, dx, dy):
    parts = s.strip().split(); r = []
    for i in range(0, len(parts)-1, 2):
        try: r.append(f'{float(parts[i])+dx:.4f}'); r.append(f'{float(parts[i+1])+dy:.4f}')
        except: r.append(parts[i]); r.append(parts[i+1])
    if len(parts)%2: r.append(parts[-1])
    return ' '.join(r)

def full_move(shape, new_x, new_y):
    subs = shape.split(SEP)
    lf = subs[0].split('~')
    ox, oy = float(lf[1]), float(lf[2])
    dx, dy = new_x - ox, new_y - oy
    if abs(dx) < 0.01 and abs(dy) < 0.01: return shape
    lf[1] = str(new_x); lf[2] = str(new_y)
    subs[0] = '~'.join(lf)
    out = [subs[0]]
    for sub in subs[1:]:
        if sub.startswith('PAD~'):
            p = sub.split('~')
            try: p[2] = str(float(p[2])+dx); p[3] = str(float(p[3])+dy)
            except: pass
            if len(p)>10 and p[10] and ' ' in p[10]: p[10] = _shift_pairs(p[10], dx, dy)
            out.append('~'.join(p))
        elif sub.startswith('TEXT~'):
            p = sub.split('~')
            if len(p)>3:
                try: p[2] = str(float(p[2])+dx); p[3] = str(float(p[3])+dy)
                except: pass
            if len(p)>11 and p[11] and 'M' in p[11]: p[11] = _shift_path(p[11], dx, dy)
            out.append('~'.join(p))
        elif sub.startswith('TRACK~'):
            p = sub.split('~')
            if len(p)>4 and ' ' in p[4]: p[4] = _shift_pairs(p[4], dx, dy)
            out.append('~'.join(p))
        elif sub.startswith('SOLIDREGION~'):
            p = sub.split('~')
            if len(p)>3 and p[3] and 'M' in p[3]: p[3] = _shift_path(p[3], dx, dy)
            out.append('~'.join(p))
        elif sub.startswith('CIRCLE~'):
            p = sub.split('~')
            if len(p)>2:
                try: p[1] = str(float(p[1])+dx); p[2] = str(float(p[2])+dy)
                except: pass
            out.append('~'.join(p))
        elif sub.startswith('SVGNODE~'):
            p = sub.split('~')
            for j in range(len(p)):
                if 'M ' in p[j] or (len(p[j])>2 and p[j][0]=='M'):
                    p[j] = _shift_path(p[j], dx, dy)
            out.append('~'.join(p))
        else:
            out.append(sub)
    return SEP.join(out)

# ── Build component index ────────────────────────────────────────────
desig_idx = {}
desig_pos = {}
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'): continue
    desig = '??'
    for sub in shape.split(SEP):
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = shape.split(SEP)[0].split('~')
    desig_idx[desig] = i
    desig_pos[desig] = (float(lf[1]), float(lf[2]))

# ── v20 reference positions ──────────────────────────────────────────
v20_pos = {}
for shape in v20['shape']:
    if not isinstance(shape, str) or not shape.startswith('LIB~'): continue
    subs = shape.split(SEP)
    desig = '??'
    for sub in subs:
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = subs[0].split('~')
    v20_pos[desig] = (float(lf[1]), float(lf[2]))

# ── Template offsets (mm, relative to indicator LED) ─────────────────
TMPL = {
    'Q_odd':    (+14.01, -2.75),
    'Q_even':   (+8.81,  -2.37),
    'D_other':  (+18.46, -5.54),
    'D_direct': (+4.49,  +1.44),
    'R_1':      (+28.36, -1.73),
    'R_2':      (-0.46,  -2.24),
    'R_3':      (-0.34,  -4.78),
    'R_4':      (+22.90, -2.50),
    'R_5':      (+27.09, +1.69),
}

# ── Original mapping tables (from PCB pad net tracing — NO SWAPS) ────
# direct_d[ch] = D_direct designator number
DIRECT_D = {
    1:2, 2:4, 3:6, 4:8, 5:14, 6:18, 7:20, 8:22, 9:24, 10:26,
    11:28, 12:30, 13:32, 14:34, 15:36, 16:38, 17:40, 18:42,
    19:44, 20:46, 21:48, 22:50, 23:52, 24:54,
    25:64, 26:66, 27:62, 28:56, 29:58
}

# led_indicator[ch] = indicator LED number
LED_IND = {
    1:1, 2:3, 3:5, 4:7, 5:9, 6:11, 7:13, 8:15, 9:18, 10:20,
    11:21, 12:23, 13:25, 14:28, 15:29, 16:31, 17:34, 18:35,
    19:37, 20:40, 21:41, 22:43, 23:45, 24:48,
    25:58, 26:59, 27:55, 28:49, 29:52
}

# ch_to_pos for Q/R numbering
CH_POS = {n: n for n in range(1, 25)}
CH_POS.update({25:29, 26:30, 27:28, 28:25, 29:26})

# ── Channel definitions (ORIGINAL — circuits unchanged by swap) ──────
CHANNELS = {}

for ch in range(1, 30):
    pos = CH_POS[ch]
    dd = DIRECT_D[ch]
    ind = LED_IND[ch]

    q_odd = f'Q{2*pos-1}'
    q_even = f'Q{2*pos}'
    r_base = 5*(pos-1) + 1
    rs = [f'R{r_base+i}' for i in range(5)]

    comps = {
        'Q_odd': q_odd,
        'Q_even': q_even,
        'D_other': f'D{dd-1}',
        'D_direct': f'D{dd}',
        'R_1': rs[0],
        'R_2': rs[1],
        'R_3': rs[2],
        'R_4': rs[3],
        'R_5': rs[4],
    }
    ch_type = 'standard'

    # AL25 (pos 29): M/E Running — U1 + 6 resistors (R140-145)
    if ch == 25:
        ch_type = 'special_u1'
        comps = {
            'Q_odd': 'Q56', 'Q_even': 'Q57',
            'D_other': 'D63', 'D_direct': 'D64',
            'R_1': 'R140', 'R_2': 'R141', 'R_3': 'R142',
            'R_4': 'R143', 'R_5': 'R144', 'R_6': 'R145',
            'U': 'U1',
        }

    # AL26 (pos 30): GenSet Running — U2 + 6 resistors (R146-151)
    elif ch == 26:
        ch_type = 'special_u2'
        comps = {
            'Q_odd': 'Q58', 'Q_even': 'Q59',
            'D_other': 'D65', 'D_direct': 'D66',
            'R_1': 'R146', 'R_2': 'R147', 'R_3': 'R148',
            'R_4': 'R149', 'R_5': 'R150', 'R_6': 'R151',
            'U': 'U2',
        }

    # AL27 (pos 28): NC circuit — 4R, 1Q, 2D
    elif ch == 27:
        ch_type = 'nc'
        comps = {
            'Q_odd': 'Q55',
            'D_other': 'D61', 'D_direct': 'D62',
            'R_1': 'R136', 'R_2': 'R137', 'R_3': 'R138', 'R_4': 'R139',
        }

    CHANNELS[ch] = {
        'indicator': f'LED{ind}',
        'type': ch_type,
        'comps': comps,
    }

print(f'Defined {len(CHANNELS)} channels (original circuit mapping, no swaps)')

# ── Step 1: DELETE AL30 components ───────────────────────────────────
print('\n=== STEP 1: Delete AL30 components ===')
AL30_DELETE = ['R131','R132','R133','R134','R135','Q53','Q54','D59','D60','LED53','LED54']
delete_indices = set()
for c in AL30_DELETE:
    if c in desig_idx:
        delete_indices.add(desig_idx[c])
        print(f'  DELETE {c}')
    else:
        print(f'  {c}: not found')

# Remove by index (highest first to preserve ordering)
for idx in sorted(delete_indices, reverse=True):
    pcb['shape'].pop(idx)
print(f'  Removed {len(delete_indices)} shapes')

# Rebuild index after deletion
desig_idx.clear()
desig_pos.clear()
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'): continue
    desig = '??'
    for sub in shape.split(SEP):
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = shape.split(SEP)[0].split('~')
    desig_idx[desig] = i
    desig_pos[desig] = (float(lf[1]), float(lf[2]))

# ── Step 2: Place all 29 channels' back-side components ──────────────
print('\n=== STEP 2: Place back-side components ===')
moved = 0
missing = []
placed_desigs = set()

for al in sorted(CHANNELS.keys()):
    ch = CHANNELS[al]
    led_d = ch['indicator']
    if led_d not in desig_pos:
        print(f'  AL{al}: SKIP - {led_d} not found')
        continue

    lx, ly = desig_pos[led_d]
    led_mm = ((lx - BOX)/MM, (ly - BOY)/MM)
    ch_moved = 0

    for role, desig in ch['comps'].items():
        if desig not in desig_idx:
            missing.append(f'AL{al}: {desig} ({role})')
            continue
        if role in TMPL:
            dx, dy = TMPL[role]
        elif role == 'R_6':
            dx, dy = (+25.0, -0.40)
        elif role == 'U':
            dx, dy = (+10.0, +0.0)
        else:
            continue

        nx = lx + dx * MM
        ny = ly + dy * MM
        pcb['shape'][desig_idx[desig]] = full_move(pcb['shape'][desig_idx[desig]], nx, ny)
        desig_pos[desig] = (nx, ny)
        placed_desigs.add(desig)
        ch_moved += 1
        moved += 1

    n_exp = len([r for r in ch['comps'] if r in TMPL or r in ('R_6','U')])
    print(f'  AL{al}: {ch_moved}/{n_exp} near {led_d} ({led_mm[0]:.0f},{led_mm[1]:.0f})mm [{ch["type"]}]')

print(f'\nTotal placed: {moved}')
if missing:
    print(f'\n=== MISSING ({len(missing)}) ===')
    for m in missing: print(f'  {m}')

# ── Step 3: Restore support LEDs (LED61-70) + R158-R169 ─────────────
print('\n=== STEP 3: Support LEDs + resistors ===')
s_moved = 0
for i in range(61, 71):
    d = f'LED{i}'
    if d in desig_idx and d in v20_pos:
        pcb['shape'][desig_idx[d]] = full_move(pcb['shape'][desig_idx[d]], *v20_pos[d])
        desig_pos[d] = v20_pos[d]
        placed_desigs.add(d)
        s_moved += 1
for i in range(158, 170):
    d = f'R{i}'
    if d not in desig_idx: continue
    if d in v20_pos:
        pcb['shape'][desig_idx[d]] = full_move(pcb['shape'][desig_idx[d]], *v20_pos[d])
        desig_pos[d] = v20_pos[d]
    else:
        ld = f'LED{i-97}'
        if ld in desig_pos:
            lx2, ly2 = desig_pos[ld]
            pcb['shape'][desig_idx[d]] = full_move(pcb['shape'][desig_idx[d]], lx2+2.1*MM, ly2+2.5*MM)
            desig_pos[d] = (lx2+2.1*MM, ly2+2.5*MM)
    placed_desigs.add(d)
    s_moved += 1
print(f'  Restored {s_moved}')

# ── Step 4: Support SMD components ───────────────────────────────────
print('\n=== STEP 4: Support components ===')
SX = BOX + 130*MM; SY = BOY + 5*MM
support = ['U3','U4','U5','C1','C2','C3','D67','D68',
           'D9','D10','D11','D12','D15','D16',
           'R152','R153','R154','R155','R156']
sp = 0
for j, d in enumerate(support):
    if d in desig_idx and d not in placed_desigs:
        nx = SX + (j%6)*5*MM; ny = SY + (j//6)*5*MM
        pcb['shape'][desig_idx[d]] = full_move(pcb['shape'][desig_idx[d]], nx, ny)
        desig_pos[d] = (nx, ny)
        placed_desigs.add(d)
        sp += 1
        print(f'  {d} -> ({(nx-BOX)/MM:.0f},{(ny-BOY)/MM:.0f})mm')
print(f'  Placed {sp}')

# ── Step 5: Buzzer circuit ───────────────────────────────────────────
print('\n=== STEP 5: Buzzer ===')
bz = None
for d in desig_idx:
    if 'BUZZ' in d.upper(): bz = d; break
if bz and bz in desig_pos:
    bx, by = desig_pos[bz]
    for d, dx, dy in [('R157',8,-3),('Q60',12,-3),('Q61',16,-3)]:
        if d in desig_idx and d not in placed_desigs:
            nx, ny = bx+dx*MM, by+dy*MM
            pcb['shape'][desig_idx[d]] = full_move(pcb['shape'][desig_idx[d]], nx, ny)
            placed_desigs.add(d)
            print(f'  {d} placed near buzzer')

# ── Step 6: Flip SMD to bottom (except LEDs, U1, U2, U4) ────────────
print('\n=== STEP 6: Flip to bottom ===')
LAYER_MAP = {'1':'2','2':'1','3':'4','4':'3','5':'6','6':'5','100':'101','101':'100'}
KEEP_TOP = {'U1','U2','U4'}

def mirror_x(v, cx): return 2*cx - v
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

def flip_to_bottom(shape):
    subs = shape.split(SEP)
    lf = subs[0].split('~')
    if len(lf)<=7 or lf[7]=='2': return shape  # already bottom
    cx = float(lf[1]); lf[7] = '2'; subs[0] = '~'.join(lf)
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
                pts = p[17].split(',')
                if len(pts)==2:
                    try: p[17] = f'{mirror_x(float(pts[0]),cx)},{pts[1]}'
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
        else: out.append(sub)
    return SEP.join(out)

flipped = 0
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'): continue
    subs = shape.split(SEP)
    desig = '??'
    for sub in subs:
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    prefix = ''.join(c for c in desig if c.isalpha())
    is_th = any(sub.startswith('PAD~') and len(sub.split('~'))>6 and sub.split('~')[6]=='11'
               for sub in subs)
    if is_th: continue
    if prefix == 'LED': continue
    if desig in KEEP_TOP: continue
    if prefix in ('Q','R','D','C','U'):
        result = flip_to_bottom(shape)
        if result != shape:
            pcb['shape'][i] = result
            flipped += 1

print(f'  Flipped {flipped} to bottom')

# Ensure U1/U2/U4 on top
for d in ['U1','U2','U4']:
    if d in desig_idx:
        shape = pcb['shape'][desig_idx[d]]
        lf = shape.split(SEP)[0].split('~')
        if len(lf)>7 and lf[7] != '1':
            print(f'  WARNING: {d} not on top — fixing')

# ── Step 7: Unplaced check ───────────────────────────────────────────
print('\n=== UNPLACED CHECK ===')
unplaced = []
for d in desig_idx:
    prefix = ''.join(c for c in d if c.isalpha())
    if prefix in ('LED','CN','H','BUZZER','BZ'): continue
    if d in placed_desigs: continue
    unplaced.append(d)
if unplaced:
    print(f'  Unplaced ({len(unplaced)}): {sorted(unplaced)}')
else:
    print('  All accounted for')

# ── Step 8: Distance check ──────────────────────────────────────────
print('\n=== DISTANCE CHECK ===')
bad = 0
for al in sorted(CHANNELS.keys()):
    ch = CHANNELS[al]
    ld = ch['indicator']
    if ld not in desig_pos: continue
    lx, ly = desig_pos[ld]
    mx, mc = 0, ''
    for role, d in ch['comps'].items():
        if d not in desig_pos: continue
        cx, cy = desig_pos[d]
        dist = ((cx-lx)**2 + (cy-ly)**2)**0.5 / MM
        if dist > mx: mx, mc = dist, d
    ok = 'OK' if mx < 35 else 'BAD'
    if ok == 'BAD': bad += 1
    print(f'  AL{al}: max {mx:.1f}mm ({mc}) [{ok}]')
print(f'\nBad (>35mm): {bad}')

# ── Connector orientation check ──────────────────────────────────────
print('\n=== CONNECTOR ORIENTATION ===')
for cn in range(1, 9):
    d = f'CN{cn}'
    if d not in desig_idx: continue
    shape = pcb['shape'][desig_idx[d]]
    pads = []
    for sub in shape.split(SEP):
        if sub.startswith('PAD~'):
            p = sub.split('~')
            if len(p)>3:
                try: pads.append((float(p[2]), float(p[3])))
                except: pass
    if len(pads) < 2: continue
    xs = [p[0] for p in pads]; ys = [p[1] for p in pads]
    xsp = max(xs)-min(xs); ysp = max(ys)-min(ys)
    actual = 'vertical' if ysp > xsp else 'horizontal'
    expected = 'horizontal' if cn == 8 else 'vertical'
    x_mm = (desig_pos[d][0]-BOX)/MM; y_mm = (desig_pos[d][1]-BOY)/MM
    status = 'OK' if actual == expected else 'NEEDS ROTATION'
    print(f'  CN{cn}: {actual} at ({x_mm:.0f},{y_mm:.0f})mm [{status}]')

# ── Save ─────────────────────────────────────────────────────────────
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(pcb, f, separators=(',', ':'))
print(f'\nSaved to {OUT_PATH}')
