# BOM notes

Every line in `bom.csv` is priced at quantity 1 (TRL 3). Item numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`. Two prices were checked on 2026-09-25: the Sensirion SPS30 at SparkFun ($60.50, or $57.48 at 25 or more) and the Adafruit SHT45 breakout ($12.50). The NO2 sensor and front-end prices are indicative estimates; the maker's pages could not be fetched. Other lines are indicative prices from a supplier type.

Totals, as printed by `docs/04-calcs/sizing.py` (AST-CAL-001, section I):

| Scope | Cost | Against |
| --- | --- | --- |
| AirStreet sensor head (lines 3 to 11) | $285.00 | $285 `budget_usd` (AST-DDR-002): within, with no margin |
| FieldNode core (lines 1 and 2) | $126.00 | Costed in the FieldNode repo (AST-DDR-001 D1) |
| Whole node | $411.00 | For reference |

The sensor-head total rose from $265 at TRL 2 because the SPS30 costs $60.50 at a checked retail price rather than $45, and the mount now includes V-saddles for 80 to 200 mm poles. Cables were shortened to 0.5 m. Under AST-DDR-002 FieldNode's back plate is left off and line 3 gains two 180 x 25 x 3 mm aluminum adapter bars for the panel bracket feet (about $2), taking the sensor head from $283.00 to $285.00. Line 4, the pod with its sensors, is also the service exchange unit, so a practical fleet needs spare pods; these are not in the per-node BOM. FieldNode's sun shield, required at sites above 45 °C, is costed in FieldNode. CalRig time, reference-station collocation and replacement NO2 sensors (about every 2 years, estimate) are running costs and are not included.
