# BOM notes

Every line in `bom.csv` is priced at quantity 1 (TRL 3). Item numbers match the callouts in `media/exploded.png` and the part keys in `cad/src/model.py`. Two prices were checked on 2026-09-25: the Sensirion SPS30 at SparkFun ($60.50, or $57.48 at 25 or more) and the Adafruit SHT45 breakout ($12.50). The NO2 sensor and front-end prices are indicative estimates; the maker's pages could not be fetched. Other lines are indicative prices from a supplier type.

Totals, as printed by `docs/04-calcs/sizing.py` (AST-CAL-001 v0.6, section I), updated 2026-10-02:

| Scope | Cost | Against |
| --- | --- | --- |
| AirStreet sensor head (lines 3 to 11) | $302.50 | $285 value-engineering target (`budget_usd`): $17.50 over |
| FieldNode core (lines 1 and 2) | $131.00 | Costed in the FieldNode repo (AST-DDR-001 D1): FieldNode's $139.00 less its unused $8.00 pole mounting kit |
| Whole node | $433.50 | For reference |

Value-engineering target: USD 285. Estimated cost of the constructable design: USD 302.50 (USD 17.50 over the target).

How the sensor head got here: $265 at TRL 2; $283.00 at TRL 3 (checked SPS30 price, V-saddles for 80 to 200 mm poles, shorter cables); $285.00 under AST-DDR-002 (adapter bars for the panel bracket); $303.00 when the design was made constructable (AST-DDR-003: adapter plates and cross arm, band stock, spacers, probe tube and lead, inserts, glands, probe socket, terminal block and fixings); and $302.50 on 2026-10-02 when the four lightening steps of AST-DDR-003, A1 were carried in. In that last step line 3 went from $21.00 to $21.50 (the 40 x 4 mm rail saves about $0.50 of metal, priced by weight, and the saddles are repriced at about $3.00 of filament at 40 % infill, the $1.50 used before being low; the plate windows save weight, not purchase cost) and line 8 from $10.00 to $9.00 (the 1.5 mm shield plates use about 0.04 kg less ASA at about $30/kg).

Mass, as printed by `sizing.py` [F4], [F5], [F8]: 3.62 kg on the pole and 3.78 kg with FieldNode's sun shield, against the R13 limit of 4.0 kg including the shield (it was 3.84 kg and 4.00 kg before the lightening). The lightened parts weigh: rail 0.19 kg (was 0.24), adapter plates 0.21 kg (was 0.27), V-saddles 0.10 kg at 40 % infill (0.18 kg solid), shield plates, cap and spacers 0.23 kg (was 0.27).

Line 4, the pod with its sensors, is also the service exchange unit, so a practical fleet needs spare pods; these are not in the per-node BOM. FieldNode's sun shield, required at sites above 45 °C, is costed in FieldNode. CalRig time, reference-station collocation and replacement NO2 sensors (about every 2 years, estimate) are running costs and are not included. The radio band and FieldNode antenna are set when the first partner is agreed (US915 in North America, EU868 in Europe; decision of 2026-10-02); the BOM does not yet name one.
