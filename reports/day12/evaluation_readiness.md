# Day 12 — Evaluation readiness checklist

Bằng chứng máy đọc: [readiness.json](readiness.json), [audit.json](audit.json), [manifest](pilot_manifest.json). Hiện **32 pending, 0 graded, 0 abstain đã ghi, 0 assessor**; 173 rows Day 11 vẫn chưa có nhãn. “Không có abstain” ở đây chỉ vì chưa có người chấm, không có nghĩa evidence đã đủ.

| Hạng mục | Điều kiện | Trạng thái hiện hành |
|---|---|---|
| Snapshot/lineage | Đúng hash 8 inputs, đủ28 cột, code truy vết, ID/cutoff được kiểm | Đạt kiểm nhất quán nội bộ; nguồn ngoài chưa xác minh |
| Age integrity | Audit hết4.112, phân loại DOB và công thức | Đạt audit; **1 correction PROPOSED**, chưa áp dụng |
| Pilot reproducibility | Universe173, seed/version/sample32, không dùng ranking | Đạt; đảo rows vẫn cùng sample |
| Annotation schema | IDs/grade/metadata/assessor/time/evidence hợp lệ | Template đạt pending; chưa có completed human records |
| Precision@K | Assessor độc lập được review; toàn bộ returned Top K có grade; K cố định, empty policy rõ | **BLOCKED**, chưa labels. Chấm pilot có thể không phủ Top K; không coi thiếu là0 |
| Recall@K | Full eligible universe của scenario có grade; có relevant grade≥2 | **BLOCKED**. Pilot8 không đủ cho pools22/10/94/47 |
| NDCG@K | Full universe có grade để biết IDCG; gain2^grade−1; IDCG>0 | **BLOCKED**, không dùng subset/pilot làm ideal của catalogue |
| Label coverage | Đếm grade thật theo assessor/universe | 0/173 hiện tại; pilot chuẩn bị32/173 không phải label coverage |
| Catalogue/request coverage | Universe/query/method/returned IDs đã đóng băng | Tính được từ Day11 frozen results; là hành vi, không quality |
| Inter-rater agreement | ≥2 bộ độc lập cùng version/scope, ≥2 common graded items; ghi paired coverage | **BLOCKED**, registry trống. Không chấm thay chuyên gia |
| Temporal evaluation | As-of metadata + availability times + split/labels hợp lệ | **BLOCKED**, xem temporal review |
| Production/web/privacy | FastAPI/Neon/Streamlit/Gemini/session isolation | Chưa triển khai; không phải đầu ra Day12 |

Readiness đọc **Top5 và universe đã đóng băng trong Day11**, kiểm hashes/source; không gọi đó là benchmark ranking mới. Suite regression cũ được chạy lại trong phiên Day12 để bảo vệ API/ranking. Công cụ readiness chỉ nhận K≤5 với record Top5 hiện tại; không giả có full ranking khi K lớn hơn.

Mỗi assessor được xét riêng; không chọn người cho metric cao nhất. `independence_confirmed` cần coordinator review ngoài code. SYNTHETIC bị loại khỏi gate human mặc định. `actual_relevance_metrics` và `actual_agreement_summary` trong JSON đều null, không phải0. Với nguồn có labels hợp lệ sau này mới dùng metrics Day11 và report đúng universe/scope; bộ pilot không thay thế annotation toàn173.

## Điều kiện chuyển công việc Day13 (chưa triển khai)

1. Xác nhận người chấm và provenance; thực hiện pilot độc lập nếu có, giữ bản gốc và review disagreement/uncertainty, không dùng model labels.
2. Review chính sách sửa tuổi/DOB và quyền áp dụng. Nếu chưa được phép giữ proposed; nếu được phép, tạo snapshot mới và đánh giá tác động có version trước promote, giữ baseline.
3. Quyết định final evaluation queries/pool/split và evidence cần thêm. Nếu vẫn thiếu human labels hoặc as-of metadata, công bố phần bị chặn, tiếp tục đánh giá hành vi trong phạm vi được giao; không bịa kết quả relevance/temporal.
4. Chưa làm FastAPI/Neon/Gemini hoặc deploy; scope MVP anonymous và lịch31 ngày vẫn theo AGENTS/HANDOFF.
