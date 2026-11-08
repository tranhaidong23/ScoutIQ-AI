

<!-- CHECKPOINT_20261108_START -->
## Bàn giao hiện hành — 2026-11-08

Nguồn tiếp tục cho Claude Code: [bàn giao tổng hợp Day1–13](../docs/CLAUDE_HANDOFF_2026-11-08.md). Mục này ưu tiên về trạng thái Git/bàn giao; các mục bên dưới là lịch sử được giữ nguyên. Người dùng đã yêu cầu commit/push checkpoint Day5–13 hôm nay; quyền này không áp dụng tự động cho Day14/deploy.

Day13 hoàn thành công cụ/tài liệu; chưa assessor/nhãn thật,32 pending, final relevance/ agreement bị chặn. Correction giữ PROPOSED, không đổi ranking/dataset. Latest full suite742 passed ngày06/11; checkpoint08/11 đối chiếu hash bản đã test, không tuyên bố chạy suite mới. Day14 FastAPI+Neon chưa triển khai; MVP không login/signup, Gemini chỉ hiểu yêu cầu/giải thích.

Tài liệu bàn giao ghi lịch sử/quyết định/roadmap,8 dataset và backup riêng,cách setup/kiểm hash/tests,limitations và prompt tiếp tục. `.gitattributes` giữ bytes để source/artifact hashes không đổi khi clone; docs/environment-checkpoint.json ghi môi trường quan sát mới, không phải lock. Commit chứa tài liệu bàn giao là checkpoint; tra hash và kiểm remote bằng lệnh trong tài liệu, không dùng các đoạn HEAD c4d638c/chưa commit lịch sử làm trạng thái hiện hành.
<!-- CHECKPOINT_20261108_END -->


<!-- DAY13_CURRENT_START -->
## Day 13 — 2026-11-06: pilot intake và review

**Hoàn thành phần công cụ local; pilot với người thật và final evaluation vẫn BLOCKED.** Người dùng xác nhận chưa có assessor/nhãn. Snapshot thật giữ nguyên: 32 pending, 0 graded, 0 assessor; relevance cuối null, agreement bị chặn. Correction Day12 vẫn PROPOSED/applied=false/approval=null; không đổi dữ liệu, ranking, scaler, eligibility hoặc API.

Thêm src/evaluation/review.py, run_day13.py và tests/test_day13_review.py. Runner kiểm hashes source/input frozen, tái dựng manifest seed12, nhập nhiều CSV + registry tường minh, từ chối trùng/version sai/SYNTHETIC; báo coverage missing/pending/abstain/uncertainty và queue bất đồng OPEN, không adjudicate. Output mới, không overwrite; giữ bản chấm thật ngoài repo và không sao chép free-text notes/evidence vào output. Registry cần review con người, không tự chứng minh độc lập.

Bằng chứng: reports/day13/summary.md, review.json, review_queue.json, validation.json; quy trình pilot_review_workflow.md, quyết định correction_decision.md, final_evaluation_plan.md và phase_review.md. Tests: **742 passed, 0 failed (762.99s; 717 cũ +25 mới)**; xem reports/day13/validation.json. Không có dependency mới.

Day14 dự kiến phần kỹ thuật FastAPI + Neon khi được giao; MVP anonymous không login/signup, Gemini phase sau chỉ hiểu yêu cầu/giải thích. Chưa production hoặc chất lượng scouting được nghiệm thu. Giữ blockers labels/temporal và correction deferred; không bịa nhãn để mở gate. Day1–12 bên dưới là lịch sử được bảo toàn.

Git main/HEAD c4d638c; chưa stage/commit/push. Checkpoint trước đã fetch và kiểm backup 8 datasets ở ngoài repo; archive trên cùng ổ C chưa là backup ngoài máy. Day13 thêm file nên danh sách stage 120 file trước đây cần rà lại khi làm Git.
<!-- DAY13_CURRENT_END -->

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

## 2026-10-27 — Lộ trình chính thức 31 ngày làm việc

### Hiệu lực và tiến độ hiện tại

- Theo yêu cầu mới của người dùng, lộ trình chính thức có **31 ngày làm việc**. **Day 1–4 đã hoàn thành; Day 5–31 chưa triển khai, trạng thái Dự kiến.** Mục này cập nhật các ghi nhận trạng thái và phân bổ công việc cũ; các phần lịch sử phía trên vẫn được giữ nguyên.
- Ngày làm việc là thứ tự thực hiện, không quy đổi sang ngày lịch khi chưa có lịch bắt đầu được thống nhất. Đã hoàn thành 4 mốc ngày, còn 27 mốc ngày; không suy ra phần trăm hoàn thiện sản phẩm từ số ngày.
- Giữ nguyên toàn bộ mục tiêu, đối tượng và yêu cầu sản phẩm trong `AGENTS.md`: FastAPI, Streamlit, PostgreSQL, authentication, privacy, bộ lọc, top 3–5, so sánh bằng biểu đồ, OpenAI scouting chat dựa trên dữ liệu thật, cloud và kiểm thử.
- Dữ liệu vẫn là Transfermarkt 2025/26, cutoff 2026-06-12; không tạo dữ liệu bóng đá giả, không suy luận nhân quả từ tương quan, không coi market value là phí chuyển nhượng hoặc điểm kỹ năng.
- Đây là **cập nhật kế hoạch**, không phải báo cáo kết quả thực hiện Day 5 trở đi. Mọi đầu ra/test/triển khai trong các bảng dưới đây đều là dự kiến.

### Nền tảng đã hoàn thành — Day 1–4

| Ngày | Công việc | Bằng chứng đã ghi nhận |
|---|---|---|
| Day 1 | Thu thập và kiểm tra 5 bảng nguồn | Code collection, báo cáo chất lượng, commit `86c0360` |
| Day 2 | Làm sạch, tích hợp và lọc ứng viên | 8.322 cầu thủ tích hợp, 4.112 ứng viên; code preprocessing |
| Day 3 | EDA và phân tích vị trí/nhóm tuổi | 5 biểu đồ, 2 bảng tổng hợp; Day 2–3 được lưu riêng trong commit `c4d638c` |
| Day 4 | Feature Engineering | 4.112 dòng × 28 cột, 8 đặc trưng tạo/kiểm tra, 23 test đạt ở lần thực hiện Day 4; commit `266f90f` |

Kết quả test ở đây là bằng chứng lịch sử đã có, không phải test mới chạy khi lập lộ trình.

### Day 5–10 — Recommendation Engine

| Ngày | Công việc chi tiết dự kiến | Đầu ra và điều kiện nghiệm thu dự kiến |
|---|---|---|
| Day 5 | Định nghĩa tình huống tuyển trạch, cấu trúc yêu cầu tìm kiếm và vector đặc trưng ban đầu. Rà missing metadata/chiều cao 19 cm, quyết định cách loại metadata chưa xác minh khỏi vector. Tách ràng buộc ngân sách/tuổi khỏi hiệu suất; ghi cách xử lý phụ thuộc giữa goals, assists và contributions. | Đặc tả engine, từ điển feature và baseline đơn giản có thể chạy trên dữ liệu thật; test đầu vào/phép lọc cơ bản. Không tự sửa chiều cao hoặc tạo ground truth. **Mốc commit/push Day 5.** |
| Day 6 | Xây pipeline chuẩn hóa và content-based similarity; triển khai weighted cosine similarity với trọng số cấu hình rõ ràng. Xử lý vector 0, missing bắt buộc và tham chiếu percentile. | Module tính tương đồng và cấu hình; kết quả hữu hạn, lặp lại được, xử lý đầu vào không hợp lệ; scaler/tham chiếu chỉ dùng dữ liệu thuộc phạm vi cho phép. Chưa kết luận cấu hình tốt nhất. |
| Day 7 | Xây phương án KNN để đối chiếu với weighted cosine trên cùng bộ tình huống và feature. Định nghĩa metric khoảng cách, số láng giềng, xử lý hòa điểm và loại chính cầu thủ tham chiếu nếu có. | KNN chạy được, không trùng ID trong kết quả; đối chiếu top-K và thời gian với baseline, ghi cấu hình thực chạy; chưa chọn theo cảm tính hoặc định giá. |
| Day 8 | Hoàn thiện bộ lọc vị trí, min/max tuổi, ngân sách EUR và ngưỡng hiệu suất; kết hợp lọc với ranking. Xử lý điều kiện biên, không có hoặc thiếu ứng viên. | Top 3–5 tuân thủ mọi ràng buộc; trả ít hơn khi thiếu, không tự nới bộ lọc; test ngân sách/tuổi sát biên, filter rỗng và input sai. |
| Day 9 | Bổ sung lý do gợi ý dựa trên feature, dữ liệu đầu ra phục vụ so sánh và giới hạn theo vị trí. Kiểm tra độ ổn định với đồng hạng, thay đổi thứ tự dòng và các nhóm cầu thủ ít phân biệt bằng chỉ số tấn công. | Kết quả có player ID, số liệu gốc, điểm tương đồng, điều kiện lọc/cutoff và lý do có thể truy vết. Dữ liệu so sánh thống nhất đơn vị; biểu đồ giao diện triển khai ở Day 21. |
| Day 10 | Tích hợp engine thành dịch vụ Python dùng lại được cho API; ổn định cấu hình, tài liệu sử dụng và test hồi quy theo các tình huống đã định nghĩa. Chốt phiên bản engine ứng viên để đánh giá chính thức. | Pipeline tìm kiếm → lọc → ranking → giải thích chạy cục bộ trên dữ liệu thật; test liên quan đạt, giới hạn được ghi nhận. **Mốc commit/push Day 10**; chưa tuyên bố model đã được đánh giá toàn diện. |

### Day 11–16 — Model Evaluation, PostgreSQL và FastAPI

| Ngày | Công việc chi tiết dự kiến | Đầu ra và điều kiện nghiệm thu dự kiến |
|---|---|---|
| Day 11 | Định nghĩa bộ tình huống đánh giá, rubric chuyên môn và baseline trước khi chọn cấu hình. Đánh giá tính hợp lệ bộ lọc, độ phủ, độ ổn định, thời gian trả kết quả; rà leakage và thiết kế split theo dữ liệu thực có. | Protocol đánh giá và bộ tình huống có nguồn. Chỉ dùng Precision@K/NDCG nếu có nhãn phù hợp; thiếu nhãn phải nêu rõ, không bịa relevance hoặc dùng giá trị thị trường làm ground truth chất lượng. |
| Day 12 | Chạy đánh giá so sánh weighted cosine/KNN và baseline; ablation feature phụ thuộc; phân tích trọng số, scaling, mốc reliability và nhóm vị trí. Chọn cấu hình bằng bằng chứng, ghi thất bại và giới hạn. | Báo cáo kết quả có cấu hình, lệnh, dữ liệu/cutoff và metric thực đo; tách tuning khỏi đánh giá khi thiết kế có holdout. Không tuyên bố đủ khả năng đánh giá thủ môn/hậu vệ nếu thiếu chỉ số. |
| Day 13 | Thiết kế PostgreSQL: `users`, `search_history`, `chat_sessions`, `chat_messages`, `recommendation_results`; xác định khóa ngoại, chủ sở hữu, timestamp, phiên bản engine và thông tin tái lập gợi ý. Thiết kế mật khẩu băm và vòng đời phiên trước khi viết auth. | ERD/schema, data dictionary, migration đầu tiên và quy tắc lưu/xóa dữ liệu; không lưu mật khẩu rõ. Mọi bản ghi riêng tư có đường liên kết tới user; message thuộc session có chủ sở hữu. |
| Day 14 | Triển khai lớp truy cập PostgreSQL cục bộ và migration. Lưu/đọc lịch sử tìm kiếm, phiên/tin nhắn chat và kết quả gợi ý; xử lý transaction, rollback và truy vấn theo user. | Test persistence, khóa ngoại, transaction và truy vấn theo chủ sở hữu trên DB kiểm thử riêng. Không dùng dữ liệu tài khoản thật làm fixture hoặc ghi secrets vào log/repo. Auth đầy đủ tiếp tục ở Day 17–18. |
| Day 15 | Xây FastAPI với schema request/response, validation, health check, endpoint tìm kiếm/recommendation/comparison; nối engine và PostgreSQL, chuẩn hóa lỗi/cấu hình môi trường. | API chạy cục bộ, hợp đồng OpenAPI và test route chính; response không lộ secrets/thông tin nội bộ. **Mốc commit/push Day 15.** Chưa công khai endpoint dữ liệu riêng. |
| Day 16 | Kiểm thử tích hợp FastAPI ↔ PostgreSQL ↔ engine: lưu/truy xuất kết quả, dữ liệu không hợp lệ, thiếu ứng viên, lỗi DB và tính nhất quán response. Rà điểm cần gắn authentication. | Bằng chứng integration tests và hướng dẫn chạy local; dịch vụ ứng viên cho UI/auth. Các đường truy cập dữ liệu riêng phải được bảo vệ trước khi triển khai công khai ở giai đoạn sau. |

### Day 17–23 — Authentication, Privacy, Streamlit và OpenAI API

| Ngày | Công việc chi tiết dự kiến | Đầu ra và điều kiện nghiệm thu dự kiến |
|---|---|---|
| Day 17 | Triển khai đăng ký, đăng nhập, đăng xuất; băm mật khẩu, xác thực input, hết hạn và vô hiệu hóa phiên/token theo thiết kế. Gắn danh tính đã xác thực vào request backend. | Test tài khoản trùng, sai mật khẩu, truy cập khi chưa đăng nhập, hết hạn và logout. Mật khẩu/token không xuất hiện trong response/log; không chỉ xóa trạng thái UI để giả lập logout. |
| Day 18 | Áp quyền sở hữu cho history, chat sessions/messages, recommendation results ở backend; rà endpoint đọc/ghi và chống truy cập chéo user. | Test hai tài khoản kiểm thử tách biệt cho cả đọc/ghi, thay ID và session; không rò dữ liệu giữa user. Không tin `user_id` do client tự gửi để quyết định quyền. |
| Day 19 | Xây khung Streamlit, điều hướng đăng ký/đăng nhập/đăng xuất, quản lý trạng thái phiên và API client. Hiển thị lỗi/kết quả theo quyền người dùng. | Luồng auth qua UI và backend hoạt động cục bộ; xóa trạng thái/cache riêng khi logout, không chia sẻ dữ liệu riêng qua cache giữa phiên. |
| Day 20 | Tích hợp UI tìm kiếm vị trí/tuổi/ngân sách/hiệu suất, top 3–5 và lịch sử riêng. Hiển thị đơn vị EUR, cutoff, lý do gợi ý và trạng thái không có kết quả. | Luồng đăng nhập → tìm kiếm → gợi ý → xem lại lịch sử có bằng chứng kiểm tra; các bộ lọc giữ đúng nghĩa. **Mốc commit/push Day 20.** |
| Day 21 | Tạo so sánh cầu thủ bằng biểu đồ và bảng; chọn cùng bối cảnh vị trí, đơn vị/thang đo rõ ràng, phân biệt số liệu gốc với percentile. | UI so sánh từ số liệu backend thật; biểu đồ không biến giá thị trường thành kỹ năng, không điền missing bằng 0; cảnh báo giới hạn chỉ số thủ môn/hậu vệ. |
| Day 22 | Tích hợp OpenAI API phía server: truy xuất context cầu thủ/recommendation thật, xây prompt có nguồn/cutoff, kiểm soát timeout, lỗi API và chi phí sử dụng. Bảo vệ key và chỉ chuyển dữ liệu cần thiết. | Scouting chat trả lời có căn cứ, báo thiếu thông tin thay vì bịa; test ràng buộc dữ liệu, lỗi dịch vụ và dữ liệu người dùng khác không lọt vào context. Kiểm tra API thật cần credentials hợp lệ qua secrets, không ghi vào repo. |
| Day 23 | Nối chat vào Streamlit; lưu/khôi phục chat sessions và messages theo user; liên kết kết quả gợi ý/so sánh trong hội thoại, rà privacy và lỗi đầu-cuối. | Luồng auth → search → recommendation → comparison → chat → history hoạt động cục bộ. Đối chiếu câu trả lời mẫu với dữ liệu; không tuyên bố đã kiểm chứng API thật nếu chỉ chạy mock. |

### Day 24–31 — Cloud Deployment, Integration Testing, Final Report và Presentation Slides

| Ngày | Công việc chi tiết dự kiến | Đầu ra và điều kiện nghiệm thu dự kiến |
|---|---|---|
| Day 24 | Chuẩn bị phương án cloud cho FastAPI, Streamlit và PostgreSQL; cấu hình build/start, secrets, HTTPS, migration, lưu dữ liệu, backup/restore, health check và chi phí. Rà quyền truy cập endpoint trước khi công khai. | Gói cấu hình triển khai và hướng dẫn vận hành/rollback có thể xem xét; kiểm tra build/config cục bộ. Trình phương án cụ thể khi cần phép deploy, chưa tự tạo hoặc triển khai hạ tầng cloud. |
| Day 25 | Nếu được phép, triển khai môi trường staging cloud, chạy migration và nạp dữ liệu thật theo chính sách; kiểm tra kết nối, persistence, auth và secrets. | URL và smoke-test cloud thực chạy khi đã được phép; nếu chưa, ghi rõ deploy bị chặn, chỉ hoàn thiện cấu hình/kiểm tra local. **Mốc commit/push Day 25**; quyền push và deploy được xét riêng. |
| Day 26 | Chạy integration/E2E trên các môi trường được phép: auth, privacy, search, top 3–5, comparison, chat, history. Kiểm tra lỗi mạng/API/DB và khả năng khôi phục phiên. | Báo cáo test có môi trường, bước tái hiện, kết quả và lỗi còn lại; ưu tiên sửa lỗi mất dữ liệu, truy cập chéo user, sai bộ lọc hoặc bịa thống kê. Nếu thiếu cloud, không gọi kết quả local là kiểm thử cloud. |
| Day 27 | Kiểm tra hiệu năng, truy cập đồng thời, bảo mật cấu hình, logging, backup/restore và rollback; sửa lỗi, chạy hồi quy có mục tiêu. | Đo latency/tải trong điều kiện ghi rõ; xác nhận bảo toàn dữ liệu và quyền riêng tư. Ghi giới hạn vận hành và checklist release, không tuyên bố khả năng mở rộng chưa đo. |
| Day 28 | Viết Final Report: vấn đề, nguồn dữ liệu/cutoff, EDA, feature engineering, recommendation/evaluation, kiến trúc, privacy, triển khai và kiểm thử. Tổng hợp hạn chế, nguồn tham khảo và hướng phát triển. | Bản báo cáo đầy đủ, số liệu truy vết được tới artefact; tách kết quả đã làm với kế hoạch/chưa kiểm chứng; không suy luận nhân quả hoặc gọi market value là phí chuyển nhượng. |
| Day 29 | Làm Presentation Slides và kịch bản demo: câu chuyện sản phẩm, sơ đồ kiến trúc, biểu đồ, kết quả đánh giá, giới hạn và câu hỏi phản biện. Chuẩn bị minh họa từ dữ liệu thật. | Deck, kịch bản demo và bộ câu hỏi/đáp; ảnh minh họa không lộ key, mật khẩu hoặc thông tin riêng; số liệu khớp Final Report. |
| Day 30 | Tổng duyệt demo, kiểm tra từ môi trường sạch theo hướng dẫn, đóng gói release candidate; rà report/slides, dependency, cấu hình và bugs. Chỉ sửa lỗi cần thiết và chạy test liên quan. | Release candidate có bằng chứng nghiệm thu, tài liệu cài đặt/vận hành, release notes và danh sách giới hạn. **Mốc commit/push Day 30.** Chưa tự phát hành hoặc deploy bản cuối. |
| Day 31 | Nghiệm thu cuối: đối chiếu toàn bộ yêu cầu sản phẩm, demo, test, Final Report và Slides. Chuẩn bị commit/tag/release cuối; chỉ push, công bố release hoặc deploy khi được phép. | **Final release Day 31** khi đủ bằng chứng và quyền thực hiện; bàn giao source, báo cáo, slides, hướng dẫn và môi trường được phê duyệt. Nếu còn yêu cầu bắt buộc hoặc quyền bị thiếu, ghi chưa hoàn tất, không tự đánh dấu release thành công. |

### Điều kiện chuyển giai đoạn và phạm vi kiểm chứng

- Day 10 cần engine cục bộ tái lập được; Day 12 cần đánh giá có cơ sở trước khi chọn cấu hình sử dụng cho ứng dụng. Không hy sinh tính trung thực để đạt mốc.
- Day 16 cần persistence/API cục bộ; Day 18 cần cách ly dữ liệu theo user. Cloud chỉ triển khai sau khi auth/privacy và cấu hình cần thiết được kiểm tra, đồng thời có phép deploy.
- Day 23 cần các luồng sản phẩm tích hợp cục bộ; kiểm tra OpenAI API thật phải được phân biệt với test giả lập lỗi dịch vụ. Không tạo dữ liệu cầu thủ giả để demo hoặc đánh giá.
- Chỉ đưa feature đã được chọn và xử lý phù hợp vào engine, không dùng toàn bộ 28 cột làm vector. Mốc reliability, log định giá và percentile không tự trở thành điểm kỹ năng.
- Nếu thiếu thời gian, dữ liệu, credentials hoặc quyền triển khai, ghi trở ngại và đề xuất điều chỉnh; không âm thầm bỏ yêu cầu sản phẩm, đổi cutoff hoặc ghi nhận công việc chưa làm là đã hoàn thành.

### Mốc commit/push chính thức (đều là dự kiến)

| Mốc | Nội dung dự kiến đóng gói | Điều kiện |
|---|---|---|
| Day 5 | Đặc tả feature/input và baseline Recommendation Engine ban đầu | Rà diff, dữ liệu và test; commit theo phạm vi được giao; push khi người dùng cho phép |
| Day 10 | Recommendation Engine tích hợp và test hồi quy | Ghi cấu hình, giới hạn và bằng chứng; push khi được phép |
| Day 15 | Đánh giá mô hình, PostgreSQL và FastAPI bước đầu | Không gộp secrets/dataset bị ignore; push khi được phép |
| Day 20 | Authentication, Privacy và Streamlit search/history | Có kiểm tra quyền sở hữu và luồng chính; push khi được phép |
| Day 25 | UI comparison/chat, cấu hình cloud và kết quả staging thực có | Không gọi cấu hình là deploy; push/deploy chỉ với quyền tương ứng |
| Day 30 | Integration tests, Final Report, Slides và release candidate | Đối chiếu bằng chứng, lỗi còn lại và docs; push khi được phép |
| Day 31 | Final release: commit/tag và bản phát hành dự kiến | Đủ yêu cầu nghiệm thu; push, công bố release/tag và deploy chỉ khi được phép |

- Trước mỗi mốc: kiểm tra Git status/branch/remote, diff, secrets, danh sách file, test phù hợp và lịch sử local/remote. Không force-add dữ liệu bị ignore; không viết lại lịch sử, force push hoặc reset --hard.
- Các mốc trên là lịch dự kiến, **không phải quyền push/deploy tự động**. Quyền push lần trước không được mở rộng sang mốc tương lai. Nếu chưa được phép, giữ kết quả ở local và báo rõ phần đang chờ.
- Khi một mốc thực sự hoàn tất, bổ sung commit hash và trạng thái push/deploy thực tế vào nhật ký; không điền hash hoặc kết quả giả cho các mốc tương lai.

### Đối chiếu Git và phạm vi phiên lập kế hoạch

- Trước chỉnh sửa: `main` theo dõi `origin/main`, working tree sạch theo kiểm tra local. Lịch sử hiện có, từ cũ tới mới: `86c0360` (Day 1) → `266f90f` (Day 4) → `c4d638c` (commit riêng Day 2–3). Thứ tự commit phản ánh thời điểm lưu mốc, không viết lại để đổi thứ tự ngày.
- Lần kết nối GitHub trước đã push theo quyền được cấp tới `https://github.com/tranhaidong23/ScoutIQ-AI`; phiên lập kế hoạch này không fetch/push hoặc kiểm chứng trạng thái GitHub mới.
- Chỉ cập nhật `AGENTS.md` và `reports/project_log.md`; giữ nguyên các yêu cầu và nội dung lịch sử. Không tạo/sửa Python, dữ liệu, schema, giao diện, mô hình hoặc hạ tầng; không triển khai Day 5.
- Kiểm tra phù hợp cho thay đổi này: đối chiếu đủ 27 ngày Day 5–31, đúng 5 giai đoạn và 7 mốc Git; giữ nguyên nội dung cũ, kiểm tra diff/phạm vi file. Không cần chạy lại pipeline hoặc test sản phẩm cho thay đổi kế hoạch.
- Không stage, commit, push, deploy hoặc tạo release trong phiên này. Trạng thái Day 5–31 vẫn là **Dự kiến**.

## 2026-10-28 — Day 5: Baseline Content-Based Recommendation

### Trạng thái và phạm vi

- **Đã hoàn thành có bằng chứng** trong phạm vi Day 5 được giao: kiểm tra features, lựa chọn đặc trưng theo vị trí, chuẩn hóa, cosine recommender, bộ lọc, Top K có giải thích, kịch bản thực và kiểm thử.
- Mục này cập nhật trạng thái Day 5 của lộ trình trước; **Day 1–5 hoàn thành, Day 6–31 chưa triển khai**. Baseline dùng cosine chưa tối ưu trọng số. Theo yêu cầu mới, phần chuẩn hóa/cosine và giải thích cơ bản được thực hiện ngay Day 5; Day 6 tiếp tục weighted cosine và đánh giá độ nhạy, không coi toàn bộ Day 6 đã xong.
- Defender/GK chỉ được trả shortlist theo **hồ sơ bối cảnh**, không tuyên bố đã có mô hình đánh giá năng lực phòng ngự/bắt bóng. Các thiếu hụt dữ liệu chuyên môn vẫn còn.
- Không commit, push hoặc deploy theo yêu cầu phiên này, dù lộ trình có mốc Git Day 5. Thay đổi kế hoạch chưa commit từ phiên trước trong `AGENTS.md` và nhật ký được giữ nguyên.

### Kiểm tra đầu vào

- Đã đọc `AGENTS.md`, nhật ký, insights và code Day 4 trước khi triển khai.
- `data/processed/scoutiq_features_2025_26.csv`: **4.112 dòng × 28 cột**, 4.112 ID duy nhất; validation Day 4 đạt, không infinity hoặc sai per90 vượt tolerance; 8 đặc trưng Day 4 không missing.
- Missing metadata vẫn là foot 24, height 23, current_club_name 16 và club_name_verified 16. Chiều cao 19 cm của Connor Allan (`743556`) giữ nguyên, không suy đoán sửa thành 190; loại chiều cao khỏi vector. Chưa xác minh lại giá trị đúng từ nguồn.
- Ngày định giá được kiểm tra với cutoff 2026-06-12; việc này không chứng minh toàn bộ metadata có đúng thời điểm lịch sử.
- SHA-256 input: `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`.

### Đặc trưng và thuật toán thực hiện

| Vị trí | Đặc trưng số (StandardScaler riêng theo vị trí) | One-hot | Phạm vi kết quả |
|---|---|---|---|
| Attack | goals_per90, assists_per90 | sub_position | Đóng góp tấn công và vai trò; 6 chiều sau mã hóa trong lần chạy |
| Midfield | goals_per90, assists_per90 | sub_position | Chỉ đóng góp tấn công, chưa mô tả chuyền/phòng ngự; 7 chiều |
| Defender | age, minutes_played | sub_position, foot | Hồ sơ bối cảnh, không điểm phòng ngự; 8 chiều |
| Goalkeeper | age, minutes_played | foot | Hồ sơ bối cảnh, không điểm bắt bóng; 5 chiều |

- Attack/Midfield dùng cùng loại số đo vì dữ liệu chưa có chỉ số chuyên biệt đáng tin cậy, nhưng fit riêng và mã hóa các vai trò khác nhau. Defender/GK không dùng goals, assists hoặc các biến dẫn xuất của chúng.
- Không chọn market value/log value, percentile Day 4, chiều cao, CLB, ID, reliability hoặc goal contributions vào vector. Tránh đếm lặp và tránh dùng percentile toàn tập trong kiểm tra held-out. Tuổi/phút trong Defender/GK là bối cảnh, không khẳng định ít tuổi/nhiều phút là giỏi hơn.
- API nhận ID cầu thủ tham chiếu thật cùng `SearchFilters(position, min_age, max_age, max_budget_eur, min_minutes)` và `top_k` mặc định 5. Vị trí phải khớp tham chiếu; chính ID đó bị loại khỏi kết quả. Tham chiếu có thể ngoài bộ lọc tuổi/ngân sách của shortlist.
- Fit scaler/danh mục trên tập reference trước tìm kiếm; không fit lại sau lọc. Mặc định constructor dùng catalogue cho truy xuất mô tả, hoặc nhận `fit_player_ids` tường minh để tách tham chiếu fit khỏi truy vấn.
- Ghép z-score và one-hot, L2 normalize, tích vô hướng để tính cosine. Trọng số mỗi chiều bằng 1, chưa đánh giá tỷ trọng block. Score trong [-1,1], không quy đổi thành xác suất; xếp giảm dần sau làm tròn 12 chữ số, hòa điểm theo ID tăng dần.
- Bộ lọc bao gồm biên tuổi/ngân sách/phút; ngân sách dùng EUR gốc. Trả ít hơn K khi thiếu, không tự nới điều kiện. Dataset đã lọc >=900 phút nên không khôi phục cầu thủ bị loại khi yêu cầu min_minutes thấp hơn.
- Missing/unseen category được mã hóa block 0, không tạo chân thuận giả hoặc thưởng điểm cho cùng thiếu. Vector 0 không được xếp hạng tùy ý: báo lỗi trạng thái cho query hoặc loại ứng viên có đếm số lượng. Lần chạy thực không có vector 0.
- Kết quả có tên, CLB (null khi thiếu), vị trí, tuổi, phút, market value, ngày định giá, similarity, phạm vi diễn giải và explanation; `evidence` giữ số liệu hai cầu thủ, `cosine_components` phân rã tổng score. Không dùng LLM để bịa giải thích.

### Kịch bản thực và kiểm tra leakage

Runner loại 4 ID tham chiếu khỏi fit: Harry Kane `132098`, Hans Vanaken `137576`, Virgil van Dijk `139208`, Lukas Hornicek `629773`. Fit **4.108** người: Attack 1.058, Midfield 1.203, Defender 1.522, Goalkeeper 325. Số ID giao giữa query và fit = **0**.

| Kịch bản | Bộ lọc tuổi / ngân sách tối đa / phút tối thiểu | Ứng viên sau lọc, loại bản thân | Kết quả |
|---|---|---:|---|
| Attack, tham chiếu Harry Kane | 18–29 / €30M / 1.800 | 349 | Top 5, checks đạt |
| Midfield, tham chiếu Hans Vanaken | 20–30 / €15M / 1.800 | 405 | Top 5, checks đạt |
| Defender, tham chiếu Virgil van Dijk | 22–32 / €15M / 2.000 | 512 | Top 5 hồ sơ bối cảnh, checks đạt |
| Goalkeeper, tham chiếu Lukas Hornicek | 20–30 / €10M / 1.800 | 107 | Top 5 hồ sơ bối cảnh, checks đạt |
| Attack, ngân sách bằng 0 | 18–29 / €0 / 1.800 | 0 | Rỗng, không nới filter, checks đạt |

- Toàn bộ Top 5 và explanation nằm trong `reports/day5_recommendation_examples.md`; JSON cùng tên chứa cấu hình/scaler/categorical vocabulary, hash fit IDs, schema, chất lượng dữ liệu và đóng góp từng chiều.
- Kiểm tra fit boundary: thay đổi riêng số liệu của 4 query trong bộ nhớ không làm thay đổi mean/scale/vocabulary/hash tập fit. Search với bộ lọc khác nhau cũng không fit lại. Không sử dụng percentile đã tính từ toàn catalogue.
- Đây là kiểm tra preprocessing/logic, **không phải temporal split, kiểm toán leakage toàn bộ pipeline hoặc đánh giá chất lượng recommendation**. Không có nhãn chuyên gia nên không báo Precision@K/NDCG hay “độ chính xác”.

### File và lệnh đã chạy

- Tạo `src/recommendation/baseline.py`: policy theo vị trí, validation, chuẩn hóa, cosine, bộ lọc và giải thích.
- Tạo `src/recommendation/run_day5.py`: 5 kịch bản dữ liệu thật, assertion bộ lọc/score/thứ hạng và xuất báo cáo.
- Tạo `src/recommendation/README.md`: hợp đồng sử dụng, feature selection, công thức và giới hạn.
- Tạo `tests/test_recommendation.py`: 34 test cases mới.
- Tạo `reports/day5_recommendation_examples.json` và `.md`; bổ sung hai báo cáo và trạng thái hiện hành trong `AGENTS.md`.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_recommendation.py tests/test_features.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day5
```

- Môi trường `.venv`: Python 3.13.7, pandas 3.0.6, NumPy 2.5.4, scikit-learn 1.9.1. Không cài dependency mới.
- Kết quả cuối: **57 passed in 6.06s**, exit code 0 (**34 mới + 23 Day 4**). Bao phủ 5 kịch bản, công thức cosine độc lập, Top K từ thứ hạng đầy đủ, filter biên, thiếu ứng viên, vector 0, input/ID sai, duplicate/missing/infinity/future valuation, bảo toàn dữ liệu và thứ tự ổn định.
- Có kiểm tra bất biến: thay định giá/CLB/chiều cao/percentile không đổi ID/score khi không áp ngân sách; thay bàn thắng/kiến tạo của GK/Defender không đổi thứ hạng. Các thay đổi kiểm thử chỉ nằm trong bản sao bộ nhớ, không tạo dữ liệu cầu thủ giả trong output.
- Lần test đầu có 1 failure ở fixture kiểm tra leakage: fixture đã tính lại per90 cho cả tập fit, gây chênh float khoảng `1e-16`. Đã sửa fixture để chỉ thay đổi các hàng held-out đúng ý định; không nới assertion để che lỗi. Lần chạy cuối đạt như trên.
- Runner exit code 0; cả 5 scenario checks đạt, CSV features không đổi SHA-256. Không chạy lại pipeline cleaning/EDA/feature engineering có tác dụng ghi đè dữ liệu.

### Phát hiện và Day 6

- Ví dụ Franculino có cosine **0,991291** với Harry Kane dù goals/90 **0,917476 vs 1,266144**. Similarity cao chỉ thể hiện hướng vector mã hóa và vai trò, không chứng minh khả năng ghi bàn bằng nhau hoặc thay thế tương đương.
- Baseline một phần phụ thuộc hình học của z-score và one-hot; score giữa các vị trí không so sánh trực tiếp. Chưa hiệu chỉnh chất lượng giải đấu, tactical fit, hợp đồng/chấn thương hoặc mức phí mua thực tế.
- Defender/GK cần dữ liệu phòng ngự/bắt bóng thật trước khi đánh giá năng lực. Không thay thế bằng bàn thắng, không suy luận causal hoặc tự tạo chỉ số.
- **Day 6 dự kiến:** thử weighted cosine với trọng số/block rõ ràng; ablation số đo/vai trò, độ nhạy chuẩn hóa và tham chiếu fit; xem vấn đề cosine coi các vector cùng hướng là gần dù biên độ khác; đánh giá cách trình bày hoặc từ chối xếp hạng năng lực Defender/GK khi thiếu dữ liệu. Chưa triển khai KNN, API, UI hoặc đánh giá chuyên gia.
- HEAD vẫn ở mốc trước Day 5 (`c4d638c`); không stage/commit/push/deploy trong nhiệm vụ này. Không ghi đè thay đổi tài liệu chưa commit từ phiên lập kế hoạch.

## 2026-11-02 — Thiết lập tài liệu bàn giao Codex Windows → Claude Code

### Mục tiêu, trạng thái và phạm vi

- **Đã hoàn thành trong phạm vi thiết lập tài liệu local.** Chuẩn bị AI mới hiểu sản phẩm, tái tạo môi trường, nhận snapshot và tiếp tục mà không cần lịch sử chat. **Chưa nghiệm thu chuyển máy thực tế; Day cuối vẫn là Day 5, Day 6 chưa triển khai.**
- Đọc AGENTS, báo cáo/artefact, scripts/tests, requirements, Git status/log/remote/diff. Phân biệt kiểm tra trực tiếp phiên này, số liệu lịch sử và kế hoạch; không xóa nội dung cũ.
- Không tải lại dữ liệu, chạy pipeline ghi đè hoặc đổi mã nguồn, tests, requirements/.gitignore. Không cài thêm dependency, stage/commit/push/deploy hoặc upload dữ liệu/secrets.

### File tạo/cập nhật

- Tạo [CLAUDE.md](../CLAUDE.md): thứ tự đọc, quy tắc và checklist sau mỗi Day.
- Tạo [PROJECT_CONTEXT](../docs/PROJECT_CONTEXT.md): đầy đủ yêu cầu sản phẩm, dữ liệu, tổng hợp Day 1–5 (mục tiêu/file/data/thuật toán/test/insight/giới hạn/commit), kế hoạch Day 6–31.
- Tạo [ARCHITECTURE](../docs/ARCHITECTURE.md): module/data flow và recommender hiện có; phân biệt FastAPI/Streamlit/PostgreSQL/OpenAI/cloud dự kiến.
- Tạo [FILE_INVENTORY](../docs/FILE_INVENTORY.md): source/tests/tài liệu/artefact, input/output/dependency và thư mục rỗng.
- Tạo [HANDOFF](../docs/HANDOFF.md): Day/HEAD/status, source chưa commit, blockers, next steps, lệnh, mẫu cập nhật và điều kiện chuyển máy.
- Tạo [SETUP](../docs/SETUP.md): clone, venv mới Windows/POSIX, dependencies, nhận/tái tạo snapshot, hash/tests và chạy baseline; chưa có app web để khởi chạy.
- Tạo [DATA_MANIFEST.json](../docs/DATA_MANIFEST.json) và [environment-observed.json](../docs/environment-observed.json): hash/bytes 8 dataset, schema/shape 3 processed; Python/OS/11 dependency trực tiếp + pip. Không chứa payload dataset hay secrets; environment là quan sát, không full lock.
- Bổ sung AGENTS và hai báo cáo; giữ nguyên lịch sử và thay đổi sẵn có của người dùng.

### Bằng chứng kiểm tra mới

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pip check
git status --short --branch
git log -3 --format="%H %s"
git remote -v
git rev-parse origin/main
git diff --check
```

- **57 passed in 10.67s**, exit 0: 23 feature + 34 recommendation. Đây là lượt chạy mới, khác thời gian test Day 5 lịch sử.
- **No broken requirements found**, exit 0. Python 3.13.7 trên Windows 11; pandas 3.0.6, numpy 2.5.4, sklearn 1.9.1; xem environment-observed cho phiên bản trực tiếp khác.
- Đọc bytes và SHA-256 cả 5 raw + 3 processed; đọc shape/schema processed: players **8.322×20**, candidates **4.112×21**, features **4.112×28**. Không đếm lại toàn bộ raw hôm nay; số hàng raw trong PROJECT_CONTEXT được gắn nhãn lịch sử từ day1_data_quality.
- Kiểm tra liên kết Markdown của bộ bàn giao, JSON parse, code fences, cú pháp 6 đoạn Python inline trong SETUP, đối chiếu inventory với toàn bộ source/tests/reports/docs và root files liên quan: không phát hiện link hỏng/file thiếu. Kiểm tra cú pháp không thay thế chạy fresh-install trên máy mới.
- Đối chiếu hash: source, tests, datasets, artefact cũ, requirements và .gitignore không đổi. Tiền tố byte của AGENTS/project_log/insights giữ nguyên nội dung cũ; chỉ bổ sung. HEAD/Git index không đổi. git diff --check không báo lỗi whitespace; có cảnh báo Git về LF→CRLF của AGENTS, không phải lỗi test.

### Phát hiện ảnh hưởng bàn giao và Git

- Branch main; HEAD **c4d638c2d10c542c897ccf95dedde540814925b1**. origin fetch/push là https://github.com/tranhaidong23/ScoutIQ-AI.git; origin/main cache trùng HEAD. **Không fetch/kiểm chứng remote trực tiếp** trong phiên này.
- Lịch sử giữ nguyên: 86c0360 (Day 1) → 266f90f (Day 4) → c4d638c (Day 2–3). Day 5 chưa commit; source/tests/báo cáo Day 5 untracked có từ trước phiên tài liệu. Ba tài liệu quản lý đã modified từ trước; phiên này chỉ bổ sung.
- Sau phiên: thêm CLAUDE/docs untracked, ba tài liệu quản lý tiếp tục modified; không có staged changes. Clone commit hiện tại không chứa Day 5 hoặc bộ bàn giao mới. Cần nhiệm vụ rà soát/commit/push được phép trước khi chuyển máy, không tự thực hiện.
- .gitignore bảo vệ raw/processed/external, venv và .env/.env.*; .env.example cũng bị ignore. Baseline chưa cần biến môi trường ứng dụng nên chưa tạo template giả. Khi triển khai cấu hình thật mới tạo placeholder và exception có chủ đích.
- requirements.txt UTF-16 LE BOM, chưa pin. SETUP chuyển bản tạm UTF-8 trong venv và dùng phiên bản quan sát làm constraints tham khảo; chưa xác minh availability/cross-platform hoặc dependency bắc cầu.
- Downloader dùng URL mutable và skip file khác rỗng; tái tải không bảo đảm snapshot giống. Đề xuất kho riêng/ổ đĩa cho 5 raw + 3 processed, kiểm manifest trước/sau chuyển; chưa chọn kho, tạo archive hay upload.

### Quy trình tiếp tục và phần chưa kiểm chứng

- Sau mỗi Day: chạy tests thực có; cập nhật project_log, insights_and_defense, HANDOFF; cập nhật inventory/I/O/dependency khi thay đổi, SETUP/ARCHITECTURE nếu cách chạy/thiết kế đổi. Cập nhật trạng thái AGENTS/PROJECT_CONTEXT, giữ lịch sử trong log.
- Đề xuất commit/push ở Day **5, 10, 15, 20, 25, 30**, final release **31**; không tự coi lịch mốc là quyền thao tác.
- Khi chuyển máy: làm mới status/hash/môi trường, nhận đủ source+data và chạy từ clone sạch. Chưa kiểm fresh install, raw→features đầy đủ, Linux/macOS, GitHub trực tiếp hoặc app web/cloud trong phiên này.
- Day 6 khi được giao: weighted cosine/block weights và độ nhạy, giữ baseline và fit boundary; không mặc định giá thị trường là kỹ năng, không xếp hạng năng lực GK/Defender khi thiếu chỉ số.

## 2026-11-02 — Day 6: Weighted Cosine Similarity & Recommendation Evaluation

### Trạng thái và bảo toàn baseline

- **Đã hoàn thành có bằng chứng trong phạm vi Day 6 được giao**: weighted cosine + đánh giá hành vi/độ nhạy, không phải nghiệm thu chất lượng tuyển trạch hay toàn bộ Model Evaluation Day 11–12. Day 7 chưa triển khai.
- Đọc AGENTS/CLAUDE/HANDOFF, logs/insights, code/tests Day 4–5. Trước sửa: main tại c4d638c, ba tài liệu quản lý modified; CLAUDE/docs, code/tests/báo cáo Day 5 untracked từ trước; không có staged changes. Giữ nguyên thay đổi đó.
- Lượt kiểm baseline đầu phiên: **57 passed in 6.43s**, exit 0. Không sửa baseline.py, run_day5.py, build_features.py, tests cũ hoặc artefact Day 4–5; tái lập trong RAM, không chạy runner Day 5 ghi đè báo cáo.
- Dataset features SHA-256 **425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0**, 4.112×28; cutoff 2026-06-12, mùa 2025/26. Reference 4.108 ID, loại 4 query 132098/137576/139208/629773; fit Attack/Midfield/Defender/GK lần lượt 1.058/1.203/1.522/325.

### Code, thuật toán và cấu hình

- Tạo [weighted.py](../src/recommendation/weighted.py): subclass dùng nguyên preprocessing/filter/ranking Day 5; cosine = sum(w*x*y)/sqrt(sum(w*x²)*sum(w*y²)), thực hiện sqrt(w/max_w) rồi L2. Trọng số semantic theo position, categorical áp lên từng indicator trong cùng block.
- Validation đủ 4 position và đúng feature keys; w hữu hạn >=0, không bool/string/NaN/∞, mỗi vị trí còn trọng số dương; dynamic range underflow bị từ chối. Zero từng feature là ablation, toàn zero không hợp lệ; query/candidate vector 0 xử lý theo hợp đồng Day 5. Explanation không viện dẫn feature bị ablate.
- Tạo [evaluation.py](../src/recommendation/evaluation.py): filter/score/ID/order/components checks, overlap@K và Spearman full-common với average ranks của score, undefined trả null có lý do.
- Tạo [run_day6.py](../src/recommendation/run_day6.py): kiểm hash/baseline lịch sử, unit-weight parity, 6 config × 5 SCENARIOS không đổi; audit reference-only correlations; bảo vệ output cũ bằng từ chối overwrite mặc định.
- Tạo [DAY6.md](../src/recommendation/DAY6.md): API/công thức, đầy đủ weights và protocol/giới hạn/Day 7; [tests/test_weighted_recommendation.py](../tests/test_weighted_recommendation.py): 52 test cases mới.

Theo thứ tự Attack/Midfield=(g90,a90,role), Defender=(age,minutes,role,foot), GK=(age,minutes,foot):

| Cấu hình | Attack | Midfield | Defender | GK |
|---|---|---|---|---|
| baseline | 1/1/1 | 1/1/1 | 1/1/1/1 | 1/1/1 |
| weighted_default | .4/.4/.2 | .3/.5/.2 | .2/.2/.4/.2 | .25/.25/.5 |
| numeric_emphasis | .6/.3/.1 | .2/.7/.1 | .4/.4/.1/.1 | .45/.45/.1 |
| categorical_emphasis | .2/.2/.6 | .15/.25/.6 | .1/.1/.6/.2 | .1/.1/.8 |
| ablate_categories | .4/.4/0 | .3/.5/0 | .2/.2/0/0 | .25/.25/0 |
| ablate_first_numeric | 0/.4/.2 | 0/.5/.2 | 0/.2/.4/.2 | 0/.25/.5 |

Weights là giả thuyết có chủ đích, không được học từ labels/chuyên gia. Attack/Midfield chỉ mô tả đóng góp tấn công; numeric Defender/GK là context, không điểm kỹ năng. Không dùng market value/log value/reliability/percentile/contributions hoặc chiều cao làm vector; không nhân reliability vào score.

### Lệnh và kết quả thực chạy

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day6
```

- Suite sau triển khai: **109 passed in 13.12s; 0 failed; exit 0** (57 cũ + 52 mới). Bao phủ oracle weighted cosine độc lập cả 4 position, unit-weight baseline regression, weights/input invalid, zero weights/vector, partial ablation, missing categories, scale invariance, filters biên/rỗng, reproducibility, held-out fit isolation và no-price/no-GK-goals. Tests dùng data thật, fault injection chỉ trong RAM/temp; không sửa dataset.
- Runner exit 0: **5/5 Day 5 exact match** ID/score/filter/count/status và fit audit; weights=1 khớp full ranking. **30/30 tổ hợp** đạt filters, score [-1,1]/finite, unique/exclude-query, deterministic sorting, components sum, top-K prefix và fit không thay sau search. Kiểm lặp và đảo catalogue/fit IDs.
- 24 nonempty và 6 empty; eligible 349/405/512/107/0 không đổi giữa config, không vector 0 bị loại trong các query thực. Empty contract checks là vacuous, overlap/rho là null, không gán 1.
- Python 3.13.7, pandas 3.0.6, numpy 2.5.4, sklearn 1.9.1 trên Windows; không cài dependency mới. JSON lưu OS/Python/libs, source hashes, Git local, thời điểm UTC, dataset, query/filter, fit và weights.

| Cấu hình | Overlap@5 Attack / Mid / Def / GK | Mean overlap (4 query) | Mean Spearman full-common |
|---|---|---:|---:|
| baseline | 1 / 1 / 1 / 1 | 1.00 | 1.0000 |
| weighted_default | .8 / 1 / 1 / .8 | .90 | .9882 |
| numeric_emphasis | .6 / 1 / 1 / 1 | .90 | .9723 |
| categorical_emphasis | .8 / 1 / .8 / .8 | .85 | .9265 |
| ablate_categories | 0 / .4 / .2 / .4 | .25 | .8785 |
| ablate_first_numeric | 0 / .6 / .2 / .6 | .35 | .7397 |

Overlap=intersection/K, giữ K=5; Spearman tính trên full rankable pool chung bằng average rank của score đã round12, không coi ID tie-break là mức tương đồng. Tất cả config có cùng pool trong lần chạy. Mean chỉ mô tả 4 query cố định; không chọn config tốt nhất bằng stability, không tính Precision@K/NDCG@K vì chưa có relevance labels.

### Artefact và phát hiện

- Tạo riêng reports/day6/: [evaluation.json](day6/evaluation.json), [metrics.csv](day6/metrics.csv) 30 dòng, [rankings.csv](day6/rankings.csv) 8.238 dòng, [correlations.csv](day6/correlations.csv) 264 cặp, [comparison.png](day6/comparison.png), [correlations.png](day6/correlations.png), [summary.md](day6/summary.md). Hai hình đã xem để kiểm nhãn/bố cục; không gọi biểu đồ ổn định là chất lượng.
- Top 5 default truy vấn Kane: Franculino .993602; Luis Suárez .981602; Gianluca Scamacca .960249; Jonathan Burkardt .955912; Tammy Abraham .954119. Truy vấn Vanaken: Ringo Meerveld .999750; Nikola Vlašić .998645; Thijs Oosting .992523; Fabian Rieder .992131; Carlo Holse .988221. Metadata CLB/tuổi/giá và evidence xem summary/JSON; giá là market value lịch sử.
- Audit fit-only: Attack corr goals–goals/90=.810577, assists–assists/90=.830681; Midfield=.882477/.852483. Goals/90–assists/90: Attack=-.018939, Midfield=.347238. Không tự bỏ một trong hai chỉ vì giả định tương quan cao.
- Contributions/90 là tổng đúng của g90+a90; minutes–reliability Pearson .914953–.960653 theo position. Giữ tránh đếm lặp, không dùng reliability như kỹ năng; tương quan không causal.
- Attack ablate_categories overlap=0 nhưng rho=.933110: ổn định toàn ranking không đảm bảo Top 5 giống. Trọng số thay đổi kết quả có thể mạnh ngay trong cùng dataset; chưa có ground truth để gọi đổi thứ hạng là cải thiện.

### Tài liệu, hạn chế và Day 7

- Cập nhật AGENTS/CLAUDE, HANDOFF, FILE_INVENTORY, PROJECT_CONTEXT, ARCHITECTURE, SETUP và hai báo cáo; giữ các snapshot lịch sử có nhãn. HEAD/index không đổi, dữ liệu nguồn và artefact Day 4–5 giữ nguyên. Không stage/commit/push/deploy; source Day 5–6/docs vẫn chưa commit.
- Giới hạn: chỉ 4 query thực + 1 rỗng, weights heuristic, chưa temporal evaluation/expert labels/league adjustment; Defender/GK thiếu chỉ số chuyên môn, metadata CLB/cầu thủ chưa audit đầy đủ theo cutoff. Subclass phụ thuộc matrix nội bộ baseline, được bảo vệ bằng parity tests.
- Day 7: KNN đối chứng cùng representation/reference/filter; kiểm cosine-distance parity/tie/self-exclusion, top-K/pool và thời gian; khảo sát metric khác có lý do, không chọn theo thị giá hoặc bịa labels. Giữ baseline và default Day 6 như đối chứng, chưa chọn winner.
- Mốc Git Day 5 còn chờ nhiệm vụ được phép; mốc kế tiếp Day 10 (sau đó 15/20/25/30/31). Lịch không cấp quyền tự commit/push/deploy. Chưa fresh-install hoặc chuyển máy trong Day 6.

### Kiểm tra cuối phiên Day 6

- Tính lại overlap và Spearman từ rankings.csv khớp metrics trong evaluation.json; 30 dòng metrics, 8.238 ranked rows, 264 correlation pairs. Source hashes trong JSON vẫn khớp file thực thi.
- Kiểm link tài liệu và inventory: không link hỏng/file thiếu. git diff --check không báo lỗi whitespace (Git có cảnh báo LF→CRLF của AGENTS).
- Đối chiếu snapshot đầu phiên: chỉ 9 tài liệu sẵn có thay đổi đúng phạm vi; không đổi source/tests/artefact Day 4–5, raw/processed, requirements, .gitignore hoặc manifests cũ. Các file Day 6 là mới.
- Tiền tố byte AGENTS/project_log/insights giữ nguyên, chỉ bổ sung lịch sử. HEAD và Git index không đổi; không stage/commit/push/deploy. Thay đổi chưa commit của người dùng được bảo toàn.

## 2026-11-02 — Rà soát Day 6 trước Day 7 (chỉ kiểm tra và tài liệu)

- **Kết quả mới:** chạy `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider` → **109 passed in 14.60s, 0 failed** (23 features + 34 baseline + 52 weighted/evaluation). Chạy `.\.venv\Scripts\python.exe -B -m pip check` → **No broken requirements found**, exit 0. Không chạy lại runner/cleaning/EDA ghi file.
- Đối chiếu trực tiếp 8/8 dataset với DATA_MANIFEST: SHA-256 và kích thước đều khớp. Processed shapes: 8.322×20, 4.112×21, 4.112×28. 6 source hashes lưu trong Day 6 JSON đều khớp code; features hash cũng khớp báo cáo.
- Artefact Day 6 có đủ 7 file: evaluation.json, metrics.csv (30 dòng), rankings.csv (8.238 dòng), correlations.csv (264 cặp), comparison.png, correlations.png, summary.md. Flags filter/score/ID/sort/components/full-ranking/determinism/pool trong CSV đều true. 5 kịch bản baseline exact-match là bằng chứng đã lưu từ runner Day 6, không mô tả là runner mới chạy hôm nay.
- File Day 6 đối chiếu theo nhật ký/inventory và thực tế: 3 module weighted.py/evaluation.py/run_day6.py, tests/test_weighted_recommendation.py, hướng dẫn DAY6.md và 7 artefact trên. Day 6 đã cập nhật AGENTS/CLAUDE, 5 docs (HANDOFF/FILE_INVENTORY/PROJECT_CONTEXT/ARCHITECTURE/SETUP), project_log và insights. Do chưa commit Day 5–6, không suy ngày tạo từng file chỉ từ git status.
- HANDOFF đã có trạng thái Day 6, kết quả, lệnh test/runner giữ artefact cũ và scope Day 7. Bổ sung bằng chứng rà soát mới; giữ thời gian test cũ làm lịch sử.
- Chỉnh CLAUDE để yêu cầu đủ source/tests Day 5–6 và đọc DAY6.md. Chỉnh SETUP để các bước chạy hiện hành dùng 109 tests và nêu rõ reports/day5_recommendation_examples.json là prerequisite của runner Day 6. Giữ ghi nhận 57 tests ở phần lịch sử môi trường.
- **Git:** branch main; origin fetch/push https://github.com/tranhaidong23/ScoutIQ-AI.git; commit gần nhất c4d638c2d10c542c897ccf95dedde540814925b1, message `feat: complete ScoutIQ Day 2 data preparation and Day 3 EDA`. Ref origin/main cache trùng HEAD; không fetch/xác minh GitHub trực tiếp. AGENTS và hai reports modified; CLAUDE/docs, source/tests/báo cáo Day 5–6 untracked; không có staged diff.
- **Chuyển máy:** hướng dẫn đủ để thực hiện có điều kiện, chưa nghiệm thu thực tế. Cần bàn giao source chưa commit + JSON đối chứng, snapshot ngoài Git, venv mới. Requirements UTF-16/unpinned và source URL mutable vẫn là giới hạn; chưa full lock/fresh-install/raw rebuild/cross-platform. Không upload data/secrets.
- **Day 7 khi được giao:** KNN cùng representation/scaler/reference/filter, đối chứng cosine-distance và weighted cosine, tie/self-exclusion, Top K/pool/latency; không suy stability thành quality, không relevance metrics khi thiếu labels, Defender/GK context-only. Không triển khai Day 7 trong phiên rà soát.
- Phiên này chỉ sửa CLAUDE, SETUP, HANDOFF và bổ sung hai báo cáo; không tạo/sửa code, tests, dataset hoặc artefact thực nghiệm. Không stage/commit/push/deploy.

## 2026-11-02 — Day 7: KNN Benchmark & Recommendation Robustness

### Phạm vi và bảo toàn baseline

- **Đã hoàn thành có bằng chứng trong phạm vi Day 7**, Day 8 chưa triển khai. Đọc hướng dẫn, HANDOFF/ARCHITECTURE, log/insights và code Day 5–6 trước sửa.
- Git đầu phiên main/c4d638c, đã có AGENTS/reports modified, CLAUDE/docs và source/tests/reports Day 5–6 untracked; không staged. Giữ nguyên baseline.py, weighted.py, evaluation.py, run_day5.py/run_day6.py, tests cũ, datasets và artefact cũ.
- Lượt baseline đầu phiên: **109 passed in 15.45s**, exit 0. Không tải lại dữ liệu hoặc chạy cleaning/EDA/runner cũ ghi đè.
- Snapshot features **4.112×28**, SHA-256 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0, season 2025/26, cutoff 2026-06-12. Fit 4.108 người, loại 4 query IDs 132098/137576/139208/629773, cùng SCENARIOS và eligible 349/405/512/107/0.

### Implementation và file

- Tạo [knn.py](../src/recommendation/knn.py): KNNRecommender composition với nguyên baseline/weighted representation. NearestNeighbors(metric=cosine, algorithm=brute, n_jobs=1); filter/exclude query/zero candidates trước, fit neighbors trên encoded pool rồi lấy tất cả neighbors. Score round(1-distance,12), sort giảm dần + ID tăng dần, cắt K; không mất boundary ties, không refit scaler/category.
- K quá lớn trả số có thật; query vector 0 trả zero_reference_vector, empty trả no_candidates; NaN/infinity/shape sai/invalid request bị từ chối. Output giữ dữ liệu thật/evidence/limits, thêm cosine_distance. Defender/GK context-only; không market value/reliability skill.
- Tạo [run_day7.py](../src/recommendation/run_day7.py): đối chiếu source/input hash và JSON baseline, parity/robustness, warm-up/multiple timing runs; từ chối output cũ, dùng --output-dir mới để chạy lại. Không có --overwrite.
- Tạo [tests/test_knn_recommendation.py](../tests/test_knn_recommendation.py): 69 tests mới; [DAY7.md](../src/recommendation/DAY7.md): API, protocol, kết quả, Q&A/Day 8.
- 8 outputs mới trong reports/day7: [evaluation.json](day7/evaluation.json), [comparisons.csv](day7/comparisons.csv), [robustness.csv](day7/robustness.csv), [timings.csv](day7/timings.csv), [benchmark.csv](day7/benchmark.csv), [rankings.csv](day7/rankings.csv), [latency.png](day7/latency.png), [summary.md](day7/summary.md).

### Kiểm thử và parity

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day7
```

- Full suite: **178 passed in 20.19s, 0 failed**, exit 0 (109 cũ + 69 mới). Tests có tie thật theo foot-only GK qua ranh giới K, zero vectors, NaN/invalid, filter biên/rỗng, K=1/3/5/50/10000, reference/row-order/repeat invariance và 5 cấu hình Day 6 khác. Vectors/timing fixtures toán học chỉ kiểm công thức/aggregation, không export thành dữ liệu cầu thủ hoặc benchmark giả.
- Runner exit 0: tái lập Top 5 Day 5 và weighted_default Day 6 từ artefact cũ; fit audits KNN/direct bằng nhau. **10/10 cặp full ranking** đạt parity/filter/score/unique/exclude-query/determinism; **50/50 trường hợp K** đạt prefix/parity.
- 8 cặp nonempty overlap@5=1, Spearman full-common≈1; 2 empty null/N/A. Score max absolute difference **0**; max |distance−(1−tổng cosine_components)| **4,440892098500626e-16**; tolerance 1e-11 bao gồm round12.
- Không Precision@K/NDCG@K vì chưa có trustworthy relevance labels; similarity/parity không phải tuyển trạch tốt hơn. Query không tham gia fit scaler/category nhưng chưa có temporal evaluation.

### Benchmark thực đo và quyết định

- Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1, matplotlib 3.11.2. CPU Intel64 Family 6 Model 154 Stepping 4, 12 logical CPUs. Không cài dependency mới; threadpoolctl có sẵn qua sklearn.
- **5 warm-up + 50 measured/method/query**, 2 representations × 5 queries × 2 methods = **1.000 measured calls** và 100 warm-up calls. Không chạy tests/project jobs đồng thời; threadpool_limit=1/NN n_jobs=1, threadpool info lưu trong JSON.
- perf_counter_ns; alternating direct→KNN và KNN→direct theo repeat; cùng K=5 và cùng filtered/nonzero pool. Đo full recommend gồm filters, KNN.fit, retrieval, sort, evidence/explanation. Không gồm constructor/scaler fit, CSV I/O, assertions hoặc output writing.
- p95 = numpy.percentile(method=linear) trên 50 mẫu/nhóm; raw samples lưu repeat/order. Empty không gọi kneighbors, chỉ đo no-results overhead.

Đơn vị dưới là **median / p95 ms**, không phải SLA:

| Query | Day 5 direct | Day 5 KNN | Day 6 direct | Day 6 KNN |
|---|---:|---:|---:|---:|
| Attack | 2.466 / 3.131 | 3.474 / 4.032 | 4.889 / 7.154 | 6.643 / 10.116 |
| Midfield | 4.796 / 6.824 | 6.651 / 9.715 | 4.888 / 6.973 | 6.700 / 9.845 |
| Defender | 5.196 / 7.966 | 6.932 / 10.839 | 5.378 / 7.968 | 7.109 / 10.243 |
| GK | 4.480 / 6.328 | 6.154 / 8.462 | 4.568 / 6.783 | 6.167 / 9.333 |
| Empty | 2.603 / 3.678 | 2.666 / 3.302 | 1.781 / 2.714 | 1.815 / 2.860 |

- KNN median cao hơn direct ở 8/8 nonempty trong phiên đo. **Giữ direct làm phương án hiện hành, KNN làm đối chứng**; chưa có lợi ích quality/tốc độ được chứng minh để thay baseline. Không kết luận KNN luôn chậm trên mọi kiến trúc/dataset; đây là full-request latency gồm chi phí adapter.
- Top 5 weighted KNN khớp Day 6: Kane → Franculino, Luis Suárez, Gianluca Scamacca, Jonathan Burkardt, Tammy Abraham; Vanaken → Ringo Meerveld, Nikola Vlašić, Thijs Oosting, Fabian Rieder, Carlo Holse. Score/evidence/CLB/giá thực có trong JSON; chưa mặc định metadata đúng CLB tại cutoff.
- Artefact: comparisons 10 dòng; robustness 50; timings 1.000; benchmark 20 nhóm; rankings 5.492 dòng. Đã xem latency.png để kiểm nhãn/bố cục; hình biểu diễn timing, không quality.

### Hạn chế, bàn giao và Day 8

- Benchmark một máy/phiên, còn OS/background/CPU jitter; không cold-start, load/concurrency/cloud test hoặc confidence interval. Lấy mọi neighbor là lựa chọn đảm bảo tie parity, chưa tối ưu catalogue lớn/ANN.
- KNN.fit trên filtered vectors không học relevance hoặc refit preprocessing. Adapter phụ thuộc private representation/response contract baseline, cần giữ regression khi sửa sau này. Không bịa defensive/GK metrics.
- Cập nhật AGENTS/CLAUDE, HANDOFF, FILE_INVENTORY, ARCHITECTURE, PROJECT_CONTEXT, SETUP và hai báo cáo; dữ liệu/requirements/manifests cũ không đổi. Source Day 5–7/docs chưa commit; HEAD main vẫn c4d638c, không stage/commit/push/deploy/fetch.
- Day 8 dự kiến hoàn thiện position/age/EUR/minutes và ngưỡng hiệu suất phù hợp dữ liệu thật, input/schema/đơn vị/biên/empty và filter→ranking consistency; không dùng giá làm skill hoặc bàn thắng để đánh giá GK. Chưa triển khai Day 8.
- Máy mới cần source/tests Day 5–7, JSON Day 5 + Day 6 đúng hashes và snapshot ngoài Git; chưa nghiệm thu fresh-install/chuyển máy. Day 5 mốc Git còn chờ nhiệm vụ riêng, mốc kế tiếp Day 10 theo roadmap; lịch không tự cấp quyền thao tác.

### Kiểm tra cuối phiên Day 7

- Độc lập tính lại median/p95 từ 1.000 timing samples theo 20 nhóm: khớp benchmark.csv; 10 comparison checks và 50 robustness checks đều đạt. Source hashes và prior-input hashes trong JSON khớp file thực tế.
- Không link tài liệu hỏng hoặc file thiếu trong inventory. Đã kiểm 12 file mới Day 7; chỉ 9 tài liệu quản lý sẵn có được cập nhật đúng phạm vi.
- Snapshot đầu/cuối cho thấy code/tests/data/artefact Day 5–6, requirements/.gitignore/manifests không đổi; tiền tố lịch sử AGENTS và hai báo cáo giữ nguyên. Git index/HEAD vẫn nguyên, không staged changes. git diff --check không báo lỗi whitespace (có cảnh báo LF→CRLF của AGENTS).

## 2026-11-02 — Bổ sung hệ thống thuyết trình và bảo vệ (sau Day 7)

### Phạm vi và đối chiếu

- Nhiệm vụ chỉ thiết lập tài liệu, không làm Day 8 hoặc thay thuật toán. Đọc hướng dẫn, CLAUDE/HANDOFF/inventory, nhật ký/insights, source collection/preprocessing/EDA/features/recommendation/tests, báo cáo thực nghiệm và Git local.
- Tạo [PRESENTATION_AND_DEFENSE.md](PRESENTATION_AND_DEFENSE.md): tổng hợp Day 1–7; mỗi Day có mục tiêu/công việc, file/chức năng/input-output, công thức/lý do, kết quả dẫn nguồn, khó khăn/cách giải quyết, hạn chế và 4 Q&A (28 cặp tổng cộng). Phân biệt đối chiếu artefact, lịch sử chạy, giả thuyết, kế hoạch; có hướng dẫn dùng khi thuyết trình và quy trình bổ sung Day mới.
- Số liệu lấy từ day1_data_quality, bảng EDA, day4_feature_quality, báo cáo Day 5 và CSV/JSON Day 6–7; không chạy lại downloader/cleaning/EDA/features/runners để viết tài liệu. Số tests 23/57/109/178 và thời gian là kết quả các lần chạy trong lịch sử, không là lượt pytest mới.
- Git log --name-only xác nhận Day 1 ở 86c0360, Day 4 ở 266f90f, Day 2–3 ở c4d638c; giữ nguyên thứ tự commit. Day 5–7 có code/artefact local nhưng chưa commit. Git main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1, origin cấu hình đúng URL ScoutIQ-AI; không fetch/xác minh remote trực tiếp, không staged diff khi bắt đầu.
- Cập nhật AGENTS.md và CLAUDE.md: bắt buộc cập nhật PRESENTATION_AND_DEFENSE cùng project_log, insights_and_defense và HANDOFF sau mỗi Day, đủ 3–5 Q&A, link tương đối và mức độ bằng chứng. Cập nhật HANDOFF và FILE_INVENTORY để AI mới tìm được hồ sơ; giữ nguyên trạng thái Day 7/Day 8 chưa triển khai.

### Kiểm tra và giới hạn

- Kiểm tra tài liệu bằng đọc/diff, đường dẫn tương đối, cấu trúc bảy Day và 28 Q&A; đối chiếu số liệu với CSV/JSON và code. So snapshot trước/sau để bảo vệ source/tests/data/artefact thực nghiệm, manifests và Git index; kết quả kiểm tra cuối được ghi tiếp dưới đây.
- Không chạy pytest trong phiên tài liệu; kết quả gần nhất được nhật ký Day 7 ghi nhận là 178 passed, 0 failed trong 20,19 s. Không tạo test hoặc kết quả Data Science mới.
- Blockers chuyển máy vẫn còn: source/docs chưa commit, snapshot data ngoài Git, chưa nghiệm thu fresh clone/install trên máy đích. Không upload data/secrets, không stage/commit/push/deploy.
- Bước tiếp theo: dùng hồ sơ khi chuẩn bị trình bày; sau mỗi Day bổ sung bằng chứng/Q&A đồng bộ. Day 8 và các mốc Git chỉ thực hiện khi có nhiệm vụ/quyền tương ứng.

### Kết quả kiểm tra cuối phiên tài liệu

- Kiểm tra bằng Python stdlib đọc file/CSV/JSON, không import hoặc chạy pipeline: đủ 7 Day, mỗi Day 4 Q&A; 219 liên kết tương đối trong 7 tài liệu đều trỏ tới file có thật. Các shape dataset, số ID, ngưỡng phút, số cột mới, mean overlap và counts/parity/timing Day 6–7 khớp nguồn đã nêu.
- So SHA-256 với snapshot đầu phiên: chỉ 6 tài liệu cũ thay đổi và thêm PRESENTATION_AND_DEFENSE.md; 68 file còn lại không đổi, gồm source/tests/data/artefact thực nghiệm, requirements/.gitignore/manifests và Git index. Tiền tố lịch sử AGENTS, project_log, insights và inventory được giữ nguyên khi bổ sung.
- git diff --check không báo lỗi whitespace; có cảnh báo cấu hình LF→CRLF của AGENTS, không phải lỗi kiểm tra. HEAD vẫn c4d638c2d10c542c897ccf95dedde540814925b1, không staged diff. Không chạy pytest, không stage/commit/push/deploy.

## 2026-11-02 — Day 8: Advanced Filtering & Search Constraints

### Trạng thái, baseline và file

- **Đã hoàn thành có bằng chứng trong phạm vi Day 8**; chưa làm Day 9. Đọc AGENTS/CLAUDE/HANDOFF/ARCHITECTURE/inventory/log/insights/PRESENTATION_AND_DEFENSE và code/tests Day 5–7 trước sửa.
- Git đầu phiên main/c4d638c2d10c542c897ccf95dedde540814925b1, AGENTS/log/insights modified và source/tests/docs/reports Day 5–7 untracked; không staged. Snapshot trước sửa ghi hash 75 file liên quan, không xóa/ghi đè thay đổi sẵn có.
- Baseline test bằng .venv: **178 passed in 26.39s**, exit 0. Không chạy lại pipeline/runner cũ ghi đè.
- Tạo [constraints.py](../src/recommendation/constraints.py): SearchConstraints chứa SearchFilters, parse budget unit nghiêm, hard mask/audit, AdvancedRecommender bọc nguyên cosine/weighted/KNN. Tạo [run_day8.py](../src/recommendation/run_day8.py), [DAY8.md](../src/recommendation/DAY8.md), [test_advanced_constraints.py](../tests/test_advanced_constraints.py).
- Tạo reports/day8: [evaluation.json](day8/evaluation.json), [scenarios.csv](day8/scenarios.csv) 20 dòng, [filter_stages.csv](day8/filter_stages.csv) 164 dòng, [top5.csv](day8/top5.csv) 80 dòng, [rankings.csv](day8/rankings.csv) 692 dòng, [summary.md](day8/summary.md). Bảng trước/sau đủ thể hiện 5 tình huống nên không thêm biểu đồ trùng thông tin.

### Thiết kế và dữ liệu

- Features 4.112×28, SHA-256 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0, mùa 2025/26/cutoff 2026-06-12. Fit 4.108, loại 4 query IDs 132098/137576/139208/629773; không temporal split. Không đổi feature/scaler/weights, fit IDs hoặc dataset.
- Hard AND giữa position, tuổi, budget EUR, min phút, roles (OR trong danh sách), g90/a90, hard foot, excluded club IDs; mọi biên numeric inclusive. Query chỉ là tham chiếu, không bắt buộc thỏa điều kiện ứng viên.
- from_request chấp nhận max_budget_eur hoặc budget_value+budget_unit EUR/EUR_million, không cả hai; triệu EUR nhân 1e6 rõ ràng. Từ chối typo/unknown field, âm, NaN/infinity/overflow, bool/string giả số, min>max, role không đúng position, club ID lạ/trùng. Không đoán 5 EUR thành 5 triệu.
- Hard foot so left/right/both chính xác, missing không đạt; club missing không chứng minh ngoài exclusion nên bị loại khi active. Không impute. Soft foot giữ nonmatch/missing, chỉ phá hòa cosine round12, sau đó ID; không cộng skill score. GK từ chối g90/a90 threshold, Defender nếu dùng chỉ là chỉ số tấn công.
- Lọc trên catalogue rồi tạo request-local view của encoded matrices đã fit, giữ query vector; gọi nguyên engine để ranking. Không refit scaler hoặc mutate engine. Full ranking phục vụ soft tie ở boundary K. Adapter truy cập private representation, có regression bảo vệ; source/API cũ không thay đổi.

### Thực nghiệm và kiểm thử

Lệnh đã chạy:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day8
```

- Suite đầu sau thêm tests có **1 collection error** vì parametrization tên request trùng fixture dành riêng pytest. Đổi tên thành payload; không nới assertion hoặc sửa thuật toán để che lỗi.
- Suite cuối **338 passed in 34.89s, 0 failed**, exit 0 = 178 cũ + 160 mới. Kiểm validation/unit/missing, biên/tổ hợp, 4 engines, legacy/full-score regression, Top K/rỗng/zero, pool trước KNN, soft ties thật qua boundary/đảo dòng, engine/input không đổi và không fit scaler khi search. Biến thể lỗi/missing chỉ trong RAM, không xuất cầu thủ giả.
- Runner exit 0: 20/20 legacy checks và 20/20 scenario–engine cases đạt, direct/KNN cùng representation khớp full ranking. Row-wise oracle độc lập kiểm pool; tests đối chiếu ranking cũ giao hard pool, score không đổi. Empty filter checks vacuous, không relevance metrics.
- Môi trường: Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1. Không cài dependency mới, không benchmark latency Day 8. JSON ghi hash/source/env/reference/config/query và HEAD.

| Scenario | Constraints chính (thêm position/role) | Position trước → hard pool | Trả K |
|---|---|---:|---:|
| Tiền đạo trẻ / Kane | Centre-Forward; 18–23; ≤5M EUR; ≥1200 phút; g90≥.3; loại club 27; soft left | 1059 → 22 | 5 |
| Tiền vệ kiến tạo / Vanaken | Attacking Midfield; 20–29; ≤10M; ≥1200 phút; a90≥.15; hard left; loại 2282 | 1204 → 10 | 5 |
| Hậu vệ kinh nghiệm / Van Dijk | Centre-Back; 28–35; ≤5M; ≥2000 phút; hard right; loại 31 | 1523 → 94 | 5 |
| GK ngân sách / Hornicek | Goalkeeper; 20–30; ≤3M; ≥1800 phút; hard right; loại 1075 | 326 → 47 | 5 |
| No-results / Kane | Centre-Forward; 18–23; 0 EUR; ≥1200 phút; g90≥.3; hard left | 1059 → 0 | 0 |

Catalogue trước mọi lọc 4.112; position count gồm query, audit có bước self-exclusion riêng. Pools giống cả bốn engine, tất cả nonempty còn rankable. Top 5 weighted với CLB/tuổi/giá/score/evidence có trong summary/JSON/CSV; đây là config Day 6 giả thuyết, không được chọn là tốt nhất.

### Quyết định, hạn chế và bàn giao

- Giữ direct là phương án hiện hành theo Day 7; Day 8 mở rộng constraints tương thích cả bốn đường chạy. Soft foot chỉ ưu tiên khi hòa, không là preference model đã học.
- Metadata CLB chưa kiểm toán tại cutoff; 24 foot missing giữ nguyên. Chính sách hard fail-closed có thể loại người vì thiếu metadata; phải nêu rõ. Chưa có nhãn relevance/temporal evaluation, không Precision/NDCG. Defender/GK context_profile_only; market value không skill hoặc phí chuyển nhượng.
- Chưa đo overhead adapter/full ranking hoặc concurrency/cloud, chưa nghiệm thu fresh-install/chuyển máy. Source Day 5–8/docs chưa commit; data ngoài Git, cần đúng snapshot/prior JSON/hash.
- Cập nhật AGENTS/CLAUDE, project_log/insights/PRESENTATION_AND_DEFENSE, HANDOFF/FILE_INVENTORY/ARCHITECTURE/SETUP/PROJECT_CONTEXT. Day 9 dự kiến explanation truy vết và dữ liệu so sánh thống nhất đơn vị/cutoff, ties/đảo dòng/nhóm ít phân biệt; UI charts vẫn Day 21.
- Không stage/commit/push/deploy/fetch. Theo yêu cầu người dùng để commit khi chuyển máy, không tự thực hiện mốc Git trong phiên này. Kết quả kiểm tra bảo toàn/links cuối phiên ghi tiếp bên dưới.

### Rà soát điều kiện biên và kiểm tra cuối Day 8

- Lượt 338 passed in 34.89s ở trên là kết quả trước đợt rà soát cuối. Phát hiện từ code: K nội bộ để lấy full ranking tính cả zero candidates, có thể tạo cảnh báo thiếu K dù số kết quả người dùng yêu cầu vẫn đủ. Đổi K nội bộ sang số rankable, bổ sung assertion với cosine/KNN trong test zero-vector hiện có; không thay score/filters/feature.
- Chạy lại toàn suite bằng cùng lệnh: **338 passed in 44.83s, 0 failed**, exit 0. Đây là kết quả hiện hành. Không suy tốc độ search từ thời gian suite; runner không benchmark latency Day 8.
- Chạy lại `python -B -m src.recommendation.run_day8 --output-dir reports/day8_verified`: exit 0, 20 legacy checks + 20 scenario–engine cases vẫn đạt. Đối chiếu 4 CSV/summary và toàn response với lần đầu: giống nhau. Chỉ sau khi xác nhận hash các output do chính phiên Day 8 vừa tạo không bị sửa bên ngoài, chuyển output cuối về reports/day8 và bỏ directory tạm rỗng; JSON ghi source hashes/thời điểm lần cuối. Không thay artefact Day 5–7, không cung cấp tùy chọn overwrite trong runner.
- Kiểm độc lập 692 dòng rankings.csv: tất cả thỏa hard constraints; counts CSV 20/164/80/692 khớp JSON. 9 source hashes và 4 input hashes trong JSON khớp file thực tế. Tám mục Day trong PRESENTATION_AND_DEFENSE có 4 Q&A mỗi Day (32 cặp).
- Snapshot đầu/cuối: 10 file mới, chỉ 10 tài liệu quản lý cũ được cập nhật; 65 file còn lại giữ nguyên hash, bao gồm source/tests/data/artefact cũ, requirements/.gitignore/manifests và Git index. Tiền tố lịch sử AGENTS/project_log/insights/inventory giữ nguyên. Không có dữ liệu cầu thủ giả hoặc API key/mật khẩu được thêm.
- Kiểm 286 liên kết tương đối: không link hỏng; UTF-8 và whitespace tài liệu đạt. git diff --check không báo lỗi (chỉ cảnh báo LF→CRLF của AGENTS). HEAD vẫn c4d638c2d10c542c897ccf95dedde540814925b1, branch main; không staged changes, không commit/push/deploy/fetch.

## 2026-11-02 — Day 9: Recommendation Explainability & Player Comparison

**Trạng thái: Đã hoàn thành có bằng chứng trong phạm vi local được giao. Day 10 chưa triển khai.** Đã đọc hướng dẫn, HANDOFF/ARCHITECTURE/log/insights/PRESENTATION_AND_DEFENSE và review code/tests Day 5–8 trước thay đổi. Giữ nguyên ranking, feature selection, scaler/reference, eligibility, hard/soft filters và API cũ; không bắt đầu dịch vụ/API/UI/chat.

### File, đầu vào và thiết kế

- [comparison.py](../src/recommendation/comparison.py): catalogue thật → identity/missing/unit và so sánh 2–5 ID hợp lệ; delta có dấu, tuyệt đối và tương đối, xử lý 0/missing. Attack/Midfield cùng nhóm có g90/a90; Defender/GK/nhóm lẫn chỉ bối cảnh, không kết luận tổng thể.
- [explainability.py](../src/recommendation/explainability.py): bọc fitted engine, giữ nguyên response, thêm evidence tách text rule-based. Feature raw/weight/cosine components/reference differences, hard constraints required/observed/passed, soft preference và missing. Kiểm tổng components, JSON hữu hạn; explain_response đối chiếu chính xác response với engine/request trước khi giải thích.
- [run_day9.py](../src/recommendation/run_day9.py), [DAY9.md](../src/recommendation/DAY9.md), [115 tests mới](../tests/test_explainability.py). Runner tái dùng SCENARIOS/make_engines Day 8; output-dir phải mới.
- Bảy outputs: [evaluation.json](day9/evaluation.json), [checks.csv](day9/checks.csv), [top5.csv](day9/top5.csv), [feature_evidence.csv](day9/feature_evidence.csv), [comparisons.csv](day9/comparisons.csv), [attack_comparison.png](day9/attack_comparison.png), [summary.md](day9/summary.md). CSV lần lượt 20/80/260/448 dòng; JSON có 20 cases, 80 explanations, 32 comparison groups. Biểu đồ đã xem kiểm nhãn/đơn vị/bố cục.
- Features 4.112×28, SHA-256 `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`; season 2025/26, cutoff 2026-06-12. Fit 4.108 ID loại queries 132098/137576/139208/629773 như Day 8. Đầu vào thêm reports/day8/evaluation.json; runner kiểm 9 source hashes cũ, ghi 12 source hashes hiện hành/2 input hashes. Không tái chạy pipeline ghi dataset.

### Kiểm thử và thực nghiệm trực tiếp

Lệnh: `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`.

- Baseline trước sửa: **338 passed in 47.81s**, exit 0.
- Lượt mới đầu: **452 passed, 1 failed in 81.33s**, exit 1. Test infinity bị pandas 3 chặn gán vào int64 trước khi tới validator; sửa dtype fixture sang float, giữ assertion validator phải từ chối infinity. Không đổi dữ liệu thật hoặc nới validation.
- Lượt cuối: **453 passed in 59.76s, 0 failed**, exit 0 (338 cũ + 115 mới). Kiểm regression bốn engines/legacy API, rank/ID/score/NaN/inf/units tampering, 2–5 người, zero denominator, missing thật, zero query, ablation, không refit/mutate và permutation.
- `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day9`: exit 0. **20/20 response khớp nguyên Day 8**, gồm scores/ranks/pools/status/constraints/evidence cũ. Audits fit và input hashes không đổi. Không benchmark latency hoặc tính Precision/NDCG.
- Windows 11 (10.0.26300), Python 3.13.7, numpy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1; không cài dependencies hoặc gọi API.

| Kịch bản Day 8 / reference | Pool hard | K trả mỗi engine | Weighted top 1 / score |
|---|---:|---:|---|
| Tiền đạo trẻ, ngân sách thấp / Kane | 22 | 5 | Barney Stewart / 0.956332 |
| Tiền vệ kiến tạo / Vanaken | 10 | 5 | Jeppe Erenbjerg / 0.922962 |
| Hậu vệ kinh nghiệm / Van Dijk | 94 | 5 | Brandon Mechele / 0.999090 |
| GK trong ngân sách / Hornicek | 47 | 5 | Elías Ólafsson / 0.863745 |
| No-results / Kane | 0 | 0 | Không có; explanation/comparison rỗng |

Top 5 và text cho cả năm kịch bản weighted nằm trong summary; JSON/CSV có đủ bốn engines. Reference + Top 4 là nhóm 5 người; reference + ứng viên hạng 5 là nhóm 2 người, bao phủ cả shortlist. So sánh giữ đơn vị gốc, không xếp hạng mới. Difference = candidate − reference; absolute = abs(difference); relative = 100×difference/abs(reference), null nếu 0/missing. Null không đổi thành 0.

### Quyết định, bằng chứng, giới hạn và bàn giao

- Barney Stewart so Kane: g90 0.6293706294 so 1.2661439114, delta −0.6367732821, relative −50.29233062%, dù weighted cosine 0.956331763076. Tương đồng góc vector không có nghĩa bằng sản lượng hoặc chất lượng. Không gọi relative là tỷ lệ kém kỹ năng.
- Maswanhise thiếu foot thật, evidence giữ null, vẫn hợp lệ vì soft foot chỉ phá hòa; không bịa chân thuận. Components chỉ giải thích phép tính hình học, không nguyên nhân hoặc % kỹ năng. Giá trị thị trường chỉ hiển thị/so bối cảnh/ngân sách.
- Chưa có relevance labels/temporal validation/league adjustment, kỹ năng Defender/GK, đánh giá hữu ích explanation bởi scouts; chưa benchmark overhead. Adapter dùng private catalogue/representation, cần regression khi internals đổi. JSON chưa là FastAPI/Pydantic service contract, chưa có auth/privacy/API/chat.
- Cập nhật AGENTS/CLAUDE, ba báo cáo quản lý, HANDOFF/FILE_INVENTORY/ARCHITECTURE/SETUP/PROJECT_CONTEXT. Day 10 dự kiến tích hợp engine thành dịch vụ Python dùng lại, ổn định cấu hình/pipeline và test hồi quy, chốt phiên bản ứng viên để đánh giá; chưa triển khai.
- Git main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1, source Day 5–9/docs chưa commit; giữ index/thay đổi cũ. Không commit/push/deploy/fetch. Chuyển máy còn cần source, prior JSON và 8 dataset ngoài Git; fresh-install chưa nghiệm thu. Mốc Day 10 chỉ đề xuất khi được phép, theo yêu cầu để commit khi chuyển máy.

### Kiểm tra cuối Day 9

- Snapshot đầu/cuối: 12 file mới; đúng 10 tài liệu cũ cập nhật; 75 file cũ khác giữ nguyên SHA-256, gồm source/tests/data/artefact cũ, requirements/.gitignore/manifests và Git index. Tiền tố lịch sử AGENTS/project_log/insights/inventory được đối chiếu nguyên vẹn.
- 350 liên kết tương đối của tài liệu cập nhật/DAY9/summary đều tồn tại; UTF-8 hợp lệ, không replacement characters. PRESENTATION_AND_DEFENSE có 9 mục Day, mỗi Day 4 Q&A (36 cặp). Đã xem PNG để kiểm nhãn/bố cục/đơn vị.
- Script đối chiếu độc lập đọc lại CSV nguồn: 80 explanations có đúng identity/reference/feature values, ID/rank/score; 448 numeric differences khớp raw values/công thức; 20 response nguyên khớp Day 8; CSV counts 20/80/260/448. 12 source hashes + 2 input hashes khớp, JSON hữu hạn; lượt cuối exit 0. Hai lỗi của script kiểm tra tạm đã sửa: giữ cột player_id khi set_index (drop=False), và tránh in tên Unicode không hỗ trợ bởi console cp1258. Không phải lỗi module hoặc dữ liệu, không thay file sản phẩm để xử lý.
- git diff --check đạt (chỉ cảnh báo LF→CRLF của AGENTS); không staged diff; branch main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1 giữ nguyên. Không stage/commit/push/deploy/fetch, không triển khai Day 10.

## 2026-11-02 — Day 10: Recommendation Engine Integration & Phase Review

**Trạng thái: Đã hoàn thành có bằng chứng trong phạm vi local; Day 11 chưa triển khai.** Đọc AGENTS/CLAUDE/HANDOFF/ARCHITECTURE/PROJECT_CONTEXT, log/insights/PRESENTATION_AND_DEFENSE, review code/tests Day 5–9 trước sửa. Không refactor engine cũ hoặc thay feature/scaler/eligibility/weights/ranking.

### File, kiến trúc và contract

- [config.py](../src/recommendation/config.py): ProjectPaths từ module/root được truyền, không hardcode Windows; ServiceConfig default cosine/K=5, weights Day 6 được validate/copy phía server, không nhận user weights hoặc tự tune.
- [schemas.py](../src/recommendation/schemas.py): Draft 2020-12 request/response schemas, strict native JSON/finite/duplicate-key checks và cross-field metadata/ID/score/rank/filter/unit/component/text/comparison checks. Legacy payload có vùng extension để giữ API; chưa HTTP/Pydantic contract.
- [service.py](../src/recommendation/service.py): một snapshot/config, khởi tạo bốn engines; parse request → hard filters → ranking/Top K → Day 9 structured explanation → optional groups 2–5 người → response validation. Giữ nguyên response cũ trong explanation.recommendation. Không refit scaler/request-result cache/API/network.
- [run_day10.py](../src/recommendation/run_day10.py), [DAY10.md](../src/recommendation/DAY10.md), [tests/test_service.py](../tests/test_service.py). requirements.txt thêm jsonschema>=4.18,<5, giữ UTF-16/nội dung cũ; 4.26.0 có sẵn nên không cài mới. Kiểm môi trường thấy Pydantic chưa cài, không dùng hoặc thêm dependency này.
- [reports/day10](day10/summary.md): evaluation.json; request.schema.json; response.schema.json; checks.csv (20); top5.csv (80); timings.csv (400); benchmark.csv (20); summary.md; [phase_review.md](day10/phase_review.md) tổng kết Day 5–10. Không tạo biểu đồ mới vì bảng đủ trình bày protocol/median/p95; dữ liệu mẫu raw được giữ.

Response `scoutiq.service.v1` có request được áp dụng defaults; metadata method/normalized filters/candidate_count/rankable_count/returned_count/top_k/dataset/version/configuration_id/limitations; nguyên envelope Day 9 và optional comparisons. Candidate count qua hard (loại query) có thể chứa zero vectors; rankable trừ chúng; zero reference có thể trả 0 dù rankable>0. No-results giữ constraints, không fake row. Compare chia reference + mỗi block tối đa 4 kết quả, đủ shortlist. Default comparison=false.

Dataset 4.112×28, Transfermarkt 2025/26 cutoff 2026-06-12, CSV SHA-256 `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`. Fit 4.108 IDs như Day 9, loại 4 queries; không temporal split. Service ghi content hash bảng sort ID và hash bytes CSV khi từ file, configuration hash từ config/audit/data; không coi hash config là Git commit. Runner kiểm 12 source hashes cũ trước chạy; JSON lưu 16 source hashes hiện hành/3 prior input hashes/fit IDs/config/env/HEAD.

### Kiểm thử trực tiếp

Lệnh: `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`.

- Baseline đầu phiên **453 passed in 58.18s**, exit 0. Tests mới riêng **96 passed in 19.35s**. Toàn suite **549 passed in 62.01s, 0 failed**, exit 0 (453 cũ + 96 mới). Không có test fail trong các lượt này. Sau suite chỉ sửa link phase review trong runner cho output-dir khác, không đổi pipeline; runner cuối chạy exit 0 và ghi hash source cuối.
- Kiểm API/JSON/defaults/unit conversion/unknown fields, ID/K/NaN/Inf/duplicate JSON keys, config isolation, no-refit/no-mutation, permutation, zero reference/zero candidates, K=1/3/5/10000, nhóm comparison, tampered response và latency summary math. Tests dùng snapshot thật, biến thể lỗi trong RAM; không tạo cầu thủ giả/ghi dataset.
- `pip check`: No broken requirements found. Windows 11/Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1, jsonschema 4.26.0, threadpoolctl 3.7.0. Không cài môi trường sạch hoặc chuyển máy trong phiên.
- Runner `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day10` exit 0: **20/20 full responses Day 8 + envelopes/comparisons Day 9 khớp**, 80 Top 5 rows, pools 22/10/94/47/0, returned 5/5/5/5/0. Đối chiếu mạnh hơn chỉ IDs/score; không thay algorithm/weights hoặc đánh giá quality từ parity.

### Latency và reproducibility

- Đo recommend_json gồm parse/validation, hard filters/ranking, Top K, explanation/text, comparison=true, response validation và serialization; không CSV I/O/khởi tạo/fit/network/HTTP/auth. 3 warm-up + 20 đo × 20 cases = 60 warm-up/400 measured calls; rotate thứ tự cases, threadpool limit=1; không chạy pytest đồng thời. JSON mọi lần giống đối chứng; fit audits/input hashes giữ nguyên.
- Mỗi nonempty case median 74,381–141,391 ms; p95 102,959–193,290 ms. Empty median 24,718–32,357 ms; p95 43,127–55,904 ms. Đây là khoảng của 16/4 nhóm tương ứng, không percentile gộp. Bảng đầy đủ tại [benchmark.csv](day10/benchmark.csv)/phase review; p95 tính numpy linear.
- Startup một quan sát 1.423,006 ms, không median/p95 startup. Chỉ 20 mẫu/case, outliers và tải nền chưa kiểm soát đầy đủ; không cam kết cloud SLA/throughput hoặc suy module overhead riêng. Day 7 đo phạm vi khác, không so trực tiếp thời gian giữa hai Day. Không dùng latency để chứng minh model/scouting quality.

### Phase review, giới hạn và bước tiếp theo

- [Phase review](day10/phase_review.md) phân biệt bằng chứng lịch sử từng Day 5–9 và kiểm chứng mới Day 10. Chốt **ứng viên tích hợp local v1** để đánh giá chính thức; không chọn trọng số tối ưu/production release. Bốn methods giữ cùng feature/reference/filters; default direct cosine tiếp tục, weighted là giả thuyết, KNN đối chứng.
- Chưa relevance labels/expert review, temporal/metadata-at-cutoff audit, league/tactical/uncertainty adjustment hoặc skill Defender/GK. Market value không skill/phí mua, similarity không probability; không Precision/NDCG thiếu nhãn.
- Private adapters và full ranking/bốn engine trong RAM cần regression/đánh giá tài nguyên khi scale. JSON Schema legacy extensions/runtime strict integer cần giữ khi tích hợp FastAPI. Chưa auth/privacy/HTTP/DB/UI/OpenAI/cloud/concurrency. Source/schema version và môi trường phải đi cùng hash khi tái lập; canonical content/audit hash chưa bảo đảm xuyên mọi phiên bản pandas/numeric backend.
- **Day 11 dự kiến:** protocol/rubric/tình huống có nguồn, baseline/coverage/filter correctness/stability/latency, rà leakage/split khả thi. Chỉ relevance metrics khi có nhãn đáng tin; không dùng market value làm ground truth. Chưa thực hiện Day 11.
- Cập nhật đầy đủ 10 tài liệu quản lý/handoff và requirement khai báo; giữ main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1/index/thay đổi cũ. Không stage/commit/push/deploy/fetch. Source Day 5–10/docs chưa commit, clone HEAD thiếu công việc mới; bàn giao data ngoài Git/fresh-install chưa nghiệm thu. Mốc Day 10 chờ người dùng quyết định khi chuyển máy.

### Kiểm tra cuối Day 10

- Snapshot đầu/cuối: **15 file mới**, chỉ **10 tài liệu cũ + requirements.txt** thay đổi; **86 file cũ còn lại giữ nguyên SHA-256**, gồm source/tests/data/artefact Day 5–9, manifests/.gitignore và Git index. Prefix lịch sử AGENTS/log/insights/inventory giữ nguyên. Requirements giữ nguyên toàn bytes cũ, chỉ thêm CRLF phân cách cuối file và dòng jsonschema; kiểm tra tạm ban đầu giả định file đã có newline nên assertion chưa đúng, đã đối chiếu prefix thực và xác nhận bảo toàn, không sửa lại nội dung cũ.
- **445 liên kết tương đối** hợp lệ, UTF-8 tài liệu không có replacement character. PRESENTATION_AND_DEFENSE có 10 Day × 4 Q&A = 40 cặp; phase review riêng có 4 Q&A. Không xóa lịch sử hoặc tự đánh dấu Day 11 hoàn thành.
- Đối chiếu độc lập JSON/CSV: 20 schema/semantic checks và full Day 8–9 response/comparison parity đạt; 16 source hashes/3 input hashes khớp; schema export đúng definitions code; JSON hữu hạn. Counts CSV checks/Top5/timings/benchmark=20/80/400/20. Tính lại median/p95 từ 20 mẫu/case khớp benchmark trong sai số 1e-10; repeat indices đủ 0–19. Script kiểm cuối exit 0.
- git diff --check đạt (chỉ cảnh báo LF→CRLF AGENTS); không staged diff; branch main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1 giữ nguyên. Không commit/push/deploy/fetch hoặc triển khai Day 11.


<!-- DAY11_APPEND_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Day 11 — Recommendation Evaluation Protocol & Relevance Assessment (2026-11-03)

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

**Day cuối: Day 11 — hoàn thành protocol, công cụ đánh giá và audit local; chưa có relevance labels độc lập. Day 12 chưa triển khai.** Không coi hoàn thành protocol là đã xác nhận chất lượng tuyển trạch. Engine/scaler/weights/eligibility Day 5–10 giữ nguyên. Bốn demo có 22/10/94/47 ứng viên, 173 hàng unlabeled; 16/16 full responses khớp Day 10 và repeat/filter đúng. P@K/Recall@K/NDCG@K thực đều null. SYNTHETIC chỉ kiểm công thức. Kết quả test cuối phiên xem reports/day11/validation.json.

### Thực hiện và bằng chứng mới

- Đọc AGENTS/CLAUDE/docs/logs/phase review/code/tests Day 5–10; kiểm Git trước sửa. Baseline chạy mới **549 passed, 0 failed, 83,95s**. Nhánh main, HEAD c4d638c; không stage/commit/push/deploy/fetch. Bảo toàn thay đổi cũ/index.
- Thêm src/evaluation (__init__, metrics, audit, run_day11), tests/test_evaluation_protocol.py; reports/day11 có protocol/rubric, 173-row unlabeled template, evidence packet, audit JSON/findings, evaluation JSON, synthetic math, summary/run_summary/validation. FILE_INVENTORY liệt kê I/O/dependencies đầy đủ. Không đổi requirements hoặc code/data/artefact engine cũ.
- P@K chỉ khi returned Top K có grade; Recall/NDCG cần full eligible labels; score/gain/denominator/empty/tie được công bố. Missing grade không 0. 64 tests mới ban đầu đạt; toàn suite giai đoạn đó 613 passed/0 failed/111,68s. Sau đó bổ sung 6 checks artefact/provenance; kết quả suite cuối lưu [validation.json](day11/validation.json), không lấy con số cũ làm con số cuối.
- Runner `.venv\Scripts\python.exe -B -m src.evaluation.run_day11` chạy thành công: 16/16 full response Day 10 parity + repeat/hard filters, 173 unlabeled rows, pools22/10/94/47, source/data hashes/môi trường/fit IDs được ghi. Không tái chạy timing Day 10. Relevance thực null; synthetic P@3=2/3,R@3=1,NDCG@3≈0,692020 chỉ toán học.
- Audit chỉ đọc raw xác nhận 4.112×28, 0 aggregation mismatch, valuation/date match; 4.198 integrated dưới 900 phút, retention theo vị trí khác nhau. Metadata temporal chưa xác minh; mixed competitions chưa normalize. Phát hiện 1 tuổi lệch lịch (341429,29→30), ghi [audit_findings](day11/audit_findings.md); không sửa để bảo toàn engine/snapshot.
- Cập nhật đồng bộ 10 docs scope/roadmap/handoff. Chuẩn relevance/annotation cần independent human; thiếu người/nhãn là blocker cho quality, không cho phép tự điền. Defender/GK chỉ context. Gemini không ranking/label; Neon dùng chung vẫn phải session isolation; auth/sync future.

### Lộ trình 31 ngày thay thế phân công Day 11–31 cũ

| Day | Công việc / đầu ra và điều kiện nghiệm thu | Trạng thái |
|---|---|---|
| 1–10 | Giữ lịch sử collection → feature → engine/service/phase review; không thay artefact hoặc thuật toán | Đã có bằng chứng local |
| 11 | Protocol/rubric 0–3, annotation mẫu, audit, metrics có gate, tests | Hoàn thành công cụ; relevance thật chưa có |
| 12 | Review/pilot annotation với assessor độc lập nếu có; evidence/coverage/provenance và kế hoạch xử lý thiếu dữ liệu/tuổi boundary | Kế hoạch, chưa chấm thay người |
| 13 | Đánh giá có nhãn nếu đủ; phân tích vị trí/bias/split; nếu thiếu nhãn công bố giới hạn và đóng băng baseline có version | Kế hoạch, không tự tối ưu weights |
| 14 | FastAPI local bọc service/schema, errors/config/health; parity request–response | Kế hoạch |
| 15 | Neon PostgreSQL: schema/migration cho anonymous sessions, search_history, recommendation_results; quan hệ sở hữu và retention | Kế hoạch; mốc Git cần phép |
| 16 | API lưu/đọc/xóa lịch sử bằng browser session token; kiểm isolation, validation, không lộ DB credentials | Kế hoạch |
| 17 | Backend+DB integration, lỗi kết nối, secret/config/log redaction, rate-limit/quota design; local nghiệm thu | Kế hoạch |
| 18 | Streamlit forms và trạng thái loading/error/no-results; đơn vị EUR/cutoff rõ | Kế hoạch |
| 19 | UI Top 3–5, structured evidence, comparison 2–5 và biểu đồ đúng đơn vị/phạm vi | Kế hoạch |
| 20 | Lịch sử theo browser, xóa lịch sử/reset session, caveat mất token; UI/API tests | Kế hoạch; mốc Git cần phép |
| 21 | Gemini request interpretation → schema → validation; không tự filter/rank ngoài Python engine | Kế hoạch |
| 22 | Gemini giải thích từ evidence, nguồn/uncertainty; nếu lưu hội thoại thì chat_sessions/chat_messages thuộc anonymous session | Kế hoạch |
| 23 | Tích hợp UI/API/Gemini: prompt injection, hallucination, lỗi/quota/fallback, privacy và tests | Kế hoạch |
| 24 | Integration tests toàn luồng, isolation browser A/B, no-results và failure paths | Kế hoạch |
| 25 | Cấu hình cloud/secrets/migration/backup/runbook; staging deploy chỉ khi được phép | Kế hoạch; mốc Git cần phép |
| 26 | Cloud smoke/integration/performance theo tải thực được phép; nếu chưa deploy thì ghi bị chặn phần cloud | Kế hoạch |
| 27 | Hardening, regression, data retention/restore, vận hành/demo rehearsal | Kế hoạch |
| 28 | Final report: dữ liệu/phương pháp/protocol/bằng chứng/giới hạn, phân biệt synthetic và human | Kế hoạch |
| 29 | Slides, biểu đồ có nguồn, script demo và Q&A | Kế hoạch |
| 30 | Kiểm báo cáo/slides/demo, fresh-machine handoff và full regression | Kế hoạch; mốc Git cần phép |
| 31 | Nghiệm thu final, demo, release notes/handoff; commit/tag/release/push khi có phép riêng | Kế hoạch |

Day là thứ tự công việc, không phải ngày lịch. Mốc Git giữ Day 5, 10, 15, 20, 25, 30 và final 31; không cấp quyền tự commit/push/deploy. Ngày nào thiếu assessor, dữ liệu hoặc hạ tầng thì ghi rõ phần bị chặn, không tự tạo bằng chứng. Không đưa authentication trở lại critical path MVP; dành phần riêng Future Development.

### Giới hạn và bước tiếp

Day 11 hoàn tất protocol/công cụ/audit, không phải đã đo relevance thực hoặc nghiệm thu sản phẩm web. Day 12 chỉ là kế hoạch pilot/review annotation, provenance/coverage/split, xử lý age issue có version khi được giao. Chưa có fresh-machine install, source Day 5–11 chưa commit, data ignored cần bàn giao riêng. Mốc Git tiếp theo cần quyền riêng; không sửa lịch sử commit trước đó.

<!-- DAY11_APPEND_END -->

<!-- DAY12_APPEND_START -->
**Kiểm thử Day 12: 717 passed, 0 failed (619 cũ + 98 mới), 144,09s; exit code 0.**

## Day 12 — Data Integrity, Annotation Pilot & Evaluation Readiness (2026-11-03)

**Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

Đã đọc hướng dẫn/bàn giao/reports và pipeline/tests Day 1–11; lưu hash 128 file trước sửa để bảo toàn thay đổi/index. Baseline tái chạy **619 passed, 0 failed, 109,16s**; **98 tests Day 12 riêng passed, 0 failed, 8,75s**. Full suite cuối: [validation](day12/validation.json). Runner `.venv\\Scripts\\python.exe -B -m src.evaluation.run_day12` thành công, output mới, không gọi mạng hoặc apply correction.

Mới: integrity.py, pilot.py, run_day12.py; hai test files Day 12; reports/day12 gồm age audit đủ 4.112 rows/subset 1 lệch, exclusions đủ 8.322, coverage, lineage 28 cột, proposal JSON, pilot manifest/template/evidence, registry rỗng, audit/readiness JSON, sáu Markdown và validation. [Inventory](../docs/FILE_INVENTORY.md) liệt kê I/O/phụ thuộc.

Phát hiện mới/kiểm lại: 1 lỗi approximate_year_length; DOB ứng viên không thiếu/invalid/conflict, raw có 49 DOB thiếu. Hash 8 inputs và toàn bộ read-only audit Day 11 khớp. Missing còn 24 foot/23 height/16 tên CLB mỗi cột; height 19 cm giữ cờ review. Minutes loại 4.198; freshness fail độc lập 226 nhưng chỉ loại thêm 12. Nhóm 17–20 giữ 217/906=23,95%, không kết luận nhân quả. Metadata as-of/publication time còn thiếu, league proxy không phải league lịch sử.

Correction PROPOSED, chưa áp dụng/phê duyệt; snapshot/engine/API giữ nguyên. Pilot seed 12 chọn 8/scenario, tái lập khi đảo rows, không dùng rank/score; 0 assessor/labels. Validator có grade/schema/version/uncertainty/abstain/registry; agreement chỉ khi đủ bộ nhãn độc lập phù hợp. Synthetic chỉ unit fixtures. Cập nhật 10 docs, giữ lịch sử.

Git main/HEAD c4d638c, origin ScoutIQ-AI.git; không fetch, stage/commit/push/deploy. Requirements dirty từ trước không sửa, source Day 5–12 chưa commit và data bị ignore. Chưa nghiệm thu fresh-install/máy mới.

**Day 13 dự kiến, chưa triển khai:** xác nhận assessor thật và thực hiện pilot độc lập nếu có; review provenance, uncertainty, abstention và disagreement. Tách pilot khỏi final evaluation; thiếu nhãn thì giữ metrics thật bị chặn. Review chính sách calendar/DOB và quyền áp dụng correction, chỉ tạo snapshot mới và đo tác động trong nhiệm vụ được phép. As-of metadata và temporal split hợp lệ vẫn còn thiếu.

<!-- DAY12_APPEND_END -->

### Day13 — Nội dung bảo vệ và bàn giao

Mục tiêu: chuyển từ template sang intake/review có kiểm chứng provenance, bảo toàn nhãn và nguồn. Input: 8 dataset frozen, source/evidence Day11–12, CSV/registry riêng nếu có. Output: JSON coverage/readiness/queue cùng hashes, không sửa ranking. Thuật toán: validate hợp đồng → group theo scenario/assessor → đếm missing/pending/abstain/graded/uncertainty → so grade từng cặp trên common items → giữ bất đồng để coordinator review; agreement kế thừa công thức Day12.

Khó khăn thực tế: chưa có người chấm, nên kết quả thật bị chặn. Checkpoint trước gặp quyền thư mục pytest tạm; Day13 dùng --basetemp mới ngoài repo. Chưa có temporal metadata và DOB độc lập, không sửa dataset. Unit fixtures có ghi rõ SYNTHETIC, gồm các khai báo human giả lập chỉ trong tests để kiểm contract, không chuyển vào báo cáo chất lượng.

1. **Tại sao queue rỗng?** Vì chưa có assessor; không có bằng chứng rằng các chuyên gia đồng thuận.
2. **Tại sao missing khác pending/abstain?** Missing chưa nộp hàng; pending chưa quyết định; abstain đã xem nhưng thiếu bằng chứng. Cả ba không thành grade0.
3. **Hai ID đã chứng minh độc lập chưa?** Chưa; registry declaration cần review bằng chứng người thật, ngoài khả năng validator.
4. **Tại sao không sửa tuổi ngay?** Phép tính đã có đề xuất, nhưng nguồn DOB/chính sách và quyền áp dụng chưa đủ; cần snapshot mới và review tác động trước promote.
5. **Có thể làm Day14 khi chưa có quality metrics?** Có thể tiếp tục kỹ thuật theo nhiệm vụ, nhưng phải giữ blockers và không tuyên bố quality/production đã đạt.
