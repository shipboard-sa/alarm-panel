"""Replicate AL20 circuit layout to all 30 channels.

Reads the reference AL20 template offsets and applies them to every channel.
Component groupings derived from schematic + PCB net tracing.
AL27/AL28 are flagged as special but still get standard placement.
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pcb_path = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_PCB_PCB_Alarm-v2.1-LEDS-v20_2026-10-28.json'

with open(pcb_path, 'r', encoding='utf-8') as f:
    pcb = json.load(f)

SEP = '#@$'
MM = 3.937
BOX = 4047.559
BOY = 3046.528

# --- full_move ---
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

# --- Build component index ---
desig_idx = {}
desig_pos = {}
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'):
        continue
    desig = '??'
    for sub in shape.split(SEP):
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = shape.split(SEP)[0].split('~')
    desig_idx[desig] = i
    desig_pos[desig] = (float(lf[1]), float(lf[2]))

# --- Template offsets (mm, relative to LED indicator) ---
# From the reference AL20
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

# --- Channel definitions (from schematic + PCB net tracing) ---
# Position mapping for Q/R numbering (channels 25-30 are remapped)
ch_to_pos = {n: n for n in range(1, 25)}
ch_to_pos.update({25:29, 26:30, 27:28, 28:25, 29:26, 30:27})

# Direct D per channel (from PCB pad nets)
direct_d = {
    1:2, 2:4, 3:6, 4:8, 5:14, 6:18, 7:20, 8:22, 9:24, 10:26,
    11:28, 12:30, 13:32, 14:34, 15:36, 16:38, 17:40, 18:42, 19:44, 20:46,
    21:48, 22:50, 23:52, 24:54, 25:64, 26:66, 27:62, 28:56, 29:58, 30:60
}

# LED indicator per channel (from PCB pad nets)
led_indicator = {
    1:1, 2:3, 3:5, 4:7, 5:9, 6:11, 7:13, 8:15, 9:18, 10:20,
    11:21, 12:23, 13:25, 14:28, 15:29, 16:31, 17:34, 18:35,
    19:37, 20:40, 21:41, 22:43, 23:45, 24:48,
    25:58, 26:59, 27:55, 28:49, 29:52, 30:53
}

def get_channel_components(ch):
    """Return {role: designator} for a channel's back-side components."""
    pos = ch_to_pos[ch]
    q_odd = f'Q{2*pos-1}'
    q_even = f'Q{2*pos}'
    r_base = 5*(pos-1) + 1
    rs = [f'R{r_base+i}' for i in range(5)]
    d_dir_num = direct_d[ch]
    d_oth_num = d_dir_num - 1
    return {
        'Q_odd': q_odd,
        'Q_even': q_even,
        'D_other': f'D{d_oth_num}',
        'D_direct': f'D{d_dir_num}',
        'R_1': rs[0],
        'R_2': rs[1],
        'R_3': rs[2],
        'R_4': rs[3],
        'R_5': rs[4],
    }

# --- Replicate ---
moved = 0
missing = []
for ch in range(1, 31):
    if ch == 20:
        continue  # template already arranged

    led_desig = f'LED{led_indicator[ch]}'
    if led_desig not in desig_pos:
        print(f'  AL{ch}: SKIP - {led_desig} not found in PCB')
        continue

    led_x, led_y = desig_pos[led_desig]
    led_x_mm = (led_x - BOX) / MM
    led_y_mm = (led_y - BOY) / MM

    comps = get_channel_components(ch)
    ch_moved = 0

    for role, desig in comps.items():
        if desig not in desig_idx:
            missing.append(f'AL{ch}: {desig} ({role}) NOT FOUND')
            continue

        dx_mm, dy_mm = TMPL[role]
        new_x = led_x + dx_mm * MM
        new_y = led_y + dy_mm * MM

        idx = desig_idx[desig]
        pcb['shape'][idx] = full_move(pcb['shape'][idx], new_x, new_y)
        desig_pos[desig] = (new_x, new_y)
        ch_moved += 1
        moved += 1

    print(f'  AL{ch}: {ch_moved}/9 placed near {led_desig} ({led_x_mm:.0f},{led_y_mm:.0f})mm')

print(f'\nTotal moved: {moved} components across 29 channels')

if missing:
    print(f'\n=== MISSING ({len(missing)}) ===')
    for m in missing:
        print(f'  {m}')

# --- Verify: check max distance per channel ---
print('\n=== POST-REPLICATION DISTANCE CHECK ===')
bad = 0
for ch in range(1, 31):
    led_desig = f'LED{led_indicator[ch]}'
    if led_desig not in desig_pos:
        continue
    led_x, led_y = desig_pos[led_desig]
    comps = get_channel_components(ch)
    max_dist = 0
    max_comp = ''
    for role, desig in comps.items():
        if desig not in desig_pos:
            continue
        cx, cy = desig_pos[desig]
        dist = ((cx - led_x)**2 + (cy - led_y)**2)**0.5 / MM
        if dist > max_dist:
            max_dist = dist
            max_comp = desig
    status = 'OK' if max_dist < 35 else 'BAD'
    if status == 'BAD':
        bad += 1
    print(f'  AL{ch}: max {max_dist:.1f}mm ({max_comp}) [{status}]')

print(f'\nBad channels (>35mm): {bad}')

with open(pcb_path, 'w', encoding='utf-8') as f:
    json.dump(pcb, f, separators=(',', ':'))
print('Saved.')
