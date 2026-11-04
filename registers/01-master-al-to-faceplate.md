# Master AL-to-Faceplate Register
<!-- Purpose: Maps every AL channel to its V2 faceplate position, function, and LED pair -->
<!-- Version: 0.5 (H4/H5 corrected per schematic, CN9 added, V2.2 2026-10-29) -->
<!-- Scope: V2.2 alarm panel, 29 channels (AL1-AL29) -->

## Sources
- io_master.yml (AL-1 through AL-21 functions)
- Electrical Circuits2.xlsx "Master Alarm Panel" sheet (as-built V1, NO/NC types)
- Faceplate V2 HTML (agreed layout, faceplate_v20.html)

- AL-9 V2 = NO (was NC as-built, reused circuit)
- Note: U1/U2/U4 are YLED0805YG green LEDs driven directly by 24V buses (not AL circuits)
  - U1 = M/E ignition 24V (engine running indicator)
  - U2 = GenSet ignition 24V (genset running indicator)
  - U4 = Panel +24V (panel power indicator)
- Note: LED59 is AL7 alarm LED; LED13/14 are AL26 (2026-10-28)
- Correction: AL25/AL26 are spare channels, NOT green LED drivers

## LED Pair Convention
Each AL has two LEDs: one RED indicator (LED0805-RD_RED, pin 1 on AL signal net) and one ORANGE backlight (LED0805-RD_ORANGE / BL-HJC35A-AV-TRB, pin 1 on GND, powered via +24V_LEDs bus through current-limit resistor). The indicator lights when the alarm is active; the backlight illuminates the faceplate text label continuously when the panel is powered.

## Column 1 — BILGE / WATER (7 rows)

| Pos | Faceplate Label    | AL  | Function (io_master)     | V1 NO/NC | V2 NO/NC | Indicator (RED) | Backlight (ORG) | Status    |
|-----|--------------------|-----|--------------------------|----------|----------|-----------------|-----------------|-----------|
| 1   | Salon High Water   | AL4 | high_water_salon         | NO       | NO       | LED7            | LED8            | CONFIRMED |
| 2   | Salon Bilge        | AL3 | salon_bilge_pump         | NO       | NO       | LED5            | LED6            | CONFIRMED |
| 3   | Engine Bilge       | AL1 | engine_bilge_pump        | NO       | NO       | LED1            | LED2            | CONFIRMED |
| 4   | Bow High Water     | AL2 | high_water_bow           | NO       | NO       | LED3            | LED4            | CONFIRMED |
| 5   | Bow Bilge Pump     | AL9 | bow_bilge_pump           | NC       | **NO**   | LED18           | LED17           | CONFIRMED (V2 type change) |
| 6   | FW Pump            | AL5 | fresh_water_pump         | NO       | NO       | LED9            | LED10           | CONFIRMED |
| 7   | Spare              | AL27| spare                    | —        | NO       | LED15           | LED16           | CONFIRMED (netlist-verified) |

## Column 2 — FIRE + ENGINE (7 rows, 2 with dual LEDs)

| Pos | Faceplate Label     | AL  | Function (io_master)       | V1 NO/NC | V2 NO/NC | Indicator (RED) | Backlight (ORG) | Status    |
|-----|---------------------|-----|----------------------------|----------|----------|-----------------|-----------------|-----------|
| 1   | E/R Heat            | AL19| er_heat                    | NO       | NO       | LED37           | LED38           | CONFIRMED |
| 2   | E/R Smoke           | AL20| er_smoke                   | NO       | NO       | LED40           | LED39           | CONFIRMED |
| 3   | Spare               | AL22| spare                      | —        | NO       | LED43           | LED44           | CONFIRMED |
| 4   | Eng Raw Water       | AL6 | yanmar_raw_water_flow      | NO       | NO       | LED58           | LED57           | **CORRECTED** (was LED11/12) |
| 5   | GenSet Raw Water    | AL7 | genset_raw_water_flow      | NO       | NO       | LED59           | LED60           | **CORRECTED** (was LED13/14) |
| 6   | Water in Fuel       | AL18| water_in_fuel              | NO       | NO       | LED35           | LED36           | CONFIRMED |
| 7   | Spare               | AL23| spare                      | —        | NO       | LED45           | LED46           | CONFIRMED |

### Running/Power Indicator LEDs (NOT AL circuits — driven directly by 24V buses)
| Row | Component | Function             | Driven By         | Color       |
|-----|-----------|----------------------|-------------------|-------------|
| 4   | U1        | M/E Running          | M/E ignition +24V | Green (YLED0805YG) |
| 5   | U2        | GenSet Running       | GenSet ignition +24V | Green (YLED0805YG) |
| —   | U4        | Panel Power          | Panel +24V        | Green (YLED0805YG) |

## Column 3 — ELECTRICAL (7 active + 1 OPEN)

| Pos | Faceplate Label     | AL   | Function (io_master)       | V1 NO/NC | V2 NO/NC    | Indicator (RED) | Backlight (ORG) | Status    |
|-----|---------------------|------|----------------------------|----------|-------------|-----------------|-----------------|-----------|
| 1   | Master Electrical   | AL16 | victron_master_alarm       | NO       | NO          | LED31           | LED32           | CONFIRMED |
| 2   | Inverter / Charger  | AL14 | multiplus_alarm            | NO       | NO          | LED28           | LED27           | CONFIRMED |
| 3   | House Load Cutoff   | AL15 | batteryprotect_alarm       | NO       | NO          | LED29           | LED30           | CONFIRMED |
| 4   | Balmar              | AL21 | wakespeed_alarm            | NO       | NO          | LED41           | LED42           | CONFIRMED |
| 5   | Overcharging        | AL24 | overcharging_detect        | —        | comparator  | LED48           | LED47           | CONFIRMED |
| 6   | Battery Temp        | AL28 | battery_temp               | —        | comparator  | LED49           | LED50           | **CORRECTED** (was LED57/58) |
| 7   | Spare               | AL29 | spare                      | —        | NO          | LED52           | LED51           | CONFIRMED |
| 8   | *(OPEN)*            | —    | —                          | —        | —           | —               | —               | No circuit/LED |

## Column 4 — REFRIGERATION + NAV/SECURITY (8 rows)

| Pos | Faceplate Label     | AL   | Function (io_master)       | V1 NO/NC | V2 NO/NC | Indicator (RED) | Backlight (ORG) | Status    |
|-----|---------------------|------|----------------------------|----------|----------|-----------------|-----------------|-----------|
| 1   | Fridge / Freezer    | AL17 | cold_storage_temp_alarm    | NO       | NO       | LED34           | LED33           | CONFIRMED |
| 2   | Spare               | AL25 | spare                      | —        | NO       | LED11           | LED12           | **CORRECTED** (was LED49/50) |
| 3   | AIS                 | AL11 | ais_alarm                  | NO       | NO       | LED21           | LED22           | CONFIRMED |
| 4   | Anchor Drag         | AL12 | anchor_drag                | NO       | NO       | LED23           | LED24           | CONFIRMED |
| 5   | Autopilot           | AL10 | autopilot_ccu_error        | NO       | NO       | LED20           | LED19           | CONFIRMED |
| 6   | Automation          | AL13 | automation_heartbeat       | NO       | NO       | LED25           | LED26           | CONFIRMED |
| 7   | Dinghy Theft (NC)   | AL8  | dinghy_theft_loop          | NC       | NC       | LED55           | LED56           | **CORRECTED** (was LED15/16) |
| 8   | Spare               | AL26 | spare                      | —        | NO       | LED13           | LED14           | **CORRECTED** (was LED53/54) |

## Spare AL Assignments (resolved from connector groupings)

All 5 spare ALs assigned 1:1 to the 5 spare faceplate positions, based on which
connector (column group) each AL appears on:

| Spare Position | AL   | Connector | Indicator (RED) | Backlight (ORG) |
|---------------|------|-----------|-----------------|-----------------|
| Col 1 Row 7   | AL27 | CN8       | LED15           | LED16           |
| Col 2 Row 3   | AL22 | CN5       | LED43           | LED44           |
| Col 2 Row 7   | AL23 | CN2       | LED45           | LED46           |
| Col 4 Row 2   | AL25 | CN4       | LED11           | LED12           |
| Col 4 Row 8   | AL26 | CN3       | LED13           | LED14           |

## Power/Running Indicator LEDs (not AL circuits)
U1, U2, U4 are YLED0805YG green LEDs driven directly by 24V buses:
- U1: M/E ignition +24V (engine running), on Col 2 Row 4 alongside AL6 red LED
- U2: GenSet ignition +24V (genset running), on Col 2 Row 5 alongside AL7 red LED
- U4: Panel +24V (panel power indicator)

## Zone Backlight LEDs (LED61–70)
10 additional ORANGE backlight LEDs on the +24V_LEDs bus illuminate non-AL text labels on the faceplate.
MUTE and TEST are lighted panel-mount pushbuttons with built-in LEDs (not PCB backlight).

| LED   | Label Illuminated            |
|-------|------------------------------|
| LED61 | BILGE / WATER header         |
| LED62 | FIRE header                  |
| LED63 | ENGINE sub-header            |
| LED64 | ELECTRICAL header            |
| LED65 | REFRIGERATION header         |
| LED66 | NAV / SECURITY sub-header    |
| LED67 | Title (left) — YOUR VESSEL NAME |
| LED68 | Title (right) — YOUR VESSEL NAME |
| LED69 | MASTER ALARM PANEL subtitle  |
| LED70 | PWR label                    |

Note: LED-to-label mapping for LED61–70 is ASSUMED from faceplate layout (not explicit in schematic).

## Panel-Mount Button Headers
MUTE and TEST are lighted panel-mount pushbuttons wired to 2-pin through-hole headers on the PCB.

| Header | Button | Pin 1 Net | Pin 2 Net | Package                        |
|--------|--------|-----------|-----------|--------------------------------|
| H4     | TEST   | TestLEDs  | GND       | PZ254V-11-02P (2.54mm TH, C492401) |
| H5     | MUTE   | MuteBus   | GND       | PZ254V-11-02P (2.54mm TH, C492401) |

## External Interface Connector (CN9)
3-pin KF142V-5.08-3P near buzzer/mute area. Provides mute acknowledgement and remote mute signals to the Ship's Automation engine, plus external buzzer output.

| Pin | Net       | Function                                    |
|-----|-----------|---------------------------------------------|
| 1   | MuteBus   | Mute Out — Pi reads this to detect panel ack |
| 2   | MuteBus   | Mute In — Pi writes this for remote mute     |
| 3   | BuzzerBus | Buzzer Out — drives external buzzer           |

Both pins 1 and 2 are on the MuteBus net, giving the Pi separate read/write terminals.

## Open Questions
1. Col 3 Pos 8 (OPEN) — confirm no circuit or LED behind this position
2. LED67/68 — confirm two LEDs for the title text, or should it be one?
