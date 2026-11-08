# Day 10 — Integration & Local Service Latency

20/20 full Day 8 responses + Day 9 explanations/comparisons exact. No new weights or model selection.
JSON responses reproducible; state/input hashes unchanged. Dataset 4,112 x 28; fit 4,108; cutoff 2026-06-12.

Warm-up 3/case; 20 measurements/case; 400 measured calls. One thread, rotating order.
Full recommend_json includes optional comparisons and response validation; excludes startup/CSV/network.
Startup (single observation): 1423.005 ms. Local latency, not cloud performance/scouting quality.

| Scenario | Method | Candidates | Returned | Median ms | p95 ms |
|---|---|---:|---:|---:|---:|
| young_low_budget_striker | cosine | 22 | 5 | 85.663 | 150.281 |
| young_low_budget_striker | weighted_cosine | 22 | 5 | 90.031 | 145.246 |
| young_low_budget_striker | knn_cosine | 22 | 5 | 85.961 | 135.414 |
| young_low_budget_striker | knn_weighted_cosine | 22 | 5 | 95.938 | 122.860 |
| creative_midfielder | cosine | 10 | 5 | 74.381 | 102.959 |
| creative_midfielder | weighted_cosine | 10 | 5 | 80.826 | 103.740 |
| creative_midfielder | knn_cosine | 10 | 5 | 76.931 | 112.386 |
| creative_midfielder | knn_weighted_cosine | 10 | 5 | 85.739 | 108.948 |
| experienced_defender | cosine | 94 | 5 | 125.829 | 156.275 |
| experienced_defender | weighted_cosine | 94 | 5 | 125.921 | 158.670 |
| experienced_defender | knn_cosine | 94 | 5 | 131.079 | 161.772 |
| experienced_defender | knn_weighted_cosine | 94 | 5 | 141.391 | 193.290 |
| budget_goalkeeper | cosine | 47 | 5 | 94.444 | 138.373 |
| budget_goalkeeper | weighted_cosine | 47 | 5 | 95.010 | 149.366 |
| budget_goalkeeper | knn_cosine | 47 | 5 | 101.926 | 163.410 |
| budget_goalkeeper | knn_weighted_cosine | 47 | 5 | 95.522 | 154.879 |
| no_results | cosine | 0 | 0 | 29.309 | 55.904 |
| no_results | weighted_cosine | 0 | 0 | 32.203 | 53.664 |
| no_results | knn_cosine | 0 | 0 | 32.357 | 43.127 |
| no_results | knn_weighted_cosine | 0 | 0 | 24.718 | 51.294 |

## Top 5 weighted cosine

| Scenario | Rank | ID | Player | Score |
|---|---:|---:|---|---:|
| young_low_budget_striker | 1 | 1360186 | Barney Stewart | 0.956332 |
| young_low_budget_striker | 2 | 818445 | Milan Zonneveld | 0.926601 |
| young_low_budget_striker | 3 | 467720 | Youssoufa Moukoko | 0.915929 |
| young_low_budget_striker | 4 | 845568 | Marko Milovanović | 0.890610 |
| young_low_budget_striker | 5 | 670987 | Tawanda Maswanhise | 0.883390 |
| creative_midfielder | 1 | 543302 | Jeppe Erenbjerg | 0.922962 |
| creative_midfielder | 2 | 1175048 | Robin van Cruijsen | 0.915103 |
| creative_midfielder | 3 | 652061 | Adam Karabec | 0.826067 |
| creative_midfielder | 4 | 896234 | Guillermo Balzi | 0.700985 |
| creative_midfielder | 5 | 485672 | Elijah Just | 0.671222 |
| experienced_defender | 1 | 236168 | Brandon Mechele | 0.999090 |
| experienced_defender | 2 | 124502 | Matthias Ginter | 0.995862 |
| experienced_defender | 3 | 244221 | Christian Burgess | 0.977334 |
| experienced_defender | 4 | 187718 | Clinton Mata | 0.969863 |
| experienced_defender | 5 | 173504 | James Tarkowski | 0.960660 |
| budget_goalkeeper | 1 | 464373 | Elías Ólafsson | 0.863745 |
| budget_goalkeeper | 2 | 403564 | Jon McCracken | 0.863250 |
| budget_goalkeeper | 3 | 338665 | Brent Gabriël | 0.860127 |
| budget_goalkeeper | 4 | 337290 | Shamal George | 0.823090 |
| budget_goalkeeper | 5 | 360338 | Marcos Peano | 0.812324 |

No-results: 0 candidates/results/comparisons; constraints remain unchanged.
See evaluation.json for full request/evidence/text/comparisons, hashes and environment; request.schema.json/response.schema.json for contracts.
No API calls/endpoints, no commit/push/deploy. Phase review and limits: [phase_review.md](phase_review.md).
