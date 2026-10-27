# ScoutIQ – Hướng dẫn dự án và làm việc trong repository

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
