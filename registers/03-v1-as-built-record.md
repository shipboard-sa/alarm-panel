# V1 Aqualarm Panel — As-Built Record
<!-- Purpose: Documents the original Aqualarm panel configuration as installed -->
<!-- Version: 0.1 -->
<!-- Source: Electrical Circuits2.xlsx "Master Alarm Panel" sheet -->

## Terminal Assignments (as-built, from spreadsheet)

| Terminal | Function                          | NO/NC | Source                                | Status      |
|----------|-----------------------------------|-------|---------------------------------------|-------------|
| AO 4     | Power                             | +24V  | Always On                             | —           |
| AL-GRND  | Ground                            | (-)   |                                       | —           |
| ME +     | Main Engine Ignition              | +24V  | R10                                   | —           |
| ME -     | Main Engine Ground                | (-)   |                                       | —           |
| GS +     | GenSet Ignition                   | +24V  | R9                                    | Needs test  |
| GS -     | GenSet Ground                     | (-)   |                                       | —           |
| AL-1     | Engine Bilge Pump                 | NO    | R25                                   | Tested ✓    |
| AL-2     | High Water Bow                    | NO    | Float Switch - Bow                    | Tested ✓    |
| AL-3     | Salon Bilge Pump                  | NO    | R26                                   | Tested ✓    |
| AL-4     | High Water - Salon                | NO    | Float Switch - Salon Bilge            | Tested ✓    |
| AL-5     | Fresh Water Pump                  | NO    | R27                                   | Tested ✓    |
| AL-6     | Main Engine Water Flow            | NO    | Water Flow Detector - E/R M-E         | Needs test  |
| AL-7     | GenSet Water Flow                 | NO    | Water Flow Detector - E/R GenSet      | Needs test  |
| AL-8     | Dinghy Theft                      | NC    | Dinghy Theft Loop - Cockpit/Helm Switch | Tested ✓  |
| AL-9     | Bow Bilge Pump                    | NC    | R28                                   | Tested ✓    |
| AL-10    | Auto Pilot CCU Error              | NO    | R24                                   | Needs test  |
| AL-11    | AIS                               | NO    | R1 - RTU 1                            | Needs forced error test |
| AL-12    | Anchor Drag                       | NO    | Anchor Drag - Nav Station             | —           |
| AL-13    | Spare                             | NO    | —                                     | —           |
| AL-14    | Multiplus - alarm relay           | NO    | R19                                   | Needs test  |
| AL-15    | Battery Protect - Alarm out       | NO    | R22                                   | Needs test  |
| AL-16    | Cerbo GX - master alarm           | NO    | R20                                   | Tested ✓    |
| AL-17    | Refrigeration (Cerbo GX Temp)     | NO    | R21                                   | Tested ✓    |
| AL-18    | Water In Fuel                     | NO    | Water In Fuel Sensor - Racor - E/R    | Needs test  |
| AL-19    | Engine Room - Fire (Heat)         | NO    | Heat Sensor in E/R                    | Needs test  |
| AL-20    | Engine Room - Smoke               | NO    | R11                                   | Tested ✓    |
| AL-21    | Balmar (Wakespeed) Alarm          | NO    | R1 - RTU 2                            | Tested ✓    |
| Buzzer   | Buzzer Output                     | +24V  | —                                     | Tested ✓    |

## V1 → V2 Changes

| AL  | V1 Function    | V2 Function          | Change                          |
|-----|----------------|----------------------|---------------------------------|
| AL-9| Bow Bilge (NC) | Bow Bilge (**NO**)   | Circuit type NC→NO (reused circuit 2026-10-28) |
| AL-13| Spare          | Automation Heartbeat | New function assignment         |
| —   | —              | AL22-AL29 added      | 8 new channels (2 comparator, 2 running detect, 4 spare/NO) |
| —   | —              | M/E Running (AL25)   | New 24V detect circuit with U1  |
| —   | —              | GenSet Running (AL26)| New 24V detect circuit with U2  |
| —   | —              | Overcharging (AL24)  | New comparator circuit          |
| —   | —              | Battery Temp (AL28)  | New comparator circuit          |
