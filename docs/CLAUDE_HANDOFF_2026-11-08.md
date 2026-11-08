# Bàn giao ScoutIQ cho Claude Code — 2026-11-08

Đọc tài liệu này khi tiếp tục ngày 2026-11-09; không cần lịch sử chat. Đây là trạng thái mới nhất, ưu tiên hơn các đoạn lịch sử ghi Day cũ/chưa commit/authentication/OpenAI. Không xóa những đoạn lịch sử đó.

## Điểm vào và trạng thái

- Repository local: `C:\Users\Admin\Documents\ScoutIQ`; remote: https://github.com/tranhaidong23/ScoutIQ-AI.git; branch `main`.
- Người dùng yêu cầu checkpoint commit/push Day5–13 và lưu đủ thông tin để chuyển sang Claude Code. Quyền này chỉ cho checkpoint hiện tại, không tự cấp quyền push/deploy cho Day tiếp theo.
- Commit bàn giao là commit thêm tài liệu này; tra chính xác bằng `git log -1 --format="%H %s" -- docs/CLAUDE_HANDOFF_2026-11-08.md`. Không nhúng hash của chính commit vào file của nó. Kiểm tra `git fetch origin`, `git status -sb`, `git rev-list --left-right --count main...origin/main` để xác minh đồng bộ thực tế. Không reset/force push nếu có thay đổi khác.
- Day13 hoàn thành công cụ/tài liệu local, chưa hoàn thành pilot người thật hoặc xác nhận chất lượng. Day14 chưa triển khai. Backend/frontend/database chưa có sản phẩm chạy.
- Latest full suite: **742 passed, 0 failed, 762.99s ngày2026-11-06**, bằng chứng [validation](../reports/day13/validation.json). Checkpoint08/11 kiểm hash xác nhận source/tests/requirements/evidence còn đúng bản đã test; không chạy lại full suite chỉ vì bổ sung tài liệu. Không gọi đây là kết quả test mới08/11 hoặc nghiệm thu máy mới.

## Sản phẩm và quyết định hiện hành

ScoutIQ — Intelligent Football Scouting & Transfer Recommendation System, “Scout Smarter. Sign Better.” Hỗ trợ scouts/CLB tìm, lọc, đề xuất top3–5, giải thích evidence, so sánh và lịch sử tìm kiếm.

MVP **không login/signup**. Stack đích: Streamlit + FastAPI + Neon PostgreSQL + Gemini API qua Google AI Studio + Python recommendation engine. Gemini chỉ hiểu yêu cầu/giải thích evidence; Python giữ filter/ranking, không dùng LLM tạo ground truth. Authentication và đồng bộ đa thiết bị thuộc Future Development. Các mục OpenAI/auth bên dưới tài liệu cũ là lịch sử, đã bị thay thế.

Anonymous không phải dữ liệu công khai: browser session/token ngẫu nhiên khó đoán, kiểm quyền đọc/ghi/xóa phía server, không tin session ID do client tự chọn; thiết kế retention và session isolation ở phase backend. Secrets Gemini/Neon chỉ ở server/env, không frontend/log/Git. Chưa triển khai hay cấu hình dịch vụ thật.

## Lịch sử và bằng chứng

| Day | Nội dung và kết quả chính | Nguồn |
|---|---|---|
|1|Thu thập5 bảng Transfermarkt; raw snapshot|src/collection, reports/project_log.md|
|2|Tích hợp8.322 người, lọc còn4.112 ứng viên|src/preprocessing|
|3|EDA và biểu đồ tuổi/vị trí/giá trị/hiệu suất|src/eda, reports/figures|
|4|Feature engineering 4.112×28; 23 tests|src/features, reports/day4_feature_quality.json|
|5|Baseline cosine theo vị trí, fit reference-only; tổng57 tests|src/recommendation/baseline.py, reports/day5_recommendation_examples.json|
|6|Weighted cosine và sensitivity; tổng109 tests|reports/day6|
|7|KNN đối chứng cùng representation, full ranking parity; tổng178 tests|reports/day7|
|8|Hard constraints + soft foot tie-break, boundary cases; tổng338 tests|reports/day8|
|9|Structured explanation và comparison; tổng453 tests|reports/day9|
|10|Service/request-response schema/config; tổng549 tests|reports/day10|
|11|Evaluation protocol/rubric0–3/audit; tổng619 tests,173 unlabeled|reports/day11|
|12|Age integrity/lineage/coverage, pilot32 seed12; tổng717 tests|reports/day12|
|13|Pilot intake, provenance/coverage/review queue; tổng742 tests|reports/day13|

Các con số tests là lịch sử từng mốc, không cộng lại. Chi tiết quyết định, công thức, khó khăn và Q&A: [project log](../reports/project_log.md), [insights](../reports/insights_and_defense.md), [presentation/defense](../reports/PRESENTATION_AND_DEFENSE.md). Bản đồ module: [inventory](FILE_INVENTORY.md); kiến trúc: [ARCHITECTURE](ARCHITECTURE.md); roadmap: [PROJECT_CONTEXT](PROJECT_CONTEXT.md).

## Bảo toàn dữ liệu và giới hạn

- Transfermarkt mùa2025/26 (`season=2025`), cutoff2026-06-12; không phải live data. 5 raw +3 processed ngoài Git, [manifest SHA-256](DATA_MANIFEST.json).
- Eligibility: ít nhất900 phút, position có giá trị, market value>0, valuation trong0–365 ngày trước cutoff. Market value là ước tính EUR, không phí chuyển nhượng và không feature kỹ năng.
- Bốn demo có22/10/94/47 ứng viên. Attack/Midfield dùng evidence tấn công và role; Defender/GK chỉ context-profile, chưa đo kỹ năng phòng ngự/bắt bóng. Similarity không là xác suất hoặc điểm kỹ năng tổng quát.
- Metadata CLB/vai trò tại cutoff và publication/as-of times chưa đủ: chưa temporal split hợp lệ. Không đổi tên random split/query holdout thành temporal evaluation.
- Một tuổi lệch ID341429 Davinson Sánchez: snapshot29, calendar30 theo DOB1996-06-12. [Correction](../reports/day12/correction_proposal.json) **PROPOSED/applied=false/approval=null**. Chưa DOB độc lập/phê duyệt, không sửa raw/canonical/scaler/ranking. Cần snapshot version mới và đo tác động trước promote.
- Height19cm ID743556 chưa xác minh; giữ cờ review. Raw có49 DOB thiếu nằm ngoài ứng viên; missing foot/height/CLB giữ nguyên.
- Người dùng xác nhận chưa có assessor hoặc labels. 32 pilot pending; 173 demo pairs chưa nhãn. Precision/Recall/NDCG thật và agreement bị chặn/null. Không giả assessor, không dùng similarity/rank/Gemini làm nhãn. SYNTHETIC chỉ kiểm công thức. Pilot calibration không phải final independent test.
- Day13 intake: file riêng +registry tường minh, không trùng hàng xuyên file, không trộn version/scope/source. Giữ free-text và định danh người thật ngoài Git. Review queue không tự adjudicate. Xem [workflow](../reports/day13/pilot_review_workflow.md).

## Snapshot riêng và chuyển máy

Backup đã kiểm08/11: `C:\Users\Admin\Documents\ChatGPT\khdl\ScoutIQ-Day12-datasets-20261103.zip`, gồm8 dataset +DATA_MANIFEST.json; tên Day12 vẫn hợp lệ vì Day13 giữ nguyên snapshot. Kích thước63.161.425 bytes. SHA-256 ZIP: `bc3ec4b21c3e1c845dccf1c3c49d6f0d4a0821811d3ba62eb4ebb30017d0b192`; checksum nằm cạnh ZIP. Đã đọc lại từng file trong archive và đối chiếu manifest.

Backup ở cùng ổC, chưa có bản ngoài máy. Nếu chỉ đổi công cụ trên máy này, dùng nguyên repo/venv hiện có và kiểm trạng thái trước khi sửa. Nếu đổi máy: chuyển ZIP/checksum qua ổ ngoài hoặc kho riêng có quyền phù hợp; không upload dataset/venv/.env lên GitHub. Clone Git riêng, giải nén giữ đường dẫn data/raw và data/processed, đối chiếu8 hashes theo SETUP trước chạy. Nguồn tải mutable không bảo đảm lấy lại đúng snapshot.

`.gitattributes` giữ nguyên bytes (`* -text`) vì source/artifacts bị khóa SHA-256. Không bật formatter, newline normalization hoặc rewrite artifacts chỉ để làm đẹp. Trước thay đổi thuật toán/source frozen, phải có version/provenance/regression phù hợp; không sửa hash để che lệch.

## Môi trường và lệnh bắt đầu

Đọc [SETUP](SETUP.md) để tạo venv mới/cài requirements. requirements.txt UTF-16LE BOM, phần lớn unpinned; jsonschema>=4.18,<5 đã thêm. environment-observed.json là snapshot cũ; environment-checkpoint.json mới ghi versions quan sát08/11, **không full lock hay bằng chứng fresh-install**. Không copy venv sang máy mới. threadpoolctl hiện có qua scikit-learn, chưa direct requirement.

Từ repo root trên máy hiện tại:

```powershell
git status -sb
.\.venv\Scripts\python.exe -B -m pip check
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
```

Nếu Windows từ chối temp pytest: chọn một --basetemp hoàn toàn mới ngoài repo; pytest có thể xóa thư mục đó nên không dùng thư mục chứa dữ liệu. Khi chuyển máy phải chạy lại tests thật, ghi kết quả thực, không mặc định742 sẽ đạt. Không chạy cleaning/EDA/build_features hoặc runners ghi output cố định trên bản duy nhất. Day11–13 runners cần output-dir mới, không overwrite evidence/annotations.

## Day14 — phạm vi tiếp tục khi người dùng giao

Đọc AGENTS → CLAUDE → tài liệu này → HANDOFF → PROJECT_CONTEXT/ARCHITECTURE/SETUP → reports/day13/phase_review.md → service/config/schemas và tests tương ứng. Rà git status trước khi sửa, bảo toàn thay đổi có sẵn.

1. Xác nhận scope nền tảng FastAPI + Neon trong phaseDay14–17; không tự làm toàn bộ phase hoặc frontend/Gemini/deploy.
2. Thiết kế adapter tái dùng RecommendationService, giữ request/response validation, filters, deterministic ranking, no-results, comparison và limitations. Không viết engine thứ hai.
3. Thiết kế dữ liệu/search history theo anonymous session, token/ownership/isolation/retention; không thêm users/password/login bắt buộc. Chưa có migration/schema/service thực để giả định dùng được.
4. Bổ sung dependencies/API tests theo phần thực sự triển khai; không ghi credentials vào repo. Khi cần kết nối Neon thật, yêu cầu cấu hình an toàn từ người dùng; không bịa URL/key hoặc tuyên bố kết nối thành công khi chưa chạy.
5. Sau Day14 cập nhật tests thực, log/insights/PRESENTATION/HANDOFF/inventory/setup/architecture. Giữ blockers expert labels/temporal/correction. Commit/push tiếp theo cần quyền nhiệm vụ mới; checkpoint này không là quyền deploy.

## Câu mở đầu cho Claude Code

“Tiếp tục ScoutIQ tại repository này. Đọc CLAUDE.md, AGENTS.md và docs/CLAUDE_HANDOFF_2026-11-08.md trước; xác minh Git/snapshot/môi trường. Day13 đã hoàn thành công cụ,742 tests; labels thật vẫn thiếu, correction PROPOSED. Triển khai Day14 nền tảng FastAPI + Neon đúng roadmap MVP không login/signup, bảo toàn ranking/dữ liệu/lịch sử. Cập nhật bộ tài liệu bàn giao và kiểm thử thực sau khi làm. Không tự commit/push/deploy.”
