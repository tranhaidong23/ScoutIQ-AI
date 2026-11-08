# Day 6 — Weighted cosine và đánh giá hành vi

Ngày thực hiện 2026-11-02. Giữ nguyên baseline.py, run_day5.py, tests Day 4–5 và báo cáo Day 5. Kết quả Day 6 lưu riêng [reports/day6](../../reports/day6/summary.md).

## API, công thức và hợp đồng

```python
from src.recommendation.weighted import WeightedCosineRecommender, default_weights
from src.recommendation.baseline import SearchFilters

weights = default_weights()
engine = WeightedCosineRecommender.from_csv(weights=weights)
result = engine.recommend(
    132098, SearchFilters("Attack", 18, 29, 30_000_000, 1800), top_k=5
)
```

Ví dụ API trên fit toàn catalogue cho truy xuất mô tả; runner dùng fit IDs riêng, loại 4 query, như Day 5.

Trên vector x/y đã StandardScaler + one-hot theo vị trí:

**cos_w(x,y) = Σ(w_i x_i y_i) / √[Σ(w_i x_i²) Σ(w_i y_i²)].**

Thực thi bằng nhân mỗi chiều với sqrt(w/max_w) rồi L2 normalize. Chia cùng max_w không đổi cosine, tránh số quá lớn. Nhân trực tiếp vector với w sẽ vô tình dùng w²: tests có oracle độc lập để phát hiện lỗi đó.

Trọng số phải là số thực hữu hạn, không âm (bool/string/NaN/∞ bị từ chối). Cấu hình truyền vào phải đủ đúng 4 position và đúng semantic feature keys; không chấp nhận market value, reliability hay thêm bàn thắng cho GK. Mỗi vị trí phải còn >=1 trọng số dương. Trọng số 0 là ablation hợp lệ; toàn 0 bị từ chối. Dynamic range gây underflow bị từ chối; vector có norm <=1e-12 dùng quy tắc zero-vector Day 5. Vector query 0 trả status rõ; candidate 0 bị loại và đếm.

Một trọng số categorical áp cho từng chiều one-hot của **cùng block**, không chia theo số category: mỗi block có tối đa một indicator=1. Missing/unseen vẫn block 0. Các số trọng số không phải tỷ lệ đóng góp điểm cố định hay xác suất; đóng góp còn phụ thuộc z-score, norm và dữ liệu. Numeric variance và categorical energy khác nhau; chưa tối ưu block normalization.

Dùng lại validation/fit/filter/ranking từ baseline, không đổi baseline. Subclass phụ thuộc cấu trúc matrix nội bộ Day 5, có tests parity để phát hiện thay đổi. Các feature bị ablate không xuất hiện như lý do trong evidence/explanation; component bằng 0 còn trong audit để truy vết. Giữ min/max age, EUR budget, min minutes, exclude query, tie ID và xử lý thiếu ứng viên.

## Cấu hình đã thực nghiệm

Thứ tự trọng số:

- Attack/Midfield: (goals_per90, assists_per90, sub_position).
- Defender: (age, minutes_played, sub_position, foot).
- Goalkeeper: (age, minutes_played, foot).

| Cấu hình | Attack | Midfield | Defender | GK |
|---|---|---|---|---|
| baseline | (1,1,1) | (1,1,1) | (1,1,1,1) | (1,1,1) |
| weighted_default | (.4,.4,.2) | (.3,.5,.2) | (.2,.2,.4,.2) | (.25,.25,.5) |
| numeric_emphasis | (.6,.3,.1) | (.2,.7,.1) | (.4,.4,.1,.1) | (.45,.45,.1) |
| categorical_emphasis | (.2,.2,.6) | (.15,.25,.6) | (.1,.1,.6,.2) | (.1,.1,.8) |
| ablate_categories | (.4,.4,0) | (.3,.5,0) | (.2,.2,0,0) | (.25,.25,0) |
| ablate_first_numeric | (0,.4,.2) | (0,.5,.2) | (0,.2,.4,.2) | (0,.25,.5) |

Default giả thuyết ưu tiên số liệu tấn công hơn role ở Attack/Midfield, ưu tiên assists tương đối ở Midfield; các nhóm context dùng thông tin tuổi/phút/vai trò/chân thuận. Đây **không phải trọng số học từ chuyên gia hoặc cấu hình thắng cuộc**. numeric_emphasis chỉ nhấn numeric, không thể gọi là hiệu suất phòng ngự/GK. Hai ablation thay đúng các field mô tả trên, giữ các trọng số còn lại.

Không dùng goals và goals/90 đồng thời; không thêm contributions/90 là tổng tuyến tính của goals/90 + assists/90. Không dùng percentile tính toàn catalogue để fit held-out. Minutes là bối cảnh ở Defender/GK, filter ở các nhóm; reliability=min(minutes/2700,1) chỉ heuristic quan sát, không nhân vào score. Market value chỉ lọc ngân sách/hiển thị, không định nghĩa kỹ năng hoặc relevance.

## Protocol và kết quả

Input 4.112×28, SHA-256 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0, mùa 2025/26, cutoff 2026-06-12. Reference 4.108 người, loại các query IDs 132098/137576/139208/629773. Tập fit theo vị trí: Attack 1.058, Midfield 1.203, Defender 1.522, GK 325. Scaler/category fit trước filter, không refit theo query.

5 SCENARIOS Day 5 giữ nguyên: Harry Kane Attack 18–29, €30M, >=1.800 phút; Hans Vanaken Midfield 20–30, €15M, >=1.800; Virgil van Dijk Defender 22–32, €15M, >=2.000; Lukas Hornicek GK 20–30, €10M, >=1.800; Attack ngân sách 0. ID là khóa truy vấn.

Runner:
1. So hash dataset và tái lập 5 kết quả Day 5, exact ID/score/filter/count/status/fit audit; không ghi lại artefact cũ.
2. Đối chiếu unit weights với baseline trên **toàn bộ ranking**.
3. Chạy 6 cấu hình × 5 kịch bản, kiểm tất cả hàng rankable: filters, score hữu hạn [-1,1], ID duy nhất/không query, sort và tổng explanation components.
4. Kiểm lặp và đảo thứ tự catalogue/fit IDs; kiểm Top K là prefix full ranking, không thay tham số fit.
5. Overlap@5 = |giao hai Top 5|/5; không đổi mẫu số khi ít hơn 5. Nếu một danh sách rỗng: null/N/A.
6. Spearman full-common: lấy toàn bộ pool rankable chung, average rank của score đã làm tròn 12 chữ số, rồi Pearson giữa hai rank vectors. Score ties không bị biến thành khác biệt giả do ID tie-break. Nếu <2 người hoặc rank hằng: null kèm lý do. Chỉ kiểm pool chung có thể che khác coverage, nên luôn lưu same_rankable_pool và số lượng.
7. Không tính Precision@K/NDCG@K: không có relevance labels đáng tin cậy.

Tất cả 30 tổ hợp đạt checks; 24 nonempty, 6 empty (check filter empty là vacuous, không giả 100% chất lượng). 8.238 dòng full ranking được lưu CSV. Pool không đổi giữa cấu hình trong lần chạy này.

| Cấu hình | Overlap@5 Attack / Mid / Def / GK | Trung bình 4 truy vấn | Spearman trung bình |
|---|---|---:|---:|
| baseline | 1 / 1 / 1 / 1 | 1.00 | 1.0000 |
| weighted_default | .8 / 1 / 1 / .8 | .90 | .9882 |
| numeric_emphasis | .6 / 1 / 1 / 1 | .90 | .9723 |
| categorical_emphasis | .8 / 1 / .8 / .8 | .85 | .9265 |
| ablate_categories | 0 / .4 / .2 / .4 | .25 | .8785 |
| ablate_first_numeric | 0 / .6 / .2 / .6 | .35 | .7397 |

Trung bình chỉ mô tả 4 query cố định, không ước lượng chất lượng dân số. Bỏ categorical ở Attack: overlap=0 dù rho=.9331; shortlist nhạy hơn full-rank correlation. Giữ baseline làm đối chứng; chưa chọn cấu hình sản xuất.

Audit Pearson/Spearman 264 cặp theo position trên reference, ngưỡng |Pearson|>=.8 là cờ mô tả. Attack goals–goals/90=.8106, assists–assists/90=.8307; Midfield tương ứng .8825/.8525. Goals/90–assists/90 chỉ -.0189 ở Attack và .3472 ở Midfield, chưa có lý do loại một trong hai chỉ vì tương quan. Minutes–reliability Pearson .9150–.9607; thêm cả hai dễ đếm lặp thời lượng. Tương quan GK có thể do biến tấn công thưa; không dùng để suy ra kỹ năng GK.

## Chạy và artefact

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day6
```

Lần đầu ghi reports/day6/. Nếu đã tồn tại, script từ chối; để so lần mới mà giữ cũ:

```powershell
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day6 --output-dir reports/day6_rerun
```

Chỉ dùng --overwrite nếu chủ động muốn thay artefact Day 6. Không ghi data/raw, processed hoặc report Day 5. Linux/macOS thay executable bằng .venv/bin/python.

- evaluation.json: source/dataset hash, query/filter, environment, Git local, fit audit, cấu hình, checks, metrics, Top 5 đầy đủ evidence.
- metrics.csv: 30 dòng cấu hình–kịch bản.
- rankings.csv: 8.238 hàng ranked, dùng đối chiếu các metric.
- correlations.csv: 264 cặp reference-only, Pearson/Spearman và lý do undefined nếu có.
- comparison.png: overlap và Spearman theo query/config; không biểu diễn scouting quality.
- correlations.png: các biến chẩn đoán theo 4 vị trí (không phải tất cả được dùng trong model).
- summary.md: bảng so sánh và Top 5 mặc định.

109 tests pass (57 cũ + 52 mới), 0 failed trong lần chạy 13,12 giây. Hai hình đã xem để kiểm tra nhãn/bố cục. Tests và thí nghiệm không thay temporal evaluation/đánh giá chuyên gia. Chưa điều chỉnh giải đấu, role thực tế, chấn thương/hợp đồng hoặc metadata CLB tại cutoff.

Day 7: KNN trên cùng representation/reference/filter; cosine distance đối chứng parity và tie handling, sau đó mới khảo sát metric khác có cơ sở, độ nhạy và thời gian. Không chọn cấu hình bằng market value hoặc cố làm overlap cao; không thêm nhãn relevance giả.

