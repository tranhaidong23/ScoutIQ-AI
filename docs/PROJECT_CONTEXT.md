# ScoutIQ — Bối cảnh sản phẩm và 31 ngày làm việc

<!-- CHECKPOINT_20261108_START -->
## Bàn giao hiện hành — 2026-11-08

Nguồn tiếp tục cho Claude Code: [bàn giao tổng hợp Day1–13](CLAUDE_HANDOFF_2026-11-08.md). Mục này ưu tiên về trạng thái Git/bàn giao; các mục bên dưới là lịch sử được giữ nguyên. Người dùng đã yêu cầu commit/push checkpoint Day5–13 hôm nay; quyền này không áp dụng tự động cho Day14/deploy.

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


<!-- DAY12_CURRENT_START -->
**Kiểm thử Day 12: 717 passed, 0 failed (619 cũ + 98 mới), 144,09s; exit code 0.**

## Trạng thái hiện hành sau Day 12 — 2026-11-03

**Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

Lộ trình 31 ngày và scope mới Day 11 giữ nguyên. Day 11 đã có protocol/công cụ; Day 12 đã audit integrity/provenance/coverage, thiết kế correction PROPOSED, chuẩn bị pilot 32 mẫu và validation/agreement/readiness gates. Chưa có người thật chấm, không coi hoàn tất tooling là đã đánh giá relevance. [Bằng chứng](../reports/day12/summary.md), [readiness](../reports/day12/evaluation_readiness.md).

**Day 13 dự kiến, chưa triển khai:** xác nhận assessor thật và thực hiện pilot độc lập nếu có; review provenance, uncertainty, abstention và disagreement. Tách pilot khỏi final evaluation; thiếu nhãn thì giữ metrics thật bị chặn. Review chính sách calendar/DOB và quyền áp dụng correction, chỉ tạo snapshot mới và đo tác động trong nhiệm vụ được phép. As-of metadata và temporal split hợp lệ vẫn còn thiếu.

Day 14–17 FastAPI+Neon, 18–23 Streamlit+Gemini, 24–27 integration/cloud khi có phép, 28–31 report/slides/demo vẫn dự kiến. Auth/sync là Future Development; privacy anonymous browser vẫn bắt buộc trong phase web. Các bảng trạng thái trước bên dưới là lịch sử.

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Phạm vi và roadmap hiện hành — 2026-11-03

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

**Day cuối: Day 11 — hoàn thành protocol, công cụ đánh giá và audit local; chưa có relevance labels độc lập. Day 12 chưa triển khai.** Không coi hoàn thành protocol là đã xác nhận chất lượng tuyển trạch. Engine/scaler/weights/eligibility Day 5–10 giữ nguyên. Bốn demo có 22/10/94/47 ứng viên, 173 hàng unlabeled; 16/16 full responses khớp Day 10 và repeat/filter đúng. P@K/Recall@K/NDCG@K thực đều null. SYNTHETIC chỉ kiểm công thức. Kết quả test cuối phiên xem reports/day11/validation.json.

Tên/tagline/mục tiêu/đối tượng ScoutIQ giữ nguyên. MVP phục vụ scouts, sporting directors, recruitment analysts và CLB: tìm/lọc theo dữ liệu, Top 3–5 khi đủ ứng viên, lý giải có evidence, comparison đúng đơn vị và lịch sử anonymous theo browser. Snapshot Transfermarkt 2025/26, cutoff 2026-06-12 vẫn giữ; không dữ liệu live hoặc synthetic football metrics. Market value chỉ hỗ trợ ngân sách, không fee/skill; không đánh giá GK bằng bàn thắng.

**Đã có:** pipeline/data audit, engine cosine/weighted/KNN, filters, explanation/comparison, service Python+JSON schemas, evaluation protocol/metrics gate. **Chưa có:** FastAPI endpoints, Neon schema/migration/session isolation, Streamlit/Gemini/cloud. Đổi nhà cung cấp chat không thay ranking hoặc tạo label. Các yêu cầu login/password/users/private-account/history-sync trong tài liệu cũ chuyển Future Development. Privacy lịch sử browser vẫn thuộc MVP và phải kiểm backend sau này.

### Kế hoạch 31 ngày cập nhật

| Day | Công việc / đầu ra và điều kiện nghiệm thu | Trạng thái |
|---|---|---|
| 1–10 | Giữ lịch sử collection → feature → engine/service/phase review; không thay artefact hoặc thuật toán | Đã có bằng chứng local |
| 11 | Protocol/rubric 0–3, annotation mẫu, audit, metrics có gate, tests | Hoàn thành công cụ; relevance thật chưa có |
| 12 | Review/pilot annotation với assessor độc lập nếu có; evidence/coverage/provenance và kế hoạch xử lý thiếu dữ liệu/tuổi boundary | Kế hoạch, chưa chấm thay người |
| 13 | Đánh giá có nhãn nếu đủ; phân tích vị trí/bias/split; nếu thiếu nhãn công bố giới hạn và đóng băng baseline có version | Kế hoạch, không tự tối ưu weights |
| 14 | FastAPI local bọc service/schema, errors/config/health; parity request–response | Kế hoạch |
| 15 | Neon PostgreSQL: schema/migration cho anonymous sessions, search_history, recommendation_results; quan hệ sở hữu và retention | Kế hoạch; mốc Git cần phép |
| 16 | API lưu/đọc/xóa lịch sử bằng browser session token; kiểm isolation, validation, không lộ DB credentials | Kế hoạch |
| 17 | Backend+DB integration, lỗi kết nối, secret/config/log redaction, rate-limit/quota design; local nghiệm thu | Kế hoạch |
| 18 | Streamlit forms và trạng thái loading/error/no-results; đơn vị EUR/cutoff rõ | Kế hoạch |
| 19 | UI Top 3–5, structured evidence, comparison 2–5 và biểu đồ đúng đơn vị/phạm vi | Kế hoạch |
| 20 | Lịch sử theo browser, xóa lịch sử/reset session, caveat mất token; UI/API tests | Kế hoạch; mốc Git cần phép |
| 21 | Gemini request interpretation → schema → validation; không tự filter/rank ngoài Python engine | Kế hoạch |
| 22 | Gemini giải thích từ evidence, nguồn/uncertainty; nếu lưu hội thoại thì chat_sessions/chat_messages thuộc anonymous session | Kế hoạch |
| 23 | Tích hợp UI/API/Gemini: prompt injection, hallucination, lỗi/quota/fallback, privacy và tests | Kế hoạch |
| 24 | Integration tests toàn luồng, isolation browser A/B, no-results và failure paths | Kế hoạch |
| 25 | Cấu hình cloud/secrets/migration/backup/runbook; staging deploy chỉ khi được phép | Kế hoạch; mốc Git cần phép |
| 26 | Cloud smoke/integration/performance theo tải thực được phép; nếu chưa deploy thì ghi bị chặn phần cloud | Kế hoạch |
| 27 | Hardening, regression, data retention/restore, vận hành/demo rehearsal | Kế hoạch |
| 28 | Final report: dữ liệu/phương pháp/protocol/bằng chứng/giới hạn, phân biệt synthetic và human | Kế hoạch |
| 29 | Slides, biểu đồ có nguồn, script demo và Q&A | Kế hoạch |
| 30 | Kiểm báo cáo/slides/demo, fresh-machine handoff và full regression | Kế hoạch; mốc Git cần phép |
| 31 | Nghiệm thu final, demo, release notes/handoff; commit/tag/release/push khi có phép riêng | Kế hoạch |

Day là thứ tự công việc, không phải ngày lịch. Mốc Git giữ Day 5, 10, 15, 20, 25, 30 và final 31; không cấp quyền tự commit/push/deploy. Ngày nào thiếu assessor, dữ liệu hoặc hạ tầng thì ghi rõ phần bị chặn, không tự tạo bằng chứng. Không đưa authentication trở lại critical path MVP; dành phần riêng Future Development.

Day 11 file/kết quả chi tiết: [summary](../reports/day11/summary.md), [audit](../reports/day11/audit_findings.md), [protocol](../reports/day11/evaluation_protocol.md). Kiểm thử cuối phiên lưu [validation](../reports/day11/validation.json). Không xóa/viết lại các thành tựu hoặc quyết định trong lịch sử bên dưới.

### Hồ sơ sản phẩm và lộ trình trước ngày 2026-11-03

<!-- DAY11_CURRENT_END -->

Cập nhật sau triển khai Day 10 ngày 2026-11-02. **Day 1–10 hoàn thành trong phạm vi local đã giao; Day 11–31 dự kiến.** Đây không phải tỷ lệ hoàn thiện toàn sản phẩm hoặc nghiệm thu chất lượng tuyển trạch. “Day” là thứ tự công việc, không phải ngày lịch. Bản đầy đủ về điều kiện nghiệm thu từng ngày nằm trong [project_log](../reports/project_log.md); quy tắc bắt buộc nằm ở [AGENTS](../AGENTS.md). Các kết quả V/H bên dưới về Day 1–5 thuộc phiên bàn giao trước; bằng chứng Day 6–10 ở mục riêng/báo cáo mới. Trạng thái Day cuối trong các đoạn lịch sử được thay bằng cập nhật này.

**Day 10:** [DAY10.md](../src/recommendation/DAY10.md), config/schemas/service/runner và 96 tests mới; [summary](../reports/day10/summary.md), [phase review Day 5–10](../reports/day10/phase_review.md). Unified Python service + request/response JSON schemas, metadata/version/hash/counts/units, optional comparison; giữ thuật toán Day 5–9, 549 tests đạt. 20/20 responses/explanations/comparisons khớp, 400 latency calls deterministic; chỉ latency local, không cloud SLA/relevance quality. Chốt ứng viên tích hợp để đánh giá, chưa API endpoint/auth/privacy/OpenAI. Day 11 dự kiến protocol/rubric/tình huống có nguồn, leakage/split/metrics phù hợp nhãn; chưa triển khai. Công việc Day 5–10 chưa commit, mốc Git chờ quyết định khi chuyển máy.

**Day 9:** [DAY9.md](../src/recommendation/DAY9.md), explainability.py/comparison.py/run_day9.py, 115 tests mới và [reports/day9/summary.md](../reports/day9/summary.md) + JSON/4 CSV/PNG. Evidence tách text, so sánh 2–5 người theo đơn vị thật, zero/missing→null có lý do; Defender/GK chỉ context, không market value skill. 453 tests đạt, 20/20 response khớp nguyên Day 8, 80 explanations/32 groups. Không sửa engine/scaler/eligibility/ranking hoặc gọi API; Day 10 dự kiến dịch vụ Python tích hợp/cấu hình/regression. Chưa commit/push/deploy, source/data transfer và fresh-install chưa nghiệm thu.

**Day 8:** constraints.py/run_day8.py/DAY8.md và tests/test_advanced_constraints.py; [reports/day8/summary.md](../reports/day8/summary.md) + JSON/4 CSV. Hard position/roles/age/EUR/minutes/g90/a90/foot/club trước ranking; soft foot chỉ phá hòa, không đổi cosine/scaler. Giữ source/API/tests Day 5–7; 338 tests đạt, 0 failed, 20 legacy checks + 20 scenario–engine cases đạt. Pools 22/10/94/47/0; Defender/GK context-only, không goals/assists threshold cho GK, không market value skill. Day 9 chuẩn hóa explanation và dữ liệu so sánh, chưa triển khai; trạng thái “Day 8 dự kiến” trong ghi nhận cũ bên dưới thuộc lịch sử. Chưa commit/push/deploy, để commit khi chuyển máy theo nhiệm vụ được phép.

## Sản phẩm phải xây dựng

**ScoutIQ – Intelligent Football Scouting & Transfer Recommendation System.** Tagline: **Scout Smarter. Sign Better.** Nền tảng Data Science, Recommendation Engine và AI hội thoại dành cho football scouts, sporting directors, recruitment analysts và CLB bóng đá.

Phạm vi bắt buộc được giữ nguyên:

- Đăng ký/đăng nhập/đăng xuất; mật khẩu băm; dữ liệu riêng tư và kiểm tra quyền sở hữu ở backend.
- PostgreSQL lưu users, search_history, chat_sessions, chat_messages, recommendation_results; message thuộc session có chủ sở hữu.
- Tìm theo vị trí, tuổi, ngân sách EUR, hiệu suất; top 3–5 bằng content-based recommendation, đánh giá weighted cosine/KNN. Thiếu ứng viên thì trả số lượng thực và giải thích.
- So sánh bằng biểu đồ có đơn vị, bối cảnh vị trí và missing rõ ràng.
- Scouting chat qua OpenAI API dựa trên dữ liệu truy xuất thật, có căn cứ/cutoff, báo thiếu thay vì bịa.
- FastAPI backend, Streamlit frontend, PostgreSQL; keys/cấu hình DB ở server.
- Cloud khi được phép; kiểm thử dữ liệu, engine, API, auth/privacy và luồng tích hợp; Final Report và Presentation Slides.

## Nguồn và nguyên tắc

Nguồn nghiệp vụ: Transfermarkt; code tải 5 bảng qua URL được ghi trong [SETUP](SETUP.md). Snapshot mùa **2025/26**, season nguồn = 2025, cutoff **2026-06-12**; không phải dữ liệu trực tiếp hiện tại. 5 raw .csv.gz và 3 processed .csv được giữ ngoài Git. [DATA_MANIFEST](DATA_MANIFEST.json) ghi hash/kích thước kiểm tra trực tiếp, không chứa dữ liệu cầu thủ.

Ứng viên: >=900 phút, vị trí không trống, giá trị thị trường dương, định giá 0–365 ngày trước cutoff. Tuổi được tính tại cutoff. Thống kê trận được lọc theo mùa/ngày trong clean_data.py; metadata CLB/cầu thủ chưa được chứng minh đồng nhất thời điểm.

Không tạo dữ liệu giả; không điền missing bằng 0 vô căn cứ; tương quan không chứng minh nhân quả. Market value không phải phí chuyển nhượng hoặc nhãn kỹ năng. Ngưỡng phút, reliability và độ mới định giá là lựa chọn cần đánh giá độ nhạy. Chỉ fit preprocessing trên tập tham chiếu hợp lệ; chưa có temporal evaluation. Không gọi percentile tấn công là chất lượng tổng hợp, nhất là hậu vệ/thủ môn.

## Cách đọc bằng chứng

- **V (xác minh 2026-11-02):** đọc code/file/Git local, hash 8 dataset, shape/schema 3 processed, chạy 57 tests và pip check trên venv hiện có.
- **H (bằng chứng lịch sử):** nhật ký và artefact đã lưu; không có nghĩa pipeline tương ứng được chạy lại hôm nay.
- **P (dự kiến):** chưa triển khai/nghiệm thu. Không gán commit/test cho tương lai.

Không chạy lại tải dữ liệu, cleaning, EDA, build_features hoặc runner ghi báo cáo trong phiên bàn giao. Không fetch để xác minh GitHub; origin/main là ref cache local.

## Tổng hợp Day 1–5

### Day 1 — Thu thập và kiểm tra

Mục tiêu: có 5 bảng players, clubs, games, appearances, player_valuations. File: src/collection/download_data.py, inspect_data.py, check_season.py; reports/day1_data_quality.csv.

Dữ liệu/thuật toán: HTTP streaming tải gzip, pandas kiểm tra shape/missing/duplicate và độ phủ mùa. H: 50.149 players, 796 clubs, 88.958 games, 1.894.350 appearances, 656.301 valuations trong báo cáo chất lượng. V: 5 file raw hiện hữu và hash đã ghi; không đếm lại raw toàn bộ hôm nay.

Test: báo cáo kiểm tra dữ liệu lịch sử, chưa có suite tự động Day 1 riêng. Insight: cần lọc mùa/cutoff và dùng lịch sử định giá. Hạn chế: downloader không pin phiên bản hay kiểm checksum, bỏ qua file sẵn có khác rỗng; thông báo kết thúc không chứng minh tải đủ. Commit: 86c036050d58ceca819858a8ed1391d3fbefaf9d.

### Day 2 — Cleaning, integration, candidates

File: 5 script src/preprocessing/; dữ liệu vào 5 raw, ra scoutiq_players_2025_26.csv **8.322 × 20** và scoutiq_candidates_2025_26.csv **4.112 × 21** (V shape).

Thuật toán: lọc games season/ngày, ghép appearances, xử lý thống kê hợp lệ, deduplicate appearance ID, tổng hợp phút/goals/assists/matches theo player; tính per90/tuổi, ghép metadata và định giá dương gần nhất <=cutoff; lọc ứng viên. Test: validate_data.py in kiểm tra mô tả (không phải suite assertion); kiểm tra candidates trong 23 tests Day 4 đang pass (V), chưa chạy lại raw→processed.

Insight: cần tách pool tích hợp khỏi tập đủ bằng chứng ra sân; per90 có từ Day 2. Hạn chế: ngưỡng 900 phút/365 ngày tạo selection bias; metadata hiện tại có thể khác cutoff. Commit chung Day 2–3: c4d638c2d10c542c897ccf95dedde540814925b1.

### Day 3 — EDA

File: src/eda/eda_analysis.py, age_group_analysis.py; 5 PNG và 2 bảng day3_*_summary.csv. Input: candidates; thuật toán: phân phối, scatter/boxplot, Pearson, groupby vị trí, nhóm tuổi.

H: market value trung bình khoảng 9,24 triệu EUR, median 3 triệu EUR; tương quan tuổi/định giá khoảng -0,24, không chứng minh quan hệ nhân quả. V: code/artefact hiện hữu; không chạy lại EDA hay thẩm định từng hình trong phiên này. Chưa có test tự động EDA riêng. Hạn chế: mẫu đã lọc, skew lớn, goals/assists không đo toàn diện defender/GK. Commit chung: c4d638c2d10c542c897ccf95dedde540814925b1.

### Day 4 — Feature Engineering

File: src/features/build_features.py, tests/test_features.py, reports/day4_feature_quality.json, figures/day4_market_value_transformation.png. Input: candidates; output features **4.112 × 28** (V).

8 đặc trưng được tạo/kiểm tra, 7 cột thêm: goals+assists; contributions*90/minutes; EUR/1e6; log1p(market_value_m); min(minutes/2700,1); 3 percentile goals_per90/assists_per90/contributions_per90 theo position = 100*average_rank/group_size. contributions_per90 đã tồn tại.

23 tests Day 4 đạt trong lượt test mới (V); gồm missing/infinity/duplicate, range/per90, percentile, roundtrip. H: skew định giá 4,222779 → 0,632063 sau log; 939 cầu thủ reliability=1; GK nhiều giá trị bàn thắng 0 làm percentile ít phân biệt. Log làm giảm lệch, không biến định giá thành kỹ năng.

Hạn chế: foot/height/CLB có missing, chiều cao 19 cm player_id=743556 chưa xác minh; không sửa đoán. Commit: 266f90f4a735289fbf9b78ac6aeca9c0acc68b0e.

### Day 5 — Baseline content-based

File: src/recommendation/baseline.py, run_day5.py, README.md; tests/test_recommendation.py; reports/day5_recommendation_examples.json và .md. Input: features; output Top K và explanation có evidence, báo cáo 5 kịch bản thật.

Thuật toán: StandardScaler theo vị trí + one-hot, L2 normalize/cosine; filter trước ranking, loại query, score giảm dần rồi ID tăng dần. Attack/Midfield: goals/90, assists/90, vai trò. Defender/GK: context tuổi/phút/chân thuận (Defender thêm vai trò), không đánh giá phòng ngự/bắt bóng. Không dùng market value/log value/reliability/percentile toàn catalogue/chiều cao/CLB làm feature.

V: **34 tests recommendation + 23 feature = 57 passed**, 10,67 giây. H: runner có 5 kịch bản, fit 4.108 người, loại 4 query; eligible Attack/Midfield/Defender/GK lần lượt 349/405/512/107, mỗi nhóm trả 5; ngân sách 0 trả 0. Không chạy lại runner ghi file hôm nay.

Insight: cosine cao có thể chỉ gần hướng vector, không bằng nhau về hiệu suất tuyệt đối. Hạn chế: chưa đánh giá relevance chuyên gia, temporal leakage đầy đủ, trọng số/độ nhạy, KNN; score không phải xác suất chuyển nhượng. **Chưa commit Day 5** tại lần kiểm tra này.

Thứ tự lịch sử Git là Day 1 → Day 4 → Day 2–3, theo thời điểm commit; giữ nguyên, không viết lại để khớp thứ tự công việc.

## Day 6 — Weighted Cosine Similarity & Recommendation Evaluation (đã kiểm chứng)

Mục tiêu: tái lập baseline, thêm trọng số theo vị trí và kiểm hành vi/độ nhạy. Code mới weighted.py, evaluation.py, run_day6.py; hướng dẫn [DAY6.md](../src/recommendation/DAY6.md); tests/test_weighted_recommendation.py. Baseline và dữ liệu Day 4–5 giữ nguyên.

Input 4.112×28, fit 4.108 người loại 4 query; 6 cấu hình × 5 kịch bản chung. Weighted cosine bằng sqrt(w) trước L2, w hữu hạn không âm; toàn zero bị từ chối, zero từng feature là ablation. Không dùng market value/reliability làm kỹ năng, Defender/GK chỉ context. Audit tương quan fit-only tránh đếm lặp raw/per90/contributions/reliability.

V: 109 tests pass, 0 failed (57 cũ + 52 mới); runner tái lập 5 kịch bản Day 5, unit weights khớp toàn ranking, 30 tổ hợp đạt filter/score/order/determinism. Đầu ra reports/day6 gồm JSON, 3 CSV (30 metrics, 8.238 ranked rows, 264 correlation pairs), 2 PNG và summary. Default overlap@5 trung bình .90; bỏ categorical .25, bỏ numeric đầu tiên .35. Đây là độ nhạy, không phải scouting accuracy; không tính Precision/NDCG vì thiếu relevance labels. Chưa chọn trọng số tối ưu, chưa temporal evaluation/KNN. Day 6 chưa commit; HEAD vẫn c4d638c.

## Day 7 — KNN Benchmark & Recommendation Robustness (đã kiểm chứng)

Mục tiêu: đối chứng NearestNeighbors cosine với direct cosine trên cùng representation/reference/filter Day 5 và weighted Day 6. Code mới knn.py/run_day7.py, tests/test_knn_recommendation.py, [DAY7.md](../src/recommendation/DAY7.md); không sửa baseline cũ. Fit preprocessing 4.108 người, 4 query giữ riêng, input 4.112×28 không đổi.

KNN brute-force trên pool đã lọc, loại query/zero vector, lấy toàn bộ neighbors để tie round12 + ID xác định rồi cắt K. V: 178 tests đạt, 0 failed; 10 cặp full-ranking parity và 50 trường hợp K=1/3/5/50/10000 đạt. Nonempty overlap@5=1, Spearman≈1; score difference=0, distance=1-cos sai số tối đa 4,44e-16. Đây là tương đương truy xuất, không nhãn relevance.

Benchmark 5 warm-up + 50 measured/method/query, một luồng, alternating order: 1.000 timed calls, median/p95, cùng K=5/pool. KNN median cao hơn direct ở 8/8 query nonempty trong phiên Windows hiện có. Giữ direct làm phương án hiện hành, KNN đối chứng; chưa khẳng định mọi workload hoặc quality. Chưa cold-start/load/cloud/CI confidence interval.

reports/day7 có evaluation.json, comparisons.csv (10), robustness.csv (50), timings.csv (1.000), benchmark.csv (20), rankings.csv (5.492), latency.png, summary.md. Không có relevance labels nên không Precision/NDCG, Defender/GK vẫn context-only. HEAD c4d638c, Day 7 chưa commit; chưa push/deploy. Day 8 tiếp tục bộ lọc/hiệu suất thật và điều kiện biên.

## Roadmap còn lại — Day 8–31 là P

Tên đầu ra dưới đây là hạng mục dự kiến, không phải file đã tồn tại. Chi tiết nghiệm thu trong project_log.

| Day | Mục tiêu/đầu ra dự kiến | Kiểm chứng/giới hạn bắt buộc |
|---|---|---|
| 8 | Hoàn thiện filter vị trí/tuổi/EUR/hiệu suất | Biên, input sai, thiếu/rỗng; không nới điều kiện |
| 9 | Explanation và dữ liệu so sánh | Evidence, đơn vị, cutoff, tie/order stability; UI chart ở Day 21 |
| 10 | Dịch vụ engine Python tích hợp | Regression, cấu hình/tài liệu; mốc commit/push đề xuất |
| 11 | Protocol đánh giá và rubric | Chỉ dùng Precision@K/NDCG nếu có nhãn thật; rà leakage |
| 12 | So baseline/weighted cosine/KNN, ablation | Metric thực đo, split/tuning hợp lệ, giới hạn vị trí |
| 13 | ERD/schema/migration PostgreSQL | Đủ 5 bảng, FK/ownership, password hash design |
| 14 | Persistence PostgreSQL cục bộ | Transaction/rollback, owner queries, DB test riêng |
| 15 | FastAPI contracts/routes và engine/DB | Validation/route tests; mốc Git; chưa public dữ liệu riêng |
| 16 | Tích hợp API ↔ DB ↔ engine | Lỗi DB/input, response consistency; điểm gắn auth |
| 17 | Register/login/logout và vòng đời phiên | Sai mật khẩu, trùng account, hết hạn/logout |
| 18 | Backend privacy/ownership | Hai user, đọc/ghi chéo, giả ID/session; không chỉ ẩn UI |
| 19 | Streamlit auth/navigation/API client | Luồng local, logout và cache riêng |
| 20 | UI search/top 3–5/history | E2E local, EUR/cutoff/no-results; mốc Git |
| 21 | Bảng và biểu đồ so sánh | Dữ liệu thật, cùng bối cảnh, missing rõ; không biến giá thành kỹ năng |
| 22 | OpenAI API server-side, grounding | Nguồn/cutoff, thiếu thông tin, lỗi/timeout/chi phí; tách mock/API thật |
| 23 | Chat UI, session/message persistence | Auth→search→compare→chat→history, ownership |
| 24 | Chuẩn bị cloud/build/config/backup | Kiểm tra local; chưa deploy nếu chưa được phép |
| 25 | Staging khi được phép | Smoke test cloud thật; nếu thiếu phép ghi bị chặn; mốc Git |
| 26 | Integration/E2E các môi trường được phép | Luồng chính và lỗi mạng/API/DB; không gọi local là cloud |
| 27 | Hiệu năng/bảo mật/backup/rollback | Đo có điều kiện rõ, restore và regression |
| 28 | Final Report | Số liệu truy vết, giới hạn, nguồn; kết quả tách khỏi kế hoạch |
| 29 | Presentation Slides và demo/Q&A | Khớp report, dữ liệu thật, không lộ secrets |
| 30 | Rehearsal, clean setup, release candidate | Test/hướng dẫn/bugs; mốc Git, chưa tự phát hành |
| 31 | Nghiệm thu, final release và bàn giao | Đủ yêu cầu + bằng chứng + quyền; commit/tag/push/release/deploy theo phép |

Day 5 đã làm sớm chuẩn hóa, cosine, filter và explanation cơ bản theo yêu cầu. Day 6 đã kiểm chứng weighted cosine/độ nhạy, Day 7 đã thực hiện KNN benchmark/robustness; Day 8–9 vẫn cần phần hoàn thiện tương ứng, không đánh dấu hoàn thành theo suy diễn.

Sau mỗi Day thực hiện quy trình [CLAUDE](../CLAUDE.md) và cập nhật [HANDOFF](HANDOFF.md). Các mốc Git chính thức: **5, 10, 15, 20, 25, 30, 31**. Mốc không thay thế sự cho phép; nhiệm vụ bàn giao hiện tại không commit/push/deploy.
