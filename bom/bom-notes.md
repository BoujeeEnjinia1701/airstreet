# BOM notes

Every line in `bom.csv` is priced at quantity 1 (TRL 3). Item numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`. Two prices were checked on 2026-09-25: the Sensirion SPS30 at SparkFun ($60.50, or $57.48 at 25 or more) and the Adafruit SHT45 breakout ($12.50). The NO2 sensor and front-end prices are indicative estimates; the maker's pages could not be fetched. Other lines are indicative prices from a supplier type.

Totals, as printed by `docs/04-calcs/sizing.py` (AST-CAL-001, section I):

| Scope | Cost | Against |
| --- | --- | --- |
| AirStreet sensor head (lines 3 to 11) | $283.00 | $180 `budget_usd` (over by $103.00); $280 proposed in AST-DDR-001 D1, awaiting Amish (over by $3.00) |
| FieldNode core (lines 1 and 2) | $126.00 | Costed in the FieldNode repo (AST-DDR-001 D1) |
| Whole node | $409.00 | For reference |

The sensor-head total rose from $265 at TRL 2 because the SPS30 costs $60.50 at a checked retail price rather than $45, and the mount now includes V-saddles for 80 to 200 mm poles. Cables were shortened to 0.5 m. CalRig time, reference-station collocation and replacement NO2 sensors (about every 2 years, estimate) are running costs and are not included.
