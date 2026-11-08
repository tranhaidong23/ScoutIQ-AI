# Day 12 — Age integrity, ngày sinh và phương án sửa có phiên bản

Kiểm tra mới 2026-11-03. Nguồn: [audit.json](audit.json), [4.112 dòng audit](age_integrity_audit.csv), [dòng khác biệt](age_discrepancies.csv), [code](../../src/evaluation/integrity.py). Không sửa raw, processed, engine hoặc API. Ngày kiểm tra không phải cutoff dữ liệu: cutoff vẫn **2026-06-12**.

## Kết quả toàn bộ ứng viên

| Kiểm tra | Kết quả mới |
|---|---:|
| Ứng viên / ID duy nhất | 4.112 / 4.112 |
| DOB parse hợp lệ, không tương lai, tuổi theo lịch 0–100 | 4.112 |
| Tuổi snapshot = công thức cũ = tuổi theo lịch | 4.111 |
| Sai khác do số ngày/năm xấp xỉ | 1 |
| DOB thiếu/không hợp lệ/xung đột hoặc không tìm thấy raw trong ứng viên | 0 |
| Player rows raw | 50.149 |
| DOB raw thiếu / hợp lệ | 49 / 50.100 |
| Raw DOB không trống nhưng pandas parser cũ trả NaT | 0 |
| Raw duplicate player IDs | 0 |

49 DOB thiếu ở toàn raw không nằm trong 4.112 ứng viên. Không suy nguyên nhân bị loại của 49 người từ kiểm tra này: pipeline còn phụ thuộc mùa, appearances, join và định giá. Các phân loại ngày là kiểm tra nội bộ snapshot, **không xác nhận DOB ngoài đời từ nguồn độc lập**.

| player_id | Tên | DOB raw | Cutoff | Snapshot / công thức cũ | Calendar age | Nguyên nhân |
|---:|---|---|---|---:|---:|---|
| 341429 | Davinson Sánchez | 1996-06-12 00:00:00 | 2026-06-12 | 29 / 29 | 30 | `approximate_year_length` |

Raw `players.csv.gz`, bản ghi CSV số **20.869** (đếm header là dòng 1), một bản ghi DOB, 10.957 ngày sống. Công thức [clean_data.py](../../src/preprocessing/clean_data.py) dùng `int(days / 365.2425)` khi days≥0. Vì `30 * 365.2425 = 10957.275`, phép chia rồi cắt phần thập phân trả 29 ngay sinh nhật 30. Đây là lỗi xấp xỉ ở boundary theo DOB hiện có, không phải thiếu dữ liệu hay chuyển nhầm ngày/tháng trong snapshot này.

## Chính sách parsing và kiểm thử

Audit nhận ISO `YYYY-MM-DD` hoặc timestamp midnight `YYYY-MM-DD 00:00:00`/`T00:00:00` (phần thập phân toàn 0 được phép). Không đoán `dd/mm` với `mm/dd`; không tự đổi timezone hoặc bỏ giờ khác midnight. Phân loại missing, invalid format, invalid calendar, future DOB, age>100, DOB conflict, invalid snapshot age, sai khác công thức và sai khác chưa giải thích. Audit không thay parser production.

Tuổi theo lịch: `cutoff.year - dob.year - ((cutoff.month, cutoff.day) < (dob.month, dob.day))`. Người sinh 29/2 được tính sang tuổi mới vào 1/3 năm không nhuận theo quy ước tuple này; đây là **chính sách dữ liệu cần phê duyệt**, không khẳng định quy tắc tuổi pháp lý. Cutoff bắt buộc một ngày ISO rõ ràng. Tests có ngày trước/đúng/sau sinh nhật, năm nhuận, đổi năm, tuổi 0/100, tương lai, parsing sai, duplicate/conflicting DOB, ID sai và giữ nguyên input.

## Versioned correction — chỉ PROPOSED

[correction_proposal.json](correction_proposal.json) chứa version `scoutiq.age-calendar.v2.proposed`, old/proposed value, DOB/cutoff, hash 8 inputs, `applied=false`, `approval=null`. Không có hàm apply tự động và **không tạo dataset sửa** trong Day 12.

Quy trình dự kiến khi có nhiệm vụ cho phép:

1. Review DOB/source evidence và chính sách calendar/leap-day; xác nhận phạm vi sửa. Nếu evidence xung đột, giữ proposed hoặc blocked; không chọn tùy ý một DOB.
2. Kiểm lại input hashes; tạo thư mục phiên bản mới `data/processed/versions/<approved-version>/`, manifest dẫn về parent snapshot/hash, version code/cutoff, diff từng ID/cột. Không ghi đè tên file canonical hiện tại, không sửa raw.
3. Kiểm ID/schema/per90 và các cột phụ thuộc; giữ bản cũ. Correction dataset cần được kiểm như một phiên bản riêng, không sửa test expected của baseline để che regression.
4. Tuổi vừa là hard filter vừa là numeric context feature Defender/GK. Đo tác động bộ lọc tuổi, reference scaler/config hash, scores/ranking/explanations theo hai phiên bản, cùng query. Không khẳng định sửa một hàng chỉ ảnh hưởng một kết quả: refit scaler có thể ảnh hưởng cả nhóm.
5. Chỉ đổi service configuration/dataset version khi được phép promote. Rollback dùng nguyên snapshot/config cũ, không reset Git hoặc xóa lịch sử.

Day 2 eligibility không lọc tuổi, nhưng điều này **không** đủ để tuyên bố search pools/ranking bất biến. Day 12 chưa áp dụng sửa hoặc đo ranking trên dữ liệu sửa; yêu cầu giữ nguyên ranking/scaler/weights/eligibility/API được tuân thủ.
