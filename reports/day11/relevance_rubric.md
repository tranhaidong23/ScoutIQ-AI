# Relevance rubric v1 — Day 11

Đối tượng: mức phù hợp **hồ sơ với một scenario đã cố định**, không đánh giá cầu thủ tuyệt đối. Trạng thái: **rubric dự thảo có thể thực hiện, chưa được chuyên gia hiệu chuẩn**. Không lấy similarity, thứ hạng, market value, danh tiếng hoặc kết quả Gemini làm nhãn. Xem [protocol](evaluation_protocol.md) để biết universe, quy tắc metric và provenance.

## Bốn phần phải ghi bằng chứng

- **Hard constraints:** vị trí/sub-position, khoảng tuổi, EUR, phút, per90 khi có, chân thuận hard, CLB bị loại. Ghi số thực/đơn vị/cutoff và pass/fail/unknown; tất cả là AND ngoài danh sách OR trong cùng trường. Nếu packet không thỏa hard constraint, dừng kiểm tra pipeline; không lặng lẽ xóa người đó khỏi universe. Trường hợp xác nhận không phù hợp chấm 0 và ghi sự cố; metric chỉ phát hành sau xử lý sai universe có version.
- **Role:** loại vai trò thật trong dữ liệu và nhu cầu được mô tả. Sub-position là nhãn thô, không đủ tactical fit/formation. Reference là ngữ cảnh, không phải ground truth. Soft foot không loại candidate và không tự động cộng điểm.
- **Performance:** Attack/Midfield dùng goals/90, assists/90 và số phút trong bối cảnh nguồn. Không cộng lại goals+assists+contributions hoặc xem cao hơn là tốt hơn tự động. Defender/GK: chỉ hồ sơ tuổi/phút/chân thuận/vai trò; phần kỹ năng phòng ngự/bắt bóng ghi **không đủ dữ liệu**, không suy từ bàn thắng.
- **Evidence quality:** nguồn/cutoff/độ đầy đủ, thiếu metadata, mẫu phút, hỗn hợp giải đấu, sự phù hợp loại metric với vai trò. Minutes reliability là heuristic, không phải confidence interval. Có thể có đủ evidence cho context suitability nhưng thiếu evidence cho sporting quality; phải ghi đúng phạm vi trong notes.

## Thang điểm 0–3 (relevant = grade ≥2)

| Grade | Định nghĩa và điều kiện |
|---:|---|
| 0 — Không phù hợp có bằng chứng | Có hard constraint bị vi phạm đã xác nhận, hoặc có bằng chứng rõ hồ sơ/vai trò trái với yêu cầu đã cố định. Ghi lý do cụ thể; **không dùng 0 cho dữ liệu thiếu/chưa chấm**. |
| 1 — Phù hợp yếu | Hard constraints đạt nhưng role/performance trong phạm vi có dữ liệu chỉ hỗ trợ yếu cho nhu cầu; ghi hạn chế cụ thể có bằng chứng. Không tự chấm 1 chỉ vì thiếu chỉ số phòng ngự. |
| 2 — Phù hợp để xem xét | Hard constraints đạt; role và bằng chứng hiệu suất/bối cảnh liên quan đủ hỗ trợ đưa vào shortlist review, kèm caveat. Không đồng nghĩa nên ký hợp đồng. |
| 3 — Phù hợp mạnh trong phạm vi đánh giá | Hard constraints đạt; nhiều bằng chứng liên quan, nhất quán, có nguồn và lý giải độc lập hỗ trợ ưu tiên xem xét cho scenario. Không đồng nghĩa tốt hơn mọi cầu thủ, không yêu cầu bắt chước rank của engine. |
| Trống — Abstain/unlabeled | Không đủ bằng chứng quan trọng, chưa có assessor, chưa giải quyết mâu thuẫn nguồn hoặc nhu cầu chưa rõ. Ghi lý do trong notes; không tính là grade 0. |

Đây là quy tắc định tính, không ép một công thức số giả làm nhãn. Mức 2/3 cần assessor giải thích sự khác biệt; trước đánh giá thật nên hiệu chuẩn rubric trên ví dụ pilot riêng, ghi bất đồng và sửa phiên bản **trước** chấm test set. Không ép distribution số lượng grade.

## Hướng dẫn theo scenario

| Scenario | Evidence được phép dùng hiện tại | Kết luận không được phép |
|---|---|---|
| Tiền đạo trẻ ngân sách thấp | Tuổi/phút/EUR/vai trò; goals/90 cùng assists/90 có nguồn; soft foot chỉ preference | “Rẻ nên kỹ năng thấp”, “giống Kane nên sẽ ghi bàn như Kane” |
| Tiền vệ kiến tạo | Attacking Midfield, chân trái hard, assists/90 và mẫu phút; giới hạn không có xA/chances created | “Assists chứng minh sáng tạo nhân quả”, “similarity là xác suất thành công” |
| Hậu vệ kinh nghiệm | Centre-Back, tuổi/phút/chân phải/giá trị/CLB, metadata có caveat | Xếp hạng tackling, aerial duels, positioning từ tuổi/phút hoặc goals |
| GK trong ngân sách | Tuổi/phút/chân phải/EUR, metadata vị trí | Suy save ability, PSxG, clean sheets, distribution từ goals/assists |

**Defender/GK grade nếu có chỉ dành cho context-profile suitability.** Không gộp chúng thành metric kỹ năng chung với Attack/Midfield. Nếu người chấm cần năng lực chuyên môn phòng ngự/bắt bóng để quyết định, abstain cho đến khi có evidence mới có nguồn.

## Trường annotation và lưu trữ

[annotation_template.csv](annotation_template.csv): `scenario_id, player_id, assessor_id, timestamp, relevance_grade, evidence, notes, label_source`. `timestamp` là lúc đánh giá, không phải cutoff dữ liệu. `evidence` nên ghi `source_path/hash; field=value unit; cutoff; reasoning`, không cần chép thông tin riêng tư. `notes` ghi role/performance scope, uncertainty, abstain/adjudication.

- `independent_human`: người thật chấm độc lập theo protocol; phải được coordinator kiểm tra provenance. Code không thể chứng minh tính độc lập chỉ từ chuỗi này.
- `SYNTHETIC`: fixture toán học tách biệt, không gắn nhãn giả cho 173 cầu thủ; không đưa vào metric chất lượng thực.
- `unlabeled`: trạng thái toàn bộ template hiện tại, không có assessor/grade/time giả. Khi thiếu thông tin sau review vẫn có thể giữ unlabeled với notes.

Lưu nhãn thật vào bản sao riêng của template; không sửa artefact mẫu đã đóng băng hoặc ghi secrets/thông tin cá nhân vào Git. Không trộn nhiều nguồn/người chấm trong một lần `assess_ranking`; chọn bộ nhãn rõ ràng trước, giữ bản gốc để audit. Chưa thu thập nhãn hoặc triển khai adjudication trong Day 11.
