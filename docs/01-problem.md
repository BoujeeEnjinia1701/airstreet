---
doc_id: AST-PRB-001
title: AirStreet problem statement
project: AirStreet
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update; constraints and open questions reflect AST-DDR-001 and AST-CAL-001
---

# AirStreet problem statement

Regulatory air monitors are few and far apart, missing the streets where people breathe traffic pollution.

## The problem

Traffic pollution varies sharply over short distances, but official monitoring is designed to describe whole cities. When Google Street View cars carrying reference-grade instruments drove every street in a 30 km² area of Oakland, California, nitrogen dioxide (NO2), nitric oxide and black carbon varied by up to 5 to 8 times within single city blocks ([Apte et al., 2017](https://pubs.acs.org/doi/10.1021/acs.est.7b00891)). A single fixed station cannot show that pattern, and many cities have no station at all. Only 12 % of India's 4,041 census cities and towns have any air quality monitoring ([CSE, 2023](https://www.cseindia.org/only-12-per-cent-of-india-s-census-cities-and-towns-have-air-quality-monitoring-stations-11779)), and in 2020 OpenAQ found no public national government monitoring program in 13 populous countries, including Pakistan, Nigeria, Ethiopia, Kenya and Uganda ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)).

The health stakes are large. Ambient air pollution caused an estimated 4.2 million premature deaths worldwide in 2019 ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)). NO2 comes mainly from burning fuel in cars, trucks, buses, power plants and off-road equipment ([US EPA](https://www.epa.gov/no2-pollution/basic-information-about-no2)), so it is highest on busy streets, and more than 45 million people in the United States live within about 90 m (300 ft) of a major transportation facility ([US EPA](https://www.epa.gov/air-research/research-near-roadway-and-other-near-source-air-pollution)).

Low-cost sensors could fill the gap between stations, but raw readings are not trusted. Uncorrected PurpleAir particle sensors overestimated PM2.5 by about 40 % across the United States until a humidity-aware correction cut the error from 8 to 3 µg/m³ ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)). Electrochemical NO2 sensors respond to temperature, humidity and other gases, and laboratory calibration alone does not correct this; in a Pittsburgh study only field-calibrated models reached a mean absolute error of about 3.5 ppb for NO2 ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)).

AirStreet addresses one specific gap: an open, pole-mounted node that measures PM2.5 and NO2 at street level, with a calibration method stated up front, so a city, school or community group can build a neighborhood map that others can check.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Residents and community groups | See pollution on their own streets, near schools and clinics, and track whether it changes | Street poles on residential and arterial roads |
| Municipal environment and transport teams | Evaluate interventions such as low-traffic streets, school streets, bus corridors and freight routes | 10 to 100 nodes per district, alongside at least one reference station |
| Schools and universities | Teaching and research on exposure, with raw data and a documented method | Campus and nearby streets |
| Street furniture owners (utilities, city lighting) | A small, light device that does not interfere with the pole or its wiring | Street light and signal poles |
| Researchers and data platforms | Raw signals and calibration versions, so data can be reprocessed | Open data portals |

## Operating environment

- Mounted on a street light or signal pole, inlets 3.0 m above the sidewalk (AST-DDR-001 D7, adopted for TRL 3 work, open for Amish's review), on the street side and within a few meters of the kerb.
- Outdoor, in sun, rain, dust and traffic spray; temperate to hot humid climates (about -10 to 50 °C, 10 to 100 % RH, estimate to be confirmed with partners). FieldNode is rated to 45 °C ambient and the SPS30 particle sensor is recommended for 20 to 80 % RH, so the hottest and most humid sites are at risk (AST-CAL-001).
- No mains power: runs on the FieldNode solar and battery core.
- Data over LoRaWAN to a community or municipal gateway (for example the lab's TwinKit gateway) or a public network.

## Constraints

- Garage-buildable prototype. The $180 `budget_usd` covers the AirStreet sensor head; the FieldNode core is costed in FieldNode (AST-DDR-001 D1). A rise to about $280 is recommended and awaiting Amish. The sensor head costs $283.00 at TRL 3 prices, over both figures (see [03-requirements.md](03-requirements.md)).
- Built on FieldNode, the lab's shared outdoor core, with its power budget and sensor port pinout.
- Temperature, humidity and particle checks on CalRig. CalRig does not cover NO2, so NO2 must be calibrated by field collocation with a reference station.
- Levels only: no images, audio or personal data collected or sent.
- Mounting only with the pole owner's permission, without drilling the pole or opening its electrical access.

## Out of scope

- Regulatory compliance monitoring. AirStreet data are indicative and do not replace reference stations.
- Other pollutants (ozone, carbon monoxide, black carbon, ultrafine particles) in this version.
- Personal exposure devices and indoor use.
- Health advice or medical claims.

## Prior work

- Street-scale mapping with reference instruments on vehicles showed block-level variation ([Apte et al., 2017](https://pubs.acs.org/doi/10.1021/acs.est.7b00891)).
- Community and city networks of low-cost sensors already operate, for example AirQo, which reports more than 400 PM2.5 sensors across 14 African countries ([AirQo](https://www.airqo.net/)), and Breathe London, a sensing network developed with the Mayor of London ([Breathe London](https://www.breathelondon.org/)).
- The US EPA published performance testing protocols for NO2, CO and SO2 sensors in February 2024, including field evaluation alongside regulatory monitors ([US EPA](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols)).
- Humidity correction for optical particle sensors ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)) and field calibration of electrochemical gas sensors ([Zimmerman et al., 2018](https://amt.copernicus.org/articles/11/291/2018/)) are established methods that AirStreet adopts rather than reinvents.

What is missing is an open, documented node design that pairs these sensors with a stated, repeatable calibration route and publishes raw signals.

## Open questions

- Which city and partner first, and which reference station can host a collocation? Proposed, awaiting Amish (AST-DDR-001 O1).
- Inlet height: 3.0 m is adopted for TRL 3 work, open for Amish's review; partners may still prefer a lower inlet, closer to the breathing zone.
- Is NO2 accuracy of about 4 to 5 ppb hourly, which cannot resolve the WHO annual guideline but can rank streets, useful enough for the first partner's questions? To be tested with users.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
