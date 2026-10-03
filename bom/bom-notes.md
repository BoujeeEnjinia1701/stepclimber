# BOM notes

Prices are indicative estimates in US dollars for one prototype, checked at TRL 3 against the budget; none is a supplier quote. Item numbers 1 to 11 match the exploded view (`media/exploded.png`); items 12 and 13 have no callout. Every line is priced.

| Group | Items | Cost |
| --- | --- | --- |
| Frame, clusters and drive | 1 to 4 | $404 |
| Electronics and controls | 5, 6, 8, 9, 13 | $120 |
| Battery and charger | 7, 12 | $145 |
| Load strap and skids | 10, 11 | $20 |
| Parts added for construction (SCM-DDR-003) | 14 to 17 | $99 |
| **Total** | 1 to 17 | **$788** |

Value-engineering target: USD 650 (`budget_usd` in `project.yaml`, unchanged). Estimated cost of the constructable design: USD 788 (USD 138 over the target). `docs/04-calcs/sizing.py` recomputes the total from `bom/bom.csv`.

Line 3 changed on 2026-10-02 (SCM-DEC-001, item 1): the 25 mm cluster shaft is 4140 quenched and tempered alloy steel with a mill certificate instead of 1018 bright bar, which adds about USD 12 (USD 96 to USD 108). The basis is about USD 22 per metre for 25 mm 4140 bar, 0.5 m needed, with the keyway milled, against about USD 8 for 1018 bright bar. Mass is unchanged (both steels are 7,850 kg/m3). The price is indicative; the first supplier quote replaces it.

Items 1 to 11 match the exploded view (`media/exploded.png`); items 12 to 17 have no callout. Every line is priced. Items 14 to 17 were added to make the design buildable (SCM-DDR-003).

Shipping, taxes and tools are not included.
