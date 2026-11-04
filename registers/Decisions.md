<!--
Purpose: Decision register for the Alarm Panel V2 PCB — every binding choice about
  schematic, layout, component selection, and fabrication.
Version: v1 (2026-10-30) - created.
Scope: STANDALONE UTILITY - PCB design project.
Architecture: Alarm panel register. Prefix AP-D-. Circuit-level decisions that affect the
  panel live in wiring-io wiki/Design-Decisions.md.
Invocation: n/a (reference doc)
-->

# Alarm Panel — Decision Register

Prefix: **AP-D-**. One row per binding choice.

| ID | Decision | Status | Cross-refs |
|----|----------|--------|------------|
| AP-D-001 | **V2.2 ordered 2026-10-29 from JLCPCB.** V2.1 cancelled (missing mute/buzzer connector). | ORDERED | CHECKPOINT |
| AP-D-002 | **U1/U2/U4 = green indicator LEDs (YLED0805YG), not ICs.** | ACCEPTED | Memory `feedback-alarm-panel-u-packages` |
| AP-D-003 | **AL25/AL26 = spare channels, not LED drivers.** | ACCEPTED | Memory `feedback-alarm-panel-u-packages` |
| AP-D-004 | **Connectors sit one column LEFT of their LEDs (signal flow convention).** | ACCEPTED | Memory `alarm-pcb-layout-lessons` |
