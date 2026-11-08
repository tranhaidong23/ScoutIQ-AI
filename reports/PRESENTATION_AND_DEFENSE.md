# ScoutIQ — Hồ sơ thuyết trình và bảo vệ dự án

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


Cập nhật **2026-11-02**, đối chiếu đến **Day 10**. Day là ngày làm việc của dự án, không phải ngày lịch. Tài liệu này giúp trình bày quyết định và trả lời phản biện từ bằng chứng trong repository; không cần lịch sử chat Codex/Claude. Phần Day 1–9 giữ kết quả các phiên trước; mục Day 10 cuối file bổ sung lần triển khai/kiểm thử mới và phase review. Có 4 Q&A mỗi Day (40 cặp).

## Cách đọc và mức độ bằng chứng

- **[Đối chiếu]**: đã đọc code, CSV/JSON, tài liệu hoặc Git local trong phiên tổng hợp này. Đọc báo cáo không đồng nghĩa chạy lại thí nghiệm.
- **[Lịch sử chạy]**: kết quả thực thi được nhật ký/báo cáo cũ ghi nhận. Các số test Day 1–7 bên dưới thuộc những lần chạy đó; phiên tổng hợp tài liệu trước **không chạy lại pytest, pipeline dữ liệu hay benchmark**. Day 8 sau đó đã chạy suite/runner mới, ghi riêng tại mục Day 8.
- **[Giả thuyết]**: lựa chọn hoặc cách giải thích còn cần kiểm chứng; không trình bày như kết luận chất lượng.
- **[Kế hoạch]**: việc chưa làm hoặc chưa nghiệm thu. Không có số liệu kết quả dự kiến để thay kết quả thực.
- **[Kiểm chứng mới Day 9]**: suite/runner/đối chiếu trực tiếp trong nhiệm vụ Day 9; không suy ra đã tái chạy collection/cleaning/EDA hoặc đánh giá relevance. Các kế hoạch Day 9 trong mục lịch sử đã được cập nhật bằng phần Day 9 cuối file; Day 10 vẫn chưa triển khai.
- **[Kiểm chứng mới Day 10]**: suite/service runner/benchmark/đối chiếu trực tiếp trong nhiệm vụ Day 10 sau mục lịch sử trên. Day 10 đã triển khai; Day 11 chưa triển khai. [Phase review](day10/phase_review.md) tách kết quả lịch sử Day 5–9 với kiểm chứng mới, không nghiệm thu scouting quality/production.

Nguồn gốc: [project_log](project_log.md), [insights_and_defense](insights_and_defense.md), code/tests và các artefact được liên kết theo từng Day. Khi có đính chính, thêm bằng chứng và chỉ rõ nội dung bị thay thế; giữ lịch sử. Khó khăn dưới đây gồm bài toán kỹ thuật cần xử lý và sự cố có nhật ký; không giả định mọi rủi ro đều đã gây lỗi thực tế.

**Phạm vi sản phẩm:** ScoutIQ — Intelligent Football Scouting & Transfer Recommendation System; *Scout Smarter. Sign Better.* Phục vụ scouts, sporting directors, recruitment analysts và CLB. Đã có pipeline dữ liệu và recommendation chạy local; chưa có sản phẩm web hoàn chỉnh. Authentication, quyền sở hữu dữ liệu theo user, PostgreSQL, FastAPI, Streamlit, so sánh trên UI, OpenAI chat có căn cứ và cloud vẫn thuộc [roadmap 31 ngày](../docs/PROJECT_CONTEXT.md) và [yêu cầu sản phẩm](../AGENTS.md).

**Phạm vi dữ liệu:** Transfermarkt, mùa 2025/26 (`season == 2025`), cutoff **2026-06-12**, không phải dữ liệu trực tiếp hiện tại. Tất cả kết quả recommendation dùng features **4.112 cầu thủ × 28 cột**, không phải 28 đặc trưng kỹ năng. SHA-256 features: `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`. [Manifest](../docs/DATA_MANIFEST.json) và [SETUP](../docs/SETUP.md) mô tả dữ liệu ngoài Git; clone riêng repository không tự có CSV trong `data/`.

## Mốc bằng chứng và Git

| Day | Đầu ra chính | Kiểm thử được ghi nhận | Commit chứa công việc |
|---|---|---|---|
| 1 | 5 bảng raw, báo cáo chất lượng | Script kiểm tra; không có số pytest được ghi nhận cho Day 1 | `86c036050d58ceca819858a8ed1391d3fbefaf9d` |
| 2 | 8.322 hồ sơ tích hợp → 4.112 ứng viên | Kiểm tra dữ liệu bằng script; không coi stdout là suite test | `c4d638c2d10c542c897ccf95dedde540814925b1` |
| 3 | 5 biểu đồ, 2 bảng tổng hợp | Đối chiếu artefact/code; không có suite EDA riêng được ghi nhận | Cùng commit Day 2 |
| 4 | Features 4.112 × 28, quality JSON | 23 passed, 0 failed, 1,98 s | `266f90f4a735289fbf9b78ac6aeca9c0acc68b0e` |
| 5 | Content-based cosine và 5 kịch bản | 57 passed, 0 failed, 6,06 s = 23 cũ + 34 mới | Chưa commit |
| 6 | Weighted cosine, ablation, 30 cấu hình–truy vấn | 109 passed, 0 failed, 13,12 s = 57 cũ + 52 mới | Chưa commit |
| 7 | KNN parity, robustness, benchmark | 178 passed, 0 failed, 20,19 s = 109 cũ + 69 mới | Chưa commit |
| 8 | Advanced constraints tương thích Day 5–7, 5 scenarios × 4 engine | Lượt cuối 338 passed, 0 failed, 44,83 s = 178 cũ + 160 mới | Chưa commit; để khi chuyển máy theo yêu cầu |
| 9 | Evidence/text tách riêng, comparison 2–5, 20 responses giữ nguyên | Lượt cuối 453 passed, 0 failed, 59,76 s = 338 cũ + 115 mới | Chưa commit; không push/deploy |
| 10 | Unified service/config/JSON schemas, parity và 400 latency calls, phase review | 549 passed, 0 failed, 62,01 s = 453 cũ + 96 mới | Chưa commit; chờ người dùng khi chuyển máy |

[Đối chiếu] `git log --name-only` xác nhận thứ tự commit thực là **Day 1 → Day 4 → Day 2–3**. Đây là thứ tự lưu vào Git, không dùng nó để suy thứ tự thực hiện công việc. Branch `main`, HEAD `c4d638c2d10c542c897ccf95dedde540814925b1`, origin `https://github.com/tranhaidong23/ScoutIQ-AI.git`; không fetch/xác minh GitHub trực tiếp trong phiên này. Working tree có thay đổi sẵn có, không có staged diff. Source/tests/reports Day 5–7 và bộ bàn giao chưa nằm trong HEAD. Không tự commit/push/deploy để làm đẹp trạng thái.

## Day 1 — Thu thập và kiểm tra nguồn

### Mục tiêu và công việc

Thu thập dữ liệu thật để nối cầu thủ, CLB, trận đấu, lượt ra sân và định giá. Kiểm tra schema, quy mô, missing, duplicate và khả năng chọn mùa/cutoff trước khi thiết kế mô hình.

| File | Chức năng / input → output |
|---|---|
| [download_data.py](../src/collection/download_data.py) | HTTP streaming 5 bảng `.csv.gz` từ nguồn R2 ghi trong code → `data/raw/`; bỏ qua file sẵn có khác rỗng |
| [inspect_data.py](../src/collection/inspect_data.py) | Đọc 5 raw → [day1_data_quality.csv](day1_data_quality.csv), shape/missing/duplicate |
| [check_season.py](../src/collection/check_season.py) | Kiểm tra mùa trận đấu, coverage appearances và thời điểm định giá qua stdout |

### Phương pháp và lý do

[Đối chiếu] Download theo từng chunk để không giữ toàn bộ payload trong RAM. Kiểm kê số dòng/cột, số dòng trùng toàn bộ và tỷ lệ ô thiếu là chẩn đoán ban đầu; chưa bảo đảm khóa join duy nhất hoặc dữ liệu có ý nghĩa nghiệp vụ. Nguồn có nhiều mùa, nên cần kiểm tra `games.season` và ngày trước khi tổng hợp 2025/26. Không thay missing bằng số 0 để tăng coverage.

### Kết quả và bằng chứng

[Đối chiếu artefact lịch sử] [CSV chất lượng](day1_data_quality.csv):

| Bảng | Dòng | Cột | Duplicate toàn dòng | Missing (%) |
|---|---:|---:|---:|---:|
| players | 50.149 | 26 | 0 | 15,29 |
| clubs | 796 | 17 | 0 | 9,51 |
| appearances | 1.894.350 | 13 | 0 | 0,00 |
| games | 88.958 | 23 | 0 | 4,00 |
| player_valuations | 656.301 | 6 | 0 | 2,36 |

Đây là quy mô các bảng raw được báo cáo, không phải số ứng viên mùa 2025/26. Không đếm lại raw hoặc tải lại nguồn trong phiên tài liệu. Commit Day 1 ghi ở bảng Git; checksum bàn giao được bổ sung ở giai đoạn sau trong [manifest](../docs/DATA_MANIFEST.json), không nhận là chức năng downloader Day 1.

### Khó khăn, cách xử lý và hạn chế

Năm bảng khác đơn vị quan sát và có missing khác nhau: kiểm kê riêng từng bảng, giữ raw làm nguồn đối chiếu, để cleaning xử lý theo ngữ nghĩa. Downloader có xử lý lỗi HTTP và file tải dở, nhưng thông báo cuối vòng lặp không chứng minh tất cả tải thành công. File khác rỗng cũng chưa chứng minh checksum đúng. Không có nhật ký sự cố tải cụ thể để kể lại như một failure đã xảy ra.

[Kế hoạch] Trước chuyển máy cần bàn giao snapshot riêng đúng manifest; URL nguồn có thể thay đổi nội dung. Fresh download/fresh install trên máy khác chưa nghiệm thu. Không đưa raw lớn hoặc secrets vào Git.

### Câu hỏi phản biện

1. **Vì sao cần 5 bảng?** Cầu thủ/CLB cung cấp metadata; games xác định mùa/ngày; appearances cung cấp thống kê; valuations cung cấp định giá có thời điểm. Một bảng đơn lẻ không đủ nối hiệu suất với ràng buộc tìm kiếm.
2. **Duplicate bằng 0 có nghĩa dữ liệu sạch không?** Không. Đây là trùng toàn dòng trong báo cáo; vẫn cần kiểm khóa ID, join cardinality, missing, phạm vi và thời gian ở các Day sau.
3. **Có phải dữ liệu hiện tại không?** Không. Hệ thống nghiên cứu snapshot tại cutoff 2026-06-12; ngày đọc báo cáo hoặc tải file không biến snapshot thành dữ liệu live.
4. **Clone Git có tái tạo chính xác raw không?** Chưa. Raw bị ignore, downloader dùng URL mutable và chưa khóa snapshot bằng checksum. Cần bản dữ liệu riêng khớp manifest và kiểm tra trên máy đích theo SETUP.

## Day 2 — Làm sạch, tích hợp và lọc ứng viên

### Mục tiêu và công việc

Tạo bảng một hàng/cầu thủ cho mùa đã chọn; tính thống kê và định giá tại cutoff; tạo tập ứng viên có thời lượng thi đấu và thông tin đủ cho bước phân tích.

| File | Chức năng / input → output |
|---|---|
| [01_explore_data.py](../src/preprocessing/01_explore_data.py), [02_check_columns.py](../src/preprocessing/02_check_columns.py) | Đọc mẫu/schema raw trước khi chọn cột và join |
| [clean_data.py](../src/preprocessing/clean_data.py) | 5 raw → `data/processed/scoutiq_players_2025_26.csv` |
| [create_candidates.py](../src/preprocessing/create_candidates.py) | Players → `data/processed/scoutiq_candidates_2025_26.csv` theo 4 điều kiện |
| [validate_data.py](../src/preprocessing/validate_data.py) | In chẩn đoán players; không phải assertion suite |

### Thuật toán, công thức và lý do

[Đối chiếu code] Chọn games mùa 2025 và ngày ≤ cutoff; nối appearances theo game ID với `many_to_one`. Loại ID/stat bắt buộc thiếu, phút ≤ 0, goals/assists âm; chỉ tính mỗi `appearance_id` một lần. Group theo player ID: cộng phút, goals, assists; số trận là số game ID phân biệt. `goals_per90 = 90 × goals / minutes_played`; assists và goal contributions/90 tương tự. Tuổi được tính từ DOB đến cutoff, chia 365,2425 ngày rồi lấy phần nguyên không âm.

Chọn định giá dương gần nhất **không sau cutoff**; nối metadata với kiểm tra cardinality `one_to_one`/`many_to_one`. Tập candidates yêu cầu **phút ≥ 900**, vị trí không trống, giá trị > 0 và `0 ≤ valuation_age_days ≤ 365`. Đây là lựa chọn về coverage/độ mới ban đầu, không phải ngưỡng tối ưu đã học.

### Kết quả và bằng chứng

[Đối chiếu manifest/báo cáo] Players **8.322 × 20**, candidates **4.112 × 21**, 4.112 ID riêng biệt: [manifest](../docs/DATA_MANIFEST.json), [quality input Day 4](day4_feature_quality.json). [Lịch sử nhật ký] 4.124 người đạt riêng ngưỡng 900 phút; áp dụng toàn bộ điều kiện còn 4.112. [Bảng vị trí](day3_position_summary.csv) xác nhận Defender 1.523, Midfield 1.204, Attack 1.059, Goalkeeper 326. Raw không bị xóa khi loại hàng khỏi output dẫn xuất.

Không có số pytest Day 2 riêng được ghi nhận. `validate_data.py` in thông tin hữu ích nhưng không thay thế bộ test tự động. Commit chung Day 2–3 là `c4d638c`.

### Khó khăn, cách xử lý và hạn chế

Join có thể nhân bản thống kê: code kiểm cardinality, deduplicate và tổng hợp theo ID. Thông tin thiếu không được tự coi là không ghi bàn; hàng thiếu stat bắt buộc bị loại. Lọc ngày trận/định giá giảm nguy cơ dùng tương lai, nhưng metadata `current_club_*` chưa được xác minh đúng thời điểm cutoff. Tên `club_name_verified` chỉ phản ánh join với bảng clubs, không phải kiểm toán lịch sử CLB độc lập.

[Giả thuyết] Ngưỡng 900 phút giúp hạn chế per90 trên mẫu quá nhỏ; chưa chứng minh bỏ được selection bias. [Kế hoạch] Kiểm độ nhạy ngưỡng, kiểm toán metadata theo thời gian và lưu đầy đủ số hàng loại theo từng nguyên nhân khi cải tiến pipeline.

### Câu hỏi phản biện

1. **Tại sao 900 phút và 365 ngày?** Đây là ngưỡng ban đầu để có thời lượng và định giá tương đối mới. Cần thực nghiệm độ nhạy; không gọi là tối ưu hoặc bảo đảm thống kê đáng tin tuyệt đối.
2. **Có làm mất dữ liệu gốc khi từ 8.322 xuống 4.112 không?** Không. Candidates là output riêng; raw và bảng players vẫn còn. Tập nhỏ hơn phản ánh phạm vi phân tích, không phải toàn bộ cầu thủ trong nguồn.
3. **Per90 có làm mọi cầu thủ so sánh công bằng không?** Chỉ chuẩn hóa theo thời lượng. Chưa điều chỉnh giải đấu, đối thủ, chiến thuật, vai trò hoặc bất định mẫu.
4. **Lọc cutoff là đã hết leakage?** Chưa. Ngày trận/định giá được chặn; metadata hiện tại và thiết kế đánh giá theo thời gian vẫn cần kiểm toán. Không được suy temporal validity từ tên cột hoặc vài assertion.

## Day 3 — Exploratory Data Analysis

### Mục tiêu và công việc

Mô tả phân phối định giá, tuổi, vị trí và đóng góp tấn công; dùng bằng chứng để định hướng feature engineering, không dùng tương quan làm chứng minh nhân quả.

| File | Chức năng / input → output |
|---|---|
| [eda_analysis.py](../src/eda/eda_analysis.py) | Candidates → 5 PNG và [day3_position_summary.csv](day3_position_summary.csv) |
| [age_group_analysis.py](../src/eda/age_group_analysis.py) | Candidates → [day3_age_group_summary.csv](day3_age_group_summary.csv) |
| [01 định giá](figures/01_market_value_distribution.png), [02 tuổi–định giá](figures/02_age_vs_market_value.png), [03 vị trí](figures/03_market_value_by_position.png) | Histogram/scatter/boxplot về phân phối và nhóm |
| [04 tấn công](figures/04_attacking_performance.png), [05 tương quan](figures/05_correlation_heatmap.png) | Goals/90–assists/90 và tương quan giữa các biến |

### Phương pháp, kết quả và bằng chứng

[Đối chiếu] Quy đổi EUR sang triệu EUR để hiển thị; groupby vị trí và nhóm tuổi, báo cả số người, mean/median. Nhóm tuổi bằng `pd.cut` với biên 16, 20, 24, 28, 32, 36, 100 trên tuổi nguyên hiện có. Tương quan là mô tả trên mẫu đã lọc.

Trên 4.112 candidates, mean định giá **9,241719 triệu EUR**, median **3 triệu**, max **200 triệu**; thống kê này được [JSON Day 4](day4_feature_quality.json) ghi lại trên cùng input. [CSV vị trí](day3_position_summary.csv): median Attack **4**, Midfield **3,5**, Defender **2,8**, GK **2 triệu EUR**. [CSV tuổi](day3_age_group_summary.csv): nhóm 17–20 có **217** người, median **10 triệu**; nhóm 37+ có **55** người, median **0,4 triệu**.

[Lịch sử nhật ký] Tương quan tuổi–định giá khoảng **−0,24**; goals–goals/90 khoảng **0,89**, assists–assists/90 khoảng **0,87** ([insights](insights_and_defense.md), phần EDA). Đây là số được ghi trong phân tích trước; không tính lại heatmap trong phiên tài liệu. Không dùng các hệ số toàn mẫu này thay hệ số fit-only theo vị trí của Day 6. Không có suite EDA riêng được ghi nhận; commit cùng Day 2 là `c4d638c`.

### Khó khăn, cách xử lý và hạn chế

Định giá lệch phải khiến mean không đại diện cầu thủ điển hình: trình bày cả median, histogram và phân nhóm. Nhóm tuổi có cỡ mẫu rất khác nhau: giữ số lượng trong bảng để tránh so trung bình thiếu bối cảnh. Không tự xóa cầu thủ đắt giá chỉ vì nằm ở đuôi phân phối.

[Giả thuyết] Nhóm trẻ có định giá cao có thể chịu selection bias do điều kiện 900 phút và coverage nguồn; chưa có nghiên cứu nhân quả. So nhóm 17–20 với 37+ không theo dõi cùng cầu thủ qua thời gian. [Kế hoạch tại Day 3, đã thực hiện một phần Day 4] kiểm tra log transformation và đặc trưng phụ thuộc; không coi đồ thị là bằng chứng recommendation tốt hơn.

### Câu hỏi phản biện

1. **Cầu thủ trẻ đắt hơn nghĩa là trẻ chơi giỏi hơn?** Không. Định giá có thể phản ánh tiềm năng, hợp đồng và nhiều yếu tố chưa quan sát; mẫu đã lọc còn có selection bias.
2. **Median hai nhóm chênh 25 lần có nghĩa mỗi cầu thủ mất 96% giá trị khi già?** Không. Đó là so sánh hai nhóm khác người, khác cỡ mẫu; không phải biến động theo thời gian của một cá nhân.
3. **Tại sao không xóa outlier 200 triệu?** Chưa có bằng chứng đó là lỗi. Giữ quan sát và mô tả độ lệch; chỉ sửa/xóa khi có lý do dữ liệu được kiểm chứng.
4. **Tương quan goals và goals/90 cao dẫn đến quyết định gì?** Cảnh báo đếm trùng tín hiệu nếu dùng cả hai. Day 5 chọn per90; Day 6 kiểm tra phụ thuộc theo vị trí, không suy rằng tương quan gây ra định giá hay chất lượng.

## Day 4 — Feature Engineering

### Mục tiêu và công việc

Tạo/kiểm tra các đặc trưng theo yêu cầu, giữ nguyên input, xuất dữ liệu dẫn xuất và bằng chứng chất lượng.

| File | Chức năng / input → output |
|---|---|
| [build_features.py](../src/features/build_features.py) | Candidates → `data/processed/scoutiq_features_2025_26.csv`, kiểm tra công thức/schema/cutoff và round-trip |
| [test_features.py](../tests/test_features.py) | Công thức, range, missing/infinity/duplicate, per90, percentile/ties, input preservation và input lỗi |
| [day4_feature_quality.json](day4_feature_quality.json) | Schema, missing/range, hash, distribution, warnings, kết quả kiểm tra |
| [Biểu đồ trước/sau log](figures/day4_market_value_transformation.png) | Histogram cùng tập 4.112 người, đơn vị, median và skewness |

### Công thức và lý do

| Đặc trưng | Công thức / cách diễn giải |
|---|---|
| goal_contributions | goals + assists |
| goal_contributions_per90 | 90 × (goals + assists) / minutes_played; đã có từ Day 2, kiểm lại |
| market_value_m | market_value_in_eur / 1.000.000 |
| log1p_market_value_m | ln(1 + market_value_m), giảm độ lệch để khảo sát phân phối |
| minutes_reliability | min(minutes_played / 2700, 1), heuristic về thời lượng |
| Ba percentile g90/a90/GC90 theo vị trí | 100 × average rank / số người cùng position; đồng hạng dùng rank trung bình |

Tham chiếu percentile là toàn bộ candidates tại cutoff **trước bộ lọc tìm kiếm**. Đây là ba chỉ số tấn công tương đối, không phải điểm chất lượng tổng hợp hoặc percentile của người dùng riêng. Đơn vị log là **triệu EUR**, khác đề xuất log EUR gốc từng nêu ở EDA; không lẫn hai công thức.

### Kết quả và bằng chứng

[Đối chiếu JSON] Output **4.112 × 28**, 8 đặc trưng tạo/kiểm tra, chỉ **7 cột mới**. Không trùng player ID hoặc infinity; missing metadata được giữ: foot **24**, height **23**, mỗi cột tên CLB **16**. Cờ bất thường height **19 cm**, ID **743556**, chưa sửa nguồn.

Skewness định giá **4,222779 → 0,632063** sau log; median 3 triệu → ln(4) ≈ **1,386294**. **939** người có reliability = 1. GK có **323/326** người zero goals, cùng percentile goals/90 khoảng **49,6933** do ties. Input hash không đổi, CSV round-trip đạt theo JSON. [Lịch sử chạy] **23 passed, 0 failed, 1,98 s**; [project_log](project_log.md) ghi lệnh và phạm vi test. Commit `266f90f`.

### Khó khăn, cách xử lý và hạn chế

Chiều cao 19 cm và metadata thiếu không có cơ sở sửa bằng suy đoán: giữ nguyên, ghi warning; recommendation sau đó không dùng chiều cao. Ties của GK cho thấy percentile toán học có thể gây hiểu nhầm: ghi rõ phương pháp và không dùng bàn thắng đánh giá GK. Log giảm lệch không chứng minh chuẩn, loại bỏ sai số nguồn hoặc cải thiện mô hình. Reliability chưa được hiệu chỉnh bằng sai số thực nghiệm.

[Kế hoạch từ Day 4] Chọn subset đặc trưng khi làm recommendation, kiểm đếm trùng/leakage và độ nhạy; không đưa tất cả cột mới vào mô hình mặc định.

### Câu hỏi phản biện

1. **Vì sao log1p trên triệu EUR?** Theo đặc tả Day 4 và đơn vị hiển thị rõ ràng. `ln(1+x/1e6)` không chỉ bằng `ln(1+x)` trừ một hằng số; phải cố định đơn vị. Giá và log giá hiện không dùng làm kỹ năng.
2. **Reliability = 1 là tin cậy 100%?** Không. Chỉ là đạt 2.700 phút theo heuristic; không phải xác suất, khoảng tin cậy hay điểm năng lực.
3. **GK không ghi bàn mà percentile gần 50 có vô lý không?** Đúng theo average-rank khi 323 người đồng hạng, nhưng không có ý nghĩa chất lượng bắt bóng. Đây là lý do không dùng nó để đánh giá GK.
4. **Đã sửa chiều cao 19 cm chưa?** Chưa; thiếu bằng chứng nguồn. Không tự đoán thành 190 cm, không biến cảnh báo thành giá trị sửa giả; feature này bị loại khỏi recommender.

## Day 5 — Baseline Content-Based Recommendation

### Mục tiêu, công việc và file

Xây baseline giải thích được từ dữ liệu thật, tách similarity khỏi ràng buộc tìm kiếm và bảo vệ preprocessing reference.

| File | Chức năng / input → output |
|---|---|
| [baseline.py](../src/recommendation/baseline.py) | Features + fit IDs + query ID + SearchFilters → Top K, score, evidence, warnings |
| [run_day5.py](../src/recommendation/run_day5.py) | 5 SCENARIOS → [JSON](day5_recommendation_examples.json), [bảng kết quả](day5_recommendation_examples.md) |
| [README.md](../src/recommendation/README.md) | Hợp đồng sử dụng, feature policy, giới hạn/leakage |
| [test_recommendation.py](../tests/test_recommendation.py) | 34 tests baseline/input/filter/ranking/evidence/reference isolation |

### Thuật toán, feature selection và lý do

| Nhóm | Numeric chuẩn hóa | Categorical one-hot | Ý nghĩa cho phép |
|---|---|---|---|
| Attack, Midfield | goals_per90, assists_per90 | sub_position | Hồ sơ đóng góp tấn công/vai trò |
| Defender | age, minutes_played | sub_position, foot | `context_profile_only` |
| Goalkeeper | age, minutes_played | foot | `context_profile_only`, không goals/assists |

StandardScaler fit theo position trên reference: `z = (x − mean_reference) / scale_reference`; categorical vocabulary cũng fit trên reference. Nối các block, chuẩn hóa L2 rồi tính `cos(x,y) = x·y / (||x|| ||y||)`, phạm vi [−1,1]. Giữ xử lý vector 0 tường minh vì cosine không xác định. Không dùng market value/log, reliability, percentile toàn catalogue, goal contributions, height, CLB hoặc ID trong vector.

Filter theo position phù hợp query, tuổi trong khoảng bao gồm hai biên, ngân sách tối đa EUR và số phút tối thiểu; loại query khỏi kết quả. Sort score làm tròn 12 chữ số giảm dần rồi player ID tăng dần; trả ít hơn K khi không đủ, không tự nới điều kiện. Explanation nêu số thật của candidate/query và giới hạn vị trí, không suy diễn kỹ năng thiếu.

### Kết quả và bằng chứng

[Đối chiếu JSON] Fit **4.108** người, loại bốn query khỏi fit trong thực nghiệm; default API có thể dùng toàn catalogue cho retrieval mô tả, không được mặc định mọi lần gọi đều có holdout.

| Truy vấn | Tuổi ứng viên | Budget EUR | Min phút | Eligible |
|---|---|---:|---:|---:|
| Harry Kane / Attack | 18–29 | 30.000.000 | 1.800 | 349 |
| Hans Vanaken / Midfield | 20–30 | 15.000.000 | 1.800 | 405 |
| Virgil van Dijk / Defender | 22–32 | 15.000.000 | 2.000 | 512 |
| Lukas Hornicek / GK | 20–30 | 10.000.000 | 1.800 | 107 |
| Kane / empty_budget | 18–29 | 0 | 1.800 | 0 |

Kane Top 5 baseline: **Franculino, Luis Suárez, Jonathan Burkardt, Júnior Brumado, Gianluca Scamacca**; tên/CLB/giá/score đầy đủ trong [báo cáo Day 5](day5_recommendation_examples.md). Ví dụ Franculino similarity ≈ **0,991291**, nhưng goals/90 ≈ **0,9175**, còn Kane ≈ **1,2661**. Cosine gần 1 không đồng nghĩa cùng sản lượng hoặc cùng năng lực.

[Lịch sử chạy] **57 passed, 0 failed, 6,06 s** gồm 34 mới + 23 Day 4; chưa có commit Day 5. Năm tình huống là kiểm hành vi, chưa phải đánh giá relevance độc lập.

### Khó khăn, cách xử lý và hạn chế

[Sự cố đã ghi trong nhật ký] Test isolation ban đầu có 1 failure: fixture tính lại per90 cả tập fit gây sai khác float khoảng `1e-16`. Sửa fixture chỉ tác động hàng held-out; không nới assertion hoặc kết luận engine bị leakage từ fixture sai. Thiếu defensive/GK metrics được giải quyết bằng giới hạn sản phẩm rõ `context_profile_only`, không tạo chỉ số giả.

[Giả thuyết] Feature policy có ích cho scouting là điều cần chuyên gia/nhãn kiểm chứng. Không điều chỉnh league/tactical fit/chấn thương/hợp đồng. Query ngoài scaler fit chưa phải temporal holdout. [Kế hoạch tại Day 5, đã thực hiện Day 6] kiểm trọng số, phụ thuộc biến và ablation.

### Câu hỏi phản biện

1. **Vì sao chọn content-based?** Có thuộc tính cầu thủ nhưng chưa có tương tác user hoặc relevance labels đáng tin. Đây là baseline có thể kiểm công thức và giải thích; không chứng minh tốt hơn mọi mô hình khác.
2. **Similarity 0,99 có nghĩa 99% chuyển nhượng thành công?** Không. Nó đo hướng vector trong không gian đã chuẩn hóa; không phải xác suất, khả năng mua hoặc điểm kỹ năng.
3. **Defender/GK được đánh giá thế nào khi thiếu chỉ số?** Chỉ so hồ sơ bối cảnh tuổi/phút/chân/vai trò có thật, gắn cảnh báo. Chưa đánh giá toàn diện phòng ngự hoặc bắt bóng.
4. **57 tests pass có đủ tin Top 5 để mua cầu thủ không?** Không. Tests kiểm hợp đồng code và isolation; cần nhãn/đánh giá chuyên gia, dữ liệu bổ sung và bối cảnh chuyển nhượng. Loại query khỏi fit không loại hết leakage thời gian.

## Day 6 — Weighted Cosine và đánh giá độ nhạy

### Mục tiêu, công việc và file

Giữ baseline để đối chiếu, triển khai trọng số không âm theo vị trí, kiểm phụ thuộc đặc trưng và so độ nhạy trên cùng dữ liệu/truy vấn.

| File | Chức năng / input → output |
|---|---|
| [weighted.py](../src/recommendation/weighted.py) | Validate weights, biến đổi vector của baseline, weighted cosine và explanation |
| [evaluation.py](../src/recommendation/evaluation.py) | Contract checks, overlap@K, Spearman trên pool chung, xử lý metric không xác định |
| [run_day6.py](../src/recommendation/run_day6.py), [DAY6.md](../src/recommendation/DAY6.md) | Runner thực nghiệm và mô tả protocol/API/kết quả |
| [test_weighted_recommendation.py](../tests/test_weighted_recommendation.py) | 52 tests mới, trọng số/vector/input lỗi, bộ lọc, parity và regression |
| [evaluation.json](day6/evaluation.json), [metrics.csv](day6/metrics.csv), [rankings.csv](day6/rankings.csv), [correlations.csv](day6/correlations.csv) | Config/reference/hash/env, 30 metric rows, 8.238 ranking rows, 264 cặp tương quan |
| [comparison.png](day6/comparison.png), [correlations.png](day6/correlations.png), [summary.md](day6/summary.md) | Hình độ nhạy/tương quan và bảng Top 5 |

### Công thức, cấu hình và lý do

`cos_w(x,y) = Σ(w_j x_j y_j) / sqrt[Σ(w_j x_j²) × Σ(w_j y_j²)]`.

Code nhân từng chiều với `sqrt(w/max(w))` rồi L2; chia chung max không đổi cosine và giảm rủi ro overflow. Trọng số phải hữu hạn, không âm, đúng tên feature/position; từ chối boolean, NaN, âm, tất cả 0 trong một nhóm và dynamic range gây underflow. Cho phép một số w=0 để ablation. Mỗi indicator trong block one-hot dùng trọng số block; hệ số không phải phần trăm cố định của score từng cặp.

| Vị trí / thứ tự feature | Default | Numeric emphasis | Categorical emphasis |
|---|---|---|---|
| Attack: g90, a90, role | 0,4 / 0,4 / 0,2 | 0,6 / 0,3 / 0,1 | 0,2 / 0,2 / 0,6 |
| Midfield: g90, a90, role | 0,3 / 0,5 / 0,2 | 0,2 / 0,7 / 0,1 | 0,15 / 0,25 / 0,6 |
| Defender: age, minutes, role, foot | 0,2 / 0,2 / 0,4 / 0,2 | 0,4 / 0,4 / 0,1 / 0,1 | 0,1 / 0,1 / 0,6 / 0,2 |
| GK: age, minutes, foot | 0,25 / 0,25 / 0,5 | 0,45 / 0,45 / 0,1 | 0,1 / 0,1 / 0,8 |

[Giả thuyết] Các weights do thiết kế thử nghiệm, chưa học từ nhãn hoặc được chuyên gia xác nhận tối ưu. Hai ablation lấy default rồi bỏ toàn categorical hoặc numeric đầu tiên (g90 cho Attack/Midfield, age cho Defender/GK). Baseline + 5 cấu hình này tạo 6 × 5 = 30 trường hợp, cùng snapshot/fit IDs/query/filter Day 5.

### Kết quả và bằng chứng

[Đối chiếu JSON/CSV] Tái lập chính xác 5 kịch bản Day 5; unit weights khớp full ranking/score baseline. 30/30 đạt contract checks và determinism, gồm 24 nonempty + 6 empty. Empty không có stability metric hợp lệ; checks trên tập rỗng không phải bằng chứng chất lượng.

| Cấu hình | Mean overlap@5 với baseline, 4 query nonempty |
|---|---:|
| baseline | 1,00 |
| weighted_default | 0,90 |
| numeric_emphasis | 0,90 |
| categorical_emphasis | 0,85 |
| ablate_categories | 0,25 |
| ablate_first_numeric | 0,35 |

`overlap@K = số ID chung trong hai Top K / K`; không gọi là Precision. Spearman dùng average-rank của score trên toàn pool chung, ghi số ứng viên chung; không tính nếu không đủ dữ liệu/score hằng. Attack bỏ categorical có **overlap@5 = 0**, dù **Spearman ≈ 0,9331**: tương quan toàn ranking cao không bảo đảm cùng shortlist.

[Đối chiếu correlations] Trên reference 4.108 người, theo vị trí: minutes–reliability Pearson **0,914953–0,960653**; GC90 = g90+a90 là quan hệ tuyến tính trực tiếp. Không thêm reliability hoặc GC90 để đếm lại tín hiệu. Correlation chỉ chẩn đoán, không chứng minh nguyên nhân hoặc predictive quality.

Default Kane Top 5: **Franculino, Luis Suárez, Gianluca Scamacca, Jonathan Burkardt, Tammy Abraham**. Vanaken: **Ringo Meerveld, Nikola Vlašić, Thijs Oosting, Fabian Rieder, Carlo Holse**. [Summary](day6/summary.md) có score/budget/CLB; không xác nhận CLB đúng tại cutoff. [Lịch sử chạy] **109 passed, 0 failed, 13,12 s**; lần rà soát sau đó 109 passed trong 14,60 s là lượt khác. Chưa commit Day 6.

### Khó khăn, cách xử lý và hạn chế

Nếu nhân vector trực tiếp với w sẽ thành hệ số w² trong tích vô hướng: dùng sqrt(w) để đúng định nghĩa. Ablation có thể tạo vector 0: giữ semantics baseline và ghi excluded/status, không gán điểm tùy tiện. Categorical làm thay shortlist mạnh, nên lưu cả full ranking và ablation thay vì chọn cấu hình từ vài tên dễ nhận biết.

Không có relevance labels: không Precision@K/NDCG@K. Bốn query nonempty không đủ khái quát mọi thị trường/CLB. Default vẫn là giả thuyết; stability không là chất lượng scouting. [Kế hoạch tại Day 6, đã thực hiện Day 7] đối chứng KNN cùng representation và benchmark có protocol.

### Câu hỏi phản biện

1. **Vì sao dùng căn bậc hai trọng số?** Cosine nhân hai vector; `sqrt(w) × sqrt(w) = w`. Nhân w vào cả hai sẽ kiểm một công thức khác với trọng số w².
2. **Default overlap 0,90 chứng minh tốt hơn baseline?** Không. Nó chỉ nói mức trùng shortlist với baseline. Một baseline kém vẫn có thể được tái lập rất ổn định.
3. **Vì sao không thêm GC90 hoặc reliability?** GC90 đã bằng tổng g90+a90; reliability là biến đổi của phút. Chúng không cung cấp mặc định tín hiệu kỹ năng độc lập và có thể đếm trùng. Chưa có bằng chứng cần nhân reliability vào score.
4. **Tại sao không công bố NDCG/Precision?** Chưa có relevance labels đáng tin. Tạo nhãn từ chính score hoặc giá thị trường rồi chấm mô hình sẽ không chứng minh chất lượng tuyển trạch.

## Day 7 — KNN Benchmark & Recommendation Robustness

### Mục tiêu, công việc và file

Kiểm KNN cosine như phương án truy xuất trên cùng representation Day 5–6; xác nhận ranking/filter/ties và đo latency công bằng, không giả định dùng thư viện là cải thiện chất lượng.

| File | Chức năng / input → output |
|---|---|
| [knn.py](../src/recommendation/knn.py) | KNNRecommender dùng lại baseline/weighted; NearestNeighbors cosine/brute/n_jobs=1 |
| [run_day7.py](../src/recommendation/run_day7.py), [DAY7.md](../src/recommendation/DAY7.md) | Parity/robustness/timing, kiểm hash artefact cũ, protocol và API; output-dir mới, không overwrite |
| [test_knn_recommendation.py](../tests/test_knn_recommendation.py) | 69 tests mới: zero/NaN/input/filter/ties/K/reproducibility/regression |
| [evaluation.json](day7/evaluation.json), [comparisons.csv](day7/comparisons.csv), [robustness.csv](day7/robustness.csv) | Config/hash/env/query/evidence; 10 cặp full ranking, 50 trường hợp K |
| [timings.csv](day7/timings.csv), [benchmark.csv](day7/benchmark.csv), [rankings.csv](day7/rankings.csv) | 1.000 mẫu timing, 20 nhóm thống kê, 5.492 ranking rows |
| [latency.png](day7/latency.png), [summary.md](day7/summary.md) | Median/p95 theo truy vấn và bảng đối chiếu |

### Thuật toán và protocol

Trên vector khác 0, `cosine_distance = 1 − cosine_similarity`. Filter trước retrieval; loại query và zero candidates; `NearestNeighbors.fit` lưu pool vector đã transform, **không refit scaler/category**. Gọi `kneighbors` với query tường minh và lấy toàn bộ ứng viên hợp lệ, chuyển score `round(1-distance,12)`, sort score giảm rồi ID tăng, cuối cùng cắt K. Lấy tất cả neighbors bảo vệ ties qua biên K; đây là lựa chọn exact retrieval hiện tại, không ANN tối ưu quy mô lớn.

Benchmark dùng 2 representations × 5 queries × 2 methods; mỗi nhóm **5 warm-up + 50 measured**, tổng **1.000 measured calls**. Đảo thứ tự direct/KNN luân phiên, `perf_counter_ns`, giới hạn threadpool=1 và n_jobs=1. Đo full recommend gồm filter, KNN.fit, retrieval, sort và explanation; không gồm constructor/scaler fit, CSV I/O, checks và ghi báo cáo. p95 dùng `numpy.percentile(method='linear')`. Empty chỉ đo no-results overhead, không chạy kneighbors.

Môi trường ghi trong [JSON](day7/evaluation.json): Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1; CPU Intel64 Family 6 Model 154 Stepping 4, 12 logical CPUs. Không coi environment quan sát là lockfile đầy đủ hoặc chứng nhận chạy trên máy khác.

### Kết quả và bằng chứng

[Đối chiếu artefact] **10/10** cặp full ranking đạt parity/filter/score/determinism; **50/50** trường hợp K=1/3/5/50/10000 đạt. Tám cặp nonempty overlap@5=1, Spearman≈1; hai empty là N/A. Max score difference **0**; max `|distance − (1 − tổng cosine_components)|` **4,440892098500626e−16**, tolerance 1e−11 có xét round12.

Ví dụ timing thực nghiệm, **median / p95 ms**; đầy đủ 20 nhóm và mẫu gốc nằm trong CSV liên kết ở trên:

| Query | Day 5 direct | Day 5 KNN | Weighted direct | Weighted KNN |
|---|---:|---:|---:|---:|
| Attack | 2,466 / 3,131 | 3,474 / 4,032 | 4,889 / 7,154 | 6,643 / 10,116 |
| Midfield | 4,796 / 6,824 | 6,651 / 9,715 | 4,888 / 6,973 | 6,700 / 9,845 |
| Defender | 5,196 / 7,966 | 6,932 / 10,839 | 5,378 / 7,968 | 7,109 / 10,243 |
| GK | 4,480 / 6,328 | 6,154 / 8,462 | 4,568 / 6,783 | 6,167 / 9,333 |

KNN median cao hơn direct ở **8/8** nonempty trong phiên này. **Quyết định hiện hành: giữ direct cosine, KNN làm đối chứng.** Weighted KNN Top 5 Kane/Vanaken đúng thứ tự và score Day 6; xem [evaluation JSON](day7/evaluation.json), không kể lại là chất lượng mới được cải thiện.

[Lịch sử chạy] Trước Day 7: 109 passed trong 15,45 s; cuối Day 7: **178 passed, 0 failed, 20,19 s**. Tests có vector/timing fixtures toán học để kiểm công thức và aggregation; không xuất chúng thành dữ liệu cầu thủ hoặc benchmark giả. Chưa commit Day 7.

### Khó khăn, cách xử lý và hạn chế

Chỉ lấy K neighbors có thể mất ties ở boundary và phụ thuộc thứ tự input: lấy toàn pool rồi sort thống nhất; test foot-only GK có nhiều hơn 5 người đồng hạng. Zero vector không có cosine hợp lệ: trả status rõ cho zero query, loại/đếm zero candidates; invalid input/NaN bị từ chối. Không tự nới filter hoặc bịa kết quả để đủ K.

Benchmark một máy/phiên, còn nhiễu CPU/OS; chưa đo cold start, concurrent load, cloud hoặc confidence interval. Chi phí adapter/KNN.fit có trong timing nên không suy latency này là chi phí kernel cosine riêng. KNN adapter phụ thuộc representation nội bộ, cần regression khi baseline đổi. Chưa có labels, temporal evaluation hoặc dữ liệu kỹ năng Defender/GK mới.

[Kế hoạch Day 8] Hoàn thiện hợp đồng filter vị trí/tuổi/EUR/phút và ngưỡng hiệu suất đúng dữ liệu thật; kiểm đơn vị, biên, input, no-results và filter→ranking. Không triển khai Day 8 trong phiên tài liệu.

### Câu hỏi phản biện

1. **KNN mới mà trả cùng Top K có thất bại không?** Không. Cùng vector và cosine distance=1−similarity thì thứ tự tương đương là kỳ vọng; parity kiểm implementation, không phải cuộc thi chất lượng.
2. **Vì sao filter trước KNN và lấy mọi neighbor?** Lọc sau global Top K có thể bỏ sót ứng viên hợp lệ. Lấy toàn pool rồi tie-break bảo vệ thứ tự ở boundary; đánh đổi thêm chi phí và chưa tối ưu catalogue lớn.
3. **Có thể nói KNN luôn chậm hơn hoặc p95 này là cloud SLA?** Không. Chỉ quan sát đường chạy, pool và máy đã đo; bao gồm fit/formatting, không có tải đồng thời hoặc hạ tầng cloud. Kết luận giữ direct chỉ áp dụng bằng chứng hiện có.
4. **NN.fit có làm rò rỉ query vào scaler?** Không trong đường chạy này: NN.fit nhận vector đã transform, scaler/categories vẫn dùng 4.108 reference loại 4 query. Nhưng điều đó chưa chứng minh metadata đúng cutoff hoặc hết leakage thời gian.

## Dùng tài liệu để thuyết trình

Trình tự gợi ý: bài toán/người dùng → nguồn/cutoff → phạm vi 4.112 ứng viên → EDA và giới hạn → feature policy → baseline/weighted → KNN đối chứng → phần chưa biết và bước tiếp theo. Dùng hình Day 3–4 để giải thích dữ liệu, hình Day 6 để nói về độ nhạy, hình Day 7 để nói về latency. Không dùng các hình này như bằng chứng mô hình đã tìm được cầu thủ giỏi nhất.

Khi trình bày demo, nêu query, bộ lọc, reference, đơn vị EUR và snapshot trước Top 5. Công bố `context_profile_only` cho Defender/GK. Lệnh chạy và điều kiện bàn giao ở [HANDOFF](../docs/HANDOFF.md); dùng output-dir mới nếu tái chạy runner, tránh ghi đè artefact lịch sử. Đây là hồ sơ nội dung, chưa phải slides hoặc sản phẩm đã deploy.

## Quy tắc cập nhật sau mỗi Day

Thực hiện cùng [project_log](project_log.md), [insights_and_defense](insights_and_defense.md) và [HANDOFF](../docs/HANDOFF.md), theo [AGENTS](../AGENTS.md) và [CLAUDE](../CLAUDE.md). Cập nhật [FILE_INVENTORY](../docs/FILE_INVENTORY.md) khi file/I/O/dependency đổi.

1. Ghi Day, ngày kiểm tra, trạng thái và mục tiêu; tách việc thực làm khỏi kế hoạch.
2. Liệt kê file/chức năng/input/output bằng link tương đối; dataset/cutoff/hash, thuật toán/công thức và lý do chọn.
3. Ghi kết quả với CSV/JSON/biểu đồ, query/config/môi trường, lệnh test và pass/fail thực có. Phân biệt lần chạy mới với đọc lại báo cáo cũ. Thiếu bằng chứng ghi Chưa xác minh/Bị chặn.
4. Ghi khó khăn thực tế/cách xử lý, hạn chế, giả thuyết, việc còn lại và **3–5 câu hỏi phản biện kèm câu trả lời**. Không biến rủi ro dự kiến thành sự cố đã xảy ra.
5. Ghi commit hash khi thực có, hoặc chưa commit; không ghi hash của commit tương lai. Đối chiếu số liệu và trạng thái giữa bốn tài liệu, giữ lịch sử và ghi đính chính rõ ràng.

Tại phiên tổng hợp ban đầu, Day 8–31 là kế hoạch; **sau triển khai Day 8 bên dưới, Day 9–31 vẫn là kế hoạch**, không điền kết quả trước. Mốc Git dự kiến Day 5, 10, 15, 20, 25, 30 và final release Day 31 chỉ là lịch đề xuất; không cấp quyền tự commit khi bị cấm, push/deploy hoặc phát hành release.

## Day 8 — Advanced Filtering & Search Constraints

### Mục tiêu, công việc và file

Mở rộng tìm kiếm theo nhu cầu tuyển trạch trên cùng representation Day 5–7; giữ API/score cũ, hard constraints trước ranking và phân biệt soft preference. [Kiểm chứng mới 2026-11-02] Triển khai code, chạy suite và runner trên dữ liệu thật; không chỉ đọc artefact lịch sử. Không commit/push/deploy, không làm Day 9.

| File | Chức năng / input → output |
|---|---|
| [constraints.py](../src/recommendation/constraints.py) | SearchConstraints chứa SearchFilters, parser unit/validation, hard mask/audit và AdvancedRecommender bọc engine đã fit |
| [run_day8.py](../src/recommendation/run_day8.py) | Features + prior JSON Day 5/6/7 + source hashes → thực nghiệm độc lập 5 scenarios × 4 engine |
| [DAY8.md](../src/recommendation/DAY8.md) | Hợp đồng API, ví dụ, đơn vị, missing, hard/soft, lệnh và giới hạn |
| [test_advanced_constraints.py](../tests/test_advanced_constraints.py) | 160 tests mới; validation, biên/tổ hợp, oracle/legacy, pool trước KNN, zero/ties/đảo dòng/no-refit |
| [evaluation.json](day8/evaluation.json), [scenarios.csv](day8/scenarios.csv) | Hash/dataset/config/reference/env/query/evidence; 20 cases với counts/status/checks |
| [filter_stages.csv](day8/filter_stages.csv) | 164 dòng audit tuần tự before/after/removed |
| [top5.csv](day8/top5.csv), [rankings.csv](day8/rankings.csv), [summary.md](day8/summary.md) | 80 dòng Top 5, 692 full-ranking rows, bảng trước/sau và explanation thật |

### Thuật toán, công thức và lý do

Hard pool là **giao** các điều kiện position, age range, budget EUR, min minutes, sub_position (hợp các role được chọn), min g90/a90, hard foot và club exclusions, sau khi loại query. Numeric biên inclusive. `EUR = budget_value × 1.000.000` chỉ khi khai `budget_unit=EUR_million`; nếu field là max_budget_eur thì 5 nghĩa là 5 EUR. Không đoán đơn vị hoặc chấp nhận typo/âm/NaN/infinity/overflow/min>max/bool thay số.

Role phải tồn tại đúng broad position, club exclusion dùng current_club_id hợp lệ trong snapshot. Active hard constraint có thuộc tính thiếu thì không đạt; không gán foot hoặc club giả. Foot left/right/both so chính xác. `foot_mode=soft` giữ người không khớp/thiếu foot và chỉ phá hòa khi cosine round12 bằng nhau; sort `(-score, -soft_match, player_id)`. Default hard bắt buộc foot khớp. Không sửa similarity, nới constraints hoặc học preference weights từ dữ liệu giả.

Tạo view riêng của encoded vectors đã fit, giữ query để tính cosine dù query không đạt tuổi/budget; gọi nguyên baseline/weighted/KNN trên pool đó. Không filter Top 5 cũ, không refit scaler/category, không mutate engine. KNN nhận filtered nonzero pool. Lấy full eligible ranking để xử lý soft ties qua boundary K; K lớn trả số có thật, empty/zero theo status cũ. Adapter dùng private representation, có regression bảo vệ, chưa tối ưu production.

GK từ chối goals/assists threshold kể cả 0; Defender có thể lọc số liệu tấn công thật nhưng không gọi đó là năng lực phòng ngự. Market value chỉ constraint/hiển thị, không là skill hay phí chuyển nhượng.

### Kết quả có bằng chứng

[Kiểm chứng mới] Features **4.112 × 28**, cùng SHA-256/cutoff đã ghi đầu tài liệu; fit **4.108**, loại 4 query, không temporal split. Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1, không dependency mới. Lệnh đã chạy:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day8
```

Baseline trước sửa **178 passed in 26.39s**; lượt đầu đạt 338 passed in 34.89s, lượt cuối sau sửa cảnh báo zero-candidate **338 passed in 44.83s, 0 failed**, exit 0. Runner cuối exit 0; **20/20 legacy checks**, **20/20 advanced cases** đạt, direct/KNN cùng representation khớp full ranking. Không có score/refit regression trên các kiểm tra này, không suy chất lượng scouting hoặc hết leakage từ đó.

| Scenario / query | Hard constraints chính | Position trước → hard pool | Top K |
|---|---|---:|---:|
| Tiền đạo trẻ / Kane | Centre-Forward, 18–23, ≤5M EUR, ≥1200 phút, g90≥.3, loại club 27; soft left | 1059 → 22 | 5 |
| Tiền vệ kiến tạo / Vanaken | Attacking Midfield, 20–29, ≤10M, ≥1200 phút, a90≥.15, hard left, loại 2282 | 1204 → 10 | 5 |
| Hậu vệ kinh nghiệm / Van Dijk | Centre-Back, 28–35, ≤5M, ≥2000 phút, hard right, loại 31 | 1523 → 94 | 5 |
| GK ngân sách / Hornicek | Goalkeeper, 20–30, ≤3M, ≥1800 phút, hard right, loại 1075 | 326 → 47 | 5 |
| No-results / Kane | Centre-Forward, 18–23, budget=0 EUR, ≥1200 phút, g90≥.3, hard left | 1059 → 0 | 0 |

Trước mọi lọc là 4.112; position count gồm query, self-exclusion có bước riêng. Counts nhất quán cả bốn engine. Empty check true là vacuous, không chứng minh relevance. [Summary](day8/summary.md) ghi đủ Top 5 weighted và explanation; cấu hình này vẫn là giả thuyết Day 6, chưa chứng minh tối ưu. Ví dụ đứng đầu: Barney Stewart (0,956332), Jeppe Erenbjerg (0,922962), Brandon Mechele (0,999090), Elías Ólafsson (0,863745). Không so score xuyên vị trí.

### Khó khăn, cách xử lý và hạn chế

- [Sự cố có bằng chứng] Suite đầu có **1 collection error** do parametrization tên request dành riêng pytest. Đổi thành payload rồi chạy lại toàn suite; không nới assertion hoặc che lỗi thuật toán.
- [Rà soát code] K nội bộ để lấy full ranking ban đầu tính cả zero candidates, có thể phát cảnh báo thiếu K dù shortlist người dùng đủ. Đổi sang số rankable, thêm assertion cho cosine/KNN và chạy lại toàn suite/runner. CSV/Top 5 của 5 scenarios không đổi; JSON cập nhật hash code cuối.
- Giữ hashes/API cũ nhưng cần hard filters trước ranking: cô lập view adapter và kiểm full ranking cũ giao pool bằng oracle độc lập; kiểm KNN pool trước retrieval, không fit scaler khi search và engine không đổi.
- Soft foot dễ gây hiểu nhầm: Kane vẫn có người chân phải đứng trước Moukoko chân trái do score cao hơn; Maswanhise thiếu foot vẫn vào Top 5. Output khai mode/match/warnings rõ. Hard foot mới loại missing/nonmatch.
- Chưa benchmark overhead full ranking/adapter, concurrency/cloud, labels relevance hoặc temporal evaluation. Metadata CLB chưa xác minh tại cutoff; 24 missing foot không tự sửa. Hard missing policy có thể loại người vì thiếu thông tin. Defender/GK chỉ context_profile_only; tuổi/phút chưa chứng minh kinh nghiệm hoặc kỹ năng.
- [Giả thuyết] Thresholds scenario phù hợp nhu cầu tuyển trạch cần chuyên gia đánh giá; correctness không là quality. [Kế hoạch] Day 9 chuẩn hóa explanation và dữ liệu so sánh thống nhất đơn vị/cutoff, kiểm truy vết/ties/đảo dòng; UI charts vẫn Day 21. Source Day 5–8/docs chưa commit, fresh-install/chuyển máy chưa nghiệm thu.

### Câu hỏi phản biện

1. **Sao không lọc lại Top 5 hiện có?** Người đủ điều kiện có thể nằm ngoài Top 5 toàn pool. Lọc trước ranking mới đúng yêu cầu; tests spy xác nhận KNN nhận pool đã lọc và oracle kiểm đầy đủ ứng viên.
2. **Budget 5 có thể hiểu là 5 triệu không?** Chỉ khi khai explicit EUR_million; max_budget_eur luôn EUR gốc. API không thể đoán ý định từ một số nhỏ, vì vậy trả lại đơn vị/giá trị đã chuẩn hóa.
3. **Ưu tiên chân trái mà chân phải đứng trước là lỗi?** Không ở soft mode: chỉ phá hòa score bằng nhau, không đổi score. Muốn bắt buộc trái dùng hard; missing không đạt hard nhưng vẫn có thể xuất hiện ở soft với match=false.
4. **338 tests và 20 cases đạt có nghĩa tuyển trạch tốt hơn?** Không. Đó là bằng chứng hợp đồng/validation/parity, chưa có relevance labels hoặc đánh giá chuyên gia. GK/Defender thiếu chỉ số kỹ năng, metadata và temporal validity vẫn cần kiểm chứng.

## Day 9 — Recommendation Explainability & Player Comparison

### Mục tiêu và công việc

Giải thích từng recommendation bằng dữ liệu thật có thể đối chiếu; so sánh 2–5 cầu thủ cùng đơn vị, tách evidence khỏi text để tích hợp API/chat sau này. Giữ nguyên feature selection/scaler/reference/similarity/ranking/eligibility/API Day 5–8; không gọi API hoặc triển khai Day 10.

| File | Chức năng / input → output |
|---|---|
| [explainability.py](../src/recommendation/explainability.py) | Engine/request → envelope chứa nguyên response + ID/raw values/units/weights/components/constraints/missing + rule-based text; explain_response kiểm response khớp engine/query |
| [comparison.py](../src/recommendation/comparison.py) | Catalogue thật + 2–5 ID/reference → raw values, categorical match, signed/absolute/relative differences và null reasons; không overall scoring |
| [run_day9.py](../src/recommendation/run_day9.py) | Features + prior Day 8 JSON/hashes/fit IDs/query/config → 20 cases, 7 artefact riêng, từ chối overwrite |
| [DAY9.md](../src/recommendation/DAY9.md), [tests](../tests/test_explainability.py) | API/schema/lệnh/giới hạn và 115 test mới, bảo vệ 338 tests cũ |
| [evaluation.json](day9/evaluation.json), [checks.csv](day9/checks.csv) | Full response/evidence/text/comparisons/config/hashes/env/Git và 20 dòng kiểm đối chứng |
| [top5.csv](day9/top5.csv), [feature_evidence.csv](day9/feature_evidence.csv), [comparisons.csv](day9/comparisons.csv) | 80 shortlist rows, 260 semantic-feature rows, 448 numeric-comparison rows; categorical comparison đầy đủ trong JSON |
| [summary.md](day9/summary.md), [biểu đồ](day9/attack_comparison.png) | Top 5 weighted của 5 scenarios, explanation/bảng so sánh; PNG reference + Top 4 Attack, ba trục đơn vị gốc |

### Thuật toán, công thức và lý do

Không đổi thuật toán retrieval. RecommendationExplainer gọi engine cũ và tạo evidence riêng từ catalogue đã validate; render text chỉ đọc evidence. Method cosine/weighted_cosine và retrieval direct/KNN được phân biệt. ID/name/position/CLB/age/minutes/EUR/valuation date, feature candidate/reference/weight và components có nguồn. Các hard constraints ghi required/observed/passed; soft foot vẫn chỉ phá hòa. Missing metadata giữ null/list, không tạo số liệu.

Tổng từng tích tọa độ vector chuẩn hóa là cosine score; tổng components của các feature hoạt động phải khớp trong 1e-10. Components có thể âm, không là causal attribution hoặc phần trăm kỹ năng. Feature bị ablate (weight=0) không được ghi nhận đóng góp. Categorical raw match tách khỏi membership trong vocabulary fit, tránh coi hai missing là giống nhau.

Compare nhận 2–5 ID nguyên dương có thật, distinct, reference trong nhóm; không sắp lại người dùng chọn. Signed delta = candidate − reference; absolute delta = abs(signed delta); relative % = 100×signed delta/abs(reference). Reference=0 → null/zero_reference; thiếu → null/missing_value; không chia infinity. NaN/inf, sai ID/kiểu/đơn vị/per90 hoặc overflow bị từ chối.

Attack/Midfield cùng nhóm so tuổi/phút/EUR/g90/a90; Defender/GK hoặc mixed positions chỉ context. Không thêm kỹ năng phòng ngự/GK, không tổng điểm tốt/xấu. Mỗi shortlist được chia reference+Top4 (5 người), rồi reference+hạng5 (2 người), đủ Top 5 mà không vượt giới hạn. No-results trả request/status/empty_reason và danh sách rỗng.

### Kết quả có dẫn chứng

[Kiểm chứng mới Day 9] Dataset/hash/cutoff giữ như đầu hồ sơ: 4.112×28, fit 4.108 loại bốn query. Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1; JSON ghi môi trường, 12 source hashes/2 input hashes. Không cài dependencies mới.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day9
```

Baseline trước sửa **338 passed in 47.81s**. Suite mới lượt đầu **452 passed, 1 failed in 81.33s**; sau sửa fixture dtype, lượt cuối **453 passed in 59.76s, 0 failed**, exit 0. Runner exit 0, **20/20 responses khớp nguyên Day 8**; score/rank/pool/constraints/status/evidence cũ giữ nguyên, audits fit không đổi. 80 explanations và 32 comparison groups; không suy chất lượng từ regression tests.

| Scenario/reference | Hard pool | Top K/engine | Top 1 weighted / score |
|---|---:|---:|---|
| Tiền đạo trẻ/ngân sách thấp — Kane | 22 | 5 | Barney Stewart / 0.956332 |
| Tiền vệ kiến tạo — Vanaken | 10 | 5 | Jeppe Erenbjerg / 0.922962 |
| Hậu vệ kinh nghiệm — Van Dijk | 94 | 5 | Brandon Mechele / 0.999090 |
| GK trong ngân sách — Hornicek | 47 | 5 | Elías Ólafsson / 0.863745 |
| No-results — Kane | 0 | 0 | Không có ứng viên |

Constraints nguyên Day 8 được giữ trong request/response JSON; bảng Day 8 phía trên ghi điều kiện. [Summary](day9/summary.md) có đủ Top 5/text/comparison của từng scenario weighted, [JSON](day9/evaluation.json) có cả cosine/weighted/KNN cosine/KNN weighted. Không so score xuyên vị trí hoặc gọi config mặc định là tốt nhất.

Ví dụ kiểm được: Barney Stewart có goals/90 **0.6293706294**, Kane **1.2661439114**, delta **−0.6367732821**, absolute **0.6367732821**, relative **−50.29233062%**, dù weighted similarity **0.956331763076**. Cosine cao không đảm bảo raw output bằng nhau; không suy kỹ năng thấp hơn 50%. Maswanhise thiếu foot vẫn trong shortlist soft, evidence ghi null thay vì đoán. PNG đã xem trực tiếp kiểm bố cục/nhãn/đơn vị, không lấy biểu đồ làm bằng chứng nhân quả.

### Khó khăn, cách giải quyết và hạn chế

- [Sự cố đã gặp] pandas 3 không cho gán infinity vào int64 trong test trước bước validator. Chuyển dtype fixture sang float, giữ nguyên assertion phải từ chối inf rồi chạy lại toàn suite; không nới validator hoặc sửa snapshot.
- Giữ API cũ mà thêm evidence: dùng wrapper/envelope; strict canonical JSON trong explain_response phát hiện cả bool rank/float ID mà phép so dict thông thường có thể xem bằng nhau. Không refit, có kiểm copy/no-mutation. Phụ thuộc private catalogue/representation cần regression khi đổi engine.
- Hai missing không chứng minh cùng category; raw match=null, membership vocabulary riêng, không thay baseline encoding. Score vẫn dựa representation có hạn chế, không cải thiện thuật toán bằng lời giải thích.
- Không relevance labels/Precision/NDCG, temporal validation hoặc league adjustments. Defender/GK chỉ context; metadata CLB tại cutoff chưa xác minh. Chưa khảo sát chất lượng/hữu ích explanation bởi scouts, chưa benchmark overhead wrapper/canonical retrieval hoặc production concurrency. JSON có version chưa là FastAPI/Pydantic contract; auth/privacy/API/chat/cloud chưa có.
- [Giả thuyết] Evidence có cấu trúc sẽ giúp chuyên gia kiểm tra khuyến nghị dễ hơn, cần kiểm chứng với người dùng. [Kế hoạch Day 10] tích hợp dịch vụ Python dùng lại cho API, ổn định cấu hình/pipeline và test hồi quy; chốt phiên bản ứng viên để đánh giá, không gọi model tối ưu. Source Day 5–9/docs chưa commit, fresh-install/chuyển máy chưa nghiệm thu. main/HEAD c4d638c giữ nguyên, không commit/push/deploy/fetch.

### Câu hỏi phản biện

1. **Similarity 0.956 nghĩa cầu thủ gần bằng Kane về chất lượng?** Không. Cosine đo góc vector sau preprocessing/weights. Barney có g90 thấp hơn reference trong snapshot dù cosine cao; chưa điều chỉnh league/tactics/uncertainty, không skill score hoặc xác suất chuyển nhượng.
2. **Đóng góp feature trong explanation có phải nguyên nhân làm cầu thủ tốt?** Không. Components chỉ phân rã phép tính hình học; có thể âm, tổng bằng score trong tolerance. Raw differences và constraints có nguồn riêng, không causal inference hoặc % tài năng.
3. **Reference bằng 0 hoặc metadata thiếu thì so sánh thế nào?** Relative=null với zero_reference, không infinity; missing có null/missing_value. Hai foot thiếu không coi là match. Dữ liệu numeric bắt buộc invalid bị từ chối, không impute để tạo comparison đẹp.
4. **453 tests đạt đã đủ cho FastAPI/OpenAI và chất lượng tuyển trạch?** Chưa. Tests chứng minh validation/parity/truy vết trên snapshot, không đánh giá người dùng hoặc nhãn relevance. JSON là đầu ra local; API schema/auth/privacy/grounded chat, performance và kiểm máy mới vẫn cần triển khai/kiểm chứng theo roadmap.

## Day 10 — Recommendation Engine Integration & Phase Review

### Mục tiêu, công việc và file

Tích hợp các modules Day 5–9 thành service Python có request/response JSON kiểm được, tách config/paths, đo latency local và chốt ứng viên engine để đánh giá. Không đổi baseline/weighted/KNN/scaler/eligibility/ranking hoặc tối ưu weights thiếu labels; chưa tạo FastAPI endpoint hoặc làm Day 11.

| File | Chức năng / input → output |
|---|---|
| [config.py](../src/recommendation/config.py) | Module/root → portable paths; explicit defaults/weights → validated/copy config, không secrets/Windows hardcode |
| [schemas.py](../src/recommendation/schemas.py) | Native JSON → Draft 2020-12 + finite/integer/domain/cross-field validation; export request/response structural core |
| [service.py](../src/recommendation/service.py) | Snapshot + fit IDs + config → bốn fitted engines; request → hard constraints/ranking/Top K/explanation/optional comparison/validated response |
| [run_day10.py](../src/recommendation/run_day10.py), [DAY10.md](../src/recommendation/DAY10.md) | Prior Day 8/9 JSON + features/source hashes → parity/serialized repeat/latency artefacts; API/schema/config/lệnh/protocol/giới hạn |
| [tests](../tests/test_service.py), [requirements](../requirements.txt) | 96 tests mới trên dữ liệu thật; jsonschema dependency trực tiếp, giữ UTF-16/nội dung requirement cũ |
| [evaluation.json](day10/evaluation.json), [request schema](day10/request.schema.json), [response schema](day10/response.schema.json) | Full responses/audits/hash/config/env/HEAD/protocol và schema export |
| [checks.csv](day10/checks.csv), [top5.csv](day10/top5.csv), [timings.csv](day10/timings.csv), [benchmark.csv](day10/benchmark.csv) | 20 parity cases, 80 Top 5 rows, 400 measured latency samples, 20 nhóm median/p95/min/max |
| [summary](day10/summary.md), [phase review](day10/phase_review.md) | Bảng kết quả/Top 5/latency và tổng kết từng Day 5–10, giới hạn/nghiệm thu/4 Q&A |

### Thuật toán, contract và lý do

Ghép module hiện có: validate request → hard constraints trước ranking → nguyên cosine/weighted/KNN geometry và deterministic ties → Top K → Day 9 evidence/text → optional comparison → validate response. Service giữ fitted engines cho một snapshot/config; không refit scaler theo query. KNN.fit vẫn chỉ trên filtered vectors như Day 7. Weights server config giữ giả thuyết Day 6; user request không nhận weights.

Schema `scoutiq.service.v1`: request áp dụng defaults (cosine/K=5/comparison=false), metadata method/normalized filters/hard candidate count/rankable/returned/K/dataset version/hashes/configuration_id/limitations, nguyên envelope Day 9 và comparisons. Chia comparison reference+block tối đa 4 người, đủ toàn Top K mà mỗi nhóm 2–5. No-results không fake row/nới điều kiện. Runtime từ chối NaN/Inf/duplicate keys/bool hoặc float ID/K, kiểm count/rank/score/units/components/evidence-text và comparison IDs/arithmetic. Standard JSON Schema integer có thể nhận 5.0, runtime strict check phải giữ khi tích hợp API tương lai.

Tổng components/delta/relative giữ công thức Day 9, zero/missing→null có lý do. Không tổng hợp kỹ năng hoặc causal attribution. Dataset version là SHA-256 bảng đầy đủ sort ID, csv_sha256 là bytes nguồn, configuration_id từ config/fitted audits/data; không phải Git commit hoặc quality label. Đường dẫn tính từ module hoặc explicit root, không theo cwd/Windows riêng. JSON schema là structural core với legacy extension, chưa typed đầy đủ mọi leaf/HTTP/Pydantic contract hoặc auth.

### Kết quả có bằng chứng

[Kiểm chứng mới Day 10] Snapshot 4.112×28, fit 4.108 loại bốn query, cùng cutoff/hash đã ghi đầu tài liệu; không temporal split. Windows 11/Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1, jsonschema 4.26.0, threadpoolctl 3.7.0. jsonschema có sẵn, chỉ khai báo requirement >=4.18,<5; không cài package, pip check đạt.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day10
```

Baseline **453 passed in 58.18s**, tests mới riêng **96 passed in 19.35s**, toàn suite **549 passed in 62.01s, 0 failed**, exit 0. Không test fail trong các lượt này. Sau suite chỉ chỉnh link phase review của runner để output-dir khác vẫn trỏ đúng; runner cuối exit 0 ghi source hash cuối. Giữ code/tests Day 5–9 và dữ liệu/artefact cũ.

**20/20 full responses Day 8, envelopes Day 9 và comparisons khớp**, không chỉ Top K/score. Pools 22/10/94/47/0 và K trả 5/5/5/5/0 cho tiền đạo/tiền vệ/hậu vệ/GK/no-results. 80 shortlist rows; Top 1 weighted vẫn Barney Stewart/Jeppe Erenbjerg/Brandon Mechele/Elías Ólafsson, không thay bằng cầu thủ giả. [Summary](day10/summary.md) có Top 5, JSON chứa toàn explanations/comparisons.

Latency: **3 warm-up + 20 đo/case, 20 cases, 400 measured calls**, rotation thứ tự, threadpool limit=1, không pytest đồng thời. Đo recommend_json trọn parse/validation/filter/rank/evidence/compare/response validation/serialization, comparison=true; loại startup/fit/CSV/network/HTTP/auth. 400 measured + 60 warm-up serialized JSON giống đối chứng, audits/input không đổi.

| Scenario | Cosine median/p95 ms | Weighted median/p95 ms |
|---|---:|---:|
| Tiền đạo trẻ | 85,663 / 150,281 | 90,031 / 145,246 |
| Tiền vệ kiến tạo | 74,381 / 102,959 | 80,826 / 103,740 |
| Hậu vệ kinh nghiệm | 125,829 / 156,275 | 125,921 / 158,670 |
| GK ngân sách | 94,444 / 138,373 | 95,010 / 149,366 |
| No-results | 29,309 / 55,904 | 32,203 / 53,664 |

Cả bốn methods trong benchmark/phase review. Nonempty median từng case 74,381–141,391 ms, p95 102,959–193,290 ms; không percentile gộp. Startup riêng một quan sát 1.423,006 ms. Không cloud SLA/quality hoặc so trực tiếp Day 7 (phạm vi khác); chưa profile stage để quy overhead cụ thể.

### Khó khăn, giải quyết và hạn chế

- Giữ thuật toán/API cũ nhưng thêm contract: dùng composition và legacy envelope, schema có extension ở payload cũ; tests kiểm full parity và cross-field consistency. API-ready local không nghĩa endpoint/auth/ownership đã có.
- Tránh nhận ID 5.0/bool, duplicate JSON keys và NaN/Inf mà parser mặc định có thể cho qua: strict native JSON traversal/parser + schema/runtime checks. Không echo payload vào lỗi để chuẩn bị dữ liệu riêng tư tương lai.
- Tránh dependency ngầm: phát hiện jsonschema 4.26.0 có sẵn, Pydantic chưa cài; khai báo jsonschema trực tiếp thay vì cài framework mới. requirements UTF-16 và nội dung cũ được giữ; không giả định máy mới đã chạy.
- 20 latency mẫu/case còn ít, min/max biến động/tải nền chưa kiểm soát đầy đủ. Không request-result cache, không benchmark concurrency/large catalogue/memory/HTTP/DB/auth/cloud. Bốn engines trong RAM/private adapters/full ranking chưa tối ưu production; giữ thuật toán trước để có đối chứng đáng tin.
- [Giả thuyết] Weights/defaults/scenarios có ích cho scouting cần chuyên gia/nhãn phù hợp. Chưa relevance labels/temporal metadata audit/league adjustment/skill GK–Defender; không market value ground truth hoặc similarity probability. Hash data/config/audit giúp truy vết, chưa guarantee bitwise xuyên mọi môi trường chưa pin.
- [Kế hoạch Day 11] protocol/rubric/tình huống có nguồn, coverage/filter/stability/latency, leakage/split khả thi; chỉ Precision/NDCG khi có nhãn đáng tin. Phase Day 5–10 chốt ứng viên tích hợp local, không model tối ưu/release. main/HEAD c4d638c giữ nguyên; source Day 5–10/docs chưa commit, chuyển máy còn cần snapshot/fresh-install. Không commit/push/deploy/fetch; mốc Day 10 chờ người dùng.

### Câu hỏi phản biện

1. **Service thống nhất có đổi model không?** Không. Composition dùng nguyên Day 5–9; 20 full responses/explanations/comparisons khớp, scaler/weights/pool giữ nguyên. Integration pass chưa chứng minh quality.
2. **Schema JSON có đủ bảo vệ request/response?** Chưa. Schema kiểm shape/type; cần domain constraints, finite/native-integer/duplicate-key và cross-field checks; auth/ownership còn ở roadmap. Legacy payload có vùng extension cần giữ regression khi nâng contract.
3. **p95 này dùng làm cam kết cloud được không?** Không. Chỉ local 20 mẫu/case, một luồng, chưa HTTP/auth/DB/concurrency và có biến động. Protocol/raw timings được lưu; Day 7 có phạm vi đo khác nên không so trực tiếp.
4. **Kết thúc Day 10 có thể tuyên bố tuyển trạch tốt hơn?** Không. Mới chốt ứng viên tích hợp để đánh giá; Day 11 thiết kế protocol/rubric/leakage/split và metric dựa nhãn thật. Không tự tạo relevance hoặc coi market value là kỹ năng.


<!-- DAY11_APPEND_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Day 11 — Recommendation Evaluation Protocol & Relevance Assessment

Ngày kiểm chứng: 2026-11-03. **Đã hoàn thành công cụ/protocol/audit; chưa chấm relevance độc lập.** Scope hiện hành: MVP anonymous, Streamlit/FastAPI/Neon/Gemini; auth và sync đa thiết bị thuộc Future Development. Mục này thay scope tương lai cũ, giữ lịch sử Day 1–10.

### Mục tiêu, công việc và file

Tách kiểm thử hành vi khỏi đánh giá phù hợp tuyển trạch. Đọc pipeline/engine/service, audit raw chỉ đọc, đóng băng 4 demo và 173 candidate-pairs, thiết kế rubric 0–3/evidence/abstain, công cụ metrics có gate và template không nhãn giả. [metrics.py](../src/evaluation/metrics.py): CSV/typed labels → validation + metrics; [audit.py](../src/evaluation/audit.py): raw/processed → evidence; [runner](../src/evaluation/run_day11.py): snapshot + Day 10 → reports mới; [tests](../tests/test_evaluation_protocol.py): SYNTHETIC math/edge cases và artefact thực. [Protocol](day11/evaluation_protocol.md), [rubric](day11/relevance_rubric.md), [template](day11/annotation_template.csv), [evidence](day11/annotation_evidence.csv), [audit](day11/audit_findings.md), [JSON](day11/evaluation.json), [summary](day11/summary.md), [validation](day11/validation.json).

### Thuật toán/công thức/lý do

Engine Day 5–10 giữ nguyên. Relevant khi grade ≥2; P@K=hits/K cố định, Recall=hits/total_relevant chỉ khi toàn eligible universe có labels; DCG=Σ(2^grade−1)/log2(rank+1), NDCG=DCG/idealDCG trên cùng universe. Thiếu nhãn/mẫu số 0 trả null/lý do; không unjudged=0. Ties giữ service order, không dùng grade phá hòa. Evidence/labels tách ranking để tránh đánh giá vòng tròn. Các công thức/gate và sklearn oracle có trong protocol/tests.

### Kết quả có bằng chứng

V: 549 baseline tests chạy mới; 16/16 full response Day 10/repeat/filter khớp, 4 pool 22/10/94/47, 173 unlabeled; toàn bộ relevance metrics thực null. Kết quả suite cuối ở validation JSON. Mỗi method coverage 20/173=11,56% trên 4 demo; overlap weighted/baseline@5=1 nhưng 3/4 query khác thứ tự. SYNTHETIC P@3=0,666667, R@3=1, NDCG@3≈0,692020 ([fixture](day11/synthetic_metrics.json)), không là số liệu football quality. Snapshot 4.112×28/SHA 425aeb9c…ca6b0/cutoff 2026-06-12; full hash/config/fit IDs/môi trường được lưu JSON, không tuning.

V audit: eligibility IDs/4 cột aggregate khớp raw, không ngày vượt cutoff trong tập kiểm; metadata lịch sử chưa xác minh; 4.198/8.322 <900 phút, mixed competitions. Phát hiện age 341429=29 so với 30 theo lịch, giữ snapshot và báo cáo issue. H: timing/correlation các Day trước chỉ đọc lại, không benchmark mới. P: pilot assessors/temporal data/backend mới. U: quality thật/fresh-install/cloud.

### Khó khăn, cách giải quyết và hạn chế

Không có nhãn độc lập: tạo template đầy đủ pool và gate thay vì nhãn từ model. Thiếu Defender/GK metrics: giới hạn context/abstain thay vì bịa skill. Metadata không as-of và tuổi xấp xỉ: công bố audit, không sửa baseline vượt phạm vi. Requirements/nguồn chưa lock và code chưa commit: ghi rõ trở ngại chuyển máy. Bốn demo không đại diện toàn thị trường; chưa agreement/temporal validation/expert quality. Scope mới chưa đồng nghĩa web/Neon/Gemini đã chạy.

### 5 câu hỏi phản biện

1. **Tại sao không lấy cosine làm nhãn relevance?** Nó là output cần kiểm tra; làm vậy đánh giá vòng tròn. Người chấm độc lập xem scenario/evidence, không rank/model; grades 0–3 không mặc định từ per90/giá.
2. **Vì sao Recall/NDCG trống dù có Top 5?** Chưa có nhãn toàn universe nên không biết total relevant hoặc ideal DCG. Null thể hiện thiếu bằng chứng; SYNTHETIC chỉ kiểm công thức, không thay expert judgment.
3. **Cutoff và query holdout đủ loại leakage chưa?** Chưa. Date probes/raw sum đúng chỉ chứng minh nhất quán snapshot; club/role metadata có thể sau cutoff, selection 900 phút/league bias và age boundary còn hạn chế. Không temporal split, không tuyên bố no-leakage.
4. **Gemini có ranking hoặc chấm relevance không?** Không. Python engine giữ hard constraints/rank; Gemini dự kiến parse intent/giải thích evidence sau validation, không sinh stats/nhãn. Chưa gọi API hoặc chọn model/deploy.
5. **Không login, Neon chung thì privacy/handoff thế nào?** Backend tương lai kiểm anonymous browser token/session cho từng read/write/delete; auth/sync thuộc future, không chia sẻ history công khai. Claude đọc scope/HANDOFF/protocol, cần source chưa commit và snapshot hash đúng/chạy tests trên máy mới; chưa nghiệm thu fresh-install.

### Day tiếp theo và Git

Day 12 dự kiến review/pilot annotation/provenance/coverage/abstention/split và kế hoạch age issue có version. Chưa triển khai Day 12, backend/Neon/Gemini. main/HEAD c4d638c, index/lịch sử giữ nguyên, không commit/push/deploy. Sau mỗi Day tiếp tục cập nhật 4 tài liệu/inventory/architecture/setup với bằng chứng thực.

<!-- DAY11_APPEND_END -->

<!-- DAY12_APPEND_START -->
**Kiểm thử Day 12: 717 passed, 0 failed (619 cũ + 98 mới), 144,09s; exit code 0.**

## Day 12 — Data Integrity, Annotation Pilot & Evaluation Readiness

Ngày kiểm chứng: 2026-11-03. **Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

### Mục tiêu, công việc, file và công thức

Audit tuổi/DOB/cutoff, provenance/coverage; thiết kế correction có version, chuẩn bị pilot và readiness. [integrity.py](../src/evaluation/integrity.py): raw DOB/snapshot → audit/classification/exclusions/coverage/lineage/proposal; [pilot.py](../src/evaluation/pilot.py): frozen 173 cặp → sample 32/template trống, validation/agreement/readiness; [runner](../src/evaluation/run_day12.py): read-only audit/hash checks → reports mới. [Tests integrity](../tests/test_day12_integrity.py), [tests pilot](../tests/test_day12_pilot.py), [summary](day12/summary.md), [validation](day12/validation.json).

Calendar age = chênh lệch năm trừ 1 nếu chưa tới sinh nhật; quy ước Feb29/March1 rõ trong audit, chưa áp dụng production. Pilot round-robin theo age strata với SHA256(version/seed/scenario/ID), không dựa rank/score. Grade 0–3/abstain giữ rubric Day 11; agreement exact và κ linear = 1−observed_disagreement/expected_disagreement, d=|a−b|/3. Expected=0 → null; numeric oracle chỉ SYNTHETIC fixtures.

### Kết quả, khó khăn và giới hạn

V (kiểm mới): audit 4.112 tuổi, 4.111 nhất quán/1 lệch ID 341429, 29→30 theo lịch; raw có 49 DOB thiếu ngoài candidates. [Findings](day12/age_integrity_findings.md), [proposal](day12/correction_proposal.json) applied=false. [Provenance](day12/provenance_audit.md): 8 input hashes/28 lineage; 4.198 loại do minutes và 12 loại thêm do freshness, không cộng 226 fail freshness độc lập vào tổng. Metadata/height outlier không sửa.

V: 32 pending, 0 assessor/labels; seed 12 tái lập khi đảo rows. Baseline 619 tests chạy lại đạt, 98 tests Day 12 riêng đạt; full suite cuối trong validation. [Guide](day12/pilot_annotation_guide.md) và [readiness](day12/evaluation_readiness.md) ngăn nhãn giả và sai mẫu số. H (bằng chứng cũ): Top5 frozen Day 11 dùng cho readiness, không benchmark timing mới. U: DOB truth ngoài nguồn, as-of metadata, expert quality, fresh-install. P: review nhãn và correction được phép trong nhiệm vụ tiếp theo.

Khó khăn: tuổi có lỗi nhưng cần giữ baseline → proposal có version, không silent fix; chưa có assessor → template/registry trống và metric gates; thiếu Defender/GK metrics → context-only/abstain; thiếu as-of metadata → temporal blocked, không đổi tên random split thành temporal validation. Không thay thuật toán hoặc triển khai Day 13/web.

### 5 câu hỏi phản biện

1. **Vì sao tuổi sai dù DOB đúng định dạng?** Công thức cũ int(days/365.2425) cắt phần thập phân; 10.957 ngày nhỏ hơn 30×365.2425=10.957,275 nên ra 29 ngay sinh nhật 30. Bằng chứng này dựa trên DOB snapshot, chưa xác minh nguồn ngoài.
2. **Vì sao chưa sửa ngay?** Nhiệm vụ yêu cầu giữ baseline. Proposal lưu parent hashes và old/new values, chưa có quyền promote dataset mới. Tuổi đi vào filter và Defender/GK scaler nên cần kiểm tác động toàn nhóm, không sửa một ô âm thầm.
3. **32 mẫu và hai người chấm đủ kết luận quality chưa?** Chưa. Pilot kiểm quy trình/rubric, không đại diện toàn 173 hoặc 4.112. Hiện chưa có hai bộ nhãn độc lập; agreement cao cũng không chứng minh nhãn đúng. Recall/NDCG cần đủ nhãn toàn eligible universe theo protocol.
4. **Cutoff pass có nghĩa no leakage?** Không. Event date khác publication time; metadata CLB/vai trò chưa as-of, percentiles toàn catalogue không được dùng vào temporal train/test. Query holdout chỉ kiểm fit; ngưỡng phút và hỗn hợp giải còn selection bias.
5. **Claude Code tiếp tục thế nào, MVP mới có ảnh hưởng không?** Đọc AGENTS/CLAUDE/HANDOFF và reports/day12, nhận source chưa commit cùng snapshot đúng hash, chạy tests trên máy mới. FastAPI/Neon/Streamlit/Gemini chưa triển khai; auth/sync là Future Development. Không dùng Gemini tạo labels hoặc ranking.

### Bàn giao và công việc tiếp theo

**Day 13 dự kiến, chưa triển khai:** xác nhận assessor thật và thực hiện pilot độc lập nếu có; review provenance, uncertainty, abstention và disagreement. Tách pilot khỏi final evaluation; thiếu nhãn thì giữ metrics thật bị chặn. Review chính sách calendar/DOB và quyền áp dụng correction, chỉ tạo snapshot mới và đo tác động trong nhiệm vụ được phép. As-of metadata và temporal split hợp lệ vẫn còn thiếu.

main/HEAD c4d638c, index/lịch sử giữ nguyên; không commit/push/deploy. Claude đọc HANDOFF/SETUP, nhận source chưa commit và snapshot đúng hash, chạy tests trên máy đích trước tuyên bố tái tạo được. Scope MVP anonymous/Neon/Gemini/Streamlit/FastAPI giữ nguyên, web chưa triển khai.

<!-- DAY12_APPEND_END -->

### Day13 — Nội dung bảo vệ và bàn giao

Mục tiêu: chuyển từ template sang intake/review có kiểm chứng provenance, bảo toàn nhãn và nguồn. Input: 8 dataset frozen, source/evidence Day11–12, CSV/registry riêng nếu có. Output: JSON coverage/readiness/queue cùng hashes, không sửa ranking. Thuật toán: validate hợp đồng → group theo scenario/assessor → đếm missing/pending/abstain/graded/uncertainty → so grade từng cặp trên common items → giữ bất đồng để coordinator review; agreement kế thừa công thức Day12.

Khó khăn thực tế: chưa có người chấm, nên kết quả thật bị chặn. Checkpoint trước gặp quyền thư mục pytest tạm; Day13 dùng --basetemp mới ngoài repo. Chưa có temporal metadata và DOB độc lập, không sửa dataset. Unit fixtures có ghi rõ SYNTHETIC, gồm các khai báo human giả lập chỉ trong tests để kiểm contract, không chuyển vào báo cáo chất lượng.

1. **Tại sao queue rỗng?** Vì chưa có assessor; không có bằng chứng rằng các chuyên gia đồng thuận.
2. **Tại sao missing khác pending/abstain?** Missing chưa nộp hàng; pending chưa quyết định; abstain đã xem nhưng thiếu bằng chứng. Cả ba không thành grade0.
3. **Hai ID đã chứng minh độc lập chưa?** Chưa; registry declaration cần review bằng chứng người thật, ngoài khả năng validator.
4. **Tại sao không sửa tuổi ngay?** Phép tính đã có đề xuất, nhưng nguồn DOB/chính sách và quyền áp dụng chưa đủ; cần snapshot mới và review tác động trước promote.
5. **Có thể làm Day14 khi chưa có quality metrics?** Có thể tiếp tục kỹ thuật theo nhiệm vụ, nhưng phải giữ blockers và không tuyên bố quality/production đã đạt.
