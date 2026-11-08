# ScoutIQ — Cài đặt và tái tạo trên máy khác

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
## Bổ sung cách chạy Day 12

Day 12 chạy local, không cần Gemini API key, Neon URL hoặc login. Cần nguyên snapshot raw/processed và reports/source Day 11; hashes được kiểm trước runner. Không import cleaning/candidates/EDA để audit vì có thể ghi đè output.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day12 --output-dir reports/day12_recheck
```

POSIX dùng `.venv/bin/python`; chọn thư mục output chưa tồn tại, không overwrite annotation.

Mặc định reports/day12 đã tồn tại nên runner từ chối. `--seed 12 --per-scenario 8` là cấu hình frozen; thay tham số tạo run/pilot khác, không đổi bản đã phát cho assessor. Nhãn thật dùng bản sao template; xem [guide](../reports/day12/pilot_annotation_guide.md). Correction JSON chỉ PROPOSED, không có lệnh apply/promotion trong Day 12.

Suite có tests đọc snapshot/artefact thật và fixtures SYNTHETIC kiểm công thức/schema. [Validation](../reports/day12/validation.json) ghi kết quả thực. Clone HEAD c4d638c chưa đủ source hiện hành; dữ liệu bị ignore cần bàn giao riêng. Fresh-install/máy mới chưa xác minh; không tự push/deploy.

### Hướng dẫn cài đặt các mốc trước

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
## Bổ sung hiện hành — chạy Day 11 và phạm vi MVP mới

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

Day 11 hoàn toàn local; không cần Gemini API key, Neon URL hoặc login. Chưa có lệnh chạy FastAPI/Streamlit/Neon/Gemini thực tế vì chưa triển khai. Các đoạn OpenAI/auth bên dưới là kế hoạch cũ, không cấu hình cho MVP hiện hành. Giữ cách clone/venv/snapshot/tests cũ, bổ sung:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck
```

```bash
.venv/bin/python -B -m pytest tests -q -p no:cacheprovider
.venv/bin/python -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck
```

Output phải chưa tồn tại; không xóa/ghi đè annotation đã chấm để chạy lại. Runner mặc định `reports/day11` sẽ từ chối nếu thư mục có sẵn. Cần nguyên snapshot 8 file theo DATA_MANIFEST và Day 10 artefacts/source; không import clean_data.py/create_candidates.py để audit vì có tác dụng ghi. Hash ở reports/day11/audit_evidence.json. Source Day 5–11/docs chưa commit; clone c4d638c chưa đủ. Fresh-install và máy đích chưa nghiệm thu. Requirements UTF-16/unpinned lịch sử giữ nguyên; không tự coi environment-observed.json là lock đầy đủ.

Annotation: sao chép reports/day11/annotation_template.csv sang file riêng ngoài artefact gốc; grade blank giữ None, không impute. `src.evaluation.metrics.load_annotations` đọc CSV; sau đó chọn scenario/assessor/provenance và gọi `assess_ranking` với candidate_ids từ evaluation.json. Không có runner tự thu human labels, không có model tạo nhãn. [Protocol](../reports/day11/evaluation_protocol.md) mô tả điều kiện được phép báo metrics.

Khi đến phase web, secrets Gemini/Neon nằm phía server/env/secrets manager; chỉ placeholder trong mẫu cấu hình. Chưa cần tạo .env.example cho Day 11, không tải credentials máy cũ. Anonymous session token không phải account; cần isolation/lifecycle/retention tests trước triển khai. Không push/deploy theo lệnh setup khi chưa được phép.

### Hướng dẫn setup lịch sử (áp dụng phần không xung đột)

<!-- DAY11_CURRENT_END -->

## Cập nhật chạy Day 10 — 2026-11-02

Nhận thêm config.py/schemas.py/service.py/run_day10.py/[DAY10.md](../src/recommendation/DAY10.md), tests/test_service.py, [reports/day10](../reports/day10/summary.md) và [phase review](../reports/day10/phase_review.md). Suite hiện hành **549 passed in 62.01s, 0 failed**; các kết quả Day 9 trở về trước bên dưới là lịch sử. Day 11 chưa triển khai.

requirements.txt thêm dependency trực tiếp `jsonschema>=4.18,<5`, giữ UTF-16/nội dung cũ. Bản 4.26.0 đã có trong .venv hiện tại; không cài package mới trong phiên; pip check đạt. Pydantic chưa cài và không được dùng. Trên máy mới cài requirements theo hướng dẫn encoding phía dưới; không chỉ dựa jsonschema transitively qua Jupyter. Không cần API key cho service local.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day10 --output-dir reports/day10_rerun --warmup 3 --repeats 20
```

Linux/macOS dùng .venv/bin/python. Output-dir phải mới, không overwrite; runner nhận --features/--prior-day8/--prior-day9 nếu đổi vị trí đầu vào. Cần features + JSON Day 8/9 và đúng source hashes; không tái chạy raw pipeline hoặc runner cũ chỉ để chạy Day 10. Không chạy pytest/tác vụ dự án nặng đồng thời benchmark. 3 warm-up/20 repeats × 20 cases, timing parse→validate→rank→explain→compare→validate→serialize, không network/startup/fit.

Service example trong DAY10 dùng RecommendationService.from_csv và fit IDs Day 9, recommend(dict)/recommend_json(str). Không truyền fit IDs sẽ fit toàn catalogue, không tương đương runner. Bốn methods có tên explicit; weights phía config, mặc định cosine. Paths portable theo module/root, không có lệnh uvicorn/streamlit vì chưa web app/endpoint. Schema export đi cùng runtime checks ID/K integer/finite/cross-field; không dùng riêng JSON Schema như đầy đủ contract.

20/20 Day 8–9 responses/explanations/comparisons nguyên vẹn, 400 measured calls deterministic; local latency không cloud SLA hoặc quality. Source/tests/docs/reports Day 5–10 vẫn chưa commit tại HEAD c4d638c; clone riêng HEAD thiếu công việc mới. Bàn giao riêng 8 datasets theo DATA_MANIFEST, prior JSON, requirements mới; không chuyển venv/secrets. Fresh-install/full lock/máy đích chưa nghiệm thu. Mốc Day 10 chờ người dùng khi chuyển máy; không tự commit/push/deploy.

## Cập nhật chạy Day 9 — 2026-11-02

Nhận thêm explainability.py/comparison.py/run_day9.py/[DAY9.md](../src/recommendation/DAY9.md), tests/test_explainability.py và reports/day9. Suite hiện hành **453 passed in 59.76s, 0 failed** trên .venv Windows hiện có; số test trong các mục bên dưới là lịch sử. Không dependency hoặc API key mới. Day 10 chưa triển khai; không có web app/API server để chạy.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day9 --output-dir reports/day9_rerun
```

Directory đầu ra phải chưa tồn tại, runner không overwrite. Linux/macOS thay executable bằng .venv/bin/python. Day 9 trực tiếp đọc features + reports/day8/evaluation.json, kiểm feature/source hashes và dùng fit IDs/config/query Day 8; không cần tái chạy raw pipeline hoặc các runner cũ. Muốn tái lập chuỗi trước đó cần prior JSON Day 5/6/7 như hướng dẫn từng mục. Mismatch phải điều tra, không sửa hash hoặc tái sinh báo cáo để che sai khác.

Kết quả: 20 responses nguyên Day 8, 80 explanations, 32 nhóm 2–5 cầu thủ; [summary](../reports/day9/summary.md) và JSON/CSV/PNG nằm riêng. Evidence tách text, null có lý do, units EUR/per90/minutes; không gọi OpenAI/FastAPI. API sample DAY9 dùng fit IDs của runner, không tự fit catalogue để tái lập số liệu.

Source/tests/docs Day 5–9 và báo cáo chưa commit tại HEAD c4d638c, clone riêng HEAD chưa đủ. Mang riêng 8 dataset theo DATA_MANIFEST, không chuyển venv/secrets. Fresh-install/full lock/máy đích chưa nghiệm thu; không thay requirements/manifests trong Day 9. Commit/push chỉ khi được cho phép trong nhiệm vụ chuyển máy; không tự thực hiện theo lịch.

## Cập nhật chạy Day 8 — 2026-11-02

Nhận thêm constraints.py, run_day8.py, DAY8.md, tests/test_advanced_constraints.py và reports/day8. Suite hiện hành **338 passed in 44.83s, 0 failed** trên .venv Windows hiện có (lượt trước chỉnh cảnh báo zero-candidate: 34,89 s); các số 178/109/57 phía dưới là lịch sử. Không cài dependency mới, không cần API key cho search local.

Chạy toàn suite: `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`.
Chạy lại thí nghiệm giữ artefact cũ: `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day8 --output-dir reports/day8_rerun` (directory phải chưa tồn tại). Linux/macOS thay executable bằng .venv/bin/python. Runner cần features và prior reports/day5_recommendation_examples.json, reports/day6/evaluation.json, reports/day7/evaluation.json; đối chiếu hashes với source/snapshot, không tái sinh tuỳ tiện báo cáo để che mismatch.

[DAY8.md](../src/recommendation/DAY8.md) có API example: SearchConstraints + AdvancedRecommender, đơn vị EUR/million tường minh, hard/soft foot và missing policy. API example default fit catalogue không giống holdout-reference của runner; dùng runner để tái lập số liệu. Không có app web để chạy. Source Day 5–8/docs chưa commit ở HEAD c4d638c; data ngoài Git, fresh-install/máy đích vẫn chưa nghiệm thu. Day 9 chưa triển khai; commit để khi chuyển máy trong nhiệm vụ được phép.

## Cập nhật chạy Day 7 — 2026-11-02

Source hiện hành cần thêm src/recommendation/knn.py, run_day7.py, DAY7.md và tests/test_knn_recommendation.py; suite hiện có **178 tests (109 cũ + 69 mới)**, đã đạt 178 passed in 20.19s, 0 failed trên máy Windows hiện có. Các số 109/57 trong snapshot bên dưới thuộc các lần trước.

Runner Day 7 cần features CSV + reports/day5_recommendation_examples.json + reports/day6/evaluation.json; giữ đúng source/dataset hashes và snapshot. Đọc [DAY7.md](../src/recommendation/DAY7.md) trước khi chạy. Không cài dependency mới; threadpoolctl dùng để giới hạn luồng đã có qua scikit-learn. Nếu môi trường mới thiếu dependency, cài lại theo requirements/constraints rồi kiểm tests, không bỏ giới hạn luồng để báo benchmark tương đương.

Chạy suite bằng `.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`. Chạy benchmark vào output-dir mới: `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day7 --output-dir reports/day7_rerun --warmup 5 --repeats 50`. Runner từ chối output cũ, không có --overwrite. Không chạy tests/project jobs đồng thời với block benchmark; không diễn giải p95 máy local thành cloud SLA. Linux/macOS thay executable bằng .venv/bin/python.

HEAD c4d638c chưa chứa source Day 5–7/docs mới. Các điều kiện nhận source, data ngoài Git, UTF-16 requirements và fresh-install ở các mục sau vẫn áp dụng. Chưa nghiệm thu chuyển máy; Day 8 chưa triển khai.

## Cập nhật chạy Day 6 — 2026-11-02

Day 6 đã triển khai sau phiên bàn giao; cần nhận thêm weighted.py, evaluation.py, run_day6.py, DAY6.md, tests/test_weighted_recommendation.py và reports/day6/. Source Day 5–6 vẫn chưa commit tại HEAD c4d638c. Data manifest/dependencies không đổi. Lượt test hiện hành: **109 passed in 13.12s, 0 failed** (57 Day 4–5 + 52 Day 6).

Lệnh test bên dưới chạy cả 109 tests khi đã nhận đủ source. Runner Day 6: `.\.venv\Scripts\python.exe -B -m src.recommendation.run_day6`; vì reports/day6 đã tồn tại, dùng `--output-dir reports/day6_rerun` để giữ kết quả cũ. Chỉ dùng `--overwrite` khi chủ động thay artefact. Chi tiết tham số/metric trong [DAY6.md](../src/recommendation/DAY6.md). Không cần credentials hay dependency mới.

Phần cài đặt bên dưới giữ bằng chứng môi trường của phiên bàn giao Day 5 (57 tests lúc đó). Chưa fresh-install trên máy đích; trạng thái Day 6 không thay bằng chứng cài sạch còn thiếu.

Cập nhật 2026-11-02. Đã kiểm tra trên venv Windows hiện có: Python 3.13.7, 57 tests pass, pip check không có dependency hỏng. **Chưa cài lại từ đầu hoặc chạy trên Linux/macOS trong phiên này.** Các lệnh dưới là runbook cho máy đích, không phải tuyên bố đã chạy.

## 1. Nhận source đúng phiên bản

Cần Git và Python 3.13 làm điểm bắt đầu tương ứng máy cũ; quyền truy cập repository nếu GitHub yêu cầu. Không đưa token vào URL/lệnh/tài liệu. Việc cài Claude Code và đăng nhập tài khoản trên máy mới thực hiện riêng; repository không cần credentials Claude/OpenAI để chạy baseline.

```text
git clone https://github.com/tranhaidong23/ScoutIQ-AI.git
cd ScoutIQ-AI
git status --short --branch
git log -5 --oneline
git remote -v
```

Tên thư mục mặc định là ScoutIQ-AI; luôn chạy từ repo root, không phụ thuộc đường dẫn Windows cũ.

**Điểm chặn hiện tại:** HEAD c4d638c chưa chứa Day 5–6/tài liệu bàn giao. Trước khi clone để tiếp tục, người dùng phải cho phép chuyển source đã rà soát qua commit/push hoặc phương án bàn giao riêng. Kiểm tra thực có CLAUDE.md, docs/HANDOFF.md; src/recommendation/baseline.py, run_day5.py, weighted.py, evaluation.py, run_day6.py, DAY6.md; tests/test_recommendation.py và tests/test_weighted_recommendation.py. Thiếu thì nhận đủ source trước khi chạy; không tạo file giả để vượt test. Đối chiếu hash commit bàn giao thực tế sau khi được phép, không mặc định main luôn ở đúng trạng thái.

**Đầu vào đối chứng bắt buộc:** reports/day5_recommendation_examples.json phải được bàn giao cùng source. Runner Day 6 đọc hash dataset, Top 5, bộ lọc và fit audit từ file này; chỉ có features CSV là chưa đủ chạy thí nghiệm. Giữ artefact Day 5 gốc, không tự ghi đè bằng một snapshot khác để vượt kiểm tra. Source hashes hiện ghi trong reports/day6/evaluation.json giúp đối chiếu code với lần chạy đã lưu.

Thư mục backend/frontend/database/notebooks/slides hiện rỗng nên không xuất hiện khi clone là bình thường. Chúng chưa chứa ứng dụng.

## 2. Venv mới và dependencies

Không copy .venv từ máy cũ. requirements.txt hiện **UTF-16 LE có BOM**, không pin phiên bản. Chuyển một bản tạm sang UTF-8 bên trong .venv (đang gitignore), giữ nguyên file gốc. [environment-observed.json](environment-observed.json) lưu phiên bản 11 dependency trực tiếp và pip đã quan sát; dùng làm constraints nếu muốn gần môi trường cũ hơn. Đây không phải lock toàn bộ dependency bắc cầu hay bảo đảm package có trên index/máy đích.

Windows PowerShell, từ repo root:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -c "from pathlib import Path; b=Path('requirements.txt').read_bytes(); s=b.decode('utf-16') if b[:2] in (b'\xff\xfe',b'\xfe\xff') else b.decode('utf-8-sig'); Path('.venv/requirements-utf8.txt').write_text(s,encoding='utf-8')"
.\.venv\Scripts\python.exe -c "import json; from pathlib import Path; p=json.loads(Path('docs/environment-observed.json').read_text(encoding='utf-8'))['packages']; Path('.venv/constraints-observed.txt').write_text('\n'.join(k+'=='+v for k,v in p.items() if k!='pip')+'\n',encoding='utf-8')"
.\.venv\Scripts\python.exe -m pip install -r .venv/requirements-utf8.txt -c .venv/constraints-observed.txt
.\.venv\Scripts\python.exe -m pip check
```

Nếu không có launcher py, dùng executable Python 3.13 đã cài để tạo venv. Không cần activation, tránh phụ thuộc execution policy PowerShell.

Linux/macOS (shell POSIX, Python 3.13 đã được cài):

```bash
python3.13 -m venv .venv
.venv/bin/python -c "from pathlib import Path; b=Path('requirements.txt').read_bytes(); s=b.decode('utf-16') if b[:2] in (b'\xff\xfe',b'\xfe\xff') else b.decode('utf-8-sig'); Path('.venv/requirements-utf8.txt').write_text(s,encoding='utf-8')"
.venv/bin/python -c "import json; from pathlib import Path; p=json.loads(Path('docs/environment-observed.json').read_text(encoding='utf-8'))['packages']; Path('.venv/constraints-observed.txt').write_text('\n'.join(k+'=='+v for k,v in p.items() if k!='pip')+'\n',encoding='utf-8')"
.venv/bin/python -m pip install -r .venv/requirements-utf8.txt -c .venv/constraints-observed.txt
.venv/bin/python -m pip check
```

Nếu constraints không cài được, ghi rõ phiên bản thiếu/lỗi và môi trường; không mặc định dữ liệu/code sai. Có thể thử môi trường riêng với requirements UTF-8 không constraints khi được giao xử lý cài đặt, rồi chạy đầy đủ tests và ghi phiên bản mới; không gọi kết quả đó là môi trường giống hệt máy cũ. Chưa có lockfile/hashes package hoặc CI cross-platform đã nghiệm thu. pip check chỉ kiểm tính tương thích dependency đã cài, không thay cho fresh-install test.

Dependencies hiện có phục vụ pandas/numpy, biểu đồ, sklearn, requests, notebook, dotenv, pytest và BeautifulSoup. Chưa khai báo bộ dependencies FastAPI/Streamlit/PostgreSQL/OpenAI cho ứng dụng; không cài và giả định app tồn tại.

## 3. Nhận snapshot dữ liệu ngoài Git

.gitignore bỏ qua data/raw/, data/processed/, data/external/, .venv và .env/.env.*. Clone không lấy các dataset. **Ưu tiên chuyển đúng snapshot**:

- 5 file data/raw/: players.csv.gz, clubs.csv.gz, games.csv.gz, appearances.csv.gz, player_valuations.csv.gz.
- 3 file data/processed/: scoutiq_players_2025_26.csv, scoutiq_candidates_2025_26.csv, scoutiq_features_2025_26.csv.
- Giữ đúng đường dẫn tương đối; dung lượng raw gzip khoảng 61,9 MB theo byte thập phân, cộng processed khoảng 4,6 MB. Không cần chuyển venv/caches.
- Đề xuất archive riêng trên ổ đĩa hoặc kho riêng có quyền truy cập phù hợp; giữ bản raw nguyên vẹn, copy vào máy mới, kiểm hash. Chưa tạo archive, chọn dịch vụ, upload hay kiểm chứng quyền phân phối trong nhiệm vụ này. Không force-add dữ liệu vào Git.

Kiểm đủ 8 file và SHA-256 từ repo root sau khi chép (stdlib, không ghi dữ liệu):

```powershell
.\.venv\Scripts\python.exe -B -c "import json,hashlib; from pathlib import Path; m=json.loads(Path('docs/DATA_MANIFEST.json').read_text(encoding='utf-8')); bad=[x['path'] for x in m['files'] if not Path(x['path']).is_file() or Path(x['path']).stat().st_size!=x['bytes'] or hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()!=x['sha256']]; print('MISMATCH/MISSING:',bad); raise SystemExit(bool(bad))"
```

Linux/macOS dùng .venv/bin/python thay executable Windows. Kỳ vọng MISMATCH/MISSING: [] và exit 0. Hash lệch thì kiểm quá trình chuyển/nguồn; **không cập nhật manifest chỉ để cho check pass**. Check này đọc bytes nên phát hiện cả khác encoding/newline, không chỉ khác giá trị bảng. Manifest là snapshot 2026-11-02, không chứa file tải tự động.

Tối thiểu về dataset để chạy 109 tests hiện hành là candidates và features đúng snapshot; để chạy raw pipeline cần đủ 5 raw. File players phục vụ kiểm tra/tái tạo candidates. Bàn giao đủ 8 để vừa chạy nhanh vừa có khả năng truy nguồn; runner Day 6 còn cần JSON Day 5 như mục 1.

## 4. Tái tạo đầu ra từ raw khi cần

Chỉ chạy trên clone làm việc mới đã có bản raw bảo toàn và bản sao artefact cần giữ. Các script dưới **ghi đè processed/report/figure theo đường dẫn cố định**, không có chế độ dry-run chung. Không chạy trên bản duy nhất chỉ để kiểm tra tài liệu.

Windows; Linux/macOS thay .\.venv\Scripts\python.exe bằng .venv/bin/python:

```powershell
.\.venv\Scripts\python.exe -B src/preprocessing/clean_data.py
.\.venv\Scripts\python.exe -B src/preprocessing/create_candidates.py
.\.venv\Scripts\python.exe -B src/features/build_features.py
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
```

Kỳ vọng theo artefact hiện có: players 8.322×20 → candidates 4.112×21 → features 4.112×28. Chạy check hash sau tái tạo; nếu bytes khác do phiên bản thư viện/serialization, so schema, values, cutoff và per90, ghi sai khác trước khi chấp nhận snapshot mới. Không khẳng định bit-for-bit tái tạo đã được thử trong phiên bàn giao.

Tái tạo báo cáo quan sát/EDA tùy nhu cầu, cũng ghi đè outputs:

```powershell
.\.venv\Scripts\python.exe -B src/collection/inspect_data.py
.\.venv\Scripts\python.exe -B src/eda/eda_analysis.py
.\.venv\Scripts\python.exe -B src/eda/age_group_analysis.py
```

check_season.py, 01_explore_data.py, 02_check_columns.py và validate_data.py chủ yếu in kết quả đọc dữ liệu; dòng “VALIDATION COMPLETED” không là bằng chứng test assertions pass. Không import các script top-level này như thư viện.

Nếu mất raw snapshot: downloader trong src/collection/download_data.py dùng URL mutable https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/{table}.csv.gz. Chưa kiểm truy cập mạng/phiên bản nguồn hôm nay. Chỉ dùng phương án tải lại ở clone riêng có data/raw trống:

```powershell
.\.venv\Scripts\python.exe -B src/collection/download_data.py
```

Script skip file sẵn có khác rỗng, không xác nhận checksum; lỗi từng bảng được in ra và thông báo kết thúc không đảm bảo đủ file. Kiểm đủ bảng/hash sau tải. Nguồn có thể đã đổi; cutoff không làm metadata tự quay lại lịch sử. Thiếu snapshot chính xác là hạn chế tái lập cần báo cáo, không tự thay dữ liệu và gọi đó là cùng kết quả.

## 5. Tests và chạy baseline hiện có

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pip check
```

Kỳ vọng khi có đầy đủ source Day 4–6: **109 tests** (23 features, 34 baseline recommendation, 52 weighted/evaluation). Lần rà soát trước Day 7 ngày 2026-11-02: 109 passed in 14.60s, 0 failed; pip check đạt. Con số 57 trong phần ghi nhận môi trường đầu tài liệu là kết quả lịch sử trước Day 6. Tests cần dữ liệu thật ngoài Git, có giả định shape/ID của snapshot. Mutation để kiểm lỗi nằm trong bộ nhớ/temp, không tạo dataset cầu thủ sản xuất giả. Tests chưa chứng minh scouting accuracy, chưa thay kiểm thử raw pipeline, API/auth/privacy/cloud.

Smoke query chỉ đọc, không ghi báo cáo:

```powershell
.\.venv\Scripts\python.exe -B -c "from src.recommendation.baseline import CosineRecommender,SearchFilters; e=CosineRecommender.from_csv(); r=e.recommend(reference_player_id=132098,filters=SearchFilters('Attack',min_age=18,max_age=29,max_budget_eur=30000000,min_minutes=1800),top_k=5); print(r)"
```

Smoke dùng default fit toàn catalogue (truy xuất mô tả); không phải cấu hình fit holdout của runner. Xem [README](../src/recommendation/README.md) để gọi thư viện và diễn giải score.

Để chạy lại 5 kịch bản và **ghi đè** reports/day5_recommendation_examples.json cùng .md:

```powershell
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day5
```

Runner fit 4.108 reference, loại 4 query; trên snapshot hiện có, 4 kịch bản trả top 5 và ngân sách 0 trả rỗng. Kiểm filter, ID và số liệu; không dùng đầu ra màn hình thay tests. Khi chạy lại cần giữ artefact cũ nếu muốn so trước/sau.

**Chưa có ứng dụng web để chạy.** Không có lệnh uvicorn, Streamlit, migration PostgreSQL hay OpenAI chat cho trạng thái Day 5. Các module này sẽ được xây ở những ngày sau.

## 6. Secrets, .env và nghiệm thu chuyển máy

Baseline không đọc biến môi trường ứng dụng và không cần API key/password/DB URL. Vì chưa có hợp đồng cấu hình, **không tạo .env.example rỗng hoặc bịa tên biến**. python-dotenv có trong requirements không có nghĩa ứng dụng đã dùng .env. .gitignore hiện bỏ cả .env.example qua .env.*; khi triển khai cấu hình thật, tạo template chỉ placeholder và thêm exception !.env.example có chủ đích, kiểm diff/secrets trước commit. Không chuyển .env thật hoặc cấu hình tài khoản giữa máy bằng Git.

Hoàn tất chuyển máy chỉ khi có source đúng phiên bản, data hash đúng hoặc sai khác đã giải thích, venv mới cài được, tests/smoke query thực chạy và nhật ký ghi OS/Python/dependencies/HEAD/kết quả. Nếu thiếu một điều kiện, ghi **Chưa xác minh/Bị chặn** tại [HANDOFF](HANDOFF.md). Không tự đánh dấu một Day mới hoàn thành chỉ vì môi trường chạy được.

### Điều kiện tiếp tục trên máy mới — rà soát trước Day 7

- Về hướng dẫn: CLAUDE/SETUP/HANDOFF đã có thứ tự đọc, yêu cầu sản phẩm, lệnh, snapshot và next steps, không cần lịch sử chat.
- Về bàn giao thực tế: **chưa nghiệm thu**. Cần nhận source Day 5–6/tài liệu/JSON đối chứng chưa commit, 8 dataset ngoài Git và tạo venv mới. Không chép .venv hoặc secrets máy cũ.
- Kiểm SHA-256 trên máy đích, cài dependencies, chạy 109 tests và pip check; chạy Day 6 vào một output-dir mới và đối chiếu kết quả nếu cần nghiệm thu thí nghiệm. Không dùng --overwrite mặc định, không sửa báo cáo cũ.
- Requirements UTF-16/unpinned đã có cách xử lý và constraints quan sát, nhưng chưa có full dependency lock, chưa chứng minh fresh-install hoặc tương thích hệ điều hành máy đích. Tải lại nguồn mutable không bảo đảm snapshot; bảo toàn raw hiện có là phương án tái lập ưu tiên.

### Chạy Day13

Từ repo root: `.venv\Scripts\python.exe -B -m src.evaluation.run_day13 --output-dir reports/day13_recheck` (output phải mới).
Nhập thật: xem [workflow](../reports/day13/pilot_review_workflow.md), cần cả --annotations và --registry, lưu output riêng ngoài repo.
Tests: `.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider --basetemp=<thu-muc-tam-moi>`.
Không dùng lại thư mục chứa dữ liệu làm basetemp vì pytest có thể xóa nó. Chọn đường dẫn mới. Requirements/môi trường giữ nguyên; chưa fresh-install.
