# BOM notes

Prices are indicative estimates in US dollars for one prototype, checked at TRL 3 against the budget; none is a supplier quote. Item numbers 1 to 11 match the exploded view (`media/exploded.png`); items 12 and 13 have no callout. Every line is priced.

| Group | Items | Cost |
| --- | --- | --- |
| Frame, clusters and drive | 1 to 4 | $295 |
| Electronics and controls | 5, 6, 8, 9, 13 | $120 |
| Battery and charger | 7, 12 | $145 |
| Load strap and skids | 10, 11 | $20 |
| **Total** | 1 to 13 | **$580** |

The total is $20 (3.3 %) under the $600 `budget_usd` in `project.yaml` and requirement R12; Amish kept the budget at $600 on 2026-09-25 (SCM-DDR-001). `docs/04-calcs/sizing.py` recomputes the total from `bom/bom.csv`.

This BOM is the baseline design. SCM-CAL-001 finds that the item 3 sprocket and guard strike stair nosings (R15) and the item 2 arms catch large nosing overhangs (R2). The cluster and drive rework proposed in SCM-DDR-001 (item 11: 200 mm wheels, 150 mm arms, a second chain stage) would add roughly $35 and 1.5 kg (rough estimate) and take the total past $600; it is proposed, awaiting Amish, and is not in this BOM.

Shipping, taxes and tools are not included.
