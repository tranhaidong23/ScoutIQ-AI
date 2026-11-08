# Day 6 — Weighted cosine: hành vi và độ nhạy

Dataset: 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0; cutoff 2026-06-12; 4112 cầu thủ; fit 4108, loại 4 query.
Tái lập chính xác Day 5 (5 kịch bản); weights=1 khớp toàn bộ thứ hạng/score baseline.
Không có relevance labels: không tính Precision@K/NDCG@K. Ổn định không phải chất lượng scouting.

| Cấu hình | Truy vấn | Overlap@5 | Spearman full common | Eligible | Trả Top K |
|---|---|---:|---:|---:|---:|
| baseline | attack_budget_30m | 1.00 | 1.0000 | 349 | 5 |
| baseline | midfield_budget_15m | 1.00 | 1.0000 | 405 | 5 |
| baseline | defender_context_15m | 1.00 | 1.0000 | 512 | 5 |
| baseline | goalkeeper_context_10m | 1.00 | 1.0000 | 107 | 5 |
| baseline | empty_budget | N/A | N/A | 0 | 0 |
| weighted_default | attack_budget_30m | 0.80 | 0.9969 | 349 | 5 |
| weighted_default | midfield_budget_15m | 1.00 | 0.9937 | 405 | 5 |
| weighted_default | defender_context_15m | 1.00 | 0.9756 | 512 | 5 |
| weighted_default | goalkeeper_context_10m | 0.80 | 0.9867 | 107 | 5 |
| weighted_default | empty_budget | N/A | N/A | 0 | 0 |
| numeric_emphasis | attack_budget_30m | 0.60 | 0.9914 | 349 | 5 |
| numeric_emphasis | midfield_budget_15m | 1.00 | 0.9719 | 405 | 5 |
| numeric_emphasis | defender_context_15m | 1.00 | 0.9518 | 512 | 5 |
| numeric_emphasis | goalkeeper_context_10m | 1.00 | 0.9742 | 107 | 5 |
| numeric_emphasis | empty_budget | N/A | N/A | 0 | 0 |
| categorical_emphasis | attack_budget_30m | 0.80 | 0.9827 | 349 | 5 |
| categorical_emphasis | midfield_budget_15m | 1.00 | 0.9864 | 405 | 5 |
| categorical_emphasis | defender_context_15m | 0.80 | 0.7823 | 512 | 5 |
| categorical_emphasis | goalkeeper_context_10m | 0.80 | 0.9548 | 107 | 5 |
| categorical_emphasis | empty_budget | N/A | N/A | 0 | 0 |
| ablate_categories | attack_budget_30m | 0.00 | 0.9331 | 349 | 5 |
| ablate_categories | midfield_budget_15m | 0.40 | 0.8857 | 405 | 5 |
| ablate_categories | defender_context_15m | 0.20 | 0.7943 | 512 | 5 |
| ablate_categories | goalkeeper_context_10m | 0.40 | 0.9010 | 107 | 5 |
| ablate_categories | empty_budget | N/A | N/A | 0 | 0 |
| ablate_first_numeric | attack_budget_30m | 0.00 | 0.5846 | 349 | 5 |
| ablate_first_numeric | midfield_budget_15m | 0.60 | 0.6647 | 405 | 5 |
| ablate_first_numeric | defender_context_15m | 0.20 | 0.7680 | 512 | 5 |
| ablate_first_numeric | goalkeeper_context_10m | 0.60 | 0.9415 | 107 | 5 |
| ablate_first_numeric | empty_budget | N/A | N/A | 0 | 0 |

Bộ lọc/score/order kiểm trên toàn bộ kết quả; deterministic kiểm lặp và đảo dòng/fit IDs.
Defender/GK chỉ context_profile_only. Metadata CLB chưa xác minh tại cutoff.

## Top 5 weighted_default (tham số và toàn bộ cấu hình trong evaluation.json)

### attack_budget_30m — Harry Kane

Filters: {"position": "Attack", "min_age": 18.0, "max_age": 29.0, "max_budget_eur": 30000000.0, "min_minutes": 1800.0}

| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |
|---|---|---|---|---:|---:|---:|---:|
| 1 | 929090 | Franculino | FC Midtjylland | 21 | 2060 | 22,000,000 | 0.993602 |
| 2 | 424784 | Luis Suárez | Sporting CP | 28 | 3767 | 30,000,000 | 0.981602 |
| 3 | 315867 | Gianluca Scamacca | Atalanta BC | 27 | 2016 | 25,000,000 | 0.960249 |
| 4 | 333647 | Jonathan Burkardt | Eintracht Frankfurt | 25 | 1882 | 30,000,000 | 0.955912 |
| 5 | 331726 | Tammy Abraham | Beşiktaş Jimnastik Kulübü | 28 | 2161 | 18,000,000 | 0.954119 |

### midfield_budget_15m — Hans Vanaken

Filters: {"position": "Midfield", "min_age": 20.0, "max_age": 30.0, "max_budget_eur": 15000000.0, "min_minutes": 1800.0}

| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |
|---|---|---|---|---:|---:|---:|---:|
| 1 | 577455 | Ringo Meerveld | SC Heerenveen | 23 | 2689 | 5,000,000 | 0.999750 |
| 2 | 293200 | Nikola Vlašić | Torino FC | 28 | 3350 | 10,000,000 | 0.998645 |
| 3 | 441216 | Thijs Oosting | PEC Zwolle | 26 | 2834 | 900,000 | 0.992523 |
| 4 | 507341 | Fabian Rieder | Stade Rennais FC | 24 | 2530 | 12,000,000 | 0.992131 |
| 5 | 345577 | Carlo Holse | Samsunspor | 27 | 2640 | 7,000,000 | 0.988221 |

### defender_context_15m — Virgil van Dijk

Filters: {"position": "Defender", "min_age": 22.0, "max_age": 32.0, "max_budget_eur": 15000000.0, "min_minutes": 2000.0}

| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |
|---|---|---|---|---:|---:|---:|---:|
| 1 | 124502 | Matthias Ginter | SC Freiburg | 32 | 4606 | 5,000,000 | 0.995862 |
| 2 | 256448 | Gianluca Mancini | Associazione Sportiva Roma | 30 | 3693 | 15,000,000 | 0.960494 |
| 3 | 243028 | Jan Bednarek | FC Porto | 30 | 3588 | 11,000,000 | 0.953317 |
| 4 | 328784 | Robin Koch | Eintracht Frankfurt | 29 | 3755 | 10,000,000 | 0.948357 |
| 5 | 277384 | Martin Valjent | RCD Mallorca | 30 | 3362 | 3,000,000 | 0.931311 |

### goalkeeper_context_10m — Lukas Hornicek

Filters: {"position": "Goalkeeper", "min_age": 20.0, "max_age": 30.0, "max_budget_eur": 10000000.0, "min_minutes": 1800.0}

| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |
|---|---|---|---|---:|---:|---:|---:|
| 1 | 426849 | Jari De Busser | Go Ahead Eagles | 26 | 4200 | 4,000,000 | 0.977990 |
| 2 | 550829 | Matej Kovar | PSV Eindhoven | 26 | 4050 | 8,000,000 | 0.972834 |
| 3 | 361256 | Berke Özer | LOSC Lille | 26 | 4035 | 10,000,000 | 0.972183 |
| 4 | 370997 | Dominik Kotarski | FC Copenhagen | 26 | 3690 | 5,000,000 | 0.948177 |
| 5 | 592924 | Andreas Jungdal | KVC Westerlo | 24 | 3600 | 3,500,000 | 0.940964 |

### empty_budget — Harry Kane

Filters: {"position": "Attack", "min_age": 18.0, "max_age": 29.0, "max_budget_eur": 0.0, "min_minutes": 1800.0}

| Hạng | ID | Tên | CLB | Tuổi | Phút | EUR | Score |
|---|---|---|---|---:|---:|---:|---:|

