# Day 12 — Hướng dẫn pilot annotation

**Trạng thái: bộ pilot đã chuẩn bị/kiểm thử, chưa có người thật chấm.** [Template](pilot_annotation_template.csv) có **32 hàng pending/unlabeled**, assessor/time/grade để trống. [Registry](assessor_registry.json) hiện là `{}`; không tạo danh tính chuyên gia. [Manifest](pilot_manifest.json) lưu sample IDs/version/seed/hash/strata; [evidence](pilot_evidence.csv) là số liệu thật, không chứa model/rank/similarity.

## Lấy mẫu và phạm vi

Tái dùng 4 demo Day 8–11, không giả là yêu cầu lịch sử của CLB. Universe 22 tiền đạo / 10 tiền vệ / 94 hậu vệ / 47 GK =173 cặp. Chọn **8 mỗi scenario** (32 tổng), seed **12**. Chia strata theo tuổi snapshot 0–16/17–20/21–24/25–28/29–32/33–36/37+; round-robin strata, thứ tự trong strata dùng SHA-256 của version/seed/scenario/ID. Sau chọn, sắp evidence theo cùng hash. Đảo rows/scenarios/IDs không đổi sample; không dùng rank/score để chọn.

Pilot kiểm độ rõ rubric, evidence, abstention và luồng bất đồng. Tỷ lệ chọn khác nhau giữa pool; không suy metric trên 32 người thành chất lượng trên 173 hoặc 4.112, không dùng pilot đã hiệu chỉnh làm final test. Không dùng thống kê tuổi audit đã sửa trong evidence: snapshot vẫn 29 ở ID 341429; correction proposed không được tự trộn vào annotation.

## Rubric và evidence

Giữ nguyên [rubric 0–3 Day 11](../day11/relevance_rubric.md), version `scoutiq.relevance.v1`: 0 không phù hợp có bằng chứng; 1 yếu; 2 phù hợp để review; 3 phù hợp mạnh trong **phạm vi đã có evidence**. Relevant ≥2. Thiếu dữ liệu/không thể kết luận → **abstain**, không chấm 0 thay missing. Hard constraints phải kiểm trước; soft foot không phải hard fail hay điểm skill. Không lấy similarity, danh tiếng, market value hoặc Gemini làm nhãn.

Attack/Midfield có evidence g90/a90 và phút; chưa xG/xA/context đối thủ. Defender/GK chỉ `context_profile_only` (tuổi/phút/vai trò/chân thuận/giá trị), các ô goals/assists trong packet để trống vì **không thuộc phạm vi đánh giá**, không phải suy dữ liệu nguồn bằng 0. Missing metadata thực ghi riêng `missing_fields`; `known_limitations` nêu phần không đủ bằng chứng. Người chấm bổ sung `missing_evidence`/notes, không bịa metrics.

## Schema và quy trình

Template giữ 8 trường Day 11, thêm `pilot_version,dataset_sha256,rubric_version,assessment_scope,decision_status,uncertainty,missing_evidence`. CSV v1 phải đúng header; reader riêng [pilot.py](../../src/evaluation/pilot.py) không thay loader/contract Day 11.

1. Coordinator sao chép template ra file riêng cho từng assessor thật. Đăng ký pseudonymous ID theo `[A-Za-z][A-Za-z0-9_-]{2,63}`, không dùng email/tên riêng; registry gồm `label_source`, boolean `independence_confirmed`, `review_evidence`. Không bật confirmed khi chưa review độc lập; không ghi secrets/thông tin cá nhân vào repo công khai.
2. Phát cùng scenario/rubric/dataset/evidence version cho ít nhất 2 người. Ẩn engine/rank/score và nhãn người khác đến khi khóa nhãn; tên cầu thủ vẫn thấy nên reputation bias chưa loại hết. Không gửi email/mời assessor tự động trong Day 12.
3. `pending`: unlabeled, grade/time/uncertainty trống. `graded`: assessor đăng ký, timestamp ISO có timezone, grade nguyên 0–3, evidence rõ nguồn/field/đơn vị/cutoff, uncertainty `low|medium|high`, source khớp registry. Uncertainty là tự đánh giá định tính, không confidence probability.
4. `abstain`: source unlabeled, grade trống, có assessor/time/uncertainty và lý do trong missing_evidence hoặc notes. Không biến abstain thành grade0, không điền nhãn trung bình.
5. Validate schema/ID/duplicates/grade/metadata/scope/provenance bằng `load_pilot_annotations` → `validate_pilot_annotations(rows, manifest, registry)`. Bản ghi ngoài sample, duplicate cùng scenario/player/assessor, case-alias assessor, mix dataset/rubric/scope, NaN/Inf/bool/float grade hoặc người chưa đăng ký đều lỗi.
6. Giữ nguyên bản nhãn gốc từng người. Bất đồng được xuất theo cặp ID/grade, rồi review evidence/adjudication trong phiên bản riêng; ghi lý do thay đổi, không sửa nhãn để tăng agreement. Chưa có adjudication thực tế trong Day 12.

Registry chỉ là khai báo có chứng cứ cần review, code không chứng minh hai ID là hai người thật độc lập. SYNTHETIC chỉ dùng unit fixtures; không chấp nhận như nhãn thật trong readiness mặc định.

## Agreement có điều kiện

Chỉ mở khi có ít nhất hai assessor phù hợp, confirmed và có **ít nhất 2 item cùng được chấm** trong cùng scenario/version/scope. Báo pairwise, không gộp Attack performance và GK context thành một chất lượng chung. Tính exact agreement và Cohen kappa với trọng số **linear**, labels0–3. Tham khảo [định nghĩa chính thức sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html); tests đối chiếu công thức bằng fixture SYNTHETIC.

Linear disagreement `d(a,b)=|a−b|/3`; κ = `1 − observed_disagreement / expected_disagreement` theo marginal labels hai người. Expected=0 (cùng một constant grade) → κ null + lý do; exact agreement có thể 1, không tự gọi κ=1. Thiếu common items → null/blocked. Báo số paired/pilot, abstain/pending và danh sách bất đồng; agreement chỉ trên common graded items có thể bị selection bias. Hai item là ngưỡng tính toán tối thiểu, không phải bằng chứng thống kê đủ mạnh hay tiêu chuẩn expert quality.

Hiện **0 assessor, 0 labels**, vì vậy không có agreement thực để công bố. Không đưa số synthetic trong unit tests vào báo cáo chất lượng.

## Chạy và nhập bản chấm sau này

```powershell
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day12 --output-dir reports/day12_recheck
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
```

Output phải là thư mục mới. Runner chỉ tạo pilot trống/audit, **không tự nhập, gửi hoặc thu nhãn người thật**. Khi có bản chấm, đọc qua Python API trên, review registry, chọn từng scenario cho `agreement_report` và `readiness_report`. Đây là công cụ sẵn sàng, chưa có dữ liệu chấm cần chạy hiện tại. POSIX dùng `.venv/bin/python`.
