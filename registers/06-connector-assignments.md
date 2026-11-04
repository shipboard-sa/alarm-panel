# Connector Pin Assignments
<!-- Purpose: Documents which AL signals connect to which connector pins -->
<!-- Version: 0.2 (CN9 added for mute/buzzer interface, V2.2 2026-10-29) -->
<!-- Source: V2.2 schematic net labels (post-swap) -->

## Connector Layout
All connectors are KF142V-5.08-8P (8 pins, 5.08mm pitch).
CN1-CN7: vertical mount (pins run top-to-bottom on PCB back).
CN8: horizontal mount (pins run left-to-right on PCB back).

## Pin Assignments (from V2.1 schematic, post-swap)

### CN1 (Column 1 group)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL4   | High Water Salon |
| 2   | AL3   | Salon Bilge      |
| 3   | AL1   | Engine Bilge     |
| 4   | AL2   | High Water Bow   |
| 5-8 | GND/+24V | Power/ground   |

### CN2 (Column 2 group — post-swap)
| Pin | Net   | Function              |
|-----|-------|-----------------------|
| 1   | AL7   | GenSet Raw Water      |
| 2   | AL18  | Water in Fuel         |
| 3   | AL23  | Spare                 |
| 4   | ME Pwr| M/E Ignition +24V    |
| 5   | GS Pwr| GenSet Ignition +24V |
| 6-8 | —     | GND/power             |

### CN3 (Column 4 group — post-swap)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL10  | Autopilot        |
| 2   | AL13  | Automation       |
| 3   | AL8   | Dinghy Theft (NC)|
| 4   | AL26  | Spare            |
| 5-8 | —     | GND/power        |

### CN4 (Column 4 group)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL17  | Fridge/Freezer   |
| 2   | AL25  | Spare            |
| 3   | AL11  | AIS              |
| 4   | AL12  | Anchor Drag      |
| 5-8 | —     | GND/power        |

### CN5 (Column 2 group)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL19  | E/R Heat         |
| 2   | AL20  | E/R Smoke        |
| 3   | AL22  | Spare            |
| 4   | AL6   | M/E Raw Water    |
| 5-8 | —     | GND/power        |

### CN6 (Column 3 group)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL24  | Overcharging     |
| 2   | AL28  | Battery Temp     |
| 3   | AL29  | Spare            |
| 4-5 | —     | Spare pins       |
| 6-8 | —     | GND/power        |

### CN7 (Column 3 group)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL16  | Master Electrical|
| 2   | AL14  | Inverter/Charger |
| 3   | AL15  | House Load Cutoff|
| 4   | AL21  | Balmar           |
| 5-8 | —     | GND/power        |

### CN8 (Column 1 group — horizontal, post-swap)
| Pin | Net   | Function         |
|-----|-------|------------------|
| 1   | AL27  | Spare            |
| 2   | AL5   | FW Pump          |
| 3   | AL9   | Bow Bilge Pump   |
| 4   | +24V  | Power            |
| 5   | GND   | Ground           |
| 6-8 | —     | —                |

### CN9 (External interface — mute/buzzer, 3-pin KF142V-5.08-3P)
| Pin | Net       | Function                                    |
|-----|-----------|---------------------------------------------|
| 1   | MuteBus   | Mute Out — Pi reads to detect panel ack      |
| 2   | MuteBus   | Mute In — Pi writes for remote mute          |
| 3   | BuzzerBus | Buzzer Out — drives external buzzer           |

CN9 is near the buzzer/mute area. Pins 1+2 both on MuteBus net (separate read/write terminals for Pi). Pin 3 on BuzzerBus net for off-panel buzzer.

## Swap Record
Three net-label swaps were applied to the schematic (connector pin assignments only — circuits and components unchanged):
1. **AL6 ↔ AL25**: M/E Raw Water signal swapped with M/E Running signal on connector pins
2. **AL7 ↔ AL26**: GenSet Raw Water signal swapped with GenSet Running signal on connector pins
3. **AL8 ↔ AL27**: Dinghy Theft signal swapped with spare signal on connector pins

## Open Questions
1. Exact pin-to-signal mapping for each connector (above is from summary, needs verification against schematic)
2. Which pins carry GND vs +24V on each connector
3. CN2 pins 4-5 (ME Pwr, GS Pwr) — confirm these are the ignition sense inputs for U1/U2
