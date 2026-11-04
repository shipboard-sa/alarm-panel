# Bill of Materials
<!-- Purpose: BOM for V2.2 alarm panel PCB (AL30 deleted, 29 channels, CN9 added) -->
<!-- Version: 0.3 (CN9 added, stats updated for V2.2 2026-10-29) -->
<!-- Scope: producible board — all part numbers from EasyEDA schematic -->

## Summary

| Category | Qty | Package | LCSC | Manufacturer Part |
|----------|-----|---------|------|-------------------|
| Resistor 2.2K 1% | 102 | 1206 | C325909 | Tyohm RMC12062.2K1%N |
| Resistor 10K | 64 | 0805 | C3013856 | Vishay TNPW080510K0FEEA |
| Diode 1N4148WX | 59 | SOD-323 | C19089391 | Yongyutai 1N4148WX |
| LED ORANGE backlight | 41 | 0805 | C5123498 | BrtLed BL-HJC35A-AV-TRB |
| LED RED indicator | 29 | 0805 | C9900019100 | SMD Red LED 0805 |
| Transistor PNP (Q_even) | 29 | SOT-23 | C52792 | ST P0102BL5AA4 |
| Transistor NPN (Q_odd) | 29 | SOT-23 | C53373686 | CCX MMBT2222A |
| Connector 8-pin 5.08mm | 8 | KF142V-5.08-8P | C475140 | KEFA KF142V-5.08-8P |
| Connector 3-pin 5.08mm | 1 | KF142V-5.08-3P | C475135 | KEFA KF142V-5.08-3P |
| Header 2-pin (H4, H5) | 2 | 2.54mm TH | C492401 | XFCN PZ254V-11-02P |
| Header 2-pin SMD (H1-H3) | 3 | 1.27mm SMD | C55213900 | Shou Han PZ1.27-1x2PLT |
| Capacitor 100nF | 3 | 0805 | C49678 | Yageo CC0805KRX7R9BB104 |
| TVS diode SMBJ26A | 3 | SMB | C135062 | Diodes Inc SMBJ26A-13-F |
| Schottky SS54 | 3 | SMA | C22452 | MDD SS54 |
| LED GREEN indicator | 3 | 0805 | C19171393 | Yongyutai YLED0805YG |
| Buzzer | 1 | TH 12mm | C96095 | HMB1206-05 |
| Diode 1N5819W | 1 | SOD-123F | C169540 | 1N5819W |
| Transistor MMBT8050D | 1 | SOT-23 | C411762 | PJSEMI MMBT8050D |
| Voltage regulator 78L05 | 1 | SOT-89 | C28642115 | 78L05-EV |
| Comparator LM393 | 1 | SOIC-8 | C7955 | ON Semi LM393DR2G |

## Component Counts by Type

| Prefix | Count | Notes |
|--------|-------|-------|
| R | 166 | 102× 1206 (2.2K) + 64× 0805 (10K) |
| LED | 70 | 29 RED + 41 ORANGE (delete LED53/LED54 for final = 68) |
| D | 66 | 59× 1N4148WX + 3× SMBJ26A + 3× SS54 + 1× 1N5819W |
| Q | 59 | 29× PNP + 29× NPN + 1× MMBT8050D |
| CN | 9 | CN1-CN8: KF142V-5.08-8P; CN9: KF142V-5.08-3P (mute/buzzer interface) |
| H | 5 | H1-H3 SMD 1.27mm, H4-H5 TH 2.54mm (MUTE/TEST buttons) |
| U | 5 | U1/U2/U4 = GREEN LEDs, U3 = 78L05, U5 = LM393 |
| C | 3 | 100nF decoupling |
| BUZZER | 1 | Through-hole piezo |
| **Total** | **384** | **382 after AL30 deletion** |

## Component Corrections (from this session)

| Designator | Old (register 0.1) | Corrected |
|------------|-------------------|-----------|
| U1 | Comparator IC (AL25) | YLED0805YG green LED — M/E running indicator |
| U2 | Comparator IC (AL26) | YLED0805YG green LED — GenSet running indicator |
| U4 | Amber LED (TEST) | YLED0805YG green LED — panel power indicator |
| U3 | — | 78L05-EV voltage regulator (SOT-89, AL28 comparator) |
| U5 | — | LM393DR2G comparator (SOIC-8, AL28 battery temp) |
| H4 | — | 2-pin TH header for TEST button |
| H5 | — | 2-pin TH header for MUTE button |
| AL25/26 | Green LED drivers | Spare NO alarm channels |
| LED53/54 | AL30 | DELETED (AL30 removed from design) |

## PCB Fabrication Specs

| Parameter | Value |
|-----------|-------|
| Layers | 2 |
| Dimensions | 279mm × 114mm |
| Substrate | FR-4 |
| Copper weight | 1 oz (ASSUMED) |
| Surface finish | HASL (ASSUMED) |
| Min trace/space | EasyEDA default |
| Connections | 950 |
| Vias | 226 |
| DRC | 0 errors |

## JLCPCB Order Checklist
1. Export Gerber from EasyEDA (File → Export → Gerber)
2. Export BOM CSV from EasyEDA (File → Export → BOM)
3. Export Pick-and-Place / CPL file from EasyEDA
4. Upload to JLCPCB.com → order PCB + SMT assembly
5. Verify all LCSC part numbers are in stock
6. Through-hole components (buzzer, CN1-CN9, H4-H5) = hand-solder

## Notes
- MUTE/TEST are lighted panel-mount pushbuttons wired to H4/H5 headers (not PCB-mounted)
- Buzzer is through-hole, soldered to PCB, sound exit through faceplate hole
- All CN connectors are KF142V-5.08-8P vertical mount TH (hand-solder)
- SMT assembly covers: LEDs, resistors, transistors, diodes, capacitors, U3, U5, H1-H3
