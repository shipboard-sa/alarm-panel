"""Restore LED61-70 and R160-R169 to their faceplate positions.

LEDs go to v20 faceplate positions (top layer).
Resistors go ~2mm right, ~2.5mm below their LED (bottom layer, already flipped).
"""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pcb_path = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_PCB_PCB_Alarm-v2.1-LEDS-v20_2026-10-28.json'
v20_path = r'D:\Documents\sailboat\Refit\your vessel\Alarm Panel\projects\Alarm v2\PCB_Alarm-v2.1-LEDS-v20.json'

with open(pcb_path, 'r', encoding='utf-8') as f:
    pcb = json.load(f)
with open(v20_path, 'r', encoding='utf-8') as f:
    v20 = json.load(f)

SEP = '#@$'
MM = 3.937
BOX = 4047.559
BOY = 3046.528

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

# --- Get v20 positions for LED61-70 and R160-R169 ---
v20_pos = {}
for shape in v20['shape']:
    if not isinstance(shape, str) or not shape.startswith('LIB~'):
        continue
    subs = shape.split(SEP)
    desig = '??'
    for sub in subs:
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    lf = subs[0].split('~')
    v20_pos[desig] = (float(lf[1]), float(lf[2]))

# --- Build index for current PCB ---
desig_idx = {}
for i, shape in enumerate(pcb['shape']):
    if not isinstance(shape, str) or not shape.startswith('LIB~'):
        continue
    desig = '??'
    for sub in shape.split(SEP):
        if sub.startswith('TEXT~P~'):
            p = sub.split('~')
            if len(p)>10: desig = p[10]
    desig_idx[desig] = i

# --- Restore LED61-70 to v20 positions ---
moved = 0
for i in range(61, 71):
    desig = f'LED{i}'
    if desig not in desig_idx or desig not in v20_pos:
        print(f'  SKIP {desig}: not found')
        continue
    target_x, target_y = v20_pos[desig]
    idx = desig_idx[desig]
    pcb['shape'][idx] = full_move(pcb['shape'][idx], target_x, target_y)
    x_mm = (target_x - BOX) / MM
    y_mm = (target_y - BOY) / MM
    print(f'  {desig} -> ({x_mm:.1f}, {y_mm:.1f})mm [top layer, faceplate position]')
    moved += 1

# --- Restore R160-R169 near their LEDs ---
# Pairing: R(159+n) pairs with LED(60+n)
# Place R at v20 offset from its LED (approximately +2mm right, +2.5mm below)
for i in range(160, 170):
    desig = f'R{i}'
    led_desig = f'LED{i - 99}'  # R160->LED61, R161->LED62, etc.
    if desig not in desig_idx:
        print(f'  SKIP {desig}: not found')
        continue
    if led_desig not in v20_pos:
        print(f'  SKIP {desig}: no LED position for {led_desig}')
        continue
    # Use the v20 R position (it was placed relative to its LED there)
    if desig in v20_pos:
        target_x, target_y = v20_pos[desig]
    else:
        # Fallback: 2mm right, 2.5mm below LED
        led_x, led_y = v20_pos[led_desig]
        target_x = led_x + 2.1 * MM
        target_y = led_y + 2.5 * MM
    idx = desig_idx[desig]
    pcb['shape'][idx] = full_move(pcb['shape'][idx], target_x, target_y)
    x_mm = (target_x - BOX) / MM
    y_mm = (target_y - BOY) / MM
    print(f'  {desig} -> ({x_mm:.1f}, {y_mm:.1f})mm [bottom layer, near {led_desig}]')
    moved += 1

print(f'\nRestored {moved} components')

with open(pcb_path, 'w', encoding='utf-8') as f:
    json.dump(pcb, f, separators=(',', ':'))
print('Saved.')
