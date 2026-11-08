# Day 11 — Protocol, relevance assessment tooling và audit

Kiểm tra mới 2026-11-03. Day 11 hoàn thành phần protocol/công cụ/audit; **chưa có relevance assessment của người thật**. Không triển khai Day 12 hoặc backend/Neon/Gemini.

**Kiểm thử cuối: 619 passed, 0 failed (549 cũ + 70 Day 11), 139,00s**, exit code 0. Nội dung lịch sử 10 tài liệu được bảo toàn; 102 file cũ khác trong manifest trước phiên không đổi, gồm dữ liệu/source/tests/artefact và Git index. Không có liên kết tương đối hỏng trong bộ tài liệu được kiểm tra.

- [Protocol](evaluation_protocol.md), [rubric 0–3](relevance_rubric.md), [audit](audit_findings.md).
- [Module metrics](../../src/evaluation/metrics.py), [audit reader](../../src/evaluation/audit.py), [runner](../../src/evaluation/run_day11.py), [tests](../../tests/test_evaluation_protocol.py).
- [Annotation template](annotation_template.csv): 173 hàng chưa chấm; [evidence packet](annotation_evidence.csv): dữ liệu thật, không rank/score/method, Defender/GK không có goals/assists trong packet. Không gắn nhãn giả cho cầu thủ thật.
- [Evaluation JSON](evaluation.json): dataset/config/source/environment, 4 demo × 4 methods, 16/16 full-response parity Day 10 + repeat/filter đúng; [raw audit JSON](audit_evidence.json): hash 8 inputs và probes chỉ đọc.
- [SYNTHETIC metrics](synthetic_metrics.json): P@3=0,666667; R@3=1; NDCG@3=0,692020 (gain 2^grade−1). Chỉ kiểm toán học, không phải kết quả scouting. Không trộn với nhãn thật.

| Demo | Hard pool | Top K mỗi method | Relevance labels | P@5 / R@5 / NDCG@5 thực |
|---|---:|---:|---:|---|
| Tiền đạo trẻ | 22 | 5 | 0 | null / null / null |
| Tiền vệ kiến tạo | 10 | 5 | 0 | null / null / null |
| Hậu vệ kinh nghiệm | 94 | 5 | 0 | null / null / null |
| GK ngân sách | 47 | 5 | 0 | null / null / null |

Mỗi method có catalogue coverage 20/173 = 11,56%, request coverage 4/4 trên **bốn demo này**. Direct/KNN cùng representation giữ nguyên thứ tự. Weighted vs baseline overlap@5=1 ở cả bốn nhưng khác thứ tự ở Attack/Midfield/GK; Defender cùng thứ tự. Không dùng coverage/overlap để khẳng định recommendation chất lượng.

Audit: tái dựng đúng 4.112 eligible IDs; raw aggregate phút/goals/assists/matches khớp; 0 appearance/valuation của tập kiểm vượt cutoff. Metadata lịch sử chưa xác minh; ngưỡng 900 phút loại 4.198/8.322 integrated trước các điều kiện khác, không đo tác động nhân quả. Phát hiện tuổi xấp xỉ lệch lịch 1 người (341429, 29 thay vì 30); giữ nguyên snapshot và ranking, ghi backlog có version. Chi tiết và nguồn trong audit findings.

Lệnh tái chạy an toàn: `.venv\Scripts\python.exe -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck` (đường dẫn mới). Không overwrite template đã chấm. Bằng chứng tests cuối phiên được ghi trong [validation.json](validation.json) và [project_log](../project_log.md).

Phạm vi sản phẩm mới: MVP không login/signup; Streamlit → FastAPI → Python engine; Neon PostgreSQL dùng chung lưu lịch sử theo browser anonymous; Gemini hiểu request/giải thích evidence, không tự rank. Auth/đồng bộ đa thiết bị là Future Development. Day 11–13 evaluation; 14–17 API+Neon; 18–23 UI+Gemini; 24–27 integration/cloud khi được phép; 28–31 report/slides/demo. Toàn bộ kiến trúc web là kế hoạch, chưa triển khai.

Day 12 dự kiến: review/pilot rubric với assessor thật nếu có; kiểm provenance/coverage/bất đồng, bổ sung kế hoạch split và xử lý age issue có kiểm soát. Chưa có labels → báo bị chặn phần relevance, không tạo nhãn thay thế. Không commit/push/deploy; giữ lịch sử Day 1–10.
