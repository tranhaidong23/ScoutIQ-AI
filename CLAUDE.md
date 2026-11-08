# ScoutIQ — Điểm bắt đầu cho Claude Code

<!-- CHECKPOINT_20261108_START -->
## Bàn giao hiện hành — 2026-11-08

Nguồn tiếp tục cho Claude Code: [bàn giao tổng hợp Day1–13](docs/CLAUDE_HANDOFF_2026-11-08.md). Mục này ưu tiên về trạng thái Git/bàn giao; các mục bên dưới là lịch sử được giữ nguyên. Người dùng đã yêu cầu commit/push checkpoint Day5–13 hôm nay; quyền này không áp dụng tự động cho Day14/deploy.

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

## Điểm tiếp tục hiện hành — Day 12

**Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

Đọc scope mới AGENTS → [HANDOFF](docs/HANDOFF.md) → [Day12 summary](reports/day12/summary.md), [age findings](reports/day12/age_integrity_findings.md), [provenance](reports/day12/provenance_audit.md), [temporal review](reports/day12/temporal_leakage_review.md), [pilot guide](reports/day12/pilot_annotation_guide.md), [readiness](reports/day12/evaluation_readiness.md), rồi code/tests mới. Giữ protocol/rubric và engine Day11, không làm lại dữ liệu để chỉ kiểm docs.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day12 --output-dir reports/day12_recheck
```

POSIX dùng `.venv/bin/python`; output phải là thư mục mới. Runner từ chối overwrite annotation và không tạo dataset sửa.

Nhãn thật sau này dùng bản sao template + registry có review; Python API `load_pilot_annotations` → `validate_pilot_annotations` → `agreement_report`/`readiness_report` theo scenario/version. Không chấm tự động; registry hiện rỗng. Raw/processed vẫn bị ignore, clone HEAD c4d638c chưa có toàn source Day5–12; chuyển snapshot riêng và kiểm fresh-install, chưa nghiệm thu máy mới.

**Day 13 dự kiến:** xác nhận assessor thật và chạy pilot độc lập khi có; review provenance/uncertainty/abstention/disagreement, tách pilot khỏi final evaluation. Nếu chưa có labels, giữ metric thật bị chặn. Review DOB/chính sách calendar và quyền áp dụng correction; chỉ tạo snapshot có version/tác động kiểm chứng trong nhiệm vụ được phép. Chưa có as-of metadata/valid temporal split, không gọi random split hoặc query-ID holdout là temporal evaluation.

### Các lần bàn giao trước (lịch sử)

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Đọc trước tiên — bàn giao Day 11 (2026-11-03)

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

**Day cuối: Day 11 — hoàn thành protocol, công cụ đánh giá và audit local; chưa có relevance labels độc lập. Day 12 chưa triển khai.** Không coi hoàn thành protocol là đã xác nhận chất lượng tuyển trạch. Engine/scaler/weights/eligibility Day 5–10 giữ nguyên. Bốn demo có 22/10/94/47 ứng viên, 173 hàng unlabeled; 16/16 full responses khớp Day 10 và repeat/filter đúng. P@K/Recall@K/NDCG@K thực đều null. SYNTHETIC chỉ kiểm công thức. Kết quả test cuối phiên xem reports/day11/validation.json.

Đọc AGENTS → HANDOFF → PROJECT_CONTEXT/ARCHITECTURE/FILE_INVENTORY/SETUP → log/insights/PRESENTATION → [Day 11 protocol](reports/day11/evaluation_protocol.md), [rubric](reports/day11/relevance_rubric.md), [audit](reports/day11/audit_findings.md) → src/evaluation và tests/test_evaluation_protocol.py; đối chiếu service/phase review Day 10. Giữ thứ tự đọc cũ cho bằng chứng lịch sử, dùng scope mới này cho quyết định tiếp theo.

Chạy `.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider`; audit/repro bằng `.venv\Scripts\python.exe -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck` (thư mục mới). POSIX dùng `.venv/bin/python`. Runner không nhận/gán human labels; khi đánh giá annotation thật dùng `load_annotations` → chọn scenario/assessor/source → `assess_ranking` với universe đã đóng băng, không thay template gốc. Tham khảo protocol để biết gate/mẫu số.

Next Day 12: review/pilot rubric với người thật nếu có, provenance/abstention/coverage và kế hoạch split, xử lý tuổi boundary có kiểm soát; không tự tạo nhãn chuyên gia, đổi weights hoặc làm backend trước nhiệm vụ. Fresh-machine chưa nghiệm thu; source Day 5–11/docs chưa commit, raw/processed bị ignore cần snapshot riêng theo DATA_MANIFEST. HEAD c4d638c trên main, origin cache không phải xác minh GitHub mới. Không stage/commit/push/deploy trong nhiệm vụ này.

Sau mỗi Day bắt buộc cập nhật bốn báo cáo/handoff như checklist lịch sử bên dưới, thêm label coverage/provenance nếu evaluation. Không suy “tests pass” thành quality hoặc “scope mới” thành API/Neon/Gemini đã tồn tại.

### Nội dung bàn giao lịch sử trước Day 11

<!-- DAY11_CURRENT_END -->

Tài liệu bàn giao cập nhật **2026-11-02**. Giao tiếp bằng tiếng Việt. Không cần lịch sử chat Codex để tiếp tục: trạng thái và bằng chứng nằm trong repository.

## Thứ tự đọc bắt buộc trước khi sửa

1. [AGENTS.md](AGENTS.md): yêu cầu sản phẩm, Data Science, bảo mật và quyền thao tác.
2. [docs/HANDOFF.md](docs/HANDOFF.md): Day gần nhất, Git, việc chưa bàn giao và nhiệm vụ tiếp theo.
3. [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md): mục tiêu, tổng hợp từng Day và roadmap 31 ngày.
4. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/SETUP.md](docs/SETUP.md), [docs/FILE_INVENTORY.md](docs/FILE_INVENTORY.md).
5. Các mục gần nhất của [project_log](reports/project_log.md), [insights_and_defense](reports/insights_and_defense.md) và [PRESENTATION_AND_DEFENSE](reports/PRESENTATION_AND_DEFENSE.md); khi cần, đọc phần lịch sử tương ứng. Hồ sơ thuyết trình tổng hợp Day 1–10, công thức, bằng chứng và phản biện; phân biệt đối chiếu artefact, lịch sử chạy, giả thuyết và kế hoạch.
6. Code và tests liên quan; với recommendation đọc [README Day 5](src/recommendation/README.md), [DAY6.md](src/recommendation/DAY6.md), [DAY7.md](src/recommendation/DAY7.md), [DAY8.md](src/recommendation/DAY8.md), [DAY9.md](src/recommendation/DAY9.md), [DAY10.md](src/recommendation/DAY10.md) và [phase review](reports/day10/phase_review.md).

Các trạng thái cũ được giữ làm lịch sử. Mục cập nhật có ngày mới hơn chỉ thay thế trạng thái được nêu rõ; không xóa yêu cầu sản phẩm. Nếu code/Git khác nhật ký, kiểm tra và ghi đính chính có bằng chứng. Không tự chọn một nguồn thuận tiện rồi báo hoàn thành.

## Khởi động phiên làm việc

- Đọc Git status, branch, log và diff trước khi sửa; giữ nguyên thay đổi của người dùng và Git index.
- Kiểm tra đã nhận đủ **source/tests Day 5–7, tài liệu, reports/day5_recommendation_examples.json, reports/day6/evaluation.json và dữ liệu ngoài Git**. Runner Day 7 dùng hai JSON cũ và source hashes để đối chứng baseline; không bỏ file hoặc tự tạo lại khi chưa xác minh snapshot. HEAD hiện ghi trong HANDOFF chưa chứa Day 5–7; clone riêng commit đó không đủ.
- Dựng venv mới trên máy đích theo SETUP; không chép venv Windows sang máy khác.
- So SHA-256 theo DATA_MANIFEST; chạy tests rồi ghi kết quả thực, Python/OS/dependencies. Nếu thiếu dữ liệu, báo thiếu, không tạo dữ liệu cầu thủ giả.
- Day cuối hiện là **Day 10** (2026-11-02): Recommendation Engine Integration & Phase Review, **549 tests đạt, 0 failed**; 20 responses/explanations/comparisons khớp nguyên Day 8–9, 400 measured calls JSON deterministic. Day 11 chưa triển khai. Đọc HANDOFF/DAY10/phase review để tiếp tục; direct cosine mặc định, weighted giả thuyết/KNN đối chứng, chưa nghiệm thu scouting quality hoặc production.
- Nhận thêm source/tests Day 8 và reports/day7/evaluation.json (đầu vào runner Day 8), ngoài các đầu vào Day 5–7 nói trên. Hard constraints phải qua AdvancedRecommender/SearchConstraints; không truyền thẳng vào engine cũ. Soft foot chỉ phá hòa, budget phải có đơn vị rõ, missing hard fail-closed; không refit preprocessing theo query. Source Day 5–8/docs chưa commit; người dùng yêu cầu để commit khi chuyển máy, không tự commit/push/deploy.
- Nhận thêm source/tests Day 9 và reports/day8/evaluation.json (đầu vào đối chứng runner Day 9); source Day 5–9/docs chưa có trong HEAD c4d638c. Lệnh hiện hành ở HANDOFF/SETUP; runner cần output-dir mới. Evidence tách text, envelope giữ response gốc, comparison 2–5 người gồm reference, null có lý do khi mẫu số 0/missing; không tự đổi score hoặc kết luận tổng thể. JSON chưa phải API contract production; chưa gọi OpenAI/FastAPI. Day 10 chỉ làm khi được giao.
- Day 10 đã được giao và triển khai sau snapshot trên: nhận source/tests/docs Day 5–10 và JSON Day 8/9 đúng hashes để chạy runner mới. requirements khai báo jsonschema>=4.18,<5; 4.26.0 có sẵn trong máy cũ, không phải bằng chứng môi trường sạch. Service có JSON schemas + domain/semantic/native-integer checks, chưa endpoint FastAPI/Pydantic; không tự đổi thuật toán/weights để tối ưu latency. Day 11 là nhiệm vụ tiếp theo khi được giao. Source chưa commit, mốc Day 10 chờ người dùng quyết định khi chuyển máy; không commit/push/deploy tự động.

## Quy tắc thực hiện

Tuân thủ toàn bộ AGENTS.md: bảo vệ raw, không bịa thống kê, không dùng định giá làm kỹ năng, không đánh giá GK bằng bàn thắng. Similarity không phải xác suất chuyển nhượng. Defender/GK hiện chỉ có hồ sơ bối cảnh. Không suy luận nhân quả từ tương quan, không coi tests hành vi là đánh giá chất lượng scouting.

Được sửa file/chạy kiểm thử trong phạm vi nhiệm vụ được giao. Đọc tác dụng ghi file của script trước khi chạy; nhiều script ghi đè báo cáo/processed tại đường dẫn cố định. Không chạy pipeline để chỉ kiểm tra tài liệu. Không đọc/in secrets vào báo cáo; API keys, mật khẩu, connection string thật không vào Git. Không tự cài credentials từ máy cũ.

Không tự stage/commit khi nhiệm vụ cấm. Push, deploy, release cần quyền tương ứng; lịch mốc không cấp quyền. Không force-add dữ liệu bị ignore, force push, reset --hard hoặc viết lại lịch sử.

## Kết thúc mỗi Day

1. Chạy tests phù hợp và suite hồi quy hiện có khi môi trường đủ; ghi lệnh, exit code, số test và lỗi còn lại. Nếu không chạy được, ghi **Bị chặn/Chưa xác minh**, không ghi pass.
2. Bổ sung project_log: mục tiêu, code/artefact, input/output, thuật toán, môi trường, tests, Git, phần còn lại.
3. Bổ sung insights_and_defense: quyết định, bằng chứng, giới hạn, câu hỏi phản biện; ghi rõ nếu không có insight mới.
4. Cập nhật HANDOFF ngay: Day cuối có bằng chứng, HEAD/branch/status, việc chưa commit, next steps, blockers và lệnh chạy. Đổi trạng thái hiện hành của AGENTS/PROJECT_CONTEXT khi cần; giữ dấu vết lịch sử trong nhật ký.
5. Cập nhật FILE_INVENTORY nếu thêm/đổi file, input/output hoặc dependency; cập nhật SETUP/ARCHITECTURE khi cách chạy/thiết kế thay đổi. Chỉ thay manifest dữ liệu khi có thay đổi snapshot được giải thích.
6. Cập nhật bắt buộc [PRESENTATION_AND_DEFENSE](reports/PRESENTATION_AND_DEFENSE.md) cùng project_log, insights_and_defense và HANDOFF sau mỗi Day: mục tiêu, công việc, file/chức năng/input-output, thuật toán/công thức/lý do, kết quả có nguồn, khó khăn/cách giải quyết, hạn chế và **3–5 câu hỏi phản biện kèm trả lời**. Dẫn link tương đối tới code/tests/CSV/JSON/biểu đồ; ghi dataset/cutoff, config/query/môi trường và test/commit thực có. Không biến đọc lại báo cáo thành chạy mới, giả thuyết thành kết luận hoặc rủi ro thành sự cố đã xảy ra. Đối chiếu bốn tài liệu, ghi đính chính và giữ lịch sử; thiếu bằng chứng ghi Chưa xác minh/Bị chặn.
7. Báo cáo bằng tiếng Việt. Đề xuất mốc commit/push **Day 5, 10, 15, 20, 25, 30, 31**; Day 31 là final release có nghiệm thu, không tự thực hiện.

Khi được phép commit sau này, ghi hash thực sau commit vào bàn giao ở lần cập nhật kế tiếp; không cố ghi hash của chính commit chưa tồn tại. Khi chuẩn bị chuyển máy, kiểm tra từ clone sạch và dữ liệu đã bàn giao, thay vì suy luận từ working tree máy cũ.
