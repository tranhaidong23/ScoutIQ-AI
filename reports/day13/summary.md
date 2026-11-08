# Day 13 — Pilot intake và review readiness

Ngày thực hiện: 2026-11-06. **Hoàn thành phần công cụ local và tài liệu; thực hiện pilot với người thật vẫn bị chặn.** Người dùng xác nhận chưa có assessor hoặc file đã chấm. Không đánh dấu hoàn thành đánh giá chất lượng tuyển trạch.

- Input thật: snapshot 4.112 × 28, 8 dataset đúng SHA-256; pilot Day12 seed12 gồm 32 hồ sơ trong 173 cặp scenario/player. Runner kiểm source/evidence frozen và tái dựng manifest từ snapshot trước khi review.
- Kết quả: **32 pending, 0 graded, 0 abstain đã ghi, 0 assessor, 0 reviewed human grades**. Queue rỗng vì chưa có người chấm, không phải không có vấn đề. Agreement theo scenario bị chặn; final relevance metrics null.
- Thêm `src/evaluation/review.py`, `run_day13.py`, `tests/test_day13_review.py`. Không dependency mới. Nhận một hoặc nhiều CSV cùng registry tường minh; kiểm trùng xuyên file, version/scope/identity/grade; từ chối SYNTHETIC trong luồng production và pending chưa gán assessor khi registry không rỗng.
- Coverage phân biệt missing submission, pending, graded, abstain theo người/scenario; uncertainty định tính không phải xác suất. Queue giữ bất đồng dù chỉ có một common item; agreement vẫn cần ít nhất hai common graded items. Không tự adjudicate hoặc sửa bản chấm.
- Ghi hash input và source, không sao chép free-text notes/evidence/review_evidence hoặc đường dẫn file riêng vào JSON. Pseudonymous assessor IDs và grade vẫn xuất hiện: review thực cần lưu ngoài repository công khai.
- Correction Day12 vẫn **PROPOSED, applied=false, approval=null**. Không áp dụng sửa tuổi, không đổi eligibility/scaler/ranking/API. Quyết định hoãn ở [correction decision](correction_decision.md).
- Validation: xem [validation.json](validation.json). Tests mới: 25 passed in 9.61s. Toàn suite: **742 passed, 0 failed — 762.99s**, exit code0 (717 cũ +25 mới).

Bằng chứng: [review.json](review.json), [queue](review_queue.json). Hướng dẫn [workflow](pilot_review_workflow.md), [final evaluation plan](final_evaluation_plan.md), [phase review](phase_review.md). Đây là review của dữ liệu frozen, không phải benchmark ranking mới hoặc temporal evaluation.
