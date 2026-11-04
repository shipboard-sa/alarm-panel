# AL-to-Circuit Mapping Register
<!-- Purpose: Documents circuit topology and special requirements per AL channel -->
<!-- Version: 0.2 (LED pairs + component refs corrected from netlist 2026-10-28) -->
<!-- Scope: V2.1 alarm panel, 29 channels -->

## Sources
- Alarm-Panel-V2-Design.md (circuit descriptions)
- Electrical Circuits2.xlsx "Master Alarm Panel" sheet (as-built V1)
- Schematic SCH_Alarm-v2.1_2026-10-28 (3).json

## Standard NO Circuit Template (23 channels)
Most channels use the same standard normally-open (NO) alarm circuit:
- **Q_odd** (NPN): signal input transistor
- **Q_even** (PNP): LED driver transistor
- **D_direct**: signal input protection diode
- **D_other**: flyback/protection diode
- **R1**: LED current-limiting resistor
- **R2**: base bias resistor (Q_odd)
- **R3**: base pull-down resistor (Q_odd)
- **R4**: collector resistor / LED path
- **R5**: emitter resistor
- **LED pair**: indicator (red, 0805 dual)

## Circuit Type per Channel

| AL  | Circuit Type | Components (position mapping) | Special Notes |
|-----|-------------|-------------------------------|---------------|
| AL1 | Standard NO | Q1,Q2, D1,D2, R1-R5, LED1/LED2 | |
| AL2 | Standard NO | Q3,Q4, D3,D4, R6-R10, LED3/LED4 | |
| AL3 | Standard NO | Q5,Q6, D5,D6, R11-R15, LED5/LED6 | |
| AL4 | Standard NO | Q7,Q8, D7,D8, R16-R20, LED7/LED8 | |
| AL5 | Standard NO | Q9,Q10, D9,D10, R21-R25, LED9/LED10 | Source: R27 relay |
| AL6 | Standard NO | Q59,Q60, D63,D64, R141-R145, LED58/LED57 | Yanmar raw water flow; + U1 green M/E running |
| AL7 | Standard NO | Q61,Q62, D65,D66, R146-R151, LED59/LED60 | GenSet raw water flow; + U2 green GenSet running. LED59 |
| AL8 | **NC** | Q55,Q56, D61,D62, R136-R140, LED55/LED56 | Dinghy theft loop — NC circuit (alarm on open) |
| AL9 | **NO** (was NC) | Q17,Q18, D17,D18, R41-R45, LED17/LED18 | **V2 CHANGE**: reused circuit, now NO (was NC as-built). Source: R28 |
| AL10| Standard NO | Q19,Q20, D19,D20, R46-R50, LED19/LED20 | Autopilot CCU. Source: R24 |
| AL11| Standard NO | Q21,Q22, D21,D22, R51-R55, LED21/LED22 | AIS alarm. Source: R1 RTU 1 |
| AL12| Standard NO | Q23,Q24, D23,D24, R56-R60, LED23/LED24 | Anchor drag |
| AL13| Standard NO | Q25,Q26, D25,D26, R61-R65, LED25/LED26 | Automation heartbeat (was Spare in V1) |
| AL14| Standard NO | Q27,Q28, D27,D28, R66-R70, LED27/LED28 | Multiplus alarm relay |
| AL15| Standard NO | Q29,Q30, D29,D30, R71-R75, LED29/LED30 | Battery Protect alarm out |
| AL16| Standard NO | Q31,Q32, D31,D32, R76-R80, LED31/LED32 | Cerbo GX master alarm |
| AL17| Standard NO | Q33,Q34, D33,D34, R81-R85, LED33/LED34 | Refrigeration (Cerbo temp alarm) |
| AL18| Standard NO | Q35,Q36, D35,D36, R86-R90, LED35/LED36 | Water in fuel sensor |
| AL19| Standard NO | Q37,Q38, D37,D38, R91-R95, LED37/LED38 | E/R heat sensor |
| AL20| Standard NO | Q39,Q40, D39,D40, R96-R100, LED39/LED40 | E/R smoke sensor |
| AL21| Standard NO | Q41,Q42, D41,D42, R101-R105, LED41/LED42 | Balmar/Wakespeed alarm |
| AL22| Standard NO | Q43,Q44, D43,D44, R106-R110, LED43/LED44 | Spare. Col 2 Row 3 (CN5) |
| AL23| Standard NO | Q45,Q46, D45,D46, R111-R115, LED45/LED46 | Spare. Col 2 Row 7 (CN2) |
| AL24| **Comparator** | Q47,Q48, D47,D48, R116-R120, LED47/LED48 | Overcharging detect (TP4056 circuit). **LEE CONFIRMED Col 3 Pos 5** |
| AL25| Standard NO | Q57,Q58, D17,D18, R26-R30, LED11/LED12 | Spare. Col 4 Row 2 (CN4). **CORRECTED** (was LED49/50) |
| AL26| Standard NO | Q13,Q14, D19,D20, R31-R35, LED13/LED14 | Spare. Col 4 Row 8 (CN3). **CORRECTED** (was LED53/54) |
| AL27| Standard NO | Q55,Q56, D21,D22, R136-R140, LED15/LED16 | Spare. Col 1 Row 7 (CN8). **CORRECTED** (was LED55/56) |
| AL28| **Comparator** | Q49,Q50, D55,D56, R121-R125, LED49/LED50 | Battery temp (TP4056 circuit). **CORRECTED** (was LED57/58) |
| AL29| Standard NO | Q51,Q52, D51,D52, R126-R130, LED51/LED52 | Spare. **LEE CONFIRMED Col 3 Pos 7** |

### Component Position Mapping Note
AL25-29 use remapped Q/R/LED numbering in the schematic (schematic position ≠ AL number):
- AL6 → LED58/57, Q59/Q60, D63/D64, R141-R145 (was mislabeled as LED11/12)
- AL7 → LED59/60, Q61/Q62, D65/D66, R146-R151 (was mislabeled as LED13/14)
- AL8 → LED55/56, Q55/Q56, D61/D62, R136-R140 (was mislabeled as LED15/16)
- AL25 → LED11/12, Q57/Q58, D17/D18, R26-R30 (was mislabeled as LED49/50)
- AL26 → LED13/14, Q13/Q14, D19/D20, R31-R35 (was mislabeled as LED53/54)
- AL27 → LED15/16, Q55/Q56, D21/D22, R136-R140 (was mislabeled as LED55/56)
- AL28 → LED49/50, Q49/Q50, D55/D56, R121-R125 (was mislabeled as LED57/58)
- AL29 → LED52/51, Q51/Q52, D57/D58, R126-R130
(AL30 / LED53/LED54 DELETED from design)

## Special Circuit Types

### NC (Normally Closed) — AL8
Alarm triggers when the loop OPENS (wire cut, connector pulled).
Circuit inverts the standard NO logic: LED off when loop closed, LED on when loop opens.

### Comparator — AL24, AL28
Uses TP4056-based comparator circuit instead of simple transistor switch.
Monitors analog voltage level against a threshold.
- AL24: Overcharging detection
- AL28: Battery temperature detection

### Power/Running Indicator LEDs (NOT AL circuits)
U1, U2, U4 are YLED0805YG green LEDs driven directly by 24V buses.
They are standalone indicators, not part of any AL alarm circuit.
- U1: M/E ignition +24V → green LED on Col 2 Row 4 (alongside AL6 red LED)
- U2: GenSet ignition +24V → green LED on Col 2 Row 5 (alongside AL7 red LED)
- U4: Panel +24V → green LED (panel power indicator)
- U3: 78L05-EV voltage regulator (SOT-89, for AL28 comparator circuit)
- U5: LM393DR2G comparator (SOIC-8, for AL28 battery temp circuit)

## Open Questions
1. Confirm component numbering for AL22-29 (the pos remapping from summary)
2. AL9 NC→NO change: does this require component value changes or just a wiring change?
3. Exact comparator circuit topology for AL24/AL28
