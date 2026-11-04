# LED Placement Grid
<!-- Purpose: Maps every LED on the faceplate to its physical position, color, and AL -->
<!-- Version: 0.1 -->
<!-- Source: faceplate_v20.html (agreed V2 faceplate layout) -->

## Faceplate Dimensions
- Faceplate: 12" × 5.5" (305mm × 140mm)
- PCB: 11" × 4.5" (279mm × 114mm), inset 0.5" from faceplate edges
- LED positions are on the PCB top layer (front/faceplate side)

## LED Position Coordinates
All coordinates in mm from PCB top-left corner.
X increases left→right, Y increases top→bottom.

### Column 1 — BILGE / WATER (X ≈ 18mm)

| Row | Y (mm) | LED Pair    | Color | AL  | Label            |
|-----|--------|-------------|-------|-----|------------------|
| 1   | 10.0   | LED7, LED8  | Red   | AL4 | Salon High Water |
| 2   | 16.1   | LED5, LED6  | Red   | AL3 | Salon Bilge      |
| 3   | 22.2   | LED1, LED2  | Red   | AL1 | Engine Bilge     |
| 4   | 28.3   | LED3, LED4  | Red   | AL2 | Bow High Water   |
| 5   | 34.4   | LED17,LED18 | Red   | AL9 | Bow Bilge Pump   |
| 6   | 40.5   | LED9, LED10 | Red   | AL5 | FW Pump          |
| 7   | 46.5   | ?, ?        | Grey  | ?   | Spare            |

### Column 2 — FIRE + ENGINE (X ≈ 55mm red, ≈52mm green)

| Row | Y (mm) | LED Pair (red) | LED Pair (green) | AL (red) | AL (green) | Label           |
|-----|--------|----------------|------------------|----------|------------|-----------------|
| 1   | 10.0   | LED37,LED38    | —                | AL19     | —          | E/R Heat        |
| 2   | 16.1   | LED39,LED40    | —                | AL20     | —          | E/R Smoke       |
| 3   | 22.2   | ?, ?           | —                | ?        | —          | Spare           |
| 4   | 34.4   | LED11,LED12    | LED61,LED62      | AL6      | AL25       | Eng Raw Water   |
| 5   | 40.5   | LED13,LED14    | LED63,LED64      | AL7      | AL26       | GenSet Raw Water|
| 6   | 46.5   | LED35,LED36    | —                | AL18     | —          | Water in Fuel   |
| 7   | 52.6   | ?, ?           | —                | ?        | —          | Spare           |

### Column 3 — ELECTRICAL (X ≈ 92mm)

| Row | Y (mm) | LED Pair    | Color | AL   | Label             |
|-----|--------|-------------|-------|------|-------------------|
| 1   | 10.0   | LED31,LED32 | Red   | AL16 | Master Electrical |
| 2   | 16.1   | LED27,LED28 | Red   | AL14 | Inverter/Charger  |
| 3   | 22.2   | LED29,LED30 | Red   | AL15 | House Load Cutoff |
| 4   | 28.3   | LED41,LED42 | Red   | AL21 | Balmar            |
| 5   | 34.4   | LED47,LED48 | Red   | AL24 | Overcharging      |
| 6   | 40.5   | LED57,LED58 | Red   | AL28 | Battery Temp      |
| 7   | 46.5   | LED51,LED52 | Grey  | AL29 | Spare             |
| 8   | —      | —           | —     | —    | *(OPEN)*          |

### Column 4 — REFRIG + NAV/SECURITY (X ≈ 130mm)

| Row | Y (mm) | LED Pair    | Color | AL   | Label            |
|-----|--------|-------------|-------|------|------------------|
| 1   | 10.0   | LED33,LED34 | Red   | AL17 | Fridge/Freezer   |
| 2   | 16.1   | ?, ?        | Grey  | ?    | Spare            |
| 3   | 28.3   | LED21,LED22 | Red   | AL11 | AIS              |
| 4   | 34.4   | LED23,LED24 | Red   | AL12 | Anchor Drag      |
| 5   | 40.5   | LED19,LED20 | Red   | AL10 | Autopilot        |
| 6   | 46.5   | LED25,LED26 | Red   | AL13 | Automation       |
| 7   | 52.6   | LED15,LED16 | Red   | AL8  | Dinghy Theft (NC)|
| 8   | 58.7   | ?, ?        | Grey  | ?    | Spare            |

### Support LEDs (Buttons row, Y ≈ 74mm)

| LED         | Color  | Function  | X (mm) |
|-------------|--------|-----------|--------|
| LED65,LED66 | Red    | MUTE btn  | ≈ 55   |
| LED69,LED70 | Amber  | TEST btn  | ≈ 92   |
| LED67,LED68 | —      | Buzzer    | ≈ 73   |

## Unresolved
- Y coordinates are APPROXIMATE — need to measure from faceplate HTML SVG coordinates
- X coordinates per column need final measurement from faceplate HTML
- 5 spare positions need AL assignments (only 3 ALs available: AL22, AL23, AL27)
- LED pair assignments for spare positions and AL22/23/27 need confirmation
- Col 2 Row 4/5 Y positions offset due to ENGINE sub-header gap
- Col 4 Row 3+ Y positions offset due to NAV/SECURITY sub-header gap

## Conversion: Faceplate SVG → PCB mm
From faceplate HTML: faceplate is 750×340 SVG units for 12"×5.5".
- Scale: 750/305 = 2.459 SVG units/mm (horizontal)
- Scale: 340/140 = 2.429 SVG units/mm (vertical)
- PCB origin offset: 0.5" (12.7mm) inset from faceplate edge on all sides
