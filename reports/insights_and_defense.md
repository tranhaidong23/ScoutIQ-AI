# ScoutIQ — Data Science Insights & Defense Notes

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


> Nhật ký phát hiện, quyết định và chuẩn bị phản biện. Cập nhật theo từng ngày. **Phân biệt rõ kết quả đã đo với giải pháp dự kiến.**

## Day 1 — Data Collection

- Nguồn: dữ liệu Transfermarkt dạng CSV nén, tải bằng Python Requests.
- Quy mô: 50.149 cầu thủ; 796 CLB; 1.894.350 bản ghi ra sân; 88.958 trận; 656.301 bản ghi định giá.
- Phạm vi mùa `season == 2025`: 9.598 trận, 157.844 lượt ra sân, 9.181 cầu thủ duy nhất.
- Bản ghi định giá gần nhất trong nguồn: 12/06/2026.
- **Giới hạn:** Giá trị thị trường là ước tính, không phải phí chuyển nhượng; cần ghi ngày chốt dữ liệu.

## Day 2 — Data Cleaning & Integration

- Sau tích hợp: 8.322 cầu thủ.
- Điều kiện ứng viên: >=900 phút, có vị trí, giá trị thị trường dương, định giá trong 365 ngày trước 12/06/2026.
- Kết quả: 4.112 cầu thủ, 4.112 `player_id` duy nhất. Defender 1.523; Midfield 1.204; Attack 1.059; Goalkeeper 326.
- **Quyết định:** Giữ dataset tích hợp riêng; không xóa vĩnh viễn các cầu thủ dưới 900 phút.
- **Giới hạn:** 900 phút là ngưỡng thử nghiệm, cần đánh giá độ nhạy; CLB hiện tại có thể khác CLB tại thời điểm thi đấu.

## Day 3 — EDA: phát hiện và phản biện

### INSIGHT 01 — Phân bố giá trị thị trường lệch phải

**Quan sát (đã đo):** 4.112 ứng viên; mean = €9,241719 triệu; median = €3 triệu; Q1 = €1 triệu; Q3 = €10 triệu; max = €200 triệu. Mean/median ≈ 3,08.

**Diễn giải:** Trung bình lớn hơn trung vị đáng kể, phù hợp với phân bố lệch phải; histogram là bằng chứng trực quan cần kiểm tra thêm. Một số cầu thủ rất đắt giá kéo mean lên. Không suy ra lỗi dữ liệu chỉ từ giá trị cao.

**Giải pháp (chưa thử nghiệm):** Thử `np.log1p(market_value_in_eur)` nếu dùng định giá làm feature cho mô hình có khoảng cách; đối chiếu phân bố trước/sau và đánh giá chất lượng recommendation. Lọc ngân sách vẫn phải dùng giá trị EUR gốc, tuyệt đối không lọc trên giá trị log.

**Kiểm chứng cần làm:** Histogram gốc và log; so sánh thống kê độ lệch (skewness); kiểm tra thay đổi thứ hạng top-K khi có/không có biến đổi; nếu định giá chỉ là ràng buộc ngân sách, có thể không cần đưa vào vector tính tương đồng.

**Hỏi:** Vì sao không xóa cầu thủ €200M?

**Đáp:** Giá trị cao chưa chứng minh là sai. Cần kiểm tra nguồn và tính hợp lệ; xóa sẽ làm méo phạm vi thị trường và khiến ScoutIQ không phục vụ được CLB ngân sách lớn.

**Hỏi:** Tại sao chọn log1p thay vì log?

**Đáp:** `log1p(x)=ln(1+x)` xác định tại x=0 và giảm độ chênh lệch tương đối giữa giá trị rất lớn. Nhưng đây chỉ là phép biến đổi ứng viên; phải kiểm chứng tác động với mô hình.

### INSIGHT 02 — Khác biệt theo vị trí

**Quan sát (đã đo):** Median market value: Attack €4M, Midfield €3,5M, Defender €2,8M, Goalkeeper €2M. Trung bình goals/90 lần lượt 0,30; 0,12; 0,05; 0,00. Trung bình assists/90: 0,16; 0,12; 0,06; 0,01.

**Diễn giải:** Các nhóm vị trí có đặc điểm hiệu suất khác nhau; không thể dùng goals/90 để xếp hạng toàn bộ cầu thủ. Chênh lệch trung vị là mô tả mẫu, không chứng minh vị trí gây ra định giá.

**Giải pháp (đang thiết kế):** Chia mô hình theo vị trí hoặc dùng trọng số đặc trưng theo vị trí. Bổ sung dữ liệu phòng ngự/thủ môn trước khi tuyên bố đánh giá toàn diện.

**Kiểm chứng cần làm:** So sánh top-K và đánh giá thủ công theo các tình huống scouting cho từng vị trí.

**Hỏi:** Vì sao không chấm điểm thủ môn theo bàn thắng?

**Đáp:** Bàn thắng không phản ánh nhiệm vụ chính của thủ môn; cần các chỉ số như save percentage, clean sheets, goals conceded (và điều chỉnh theo bối cảnh) từ nguồn phù hợp.

### INSIGHT 03 — Tuổi cầu thủ

**Quan sát (đã đo):** Mean age = 26,54; median = 26; Q1 = 23; Q3 = 29; range 17–42. Mean age theo vị trí: Attack 25,99; Defender 26,72; Goalkeeper 28,74; Midfield 26,20.

**Diễn giải:** Một nửa mẫu nằm khoảng 23–29 tuổi. Thủ môn trong mẫu có tuổi trung bình cao nhất. Chưa thể kết luận độ tuổi nào có định giá cao nhất khi chưa phân tích biểu đồ và nhóm tuổi.

**Giải pháp (dự kiến):** Bộ lọc tuổi tùy yêu cầu CLB; tuổi không phải tiêu chí xếp hạng cứng cho mọi trường hợp.

**Kiểm chứng cần làm:** Scatter age/value, median theo nhóm tuổi và theo vị trí; kiểm tra tác động của những giá trị định giá lớn.

**Hỏi:** Tuổi trẻ có làm cầu thủ đắt hơn không?

**Đáp:** Không thể suy ra quan hệ nhân quả từ tương quan quan sát. Giá trị còn phụ thuộc thành tích, hợp đồng, giải đấu, danh tiếng và nhiều yếu tố khác.

### INSIGHT 04 — Số phút và độ tin cậy của per90

**Quan sát (đã đo):** 4.124 cầu thủ có >=900 phút trong bảng tích hợp; sau kết hợp các điều kiện còn 4.112 ứng viên.

**Diễn giải:** Per90 trên mẫu rất ít phút dễ dao động; cần hạn chế ứng viên có cỡ mẫu quá nhỏ.

**Giải pháp (đã triển khai):** Ngưỡng ban đầu >=900 phút cho dataset ứng viên; giữ dataset đầy đủ để không mất dữ liệu.

**Kiểm chứng cần làm:** Thử ngưỡng 450/900/1.350 phút; xem số ứng viên và độ ổn định top-K. Không tuyên bố 900 phút là chuẩn phổ quát.

**Hỏi:** Tại sao 900 phút?

**Đáp:** Đây là heuristic khoảng 10 trận đủ 90 phút để giảm nhiễu từ mẫu quá nhỏ; cần sensitivity analysis để chọn ngưỡng phù hợp từng nhiệm vụ.

### INSIGHT 05 — Độ mới của định giá

**Quan sát (đã đo):** Trong bảng tích hợp, 226 định giá cũ hơn 365 ngày, 7.877 trong vòng 180 ngày tính đến 12/06/2026. Có 8.096 định giá trong 365 ngày; sau tất cả bộ lọc còn 4.112 ứng viên.

**Diễn giải:** Dữ liệu cũ có thể không phản ánh tình hình chuyển nhượng tại thời điểm phân tích.

**Giải pháp (đã triển khai):** Chỉ chọn định giá hợp lệ không muộn hơn cutoff; bộ lọc ứng viên yêu cầu trong 365 ngày. Hiển thị ngày định giá và cảnh báo dữ liệu lịch sử.

**Kiểm chứng cần làm:** Thử cutoff 180/365 ngày và đo độ phủ ứng viên; xác minh dữ liệu cập nhật hơn nếu muốn trình diễn scouting thời gian thực.

**Hỏi:** Tại sao không gọi đây là giá chuyển nhượng hiện tại?

**Đáp:** Vì nguồn chỉ cho ước tính lịch sử đến 12/06/2026; phí chuyển nhượng thực tế có thể khác và còn phụ thuộc đàm phán.

## Nguyên tắc trình bày

- Slide: **Số liệu → Biểu đồ → Insight → Quyết định → Kết quả kiểm chứng**.
- Dùng nhãn **Đã triển khai**, **Dự kiến**, **Chưa kiểm chứng** rõ ràng.
- Lưu biểu đồ từ `reports/figures/` và kết quả chạy thực tế làm bằng chứng.
- Không nói AI tự phát hiện hoặc tự xác thực số liệu nếu quy trình thực tế là Pandas/EDA.

## Day 3 — Phân tích trực tiếp hai biểu đồ (14/10/2026)

### INS-06 — Tuổi và giá trị thị trường
- **Bằng chứng:** Scatter plot `02_age_vs_market_value.png`; Pearson(age, market_value_m) = **−0,24** trên 4.112 cầu thủ. Các mức định giá rất cao xuất hiện chủ yếu ở nhóm tuổi trẻ và trung bình; trên 30 tuổi ít quan sát có định giá rất cao.
- **Diễn giải:** Tương quan tuyến tính âm yếu, không chứng minh tuổi là nguyên nhân định giá giảm; biểu đồ có thể có quan hệ phi tuyến và sự khác biệt giữa các vị trí.
- **Quyết định:** Bộ lọc `min_age`, `max_age`, không tự động xem tuổi thấp hơn là chất lượng cao hơn.
- **Kiểm chứng dự kiến:** Phân nhóm tuổi, tính trung vị theo tuổi và vị trí; kiểm tra Spearman/đường xu hướng và độ nhạy khi lọc.
- **Phản biện:** Tại sao không ưu tiên cầu thủ trẻ tuyệt đối? Vì tuổi chỉ là một yếu tố ràng buộc/định hướng tuyển trạch, không thay thế hiệu suất và tactical fit.
- **Trạng thái:** Phát hiện đã quan sát; kiểm chứng bổ sung chưa thực hiện.

### INS-07 — Tính trùng lặp giữa số đếm và per90
- **Bằng chứng:** Pearson(goals, goals_per90) = **0,89**; Pearson(assists, assists_per90) = **0,87**.
- **Diễn giải:** Các cặp biến liên hệ về mặt công thức; sử dụng đồng thời mà không kiểm soát trọng số có thể nhân đôi ảnh hưởng của một năng lực.
- **Quyết định đề xuất:** Thử feature set ưu tiên per90, giữ goals/assists để trình bày; minutes_played làm tiêu chí quy mô mẫu/độ tin cậy.
- **Kiểm chứng dự kiến:** Ablation test (có và không có raw counts), so sánh thứ hạng, đánh giá recommendation và độ ổn định.
- **Phản biện:** Tương quan cao không bắt buộc phải loại biến; quyết định dựa trên mục tiêu, trọng số và thực nghiệm.
- **Trạng thái:** Phát hiện đã quan sát; thay đổi feature set chưa được kiểm chứng.

### INS-08 — Số phút thi đấu và định giá
- **Bằng chứng:** Pearson(minutes_played, market_value_m) = **0,40**.
- **Diễn giải:** Tương quan dương mức vừa, không chứng minh số phút gây tăng giá trị; có thể tồn tại biến nhiễu.
- **Quyết định đề xuất:** Dùng phút thi đấu để đánh giá mức độ tham gia và độ tin cậy; không cộng điểm chất lượng một cách mặc định.
- **Kiểm chứng dự kiến:** Phân tích theo vị trí, thử thay đổi ngưỡng 450/900/1800 phút.
- **Phản biện:** Cầu thủ giỏi có thể vừa ra sân nhiều vừa đắt giá, nên tương quan không đồng nghĩa nhân quả.
- **Trạng thái:** Phát hiện đã quan sát; kiểm chứng bổ sung chưa thực hiện.

### INS-09 — Chỉ số hiệu suất và giá trị thị trường
- **Bằng chứng:** Pearson(market_value_m, goals) = **0,41**, assists = **0,41**, goals_per90 = **0,25**, assists_per90 = **0,24**.
- **Diễn giải:** Số đếm có tương quan cao hơn per90 trong tập cầu thủ gộp, nhưng không chứng minh số đếm là thước đo chất lượng tốt hơn; bị ảnh hưởng bởi thời lượng và vị trí.
- **Quyết định đề xuất:** Tách bài toán **tactical similarity** (thống kê hiệu suất phù hợp vị trí) khỏi **transfer feasibility** (ngân sách/định giá/tuổi).
- **Kiểm chứng dự kiến:** Correlation theo vị trí, đánh giá gợi ý bằng các bộ đặc trưng và trọng số khác nhau.
- **Phản biện:** Giá thị trường không phải nhãn ground-truth của chất lượng cầu thủ, không nên tối ưu chỉ để dự đoán giá.
- **Trạng thái:** Phát hiện đã quan sát; thiết kế đề xuất chưa được kiểm chứng.

### Cảnh báo trình bày
- Pearson đo **tương quan tuyến tính**, không kết luận nhân quả.
- Scatter có nhiều điểm chồng lấn và ngoại lệ; nên bổ sung biểu đồ median theo nhóm tuổi.
- Dữ liệu chỉ gồm goals/assists/minutes, chưa đủ chỉ số phòng ngự/thủ môn hoặc tactical fit chuyên sâu.
- Mọi phép kiểm định/thay đổi feature set chưa chạy phải ghi rõ là **planned**, không nói đã cải thiện mô hình.

### INS-10 — Trung vị định giá giảm qua sáu nhóm tuổi (đã kiểm chứng bằng groupby)

**Bằng chứng (4.112 ứng viên; đơn vị triệu EUR):**

| Nhóm tuổi | Số cầu thủ | Median | Mean |
|---|---:|---:|---:|
| 17–20 | 217 | 10,0 | 16,56 |
| 21–24 | 1.215 | 5,0 | 11,92 |
| 25–28 | 1.430 | 3,9 | 10,46 |
| 29–32 | 858 | 2,0 | 5,09 |
| 33–36 | 337 | 0,8 | 1,65 |
| 37+ | 55 | 0,4 | 0,81 |

**Quan sát:** Trung vị giảm liên tiếp qua các nhóm tuổi. Nhóm 17–20 có median gấp 25 lần nhóm 37+ (10/0,4). Mean cao hơn median ở mọi nhóm. Đây là mô tả trên mẫu đã lọc, không chứng minh quan hệ nhân quả hoặc quy luật cho toàn thị trường.

**Giải thích / giới hạn:** Lọc >=900 phút có thể gây thiên lệch chọn mẫu: cầu thủ 17–20 đạt ngưỡng có thể là nhóm trẻ đã được thi đấu nhiều và được đánh giá cao. Cỡ mẫu nhóm 37+ chỉ 55 người; giá trị bị ảnh hưởng bởi vị trí, giải đấu, hợp đồng và nhiều biến không quan sát. Chênh lệch 25 lần là tỷ số giữa hai trung vị nhóm, không phải mức giảm giá của cùng một cầu thủ khi già đi.

**Quyết định:** Cho phép lọc độ tuổi theo chiến lược CLB; không tự động coi trẻ hơn là chất lượng hơn. Dùng median để báo cáo thị trường, không loại cầu thủ lớn tuổi chỉ vì tuổi. Nếu cần suy luận sâu hơn, phân tích median theo tuổi × vị trí và các nhóm giải đấu, thử Spearman, kiểm tra độ nhạy với ngưỡng 450/900/1800 phút.

**Kiểm chứng:** Đã chạy `src/eda/age_group_analysis.py` và xuất `reports/day3_age_group_summary.csv`. Chưa kiểm tra theo vị trí/giải đấu hay các ngưỡng phút khác.

**Phản biện 1:** “Cầu thủ càng trẻ càng tốt?” → Không. Đây là định giá trên tập mẫu đã lọc, không phải chỉ số chất lượng và không suy ra nhân quả.

**Phản biện 2:** “Giảm 25 lần có nghĩa mỗi cầu thủ mất 96% giá trị khi già đi?” → Không. Đây là so sánh trung vị giữa hai nhóm cầu thủ khác nhau, không phải dữ liệu theo dõi cùng một người qua thời gian.

**Phản biện 3:** “Tại sao nhóm 17–20 có median cao?” → Có thể do hiệu ứng chọn mẫu 900 phút, nhưng đó là giả thuyết cần kiểm tra, không phải nguyên nhân đã được chứng minh.

**Trạng thái:** Phân tích nhóm tuổi đã hoàn tất; các kiểm chứng sâu hơn được đề xuất cho giai đoạn tiếp theo.

## Day 3 — Kết luận

- EDA trên 4.112 ứng viên; đã chạy 5 biểu đồ, thống kê theo vị trí và thống kê 6 nhóm tuổi.
- Insight đáng trình bày: mean €9,24M > median €3M; Pearson(age,value) −0,24; trung vị nhóm tuổi giảm từ €10M xuống €0,4M; goals vs goals/90 r=0,89; assists vs assists/90 r=0,87.
- Các đề xuất như log1p, chọn feature set, đánh giá theo vị trí chưa được tuyên bố là đã cải thiện mô hình.
- Artefacts: `reports/figures/01_...png` đến `05_...png`, `reports/day3_position_summary.csv`, `reports/day3_age_group_summary.csv`.

## 2026-10-27 – Quản lý bằng chứng và quyết định dự án

### DOC-01 — Giữ nguyên lịch sử, phân biệt trạng thái xác minh

- **Quyết định:** Giữ nguyên các phát hiện Day 1–3; bổ sung hướng dẫn gốc tại `../AGENTS.md` và tiến độ trong `project_log.md`. Khi có số liệu mới khác số liệu cũ, thêm mục đính chính kèm bằng chứng, không xóa lịch sử.
- **Bằng chứng kiểm tra lần này:** Đã đọc code preprocessing/EDA, hai CSV tổng hợp Day 3 và nội dung báo cáo; xác nhận 5 ảnh EDA hiện diện. Tổng số cầu thủ ở cả hai bảng tổng hợp đều là 4.112.
- **Giới hạn:** Không chạy lại pipeline hoặc EDA, không xác minh lại toàn bộ số liệu nguồn/ảnh. Các tuyên bố “đã chạy” trong phần lịch sử là ghi nhận trước đây, không phải lần chạy mới ngày 2026-10-27.
- **Trạng thái:** Đã đối chiếu tài liệu và artefact; không phát sinh kết quả thực nghiệm Data Science mới.
- **Phản biện:** “Có file kết quả nghĩa là pipeline tái lập được?” → Chưa đủ. Cần chạy lại trong phạm vi được phép, ghi môi trường, phiên bản dữ liệu, lệnh và kết quả trước khi tuyên bố tái lập thành công.

### DOC-02 — Day 4 và lựa chọn mô hình vẫn cần kiểm chứng

- **Quyết định:** Day 4 Feature Engineering **chưa xác nhận hoàn thành**. Content-based recommendation, weighted cosine similarity/KNN, log1p, scaling và trọng số theo vị trí là hướng thiết kế/đánh giá, không phải mô hình đã chứng minh hiệu quả.
- **Bằng chứng:** `src/preprocessing/clean_data.py` đã có phép tính per90; các báo cáo cũ vẫn ghi việc chọn feature và đánh giá recommendation là dự kiến. Chưa thấy artefact mô hình/đánh giá Day 4 trong danh sách đã kiểm tra.
- **Giới hạn:** Sự hiện diện của per90 không chứng minh đã chọn xong feature set, xử lý missing values, kiểm tra leakage hoặc đánh giá top-K.
- **Kiểm chứng còn thiếu:** Định nghĩa baseline và tình huống scouting; kiểm tra bộ lọc; so sánh feature/trọng số; đánh giá độ ổn định top 3–5 và độ nhạy với ngưỡng phút/định giá.
- **Phản biện:** “Vì sao cosine hoặc KNN phù hợp?” → Đây là phương pháp ứng viên để tìm tương đồng đặc trưng; phải kiểm chứng chất lượng feature, chuẩn hóa, trọng số và kết quả theo nhiệm vụ trước khi chọn.
- **Trạng thái:** Quy tắc trạng thái đã ghi nhận; chưa triển khai Day 4 trong nhiệm vụ tài liệu.

### DOC-03 — Cutoff và kiểm tra data leakage

- **Bằng chứng từ code:** `clean_data.py` lọc trận mùa 2025 tới cutoff và chọn định giá không muộn hơn 2026-06-12; `create_candidates.py` giới hạn tuổi định giá trong 0–365 ngày.
- **Quyết định:** Kiểm tra cutoff ở từng nguồn/đặc trưng, ghi nguồn gốc và thời điểm dữ liệu; nếu có train/evaluation, bảo đảm các bước fit tiền xử lý không dùng dữ liệu ngoài tập được phép.
- **Giới hạn:** Các bộ lọc ngày chưa chứng minh toàn bộ pipeline không có leakage. Metadata `current_club_*` có thể không phản ánh CLB trong mùa 2025/26; đây là hạn chế đã ghi nhận, cần kiểm tra theo thời điểm nếu dùng làm feature.
- **Phản biện:** “Đã lọc ngày định giá thì hết leakage?” → Không. Cần kiểm tra cả dữ liệu trận, metadata, phép join, feature và thiết kế đánh giá.
- **Trạng thái:** Đã đọc logic lọc; chưa thực hiện kiểm toán leakage đầy đủ hoặc thay đổi code.

### DOC-04 — Phạm vi sản phẩm, quyền riêng tư và AI dựa trên dữ liệu

- **Quyết định:** FastAPI, Streamlit, PostgreSQL, đăng ký/đăng nhập/đăng xuất, dữ liệu riêng tư, search, recommendation, biểu đồ, OpenAI scouting chat, cloud và tests là yêu cầu bắt buộc trong `AGENTS.md`.
- **Giới hạn xác minh:** Chưa thấy file trong `backend/`, `frontend/`, `database/`, `tests/` tại lần kiểm tra này; chưa có bằng chứng đã triển khai các chức năng đó.
- **Tiêu chí cần kiểm chứng khi triển khai:** Backend kiểm tra chủ sở hữu lịch sử/chat/kết quả; tài khoản khác không thể đọc/ghi dữ liệu riêng; không lộ API key/mật khẩu; chat phải dựa trên dữ liệu truy xuất và nói rõ khi thiếu bằng chứng.
- **Phản biện:** “AI có thể tự bổ sung chỉ số còn thiếu?” → Không bịa dữ liệu. Phải báo thiếu và chỉ bổ sung từ nguồn thật có thể kiểm chứng.
- **Phản biện:** “Giá trị thị trường dưới ngân sách có bảo đảm mua được cầu thủ?” → Không. Đây là bộ lọc dựa trên ước tính lịch sử, không phải báo giá hay cam kết phí chuyển nhượng.
- **Trạng thái:** Yêu cầu/tiêu chí tương lai; chưa có kết quả test ứng dụng.

## Mẫu ghi phát hiện và quyết định tiếp theo

- **Mã / ngày / chủ đề:**
- **Quan sát hoặc giả thuyết:** Phân biệt kết quả đã đo với điều cần kiểm tra.
- **Bằng chứng:** Dataset/cutoff, đường dẫn code/artefact, lệnh và số liệu thực có.
- **Quyết định và lý do:** Lựa chọn, phương án so sánh, ảnh hưởng dự kiến.
- **Giới hạn:** Missing values, thiên lệch mẫu, thời điểm, yếu tố chưa quan sát.
- **Kiểm chứng:** Đã chạy gì, kết quả gì, phần nào chưa thực hiện.
- **Câu hỏi phản biện và trả lời:** Trả lời trong phạm vi bằng chứng; không suy diễn nhân quả hoặc bịa thống kê.
- **Trạng thái / liên kết nhật ký:** Dùng trạng thái thống nhất với `project_log.md`; ghi rõ nếu thay thế/đính chính mục cũ.

## 2026-10-27 — Day 4: Feature Engineering đã thực hiện

Mục này cập nhật trạng thái “chưa xác nhận hoàn thành” của DOC-02 theo nhiệm vụ Day 4 được người dùng giao sau đó. Đặc trưng và kiểm tra đã thực hiện; mô hình recommendation và các thử nghiệm Day 5 vẫn chưa thực hiện. Bằng chứng chung: `src/features/build_features.py`, `tests/test_features.py`, `day4_feature_quality.json`, `figures/day4_market_value_transformation.png` và CSV features trong `data/processed/`. Lệnh và kết quả kiểm thử xem phần Day 4 của `project_log.md`.

### INS-11 — Log giảm lệch định giá, không tạo điểm kỹ năng

- **Quan sát đã đo:** Trên 4.112 cầu thủ, `market_value_m` có mean 9,241719, median 3, min 0,025, max 200; skewness **4,222779**. Sau `ln(1 + market_value_m)`, mean 1,639695, median 1,386294, min 0,024693, max 5,303305; skewness **0,632063**.
- **Bằng chứng:** Hai histogram trong ảnh Day 4 và thống kê `market_value_distribution` trong JSON. Biểu đồ gốc tập trung nhiều quan sát ở vùng giá thấp với đuôi dài; log nén vùng giá cao và làm các vùng giá thấp/trung bình dễ phân biệt hơn. Mỗi hình có 40 bins đều trên thang riêng; không so sánh chiều cao từng bin như cùng khoảng EUR.
- **Quyết định:** Giữ EUR gốc để lọc ngân sách; thêm `market_value_m` và log để mô tả/thử nghiệm sau này. Không tạo skill score từ định giá.
- **Giới hạn:** Log đơn điệu nên giữ thứ tự định giá, nhưng thay đổi khoảng cách. Giảm skewness không chứng minh phân phối chuẩn, không giải quyết mọi outlier và không chứng minh gợi ý tốt hơn. Đây vẫn là market value lịch sử, không phải phí chuyển nhượng.
- **Phản biện:** “Vì sao log trên triệu EUR thay vì EUR?” → Đúng đặc tả Day 4 và có thang diễn giải rõ ràng. `log1p(x/1e6)` không tương đương `log1p(x)` trừ một hằng số; đơn vị ảnh hưởng hình dạng/khoảng cách, phải cố định và ghi rõ.
- **Trạng thái:** Đã triển khai, kiểm tra công thức nghịch đảo và quan sát biểu đồ; chưa đưa vào mô hình hoặc đánh giá tác động top-K.

### INS-12 — Reliability có trần là heuristic về thời lượng

- **Quan sát đã đo:** `min(minutes_played/2700, 1)` nằm trong [0,333333; 1], median 0,734444; **939/4.112** cầu thủ đạt trần 1.
- **Quyết định:** Giữ riêng cột `minutes_reliability`, không dùng để tự động nhân hoặc tăng điểm kỹ năng. 2.700 phút tương đương 30 × 90 phút, là mốc quy ước cho đặc tả này.
- **Giới hạn:** Đây không phải xác suất đáng tin, khoảng tin cậy, mức thể lực hoặc kỹ năng. Không mô hình hóa chấn thương, vai trò, chất lượng đối thủ, giải đấu hay độ biến thiên hiệu suất; mọi cầu thủ trên 2.700 phút nhận cùng giá trị.
- **Phản biện:** “Reliability = 1 có nghĩa cầu thủ chắc chắn tốt?” → Không; chỉ đạt trần thời lượng của heuristic. Cần kiểm tra độ nhạy với mốc phút khác và đánh giá ngoài mẫu trước khi dùng cho xếp hạng.
- **Trạng thái:** Đã tính và kiểm thử chặn trần/công thức; chưa được hiệu chỉnh hoặc kiểm chứng dự báo.

### INS-13 — Percentile theo vị trí và ảnh hưởng đồng hạng

- **Quyết định đã triển khai:** Với ba cột goals/90, assists/90 và goal contributions/90, tính `100 * average_rank / n_position`. Thang `(0,100]`; đồng hạng chia sẻ hạng trung bình. Tập tham chiếu cố định là toàn bộ tập ứng viên tại cutoff trước bộ lọc tìm kiếm.
- **Bằng chứng đã đo:** 323/326 thủ môn có goals=0 và cùng percentile goals/90 **49,693252**. Defender có 638/1.523 cầu thủ goals=0 với percentile **20,978332**; Attack có 38/1.059 với percentile **1,841360**. Đây là hạng trung bình, không phải tỷ lệ phần trăm cầu thủ bị vượt qua nghiêm ngặt.
- **Giới hạn:** Cùng percentile ở các vị trí không có nghĩa cùng hiệu suất tuyệt đối hoặc cùng chất lượng. Nhóm vị trí rộng che khuất vai trò; nhiều đồng hạng làm mất khả năng phân biệt. Các chỉ số tấn công không đánh giá đầy đủ thủ môn/hậu vệ.
- **Phản biện:** “Không ghi bàn sao percentile thủ môn gần 50?” → 323 cầu thủ đồng hạng tại mức 0 nhận hạng trung bình 162; `162/326*100 ≈ 49,69`. Đây là đặc tính phép tính, không phải bằng chứng họ có kỹ năng ghi bàn trung bình hoặc chơi tốt.
- **Phản biện:** “Nên tính lại percentile sau lọc ngân sách?” → Chưa làm vậy: giữ tập tham chiếu giúp cùng một cầu thủ có giá trị ổn định giữa các tìm kiếm trên snapshot. Nếu thay đổi tập tham chiếu phải định nghĩa lại và hiển thị rõ.
- **Trạng thái:** Đã kiểm tra đồng hạng bằng công thức đếm số quan sát thấp hơn/bằng nhau, kiểm tra từng vị trí và tính bất biến khi đảo thứ tự dòng; chưa đánh giá chất lượng recommendation.

### INS-14 — Metadata chưa sạch hoàn toàn dù đặc trưng tính được

- **Bằng chứng:** 4.112 ID duy nhất; không infinity; 8 đặc trưng không missing. Metadata còn thiếu foot 24, height 23, tên CLB hiện tại 16 và tên CLB đối chiếu 16. Connor Allan, `player_id=743556`, có chiều cao **19 cm**.
- **Quyết định:** Giữ nguyên giá trị thiếu và chiều cao nghi vấn trong CSV dẫn xuất để truy vết; không tự điền 0, đoán 190 cm, loại cầu thủ hoặc dùng chiều cao làm feature. Khoảng 140–220 cm chỉ là bộ lọc rà soát được ghi trong JSON.
- **Giới hạn:** Kiểm tra đủ điều kiện phép tính không đồng nghĩa mọi dữ liệu nguồn đều đúng. Các cột metadata giữ lại chưa sẵn sàng tự động đưa vào vector mô hình.
- **Phản biện:** “Tại sao không sửa 19 thành 190?” → Chưa có bằng chứng nguồn xác nhận. Tự sửa sẽ tạo thông tin không được kiểm chứng; Day 5 phải đối chiếu nguồn thật và ghi lịch sử sửa nếu có.
- **Trạng thái:** Đã phát hiện và báo cáo; chưa xác minh giá trị đúng hoặc thực hiện imputation.

### INS-15 — Đóng góp bàn thắng và rủi ro lặp ảnh hưởng

- **Bằng chứng:** `goal_contributions = goals + assists` có khoảng 0–69; `goal_contributions_per90` khoảng 0–1,432196. Cột per90 đã có từ Day 2 được kiểm tra trước khi tính lại; sai số đầu vào tối đa khoảng `2,22e-16`, phù hợp sai số số thực.
- **Quyết định:** Xuất đủ các cột theo yêu cầu để phân tích; chưa coi tất cả 28 cột là feature mô hình. Goal contributions per90 là tổng chính xác của goals/90 và assists/90, cần tránh đếm lặp khi thiết kế vector/trọng số.
- **Giới hạn:** Goals và assists được cộng trọng số bằng nhau theo định nghĩa, không đại diện mọi đóng góp trên sân. Tổng và per90 không phải hai nguồn thông tin độc lập; percentile cũng là biến dẫn xuất từ cùng chỉ số.
- **Phản biện:** “Thêm nhiều cột có luôn làm recommendation tốt hơn?” → Không. Biến phụ thuộc hoặc không phù hợp vị trí có thể làm lệch khoảng cách; cần ablation và baseline ở Day 5.
- **Trạng thái:** Công thức/CSV round-trip đã kiểm tra; chưa chọn feature set cuối cùng.

### Kiểm chứng và việc còn lại ở Day 5

- **Đã thực hiện:** 23 test đạt; kiểm tra missing/infinity/ID/phạm vi/per90, cutoff định giá và tuổi định giá, percentile, CSV round-trip; SHA-256 xác nhận 5 raw + 2 CSV cũ không đổi; không tạo dữ liệu nghiệp vụ giả. Biểu đồ được mở để kiểm tra trực quan.
- **Chưa kết luận:** Chưa có bằng chứng về độ chính xác recommendation, độ phù hợp tactical fit, tính nhân quả hoặc tính tối ưu của trọng số/mốc phút. Chưa kiểm toán đầy đủ leakage ở metadata và dữ liệu gốc từng trận.
- **Day 5 dự kiến:** Xác minh metadata bất thường/thiếu; chọn đặc trưng và scaling theo nhiệm vụ; baseline cosine/KNN phù hợp, không mặc định đưa giá thị trường vào điểm kỹ năng; ablation biến phụ thuộc; đánh giá top 3–5 và tuân thủ bộ lọc; phân tích độ nhạy reliability; xử lý thiếu chỉ số phòng ngự/thủ môn. Khi có holdout/đánh giá theo thời gian, chỉ fit tiền xử lý và tập tham chiếu percentile trên dữ liệu được phép.

## 2026-10-28 — Day 5: Baseline cosine đã triển khai

Mục này cập nhật phần Day 5 dự kiến bằng kết quả thực có. Bằng chứng: `src/recommendation/`, `tests/test_recommendation.py`, `reports/day5_recommendation_examples.json` và `.md`. Baseline/kiểm thử hành vi đã hoàn thành; chất lượng scouting, trọng số tối ưu, KNN và đánh giá chuyên gia vẫn chưa được xác nhận.

### INS-16 — Feature selection phải phản ánh dữ liệu thật theo vị trí

- **Quyết định đã triển khai:** Attack/Midfield dùng goals/90, assists/90 và one-hot vai trò; mỗi vị trí có scaler riêng. Defender dùng tuổi, phút, vai trò, chân thuận; GK dùng tuổi, phút, chân thuận. Hai nhóm sau luôn mang nhãn `context_profile_only`.
- **Bằng chứng:** Không có cột tackles, interceptions, save percentage hoặc chất lượng chuyền bóng trong 28 cột hiện có. 34 test recommendation kiểm tra policy và bất biến thứ hạng GK/Defender khi thay goals/assists trong bộ nhớ.
- **Giới hạn:** Tuổi/thời lượng/chân thuận chỉ tạo shortlist hồ sơ, không đo kỹ năng phòng ngự/bắt bóng. Attack/Midfield cũng chưa có xG, pressing, chuyền bóng hoặc điều chỉnh giải đấu. Không tuyên bố đây là hệ thống đánh giá toàn diện mọi vị trí.
- **Phản biện:** “Vì sao không dùng goals/90 cho GK vì sẵn dữ liệu?” → Không phù hợp nhiệm vụ thủ môn, có thể tạo xếp hạng gây hiểu nhầm. Giữ shortlist bối cảnh với cảnh báo và cần dữ liệu chuyên môn thật.
- **Phản biện:** “Tuổi/phút có đang bị biến thành điểm kỹ năng?” → Không trong cách diễn giải baseline: tìm hồ sơ giống tham chiếu, không thưởng tuyến tính cho trẻ/nhiều phút. Tuy vậy geometry của chúng vẫn quyết định shortlist, nên không được dùng score này làm bằng chứng năng lực.
- **Trạng thái:** Đã tính và kiểm thử; chưa kiểm chứng ích lợi tuyển trạch của shortlist bối cảnh.

### INS-17 — Tách định giá và các biến trùng thông tin khỏi vector

- **Quyết định:** Market value chỉ dùng lọc ngân sách EUR và hiển thị; không dùng làm feature, trọng số hoặc tie-break. Loại log định giá, reliability, goal contributions, percentile Day 4, CLB và chiều cao khỏi vector.
- **Bằng chứng:** Test nhân định giá lên và thay các biến không chọn không làm thay đổi ID/score khi bỏ bộ lọc ngân sách; tie-break là ID tăng dần. Hai per90 được dùng độc lập, không thêm tổng contributions gây đếm lặp.
- **Giới hạn:** Thay ngân sách có thể thay tập ứng viên hợp lệ, nhưng không nên đổi similarity của một cặp còn trong cùng model. Ngân sách theo market value không chứng minh CLB mua được cầu thủ với số tiền đó.
- **Phản biện:** “Tại sao không dùng mọi cột sau feature engineering?” → Cột dẫn xuất/phụ thuộc, metadata chưa xác minh và biến ràng buộc không tự động phù hợp cho khoảng cách. Thêm cột có thể làm lệch trọng số và diễn giải.
- **Trạng thái:** Loại biến và tính bất biến đã kiểm thử; chưa ablation có hệ thống để chọn cấu hình tốt nhất.

### INS-18 — Similarity cao không có nghĩa hiệu suất bằng nhau

- **Quan sát đã đo:** Kịch bản Attack tham chiếu Harry Kane, tuổi 18–29, tối đa €30M, >=1.800 phút có 349 ứng viên. Franculino đứng đầu, cosine **0,991291280497**; goals/90 **0,9174757282** so với Kane **1,2661439114**, assists/90 **0,1310679612** so với **0,1660516605**; cả hai là Centre-Forward.
- **Giải thích:** Cosine đo góc của vector z-score + one-hot đã chuẩn hóa L2. Góc gần nhau không buộc các giá trị thô bằng nhau; vai trò giống nhau đóng góp vào score. Khoảng cách này không được hiệu chỉnh thành xác suất chuyển nhượng.
- **Bằng chứng:** JSON lưu `evidence` và `cosine_components`; tests tính lại bằng công thức độc lập và kiểm tra tổng đóng góp bằng score trong tolerance.
- **Phản biện:** “0,99 có nghĩa 99% khả năng chiêu mộ hoặc chất lượng bằng Kane?” → Không. Đây là cosine trong representation đã chọn, không có mô hình xác suất hay nhãn chất lượng hỗ trợ cách hiểu đó.
- **Day 6:** Kiểm tra ảnh hưởng trọng số, scale và mức hiệu suất tuyệt đối; không tự thêm metric ngoài dữ liệu chỉ để tạo thứ hạng đẹp.

### INS-19 — Kiểm tra ranh giới fit, không tuyên bố hết mọi leakage

- **Đã thực hiện:** Fit trên **4.108** cầu thủ sau khi loại 4 ID tham chiếu thật; intersection query/fit = 0. Fit riêng từng vị trí, trước filter, không refit khi tìm kiếm. Tests thay riêng held-out và xác nhận mean/scale/vocabulary không đổi. Percentile Day 4 tính toàn catalogue không được sử dụng.
- **Bằng chứng:** Báo cáo model có số lượng/hash ID fit, mean/scale và danh mục mã hóa. Validation kiểm tra ngày định giá không vượt cutoff, valuation_age_days và per90 nhất quán.
- **Giới hạn:** Đây là kiểm tra preprocessing với query giữ riêng, không phải temporal evaluation hay nhãn ground truth độc lập. Snapshot vẫn có metadata thời điểm chưa được kiểm toán, và nguồn phút/thống kê từng trận chưa được xác minh lại trong Day 5.
- **Phản biện:** “Loại 4 ID khỏi fit đủ để tuyên bố recommendation chính xác?” → Không; đó chỉ bảo vệ một ranh giới dữ liệu. Cần protocol đánh giá, tiêu chí chuyên môn và dữ liệu phù hợp ở giai đoạn Model Evaluation.
- **Ghi nhận kỹ thuật:** Fixture đầu tiên vô tình tính lại per90 cho cả reference set làm đổi floating-point rất nhỏ; đã sửa để chỉ tác động held-out. Không dùng fixture đó để kết luận có leakage trong engine.

### INS-20 — Xử lý dữ liệu thiếu và kết quả rỗng minh bạch

- **Đã thực hiện:** 5 kịch bản trả lần lượt 5/5/5/5/0 cầu thủ; tất cả checks filter/score/thứ hạng đạt. Mức ngân sách 0 không tự tăng để đủ Top 5. Không trả chính cầu thủ tham chiếu hoặc ID trùng.
- **Dữ liệu thiếu:** Catalogue còn 24 foot, 23 height, 16 tên CLB ở mỗi cột tên liên quan; số này là ô thiếu theo cột. Defender/GK mỗi nhóm có 3 foot thiếu. Missing/unseen category là block 0, không tạo category có “chân thuận chưa biết” để thưởng cho hai missing giống nhau. CLB thiếu giữ null.
- **Quyết định:** Không dùng chiều cao 19 cm, không sửa hoặc impute khi chưa có bằng chứng nguồn. Vector 0 trả trạng thái/loại có thống kê thay vì xếp hạng giả; lần chạy thực có 0 vector 0 ở cả bốn vị trí.
- **Giới hạn:** Block 0 có thể ảnh hưởng hướng vector và không khôi phục thông tin thiếu; cần phân tích độ nhạy. CLB hiện tại không mặc định là CLB ở cutoff. Hạ yêu cầu phút dưới 900 không khôi phục cầu thủ đã bị lọc ở Day 2.
- **Trạng thái:** **57 test đạt (34 Day 5 + 23 Day 4)**; không có đánh giá chất lượng hoặc triển khai Day 6 trong kết quả này.

## 2026-11-02 — Bằng chứng và giới hạn của bàn giao liên máy/liên AI

Phiên này chỉ thiết lập tài liệu. Không có insight mới về chất lượng cầu thủ hoặc cải thiện mô hình; các phát hiện dưới đây liên quan tái lập và quản lý bằng chứng. Day cuối vẫn là Day 5.

### INS-21 — Working tree hoàn thành không đồng nghĩa clone nhận đủ

- **Xác minh:** HEAD/main và origin/main cache đều c4d638c; Day 5 code/tests/báo cáo untracked, tài liệu roadmap/trạng thái modified có từ trước. Phiên bàn giao bổ sung CLAUDE/docs và ba tài liệu quản lý, không thay index/HEAD.
- **Quyết định:** HANDOFF ghi rõ trạng thái unpublished và điều kiện chuyển source; giữ nguyên thứ tự commit Day 1 → Day 4 → Day 2–3. Không tạo commit hoặc push khi nhiệm vụ chỉ yêu cầu tài liệu.
- **Phản biện:** “Clone GitHub là tiếp tục được Day 6 ngay?” → Chưa: cần source Day 5/tài liệu được bàn giao thực và dữ liệu ngoài Git. Không kiểm remote trực tiếp nên origin/main cache không chứng minh GitHub hiện tại.
- **Cần làm trước chuyển máy:** theo nhiệm vụ được phép, rà diff/secrets/test rồi commit/push hoặc phương án chuyển source riêng; ghi hash thực, không bịa commit cho Day 5.

### INS-22 — Cutoff không thay thế version của snapshot

- **Xác minh:** 8 file data local có hash/bytes trong [DATA_MANIFEST](../docs/DATA_MANIFEST.json); processed lần lượt 8.322×20, 4.112×21, 4.112×28. .gitignore loại toàn bộ raw/processed. Downloader dùng URL mutable, bỏ qua file sẵn có khác rỗng, không kiểm checksum.
- **Quyết định:** đề xuất lưu/chuyển riêng raw + processed, giữ raw nguyên vẹn và đối chiếu SHA-256; không upload hoặc force-add vào Git. Manifest chỉ chứa metadata tái lập, không chứa dataset.
- **Phản biện:** “Tải lại rồi lọc cutoff 2026-06-12 có chắc tái tạo đúng?” → Không. Metadata hoặc dữ liệu nguồn có thể đổi, file có thể thiếu/hỏng; cutoff chỉ là một ràng buộc thời gian, không là version bất biến.
- **Giới hạn:** chưa chạy lại raw pipeline hoặc kiểm nguồn mạng trong phiên này. Nếu hash khác cần so schema/values/nguồn/serialization và ghi snapshot mới có lý do; không sửa manifest để che sai khác. Quyền phân phối dữ liệu/kho lưu riêng chưa được xác minh.

### INS-23 — Tests trên venv cũ không chứng minh cài lại được

- **Xác minh mới:** 57 tests đạt trong 10,67 giây; pip check báo không có dependency hỏng. Python 3.13.7; phiên bản direct dependencies trong [environment-observed](../docs/environment-observed.json). requirements.txt UTF-16 LE BOM, chưa pin.
- **Quyết định:** SETUP có Windows/POSIX, venv mới, bản requirements tạm UTF-8 và constraints quan sát; không đổi requirements gốc ở nhiệm vụ tài liệu. Không chép venv Windows. Không tạo .env.example khi baseline chưa có hợp đồng biến môi trường và không cần key/DB.
- **Phản biện:** “57 tests pass nghĩa là sẵn sàng chạy ứng dụng trên máy mới?” → Chỉ xác minh features/recommender trên máy cũ và dữ liệu hiện có. Chưa cài sạch, chưa khóa dependency bắc cầu, chưa kiểm các package tương thích/sẵn có trên máy đích. Backend/frontend/PostgreSQL/OpenAI/cloud chưa triển khai.
- **Giới hạn:** chưa có app web entrypoint; pip check không kiểm nguồn dữ liệu, relevance scouting hay bảo mật auth/privacy. Không tự tạo các lệnh chạy service không tồn tại.

### INS-24 — Bàn giao cần phân biệt bằng chứng theo thời điểm

- **Quyết định:** PROJECT_CONTEXT dùng V (kiểm trực tiếp hôm nay), H (log/artefact lịch sử), P (kế hoạch). Không gọi số liệu raw/EDA hoặc kịch bản trong report là pipeline mới chạy hôm nay. HANDOFF ghi Day/HEAD/status, blockers, lệnh, hạn chế và next steps.
- **Bằng chứng:** kiểm link/JSON/inventory/cú pháp lệnh inline và bảo toàn hash source/data; ba tài liệu lịch sử giữ nguyên tiền tố cũ. Các kiểm tra này chỉ nghiệm thu tài liệu local, không nghiệm thu chuyển máy.
- **Phản biện:** “AI mới có cần biết chat Codex để hiểu quyết định?” → Không: đọc CLAUDE → AGENTS/HANDOFF → context/architecture/setup/inventory → log/insights → code/tests. Nếu khác thực tế, kiểm tra và ghi đính chính; không xóa lịch sử.
- **Quy trình:** sau mỗi Day chạy tests và cập nhật log/insights/HANDOFF, inventory khi đổi file/I/O/dependency; phản ánh thay đổi hiện hành trong AGENTS/context. Đề xuất mốc Git 5/10/15/20/25/30/31, chỉ thao tác theo quyền tương ứng. Làm mới bằng chứng khi chuyển máy thực tế, không coi snapshot hôm nay là bảo đảm cho một tuần sau.

## 2026-11-02 — Day 6: Weighted cosine và đánh giá hành vi/độ nhạy

### INS-25 — Định nghĩa trọng số phải đúng hình học

- **Quyết định:** cosine_w=sum(w*x*y)/sqrt(sum(w*x²)*sum(w*y²)); nhân sqrt(w/max_w) trước L2, không nhân w rồi vô tình dùng w². Numeric z-score và categorical one-hot giữ fit-only Day 5. Trọng số block áp mỗi indicator, không chia theo số category.
- **Bằng chứng:** oracle scalar độc lập trên 4 position; weights=1 khớp toàn ranking/score baseline; nhân mọi weights cùng 1e-200/1e200 không đổi signature. W>=0 hữu hạn, toàn zero/NaN/∞/âm/keys sai bị từ chối; partial zero ablate, vector zero xử lý rõ.
- **Phản biện:** “w=.4 nghĩa là 40% khả năng chuyển nhượng hay đóng góp cố định 40% score?” → Không. Đây là hệ số hình học; score còn tùy z-score, hướng/norm, category và các feature khác, không là xác suất.
- **Giới hạn:** default là heuristic, chưa học từ labels/chuyên gia; numeric và categorical không có energy bằng nhau. Giữ baseline, chưa chọn model thắng cuộc.

### INS-26 — Tương quan phải kiểm theo vị trí và trên reference

- **Bằng chứng:** 264 cặp Pearson/Spearman trên fit 4.108 người, chia position; ngưỡng |Pearson|>=.8 là cờ mô tả. Attack goals–g90=.810577, assists–a90=.830681; Midfield=.882477/.852483. g90–a90 chỉ -.018939 (Attack), .347238 (Midfield).
- **Quyết định:** tiếp tục chọn g90/a90, không thêm số đếm, tổng contributions hoặc percentile dẫn xuất; contributions/90=g90+a90 là phụ thuộc tuyến tính đúng ngay cả khi pairwise corr từng cặp chưa hoàn hảo. Không tự bỏ g90/a90 chỉ bằng cảm tính.
- **Phân biệt độ tin cậy:** minutes–reliability Pearson .914953–.960653; reliability là min(minutes/2700,1), không là chỉ số hiệu suất độc lập, không nhân vào similarity. Defender/GK minutes/age chỉ mô tả context.
- **Phản biện:** “GK goals–g90=.983231 nghĩa là goals là feature GK tốt?” → Không. Tương quan trong biến thưa không chứng minh giá trị chuyên môn; GK không dùng bàn thắng. Heatmap chẩn đoán chứa biến không nằm trong vector.
- **Giới hạn:** reference đã qua selection >=900 phút/định giá; correlation không causal; chưa chuẩn hóa giải đấu hoặc đo tactical fit.

### INS-27 — Full-rank correlation cao có thể che shortlist thay đổi

- **Bằng chứng:** cùng 5 kịch bản Day 5 và 6 cấu hình: 30 checks đạt; Attack bỏ categorical overlap@5=0 nhưng Spearman full-common=.933110. Default mean overlap 4 query=.90; numeric_emphasis=.90; categorical_emphasis=.85; bỏ categorical=.25; bỏ numeric đầu tiên=.35.
- **Quyết định:** báo cả overlap@K và full-common Spearman, mẫu số K cố định, cùng pool/count, ties average theo score (không theo ID). Empty/constant/không đủ người trả null với lý do. Không coi null là 0 hoặc stability hoàn hảo.
- **Phản biện:** “Cấu hình gần baseline nhất là tốt nhất?” → Không; nó chỉ ít thay đổi hơn. Baseline có thể thiếu tiêu chí tuyển trạch, nên giữ giống không chứng minh chất lượng.
- **Giới hạn:** chỉ 4 query nonempty, không có khoảng tin cậy hay đánh giá chuyên gia. Mean descriptive qua vị trí không phải quality metric. Chưa tính Precision@K/NDCG@K vì thiếu relevance labels thật.

### INS-28 — Hồi quy và tái lập là bằng chứng hành vi, không hết leakage

- **Bằng chứng mới:** 57 tests cũ đạt trước sửa; suite cuối 109 passed, 0 failed. Tái lập 5/5 Day 5 exact IDs/scores/filters/count/status/fit audit; unit weights match full ranking; 30/30 cấu hình–kịch bản filter/score/order/determinism đạt. Dữ liệu/artefact/code baseline được giữ nguyên, 8.238 rows ranking lưu riêng.
- **Quyết định:** cùng snapshot/hash và query split, không tuning bằng future metadata hay market value; fit không đổi qua query/filter hoặc held-out mutations. Kiểm lặp và đảo dòng/fit IDs, ghi source hash/môi trường/weights trong evaluation.json.
- **Phản biện:** “109 tests pass là đủ đưa ra quyết định mua cầu thủ?” → Không. Tests bảo vệ hợp đồng kỹ thuật, không cung cấp relevance labels, thông tin hợp đồng/chấn thương/chi phí mua, kỹ năng thủ môn/phòng ngự hoặc temporal evaluation.
- **Day 7:** KNN đối chứng cùng representation/reference/filter, cosine distance và tie handling; đo latency/top-K/pool, không tạo ground truth hay suy luận khả năng chuyển nhượng. Model Evaluation chính thức Day 11–12 vẫn còn.
- **Bàn giao:** HANDOFF/inventory và tài liệu hiện hành đã cập nhật Day 6; chưa commit/push/deploy. Source chưa xuất bản/dataset ngoài Git/môi trường chưa cài sạch vẫn là giới hạn chuyển máy.

## 2026-11-02 — Đối chiếu trước Day 7

- Không có insight mới về mô hình hoặc cầu thủ trong phiên kiểm tra này. Lượt chạy mới đạt **109 tests, 0 failed**, 14,60 giây; pip check đạt. 8 dataset khớp manifest và 6 source hashes khớp báo cáo Day 6.
- Làm rõ dependency bàn giao: runner Day 6 cần **reports/day5_recommendation_examples.json** để xác nhận baseline và snapshot, ngoài source và features CSV. CLAUDE/SETUP đã bổ sung yêu cầu này và số tests hiện hành; không tự tái sinh báo cáo Day 5 để che thiếu/mismatch.
- **Phản biện:** “Có tài liệu và 109 tests pass trên máy cũ nghĩa là clone trên máy mới chạy ngay?” → Chưa. Source Day 5–6/docs chưa commit, data bị ignore, environment chưa full lock/fresh-install; cần bàn giao đủ rồi xác minh trên máy đích. Đây là điều kiện tái lập, không phủ nhận kết quả Day 6 đã chạy local.
- Giữ các giới hạn Day 6: weights heuristic, chỉ 4 query nonempty, không relevance labels/temporal evaluation, Defender/GK chỉ context. Day 7 vẫn là kế hoạch KNN đối chứng; không có thay đổi thuật toán hoặc kết luận chất lượng mới trong lượt rà soát.

## 2026-11-02 — Day 7: KNN Benchmark & Robustness

### INS-29 — KNN cosine tương đương truy xuất khi representation không đổi

- **Bằng chứng:** 10 cặp full ranking trên cùng reference/filter Day 5 và weighted Day 6 khớp ordered IDs và score; max score difference=0, max |distance−(1−cos)| theo components=4,44e-16. 8 nonempty overlap@5=1, Spearman≈1; empty null. 178 tests đạt, 0 failed (69 mới).
- **Quyết định:** dùng NearestNeighbors cosine/brute như đối chứng, giữ baseline nguyên trạng. Không gọi KNN là model học relevance hoặc tốt hơn chỉ vì dùng sklearn.
- **Phản biện:** “KNN là thuật toán mới nên phải gợi ý khác/tốt hơn?” → Không. Với cùng vector và cosine distance=1−similarity trên nonzero vectors, cùng thứ tự là kết quả mong đợi. Chưa có relevance labels để đánh giá chất lượng.
- **Giới hạn:** kiểm 4 query thực + 1 empty, không temporal evaluation; GK/Defender chỉ context_profile_only, không phát sinh chỉ số kỹ năng mới.

### INS-30 — Filter và tie phải nằm trong hợp đồng truy xuất

- **Quyết định:** filter age/EUR/minutes/position, loại query/zero candidates trước NN.fit; gọi tất cả neighbors rồi round12 + sort ID, cuối cùng cắt K. Không lấy global Top K rồi filter vì có thể thiếu ứng viên hợp lệ; không để ties ở boundary phụ thuộc thứ tự input/sklearn.
- **Bằng chứng:** 50 trường hợp K=1/3/5/50/10000 đạt prefix/parity; test foot-only GK có >5 người đồng hạng, đảo catalogue/fit IDs vẫn trả đúng ID nhỏ trước. Query 0 trả status rõ, candidate 0 bị loại/đếm; NaN/invalid bị từ chối.
- **Phản biện:** “Dùng quy ước cosine distance của thư viện cho vector 0 có được không?” → Hợp đồng ScoutIQ không gán ranking cho cosine không xác định. Giữ explicit zero semantics của Day 5–6.
- **Giới hạn:** lấy mọi neighbor/brute-force để đảm bảo chính xác ở quy mô hiện tại; chưa benchmark index persistent/ANN hay tối ưu tie-boundary cho tập rất lớn. Adapter cần regression khi baseline nội bộ thay đổi.

### INS-31 — Benchmark phải có scope và điều kiện đo

- **Bằng chứng:** 5 warm-up + 50 repeats/method/query, alternating order, một luồng, 1.000 samples. Cùng K=5/pool, đo full recommend gồm KNN.fit/retrieval/response; không tính scaler fit/CSV/check/report. Raw timing và 20 median/p95 groups lưu reports/day7.
- **Quan sát:** median KNN cao hơn direct ở cả 8 nonempty trong phiên này. Ví dụ weighted Attack direct 4,889 ms (p95 7,154), KNN 6,643 ms (p95 10,116); weighted Defender direct 5,378 (7,968), KNN 7,109 (10,243).
- **Quyết định:** chưa có lợi ích đo được để thay direct; giữ KNN đối chứng. Không chọn dựa vào một lần timing hoặc chất lượng tưởng tượng.
- **Phản biện:** “Có thể kết luận mọi KNN chậm hơn dot product, hoặc p95 này là cloud SLA?” → Không. Đây là đường chạy cụ thể, gồm index fit theo pool và adapter/formatting, trên một máy Windows/phiên; background/CPU jitter còn tồn tại, không cold start/load/cloud/CI confidence interval.
- **Giới hạn:** empty không chạy kneighbors; thời gian ở đó là no-results overhead. Không suy mức tăng latency giữa vị trí thành khác biệt thuật toán hoặc kỹ năng cầu thủ.

### INS-32 — KNN.fit không đồng nghĩa refit scaler hoặc hết leakage

- **Bằng chứng:** preprocessing audits KNN/direct bằng nhau; scaler/categories fit 4.108 reference, loại 4 query; thay held-out metadata không đổi fit statistics. Search/filter và đảo dòng không đổi audit/results.
- **Giải thích:** NN.fit chỉ lưu các vector đã transform thuộc pool tìm kiếm, không học lại mean/scale/category từ query. Dữ liệu lookup có thể chứa candidate-held-out vì đây là retrieval, không được gọi là dự báo độc lập chất lượng.
- **Phản biện:** “Giữ query ngoài scaler fit là đủ để hết leakage?” → Không; metadata tại cutoff, league effects và temporal evaluation vẫn chưa hoàn tất.
- **Day 8:** hoàn thiện filters/hiệu suất đúng chỉ số thật và boundary/no-results tests; giữ privacy/API/cloud ở roadmap riêng, không thêm fake skill/labels. HANDOFF/inventory/architecture đã cập nhật; chưa commit/push/deploy, source/data transfer vẫn cần nghiệm thu trên máy mới.

## 2026-11-02 — Hồ sơ thuyết trình và bảo vệ sau Day 7

### INS-33 — Truy xuất được bằng chứng và phân biệt mức độ kết luận

- **Tài liệu mới:** [PRESENTATION_AND_DEFENSE](PRESENTATION_AND_DEFENSE.md) tổng hợp Day 1–7, mỗi Day 4 Q&A (28 cặp), công thức/lý do, file/đầu ra và link tương đối tới bằng chứng. Đây là tổng hợp lại phát hiện có nguồn, không có insight mô hình hoặc số liệu cầu thủ mới trong phiên này.
- **Quyết định:** sau mỗi Day cập nhật đồng bộ hồ sơ này, project_log, insights_and_defense và HANDOFF; quy tắc được ghi trong AGENTS/CLAUDE. Tách đối chiếu artefact, lịch sử chạy, kiểm tra mới, giả thuyết và kế hoạch; không kể rủi ro giả định như sự cố đã xảy ra.
- **Bằng chứng/giới hạn:** code, báo cáo và Git local xác nhận phạm vi đã có đến Day 7; đọc lại artefact không phải chạy thí nghiệm mới. 178 tests thuộc lần Day 7 trước, không chứng minh scouting relevance, hết leakage hay tái lập trên máy khác. Không thay thuật toán hoặc tạo nhãn để bổ sung thuyết trình.
- **Phản biện:** “Có hồ sơ đầy đủ nghĩa dự án đã hoàn thiện và clone là chạy được?” → Không. Mới hoàn thành phạm vi Day 1–7; backend/UI/DB/auth/chat/cloud còn ở roadmap. Source Day 5–7/docs chưa commit, data bị ignore và fresh-install chưa nghiệm thu. Hồ sơ giúp nhận biết rõ các điều kiện còn thiếu.
- **Phản biện:** “Thứ tự commit Day 4 trước Day 2–3 có mâu thuẫn tiến trình nghiên cứu?” → Commit phản ánh thời điểm lưu nhóm file, không tự chứng minh thứ tự thực hiện. Giữ hash/thứ tự thực, trình bày Days theo công việc và không viết lại lịch sử.

## 2026-11-02 — Day 8: Advanced Filtering & Search Constraints

### INS-34 — Hard constraints phải xác định pool trước ranking

- **Bằng chứng:** 20 legacy checks, 20 scenario–engine cases, 338 tests đạt. Spy test xác nhận KNN chỉ nhận pool hard-filtered; oracle độc lập và đối chiếu full ranking cũ chứng minh không mất ứng viên ngoài Top 5 cũ. Pool 22/10/94/47/0 thống nhất cosine/weighted/KNN cùng dataset/reference.
- **Quyết định:** view riêng của encoded data, không refit scaler/weights, không mutate engine/API cũ. Query được giữ làm vector dù không thỏa tuổi/budget của ứng viên. Không filter danh sách Top 5 cũ.
- **Phản biện:** “Lọc lại Top 5 có đơn giản hơn?” → Có nhưng có thể bỏ sót người hợp lệ ngoài shortlist. Lọc trước retrieval mới đúng hard constraints; giữ regression cho private adapter.
- **Giới hạn:** full eligible ranking và private internals chưa tối ưu/benchmark thêm, không suy throughput hoặc quality từ correctness.

### INS-35 — Đơn vị và missing là một phần hợp đồng tìm kiếm

- **Bằng chứng:** explicit EUR/EUR_million conversion, overflow/NaN/infinity/âm/type/typo/min>max bị từ chối; numeric biên inclusive, role/club IDs kiểm theo snapshot kể cả pool rỗng. Tests dùng dữ liệu thật và biến thể thiếu trong RAM, không sửa snapshot.
- **Quyết định:** max_budget_eur=5 là 5 EUR. Không đoán triệu từ độ lớn. Active hard constraint không biết thuộc tính thì không đạt; foot missing không được gán left/right, club unknown không được xem chắc chắn ngoài exclusion.
- **Phản biện:** “Sao người không thuộc CLB cấm lại bị loại khi club missing?” → Không đủ bằng chứng xác nhận không thuộc CLB cấm. Policy fail-closed được công bố, không diễn giải missing thành một CLB cụ thể.
- **Giới hạn:** exclusion dựa current_club_id, chưa kiểm đúng cutoff; có thể loại người chỉ do thiếu metadata. Market value vẫn không là phí chuyển nhượng/skill. UI tương lai phải hiển thị đơn vị và policy.

### INS-36 — Soft preference không đồng nghĩa sửa điểm tương đồng

- **Quyết định:** foot_mode=soft chỉ xếp người khớp chân trước trong nhóm score round12 bằng nhau, rồi player_id. Không nới hard constraints, không cộng điểm kỹ năng; both là nhãn riêng, không tự đổi nghĩa thành left/right.
- **Bằng chứng:** tie test role-only trên cầu thủ thật, đảo catalogue/fit IDs và direct/KNN đều khớp. Tình huống Kane còn Moukoko chân trái ở hạng 3 sau hai người chân phải vì cosine thấp hơn; Maswanhise thiếu foot vẫn ở Top 5. Đây là đúng soft contract.
- **Phản biện:** “Ưu tiên trái sao không đưa mọi người chân trái lên đầu?” → Đó sẽ là quy tắc ranking khác; Day 8 giữ cosine là tiêu chí chính. Muốn bắt buộc trái dùng hard và chấp nhận pool nhỏ hơn.
- **Giới hạn:** không học sở thích user hoặc xác nhận weights tối ưu. Tất cả threshold là scenario kiểm hành vi. GK từ chối goals/assists constraints; Defender/GK vẫn context-only, không relevance labels hoặc temporal evaluation.
- **Day 9:** chuẩn hóa explanation, dữ liệu so sánh và kiểm truy vết/ties theo roadmap. Không mở rộng sang API/UI/AI chat; chưa commit/push/deploy, chuyển máy vẫn cần source + snapshot riêng và fresh-install.

## 2026-11-02 — Day 9: Recommendation Explainability & Player Comparison

### INS-37 — Evidence là hợp đồng kiểm được, text là phần trình bày

- **Đã kiểm chứng:** [runner](../src/recommendation/run_day9.py) đối chiếu 20/20 response nguyên với Day 8; [evaluation.json](day9/evaluation.json) chứa 80 explanations/32 comparison groups; [tests](../tests/test_explainability.py) kiểm score/rank/ID/unit/components/request tampering và no-refit. Toàn suite cuối 453 passed, 0 failed (59.76s).
- **Quyết định:** [explainability.py](../src/recommendation/explainability.py) giữ response cũ, evidence có nguồn field, raw value/unit/reference/candidate, constraints và missing; text chỉ render từ evidence. Components hoạt động cộng lại bằng score trong tolerance 1e-10; feature weight=0 không nhận đóng góp. explain_response tính lại read-only cùng request để phát hiện stale/tampered response, không fit scaler.
- **Phản biện:** “Có evidence là explanation đã hữu ích cho scouts chưa?” → Chưa. Tests xác minh nhất quán kỹ thuật, chưa có đánh giá người dùng/chuyên gia. Adapter phụ thuộc private internals và đường verify thêm retrieval, chưa đo overhead; JSON chưa là API production.

### INS-38 — Cosine cao không có nghĩa hiệu suất bằng reference

- **Bằng chứng thật:** Barney Stewart là Top 1 weighted tình huống Kane, score 0.956331763076; g90 0.6293706294 so 1.2661439114. Delta −0.6367732821, absolute delta 0.6367732821, relative −50.29233062%. Xem [comparisons.csv](day9/comparisons.csv), [Top 5](day9/top5.csv), [biểu đồ](day9/attack_comparison.png).
- **Giải thích có cơ sở toán:** cosine đo góc vector sau scaling/encoding/weights, không đảm bảo raw metrics bằng nhau. Components là tích tọa độ chuẩn hóa, có thể âm; không causal attribution hoặc phần trăm tài năng. Chưa kiểm chứng trọng số là tối ưu.
- **Phản biện:** “Score 0.956 có nghĩa 95.6% giống kỹ năng Kane?” → Không. Là score phụ thuộc feature/reference/weights của mô hình; thiếu league/tactical/uncertainty adjustments và labels. Raw per90 thấp hơn 50.29% cũng không phải kết luận kỹ năng thấp hơn tương ứng.

### INS-39 — So sánh cần đơn vị và lý do cho giá trị không tính được

- **Quyết định:** [comparison.py](../src/recommendation/comparison.py) nhận 2–5 ID thật, distinct, reference trong nhóm; giữ thứ tự. Signed=candidate−reference; absolute=abs(signed); relative=100×signed/abs(reference). Reference=0 → null/zero_reference, thiếu → null/missing_value; không chia vô cực hoặc điền 0. Tests kiểm zero từ cầu thủ thật, NaN/inf/invalid ID/units/per90/overflow; dữ liệu lỗi chỉ là biến thể trong RAM.
- **Bằng chứng:** 448 dòng numeric và categorical trong 32 nhóm của JSON; mỗi shortlist có reference+Top4, rồi reference+hạng5. Attack/Midfield cùng nhóm có g90/a90, Defender/GK/mixed chỉ context. Market value EUR chỉ bối cảnh/ngân sách; không tổng điểm hoặc tự tuyên bố người tốt hơn.
- **Phản biện:** “Sao không cùng radar goals/assists cho mọi vị trí?” → Dữ liệu này không đo kỹ năng phòng ngự/bắt bóng. Cùng đơn vị chưa đủ làm chỉ số phù hợp; dùng context và ghi giới hạn, không bịa metrics.

### INS-40 — Missing và no-results vẫn cần giữ bằng chứng

- **Bằng chứng:** Maswanhise thiếu foot trong Top 5 weighted Attack; raw value=null và missing_fields có foot. Đây là soft preference, không hard filter; không đoán chân thuận. No-results có request/status/empty_reason, không explanation cầu thủ/comparison giả. Categorical raw match=null nếu thiếu, tách khỏi membership trong vocabulary fit.
- **Phản biện:** “Hai người đều thiếu có được coi giống chân thuận?” → Không. Null là không biết; vector encoding theo baseline vẫn được giữ và giải thích đúng như đã tính, không tự tạo category hoặc đổi score.
- **Hạn chế/Day 10 dự kiến:** cần tích hợp service Python/cấu hình và regression, giữ evidence lineage. Chưa temporal/metadata-at-cutoff audit, labels/expert review, benchmark overhead, fresh-install/chuyển máy. Backend/UI/DB/auth/chat/cloud vẫn roadmap; chưa làm Day 10 hoặc commit/push/deploy.

## 2026-11-02 — Day 10: Integration & Phase Review

### INS-41 — Unified service cần giữ nguyên hợp đồng thuật toán

- **Quyết định:** [service](../src/recommendation/service.py) ghép engine/AdvancedRecommender/Day 9 presenter/comparer; không refactor code cũ. Config phía service tách request, default cosine và weights Day 6 giữ nguyên, không dùng latency/stability để tự tune weights.
- **Bằng chứng:** [evaluation](day10/evaluation.json)/[checks](day10/checks.csv) đối chiếu nguyên 20 responses Day 8 và explanations/comparisons Day 9; 549 tests đạt, 96 mới. JSON deterministic cả 400 measured/60 warm-up, không mutate fitted state. Đây là integration correctness, chưa relevance quality.
- **Phản biện:** “Có service nghĩa đã có FastAPI production?” → Không. Chỉ Python callable + JSON schemas; chưa endpoint/auth/privacy/HTTP/DB. Các private adapters vẫn cần regression khi internals thay đổi.

### INS-42 — Shape validation cần đi cùng domain và cross-field consistency

- **Quyết định:** [schemas](../src/recommendation/schemas.py) dùng Draft 2020-12 để kiểm shape/type, Day 8 validate constraints, thêm native finite JSON/duplicate-key/integer và response consistency. Count qua hard không đồng nhất returned hoặc rankable khi có zero vectors; ghi riêng thay vì gọi mọi số là candidates.
- **Bằng chứng:** tests từ chối float/bool IDs/K, NaN/Inf/overflow, unit/schema/unknown fields, sửa score/rank/text/count/units/components/group. Valid JSON hữu hạn chưa đủ chứng minh dữ liệu đúng: source/candidate/evidence lineage vẫn cần service và hashes. Runtime strict ID integer chặt hơn standard JSON Schema (5.0 có thể được validator chuẩn coi là integer).
- **Phản biện:** “Vì sao cần dependency trực tiếp jsonschema nếu Jupyter có sẵn?” → Service import trực tiếp; khai báo requirement tránh phụ thuộc ngầm vào transitive dependency. Bản 4.26.0 đã có, pip check đạt; chưa chứng minh full lock/máy mới.

### INS-43 — Latency phải gắn với phạm vi đo, không quality hoặc cloud SLA

- **Bằng chứng:** [timings.csv](day10/timings.csv) 400 mẫu, [benchmark.csv](day10/benchmark.csv) 20 case groups, 3 warm-up/20 repeats/case, một luồng/rotate thứ tự. Nonempty median từng case 74,381–141,391 ms, p95 102,959–193,290 ms; empty median 24,718–32,357 ms. Startup một quan sát 1.423,006 ms.
- **Phạm vi:** toàn recommend_json với parse/validation/filter/ranking/explanation/comparison=true/serialization; loại CSV load/fit/startup/HTTP/DB/auth/network. p95 linear, không gộp percentile giữa các case. Chưa profiling từng stage hoặc comparison=false, không quy nguyên nhân overhead riêng.
- **Phản biện:** “So số Day 7 rồi nói service chậm hơn/tốt hơn?” → Phạm vi đo khác, không so trực tiếp. Tải nền và biến động local còn lớn, 20 mẫu/case; chưa concurrency/large dataset/cloud. Không chọn model theo quality từ thời gian/parity.

### INS-44 — Kết thúc phase là chốt ứng viên để đánh giá, không tạo ground truth

- **Quyết định:** [phase review Day 5–10](day10/phase_review.md) chốt integrated local v1, giữ default cosine/weighted hypotheses/KNN benchmark. Không Precision/NDCG khi thiếu nhãn, không market value skill ground truth. Defender/GK chỉ context và thiếu metrics chuyên môn.
- **Phản biện:** “549 tests đạt thì Day 11 còn gì?” → Định nghĩa protocol/rubric/tình huống có nguồn, kiểm leakage và split khả thi, chọn metrics đúng bằng chứng. Tests hành vi không thay expert evaluation hoặc temporal validation; Day 11 chưa triển khai.
- **Bàn giao:** version/hash data + config/audits, source hashes và packages giúp truy vết nhưng chưa guarantee bitwise cross-environment. Source Day 5–10/docs chưa commit, snapshot ngoài Git, fresh-install/máy đích chưa nghiệm thu. Mốc Git Day 10 chờ người dùng khi chuyển máy; không commit/push/deploy.


<!-- DAY11_APPEND_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Day 11 — Protocol, evidence và phạm vi MVP mới (2026-11-03)

### INS-45 — Relevance độc lập với similarity

Protocol/rubric 0–3 đánh giá scenario–player; không lấy score/rank/giá trị thị trường/Gemini làm nhãn. 173 cặp trong 4 demo chưa có assessor/grade, không giả là nhu cầu scout lịch sử. Evidence packet bỏ rank/method/score, shuffle seed 11; vẫn có reputation bias từ tên cầu thủ. Trạng thái: công cụ đã có, hiệu chuẩn rubric/chuyên gia chưa có. Bằng chứng [protocol](day11/evaluation_protocol.md), [rubric](day11/relevance_rubric.md), [template](day11/annotation_template.csv).

**Q:** Similarity cao tại sao không tự gán relevance=3? **A:** Như vậy dùng output làm ground truth và đánh giá vòng tròn. Người chấm độc lập phải xem nhu cầu và evidence; thiếu dữ liệu thì abstain, nhất là kỹ năng Defender/GK.

### INS-46 — Metric có gate và mẫu số công khai

P@K cần labels cho Top K đã trả; Recall/NDCG cần toàn universe có grade; thiếu labels trả null/lý do. Relevant=grade≥2, NDCG gain 2^grade−1; K cố định, ties theo thứ tự service. SYNTHETIC (abstract IDs) P@3=2/3,R@3=1,NDCG≈0,692020 kiểm công thức và đối chiếu sklearn bằng gains; không phải expert labels. Catalogue coverage20/173 và request coverage4/4 chỉ cho demo. Bằng chứng [metrics](../src/evaluation/metrics.py), [evaluation](day11/evaluation.json), [synthetic](day11/synthetic_metrics.json).

**Q:** Chấm Top 5 đủ để tính Recall/NDCG không? **A:** Không biết relevant/ideal gain ngoài Top 5; không giả unjudged=0. Tool chặn. Full eligible labeling hoặc thiết kế sampling khác có phương pháp rõ mới được thay protocol có version.

### INS-47 — Kiểm cutoff không xóa mọi leakage/bias

Audit mới: raw sums/matches của 4.112 ứng viên khớp, date/valuation không vượt cutoff trong tập kiểm; 4.198 integrated <900 phút, retention khác vị trí. Metadata current club/role/foot không as-of; games gồm league/cup/national team, không strength normalization. Phát hiện tuổi floor(days/365.2425) lệch lịch một người: 341429 tuổi 29 thay 30; ghi issue, không sửa snapshot trong Day 11. Bằng chứng [audit JSON](day11/audit_evidence.json), [findings](day11/audit_findings.md).

**Q:** Scaler loại query rồi có thể nói no leakage? **A:** Chỉ chứng minh query không ảnh hưởng fit; chưa có temporal split hoặc metadata lịch sử. Lỗi age boundary và selection>=900 có thể ảnh hưởng pool/context; cần điều tra có version, không kết luận causal hoặc sửa baseline âm thầm.

### INS-48 — MVP anonymous + Neon/Gemini là đổi scope, chưa phải implementation

Người dùng thay auth/OpenAI: MVP Streamlit/FastAPI/Neon/Gemini, không login/signup; auth/sync future. Gemini hiểu yêu cầu/giải thích evidence, Python giữ constraints/ranking; không dùng LLM tạo relevance labels. Neon chung instance nhưng session ownership phải do backend kiểm, không công khai histories. Credential/token phía server, retention/browser clearing cần thiết kế/test. Roadmap mới: Day 11–13 evaluation, 14–17 API+Neon, 18–23 UI+Gemini, 24–27 integration/cloud, 28–31 report/slides/demo. Lịch sử Day 1–10 giữ nguyên.

**Q:** Bỏ login có bỏ privacy không; Gemini có thay engine không? **A:** Không. Anonymous session vẫn cần token/isolation và hạn chế mất truy cập/cross-device. Gemini không tự xếp hạng hoặc nới filters. Đây là yêu cầu tương lai, chưa có endpoint/DB/APIcall/deploy để tuyên bố đã bảo vệ.

### INS-49 — Bàn giao bằng chứng, không chỉ checklist

549 baseline tests chạy mới; 16/16 case-method đạt parity/repeat/filter; số tests cuối/exit code ở [validation](day11/validation.json). Git main/HEAD c4d638c/index giữ nguyên; không fetch/commit/push/deploy, source Day 5–11 chưa commit, data bị ignore. Clone HEAD thiếu source; snapshot/hash + môi trường quan sát chưa chứng minh fresh-install. HANDOFF/SETUP cập nhật lệnh output mới để không ghi đè annotation.

**Q:** Claude Code có thể tiếp tục ngay bằng clone không? **A:** Chưa nếu chỉ clone HEAD hiện tại. Cần bàn giao source khi được phép Git, riêng snapshot đúng hash, cài môi trường và chạy tests trên máy đích. Day 12 chưa làm; thiếu assessor phải giữ relevance bị chặn thay vì tạo kết quả.

<!-- DAY11_APPEND_END -->

<!-- DAY12_APPEND_START -->
**Kiểm thử Day 12: 717 passed, 0 failed (619 cũ + 98 mới), 144,09s; exit code 0.**

## Day 12 — Integrity và readiness (2026-11-03)

### INS-50 — Calendar integrity có bằng chứng, correction chưa áp dụng

[Audit](day12/age_integrity_audit.csv): 4.111 consistent/1 approximate_year_length. ID 341429 DOB 1996-06-12, cutoff 2026-06-12, 10.957 ngày, legacy 29/calendar 30. Raw có 49 DOB thiếu ngoài tập candidates; nguồn DOB ngoài snapshot chưa xác minh. [Proposal](day12/correction_proposal.json) PROPOSED/applied=false, không ghi đè dataset. Age boundary và context scaler cần kiểm tác động riêng khi được phép.

### INS-51 — Selection counts cần mẫu số/thứ tự

[Exclusions](day12/eligibility_exclusions.csv): 4.198 fail minutes, 226 fail freshness độc lập nhưng chỉ 12 loại thêm; không cộng chồng. [Coverage](day12/coverage_analysis.csv): 217/906 nhóm 17–20 giữ lại (23,95%), so với 1.430/2.566 nhóm 25–28 (55,73%). Đây là mô tả selection, không causal/quality. Missing/outlier giữ nguyên, không impute skill.

### INS-52 — Event cutoff khác information availability

[Lineage](day12/feature_lineage.csv) đủ 28 cột, 8 input hashes/read-only audit Day 11 khớp. Metadata CLB/role/foot không as-of; publication/revision times không có, per90 trộn competitions. [Temporal review](day12/temporal_leakage_review.md): chưa có valid temporal holdout; query ID holdout chỉ kiểm fit, không tạo split giả để đạt roadmap.

### INS-53 — Pilot chưa phải expert evaluation

32 pending rows, 8/scenario, seed 12/age strata/SHA256, không rank/score. Registry rỗng, grade/time/assessor trống. [Guide](day12/pilot_annotation_guide.md) giữ rubric 0–3, context-only Defender/GK, uncertainty/abstain và review bất đồng. Validator gắn source/hash/rubric/scope, không trộn provenance. Exact/linear-weighted kappa cần ít nhất 2 raters/2 common items; mẫu số kỳ vọng 0 trả null. Chưa thu/gửi nhãn hoặc chấm thay chuyên gia.

### INS-54 — Readiness phân biệt đạt và bị chặn

[Readiness](day12/evaluation_readiness.md): coverage hành vi tính được từ frozen queries; P/R/NDCG/agreement thật bị chặn, temporal metadata thiếu. Pilot không đủ nhãn toàn 173 cho Recall/NDCG. SYNTHETIC oracle chỉ kiểm công thức, tests schema không chứng nhận nhãn độc lập. **Day 13 dự kiến, chưa triển khai:** xác nhận assessor thật và thực hiện pilot độc lập nếu có; review provenance, uncertainty, abstention và disagreement. Tách pilot khỏi final evaluation; thiếu nhãn thì giữ metrics thật bị chặn. Review chính sách calendar/DOB và quyền áp dụng correction, chỉ tạo snapshot mới và đo tác động trong nhiệm vụ được phép. As-of metadata và temporal split hợp lệ vẫn còn thiếu.

### 5 câu hỏi phản biện

1. **Vì sao tuổi sai dù DOB đúng định dạng?** Công thức cũ int(days/365.2425) cắt phần thập phân; 10.957 ngày nhỏ hơn 30×365.2425=10.957,275 nên ra 29 ngay sinh nhật 30. Bằng chứng này dựa trên DOB snapshot, chưa xác minh nguồn ngoài.
2. **Vì sao chưa sửa ngay?** Nhiệm vụ yêu cầu giữ baseline. Proposal lưu parent hashes và old/new values, chưa có quyền promote dataset mới. Tuổi đi vào filter và Defender/GK scaler nên cần kiểm tác động toàn nhóm, không sửa một ô âm thầm.
3. **32 mẫu và hai người chấm đủ kết luận quality chưa?** Chưa. Pilot kiểm quy trình/rubric, không đại diện toàn 173 hoặc 4.112. Hiện chưa có hai bộ nhãn độc lập; agreement cao cũng không chứng minh nhãn đúng. Recall/NDCG cần đủ nhãn toàn eligible universe theo protocol.
4. **Cutoff pass có nghĩa no leakage?** Không. Event date khác publication time; metadata CLB/vai trò chưa as-of, percentiles toàn catalogue không được dùng vào temporal train/test. Query holdout chỉ kiểm fit; ngưỡng phút và hỗn hợp giải còn selection bias.
5. **Claude Code tiếp tục thế nào, MVP mới có ảnh hưởng không?** Đọc AGENTS/CLAUDE/HANDOFF và reports/day12, nhận source chưa commit cùng snapshot đúng hash, chạy tests trên máy mới. FastAPI/Neon/Streamlit/Gemini chưa triển khai; auth/sync là Future Development. Không dùng Gemini tạo labels hoặc ranking.

<!-- DAY12_APPEND_END -->

### Day13 — Nội dung bảo vệ và bàn giao

Mục tiêu: chuyển từ template sang intake/review có kiểm chứng provenance, bảo toàn nhãn và nguồn. Input: 8 dataset frozen, source/evidence Day11–12, CSV/registry riêng nếu có. Output: JSON coverage/readiness/queue cùng hashes, không sửa ranking. Thuật toán: validate hợp đồng → group theo scenario/assessor → đếm missing/pending/abstain/graded/uncertainty → so grade từng cặp trên common items → giữ bất đồng để coordinator review; agreement kế thừa công thức Day12.

Khó khăn thực tế: chưa có người chấm, nên kết quả thật bị chặn. Checkpoint trước gặp quyền thư mục pytest tạm; Day13 dùng --basetemp mới ngoài repo. Chưa có temporal metadata và DOB độc lập, không sửa dataset. Unit fixtures có ghi rõ SYNTHETIC, gồm các khai báo human giả lập chỉ trong tests để kiểm contract, không chuyển vào báo cáo chất lượng.

1. **Tại sao queue rỗng?** Vì chưa có assessor; không có bằng chứng rằng các chuyên gia đồng thuận.
2. **Tại sao missing khác pending/abstain?** Missing chưa nộp hàng; pending chưa quyết định; abstain đã xem nhưng thiếu bằng chứng. Cả ba không thành grade0.
3. **Hai ID đã chứng minh độc lập chưa?** Chưa; registry declaration cần review bằng chứng người thật, ngoài khả năng validator.
4. **Tại sao không sửa tuổi ngay?** Phép tính đã có đề xuất, nhưng nguồn DOB/chính sách và quyền áp dụng chưa đủ; cần snapshot mới và review tác động trước promote.
5. **Có thể làm Day14 khi chưa có quality metrics?** Có thể tiếp tục kỹ thuật theo nhiệm vụ, nhưng phải giữ blockers và không tuyên bố quality/production đã đạt.
