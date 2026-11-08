# Day 5 — Baseline Content-Based Player Recommendation

Chạy từ thư mục gốc bằng `.venv`:

```powershell
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day5
.\.venv\Scripts\python.exe -B -m pytest tests/test_recommendation.py tests/test_features.py -q -p no:cacheprovider
```

```python
from src.recommendation.baseline import CosineRecommender, SearchFilters

engine = CosineRecommender.from_csv()
result = engine.recommend(
    reference_player_id=132098,
    filters=SearchFilters("Attack", min_age=18, max_age=29,
                          max_budget_eur=30_000_000, min_minutes=1800),
    top_k=5,
)
```

API nhận **ID cầu thủ tham chiếu có thật**, không tự tạo hồ sơ lý tưởng. Vị trí bộ lọc phải khớp vị trí tham chiếu; tham chiếu có thể nằm ngoài ngân sách/tuổi tìm kiếm. Chính cầu thủ tham chiếu được loại khỏi kết quả.

## Feature selection và ý nghĩa

| Vị trí | Số: StandardScaler theo vị trí | Phân loại: one-hot | Phạm vi diễn giải |
|---|---|---|---|
| Attack | goals_per90, assists_per90 | sub_position | Đóng góp tấn công và vai trò, chưa đầy đủ tactical fit |
| Midfield | goals_per90, assists_per90 | sub_position | Chỉ đóng góp tấn công; chưa có chuyền bóng/thu hồi bóng |
| Defender | age, minutes_played | sub_position, foot | Hồ sơ bối cảnh, **không đánh giá kỹ năng phòng ngự** |
| Goalkeeper | age, minutes_played | foot | Hồ sơ bối cảnh, **không đánh giá năng lực bắt bóng** |

Attack/Midfield dùng cùng hai số đo vì nguồn hiện có không đủ để bịa feature chuyên biệt; vai trò và tập chuẩn hóa khác nhau. Defender/GK không dùng goals, assists hay các biến dẫn xuất từ chúng. Tuổi/phút ở hai nhóm này chỉ mô tả bối cảnh, không mặc định trẻ hơn hoặc ra sân nhiều hơn là tốt hơn. Trường `similarity_scope=context_profile_only` và cảnh báo luôn đi kèm kết quả.

Không dùng định giá, log định giá, CLB, ID, chiều cao chưa xác minh, minutes reliability, tổng goal contributions hoặc percentile Day 4 trong vector. Tránh đếm lặp số đếm/per90/contributions và không dùng percentile tính trên toàn catalogue để đánh giá held-out. Ngân sách luôn so với EUR gốc.

## Thuật toán và tái lập

1. Kiểm tra snapshot đầu vào; không impute số liệu, không loại dòng âm thầm. `from_csv` kiểm tra cả artefact Day 4; constructor kiểm tra hợp đồng cột gốc và per90 để cho phép thử tập tham chiếu riêng.
2. Chọn tập fit bằng `fit_player_ids` (nếu bỏ qua: toàn catalogue cho truy xuất mô tả, không phải holdout evaluation). Fit StandardScaler và danh mục one-hot riêng theo vị trí, **trước bộ lọc tìm kiếm**. Không fit lại khi recommend.
3. Số được biến đổi `z=(x-mean_fit)/std_fit`; cột phương sai 0 theo quy ước StandardScaler. Danh mục thiếu/chưa thấy trong fit có block 0; không tạo chân thuận/vai trò giả hoặc thưởng cho hai giá trị cùng thiếu.
4. Ghép z-score và one-hot, trọng số mỗi chiều bằng 1 ở baseline; L2 normalize rồi tích vô hướng tương đương cosine. Tỷ trọng block chưa được tối ưu; Day 6 kiểm chứng weighted cosine.
5. Lọc theo vị trí, tuổi (hai đầu bao gồm), ngân sách tối đa EUR (bao gồm), phút tối thiểu (bao gồm); bỏ chính ID tham chiếu. Catalogue đã giới hạn >=900 phút; hạ min_minutes không thêm cầu thủ ngoài dữ liệu.
6. Vector 0 không có cosine xác định: trả trạng thái rõ nếu tham chiếu 0; bỏ ứng viên vector 0 với số lượng được báo. Không trả thứ hạng tùy ý.
7. Cosine trong [-1,1] vì z-score có thể âm. Làm tròn 12 chữ số để xử lý nhiễu số thực, xếp giảm dần; hòa điểm dùng player_id tăng dần. Không dùng định giá làm tie-break. Trả ít hơn K nếu không đủ, không tự nới filter.
8. Mỗi kết quả có số liệu gốc của cả hai cầu thủ (`evidence`), đóng góp từng chiều (`cosine_components`, tổng bằng cosine trong tolerance), explanation theo template và cảnh báo. Không dùng LLM để tự diễn giải thống kê chưa có.

Missing CLB giữ `null`, giao diện báo thiếu. Metadata CLB hiện tại có thể không khớp CLB tại cutoff; không dùng CLB cho similarity. Chiều cao 19 cm giữ nguyên trong input và bị loại khỏi vector, chưa xác minh giá trị đúng.

## Kiểm tra leakage và giới hạn

Runner dùng 4 ID tham chiếu thật (Attack/Midfield/Defender/GK), loại khỏi tập fit: 4.108 cầu thủ fit, 4 truy vấn chưa tham gia fit. Kiểm tra ngày định giá <= cutoff và tuổi định giá nhất quán. Scaler/danh mục được lưu trong báo cáo để kiểm tra; tests thay đổi dữ liệu held-out trong bộ nhớ và xác nhận tham số fit không đổi.

Đây là kiểm tra ranh giới preprocessing, **không phải temporal evaluation**, không chứng minh độ chính xác recommendation. Chưa kiểm toán toàn bộ thời điểm metadata hay dữ liệu trận nguồn. Snapshot 2025/26 bị chọn mẫu bởi ngưỡng 900 phút và định giá; chưa điều chỉnh độ mạnh giải đấu, hợp đồng, chấn thương hoặc vai trò thực tế.

Cosine đo hướng vector đã mã hóa, không bảo đảm hai cầu thủ có số đo tuyệt đối bằng nhau. Score cao không phải xác suất chuyển nhượng, chất lượng cầu thủ hoặc khả năng chiêu mộ. Score không so sánh trực tiếp giữa các vị trí. KNN, trọng số được đánh giá, API/UI và đánh giá chuyên môn nằm ở các ngày tiếp theo.
