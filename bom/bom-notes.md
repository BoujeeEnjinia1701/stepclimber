# BOM notes

Prices are indicative estimates in US dollars for one prototype, checked at TRL 3 against the budget; none is a supplier quote. Item numbers 1 to 11 match the exploded view (`media/exploded.png`); items 12 and 13 have no callout. Every line is priced.

| Group | Items | Cost |
| --- | --- | --- |
| Frame, clusters and drive | 1 to 4 | $348 |
| Electronics and controls | 5, 6, 8, 9, 13 | $120 |
| Battery and charger | 7, 12 | $145 |
| Load strap and skids | 10, 11 | $20 |
| **Total** | 1 to 13 | **$633** |

The total is $17 (2.6 %) under the $650 `budget_usd` in `project.yaml` and requirement R12. The budget was $600 until Amish accepted the recommendations on 2026-09-25 (SCM-DDR-002), which revisited it once the rework parts were priced. `docs/04-calcs/sizing.py` recomputes the total from `bom/bom.csv`.

This BOM carries the cluster and drive rework decided on 2026-09-25 (SCM-DDR-002): item 2 moved to 200 mm wheels on 150 mm arms ($65 to $88) and item 3 to a two-stage chain drive with a countershaft ($50 to $80). SCM-CAL-001 v0.2 finds that both now keep clear of stair nosings (R2, R15).

Shipping, taxes and tools are not included.
