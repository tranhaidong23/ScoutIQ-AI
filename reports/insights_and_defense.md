# ScoutIQ — Data Science Insights & Defense Notes

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
