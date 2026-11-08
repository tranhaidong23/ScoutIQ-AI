# Day 7 — KNN cosine benchmark và robustness

KNN dùng cùng representation, reference và bộ lọc Day 5/6. Không mặc định tốt hơn.
Warm-up 5, measured 50 lần/method/query, thread limit=1, Top K=5.
Đo full recommend; gồm KNN.fit trên pool đã lọc, không gồm fit scaler/đọc CSV/ghi báo cáo.
Kết quả timing thuộc máy/phiên này; không là cloud SLA hoặc chất lượng tuyển trạch.

| Representation | Scenario | Method | Median ms | p95 ms |
|---|---|---|---:|---:|
| day5 | attack_budget_30m | direct | 2.4655 | 3.1309 |
| day5 | attack_budget_30m | knn | 3.4736 | 4.0315 |
| day5 | midfield_budget_15m | direct | 4.7963 | 6.8239 |
| day5 | midfield_budget_15m | knn | 6.6505 | 9.7153 |
| day5 | defender_context_15m | direct | 5.1964 | 7.9665 |
| day5 | defender_context_15m | knn | 6.9324 | 10.8385 |
| day5 | goalkeeper_context_10m | direct | 4.4798 | 6.3280 |
| day5 | goalkeeper_context_10m | knn | 6.1544 | 8.4616 |
| day5 | empty_budget | direct | 2.6027 | 3.6783 |
| day5 | empty_budget | knn | 2.6656 | 3.3019 |
| day6_default | attack_budget_30m | direct | 4.8887 | 7.1538 |
| day6_default | attack_budget_30m | knn | 6.6425 | 10.1160 |
| day6_default | midfield_budget_15m | direct | 4.8884 | 6.9730 |
| day6_default | midfield_budget_15m | knn | 6.6997 | 9.8455 |
| day6_default | defender_context_15m | direct | 5.3778 | 7.9683 |
| day6_default | defender_context_15m | knn | 7.1088 | 10.2431 |
| day6_default | goalkeeper_context_10m | direct | 4.5679 | 6.7826 |
| day6_default | goalkeeper_context_10m | knn | 6.1675 | 9.3328 |
| day6_default | empty_budget | direct | 1.7807 | 2.7137 |
| day6_default | empty_budget | knn | 1.8155 | 2.8595 |

## Parity và giới hạn

10 cặp full ranking đạt parity/filter/score/reproducibility; 50 kiểm tra K=1/3/5/50/10000 đạt.
Nonempty overlap@5=1; empty=N/A. Dùng score tolerance 1e-11, tie round12 rồi ID tăng dần.
Không tính Precision/NDCG khi thiếu labels. Defender/GK chỉ hồ sơ bối cảnh.
Top 5 đầy đủ tên/CLB/giá/score/evidence trong evaluation.json; toàn ranking trong rankings.csv.
Không thay baseline, không đổi dữ liệu. Day 8 dự kiến hoàn thiện bộ lọc hiệu suất và điều kiện biên.
