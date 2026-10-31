---
doc_id: AST-PLN-001
title: AirStreet project plan
project: AirStreet
doc_type: Project plan
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First project plan with stage gates and the reference list (kit 1.9.1 upgrade)
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "Decisions 1 to 5 done on 2026-10-30; node cost USD 437.00"
---

# AirStreet project plan

AirStreet is at stage P3 (design outputs, TRL 3): the constructable design, drawings, priced BOM, build plan, decisions register and first-pass design FMEA exist, and every concept option is modelled to D3. The next gate is P4 (verification, TRL 4), on hold while the portfolio is capped at TRL 3; Amish decided the five open decisions of AST-DEC-001 on 2026-10-30 (AST-DDR-006), so none is open now; the pole owner's load confirmation and the approach to the first partner are his actions. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Design and CAD | Design lead | D3 model of every option, STEP files, drawings AST-DWG-001 and 101 to 109 | Done at P3 (kit 1.9.1) |
| Calculations and STEM check | Design lead | AST-CAL-001 v0.8, AST-STM-001 | Done; twelve plausible rows of option A to close at TRL 4 or in FieldNode |
| Requirements and traceability | Design lead | AST-URS-001, AST-PRS-001, AST-RTM-001 | Done; targets to review with the partner |
| Build plan | Design lead | AST-BLD-001 | Done (plan, not yet built) |
| Partner and collocation site | Project lead | Agreement with a city or agency that runs a street-level NO2 reference station | Not started; first candidate named (AST-DEC-001) |
| FieldNode interface | Project lead, with FieldNode | FieldNode's agreement to the adapter plate mount and the always-on port B | Request approved 2026-10-02; agreement outstanding |
| Renders and storefront | Project lead | Options picture, product renders and cards from `cad/src/product_model.py` | To render on Amish's Mac |

## Resources needed

Table 2. Resources (TRL 4 work, on hold).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Parts for two prototype nodes and one spare pod | Built nodes for collocation | Purchase | About 1,000 (two nodes at 437.00 plus a pod at about 130; estimate) |
| 3D printer time and a maker | Printed saddles, pods, shields | About 3 days | Material only (in the BOM) |
| CalRig time | T, RH and PM checks per pod | About 2 days | Lab time |
| Reference station collocation | 14 days before deployment, then every 6 months | Partner time | To agree with the partner |
| Installer with a work platform | Two installations and one exchange | Half a day each | To quote locally |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Done |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT | Done |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed | Done except the STEM check (open: seven plausible rows of option A) and the concept selection (decided by Amish on 2026-10-30) |
| P3 Design outputs | Model, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability | Done (kit 1.9.1, 2026-10-24) |
| P4 Verification | Lab and collocation tests (TST), verification report | On hold (TRL cap 3) |
| P5 Validation | Field trial with the partner | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Done on 2026-10-30: Amish decided the five decisions of AST-DEC-001 (AST-DDR-006): option A, the diffusion tube cross-check at the anchor node and one node in five, flagged hot hours now, both EU limits for PR-004, and the text of PR-017 and PR-018.
2. Render the options picture and the product renders on Amish's Mac (`python .kit/options.py`; `.kit/export_views.py`, `.kit/photoreal.py`, `.kit/cards.py`).
3. Approach the first partner candidate; when agreed, fix the radio band and FieldNode antenna in the BOM.
4. When the TRL cap is lifted: build two nodes to AST-BLD-001 and collocate them (P4).

## References

Every source cited in this repo's documents, Chicago style.

- Alphasense. "NO2-B43F Nitrogen Dioxide Sensor." Product page and data sheet. Accessed October 24, 2026. https://www.alphasense.com/products/view-by-target-gas/no2-b43f and https://pdf.directindustry.com/pdf/alphasense/no2-b43f/16860-1025996.html.
- AirQo. "AirQo." Accessed September 25, 2026. https://www.airqo.net/.
- Apte, Joshua S., et al. "High-Resolution Air Pollution Mapping with Google Street View Cars." *Environmental Science and Technology* 51 (2017): 6999 to 7008. https://pubs.acs.org/doi/10.1021/acs.est.7b00891.
- Barkjohn, Karoline K., et al. "Development and Application of a United States-Wide Correction for PM2.5 Data Collected with the PurpleAir Sensor." *Atmospheric Measurement Techniques* 14 (2021): 4617 to 4637. https://amt.copernicus.org/articles/14/4617/2021/.
- Breathe London. "Breathe London." Accessed September 25, 2026. https://www.breathelondon.org/.
- Centre for Science and Environment. "Only 12 per cent of India's census cities and towns have air quality monitoring stations." 2023. https://www.cseindia.org/only-12-per-cent-of-india-s-census-cities-and-towns-have-air-quality-monitoring-stations-11779.
- CEN. CEN/TS 17660-1:2021, *Air Quality: Performance Evaluation of Air Quality Sensor Systems, Part 1: Gaseous Pollutants in Ambient Air*. Catalogue entry accessed October 24, 2026. https://iteh.es/catalog/standards/cen/5bdb236e-95a3-4b5b-ba7f-62ab08cd21f8/cen-ts-17660-1-2021.
- Defra. *Diffusion Tubes for Ambient NO2 Monitoring: Practical Guidance*. AEA Energy and Environment, 2008. https://laqm.defra.gov.uk/documents/0802141004_NO2_WG_PracticalGuidance_Issue1a.pdf.
- European Environment Agency. *Harm to Human Health from Air Pollution in Europe*. 2024. https://www.eea.europa.eu/en/analysis/publications/harm-to-human-health-from-air-pollution-2024.
- European Union. Directive 2008/50/EC on Ambient Air Quality and Cleaner Air for Europe. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050.
- European Union. Directive (EU) 2024/2881 on Ambient Air Quality and Cleaner Air for Europe (Recast). *Official Journal*, November 20, 2024. https://eur-lex.europa.eu/eli/dir/2024/2881/oj.
- Feather River Air Quality Management District. "Clarity Estimate" no. 1584, April 19, 2021. https://fraqmd.specialdistrict.org/files/295d30216/Item+5+-+Clarity+Estimate.pdf.
- Mapping for Change. *Air Quality Mapping Toolkit: NO2*. 2015. https://mappingforchange.org.uk/wp-content/uploads/2015/07/Air-Quality-Mapping-Toolkit_NO2_2015.pdf.
- Oklahoma Department of Environmental Quality. "National Ambient Air Quality Standards (NAAQS)." Accessed October 24, 2026. https://oklahoma.gov/deq/divisions/air-quality/ambient-monitoring/naaqs.html.
- OpenAQ. *Open Air Quality Data: The Global State of Play*. 2020. https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf.
- Palmes, E. D., et al. "Personal Sampler for Nitrogen Dioxide." *American Industrial Hygiene Association Journal* 37 (1976): 570 to 577.
- Petters, M. D., and S. M. Kreidenweis. "A Single Parameter Representation of Hygroscopic Growth and Cloud Condensation Nucleus Activity." *Atmospheric Chemistry and Physics* 7 (2007): 1961 to 1971.
- REHVA. "Ambient Air Quality Directives (AAQD)." Accessed October 24, 2026. https://www.rehva.eu/eu-policy/policy-issues/ambient-air-quality-directives-aaqd.
- Sensirion. "SPS30 Particulate Matter Sensor." Data sheet, July 2023. https://sensirion.com/products/catalog/SPS30.
- South Coast AQMD AQ-SPEC. "AQMesh v5.1 (Gas) Field Evaluation." 2021. https://www.aqmd.gov/docs/default-source/aq-spec/field-evaluations/aqmesh-v5-1_gas---field-evaluation.pdf.
- SparkFun. "Particulate Matter Sensor, SPS30 (SEN-15103)." Accessed October 24, 2026. https://www.sparkfun.com/particulate-matter-sensor-sps30.html.
- The Things Network. "Regional Limitations of RF Use." Accessed October 24, 2026. https://www.thethingsnetwork.org/docs/lorawan/regional-limitations-of-rf-use/.
- The Things Network. "The Things Network Fair Use Policy." Forum, accessed October 24, 2026. https://www.thethingsnetwork.org/forum/t/the-things-network-fair-use-policy/47689.
- US EPA. "Air Sensor Performance Targets and Testing Protocols." Accessed October 24, 2026. https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols.
- US EPA. "Basic Information about NO2." https://www.epa.gov/no2-pollution/basic-information-about-no2.
- US EPA. "Research on Near Roadway and Other Near Source Air Pollution." https://www.epa.gov/air-research/research-near-roadway-and-other-near-source-air-pollution.
- US National Park Service. "A Low-Cost Air Quality Sensor for Measuring Particulate Matter." Accessed October 24, 2026. https://www.nps.gov/articles/000/a-low-cost-air-quality-sensor-for-measuring-particulate-matter.htm.
- World Health Organization. "Ambient (Outdoor) Air Quality and Health." Fact sheet. https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health.
- Zimmerman, Naomi, et al. "A Machine Learning Calibration Model Using Random Forests to Improve Sensor Performance for Lower-Cost Air Quality Monitoring." *Atmospheric Measurement Techniques* 11 (2018): 291 to 313. https://amt.copernicus.org/articles/11/291/2018/.
- FieldNode repository: FND-CAL-001, FND-REQ-001, FND-DDR-001 and FND-DDR-003 (shared lab core).
