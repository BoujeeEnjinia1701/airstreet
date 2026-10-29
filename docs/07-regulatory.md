---
doc_id: AST-REG-001
title: AirStreet regulatory and standards register
project: AirStreet
doc_type: Regulatory register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "First register (kit 1.9.1 upgrade); the first Smart Cities register, with air quality rows A1 to A6 for other Smart Cities repos to cite"
---

# AirStreet regulatory and standards register

Which standards and regulations bear on AirStreet, where, and what is needed. AirStreet is a research and community prototype that gives indicative air quality levels; it is not a regulatory monitor, and nothing here claims compliance with an air quality standard. This is not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Rows A1 to A6 are researched once for the Smart Cities focus area and can be cited by other repos in it. Rows marked FieldNode belong to the shared FieldNode core and are assessed in its repository. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Directive 2008/50/EC on ambient air quality and cleaner air for Europe [1] | European Union | Limit values (NO2 annual 40 ug/m3) and the siting of sampling points (inlets in general 1.5 to 4 m above ground) | AirStreet's 3.0 m inlet is inside the range (PR-011); PR-004 classifies streets against 40 ug/m3 at the directive's 20 degC reference. The annex's other siting rules (distance from the kerb and from junctions) are to check per site. AirStreet data are indicative and do not replace the directive's fixed measurements | Project lead | Met by design for the inlet; does not apply as a compliance claim |
| A2 | Directive (EU) 2024/2881 on ambient air quality and cleaner air for Europe (recast), published 20 November 2024 [2] | European Union | Recast of A1; annual limit values from 2030 of 20 ug/m3 for NO2 and 10 ug/m3 for PM2.5 [3] | Sets a lower NO2 limit than PR-004 uses; at AirStreet's uncertainty a street could be classified against 20 ug/m3 only outside 13.9 to 26.1 ug/m3 (AST-CAL-001 [C5]) | Project lead | To assess (AST-DEC-001, open decision 4) |
| A3 | US National Ambient Air Quality Standards: NO2 annual 53 ppb and 1-hour 100 ppb; PM2.5 annual 9.0 ug/m3 and 24-hour 35 ug/m3 [4] | United States | Ambient standards met by regulatory (federal reference or equivalent) monitors | The first partner candidate is in Texas (AST-DEC-001); AirStreet's data can be compared with these levels as indicative values only | Partner organization | Does not apply as a compliance claim; context for a US partner |
| A4 | US EPA air sensor performance testing protocols and targets: PM2.5 and ozone (February 2021); NO2, CO and SO2 (February 2024) [5] | United States (voluntary) | Base and enhanced testing of sensors beside reference monitors, with performance targets | The route for the TRL 4 collocation and for reporting AirStreet's NO2 and PM2.5 performance in a recognised form | Design lead | Applies as practice at TRL 4; to assess against the protocol text |
| A5 | CEN/TS 17660-1:2021, performance evaluation of air quality sensor systems, part 1: gaseous pollutants in ambient air [6] | European Union (technical specification) | Laboratory and field tests and classes for sensor systems used for indicative measurement | Applies to the NO2 channel if a European partner wants a classed result; the particulate part of the series is to assess | Design lead | To assess (the text has not been read; it must be bought) |
| A6 | Defra, diffusion tubes for ambient NO2 monitoring, practical guidance [7] | United Kingdom (guidance, widely used) | Exposure of 2 to 4 weeks, 2 to 4 m height, triplicate tubes, bias adjustment by collocation, about 25 % uncertainty | Option C of AST-OPT-001 and the proposed cross-check of open decision 2 | Design lead | Applies if option C or the cross-check is chosen |
| R1 | ETSI EN 300 220 and the LoRaWAN EU868 regional parameters (1 % duty cycle per sub-band) [8] | European Union and countries using EU868 | Duty cycle and power in 863 to 870 MHz | 0.60 % at SF12 (PR-010) | Design lead | Met by design on paper (AST-CAL-001 [B3]) |
| R2 | FCC 47 CFR Part 15 and the LoRaWAN US915 regional parameters (400 ms dwell time; DR0 at SF10 carries 11 bytes) [9] | United States and countries using US915 | Dwell time and payload per data rate | The 20-byte record goes at SF9 or faster, 247 ms (PR-010) | Design lead | Met by design on paper (AST-CAL-001 [B5]); certified radio module in FieldNode |
| R3 | The Things Network fair use policy (30 s of uplink airtime a day per node; 10 downlinks) [10] | Network operator | Airtime per device | 15 min records on TTN, 23.7 s a day at SF9 (PR-008) | Design lead | Met by design on paper (AST-CAL-001 [B8]) |
| R4 | Radio Equipment Directive 2014/53/EU and national type approval | European Union; each partner country | Placing radio equipment on the market | AirStreet uses FieldNode's certified LoRa module; prototypes built by a partner are not placed on the market | FieldNode lead | To assess (FieldNode) |
| E1 | IEC 60529, degrees of protection by enclosures (IP code) | International | IP65 and other ratings | Electronics in FieldNode's IP65 enclosure; the pod is open below by design (its inlets), so its electronics rely on the drip lid, mesh and conformal coating | Design lead | Met by choice of parts on paper (FieldNode); pod to verify at TRL 4 |
| E2 | Lithium cell safety and transport: IEC 62133-2 and UN 38.3 | International | Safety and shipping of the LiFePO4 cell | The cell is in the FieldNode core | FieldNode lead | To assess (FieldNode) |
| E3 | Regulation (EU) 2023/1542 on batteries | European Union | Labelling, removability and end of life of batteries | FieldNode's cell, if units are placed on the EU market | FieldNode lead | To assess (FieldNode); not for a research prototype |
| E4 | WEEE Directive 2012/19/EU and RoHS Directive 2011/65/EU | European Union | End of life and restricted substances in electrical equipment | The sensors, boards and cables; electrochemical cells go back to their maker for disposal | Design lead | To assess before any supply beyond research prototypes |
| S1 | The pole owner's attachment rules and street works permission | Partner city | Permission, load, inspection and insurance for devices on street furniture | Every installation (PR-018); the owner checks the 3.77 kg and 125 N wind load | Partner organization | Applies; to assess with the first pole owner |
| S2 | National rules for work at height and traffic management at the roadside | Partner country | Platforms, ladders and traffic management for street works | Every installation and pod exchange (PR-018, AST-BLD-001 safety stops) | Partner organization | Applies; to assess with the partner |
| S3 | The NO2 cell maker's safety data sheet (acid electrolyte) | Supplier | Handling, storage and disposal of electrochemical cells | Cells are fitted and replaced on the ground and returned for disposal (PR-016) | Design lead | Applies |
| D1 | General Data Protection Regulation (EU) 2016/679 and similar privacy law | European Union and others | Processing of personal data | AirStreet collects levels, T and RH only: no images, audio or identifiers (PR-014) | Design lead | Does not apply (met by design) |
| D2 | The partner's open data licence and the platform's terms (for example OpenAQ) | Partner and platform | Licence and attribution for published data | Calibrated hourly data with the calibration version (AST-DDR-001 D9) | Partner organization | To assess with the partner |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

1. Directive 2008/50/EC of the European Parliament and of the Council of 21 May 2008 on ambient air quality and cleaner air for Europe, Annex III, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050, accessed 2026-09-25.
2. Directive (EU) 2024/2881 of the European Parliament and of the Council of 23 October 2024 on ambient air quality and cleaner air for Europe (recast), https://eur-lex.europa.eu/eli/dir/2024/2881/oj, and its summary at UNEP LEAP (Official Journal, 20 November 2024), https://leap.unep.org/en/countries/eu/national-legislation/directive-eu-20242881on-ambient-air-quality-and-cleaner-air, accessed 2026-10-24.
3. REHVA, "Ambient Air Quality Directives (AAQD)" (2030 annual limits of 20 ug/m3 for NO2 and 10 ug/m3 for PM2.5), https://www.rehva.eu/eu-policy/policy-issues/ambient-air-quality-directives-aaqd, accessed 2026-10-24.
4. Oklahoma Department of Environmental Quality, "National Ambient Air Quality Standards (NAAQS)" (table of the federal standards), https://oklahoma.gov/deq/divisions/air-quality/ambient-monitoring/naaqs.html, accessed 2026-10-24.
5. US EPA, "Air Sensor Performance Targets and Testing Protocols," https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols, accessed 2026-10-24.
6. CEN/TS 17660-1:2021, catalogue entry, https://iteh.es/catalog/standards/cen/5bdb236e-95a3-4b5b-ba7f-62ab08cd21f8/cen-ts-17660-1-2021, accessed 2026-10-24.
7. Defra, *Diffusion Tubes for Ambient NO2 Monitoring: Practical Guidance*, https://laqm.defra.gov.uk/documents/0802141004_NO2_WG_PracticalGuidance_Issue1a.pdf, accessed 2026-10-24.
8. The Things Network, "Regional limitations of RF use" (EU868 1 % duty cycle; US915 400 ms dwell time), https://www.thethingsnetwork.org/docs/lorawan/regional-limitations-of-rf-use/, accessed 2026-10-24.
9. The Things Network, "US902-928 MHz regional parameters," https://www.thethingsnetwork.org/docs/lorawan/regional-parameters/us915/, as cited in SLW-REG-001 (SlopeWatch); the DR0 payload of 11 bytes to confirm against the LoRaWAN regional parameters text.
10. The Things Network forum, "The Things Network Fair Use Policy," https://www.thethingsnetwork.org/forum/t/the-things-network-fair-use-policy/47689, accessed 2026-10-24.
