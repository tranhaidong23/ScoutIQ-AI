# ScoutIQ — Kiểm kê file và phụ thuộc

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
## Bổ sung Day 12 — 2026-11-03

| File | Vai trò / input → output / phụ thuộc |
|---|---|
| [integrity.py](../src/evaluation/integrity.py) | Raw DOB/snapshot → calendar audit, classification, proposal, exclusions/coverage/lineage; pandas/stdlib và validators Day 11; không sửa engine/data |
| [pilot.py](../src/evaluation/pilot.py) | Scenarios/catalogue → stratified hash sample; CSV schema/registry validation, pairwise agreement/readiness; không tạo labels |
| [run_day12.py](../src/evaluation/run_day12.py) | Snapshot/Day 11 evidence có hash → reports mới; audit chỉ đọc, không network/apply correction |
| [test_day12_integrity.py](../tests/test_day12_integrity.py), [test_day12_pilot.py](../tests/test_day12_pilot.py) | Age/date/ID/conflict, exclusions/coverage, sampling/schema/provenance/agreement/readiness; SYNTHETIC math oracle và artefact thật |
| [age_integrity_audit.csv](../reports/day12/age_integrity_audit.csv), [age_discrepancies.csv](../reports/day12/age_discrepancies.csv) | 4.112 audit rows và subset 1 lệch, nguồn/DOB/cutoff/formula/cause |
| [correction_proposal.json](../reports/day12/correction_proposal.json) | Version PROPOSED, parent hashes/old-new/gates, chưa áp dụng |
| [coverage_analysis.csv](../reports/day12/coverage_analysis.csv), [eligibility_exclusions.csv](../reports/day12/eligibility_exclusions.csv) | Retention theo vị trí/tuổi/current-club proxy; 8.322 IDs cùng flags/reasons |
| [feature_lineage.csv](../reports/day12/feature_lineage.csv) | 28 cột: source/formula/unit/engine role/as-of limitations |
| [pilot_manifest.json](../reports/day12/pilot_manifest.json), [pilot_annotation_template.csv](../reports/day12/pilot_annotation_template.csv), [pilot_evidence.csv](../reports/day12/pilot_evidence.csv) | Seed 12/strata/32 IDs; template 15 trường unlabeled; facts/missing/limits không rank/score |
| [assessor_registry.json](../reports/day12/assessor_registry.json), [readiness.json](../reports/day12/readiness.json) | Registry rỗng, counts/gates/lý do chặn; không metric chất lượng thật |
| [audit.json](../reports/day12/audit.json), [validation.json](../reports/day12/validation.json) | Provenance/hashes/environment/checks, tests và bảo toàn source/data/index |
| [summary](../reports/day12/summary.md), [age findings](../reports/day12/age_integrity_findings.md), [provenance audit](../reports/day12/provenance_audit.md), [temporal review](../reports/day12/temporal_leakage_review.md), [pilot guide](../reports/day12/pilot_annotation_guide.md), [readiness](../reports/day12/evaluation_readiness.md) | Diễn giải bằng chứng, thiết kế correction, giới hạn/workflow/next steps |

Cập nhật 10 docs: AGENTS, CLAUDE, HANDOFF, PROJECT_CONTEXT, ARCHITECTURE, FILE_INVENTORY, SETUP, project_log, insights, PRESENTATION. Không dependency mới; requirements/manifests/data/source/tests/artefact Day 1–11 giữ nguyên. Không triển khai FastAPI/Neon/Gemini.

### Danh mục các mốc trước — lịch sử

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
## Bổ sung Day 11 — 2026-11-03

Danh sách dưới đây là file mới/thay đổi Day 11; danh mục cũ giữ nguyên bên dưới. Không đổi source/tests/artefact Day 1–10, requirements, manifests hoặc dữ liệu gốc.

| File | Vai trò / input → output / dependencies |
|---|---|
| [src/evaluation/__init__.py](../src/evaluation/__init__.py) | Namespace offline evaluation |
| [metrics.py](../src/evaluation/metrics.py) | Typed annotation/CSV → validation + gated P/R/NDCG, coverage/stability; Python stdlib; không tạo nhãn hoặc sửa engine |
| [audit.py](../src/evaluation/audit.py) | Đọc raw/processed, hash, tái aggregate/eligibility/temporal/position/age probes → dict; pandas/numpy + feature validator; không ghi data |
| [run_day11.py](../src/evaluation/run_day11.py) | Day 10 evidence, SCENARIOS, snapshot → thư mục output mới; service/config/filter helper/threadpoolctl; kiểm 16 full response/repeat/filter; không network |
| [tests/test_evaluation_protocol.py](../tests/test_evaluation_protocol.py) | Fixtures SYNTHETIC, sklearn NDCG oracle, invalid/edge/provenance gates + kiểm artefact thật; cần snapshot/Day 11 reports cho integration |
| [evaluation_protocol.md](../reports/day11/evaluation_protocol.md) | Scenario nguồn, universe, blinding, labels workflow, công thức/gates, commands |
| [relevance_rubric.md](../reports/day11/relevance_rubric.md) | Grade 0–3, hard/role/performance/evidence, abstain và context-only |
| [annotation_template.csv](../reports/day11/annotation_template.csv) | 173 scenario-player rows, 8 trường, mọi nhãn trống; dùng bản sao để annotation |
| [annotation_evidence.csv](../reports/day11/annotation_evidence.csv) | Facts/units từ snapshot, seed 11, không model/rank/score; GK/Defender chỉ context |
| [evaluation.json](../reports/day11/evaluation.json) | Run/environment/source/data/config/fit IDs/scenarios/checks, metric thực null, coverage/stability |
| [audit_evidence.json](../reports/day11/audit_evidence.json) | Read-only audit/hash/missing/retention/date/aggregation/age evidence |
| [synthetic_metrics.json](../reports/day11/synthetic_metrics.json) | Abstract IDs/grades và công thức SYNTHETIC, không dữ liệu cầu thủ giả |
| [audit_findings.md](../reports/day11/audit_findings.md) | Diễn giải audit V/H/U/P, lỗi tuổi và backlog |
| [run_summary.md](../reports/day11/run_summary.md), [summary.md](../reports/day11/summary.md) | Run digest tự sinh; kết luận có kiểm chứng, giới hạn/next steps do review |
| [validation.json](../reports/day11/validation.json) | Lệnh/kết quả pytest, bảo toàn snapshot/source/index và QA tài liệu cuối phiên |

Docs cập nhật: AGENTS, CLAUDE, PROJECT_CONTEXT, ARCHITECTURE, HANDOFF, FILE_INVENTORY, SETUP, project_log, insights_and_defense, PRESENTATION_AND_DEFENSE. Scope mới bỏ auth khỏi MVP, thay OpenAI bằng Gemini, PostgreSQL đích là Neon; tất cả web/database integrations vẫn dự kiến. Không dependency mới, không môi trường/secrets mới.

### Kiểm kê các mốc trước (lịch sử)

<!-- DAY11_CURRENT_END -->

Đối chiếu 2026-11-02. Phạm vi: source, tests, tài liệu, artefact và 8 dataset cần bàn giao; không liệt kê nội bộ .git/.venv hoặc caches. Đường dẫn trong bảng tính từ repo root. “Ghi” nghĩa là chạy script có thể thay thế output tại đường dẫn cố định. Các file Day 5 và bộ bàn giao chưa commit tại thời điểm này; xem [HANDOFF](HANDOFF.md), không suy ra tracked chỉ vì file có trong bảng.

## Root và tài liệu bàn giao

| File | Vai trò / input → output / phụ thuộc |
|---|---|
| [.gitignore](../.gitignore) | Bỏ venv, caches, .env/.env.*, raw/processed/external; không thay trong phiên này |
| [requirements.txt](../requirements.txt) | 11 dependency trực tiếp, UTF-16 LE BOM, chưa pin; input cài môi trường, không phải lock |
| [AGENTS.md](../AGENTS.md) | Yêu cầu sản phẩm, quy tắc và cập nhật trạng thái; giữ các mục lịch sử |
| [CLAUDE.md](../CLAUDE.md) | Điểm vào AI mới, thứ tự đọc và checklist sau mỗi Day |
| [docs/PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Sản phẩm, dữ liệu, tổng hợp Day 1–5, roadmap Day 6–31 |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | Luồng dữ liệu, hợp đồng recommender, kiến trúc ứng dụng dự kiến |
| [docs/FILE_INVENTORY.md](FILE_INVENTORY.md) | Danh mục này; cập nhật khi thêm/đổi file, I/O hoặc dependency |
| [docs/HANDOFF.md](HANDOFF.md) | Trạng thái hiện hành, HEAD/Day, blockers, next steps, lệnh và mẫu bàn giao |
| [docs/SETUP.md](SETUP.md) | Clone/venv/data/tests/scripts, Windows và POSIX, giới hạn tái tạo |
| [docs/DATA_MANIFEST.json](DATA_MANIFEST.json) | Kích thước/SHA-256 8 dataset; row/schema 3 processed, không có payload |
| [docs/environment-observed.json](environment-observed.json) | Python/OS và phiên bản direct dependencies + pip quan sát; không là full lock |

## Collection và preprocessing

Quy ước raw5 = players, clubs, games, appearances, player_valuations trong data/raw/*.csv.gz.

| File | Input | Output/tác dụng | Dependencies |
|---|---|---|---|
| [src/collection/download_data.py](../src/collection/download_data.py) | URL mutable /{table}.csv.gz | Ghi 5 raw; skip file sẵn khác rỗng; tạo raw dir | requests, pathlib |
| [src/collection/inspect_data.py](../src/collection/inspect_data.py) | raw5 | Ghi reports/day1_data_quality.csv; in shape/missing/duplicates | pandas |
| [src/collection/check_season.py](../src/collection/check_season.py) | games, appearances, valuations | stdout mùa/coverage; không ghi dataset | pandas |
| [src/preprocessing/01_explore_data.py](../src/preprocessing/01_explore_data.py) | 5 hàng mỗi raw5 | stdout mẫu/schema | pandas |
| [src/preprocessing/02_check_columns.py](../src/preprocessing/02_check_columns.py) | Mẫu players, clubs, appearances, games | stdout cột | pandas |
| [src/preprocessing/clean_data.py](../src/preprocessing/clean_data.py) | raw5 | Ghi processed/scoutiq_players_2025_26.csv; tạo processed dir | pandas |
| [src/preprocessing/create_candidates.py](../src/preprocessing/create_candidates.py) | players processed | Ghi processed/scoutiq_candidates_2025_26.csv | pandas |
| [src/preprocessing/validate_data.py](../src/preprocessing/validate_data.py) | players processed | stdout chẩn đoán; không phải pytest/assertion suite | pandas |

Trừ downloader có main guard, các script collection quan sát/preprocessing thực thi ở top-level. Không import để chỉ đọc định nghĩa. Xem code trước khi chạy, đặc biệt downloader có xử lý xóa file tải dở khi requests lỗi; không dùng nó để xác nhận raw sẵn có.

## EDA, features, recommendation và tests

| File | Input | Output/tác dụng | Dependencies |
|---|---|---|---|
| [src/eda/eda_analysis.py](../src/eda/eda_analysis.py) | candidates | Ghi 5 PNG 01–05 và day3_position_summary.csv | pandas, numpy, matplotlib, seaborn |
| [src/eda/age_group_analysis.py](../src/eda/age_group_analysis.py) | candidates | Ghi day3_age_group_summary.csv | pandas |
| [src/features/build_features.py](../src/features/build_features.py) | candidates | Ghi features CSV, day4_feature_quality.json, day4 PNG; hàm validate/build dùng lại | pandas, numpy, matplotlib; stdlib hash/json |
| [src/recommendation/baseline.py](../src/recommendation/baseline.py) | features/DataFrame và fit IDs/query/filters | Đọc CSV, fit trong RAM, trả dict Top K/evidence; không ghi file | pandas, numpy, sklearn StandardScaler; build_features validators (kéo theo matplotlib) |
| [src/recommendation/run_day5.py](../src/recommendation/run_day5.py) | features, 5 SCENARIOS cố định | Ghi day5_recommendation_examples.json và .md | baseline, build_features, pandas, numpy, sklearn |
| [src/recommendation/README.md](../src/recommendation/README.md) | Hợp đồng/code Day 5 | Usage, feature policies, leakage/limits; tài liệu |
| [tests/test_features.py](../tests/test_features.py) | candidates thật, biến thể lỗi trong RAM | 23 tests; roundtrip file temp, không sửa source data | pytest, pandas, numpy, build_features |
| [tests/test_recommendation.py](../tests/test_recommendation.py) | features thật, SCENARIOS, biến thể RAM | 34 tests input/filter/cosine/rank/explanation/fit isolation; không ghi dataset | pytest, pandas, numpy, baseline, run_day5 |

EDA scripts thực thi top-level; feature/recommendation runner có main guard. Không có pyproject/setup package; chạy từ repo root để namespace src import đúng. Tests cần data bị ignore; checkout code riêng chưa đủ chạy.

## Artefact reports

Các kết quả số trong artefact có ngày thực hiện riêng; việc đọc chúng 2026-11-02 không phải chạy lại pipeline.

| File | Nguồn tạo / nội dung |
|---|---|
| [reports/project_log.md](../reports/project_log.md) | Nhật ký tiến độ, roadmap, code/test/Git; bổ sung theo phiên |
| [reports/insights_and_defense.md](../reports/insights_and_defense.md) | Quyết định, evidence, giới hạn và phản biện; giữ lịch sử |
| [reports/day1_data_quality.csv](../reports/day1_data_quality.csv) | inspect_data; shape, duplicates, missing_percent raw5 |
| [reports/day3_position_summary.csv](../reports/day3_position_summary.csv) | eda_analysis; tổng hợp theo vị trí |
| [reports/day3_age_group_summary.csv](../reports/day3_age_group_summary.csv) | age_group_analysis; tổng hợp theo nhóm tuổi |
| [reports/day4_feature_quality.json](../reports/day4_feature_quality.json) | build_features; schema/range/missing/per90/hash/skew/warnings |
| [reports/day5_recommendation_examples.json](../reports/day5_recommendation_examples.json) | run_day5; input hash, fit audit, scenarios, kết quả/evidence |
| [reports/day5_recommendation_examples.md](../reports/day5_recommendation_examples.md) | run_day5; bảng Top 5 và explanation cho người đọc |
| [reports/figures/01_market_value_distribution.png](../reports/figures/01_market_value_distribution.png) | EDA; phân phối market value |
| [reports/figures/02_age_vs_market_value.png](../reports/figures/02_age_vs_market_value.png) | EDA; tuổi và định giá |
| [reports/figures/03_market_value_by_position.png](../reports/figures/03_market_value_by_position.png) | EDA; định giá theo vị trí |
| [reports/figures/04_attacking_performance.png](../reports/figures/04_attacking_performance.png) | EDA; goals/90 và assists/90 |
| [reports/figures/05_correlation_heatmap.png](../reports/figures/05_correlation_heatmap.png) | EDA; tương quan, không chứng minh nhân quả |
| [reports/figures/day4_market_value_transformation.png](../reports/figures/day4_market_value_transformation.png) | build_features; phân phối triệu EUR trước/sau log1p |

## Dataset ngoài Git

Hash/bytes/schema đầy đủ trong DATA_MANIFEST. Không dùng Markdown link tới dataset để hàm ý clone đã có file.

| Đường dẫn | Vai trò/input → output sử dụng |
|---|---|
| data/raw/players.csv.gz | Metadata cầu thủ, DOB/vị trí/CLB → clean_data |
| data/raw/clubs.csv.gz | Metadata CLB → clean_data |
| data/raw/games.csv.gz | Mùa/ngày trận → lọc games, ghép appearances |
| data/raw/appearances.csv.gz | Phút/goals/assists theo trận → tổng hợp cầu thủ |
| data/raw/player_valuations.csv.gz | Định giá có ngày → chọn định giá tại cutoff |
| data/processed/scoutiq_players_2025_26.csv | clean_data output; 8.322×20 → candidates/validation |
| data/processed/scoutiq_candidates_2025_26.csv | create_candidates output; 4.112×21 → EDA/features/tests |
| data/processed/scoutiq_features_2025_26.csv | build_features output; 4.112×28 → recommender/tests |

Không có dữ liệu users/chat/history/DB thật trong phạm vi đã triển khai. Không đưa keys/passwords hoặc thông tin riêng tư vào manifests.

## Thư mục chưa triển khai và môi trường

backend/, frontend/, database/, notebooks/, slides/ hiện không có file; vai trò dự kiến lần lượt API, UI, schema/migration, thử nghiệm và trình bày. Không có Dockerfile/CI workflow/entrypoint web hoặc migration hiện hữu để liệt kê. data/external/ là đường dẫn ignore dự kiến, không phải nguồn đã dùng.

.venv/ chứa interpreter/dependencies cục bộ, không bàn giao nguyên thư mục; .git/ là metadata Git, không chỉnh tay; __pycache__/ và *.pyc là artefact chạy, không source. .env.example chưa tạo vì baseline chưa có hợp đồng biến môi trường; xem SETUP trước khi bổ sung.

Sau mỗi Day, thêm file và quan hệ I/O/dependency mới vào bảng tương ứng, ghi trạng thái đã có/dự kiến đúng thực tế. Không xóa ghi nhận lịch sử khỏi project_log khi file đổi vai trò.

## Bổ sung Day 6 — 2026-11-02

Giữ nguyên file/code/tests Day 4–5 liệt kê phía trên. Source Day 6 chưa commit; tất cả output dưới đây là dẫn xuất riêng, không thay dataset/artefact cũ.

| File | Vai trò, input → output và dependencies |
|---|---|
| [src/recommendation/weighted.py](../src/recommendation/weighted.py) | Config theo position, validation w>=0, sqrt(w)+L2; DataFrame/features → Top K/evidence; kế thừa baseline, pandas/numpy |
| [src/recommendation/evaluation.py](../src/recommendation/evaluation.py) | Full ranking → contract checks, overlap@K và Spearman average-rank trên pool chung; pandas/numpy; không relevance metrics |
| [src/recommendation/run_day6.py](../src/recommendation/run_day6.py) | Features + Day 5 JSON + SCENARIOS → 7 artefact Day 6; dùng baseline/weighted/evaluation, pandas/numpy/sklearn/matplotlib; không overwrite mặc định |
| [src/recommendation/DAY6.md](../src/recommendation/DAY6.md) | Công thức, API, cấu hình, protocol, kết quả, giới hạn và Day 7 |
| [tests/test_weighted_recommendation.py](../tests/test_weighted_recommendation.py) | Features thật + lỗi trong RAM → 52 tests mới; pytest, pandas/numpy, modules Day 5–6 |
| [reports/day6/evaluation.json](../reports/day6/evaluation.json) | Input/source hash, env/Git, reference, config/audits, 30 metrics, Top K/evidence |
| [reports/day6/metrics.csv](../reports/day6/metrics.csv) | 30 tổ hợp 6 config × 5 scenario; behavior/stability, undefined ghi trống |
| [reports/day6/rankings.csv](../reports/day6/rankings.csv) | 8.238 dòng full ranking; dùng kiểm metric chung, không là ground truth |
| [reports/day6/correlations.csv](../reports/day6/correlations.csv) | 264 cặp Pearson/Spearman, fit-only theo position; cờ abs(Pearson)>=.8 và lý do undefined |
| [reports/day6/comparison.png](../reports/day6/comparison.png) | Heatmap overlap@5 và full-common Spearman của 4 query nonempty |
| [reports/day6/correlations.png](../reports/day6/correlations.png) | 4 heatmap Pearson; biến chẩn đoán không đồng nghĩa model features |
| [reports/day6/summary.md](../reports/day6/summary.md) | Bảng so sánh và Top 5 mặc định; tự sinh bởi run_day6 |

Tổng suite hiện hành: 109 tests. AGENTS, CLAUDE, HANDOFF, PROJECT_CONTEXT, ARCHITECTURE, SETUP và hai báo cáo cập nhật trạng thái Day 6; DATA_MANIFEST và environment-observed giữ snapshot bàn giao cũ vì không đổi dữ liệu hoặc cài dependency.

## Bổ sung Day 7 — 2026-11-02

Các file Day 5–6 giữ nguyên; bảng này cập nhật trạng thái suite thành **178 tests** và thêm 12 file, chưa commit.

| File | Vai trò, input → output / dependency |
|---|---|
| [src/recommendation/knn.py](../src/recommendation/knn.py) | Features/DataFrame + fit IDs + weights/query/filter → Top K/evidence/distance; dùng nguyên representation baseline/weighted, sklearn NearestNeighbors cosine/brute, pandas/numpy |
| [src/recommendation/run_day7.py](../src/recommendation/run_day7.py) | Features + Day 5/6 JSON/source hashes → 8 artefact; parity/K robustness + benchmark warm-up/repeats; sklearn, pandas/numpy/matplotlib, threadpoolctl (đã có qua sklearn) |
| [src/recommendation/DAY7.md](../src/recommendation/DAY7.md) | Implementation/API, protocol, actual timings, Q&A, giới hạn và Day 8 |
| [tests/test_knn_recommendation.py](../tests/test_knn_recommendation.py) | Data thật, lỗi trong RAM và vector/timing fixtures toán học → 69 tests mới; không export dữ liệu giả |
| [reports/day7/evaluation.json](../reports/day7/evaluation.json) | Dataset/prior/source hash, environment/threadpools/protocol, audit/config/query/evidence/parity/timings/Git |
| [reports/day7/comparisons.csv](../reports/day7/comparisons.csv) | 10 cặp representation–scenario; full ranking/filter/distance/stability/repeat checks |
| [reports/day7/robustness.csv](../reports/day7/robustness.csv) | 50 trường hợp K=1/3/5/50/10000, prefix/full parity |
| [reports/day7/timings.csv](../reports/day7/timings.csv) | 1.000 measured latency samples, repeat/order; không gồm warm-up |
| [reports/day7/benchmark.csv](../reports/day7/benchmark.csv) | 20 nhóm × 50 samples: median/p95/min/max ms |
| [reports/day7/rankings.csv](../reports/day7/rankings.csv) | 5.492 full-ranking rows; cosine_distance chỉ có ở KNN |
| [reports/day7/latency.png](../reports/day7/latency.png) | Median/p95 local theo representation/method/scenario; không quality/SLA |
| [reports/day7/summary.md](../reports/day7/summary.md) | Bảng timing và parity/limits tự sinh |

Runner Day 7 từ chối ghi đè; --output-dir mới để chạy lại, --warmup >=1, --repeats >=10. Mặc định 5/50, không cài dependency mới, không thay requirements hoặc manifests. Các báo cáo quản lý/AGENTS/CLAUDE/HANDOFF/ARCHITECTURE/SETUP/PROJECT_CONTEXT cập nhật trạng thái Day 7; lịch sử giữ trong logs.

## Bổ sung hồ sơ thuyết trình — 2026-11-02

| File | Vai trò / input → output / phụ thuộc |
|---|---|
| [reports/PRESENTATION_AND_DEFENSE.md](../reports/PRESENTATION_AND_DEFENSE.md) | Log/insights, code/tests, CSV/JSON/biểu đồ và Git local → hồ sơ Day 1–7 với mục tiêu, file, công thức/lý do, bằng chứng, khó khăn, hạn chế, 28 Q&A; Markdown, không dependency chạy mới |

AGENTS/CLAUDE quy định cập nhật hồ sơ này cùng project_log, insights_and_defense và HANDOFF sau mỗi Day (3–5 Q&A/Day). Phiên này chỉ sửa tài liệu; trạng thái Day 7, code/tests/data/artefact thực nghiệm, requirements và manifests không đổi. Số 178 tests là kết quả lịch sử Day 7, không phải suite chạy trong phiên tài liệu.

## Bổ sung Day 8 — 2026-11-02

Suite hiện hành **338 tests (178 cũ + 160 mới)**, 0 failed. Không sửa source/tests/artefact cũ. Mười file mới của mốc:

| File | Vai trò / input → output / dependencies |
|---|---|
| [src/recommendation/constraints.py](../src/recommendation/constraints.py) | SearchFilters + advanced request + fitted engine → hard mask/audit/Top K; numpy/pandas và baseline/weighted/KNN có sẵn; không fit hay ghi dataset |
| [src/recommendation/run_day8.py](../src/recommendation/run_day8.py) | Features + prior JSON Day 5/6/7 + source hash → 6 artefact riêng; validate/oracle/legacy/parity, stdlib/numpy/pandas/sklearn; từ chối output-dir đã tồn tại |
| [src/recommendation/DAY8.md](../src/recommendation/DAY8.md) | API, đơn vị/missing/hard-soft contract, lệnh, số liệu/Q&A và Day 9 |
| [tests/test_advanced_constraints.py](../tests/test_advanced_constraints.py) | Data thật, variants RAM → 160 tests mới, pytest; không sửa dataset |
| [reports/day8/evaluation.json](../reports/day8/evaluation.json) | Dataset/source/prior hashes, môi trường/HEAD, fit IDs, config/query, audit/evidence/20 legacy checks |
| [reports/day8/scenarios.csv](../reports/day8/scenarios.csv) | 20 scenario–engine cases, counts/status/behavior checks |
| [reports/day8/filter_stages.csv](../reports/day8/filter_stages.csv) | 164 dòng before/after/removed theo thứ tự hard constraints |
| [reports/day8/top5.csv](../reports/day8/top5.csv) | 80 dòng Top 5 cho 4 nonempty scenarios × 4 engine, dữ liệu/explanation/soft match |
| [reports/day8/rankings.csv](../reports/day8/rankings.csv) | 692 dòng full eligible rankings/evidence, không ground truth |
| [reports/day8/summary.md](../reports/day8/summary.md) | Bảng trước/sau, Top 5 weighted và giới hạn, tự sinh bởi runner |

Cập nhật AGENTS/CLAUDE, project_log/insights/PRESENTATION_AND_DEFENSE, HANDOFF/ARCHITECTURE/SETUP/PROJECT_CONTEXT và inventory. Không cài dependency hoặc đổi requirements/manifests; không tạo ảnh vì bảng đã đủ thể hiện số lượng. Source Day 5–8/docs chưa commit, dữ liệu ngoài Git và fresh-install chưa nghiệm thu. Commit để khi chuyển máy theo yêu cầu, không thao tác Git trong phiên Day 8.

## Bổ sung Day 9 — 2026-11-02

Suite hiện hành **453 tests (338 cũ + 115 mới), 0 failed**. Giữ source/tests/artefact Day 5–8; 12 file mới:

| File | Vai trò / input → output / dependencies |
|---|---|
| [src/recommendation/comparison.py](../src/recommendation/comparison.py) | Catalogue đã validate + 2–5 ID → identity/units/missing/numeric và categorical comparisons; stdlib/numpy/pandas/Day 4 validator/baseline policies, không scoring hoặc ghi data |
| [src/recommendation/explainability.py](../src/recommendation/explainability.py) | Fitted engine + request/response → JSON envelope giữ nguyên recommendation, structured evidence + rule-based text; dùng comparison và Day 5–8, không API hoặc refit |
| [src/recommendation/run_day9.py](../src/recommendation/run_day9.py) | Features + reports/day8/evaluation.json + source hashes/fit IDs/query/config → 7 artefact; stdlib/numpy/pandas/sklearn/matplotlib có sẵn, output-dir phải mới |
| [src/recommendation/DAY9.md](../src/recommendation/DAY9.md) | API example, schema/units/delta/missing, cách chạy, bằng chứng/tests/giới hạn; Markdown |
| [tests/test_explainability.py](../tests/test_explainability.py) | 115 tests từ snapshot thật và biến thể lỗi chỉ trong RAM; 4 engines/legacy/tampering/units/zero/missing/2–5 IDs/ablation/no-refit/permutation, pytest và dependencies cũ |
| [reports/day9/evaluation.json](../reports/day9/evaluation.json) | 20 cases, 80 explanations, 32 groups; nguyên responses, request/reference/config/hash/env/HEAD, JSON hữu hạn |
| [reports/day9/checks.csv](../reports/day9/checks.csv) | 20 dòng pool/K/status/parity/text-from-evidence checks |
| [reports/day9/top5.csv](../reports/day9/top5.csv) | 80 dòng Top 5 với identity/score/method/scope/text; no-results không fake row |
| [reports/day9/feature_evidence.csv](../reports/day9/feature_evidence.csv) | 260 dòng selected feature/weight/raw values/unit/component sum/delta; categorical không có numeric delta |
| [reports/day9/comparisons.csv](../reports/day9/comparisons.csv) | 448 dòng numeric comparisons, signed/absolute/relative và lý do null; categorical nằm trong JSON |
| [reports/day9/attack_comparison.png](../reports/day9/attack_comparison.png) | Reference + Top 4 weighted Attack, ba panel goals/90/assists/90/minutes; không tổng điểm hoặc kết luận winner, hạng 5 ở nhóm pair trong JSON/CSV |
| [reports/day9/summary.md](../reports/day9/summary.md) | Top 5 weighted cho 5 scenarios, text/comparison tables/limits và link PNG; tự sinh từ runner |

Cập nhật 10 tài liệu quản lý: AGENTS, CLAUDE, project_log, insights_and_defense, PRESENTATION_AND_DEFENSE, HANDOFF, ARCHITECTURE, SETUP, PROJECT_CONTEXT và inventory này. Không dependency mới/đổi manifests; source/data/artefact cũ được giữ. Source Day 5–9/docs chưa commit, chuyển máy cần nhận snapshot riêng và kiểm môi trường sạch. Day 10 dự kiến dịch vụ Python tích hợp, chưa triển khai; không commit/push/deploy.

## Bổ sung Day 10 — 2026-11-02

Suite hiện hành **549 tests (453 cũ + 96 mới), 0 failed**. Không sửa source/tests/artefact Day 5–9; 15 file mới:

| File | Vai trò / input → output / dependencies |
|---|---|
| [src/recommendation/config.py](../src/recommendation/config.py) | Root/module location → portable ProjectPaths; defaults/weights → validated ServiceConfig; pathlib/dataclasses/Day 6 validation, không secrets |
| [src/recommendation/schemas.py](../src/recommendation/schemas.py) | JSON request/response → structural/domain/finite/cross-field validation; exported Draft 2020-12 definitions, jsonschema/stdlib/Day 5–9 validators |
| [src/recommendation/service.py](../src/recommendation/service.py) | Catalogue/reference/config → bốn fitted engines; dict/JSON request → finite JSON response + metadata/explanation/optional comparisons; pandas/stdlib và modules Day 5–9 |
| [src/recommendation/run_day10.py](../src/recommendation/run_day10.py) | Features + prior JSON Day 8/9/source hashes + config → parity/reproducibility/latency và 8 artefact tự sinh; numpy/pandas/threadpoolctl/stdlib/dependency metadata, output-dir mới |
| [src/recommendation/DAY10.md](../src/recommendation/DAY10.md) | API example, request/response contract, config/path/hash/validation, commands/protocol/limitations/Day 11 |
| [tests/test_service.py](../tests/test_service.py) | 96 tests: Day 9 exact parity/JSON/determinism, invalid inputs/empty/zero/large K/serialization/config/permutation/no-refit/response consistency/latency math; pytest + libs trên snapshot thật |
| [reports/day10/evaluation.json](../reports/day10/evaluation.json) | 20 full responses, checks/benchmark, dataset/reference/config/audits, 16 source/3 input hashes, env/HEAD/protocol/startup observation |
| [reports/day10/request.schema.json](../reports/day10/request.schema.json) | Request schema export từ schemas.py; runtime vẫn bổ sung native-integer/finite/domain checks |
| [reports/day10/response.schema.json](../reports/day10/response.schema.json) | Response structural core + legacy extensions; runtime vẫn bổ sung cross-field consistency |
| [reports/day10/checks.csv](../reports/day10/checks.csv) | 20 cases: status/hard/rankable/returned/K và full Day 8/9/comparison parity |
| [reports/day10/top5.csv](../reports/day10/top5.csv) | 80 shortlist rows với ID/name/position/age/EUR/minutes/score, no-results không fake row |
| [reports/day10/timings.csv](../reports/day10/timings.csv) | 400 measured calls: scenario/method/repeat/ms/response bytes; warm-up không nằm trong CSV |
| [reports/day10/benchmark.csv](../reports/day10/benchmark.csv) | 20 nhóm ×20 samples: median/p95/min/max; numpy linear percentile |
| [reports/day10/summary.md](../reports/day10/summary.md) | Bảng parity/pool/latency và Top 5 weighted, protocol/limits; tự sinh bởi runner |
| [reports/day10/phase_review.md](../reports/day10/phase_review.md) | Tổng kết Day 5–10 từ code/artefact/logs, nghiệm thu integration vs giới hạn quality, latency table, 4 Q&A, next steps; viết sau kiểm chứng |

requirements.txt được bổ sung jsonschema>=4.18,<5 (bản 4.26.0 có sẵn), giữ bytes nội dung cũ/UTF-16; pip check đạt, không cài package. Cập nhật 10 tài liệu quản lý như Day 9; không đổi dữ liệu/manifests. Source Day 5–10/docs chưa commit, data ngoài Git/fresh-install chưa nghiệm thu; không commit/push/deploy, Day 11 chưa triển khai.
