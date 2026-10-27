
# ScoutIQ – Project Development Log

## Day 1 – Data Collection & Inspection

### Objective
Collect and inspect real-world football data.

### Technologies
Python, Requests, Pandas, Git.

### Results
- 50,149 player profiles
- 796 clubs
- 1,894,350 appearances
- 88,958 games
- 656,301 valuation records
- 9,181 players with 2025/26 appearances
- Latest valuation date: 2026-06-12

### Output
- Five raw datasets
- Data quality report
- Season coverage inspection

## Day 2 – Data Cleaning & Integration

### Objective
Transform raw football data into a player-level
dataset for transfer recommendations.

### Technologies
Python, Pandas.

### Methods
1. Data exploration
2. Missing value handling
3. Duplicate removal
4. Season filtering
5. GroupBy aggregation
6. Per-90 feature engineering
7. Relational joins
8. Market valuation selection
9. Candidate filtering

### Results
- Integrated players: 8,322
- Players with >=900 minutes: 4,124
- Final candidates: 4,112
- Unique candidate IDs: 4,112

### Position Distribution
- Defender: 1,523
- Midfield: 1,204
- Attack: 1,059
- Goalkeeper: 326

### Outputs
- scoutiq_players_2025_26.csv
- scoutiq_candidates_2025_26.csv

### Limitations
- Valuations are historical estimates, not transfer fees.
- Latest valuation cutoff: 2026-06-12.
- Available performance metrics are currently limited.
- Current club may differ from the club during 2025/26.
- Candidate threshold of 900 minutes is provisional.

## Day 3 – EDA (bổ sung hồ sơ ngày 2026-10-27)

- **Trạng thái:** Hoàn thành theo xác nhận của người dùng và hồ sơ trong `insights_and_defense.md`; ngày bổ sung này không phải ngày chạy EDA.
- **Code hiện có:** `src/eda/eda_analysis.py`, `src/eda/age_group_analysis.py`.
- **Đầu ra hiện có:** 5 ảnh PNG trong `reports/figures/`, `reports/day3_position_summary.csv`, `reports/day3_age_group_summary.csv`.
- **Đối chiếu:** Bảng vị trí gồm Attack 1.059, Defender 1.523, Goalkeeper 326, Midfield 1.204, tổng 4.112; bảng 6 nhóm tuổi cũng có tổng 4.112. Trung vị theo nhóm tuổi: 10; 5; 3,9; 2; 0,8; 0,4 triệu EUR.
- **Phạm vi xác minh lần này:** Đọc code, bảng tổng hợp, tài liệu và kiểm tra sự hiện diện của ảnh; không chạy lại EDA, không thẩm định lại từng biểu đồ hay mọi thống kê cũ.
- **Kiểm thử:** Chưa có kết quả test tự động được xác minh trong lần thiết lập tài liệu. Script EDA có ghi đầu ra, nên không chạy trong nhiệm vụ chỉ chỉnh tài liệu.
- **Giới hạn:** Dữ liệu lịch sử tới 2026-06-12; thiên lệch do bộ lọc ứng viên; thiếu chỉ số phòng ngự/thủ môn; các đề xuất feature chưa chứng minh cải thiện recommendation.

## Trạng thái các mốc tại 2026-10-27

| Mốc/hạng mục | Trạng thái và căn cứ |
|---|---|
| Day 1 – Thu thập | Hoàn thành theo hồ sơ; 5 file nguồn hiện diện và có commit Day 1 |
| Day 2 – Làm sạch/tích hợp | Hoàn thành theo hồ sơ; code và 2 dataset hiện diện; 4.112 ứng viên được ghi trong báo cáo |
| Day 3 – EDA | Hoàn thành theo hồ sơ/xác nhận; code và đầu ra hiện diện, chưa chạy lại trong lần này |
| Day 4 – Feature Engineering | **Chưa xác nhận hoàn thành; chưa triển khai trong nhiệm vụ này** |
| Recommendation, FastAPI, Streamlit, PostgreSQL, auth, chat | Yêu cầu bắt buộc; chưa xác nhận triển khai |
| Cloud và kiểm thử sản phẩm | Dự kiến; chưa có bằng chứng hoàn thành được kiểm tra |

Các cột per90 trong pipeline Day 2 không đồng nghĩa Day 4 đã hoàn tất. Chỉ cập nhật trạng thái Day 4 sau khi có code, đầu ra và kiểm chứng phù hợp với phạm vi được giao.

## 2026-10-27 – Thiết lập tài liệu quản lý dự án

### Phạm vi và thay đổi

- Tạo `AGENTS.md` tại gốc: nhận diện, đối tượng, yêu cầu sản phẩm, kiến trúc, dữ liệu, nguyên tắc Data Science, bảo mật và quy tắc làm việc.
- Bổ sung nhật ký này để theo dõi tiến độ, code, kiểm tra và mốc Git; giữ nguyên phần Day 1–2.
- Bổ sung `reports/insights_and_defense.md` với quyết định quản lý bằng chứng, hạn chế và các câu hỏi cần kiểm chứng; giữ nguyên các insight cũ.
- Chỉ chỉnh tài liệu. Không thay đổi Python, dataset, cấu hình, biểu đồ; không triển khai Day 4.

### Kiểm tra và bằng chứng

- Đã đọc hai báo cáo cũ; code cleaning, candidate filtering, validation và EDA; hai bảng tổng hợp Day 3; danh sách artefact và dependency.
- Đã dùng `git status --short --branch` và `git log -5` để đối chiếu trạng thái Git trước khi sửa.
- Chưa chạy `pytest`, các script xử lý hoặc EDA trong lần này. `validate_data.py` hiện chủ yếu in thống kê; dòng “VALIDATION COMPLETED!” không đủ chứng minh mọi điều kiện dữ liệu đều đạt.
- Kiểm tra tài liệu cuối phiên được ghi riêng sau khi chạy; không coi kế hoạch kiểm tra là kết quả pass.

### Kết quả kiểm tra tài liệu ngày 2026-10-27

- `git diff --check`: không báo lỗi khoảng trắng trong phần diff được theo dõi.
- Kiểm tra chỉ đọc bằng Python (`-B`, không ghi bytecode): nội dung hai báo cáo trước khi sửa, lấy từ Git index, vẫn là phần đầu nguyên vẹn của bản hiện tại sau chuẩn hóa xuống dòng; cả hai kiểm tra đạt.
- Cả ba file tài liệu đọc được bằng UTF-8 và không có ký tự thay thế lỗi giải mã; kiểm tra đạt.
- `git diff --name-only` chỉ liệt kê hai báo cáo; `git status` ghi nhận thêm `AGENTS.md` là untracked. Hai báo cáo có trạng thái `AM` vì đã staged từ trước và nay có phần bổ sung chưa stage.
- Commit gần nhất vẫn là `86c0360`; 16 mục staged sẵn có được giữ nguyên. Không tạo commit, không stage bổ sung hoặc push.

### Mốc Git tại thời điểm bắt đầu

- Branch: `main`.
- Commit gần nhất: `86c0360` — `Day 1: ScoutIQ data collection and inspection`.
- Có sẵn **16 file mới staged**: 7 Python trong `src/eda/` và `src/preprocessing/`, 2 CSV tổng hợp Day 3, 5 biểu đồ, 2 báo cáo Markdown.
- Trước lần sửa này không thấy thay đổi unstaged hoặc file untracked trong `git status`.
- Đây là snapshot lúc kiểm tra, không phải trạng thái Git cố định. Nội dung bổ sung của các báo cáo cần được phân biệt với phiên bản đã staged trước đó.
- Không chạy `git add`, commit hoặc push trong nhiệm vụ này. Mốc commit tài liệu chỉ là dự kiến cho lúc được phép, chưa có commit mới.

### Bước tiếp theo (chưa thực hiện)

- Khi có nhiệm vụ tiếp theo, xác minh phạm vi và tiêu chí hoàn thành Day 4 trước khi triển khai.
- Kiểm tra missing values, leakage, lựa chọn feature/scaling, thiết kế baseline và cách đánh giá recommendation; ghi kết quả thực nghiệm riêng.
- Theo dõi các yêu cầu ứng dụng trong `AGENTS.md`; không đánh dấu chức năng hoàn thành chỉ vì có thư mục tương ứng.

## Mẫu cập nhật cho các mốc tiếp theo

- **Ngày / mốc / mục tiêu:**
- **Trạng thái:** Dự kiến / Đang thực hiện / Đã hoàn thành có bằng chứng / Chưa xác minh / Bị chặn.
- **Code và artefact:** Đường dẫn đã tạo/sửa, dữ liệu đầu vào và cutoff.
- **Kiểm tra:** Lệnh thực sự đã chạy, kết quả/exit code, phần chưa chạy và lý do.
- **Kết quả và giới hạn:** Số liệu có bằng chứng, lỗi còn lại, giả định chưa kiểm chứng.
- **Git:** Branch, commit thực có, staged/unstaged/untracked; không điền hash cho commit chưa tạo.
- **Bước tiếp theo:** Công việc còn lại và điều kiện hoàn thành.

## 2026-10-27 — Day 4: Feature Engineering

### Phạm vi và trạng thái

- **Đã hoàn thành có bằng chứng** trong phạm vi Day 4 mà người dùng giao ở lượt tiếp theo: kiểm tra dữ liệu, tính đặc trưng, percentile theo vị trí, biểu đồ trước/sau log, xuất CSV, kiểm thử và cập nhật tài liệu.
- Mục này cập nhật các ghi nhận “Day 4 chưa xác nhận hoàn thành” phía trên; giữ nguyên lịch sử nhiệm vụ tài liệu. Chưa xây dựng recommendation, chưa tuyên bố hoàn thành Day 5 hoặc cải thiện mô hình.

### Đầu vào và chất lượng

- `data/processed/scoutiq_candidates_2025_26.csv`: **4.112 dòng × 21 cột**, 4.112 `player_id` duy nhất, 0 ID trùng, 0 infinity trong các cột số, không thiếu các cột bắt buộc cho phép tính Day 4.
- Vị trí: Defender 1.523; Midfield 1.204; Attack 1.059; Goalkeeper 326.
- Missing metadata giữ nguyên: `foot` 24, `height_in_cm` 23, `current_club_name` 16, `club_name_verified` 16. Các số này là số ô theo cột, không phải số cầu thủ khác nhau.
- Phạm vi thực đo: tuổi 17–42; phút 900–4.970; goals 0–61; assists 0–32; định giá 25.000–200.000.000 EUR; ngày định giá 2025-10-01 đến 2026-06-11, cách cutoff 1–254 ngày.
- Cảnh báo: Connor Allan (`player_id=743556`) có `height_in_cm=19`. Khoảng 140–220 cm chỉ là ngưỡng rà soát; không tự sửa thành 190, không loại cầu thủ, không dùng chiều cao trong đặc trưng Day 4. Cần đối chiếu nguồn ở Day 5.
- Sai số tuyệt đối tối đa của per90 đầu vào so với công thức: goals và goal contributions khoảng `2,22e-16`; assists khoảng `9,71e-17`. Kiểm tra dùng `rtol=1e-9`, `atol=1e-12` để chấp nhận sai số số thực.

### Đặc trưng và quyết định

| Cột | Công thức/quy ước | Phạm vi đo được |
|---|---|---|
| `goal_contributions` | goals + assists | 0–69 |
| `goal_contributions_per90` | (goals + assists) × 90 / minutes_played; kiểm tra cột Day 2 trước khi tính lại | 0–1,432196 |
| `market_value_m` | market_value_in_eur / 1.000.000 | 0,025–200 triệu EUR |
| `log1p_market_value_m` | ln(1 + market_value_m) | 0,024693–5,303305 |
| `minutes_reliability` | min(minutes_played / 2700, 1) | 0,333333–1 |
| `goals_per90_position_percentile` | 100 × hạng trung bình / cỡ nhóm vị trí | 1,841360–100 |
| `assists_per90_position_percentile` | Cùng quy ước với assists_per90 | 5,099150–100 |
| `goal_contributions_per90_position_percentile` | Cùng quy ước với goal_contributions_per90 | 0,236072–100 |

- **8 đặc trưng được tạo/kiểm tra, 7 cột mới** vì goal contributions per90 đã có. Xuất **4.112 dòng × 28 cột**, giữ ID/thứ tự và metadata; không loại dòng, không điền missing, không tạo cầu thủ giả.
- Percentile: `rank(method="average", pct=True) * 100` trong từng `position`. Đồng hạng nhận hạng trung bình; miền lý thuyết `(0, 100]`, không bảo đảm min=0 hoặc max=100 nếu có đồng hạng. Không có ngẫu nhiên.
- Tập tham chiếu percentile là toàn bộ ứng viên tại cutoff, trước các bộ lọc người dùng. Không tự tính lại trên shortlist; khi đánh giá theo thời gian/tập holdout, cần thiết kế lại tập tham chiếu để tránh leakage.
- Định giá/log định giá chỉ phục vụ mô tả và xem xét khả thi ngân sách; chưa đưa vào điểm kỹ năng. Reliability chỉ là heuristic, không nhân vào hiệu suất hay dùng làm xác suất trong Day 4.

### Code và artefact

- Tạo `src/features/build_features.py`: hàm thuần `build_features`, kiểm tra input/output, báo cáo JSON, biểu đồ Matplotlib và entrypoint có main guard. Dừng khi dữ liệu bắt buộc không hợp lệ; không âm thầm bỏ dòng/sửa per90 lỗi.
- Tạo `tests/test_features.py`: dùng snapshot thực; lỗi giả lập chỉ trong bản sao bộ nhớ để kiểm tra chặn lỗi, không xuất thành dữ liệu nghiệp vụ.
- Tạo `data/processed/scoutiq_features_2025_26.csv`.
- Tạo `reports/day4_feature_quality.json`: schema đầy đủ, missing, infinity, numeric ranges, kiểm tra per90, thống kê, cảnh báo, phiên bản môi trường và hash input/output.
- Tạo `reports/figures/day4_market_value_transformation.png`: hai histogram 40 bins, giữ toàn bộ quan sát, có median, skewness, đơn vị và cutoff. Đã mở ảnh kiểm tra nhãn và bố cục.
- Bổ sung `AGENTS.md` và hai báo cáo để phản ánh trạng thái mới; giữ nguyên nội dung lịch sử.

### Lệnh và kết quả thực chạy

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_features.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B src/features/build_features.py
```

- Môi trường: Python 3.13.7, pandas 3.0.6, NumPy 2.5.4, Matplotlib 3.11.2 trong `.venv`; không cài thêm dependency.
- Test sau cập nhật kiểm tra percentile: **23 passed in 1.98s**, exit code 0. Bao phủ công thức, giới hạn, đồng hạng và nhóm vị trí, đảo thứ tự dòng, bảo toàn metadata/input, CSV round-trip; chặn missing bắt buộc, infinity, ID trùng, schema thiếu, tập rỗng, phút không hợp lệ, số đếm âm/lẻ, định giá không hợp lệ, cutoff sai, per90 sai và output bị sửa sai.
- Pipeline: exit code 0; input `(4112, 21)`, output `(4112, 28)`; không missing hoặc infinity trong 8 đặc trưng, không ID trùng, kiểm tra công thức/phạm vi đạt. Metadata thiếu vẫn được báo riêng, không tuyên bố toàn bộ dataset sạch tuyệt đối.
- Đọc lại CSV xuất ra, kiểm tra đặc trưng và so sánh với DataFrame trước khi ghi: đạt trong tolerance số thực.
- Đối chiếu SHA-256 trước/sau: **5 file raw + 2 CSV đầu vào hiện có không đổi**; `.git/index` không đổi. Hash tập ứng viên: `5480a88b2fb13047f65364db1795ee8f1871108de7de998f2fdc97cc1571edc9`.
- `git diff --check` không báo lỗi tại lần kiểm tra sau triển khai.

### Kết quả Data Science và giới hạn

- Skewness định giá giảm **4,222779 → 0,632063** sau `log1p(market_value_m)`. Trung vị 3 triệu EUR tương ứng `ln(4)=1,386294`; max 200 triệu tương ứng 5,303305. Phân phối vẫn lệch phải, chưa chứng minh chuẩn hoặc cải thiện recommendation.
- Reliability median **0,734444**; **939** cầu thủ đạt trần 1 (từ 2.700 phút). Không phân biệt thêm các cầu thủ đã vượt trần.
- **323/326 thủ môn** không ghi bàn nhưng có percentile goals/90 **49,693252** do đồng hạng; minh họa vì sao percentile không đồng nghĩa chất lượng thủ môn.
- `goal_contributions_per90 = goals_per90 + assists_per90`: nếu dùng cả ba cùng trọng số mặc định có thể đếm lặp ảnh hưởng tấn công. Chưa chọn vector cuối cùng hoặc trọng số mô hình.
- Chưa xác minh đầy đủ thời điểm metadata CLB; kiểm tra ngày định giá trên snapshot không thay thế kiểm toán leakage toàn bộ nguồn.

### Git và Day 5

- Nhánh vẫn `main`; không `git add`, commit, push hoặc deploy. Các staged changes có trước được giữ nguyên.
- CSV mới nằm trong `data/processed/`, đang bị ignore theo `.gitignore` hiện có. File có trên đĩa; chưa thay đổi chính sách quản lý dữ liệu hoặc force-add vào Git.
- Day 5: xác minh chiều cao bất thường/missing metadata; lựa chọn feature theo nhiệm vụ và vị trí; không mặc định dùng định giá như kỹ năng; tránh lặp goals/assists/goal contributions; thử scaling/trọng số và baseline; đánh giá top-K, bộ lọc, độ nhạy reliability và ngưỡng ứng viên; xử lý giới hạn dữ liệu phòng ngự/thủ môn và thiết kế đánh giá tránh leakage.
