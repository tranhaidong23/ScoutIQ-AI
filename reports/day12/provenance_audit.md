# Day 12 — Provenance, lineage, missing và coverage

Kiểm tra mới 2026-11-03, bằng chứng [audit.json](audit.json), [feature_lineage.csv](feature_lineage.csv), [coverage_analysis.csv](coverage_analysis.csv), [eligibility_exclusions.csv](eligibility_exclusions.csv). Code đọc dữ liệu tại [integrity.py](../../src/evaluation/integrity.py), [runner](../../src/evaluation/run_day12.py); kiểm raw thời gian/aggregate dùng lại [audit.py Day 11](../../src/evaluation/audit.py) và **đã chạy lại**, khớp toàn bộ dict bằng chứng Day 11.

## Snapshot và nguồn

- Transfermarkt, season 2025 trong raw tương ứng 2025/26, cutoff 2026-06-12. Features **4.112 × 28**, SHA-256 `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`.
- 5 raw tables: players, clubs, games, appearances, player_valuations; 3 processed: integrated players, candidates, features. SHA-256 8 inputs và hash code/bằng chứng Day 11 lưu trong audit.json; trước chạy kiểm hash khớp bản Day 11, sau phiên kiểm không bị sửa.
- [Downloader](../../src/collection/download_data.py) dùng URL R2 mutable và skip file đã có. Hash nội bộ chứng minh cùng file snapshot, **không** chứng minh authenticity nguồn, completeness, publication time hoặc tái tải y hệt từ URL hiện tại. Không tải lại trong Day 12.
- Raw/processed ngoài Git, cần bàn giao riêng theo manifest. Source chưa commit và requirements chưa full lock; chưa nghiệm thu cài sạch/máy mới. Không upload dữ liệu lớn/secrets.

## Lineage của 28 cột

CSV lineage có một hàng cho **mỗi cột**, gồm nguồn, phép biến đổi, đơn vị, vai trò trong engine và tính khả dụng tại cutoff. Unknown schema mới khiến generator lỗi, không tự gán lineage phỏng đoán.

- `matches/minutes/goals/assists`: game season/cutoff → appearances hợp lệ/dedup → group player; per90 từ số đếm/phút. Cutoff trên event date chưa chứng minh dữ liệu được công bố tại cutoff.
- Metadata và DOB lấy players snapshot; CLB lookup thêm clubs. `club_name_verified` chỉ kiểm liên kết tên, không phải verification lịch sử. Tuổi dùng phép xấp xỉ cũ; calendar value chỉ nằm trong report proposed.
- Valuation lấy latest positive ≤cutoff; freshness 0–365 ngày. EUR khác million EUR, giá trị thị trường không phải phí mua/kỹ năng. Log/value không nằm trong skill vector.
- Contribution/minutes reliability/global position percentiles có lineage nhưng không dùng trong similarity hiện hành, tránh đếm trùng hoặc đưa toàn catalogue vào fit. g90/a90 vẫn có thể tương quan; không tuyên bố mọi tín hiệu độc lập.

## Eligibility: phân biệt thất bại độc lập và loại tuần tự

Universe đầu vào ở đây là **8.322 integrated**, không phải toàn 50.149 raw players. Exclusion CSV có đủ 8.322 ID, flags và chuỗi lý do; không bỏ những người chưa bị loại để mất mẫu số.

| Quy tắc gốc | Fail độc lập trên 8.322 | Trước → sau theo thứ tự audit | Loại thêm |
|---|---:|---|---:|
| minutes ≥900 | 4.198 | 8.322 → 4.124 | 4.198 |
| market value >0 | 0 | 4.124 → 4.124 | 0 |
| valuation age 0–365 | 226 | 4.124 → 4.112 | 12 |
| position không null/rỗng | 0 | 4.112 → 4.112 | 0 |

IDs còn lại khớp chính xác tập features. Không cộng fail độc lập thành tổng loại vì các điều kiện chồng lấn. Integrated đã bị chọn bởi nguồn trận/metadata/valuation trước đó; không coi zero value failures là raw không có giá trị thiếu/không dương. Có 1 integrated position là chuỗi literal `Missing`: predicate cũ nonempty không coi chuỗi này là null, nhưng người này không vào candidates do các điều kiện khác. Day 12 ghi giới hạn semantic, không sửa eligibility; 4.112 candidates vẫn thuộc 4 nhóm được engine hỗ trợ.

## Coverage và missing

| Vị trí | Integrated | Candidates | Tỷ lệ giữ |
|---|---:|---:|---:|
| Attack | 2.457 | 1.059 | 43,10% |
| Midfield | 2.423 | 1.204 | 49,69% |
| Defender | 2.740 | 1.523 | 55,58% |
| Goalkeeper | 701 | 326 | 46,50% |

| Nhóm tuổi snapshot | Integrated | Candidates | Tỷ lệ giữ |
|---|---:|---:|---:|
| 0–16 | 7 | 0 | 0% |
| 17–20 | 906 | 217 | 23,95% |
| 21–24 | 2.512 | 1.215 | 48,37% |
| 25–28 | 2.566 | 1.430 | 55,73% |
| 29–32 | 1.547 | 858 | 55,46% |
| 33–36 | 642 | 337 | 52,49% |
| 37+ | 142 | 55 | 38,73% |

Nhóm tuổi dùng **tuổi snapshot chưa sửa**, biên số nguyên ghi rõ trong code. Đây là retention do toàn pipeline hiện hành, không phải ảnh hưởng nhân quả của riêng ngưỡng phút. Ngưỡng 900 phút chọn người đã có cơ hội thi đấu; mẫu không đại diện dự bị/tài năng mới/chấn thương hay toàn thị trường.

Coverage CSV còn có `current_club_league_proxy`: ánh xạ từ raw `current_club_domestic_competition_id`, có bucket MISSING; **không gọi đó là giải thi đấu đã xác minh tại cutoff**. Aggregate gồm league/cup/đội tuyển và chưa strength/opponent normalization. So sánh tỷ trọng trước/sau là mô tả, không metric fairness hoặc bằng chứng cầu thủ một giải tốt hơn.

Missing trên 4.112: foot **24**, height **23**, current_club_name **16**, club_name_verified **16**; các cột khác không missing, numeric infinity **0**. `height_in_cm=19` ở ID **743556** tiếp tục bị gắn cờ review theo khoảng 100–230 cm, không sửa/impute và không dùng trong engine. Khoảng này là heuristic kiểm tra, không bằng chứng DOB/chiều cao thực của người đó.

Kết luận provenance: lineage và identity snapshot có thể truy vết; nguồn ngoài, độ đầy đủ và historical availability còn chưa xác minh. Chưa đủ để tuyên bố no-leakage hoặc chất lượng recommendation thật.
