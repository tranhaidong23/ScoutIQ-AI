# ScoutIQ – Hướng dẫn dự án và làm việc trong repository

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

## Tiến độ và quy tắc hiện hành — Day 12 (2026-11-03)

**Day 12 hoàn thành phần audit, thiết kế correction có phiên bản, chuẩn bị pilot và công cụ readiness. Chưa có người thật chấm; correction vẫn PROPOSED, chưa áp dụng. Day 13 chưa triển khai.** Mục mới này cập nhật trạng thái Day cuối của các phần lịch sử bên dưới; giữ nguyên toàn bộ bằng chứng Day 1–11.

Kiểm tra mới 2026-11-03: 4.112 ứng viên × 28 cột; 4.111 tuổi nhất quán, 1 lỗi xấp xỉ ID 341429 (snapshot 29, calendar 30, DOB 1996-06-12 tại cutoff 2026-06-12). 4.112 DOB ứng viên hợp lệ; raw 50.149 có 49 DOB thiếu. Pilot seed 12 chọn 32 hồ sơ (8/scenario), tất cả pending/unlabeled, registry assessor rỗng. Relevance và agreement thật chưa tính; không lấy synthetic làm chất lượng. Kết quả tests cuối và bảo toàn file nằm trong reports/day12/validation.json.

MVP tiếp tục không login/signup; FastAPI, Streamlit, Neon và Gemini còn ở phase sau. Python engine giữ ranking; Gemini chỉ hiểu yêu cầu/giải thích evidence. Authentication/đồng bộ đa thiết bị là Future Development. Không đổi ranking/scaler/weights/eligibility/API, không commit/push/deploy.

- Đọc [summary](reports/day12/summary.md), [age findings](reports/day12/age_integrity_findings.md), [pilot guide](reports/day12/pilot_annotation_guide.md), [readiness](reports/day12/evaluation_readiness.md) trước evaluation tiếp theo.
- Correction chỉ là [proposal](reports/day12/correction_proposal.json); không tự apply/promote hoặc ghi đè canonical/raw. Cần review nguồn DOB, chính sách 29/2, quyền thực hiện, snapshot/hash/version riêng và kiểm tác động filters/scaler/ranking.
- Annotation pilot phải gắn dataset/rubric/scope/version; grade trống không phải0, không giả assessor. Registry/provenance cần review con người, code không chứng minh độc lập. Không mix synthetic/human hoặc context GK với attacking relevance.
- Chỉ tính agreement trên nhãn độc lập tương thích đủ common items; báo paired coverage/abstention và undefined kappa. Quy tắc metrics Day11 vẫn giữ; không suy quality từ coverage/stability/tests.
- Sau mỗi Day tiếp tục cập nhật log, insights, PRESENTATION, HANDOFF, inventory và setup/architecture khi cần; ghi kết quả thực và phần bị chặn.

**Day 13 dự kiến:** xác nhận assessor thật và chạy pilot độc lập khi có; review provenance/uncertainty/abstention/disagreement, tách pilot khỏi final evaluation. Nếu chưa có labels, giữ metric thật bị chặn. Review DOB/chính sách calendar và quyền áp dụng correction; chỉ tạo snapshot có version/tác động kiểm chứng trong nhiệm vụ được phép. Chưa có as-of metadata/valid temporal split, không gọi random split hoặc query-ID holdout là temporal evaluation.

### Các chỉ đạo và trạng thái trước Day 12 (lịch sử)

<!-- DAY12_CURRENT_END -->

<!-- DAY11_CURRENT_START -->
**Kiểm thử Day 11: 619 passed, 0 failed (549 cũ + 70 mới), 139,00s; exit code 0.**

## Nguồn chỉ đạo hiện hành — Day 11 / MVP mới (2026-11-03)

**Phạm vi hiện hành do người dùng đổi ngày 2026-11-03:** MVP không login/signup. Người dùng tìm/lọc/xếp hạng/giải thích/so sánh cầu thủ và có lịch sử tìm kiếm ẩn danh theo trình duyệt. Stack đích: Streamlit, FastAPI, Neon PostgreSQL dùng chung, Gemini API qua Google AI Studio và Python Recommendation Engine. Authentication và đồng bộ đa thiết bị thuộc **Future Development**. Gemini chỉ hiểu yêu cầu/giải thích evidence, không tự ranking hoặc tạo ground truth.

Mục này **thay thế yêu cầu authentication/OpenAI và phân công roadmap cũ**, không xóa lịch sử Day 1–10. Các yêu cầu không xung đột (dữ liệu thật, cutoff, top 3–5, so sánh/đơn vị, privacy, bảo vệ secrets, kiểm thử, deployment cần phép) vẫn áp dụng. Các đoạn phía dưới ghi scope/Day cuối cũ là snapshot lịch sử, không phải chỉ thị triển khai auth/OpenAI cho MVP mới.

**Day cuối: Day 11 — hoàn thành protocol, công cụ đánh giá và audit local; chưa có relevance labels độc lập. Day 12 chưa triển khai.** Không coi hoàn thành protocol là đã xác nhận chất lượng tuyển trạch. Engine/scaler/weights/eligibility Day 5–10 giữ nguyên. Bốn demo có 22/10/94/47 ứng viên, 173 hàng unlabeled; 16/16 full responses khớp Day 10 và repeat/filter đúng. P@K/Recall@K/NDCG@K thực đều null. SYNTHETIC chỉ kiểm công thức. Kết quả test cuối phiên xem reports/day11/validation.json.

### Quy tắc bổ sung bắt buộc

- Roadmap hiện hành: Day 11–13 evaluation; 14–17 FastAPI+Neon; 18–23 Streamlit+Gemini; 24–27 integration/cloud; 28–31 report/slides/demo. Chi tiết trong docs/PROJECT_CONTEXT.md và project_log. Lịch sử Day 1–10 giữ nguyên.
- Anonymous không có nghĩa lịch sử công khai: backend tương lai phải giới hạn theo browser session/token; Neon dùng chung hạ tầng nhưng tách dữ liệu logic từng session. Token khó đoán, không tin session ID do client tùy ý chỉ định, cần kiểm quyền đọc/ghi/xóa. Thiết kế token/retention còn chờ Day 14–17; không tuyên bố privacy đã triển khai. Mất token/xóa dữ liệu trình duyệt có thể mất truy cập; chưa đồng bộ đa thiết bị.
- Không có `users`/password/login bắt buộc trong MVP. Nếu lưu chat, chat_sessions/chat_messages thuộc anonymous session; không chứa API keys trong client/logs/Git. Gemini và Neon credentials phía server; chưa tích hợp/cấu hình dịch vụ trong Day 11.
- Nhãn relevance cần nguồn và assessor độc lập; không lấy score/rank/Gemini làm nhãn. Grade 0–3; missing không phải 0; Defender/GK chỉ context-profile relevance. SYNTHETIC tách khỏi số liệu thực. Theo [protocol](reports/day11/evaluation_protocol.md) và [rubric](reports/day11/relevance_rubric.md).
- Audit phát hiện 1 tuổi xấp xỉ lệch lịch (341429: 29 vs 30 tại cutoff). Không sửa âm thầm hoặc đổi snapshot/ranking để làm metric đẹp; cần thay đổi có version và regression khi được giao. Metadata CLB/role tại cutoff vẫn chưa xác minh.
- Sau mỗi Day tiếp tục cập nhật project_log, insights_and_defense, PRESENTATION_AND_DEFENSE, HANDOFF và inventory/setup/architecture khi cần; ghi tests thực, provenance, labels thiếu và hạn chế. Day 11 không commit/push/deploy và không triển khai Day 12. Mốc Git không cấp quyền.

### Lịch sử hướng dẫn trước cập nhật Day 11

Các phần bên dưới được giữ nguyên để truy vết; chỉ đạo mới ở trên có ưu tiên khi scope/trạng thái/roadmap xung đột.

<!-- DAY11_CURRENT_END -->

## Nhận diện và mục tiêu

- **Tên:** ScoutIQ – Intelligent Football Scouting & Transfer Recommendation System.
- **Tagline:** Scout Smarter. Sign Better.
- **Mục tiêu:** Xây dựng nền tảng tuyển trạch và đề xuất chuyển nhượng cầu thủ bóng đá bằng Data Science, Recommendation Engine và AI hội thoại.
- **Đối tượng:** Football scouts, sporting directors, recruitment analysts và các CLB bóng đá.
- Tài liệu này áp dụng cho toàn bộ repository. Các yêu cầu bên dưới là phạm vi sản phẩm cần xây dựng, không phải tuyên bố rằng đã triển khai xong.

## Chức năng và kiến trúc bắt buộc

1. Đăng ký, đăng nhập và đăng xuất; bảo vệ mật khẩu bằng cơ chế băm phù hợp, không lưu mật khẩu dạng rõ.
2. Dữ liệu riêng tư theo người dùng. Backend phải kiểm tra quyền sở hữu khi đọc/ghi lịch sử, hội thoại và kết quả; không chỉ ẩn dữ liệu trên giao diện.
3. **PostgreSQL** lưu `users`, `search_history`, `chat_sessions`, `chat_messages` và `recommendation_results`. Dữ liệu nghiệp vụ phải gắn với người dùng; tin nhắn phải thuộc phiên chat có chủ sở hữu. Đây là yêu cầu thiết kế, chưa xác nhận có schema/migration.
4. Tìm kiếm cầu thủ theo vị trí, tuổi, ngân sách và hiệu suất; thể hiện đơn vị, cutoff và điều kiện lọc.
5. Đề xuất **top 3–5 cầu thủ** bằng content-based recommendation, lựa chọn và đánh giá weighted cosine similarity hoặc KNN. Nếu không đủ ứng viên hợp lệ, trả số lượng thực có và giải thích; không bịa hoặc tự nới điều kiện.
6. So sánh cầu thủ bằng biểu đồ, thống nhất đơn vị và bối cảnh vị trí; hiển thị dữ liệu thiếu rõ ràng.
7. Scouting chat dùng **OpenAI API**, trả lời dựa trên dữ liệu thật được truy xuất từ hệ thống; có nguồn/bằng chứng phù hợp, thừa nhận khi thiếu dữ liệu, không bịa thống kê.
8. **FastAPI backend**, **Streamlit frontend**, **PostgreSQL database**. API key và truy cập cơ sở dữ liệu phải được quản lý phía server.
9. Triển khai cloud sau khi được cho phép; cấu hình môi trường, secrets và kiểm tra vận hành phải được ghi nhận.
10. Kiểm thử dữ liệu, recommendation, API, xác thực/phân quyền, cách ly dữ liệu giữa người dùng và các luồng tích hợp chính. Không coi kết quả in ra màn hình là bằng chứng toàn bộ test đã pass.

## Dữ liệu và tiến độ đã biết

- Nguồn: **Transfermarkt**, mùa **2025/26** (`season == 2025` trong nguồn), cutoff **2026-06-12**. Không mô tả snapshot này là dữ liệu trực tiếp hiện tại.
- **Day 1 – Thu thập:** đã thu thập 5 bảng: `players`, `clubs`, `games`, `appearances`, `player_valuations`. Các file gốc `.csv.gz` hiện có trong `data/raw/`.
- **Day 2 – Làm sạch/tích hợp:** bảng tích hợp được báo cáo có 8.322 cầu thủ; sau lọc còn **4.112 ứng viên**, theo báo cáo hiện có. Điều kiện trong `create_candidates.py`: ít nhất 900 phút, vị trí không trống, giá trị thị trường dương, định giá trong 0–365 ngày trước cutoff.
- **Day 3 – EDA:** hoàn thành theo nhật ký hiện có và xác nhận của người dùng; hiện có code, 5 biểu đồ và 2 bảng tổng hợp theo vị trí/nhóm tuổi. Lần thiết lập tài liệu ngày 2026-10-27 chỉ đối chiếu code và artefact, không chạy lại EDA.
- **Day 4 – Feature Engineering:** **chưa xác nhận hoàn thành**. Không tự đánh dấu hoàn tất hoặc triển khai trong nhiệm vụ thiết lập tài liệu này. Việc Day 2 có các cột per90 không chứng minh toàn bộ Day 4 đã xong.
- Backend, frontend, database, recommendation, chat, cloud và kiểm thử sản phẩm là các hạng mục cần theo dõi; chưa xác nhận triển khai. Tại lần đối chiếu 2026-10-27 chưa thấy file trong `backend/`, `frontend/`, `database/`, `tests/`.

## Bản đồ repository

| Đường dẫn | Vai trò |
|---|---|
| `data/raw/` | Dữ liệu gốc; bảo vệ, không ghi đè/xóa khi xử lý |
| `data/processed/` | Dataset tích hợp và tập ứng viên dẫn xuất |
| `src/collection/` | Thu thập và kiểm tra nguồn/mùa dữ liệu |
| `src/preprocessing/` | Khám phá, làm sạch, tích hợp, lọc và kiểm tra dữ liệu |
| `src/eda/` | EDA, biểu đồ, tổng hợp theo vị trí và nhóm tuổi |
| `backend/`, `frontend/`, `database/` | Vị trí dự kiến cho API, giao diện và schema/migration |
| `tests/` | Kiểm thử tự động dự kiến |
| `notebooks/` | Phân tích thử nghiệm |
| `reports/`, `reports/figures/` | Nhật ký, bằng chứng, bảng tổng hợp và biểu đồ |
| `slides/` | Tài liệu trình bày |
| `requirements.txt` | Danh sách dependency hiện có; không mặc định đã đủ cho toàn bộ sản phẩm |

## Nguyên tắc Data Science

- Không tạo dữ liệu giả hoặc bịa số liệu để lấp khoảng trống hay làm đẹp kết quả. Không diễn giải missing values thành 0 khi chưa có cơ sở.
- Tương quan không chứng minh nhân quả. Mọi kết luận phải nêu phạm vi mẫu, phương pháp, đơn vị và giới hạn.
- **Market value là ước tính giá trị thị trường, không phải phí chuyển nhượng.** Lọc ngân sách dùng EUR gốc và phải giải thích giới hạn này.
- Kiểm tra missing values, kiểu dữ liệu, trùng ID, giá trị bất hợp lý và tính toàn vẹn khi join; ghi lại số hàng bị loại và lý do khi thay đổi pipeline.
- Kiểm tra data leakage: ngày trận/định giá không vượt cutoff; xem xét thời điểm của metadata CLB/cầu thủ; khi có tập train/evaluation, chỉ fit scaler/imputer/feature selection trên tập phù hợp, không dùng dữ liệu tương lai để đánh giá quá khứ.
- Tách tính tương đồng chuyên môn khỏi ràng buộc ngân sách/tuổi. Không dùng giá trị thị trường như ground truth mặc định của chất lượng cầu thủ.
- Xem xét độ lệch định giá, độ tin cậy per90 và việc đếm trùng ảnh hưởng giữa số đếm với per90. Log transform, scaling, trọng số và feature set chỉ được coi là cải thiện sau kiểm chứng.
- Chỉ số goals/assists/minutes hiện có không đủ để khẳng định đánh giá toàn diện phòng ngự, thủ môn hoặc tactical fit. Ngưỡng 900 phút và độ mới 365 ngày là lựa chọn ban đầu, cần đánh giá độ nhạy.
- Đánh giá recommendation bằng tình huống scouting, baseline, tuân thủ bộ lọc, độ ổn định top-K và đánh giá chuyên môn có tiêu chí. Chỉ báo cáo metric phù hợp với nhãn/bằng chứng thực có; không tự tạo ground truth.

## Quy tắc làm việc

- Giao tiếp và báo cáo bằng **tiếng Việt**; giữ nguyên tên kỹ thuật khi cần.
- Đọc code, tài liệu, hướng dẫn áp dụng và trạng thái Git trước khi sửa. Được tự tạo/sửa file và chạy test trong workspace theo phạm vi nhiệm vụ đã giao.
- Bảo toàn thay đổi sẵn có của người dùng, kể cả staged changes. Không tự reset, checkout bỏ thay đổi, sửa Git index hoặc ghi đè nội dung lịch sử.
- Bảo vệ dữ liệu gốc; tạo đầu ra dẫn xuất riêng. Trước khi chạy script, kiểm tra tác dụng ghi file; các script cleaning/candidates/EDA hiện có có thể ghi đè đầu ra.
- Không đưa API key, mật khẩu, token, connection string hoặc nội dung riêng tư vào code, log, báo cáo hay Git. Dùng biến môi trường/secrets; ví dụ cấu hình chỉ chứa placeholder.
- Chạy kiểm tra phù hợp với thay đổi. Với tài liệu, kiểm tra diff, tính nhất quán, đường dẫn và bảo toàn nội dung; không chạy pipeline ghi dữ liệu chỉ để xác minh tài liệu.
- Chỉ ghi “đã hoàn thành”, “đã chạy”, “đã pass” khi có bằng chứng. Phân biệt yêu cầu, kế hoạch, kết quả cũ, kiểm tra trực tiếp và phần chưa xác minh.
- Commit theo mốc có ý nghĩa khi nhiệm vụ cho phép, với nội dung rõ ràng; không gộp thay đổi không liên quan. **Không tự push hoặc deploy khi chưa được cho phép.**
- **Giới hạn nhiệm vụ thiết lập tài liệu ngày 2026-10-27:** chỉ tạo/cập nhật tài liệu; chưa triển khai Day 4, chưa commit, chưa push GitHub hoặc deploy.

## Hệ thống tài liệu và bằng chứng

- [`reports/project_log.md`](reports/project_log.md): theo dõi ngày/mốc, mục tiêu, tiến độ, code/artefact, lệnh kiểm tra và kết quả, hạn chế, bước tiếp theo, branch/commit và trạng thái staged/unstaged.
- [`reports/insights_and_defense.md`](reports/insights_and_defense.md): lưu phát hiện, quyết định, bằng chứng, giới hạn, giả thuyết, câu hỏi phản biện và kiểm chứng còn thiếu.
- Khi cập nhật, đọc nội dung cũ trước rồi bổ sung mục mới; nếu cần đính chính, ghi rõ mục bị thay thế, lý do và bằng chứng, không xóa lịch sử âm thầm.
- Trạng thái chuẩn: **Dự kiến / Đang thực hiện / Đã hoàn thành có bằng chứng / Chưa xác minh / Bị chặn**. Ghi ngày kiểm tra và không nhầm ngày kiểm tra với ngày thực hiện công việc cũ.
- Sau mỗi mốc, cập nhật hai báo cáo với kết quả thực có; nếu không phát sinh insight mới, ghi rõ thay vì tạo phát hiện giả.

## Cập nhật sau nhiệm vụ tài liệu — Day 4 (2026-10-27)

- Người dùng đã giao nhiệm vụ triển khai Day 4 trong lượt tiếp theo. Giới hạn “chỉ thiết lập tài liệu” ở trên thuộc nhiệm vụ trước, không ngăn nhiệm vụ Day 4 được cho phép sau đó; vẫn không commit, push hoặc deploy.
- **Day 4 đã hoàn thành trong phạm vi đặc trưng được yêu cầu:** `src/features/build_features.py`; đầu ra 4.112 cầu thủ × 28 cột; 8 đặc trưng được tạo/kiểm tra, gồm 7 cột mới và `goal_contributions_per90` có từ Day 2. Chạy bằng `.venv`, 23 test đạt; chi tiết trong phần Day 4 của hai báo cáo.
- Thông tin này cập nhật trạng thái “chưa xác nhận hoàn thành” trong các phần lịch sử. Chưa triển khai hoặc đánh giá recommendation, chưa xác nhận hoàn thành Day 5.
- `reports/day4_feature_quality.json` lưu schema, missing, infinity, phạm vi, sai số per90, thống kê phân phối và SHA-256. Metadata thiếu vẫn được giữ; chiều cao 19 cm của `player_id=743556` cần xác minh nguồn, chưa sửa hoặc dùng làm feature.
- Percentile dùng `100 * average_rank / số cầu thủ cùng vị trí`, tham chiếu toàn bộ tập ứng viên tại cutoff trước bộ lọc tìm kiếm. Đây là chỉ số tấn công tương đối, không phải điểm chất lượng tổng hợp.
- Định giá và log định giá không phải kỹ năng; minutes reliability là heuristic. Day 5 cần chọn feature, xử lý phụ thuộc giữa biến, kiểm tra leakage, baseline và đánh giá theo vị trí.

## Lộ trình chính thức — 31 ngày làm việc (cập nhật 2026-10-27)

**Trạng thái hiện hành: Day 1–4 đã hoàn thành; Day 5–31 là kế hoạch, chưa triển khai.** Mục này là nguồn tham chiếu hiện hành về tiến độ và lịch làm việc, cập nhật các ghi nhận trạng thái cũ phía trên mà không xóa lịch sử. Các mục tiêu, đối tượng, chức năng bắt buộc, kiến trúc và nguyên tắc Data Science/bảo mật của ScoutIQ được giữ nguyên.

“Day” là số thứ tự ngày làm việc của dự án, không phải ngày lịch hay cam kết hoàn thành vào một ngày cụ thể. Không tự gán ngày bắt đầu, lịch cuối tuần hoặc ngày kết thúc khi chưa được thống nhất. Hiện đã hoàn thành 4/31 ngày theo mốc công việc; tỷ lệ này không đại diện phần trăm chức năng sản phẩm đã hoàn thiện.

| Giai đoạn | Phạm vi bắt buộc | Trạng thái |
|---|---|---|
| Day 1–4 | Data Collection, Cleaning & Integration, EDA, Feature Engineering | Đã hoàn thành; xem bằng chứng trong nhật ký |
| Day 5–10 | Recommendation Engine: baseline, content-based recommendation, weighted cosine similarity/KNN, bộ lọc và top 3–5 | Dự kiến |
| Day 11–16 | Model Evaluation, PostgreSQL và FastAPI | Dự kiến |
| Day 17–23 | Authentication, Privacy, Streamlit và OpenAI API | Dự kiến |
| Day 24–31 | Cloud Deployment, Integration Testing, Final Report và Presentation Slides | Dự kiến |

Kế hoạch từng ngày, đầu ra, điều kiện nghiệm thu và mốc Git được ghi trong mục **Lộ trình chính thức 31 ngày làm việc** của [`reports/project_log.md`](reports/project_log.md). Khi điều chỉnh lịch, cập nhật cả hai tài liệu, ghi lý do và giữ lại lịch sử; không bỏ yêu cầu để đạt ngày dự kiến.

### Quy tắc thực hiện lộ trình

- **Day 5–10:** Chọn vector đặc trưng có cơ sở, xử lý thiếu dữ liệu có bằng chứng, giữ riêng bộ lọc ngân sách/tuổi/vị trí/hiệu suất. Không mặc định dùng market value hoặc log market value như kỹ năng; không mặc định nhân minutes reliability vào điểm. Tránh đếm lặp goals/assists/goal contributions. Chỉ mô tả đúng giới hạn chỉ số hậu vệ/thủ môn.
- **Day 11–16:** Xây bộ tình huống và tiêu chí đánh giá trước khi chọn cấu hình; không bịa ground truth hoặc tuyên bố metric chưa đo. PostgreSQL phải lưu đủ `users`, `search_history`, `chat_sessions`, `chat_messages`, `recommendation_results`; thiết kế khóa ngoại/quyền sở hữu từ đầu. FastAPI ở giai đoạn này được phát triển/kiểm tra cục bộ; không công khai API dữ liệu riêng trước khi authentication/privacy được nghiệm thu.
- **Day 17–23:** Hoàn thiện đăng ký/đăng nhập/đăng xuất và cách ly dữ liệu ở backend, rồi tích hợp Streamlit tìm kiếm, top 3–5, so sánh bằng biểu đồ, lịch sử và scouting chat qua OpenAI API. Chat chỉ dựa trên dữ liệu thật được truy xuất, không tự điền thống kê còn thiếu; API key nằm phía server.
- **Day 24–31:** Chuẩn bị cloud, kiểm thử tích hợp, báo cáo và slides. Triển khai cloud thực tế chỉ khi người dùng cho phép. Nếu đang chờ phép hoặc thiếu hạ tầng, ghi rõ phần bị chặn và tiếp tục việc độc lập cục bộ; không ghi deploy đã hoàn thành. Final release cần bằng chứng nghiệm thu, hướng dẫn vận hành và giới hạn đã biết.
- Mỗi ngày chỉ được đánh dấu hoàn thành khi có đầu ra và kiểm tra phù hợp. Lưu lệnh/kết quả test, phát hiện và hạn chế; không tự báo pass theo kế hoạch. Nếu không đạt tiêu chí, ghi phần còn lại và điều chỉnh tiến độ minh bạch.

### Mốc Git và quyền thực hiện

- Các mốc **commit/push dự kiến**: **Day 5, 10, 15, 20, 25, 30**; **final release Day 31** gồm commit/tag/release dự kiến và push khi được phép.
- Trước mỗi mốc: rà diff, phạm vi thay đổi, secrets, dữ liệu bị ignore và test liên quan; commit có ý nghĩa, giữ nguyên lịch sử. Không force-add CSV bị ignore, không force push, reset --hard hoặc viết lại commit cũ.
- Mốc trong kế hoạch **không phải quyền tự động push, deploy hoặc phát hành release/tag lên GitHub**. Chỉ thực hiện khi có sự cho phép của người dùng cho hành động đó; lần push đã được cho phép trước đây không mặc nhiên cho phép các mốc tương lai.
- Phiên cập nhật lộ trình hiện tại chỉ sửa `AGENTS.md` và `reports/project_log.md`; không triển khai Day 5, không stage/commit/push/deploy hay tạo release.

## Tiến độ hiện hành — Day 5 (2026-10-28)

- Người dùng đã giao triển khai baseline Day 5 ở nhiệm vụ tiếp theo. **Day 1–5 đã hoàn thành theo phạm vi đã giao; Day 6–31 chưa triển khai.** Mục này cập nhật trạng thái trong các phần lịch sử, không xóa lịch sử hoặc thay yêu cầu sản phẩm/lộ trình 31 ngày.
- `src/recommendation/baseline.py` đã có cosine theo vị trí, StandardScaler fit trên tập reference riêng, bộ lọc vị trí/tuổi/ngân sách EUR/phút, Top K và giải thích dựa trên số liệu thật. `run_day5.py` chạy 5 kịch bản, lưu báo cáo; tổng 57 test đạt (34 Day 5 và 23 Day 4).
- Attack/Midfield dùng goals/90, assists/90 và vai trò. Defender/GK chỉ tìm hồ sơ bối cảnh bằng tuổi/phút/chân thuận (Defender thêm vai trò), luôn có nhãn `context_profile_only`; **không đánh giá GK bằng bàn thắng, không tuyên bố có mô hình kỹ năng phòng ngự/bắt bóng**.
- Không dùng market value/log value, reliability, percentile toàn catalogue, chiều cao nghi vấn hoặc CLB làm feature. Similarity không phải xác suất chuyển nhượng hay điểm kỹ năng. Kiểm tra loại query khỏi fit không thay thế đánh giá theo thời gian hoặc kiểm toán leakage đầy đủ.
- Baseline chuẩn hóa/cosine và giải thích cơ bản được thực hiện sớm theo yêu cầu Day 5; Day 6 tiếp tục kiểm chứng weighted cosine, tỷ trọng block và độ nhạy. Chưa làm KNN, API/UI hoặc đánh giá chuyên gia.
- Không tự stage/commit/push/deploy cho nhiệm vụ Day 5. Xem chi tiết kịch bản, bằng chứng, hạn chế và bước tiếp theo trong hai báo cáo và `src/recommendation/README.md`.

## Bàn giao liên công cụ và cập nhật sau mỗi Day — 2026-11-02

- Đã thiết lập bộ tài liệu bàn giao sang Claude Code; điểm vào [CLAUDE.md](CLAUDE.md), trạng thái hiện hành [docs/HANDOFF.md](docs/HANDOFF.md). Phiên này chỉ thiết lập tài liệu; **Day cuối vẫn là Day 5, Day 6 chưa triển khai**, không stage/commit/push/deploy. Các giới hạn nhiệm vụ cũ phía trên là lịch sử, không phải trạng thái hiện hành.
- [PROJECT_CONTEXT](docs/PROJECT_CONTEXT.md) tổng hợp sản phẩm và từng Day; [ARCHITECTURE](docs/ARCHITECTURE.md) phân biệt đã có/dự kiến; [FILE_INVENTORY](docs/FILE_INVENTORY.md) ghi vai trò, I/O, dependencies; [SETUP](docs/SETUP.md) hướng dẫn clone, môi trường, data, tests và chạy baseline.
- Kiểm tra trực tiếp trên máy Windows hiện có: 57 tests pass (23 Day 4 + 34 Day 5); pip check không phát hiện dependency hỏng. Không coi đó là bằng chứng đã cài thử trên máy mới, tái chạy raw pipeline hoặc đánh giá chất lượng scouting.
- HEAD local và origin/main cache là c4d638c; Day 5 và docs mới chưa commit. Clone commit này chưa có đủ source để tiếp tục. Chưa fetch/xác minh trạng thái GitHub trực tiếp trong phiên này.
- Dữ liệu raw/processed ngoài Git; [DATA_MANIFEST](docs/DATA_MANIFEST.json) lưu hash 8 file và schema/shape processed. Cần bàn giao riêng snapshot, không upload dữ liệu lớn/secrets. requirements UTF-16, unpinned; [environment-observed](docs/environment-observed.json) là phiên bản quan sát, không phải full lock đã kiểm chứng trên máy khác.
- **Sau mỗi Day:** chạy tests và ghi kết quả thực (hoặc lý do chưa chạy), cập nhật project_log, insights_and_defense và HANDOFF; cập nhật FILE_INVENTORY khi file/I/O/dependency đổi, SETUP/ARCHITECTURE khi cách chạy/thiết kế đổi. Giữ lịch sử trong báo cáo; cập nhật trạng thái hiện hành ở AGENTS/PROJECT_CONTEXT khi cần.
- HANDOFF phải có ngày/Day cuối có bằng chứng, branch/HEAD/status, việc chưa commit/chưa chuyển máy, snapshot/môi trường, lệnh chạy, blockers và next steps. Không cần AI mới biết lịch sử chat; mọi quyết định cần tiếp tục phải nằm trong repository.
- Báo cáo bằng tiếng Việt và đề xuất mốc commit/push Day 5, 10, 15, 20, 25, 30, final release Day 31; mốc không tự cấp quyền. Chỉ commit/push/deploy theo quyền nhiệm vụ tương ứng, giữ lịch sử và dữ liệu bị ignore.

## Tiến độ hiện hành — Day 6 (2026-11-02)

- **Day 1–6 hoàn thành trong phạm vi đã giao; Day 7–31 chưa triển khai.** Người dùng giao Day 6 sau phiên tài liệu; trạng thái/giới hạn nhiệm vụ trước là lịch sử. Không stage/commit/push/deploy trong nhiệm vụ Day 6.
- Thêm weighted.py, evaluation.py, run_day6.py, DAY6.md và tests/test_weighted_recommendation.py. Giữ nguyên code/tests/data/artefact Day 4–5. Weighted cosine dùng sqrt(w) với trọng số theo vị trí không âm, hữu hạn; không dùng market value/reliability như kỹ năng, Defender/GK chỉ context_profile_only.
- 109 tests đạt (57 cũ + 52 mới), 0 failed; tái lập đúng 5 kịch bản Day 5, unit weights khớp full ranking. 6 cấu hình × 5 kịch bản cùng snapshot/reference/filter đạt kiểm tra hành vi và deterministic ranking.
- reports/day6/ lưu JSON/3 CSV/2 PNG/summary; xem [DAY6.md](src/recommendation/DAY6.md). Mean overlap@5 trên 4 query nonempty: mặc định .90, bỏ categorical .25, bỏ numeric đầu tiên .35. Đây là độ nhạy so baseline, không chất lượng scouting; không có relevance labels nên không tính Precision/NDCG, chưa chọn trọng số tối ưu.
- Reference-only correlations củng cố tránh đếm lặp raw/per90/contributions/minutes-reliability; không suy luận nhân quả. Day 7 dự kiến KNN đối chứng trên cùng representation, metric/ties/filters và thời gian; chưa có temporal evaluation/API/UI.
- HEAD/main vẫn c4d638c, Git index không đổi; source Day 5–6/docs chưa commit. HANDOFF/inventory/log/insights đã bổ sung, mốc Day 5 vẫn chờ nhiệm vụ Git được phép; không tự push/deploy theo lịch.

## Tiến độ hiện hành — Day 7 (2026-11-02)

- **Day 1–7 hoàn thành trong phạm vi đã giao; Day 8–31 chưa triển khai.** Mục này cập nhật trạng thái các snapshot trước, không bỏ yêu cầu sản phẩm. Không commit/push/deploy.
- Thêm knn.py/run_day7.py/DAY7.md, tests/test_knn_recommendation.py và reports/day7 (JSON/5 CSV/PNG/summary). Baseline code/tests/data/artefact Day 5–6 giữ nguyên.
- KNN dùng sklearn NearestNeighbors cosine/brute, cùng reference-only scaler/features và filters. Lấy toàn bộ pool nonzero đã lọc rồi tie round12 + ID, loại query, cắt K; neighbors.fit không refit preprocessing.
- 178 tests đạt (109 cũ + 69 mới), 0 failed. 10 cặp full ranking, 50 trường hợp K và 1.000 benchmark calls; nonempty overlap@5=1/Spearman≈1, score difference=0, distance identity sai số <=4,45e-16 trong thí nghiệm.
- Benchmark local 5 warm-up/50 repeats/method/query, alternating, một luồng; KNN median cao hơn direct ở query nonempty. Giữ direct làm phương án hiện hành, KNN đối chứng; không kết luận scouting quality hoặc mọi workload. Defender/GK context-only, market value chỉ lọc/hiển thị, không Precision/NDCG khi thiếu labels.
- HANDOFF/inventory/architecture/logs đã cập nhật. Day 8 dự kiến hoàn thiện filters/hiệu suất theo dữ liệu thật và điều kiện biên; chưa triển khai. HEAD/index giữ nguyên; source Day 5–7/docs chưa commit, mốc Git cần quyền nhiệm vụ tương ứng.

## Hồ sơ thuyết trình và bảo vệ — bổ sung 2026-11-02

- [reports/PRESENTATION_AND_DEFENSE.md](reports/PRESENTATION_AND_DEFENSE.md) là hồ sơ tổng hợp phục vụ thuyết trình/bảo vệ, áp dụng cho cả Codex và Claude Code. Đọc cùng nhật ký, insights và HANDOFF trước công việc liên quan; hiện tổng hợp Day 1–7, không đánh dấu Day 8 hoặc sản phẩm web hoàn thành.
- **Sau mỗi Day, cập nhật đồng bộ bốn tài liệu:** PRESENTATION_AND_DEFENSE, reports/project_log.md, reports/insights_and_defense.md và docs/HANDOFF.md. FILE_INVENTORY cập nhật khi thêm/đổi file, I/O hoặc dependency.
- Mỗi Day trong hồ sơ phải có: mục tiêu; công việc; file/chức năng/input-output; thuật toán/công thức/lý do; kết quả có bằng chứng; khó khăn và cách giải quyết; hạn chế; **3–5 câu hỏi phản biện kèm câu trả lời**. Link tương đối tới code/tests/biểu đồ/CSV/JSON; nêu dataset/cutoff/hash, config/query/môi trường và test/commit thực có khi liên quan.
- Phân biệt đối chiếu code/artefact, kết quả chạy lịch sử, kiểm tra mới, giả thuyết và kế hoạch. Không coi đọc báo cáo là chạy lại, không tạo số test/metrics/nhãn hoặc câu chuyện sự cố chưa có bằng chứng. Thiếu bằng chứng ghi Chưa xác minh/Bị chặn.
- Giữ lịch sử; khi sửa kết luận phải ghi phần bị thay thế, lý do và nguồn. Đối chiếu số liệu/trạng thái giữa bốn tài liệu trước báo cáo. Lệnh, quyền Git và bảo vệ dữ liệu/secrets vẫn theo các quy tắc trên; bổ sung tài liệu không cấp quyền tự commit/push/deploy.

## Tiến độ hiện hành — Day 8 (2026-11-02)

- **Day 1–8 hoàn thành trong phạm vi đã giao; Day 9–31 chưa triển khai.** Thay trạng thái Day cuối của các snapshot trước, giữ lịch sử/yêu cầu sản phẩm.
- Thêm constraints.py (SearchConstraints + AdvancedRecommender), run_day8.py, DAY8.md, tests/test_advanced_constraints.py; 6 artefact reports/day8. Không sửa source/API/tests/artefact Day 5–7.
- Hard filters position/sub_position, tuổi, EUR, phút, goals/90, assists/90, chân thuận, club IDs trước ranking trên vector đã fit. Soft foot chỉ phá hòa score round12 rồi ID; không đổi score hoặc refit. GK từ chối ngưỡng goals/assists; Defender/GK vẫn context-only. Không dùng market value làm skill.
- **338 tests đạt, 0 failed** (178 cũ + 160 mới); 20 legacy checks và 20 scenario–engine cases đạt. Pools sau hard: 22/10/94/47/0; Top K 5/5/5/5/0. Same-representation direct/KNN full ranking khớp; không suy relevance quality hoặc tốc độ mới.
- Hồ sơ thuyết trình, log/insights, HANDOFF/inventory/architecture và hướng dẫn Claude đã cập nhật. Day 9 chuẩn hóa explanation và dữ liệu so sánh theo roadmap, chưa triển khai.
- Giữ main/HEAD c4d638c, index và lịch sử; source Day 5–8/docs chưa commit, data ngoài Git. Theo yêu cầu Day 8: **không commit/push/deploy; để commit khi chuyển máy trong nhiệm vụ được phép**. Lịch mốc Git không tự cấp quyền hành động.

## Tiến độ hiện hành — Day 9 (2026-11-02)

- **Day 1–9 hoàn thành trong phạm vi đã giao; Day 10–31 chưa triển khai.** Mục này cập nhật trạng thái các snapshot trước, giữ lịch sử và toàn bộ yêu cầu sản phẩm.
- Thêm comparison.py, explainability.py, run_day9.py, [DAY9.md](src/recommendation/DAY9.md), tests/test_explainability.py và 7 artefact reports/day9. Evidence tách text rule-based, JSON có version, so sánh 2–5 người bằng đơn vị gốc; mẫu số 0/missing có null và lý do. Không sửa source/API/scaler/ranking/eligibility/tests Day 5–8.
- **453 tests đạt, 0 failed** (338 cũ + 115 mới); 20 response khớp nguyên Day 8, 80 explanations/32 comparison groups. No-results không tạo cầu thủ hoặc nới constraints. Defender/GK chỉ context; không market value skill, similarity probability, causal attribution hoặc kết luận tốt hơn tổng thể.
- Bàn giao/log/insights/PRESENTATION_AND_DEFENSE/inventory/architecture/setup đã cập nhật. Day 10 dự kiến tích hợp dịch vụ Python cho API, ổn định cấu hình và regression; chưa thực hiện, chưa có web/API/chat.
- Khi sửa explanation sau này phải giữ nguyên response ranking, kiểm ID/score/units/components/constraints và render từ evidence; khi đổi internals cần kiểm adapter truy cập private representation. Chỉ gọi API/triển khai khi có nhiệm vụ phù hợp.
- main/HEAD c4d638c; giữ Git index, thay đổi cũ và snapshot dữ liệu. Source Day 5–9/docs chưa commit; clone HEAD hiện tại chưa đủ, cần bàn giao snapshot riêng/fresh-install. Không commit/push/deploy; mốc Day 10 không cấp quyền tự động.

## Tiến độ hiện hành — Day 10 (2026-11-02)

- **Day 1–10 hoàn thành trong phạm vi local đã giao; Day 11–31 chưa triển khai.** Giai đoạn Recommendation Engine có ứng viên tích hợp, chưa nghiệm thu chất lượng tuyển trạch/production. Mục này cập nhật trạng thái cũ, giữ lịch sử/yêu cầu sản phẩm.
- Thêm config.py, schemas.py, service.py, run_day10.py, [DAY10.md](src/recommendation/DAY10.md), tests/test_service.py và 9 artefact reports/day10 gồm [phase review](reports/day10/phase_review.md). Giữ source/API/tests/artefact Day 5–9, feature/scaler/eligibility/ranking/weights.
- Service validate request → hard filters → ranking/Top K → structured explanation → optional comparison → validate response. Bốn methods, default cosine; JSON có version/method/filters/counts/K/dataset/configuration hash/limitations, finite và deterministic. JSON Schema + domain/cross-field checks, chưa FastAPI endpoint/Pydantic/OpenAI.
- **549 tests đạt, 0 failed** (453 cũ + 96 mới); 20/20 full Day 8–9 responses/explanations/comparisons khớp; 400 measured calls + 60 warm-up cùng JSON. Latency local có protocol/mẫu raw/median/p95; không SLA, quality hoặc lựa chọn trọng số tối ưu.
- requirements.txt thêm jsonschema>=4.18,<5 (4.26.0 có sẵn), giữ encoding/nội dung cũ; không cài dependency trong phiên. Không đổi manifests/data; fresh-install/máy mới vẫn chưa nghiệm thu.
- Day 11 dự kiến protocol đánh giá/rubric/tình huống có nguồn và rà leakage/split/metrics theo nhãn thực có. Không Precision/NDCG thiếu labels; Defender/GK context-only, market value không skill/phí mua, similarity không probability.
- HANDOFF/SETUP/ARCHITECTURE/FILE_INVENTORY/PROJECT_CONTEXT, log/insights/PRESENTATION_AND_DEFENSE và CLAUDE cập nhật. main/HEAD c4d638c và index giữ nguyên; công việc Day 5–10 chưa commit. **Không commit/push/deploy; mốc Day 10 chờ người dùng quyết định khi chuyển máy.**
