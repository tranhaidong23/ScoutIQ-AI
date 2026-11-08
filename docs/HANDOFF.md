# ScoutIQ — Bàn giao hiện hành

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

## Bàn giao hiện hành — Day 12 / 2026-11-03

**Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

- Code mới: [integrity.py](../src/evaluation/integrity.py), [pilot.py](../src/evaluation/pilot.py), [run_day12.py](../src/evaluation/run_day12.py); hai file tests Day 12. Bằng chứng: [summary](../reports/day12/summary.md), [audit](../reports/day12/audit.json), [validation](../reports/day12/validation.json).
- Còn thiếu 24 foot, 23 height và 16 tên CLB ở mỗi cột tên; height 19 cm ID 743556 vẫn cần review. Exclusions tuần tự: 8.322 → 4.124 sau phút → 4.112 sau freshness; 226 fail freshness độc lập khác 12 người loại thêm. League proxy theo CLB hiện tại chưa phải giải lịch sử. Không có temporal split hợp lệ.
- [Correction](../reports/day12/correction_proposal.json) đã có parent hashes/old-new values/gates; applied=false, approval=null. Không dataset mới hoặc promote config. DOB ngoài snapshot chưa được xác minh.
- [Pilot](../reports/day12/pilot_manifest.json): 32 hồ sơ từ 173 cặp, age strata + SHA256, seed 12; không dùng rank/score. Assessor dùng bản sao cùng template; registry hiện rỗng. [Readiness](../reports/day12/evaluation_readiness.md) ghi các gate và lý do chặn, không công bố synthetic như quality.
- Git kiểm trực tiếp: main, HEAD `c4d638c2d10c542c897ccf95dedde540814925b1`, origin `https://github.com/tranhaidong23/ScoutIQ-AI.git`. Không fetch/xác minh remote mới; index giữ nguyên. Source Day 5–12/docs chưa commit, requirements dirty từ trước được bảo toàn.
- Chuyển máy cần bàn giao riêng 8 snapshot raw/processed theo DATA_MANIFEST; clone HEAD hiện tại chưa đủ source. Không force-add dữ liệu, upload secrets hoặc coi môi trường quan sát là full lock. Chưa nghiệm thu fresh-install/máy đích.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day12 --output-dir reports/day12_recheck
```

POSIX dùng `.venv/bin/python`; chọn thư mục output chưa tồn tại, không overwrite annotation.

**Day 13 dự kiến, chưa triển khai:** xác nhận assessor thật và thực hiện pilot độc lập nếu có; review provenance, uncertainty, abstention và disagreement. Tách pilot khỏi final evaluation; thiếu nhãn thì giữ metrics thật bị chặn. Review chính sách calendar/DOB và quyền áp dụng correction, chỉ tạo snapshot mới và đo tác động trong nhiệm vụ được phép. As-of metadata và temporal split hợp lệ vẫn còn thiếu.

Sau mỗi Day cập nhật tests/kết quả thực, project_log, insights, PRESENTATION, HANDOFF và inventory/setup/architecture khi cần. Mốc Git không cấp quyền tự commit/push/deploy.

### Các lần bàn giao trước — lịch sử

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Bàn giao hiện hành — Day 11 / 2026-11-03

**Day cuối: Day 11 — hoàn thành protocol, công cụ đánh giá và audit local; chưa có relevance labels độc lập. Day 12 chưa triển khai.** Không coi hoàn thành protocol là đã xác nhận chất lượng tuyển trạch. Engine/scaler/weights/eligibility Day 5–10 giữ nguyên. Bốn demo có 22/10/94/47 ứng viên, 173 hàng unlabeled; 16/16 full responses khớp Day 10 và repeat/filter đúng. P@K/Recall@K/NDCG@K thực đều null. SYNTHETIC chỉ kiểm công thức. Kết quả test cuối phiên xem reports/day11/validation.json.

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

- Bằng chứng: [summary](../reports/day11/summary.md), [protocol](../reports/day11/evaluation_protocol.md), [rubric](../reports/day11/relevance_rubric.md), [audit findings](../reports/day11/audit_findings.md), [evaluation](../reports/day11/evaluation.json), [validation](../reports/day11/validation.json). New code: src/evaluation/{metrics,audit,run_day11}.py và __init__.py; tests/test_evaluation_protocol.py.
- Audit mới: 4.112×28, đúng eligibility IDs; minutes/goals/assists/matches khớp raw; không appearance/valuation của tập kiểm vượt cutoff. 4.198/8.322 integrated dưới 900 phút. Metadata lịch sử CLB/vai trò/chân thuận chưa chứng minh; league/cup aggregate chưa hiệu chỉnh. Tuổi 341429 lưu 29, calendar 30 tại cutoff: đã ghi vấn đề, chưa sửa để giữ baseline.
- Relevance: 173 mẫu chưa chấm, không assessor giả. Fixture SYNTHETIC P@3=2/3, R@3=1, NDCG@3≈0,692020 chỉ kiểm công thức. Coverage 20/173 mỗi method và overlap không phải quality. Default/config/fit IDs/weights giữ nguyên.
- Git kiểm trực tiếp: branch `main`, HEAD `c4d638c2d10c542c897ccf95dedde540814925b1`, origin `https://github.com/tranhaidong23/ScoutIQ-AI.git`. Không fetch, không xác minh remote trực tiếp. Index giữ nguyên; Day 5–11 và docs có thay đổi chưa commit. Clone HEAD hiện tại thiếu source này; không coi bàn giao đã hoàn tất.
- Dữ liệu raw/processed bị .gitignore; cần bàn giao riêng 8 file theo [DATA_MANIFEST](DATA_MANIFEST.json)/audit hashes. Không force-add/upload secrets hoặc raw lớn. Requirements không đổi Day 11; môi trường hiện tại có dependencies cần thiết, chưa fresh-install/máy mới. URL download mutable không đảm bảo cùng snapshot.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck
```

POSIX `.venv/bin/python`; output phải chưa tồn tại. Runner đọc raw/processed và Day 10 evidence, giữ nguyên artefact cũ. Không chạy cleaning/candidates để kiểm tài liệu. Nhãn thật: sao chép template sang file riêng; load_annotations giữ blank là None, validate scenario/universe, chọn assessor/provenance; không dùng ranking làm nhãn. Template mẫu không bị overwrite khi rerun.

**Day 12 dự kiến (chưa làm):** tuyển/xác nhận assessor phù hợp và pilot rubric nếu có, kiểm evidence quality/provenance/coverage/abstention, thỏa thuận xử lý bất đồng và data split; rà age issue và đề xuất sửa có version. Thiếu người/nhãn → giữ relevance bị chặn, tiếp tục công việc độc lập được giao, không chế nhãn hoặc báo metric thực. Day 13 đánh giá có điều kiện; Day 14–17 mới API+Neon; chưa implementation Gemini/cloud/auth.

**Handoff Claude Code:** đọc scope mới ở AGENTS/CLAUDE trước các phần lịch sử; chạy suite và hash-check snapshot, đọc audit và protocol, giữ nguyên request/response/ranking. Sau mỗi Day cập nhật log/insights/PRESENTATION/HANDOFF, inventory khi đổi I/O, setup/architecture khi đổi contract. Các mốc Git 15/20/25/30/31 vẫn là đề xuất; Day 11 không commit/push/deploy.

### Các lần bàn giao trước — giữ nguyên để truy vết

<!-- DAY11_CURRENT_END -->

## Cập nhật hiện hành sau Day 10 — 2026-11-02

**Day cuối: Day 10 hoàn thành có bằng chứng trong phạm vi integration/phase review local. Day tiếp theo: Day 11, chưa triển khai.** Các mục trước là lịch sử; giữ toàn bộ yêu cầu sản phẩm và roadmap 31 ngày.

- Mới: [service.py](../src/recommendation/service.py), [schemas.py](../src/recommendation/schemas.py), [config.py](../src/recommendation/config.py), [run_day10.py](../src/recommendation/run_day10.py), [DAY10.md](../src/recommendation/DAY10.md), [tests](../tests/test_service.py), 9 outputs [reports/day10](../reports/day10/summary.md), gồm [phase review Day 5–10](../reports/day10/phase_review.md). Giữ source/API/tests/artefact/scaler/eligibility/weights/ranking Day 5–9.
- Unified service: request validation → hard constraints → ranking/Top K → Day 9 evidence/text → optional groups 2–5 → response validation. Bốn methods, default cosine; request không nhận weights. JSON v1 có dataset/config hash, method/normalized filters/candidate/rankable/returned counts/K/limitations; no NaN/Inf/duplicate JSON keys. Chưa FastAPI/Pydantic/HTTP/API calls.
- **549 passed in 62.01s, 0 failed**, exit 0 (453 cũ + 96 mới); baseline đầu phiên 453 passed in 58.18s; suite mới riêng 96 passed in 19.35s. pip check đạt. requirements.txt thêm jsonschema>=4.18,<5, giữ UTF-16/nội dung cũ; 4.26.0 có sẵn, không cài dependency mới.
- Runner exit 0: **20/20 full response Day 8 + envelope/comparisons Day 9 khớp**; 80 Top 5 rows, pools 22/10/94/47/0 và returned 5/5/5/5/0. Dataset 4.112×28, cutoff 2026-06-12, fit 4.108 loại bốn queries cũ; JSON lưu source/input hashes, config/audits/query/môi trường/HEAD. Không temporal split hoặc model tuning.
- Latency: 3 warm-up + 20 repeats/case, 20 cases = 400 measured calls, rotation/một luồng, không pytest đồng thời. Bao gồm recommend_json + comparison=true + schema/semantic validation/serialization, loại startup/fit/I/O/network. Nonempty median từng case 74,381–141,391 ms, p95 102,959–193,290 ms; startup một quan sát 1.423,006 ms. Raw timings/bảng median/p95 có trong reports/day10; không cloud SLA/quality hoặc so trực tiếp phạm vi Day 7. Mọi serialized response lặp lại giống nhau, fit/input không đổi.
- Git main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1; index giữ nguyên. Source Day 5–10/docs chưa commit. **Không stage/commit/push/deploy/fetch; mốc Day 10 chờ người dùng quyết định khi chuyển máy.**

Lệnh từ root (output-dir phải mới):

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day10 --output-dir reports/day10_rerun --warmup 3 --repeats 20
```

Linux/macOS thay executable bằng .venv/bin/python. Service standalone: RecommendationService.from_csv(path, fit_player_ids=...), recommend(dict)/recommend_json(str); ví dụ chính xác trong DAY10. Runner cần features + JSON Day 8/9 đúng hashes + source Day 5–10; không cần chạy pipeline raw hoặc benchmark cũ. Không truyền fit IDs nghĩa catalogue fit, không tái lập holdout của runner.

**Điều kiện chuyển máy:** clone HEAD hiện tại chưa đủ; nhận source/tests/docs/reports chưa commit, requirements mới và snapshot 8 datasets ngoài Git theo DATA_MANIFEST. JSON Schema export phải đi cùng runtime semantic/native-integer checks. Legacy schema có extension, service chưa production/API/auth/privacy. Content/audit hashes chưa đảm bảo bitwise xuyên môi trường không pin; csv_sha256/manifest nhận diện file nguồn. Fresh-install/full lock/máy đích chưa nghiệm thu.

**Day 11 khi được giao:** protocol đánh giá/rubric/tình huống có nguồn; baseline và metrics eligibility/coverage/stability/latency, rà leakage/time metadata và split khả thi. Relevance labels chưa có nên chưa Precision/NDCG; không dùng market value ground truth. Defender/GK context-only, chưa league/tactical/uncertainty adjustment/expert review. Phase review chốt ứng viên tích hợp local để đánh giá, không model tối ưu. Chưa triển khai Day 11 hoặc backend/UI/DB/auth/OpenAI/cloud. Cập nhật bốn hồ sơ bắt buộc/inventory sau Day tiếp theo.

## Cập nhật hiện hành sau Day 9 — 2026-11-02

**Day cuối: Day 9 hoàn thành có bằng chứng; Day tiếp theo: Day 10, chưa triển khai.** Các mục trước giữ làm lịch sử; yêu cầu sản phẩm/lộ trình 31 ngày giữ nguyên.

- Thêm [explainability.py](../src/recommendation/explainability.py), [comparison.py](../src/recommendation/comparison.py), [run_day9.py](../src/recommendation/run_day9.py), [DAY9.md](../src/recommendation/DAY9.md), [tests](../tests/test_explainability.py) và 7 outputs [reports/day9](../reports/day9/summary.md). Evidence tách text rule-based; ID/đơn vị/feature/reference/constraints/missing rõ ràng. So sánh 2–5 người, delta/absolute/relative, zero/missing→null với lý do; không overall winner.
- Giữ nguyên source/API/tests/artefact Day 5–8, reference/scaler/weights/eligibility/ranking; không đổi dataset/requirements/manifests. Defender/GK/mixed comparisons context-only, market value không skill/phí mua, similarity không probability.
- Dataset 4.112×28, fit 4.108 loại bốn query như Day 8; cutoff 2026-06-12. **453 passed in 59.76s, 0 failed**, exit 0 (338 cũ + 115 mới); baseline đầu phiên 338 passed in 47.81s. Lượt đầu suite mới 452 passed/1 failed do fixture inf/int64 đã sửa; không nới validator.
- Runner exit 0: **20/20 response khớp nguyên Day 8**, 80 explanations, 32 comparison groups; CSV checks/Top5/features/differences lần lượt 20/80/260/448 dòng. Pools 22/10/94/47/0, Top5/5/5/5/0. JSON ghi config/query/reference/12 source hashes/2 input hashes/environment/HEAD; PNG so sánh đã xem kiểm nhãn/bố cục. Không đo latency hoặc quality mới.
- **Git:** main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1; source Day 5–9/docs chưa commit. Giữ index và mọi thay đổi cũ; không stage/commit/push/deploy/fetch. Mốc Day 10 chỉ dự kiến; theo yêu cầu để commit khi chuyển máy trong nhiệm vụ được phép.

Lệnh từ repo root (chọn directory chưa có để giữ outputs):

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day9 --output-dir reports/day9_rerun
```

Linux/macOS dùng .venv/bin/python. Không dependency/key mới. Runner cần features + reports/day8/evaluation.json đúng hashes, và source Day 5–9; không cần chạy lại các runner cũ để chỉ chạy Day 9. Để tái lập chuỗi Day 5–8, vẫn cần các prior JSON tương ứng trong SETUP. **Clone riêng HEAD hiện tại chưa đủ**; bàn giao riêng 8 dataset theo DATA_MANIFEST, nhận toàn bộ source/tests/docs/reports chưa commit. Fresh-install/lock/máy đích chưa nghiệm thu.

**Hợp đồng cần giữ:** RecommendationExplainer.recommend trả envelope mới chứa nguyên response, render text từ evidence; explain_response đối chiếu canonical response nên thêm một lần retrieval. So sánh tối đa 5 người gồm reference; runner chia reference+Top4 và reference+hạng5. JSON có version nhưng chưa là FastAPI/Pydantic contract hoặc API service. Private catalogue/representation là dependency cần regression. Không benchmark overhead, không đánh giá hữu ích explanation bằng chuyên gia; metadata cutoff/league effects/relevance labels/temporal validation còn thiếu.

**Day 10 khi được giao:** tích hợp engine thành dịch vụ Python dùng lại cho API; ổn định cấu hình và pipeline filter→ranking→explanation/comparison; giữ validation/empty/missing/đơn vị và test hồi quy; chốt phiên bản ứng viên để đánh giá chính thức, không tuyên bố tối ưu. Rà soát chuyển máy và đề xuất mốc Git khi có quyền. Chưa triển khai Day 10/API/UI/OpenAI. Sau Day tiếp theo cập nhật log/insights/PRESENTATION_AND_DEFENSE/HANDOFF/inventory theo quy tắc.

## Cập nhật hiện hành sau Day 8 — 2026-11-02

**Day cuối: Day 8 hoàn thành có bằng chứng; Day tiếp theo: Day 9, chưa triển khai.** Các mục Day 7 trở về trước bên dưới giữ làm lịch sử. Phiên Day 8 được giao sau phiên tài liệu, không còn giới hạn chỉ thiết lập tài liệu.

- Thêm [constraints.py](../src/recommendation/constraints.py), [run_day8.py](../src/recommendation/run_day8.py), [DAY8.md](../src/recommendation/DAY8.md), [tests](../tests/test_advanced_constraints.py) và 6 artefact [reports/day8](../reports/day8/summary.md). Giữ nguyên source/API/tests/artefact Day 5–7, dữ liệu/requirements/manifests.
- Hard position/roles/age/EUR/minutes/g90/a90/foot/club IDs trước ranking; soft foot chỉ phá hòa score round12 rồi ID. SearchConstraints chứa SearchFilters, phải gọi qua AdvancedRecommender; không truyền request mới vào engine cũ. Request-local encoded view, không refit preprocessing hoặc thay weights/score.
- Budget từ max_budget_eur hoặc explicit budget_value+budget_unit EUR/EUR_million; invalid constraints không bị bỏ qua. Active hard constraint thiếu dữ liệu thì không đạt. GK không nhận goals/assists thresholds, Defender/GK context-only, market value không skill/phí mua.
- Dataset 4.112×28, fit 4.108 loại 4 query như Day 5–7. Lượt cuối **338 passed in 44.83s, 0 failed** (178 cũ + 160 mới), sau sửa cảnh báo thiếu K khi pool có zero candidate. Lượt trước đó 338 passed in 34.89s; baseline trước sửa 178 passed in 26.39s. Lỗi collection ban đầu do tên tham số pytest request đã sửa thành payload; suite cuối exit 0.
- Runner exit 0, 20 legacy checks + 20 scenario–engine cases đạt; direct/KNN full parity. Pools 22/10/94/47/0; Top K 5/5/5/5/0. CSV scenarios 20, filter stages 164, Top 5 80, full rankings 692; JSON ghi hash/config/query/reference/environment/Git. Không benchmark latency Day 8.
- **Git:** main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1; index giữ nguyên, không staged changes. Source Day 5–8/docs chưa commit; không fetch/push/deploy. Người dùng yêu cầu để commit khi chuyển máy; cần nhiệm vụ Git được phép, không tự làm theo mốc lịch.

Lệnh từ repo root:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day8 --output-dir reports/day8_rerun
```

Output-dir phải mới (runner từ chối directory tồn tại); Linux/macOS dùng .venv/bin/python. Không dependency/API key mới. Đọc DAY8.md để gọi API và hiểu hard/soft/missing; dùng bảng/JSON thực có khi trình bày.

**Điều kiện chuyển máy:** nhận source/tests/docs Day 5–8, features/candidates/raw snapshot ngoài Git và prior JSON Day 5/6/7 đúng hashes. Clone HEAD hiện tại chưa đủ. Fresh-install, full lock, temporal audit và metadata CLB tại cutoff chưa nghiệm thu. Adapter phụ thuộc private internals và full ranking, cần regression khi baseline đổi; chưa benchmark overhead/concurrency.

**Day 9 khi được giao:** explanation dựa trên số liệu gốc/cosine components/constraints, đầu ra so sánh thống nhất đơn vị/cutoff và missing; kiểm truy vết, ties/đảo dòng/nhóm ít phân biệt. Không bịa chỉ số GK/Defender, không Precision/NDCG thiếu labels. UI charts ở Day 21. Cập nhật log/insights/PRESENTATION_AND_DEFENSE/HANDOFF cùng inventory; chưa triển khai Day 9 trong phiên này.

## Bổ sung hồ sơ thuyết trình — 2026-11-02, sau Day 7

- Đọc [PRESENTATION_AND_DEFENSE](../reports/PRESENTATION_AND_DEFENSE.md) để chuẩn bị trình bày/bảo vệ: tổng hợp Day 1–7, file/công thức/kết quả có nguồn, khó khăn/giới hạn và 28 cặp hỏi–đáp. Đây là tài liệu tổng hợp, không phải thí nghiệm mới hoặc slides đã hoàn thành.
- Day cuối vẫn **Day 7**, Day 8 chưa triển khai. Số **178 passed, 0 failed** bên dưới thuộc lần chạy Day 7; phiên bổ sung này không chạy lại pytest/benchmark/pipeline. Chỉ kiểm tài liệu, liên kết, nguồn số liệu và bảo toàn file.
- Sau mỗi Day phải cập nhật đồng bộ PRESENTATION_AND_DEFENSE, project_log, insights_and_defense và HANDOFF; mỗi Day có 3–5 Q&A và phân biệt kết quả kiểm chứng/lịch sử chạy/giả thuyết/kế hoạch. Quy tắc đã ghi trong AGENTS và CLAUDE; inventory cập nhật khi thêm file.
- Git kiểm tra lại: main, HEAD c4d638c2d10c542c897ccf95dedde540814925b1, không staged diff; source Day 5–7/docs vẫn chưa commit. Không stage/commit/push/deploy/fetch. Điều kiện chuyển máy và lệnh chạy Day 7 bên dưới giữ nguyên.

## Cập nhật hiện hành sau Day 7 — 2026-11-02

**Day cuối: Day 7 hoàn thành có bằng chứng trong phạm vi KNN cosine benchmark và robustness. Day tiếp theo: Day 8, chưa triển khai.** Các mục Day 6 và phiên bàn giao bên dưới là lịch sử, không phải trạng thái hiện hành.

- Code mới: src/recommendation/knn.py, run_day7.py; tests/test_knn_recommendation.py; hướng dẫn [DAY7.md](../src/recommendation/DAY7.md). Không thay code/tests/data hoặc artefact Day 5–6.
- KNN dùng NearestNeighbors cosine/brute/n_jobs=1, đúng feature/scaler/reference của baseline Day 5 hoặc weights Day 6. Lọc rồi fit neighbors trên encoded vectors, lấy tất cả neighbors trước tie round12 + ID và Top K; không refit scaler theo query.
- Dataset vẫn 4.112×28, fit 4.108 loại 4 query; 10 cặp baseline/KNN full-ranking và 50 trường hợp K=1/3/5/50/10000 đạt. Nonempty overlap@5=1, Spearman≈1; max score difference=0, distance identity error <=4,45e-16. Empty không có metric stability hợp lệ.
- Tests: **178 passed in 20.19s, 0 failed** = 109 cũ + 69 mới. Baseline trước triển khai: 109 passed in 15.45s.
- Benchmark: 5 warm-up + 50 lần/method/query, luân phiên thứ tự, threadpool limit=1; 1.000 measured calls. Đo full recommend gồm filter/KNN.fit/retrieval/ranking/explanation, không gồm scaler/CSV I/O. KNN median cao hơn direct ở 8/8 nonempty trên máy/phiên này; chưa kết luận mọi workload hoặc chất lượng tuyển trạch. Giữ direct làm phương án hiện hành.
- reports/day7/ gồm evaluation.json, comparisons.csv (10), robustness.csv (50), timings.csv (1.000), benchmark.csv (20), rankings.csv (5.492), latency.png, summary.md. [Summary](../reports/day7/summary.md) và DAY7.md ghi bảng median/p95, Q&A, giới hạn.
- Git: main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1; index không đổi, source Day 5–7/docs vẫn chưa commit. Không stage/commit/push/deploy/fetch; giữ thay đổi có sẵn. Mốc Git kế tiếp Day 10, Day 5 còn chờ nhiệm vụ Git được phép.

Chạy suite: `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`.
Chạy benchmark lại, giữ artefact cũ: `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day7 --output-dir reports/day7_rerun --warmup 5 --repeats 50`. Chọn directory mới nếu đã tồn tại; runner không có --overwrite. Tránh chạy tests/project jobs đồng thời với benchmark. Linux/macOS thay executable bằng .venv/bin/python.

**Đầu vào bàn giao:** ngoài features/candidates và raw snapshot ngoài Git, cần source/tests Day 5–7, reports/day5_recommendation_examples.json và reports/day6/evaluation.json đúng source hashes. Clone HEAD hiện tại không đủ. Không cài dependency mới; threadpoolctl có sẵn qua sklearn. Fresh-install, full lock và kiểm máy đích vẫn chưa nghiệm thu.

**Day 8 khi được giao:** hoàn thiện bộ lọc vị trí/tuổi/EUR/phút và ngưỡng hiệu suất phù hợp dữ liệu thật; quy định schema/đơn vị/biên/no-results, kiểm kết hợp lọc→ranking và không nới điều kiện. Không dùng market value làm skill, không thêm chỉ số GK/Defender giả. Chưa có relevance labels nên chưa tính Precision/NDCG; không bắt đầu Day 8 trong nhiệm vụ Day 7.

## Snapshot sau Day 6 — 2026-11-02 (lịch sử)

**Rà soát trước Day 7 (cùng ngày, sau triển khai):** chạy lại suite bằng .venv, **109 passed in 14.60s, 0 failed**, pip check: No broken requirements found. 8/8 dataset khớp SHA-256/kích thước manifest; 6/6 source hashes trong evaluation.json khớp; artefact có 30 metric rows, 8.238 ranking rows, 264 correlation pairs. Đây là lượt test/đối chiếu mới; không chạy lại runner ghi báo cáo, cleaning/EDA hoặc cài môi trường sạch. Thời gian 13,12 giây bên dưới là lần triển khai trước, được giữ làm lịch sử.

**Kết luận bàn giao:** tài liệu đủ hướng dẫn tiếp tục có điều kiện, chưa chứng minh máy mới chạy được. CLAUDE/SETUP đã làm rõ phải nhận source/tests Day 5–6 và reports/day5_recommendation_examples.json (đầu vào đối chứng Day 6), ngoài snapshot data. Git vẫn main/c4d638c, origin cấu hình đúng; ref origin/main chỉ là cache local, chưa fetch. Source chưa commit, dữ liệu ngoài Git và fresh-install chưa nghiệm thu là các việc còn lại trước chuyển máy. Phiên rà soát chỉ bổ sung tài liệu, không làm Day 7 hoặc commit/push/deploy.

**Day cuối: Day 6 hoàn thành có bằng chứng trong phạm vi weighted cosine và đánh giá hành vi/độ nhạy. Day tiếp theo: Day 7, chưa triển khai.** Phần “phiên tài liệu” bên dưới được giữ làm snapshot lịch sử; mục này thay trạng thái Day cuối và lệnh kiểm thử cũ.

- Mới: src/recommendation/weighted.py, evaluation.py, run_day6.py, DAY6.md; tests/test_weighted_recommendation.py; reports/day6/ gồm evaluation.json, metrics.csv, rankings.csv, correlations.csv, comparison.png, correlations.png, summary.md.
- Không sửa baseline.py/run_day5.py/tests Day 4–5 hoặc artefact dữ liệu/báo cáo Day 5. Tái lập chính xác 5 kịch bản cũ; trọng số 1 khớp full ranking/score baseline.
- 4.112 cầu thủ × 28 cột, hash features vẫn 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0. Cùng fit 4.108 người và 4 query giữ riêng; không temporal split.
- 6 cấu hình × 5 kịch bản: 30/30 đạt filter/score/order/determinism; 24 nonempty + 6 empty, metric rỗng là null. Default mean overlap@5=.90; bỏ categorical=.25. Không coi ổn định là chất lượng, không có relevance labels nên không tính Precision/NDCG.
- Tests mới nhất: **109 passed in 13.12s, 0 failed** (57 cũ + 52 mới), dùng .venv; không cài dependency mới. Chi tiết trọng số, phạm vi metric, Q&A và giới hạn trong [DAY6.md](../src/recommendation/DAY6.md), [summary](../reports/day6/summary.md), project_log/insights.
- Git: main, HEAD c4d638c2d10c542c897ccf95dedde540814925b1; index không đổi, không stage/commit/push/deploy. Giữ thay đổi chưa commit từ Day 5 và bộ bàn giao; Day 6 thêm file untracked và cập nhật tài liệu. Không fetch hoặc xác minh GitHub trực tiếp.
- Source Day 5–6 + docs chưa commit; clone HEAD hiện tại vẫn thiếu chúng. Data ngoài Git, environment chưa lock/fresh-install vẫn là blockers bàn giao như snapshot bên dưới. Day 5 là mốc Git đang chờ; mốc tiếp theo Day 10, không tự tạo quyền commit/push từ lịch.

Chạy tests: `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`.
Artefact Day 6 đã tồn tại; chạy lại mà giữ cũ bằng `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day6 --output-dir reports/day6_rerun`. Script từ chối overwrite mặc định; chỉ dùng --overwrite có chủ đích. Linux/macOS thay executable bằng .venv/bin/python.

**Day 7 khi được giao:** KNN trên cùng feature/scaler/reference/filter để đối chứng với cosine/weighted cosine, kiểm cosine-distance parity, tie và self-exclusion; ghi top-K/pool/latency và độ nhạy. Giữ default Day 6 là giả thuyết, không gọi là tối ưu; chưa có relevance labels thì chưa đánh giá ranking quality. Defender/GK tiếp tục context_profile_only. Cập nhật logs/HANDOFF/inventory/tests sau mốc.

## Snapshot bàn giao trước khi triển khai Day 6 (lịch sử)

**Cập nhật: 2026-11-02. Day cuối có bằng chứng: Day 5 — baseline content-based. Day tiếp theo: Day 6, chưa triển khai.** Phiên hiện tại chỉ thiết lập tài liệu chuyển máy; không commit/push/deploy. AI mới đọc [CLAUDE](../CLAUDE.md) trước, không cần lịch sử chat Codex.

## Trạng thái Git tại lần kiểm tra

- Branch main; HEAD **c4d638c2d10c542c897ccf95dedde540814925b1**.
- Origin: https://github.com/tranhaidong23/ScoutIQ-AI.git.
- origin/main local cache cũng c4d638c; **không fetch hoặc kiểm chứng trạng thái GitHub trực tiếp trong phiên này**.
- Lịch sử từ cũ tới mới: 86c0360 Day 1 → 266f90f Day 4 → c4d638c Day 2–3. Không viết lại lịch sử.
- Khi bắt đầu: AGENTS.md, reports/project_log.md, reports/insights_and_defense.md đã modified; src/recommendation/, tests/test_recommendation.py và hai báo cáo day5_recommendation_examples chưa tracked. Không có staged diff.
- Phiên bàn giao thêm CLAUDE.md và docs/, bổ sung ba tài liệu lịch sử trên. Day 5 và tài liệu mới **vẫn chưa commit**; Git index được giữ nguyên. Đây là snapshot trạng thái, cần đọc lại git status ở phiên mới.

**Clone HEAD đã nêu không chứa Day 5 hoặc bộ tài liệu bàn giao này.** Trước khi rời máy cũ cần nhiệm vụ được phép rà soát/commit/push source Day 5 + docs; nếu không dùng Git để chuyển, người dùng phải chuẩn bị bản bàn giao source riêng đã rà secrets. Không chép toàn workspace gồm .venv/.env; không giả định tài liệu local đã có trên GitHub. Không tự thực hiện các hành động đó trong phiên tài liệu này.

## Bằng chứng mới và phần chưa xác minh

| Hạng mục | Kết quả 2026-11-02 |
|---|---|
| Tests bằng venv hiện có | 57 passed in 10.67s: 23 feature + 34 recommendation; exit 0 |
| Dependency consistency | pip check: No broken requirements found; exit 0 |
| Python/OS | Python 3.13.7, Windows 11; phiên bản package trong environment-observed.json |
| Data | 5 raw + 3 processed có hash; players 8.322×20, candidates 4.112×21, features 4.112×28 |
| Source/artifact | Đọc scripts, tests, reports, requirements và Git local |
| Chưa làm hôm nay | Fresh clone/install trên máy sạch, tải lại raw, chạy lại toàn pipeline/EDA/runner ghi báo cáo, kiểm tra GitHub trực tiếp, kiểm thử Linux/macOS |
| Sản phẩm web | Chưa có backend/frontend/database triển khai; không có app web để chạy |

Báo cáo kịch bản Day 5 là artefact lịch sử; lần test mới không được mô tả là đã tái chạy toàn bộ pipeline. [PROJECT_CONTEXT](PROJECT_CONTEXT.md) tổng hợp từng Day, phân biệt V/H/P.

## Các việc cần giải quyết để chuyển máy

1. **Source chưa xuất bản:** Day 5 + docs chưa commit/push; cần người dùng giao nhiệm vụ riêng trước chuyển máy.
2. **Dataset ngoài Git:** sao lưu/chuyển riêng 5 raw và 3 processed bằng ổ đĩa hoặc kho riêng có kiểm soát truy cập, giữ đường dẫn và kiểm SHA-256 theo [DATA_MANIFEST](DATA_MANIFEST.json). Chưa tạo/upload archive trong phiên này. Cần xác nhận quyền sử dụng/chia sẻ nguồn trước khi phân phối; không tự công khai dữ liệu.
3. **Môi trường chưa khóa:** requirements.txt UTF-16, unpinned; snapshot phiên bản là quan sát, không phải lockfile đã cài thử. [SETUP](SETUP.md) hướng dẫn chuyển bản requirements tạm sang UTF-8 trong venv và cài bằng Python mới. Kiểm tra tính sẵn có/khả năng tương thích package trên máy đích; không tuyên bố đã tái tạo thành công chỉ từ pip check máy cũ.
4. **Nguồn dữ liệu mutable:** download lại không bảo đảm snapshot cũ. Không thay hash kỳ vọng để che lệch dữ liệu; lưu bản mới riêng và xác minh.
5. **Không có service runtime:** hiện chạy scripts/library/tests. FastAPI/Streamlit/PostgreSQL/OpenAI/cloud là các Day sau; không cần key/DB cho baseline.

Trở ngại 1–3 ảnh hưởng bàn giao; không đồng nghĩa Day 5 chưa hoàn thành chức năng trong working tree. Các câu hỏi quyền truy cập repo, hệ điều hành máy đích, vị trí kho dữ liệu riêng chưa có câu trả lời xác minh; SETUP có nhánh Windows/POSIX để chuẩn bị.

## Bước tiếp theo khi được giao Day 6

- Đọc baseline/README/tests và Day 5 insights. Giữ baseline trọng số 1 làm đối chứng.
- Thiết kế trọng số numeric/categorical rõ nghĩa và thí nghiệm độ nhạy theo vị trí; tránh đếm lặp goals/assists/contributions, không thêm market value làm kỹ năng.
- Giữ fit/reference tách truy vấn, filter không làm thay tham số fit; kiểm vector 0, score hữu hạn, tie/ranking và bộ lọc.
- So ít nhất các tình huống thật hiện có, báo top-K stability và tác động trọng số; thiếu nhãn relevance thì không bịa Precision/NDCG.
- Defender/GK vẫn context_profile_only khi chưa có thống kê phù hợp; không gán trọng số bàn thắng cho GK.
- Chạy tests, ghi lệnh/cấu hình/evidence và cập nhật bộ tài liệu. Chưa làm Day 6 trong phiên bàn giao này.

## Lệnh khởi động sau khi nhận đủ source + data

Chạy từ repo root; Windows PowerShell:

```powershell
git status --short --branch
git log -5 --oneline
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pip check
```

Chưa có venv: làm [SETUP](SETUP.md). Linux/macOS thay executable bằng .venv/bin/python. Để chạy demo có ghi lại hai báo cáo Day 5, sau khi đã bảo vệ artefact cũ:

```powershell
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day5
```

SETUP có smoke query chỉ đọc không ghi báo cáo. Không chạy downloader/cleaning trên bản duy nhất của dữ liệu để “thử môi trường”.

## Quy trình cập nhật bàn giao sau mỗi Day

Cập nhật phần hiện hành của file này, thêm entry vào project_log/insights và cập nhật bắt buộc [PRESENTATION_AND_DEFENSE](../reports/PRESENTATION_AND_DEFENSE.md) (giữ lịch sử, ghi đính chính rõ ràng). Hồ sơ mỗi Day phải có mục tiêu, công việc, file/chức năng, công thức/lý do, kết quả dẫn nguồn tương đối, khó khăn/cách giải quyết, hạn chế và 3–5 Q&A; phân biệt lần chạy mới với báo cáo lịch sử, giả thuyết và kế hoạch. Đối chiếu AGENTS/PROJECT_CONTEXT, inventory và setup/architecture khi thay đổi. Không thay số liệu bằng dự định.

Mẫu nội dung cần điền:

```text
Ngày kiểm tra / Day:
Trạng thái: Dự kiến | Đang thực hiện | Đã hoàn thành có bằng chứng | Chưa xác minh | Bị chặn
Mục tiêu và phần thực sự hoàn thành:
File và input/output, snapshot/cutoff/hash:
Thuật toán/quyết định và bằng chứng:
Python/OS/dependencies, lệnh test, exit code/kết quả:
Branch / HEAD / remote ref kiểm tra khi nào:
Staged / unstaged / untracked và việc chưa bàn giao:
Commit thực có / push-deploy thực có hoặc chưa được phép:
Insights, hạn chế, blockers và cách gỡ:
Day tiếp theo / next steps / lệnh chạy:
Tài liệu đã cập nhật:
```

Mốc đề xuất commit/push: **Day 5 (đang chờ), 10, 15, 20, 25, 30; final release Day 31**. Kiểm diff/secrets/tests trước; không tự commit khi nhiệm vụ không cho phép, không tự push/deploy. Được phép ở mốc trước không tự mở quyền cho mốc sau.

Trước chuyển máy thực tế: làm mới Git/status/hash/test/version, nhận đủ source và dữ liệu, kiểm từ clone sạch theo SETUP, ghi kết quả vào nhật ký. Bộ tài liệu hiện tại là snapshot 2026-11-02, không cam kết trạng thái một tuần sau vẫn giống.
