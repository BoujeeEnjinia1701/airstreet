---
doc_id: AST-URS-001
title: AirStreet user requirements
project: AirStreet
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: First user requirements, drawn from AST-PRB-001 Tables 1 and 2 (kit 1.9.1 upgrade)
---

# AirStreet user requirements

What residents, city teams, schools, pole owners, researchers and installers need from a street air quality node, written from their side. They are drawn from the users and stakeholders in AST-PRB-001 (Tables 1 and 2) and are not yet validated with a partner; co-design sessions with the first partner (AST-DEC-001: a city or air agency with a street-level NO2 reference station) will revise them. Product requirements that meet these needs are in AST-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix AST-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Fine particles on my street | See PM2.5 on the street where I live, walk or send my children to school, close enough to a reference to trust | High | Residents and community groups (PRB Table 1) |
| UR-002 | Performance | Traffic NO2 on my street | See NO2, the traffic gas, on the same street, close enough to a reference to trust | High | Residents and community groups; city teams (PRB Table 1) |
| UR-003 | Performance | Rank streets with a stated uncertainty | Tell which streets are worse, and whether a street is above or below the legal limit, and know how sure that is | High | Municipal environment and transport teams (PRB Table 1) |
| UR-004 | Performance | Data often enough for street maps | Readings often enough to see rush hours and daily patterns, and hourly values soon after the hour | High | City teams; researchers (PRB Table 1) |
| UR-005 | Regulatory | A calibration others can check | A stated, repeatable calibration route, linked to each reading, that another group can audit | High | City teams; researchers; reference station operator (PRB Tables 1 and 2) |
| UR-006 | Usability | Raw data to reprocess | Raw sensor signals and the calibration version, so data can be recalculated when a better model or a new collocation exists | Medium | Researchers and data platforms (PRB Table 1) |
| UR-007 | Deployment and assembly | Fits existing poles without harm | Mount on existing street light and signal poles without drilling, without opening the pole and without its power | High | Street furniture owners (PRB Tables 1 and 2) |
| UR-008 | Logistics | Small and light on the pole | A known, small load and wind area that the pole owner can approve | High | Street furniture owners (PRB Tables 1 and 2) |
| UR-009 | Environment and durability | Works outdoors all year | Keep working in sun, rain, heat, cold, humidity, dust and traffic spray at street level | High | All users (PRB Table 1) |
| UR-010 | Maintenance | Quick, simple service at height | Service at the pole in minutes with hand tools, with fiddly work done on the ground | Medium | Installers and service crews; city teams (PRB Table 1) |
| UR-011 | Safety | Nothing personal collected | No images, audio or anything that identifies a person | High | Residents (PRB Table 1) |
| UR-012 | Cost | Affordable for a district network | Low enough in parts and running cost for a community group or city to deploy tens of nodes | High | Community groups; city teams (PRB Table 1) |
| UR-013 | Deployment and assembly | Own power supply | Run without mains, on its own solar and battery supply, through cloudy spells | High | Street furniture owners (PRB Table 2) |
| UR-014 | Usability | Open and buildable | An open, documented design that a school or makerspace can build and repair | Medium | Schools and universities (PRB Table 1) |
| UR-015 | Safety | Safe to install and service | Installable and serviceable without danger from traffic, height, the pole's mains or the battery | High | Installers; pole owner (PRB Tables 1 and 2) |
| UR-016 | Regulatory | Radio within the rules | Radio use within the band rules and the network's fair use where the node is deployed | Medium | Radio regulator and network operator (PRB Table 2) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
