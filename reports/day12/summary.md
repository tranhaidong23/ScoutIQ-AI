# Day 12 — Data Integrity, Annotation Pilot & Evaluation Readiness

Kiểm tra mới 2026-11-03. **Hoàn thành audit, thiết kế correction có phiên bản, bộ pilot chưa chấm và công cụ readiness.** Chưa có human relevance/agreement; correction chưa áp dụng; không triển khai Day 13 hoặc web/database/API provider.

**Kiểm thử cuối: 717 passed, 0 failed (619 cũ + 98 mới), 144,09s; exit code 0.** Xem lệnh và kiểm tra bảo toàn trong validation.json.

- [Age audit](age_integrity_audit.csv): **4.112 người**, 4.111 nhất quán, 1 lỗi xấp xỉ ở ID 341429; [findings](age_integrity_findings.md), [differences](age_discrepancies.csv). Snapshot 29, calendar 30, DOB 1996-06-12, cutoff 2026-06-12. Candidate DOB hợp lệ 4.112/4.112; raw 50.149 có 49 DOB thiếu, 0 duplicate IDs.
- [Correction proposal](correction_proposal.json): **PROPOSED**, applied=false, approval=null; chưa dataset mới, không đổi canonical paths/scaler/weights/eligibility/ranking/API.
- [Provenance audit](provenance_audit.md): hash 8 inputs/lineage 28 cột; [coverage](coverage_analysis.csv) theo vị trí/tuổi/current-club league proxy; [exclusions](eligibility_exclusions.csv) đủ 8.322 IDs. Minutes loại 4.198, freshness loại thêm 12 → 4.112; fail độc lập freshness 226, không cộng chồng sai.
- Missing còn 24 foot/23 height/16 tên CLB ở mỗi cột tên; height 19 cm ID 743556 giữ cờ review; numeric infinity 0. Metadata lịch sử/nguồn ngoài chưa xác minh, mixed competitions không được chuẩn hóa strength. [Temporal review](temporal_leakage_review.md): **chưa temporal split hợp lệ**.
- [Pilot template](pilot_annotation_template.csv): **32 rows pending**, 8/scenario, seed 12, age strata + SHA256, tái lập khi đảo rows. [Guide](pilot_annotation_guide.md), [manifest](pilot_manifest.json), [evidence](pilot_evidence.csv). Không rank/similarity/model trong packet, GK/Defender chỉ context, không giả assessor/grade.
- [Readiness](evaluation_readiness.md): Precision/Recall/NDCG/agreement thật **BLOCKED**, JSON metrics null. Registry rỗng; không dùng synthetic làm chất lượng. Có validator/provenance gates và công cụ pairwise exact/linear-weighted kappa khi đủ nhãn phù hợp.

Code mới: [integrity.py](../../src/evaluation/integrity.py), [pilot.py](../../src/evaluation/pilot.py), [run_day12.py](../../src/evaluation/run_day12.py). Tests: [integrity](../../tests/test_day12_integrity.py), [pilot](../../tests/test_day12_pilot.py). Baseline chạy mới 619 passed/0 failed; 98 tests Day 12 riêng đạt. Kết quả full suite cuối và bảo toàn file/index xem [validation.json](validation.json).

Chạy lại `.venv\Scripts\python.exe -B -m src.evaluation.run_day12 --output-dir reports/day12_recheck` với thư mục mới; không overwrite annotations/data. Raw/processed ngoài Git cần snapshot hash đúng; chưa fresh-install/máy mới. Không commit/push/deploy. Day 13 chỉ là kế hoạch trong readiness/HANDOFF, chưa triển khai.
