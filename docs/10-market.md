---
doc_id: AST-MKT-001
title: AirStreet market and viability
project: AirStreet
doc_type: Market and viability
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First market and viability note with cited benchmarks (kit 1.9.1 upgrade)
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Node cost USD 437.00; cross-check chosen on 2026-10-30"
---

# AirStreet market and viability

AirStreet is for cities, community groups and schools that want street-by-street PM2.5 and NO2 with a calibration route they can check; it sits between consumer particle sensors, which do not measure NO2, and commercial multi-gas nodes, which cost thousands of dollars or a yearly data licence per node. An open design with raw signals lets a partner build, recalibrate and audit the network itself. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| District networks run by a city or air agency | Environment and transport teams; first candidate the Dallas-Fort Worth area (AST-DEC-001); 10 to 100 nodes beside a reference station | AQMesh v5.1 with five gas pods, PM and a heated inlet: about USD 7,800 per unit as tested in 2021 [1]; Clarity Node-S: data licence USD 1,200 per node per year in a 2021 estimate, hardware included [2]; regulatory monitors "USD 10,000 and up" [3] | 433.50 per node with the FieldNode core (302.50 for the sensor head; BOM) | NO2 and PM2.5 at a fraction of the commercial price, with raw signals and an open calibration method; no licence fee |
| Community groups and residents | Neighbourhood groups near busy roads, schools and clinics | PurpleAir sensor about USD 260, PM only [3] | 433.50 per node | Adds NO2, the traffic gas, and a calibration route tied to a reference station |
| Schools and universities | Teaching and exposure research | The same commercial nodes; diffusion tubes at about £8 per tube including analysis, monthly NO2 only (2015 price) [4] | 437.00 per node, plus spare pods for exchange | A buildable, documented node whose data and method students can reprocess |
| Annual NO2 surveys | Local authorities that use diffusion tubes today | About £8 per tube with analysis [4]; triplicate tubes every month, about £290 a year per site at that price | About 130 for option C's hardware (estimate, AST-OPT-001) | Not AirStreet's market; option C and the cross-check chosen on 2026-10-30 (decision 2) show how the two methods can work together |

Cost notes. The SPS30 is USD 60.50 at quantity 1 at SparkFun (USD 57.48 at 25 or more), checked 2026-10-24 [5]. The NO2 cell (USD 90) and its front end (USD 60) are estimates that are not quoted; they are about half the sensor-head cost and are to assess with a distributor. Running costs per node are a replacement NO2 cell every 12 months, or 18 to 24 where the site's ozone record allows (AST-CAL-001 [C7]), collocation time and CalRig time; none is in the BOM.

## Open route

The design is published under CERN-OHL-S-2.0 (hardware) and MIT (software), so a city, a university or a makerspace can build nodes from the drawings, the build plan and the BOM, with a 3D printer, a saw and a drill. The pod is the exchange unit, so a partner who prints spare pods can rotate them through CalRig and the reference site and keep every node calibrated. Raw signals and versioned calibrations keep the data reusable on open platforms such as OpenAQ. The first route is through the lab's own partner (AST-DEC-001), then through the Helpful Engineering network and universities that already run air sensor studies. Nothing commercial is planned while the portfolio is capped at TRL 3.

## Sources

1. South Coast AQMD AQ-SPEC, "AQMesh v5.1 (gas) field evaluation," 2021, https://www.aqmd.gov/docs/default-source/aq-spec/field-evaluations/aqmesh-v5-1_gas---field-evaluation.pdf, accessed 2026-10-24.
2. Feather River Air Quality Management District, board item 5, "Clarity estimate" no. 1584, 19 April 2021, https://fraqmd.specialdistrict.org/files/295d30216/Item+5+-+Clarity+Estimate.pdf, accessed 2026-10-24.
3. US National Park Service, "A low-cost air quality sensor for measuring particulate matter," https://www.nps.gov/articles/000/a-low-cost-air-quality-sensor-for-measuring-particulate-matter.htm, accessed 2026-10-24.
4. Mapping for Change, *Air Quality Mapping Toolkit: NO2* (2015), https://mappingforchange.org.uk/wp-content/uploads/2015/07/Air-Quality-Mapping-Toolkit_NO2_2015.pdf, accessed 2026-10-24.
5. SparkFun, "Particulate Matter Sensor - SPS30" (SEN-15103), https://www.sparkfun.com/particulate-matter-sensor-sps30.html, accessed 2026-10-24.
