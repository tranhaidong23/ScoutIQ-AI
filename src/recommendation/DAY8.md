# Day 8 — Advanced Filtering & Search Constraints

Triển khai ngày 2026-11-02 trên snapshot 2025/26, cutoff 2026-06-12: **4.112 cầu thủ × 28 cột**. Day 5–7 giữ nguyên source, API, tests và artefact. Không có backend/UI mới, không commit/push/deploy.

## API và ranh giới

[constraints.py](constraints.py) cung cấp `SearchConstraints`, `filter_candidates` và `AdvancedRecommender`. Bọc một engine đã fit: CosineRecommender, WeightedCosineRecommender hoặc KNNRecommender (cosine/weighted). SearchConstraints chứa SearchFilters cũ, **không kế thừa** SearchFilters và không được truyền thẳng vào engine cũ để tránh bỏ qua field mới.

```python
from src.recommendation.baseline import CosineRecommender
from src.recommendation.constraints import AdvancedRecommender, SearchConstraints

constraints = SearchConstraints.from_request({
    "position": "Attack",
    "sub_positions": ["Centre-Forward"],
    "min_age": 18, "max_age": 23,
    "budget_value": 5, "budget_unit": "EUR_million",
    "min_minutes": 1200, "min_goals_per90": 0.3,
    "preferred_foot": "left", "foot_mode": "soft",
    "excluded_club_ids": [27],
})
engine = AdvancedRecommender(CosineRecommender.from_csv())
result = engine.recommend(132098, constraints, top_k=5)
```

Ví dụ API trên dùng default fit toàn catalogue để retrieval mô tả. Muốn tái lập **đúng** báo cáo Day 8, dùng runner: nó loại bốn query IDs 132098/137576/139208/629773, fit 4.108 người như Day 5–7; chưa phải temporal split. Không thay fit IDs giữa các phương pháp.

## Hợp đồng filter

| Field | Loại / quy tắc |
|---|---|
| position | Hard; một broad position hiện có, phải khớp query |
| sub_positions | Hard; OR trong danh sách, AND với các ràng buộc khác; tên chính xác, thuộc position và snapshot |
| min_age / max_age | Hard; hữu hạn, 0 ≤ min ≤ max ≤ 100; bao gồm biên |
| max_budget_eur | Hard; EUR gốc ≥ 0 hoặc None (không giới hạn), không làm tròn sang triệu |
| budget_value + budget_unit | Chỉ ở from_request; pair bắt buộc, unit EUR hoặc EUR_million; chuyển million × 1.000.000, chặn overflow; không đồng thời max_budget_eur |
| min_minutes | Hard; hữu hạn ≥ 0; hạ dưới 900 không phục hồi người ngoài catalogue |
| min_goals_per90 / min_assists_per90 | Hard; hữu hạn ≥ 0 hoặc None; không cho Goalkeeper, kể cả ngưỡng 0; Defender nếu dùng chỉ là đóng góp tấn công |
| preferred_foot | left/right/both, so chính xác; both không tự được xem là left/right |
| foot_mode=hard (mặc định) | Bắt buộc đúng chân; missing bị loại |
| foot_mode=soft | Chỉ ưu tiên đúng chân trong nhóm cosine đã round12 bằng nhau; giữ nonmatch/missing; không thêm điểm hoặc vượt score cao hơn |
| excluded_club_ids | Hard; ID nguyên dương, không bool/trùng/ID lạ trong snapshot; dựa current_club_id, không so tên mơ hồ |

Field không biết/typo, type sai, boolean thay số, âm, NaN/infinity, min>max hoặc thiếu unit pair đều báo ValueError, không lờ đi. `max_budget_eur=5` nghĩa **5 EUR**, không suy ý định “5 triệu” từ độ lớn; caller/UI tương lai phải ghi đơn vị rõ. Đây là market value lịch sử, không phải giá mua thực tế hoặc skill.

Missing policy: dữ liệu bắt buộc của engine vẫn được validator Day 4–5 kiểm nghiêm; nếu không biết thuộc tính cần cho hard constraint thì không đạt constraint. Thiếu foot không bị loại khi không có hard foot, soft foot không được ưu tiên. Thiếu club ID bị loại khi đang có club exclusion vì không chứng minh được không thuộc CLB bị cấm. Không điền missing thành 0/chân/CLB giả. Role và club ID lạ bị từ chối cả khi budget đã khiến pool rỗng.

## Luồng xử lý và tương thích

1. Validate request/query và tên/ID theo snapshot.
2. Tạo hard mask theo thứ tự: position → exclude query → age → budget → minutes → sub_position → g90/a90 → hard foot → club exclusions. Audit mỗi bước ghi before/after/removed; số bị loại phụ thuộc thứ tự, không phải tầm quan trọng nhân quả.
3. Tạo **view riêng cho request** của data/encoded vectors đã fit, giữ query chỉ để tính similarity. Không sửa engine gốc, không fit scaler/category hoặc thay feature/weight. Query không bắt buộc thỏa điều kiện của ứng viên.
4. Gọi nguyên engine trên view đã lọc. KNN nhận pool nonzero hợp lệ; direct dùng cùng cosine/weighted cosine. Zero query trả `zero_reference_vector`; zero candidates bị loại/đếm theo engine cũ.
5. Lấy full ranking rồi sort `(-score_round12, -soft_foot_match, player_id)`, cắt K. Khi không soft, tie là score → ID như Day 5–7. Tính full ranking cần thiết cho soft preference ở boundary K, chưa tối ưu catalogue lớn.
6. Output giữ score/evidence/response cũ, thêm `search_constraints`, `filter_audit`, `constraint_evidence`, `soft_preference_match` và giải thích bằng số thật. K quá lớn trả số hiện có; không có người hợp lệ thì `no_candidates`, không tự nới điều kiện.

Adapter truy cập private representation của engine; đây là nợ kỹ thuật có chủ đích để giữ hashes/API cũ. Tests kiểm exact legacy ranking/scores, pool trước KNN, reference không đổi, không gọi StandardScaler.fit lúc search, deterministic tie và đảo dòng. Nếu nội bộ baseline thay đổi, phải xem lại adapter, không chỉ cập nhật snapshots.

## Thực nghiệm và kiểm thử

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day8 --output-dir reports/day8_rerun
```

Chạy từ root, output-dir phải chưa tồn tại; runner không overwrite. Linux/macOS thay executable bằng `.venv/bin/python`. Không cần API key hoặc dependency mới. Runner đọc features và JSON Day 5/6/7, kiểm source hashes Day 7, lưu dataset/reference/config/query/environment/source hash/Git HEAD và audit; output vào directory mới sau khi các kiểm tra thực nghiệm đạt.

- Trước sửa: **178 passed in 26.39s**, exit 0.
- Lần suite đầu sau thêm tests: **1 collection error** do dùng tên tham số `request` dành riêng của pytest. Đổi tên thành `payload`, không đổi assertion hoặc thuật toán để che lỗi.
- Suite sau sửa collection: 338 passed in 34.89s. Rà soát tiếp phát hiện cảnh báo thiếu K có thể sai khi full pool chứa zero vector nhưng Top K người dùng vẫn đủ; đổi K nội bộ thành số rankable, thêm assertion cosine/KNN. Suite cuối **338 passed in 44.83s, 0 failed**, exit 0 = 178 cũ + 160 mới.
- Runner được chạy lại vào directory tạm mới sau sửa; đối chiếu 4 CSV/summary và toàn response không đổi, rồi cập nhật artefact Day 8 do chính phiên này tạo. JSON hiện ghi hash code cuối và lần chạy cuối; artefact Day 5–7 không thay đổi. Không dùng lượt test hoặc runner này để so tốc độ.
- Runner: exit 0; **20/20 legacy checks**, **20/20 scenario–engine cases** đạt; 5 query × 4 engine. Direct/KNN cùng representation khớp full ranking. Oracle row-wise độc lập kiểm eligibility; tests đối chiếu full ranking cũ giao hard pool, score giữ nguyên.
- Windows 11, Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1. Không benchmark latency Day 8, không dùng thời gian pytest làm tốc độ search.

| Scenario / query | Hard constraints chính | Soft | Position trước → sau hard | Top K |
|---|---|---|---:|---:|
| Tiền đạo trẻ / Kane | Attack, Centre-Forward, 18–23, ≤5M EUR, ≥1.200 phút, g90≥0,3, loại club 27 | left khi đồng điểm | 1.059 → 22 | 5 |
| Tiền vệ kiến tạo / Vanaken | Midfield, Attacking Midfield, 20–29, ≤10M, ≥1.200 phút, a90≥0,15, left, loại club 2282 | Không | 1.204 → 10 | 5 |
| Hậu vệ kinh nghiệm / Van Dijk | Defender, Centre-Back, 28–35, ≤5M, ≥2.000 phút, right, loại club 31 | Không | 1.523 → 94 | 5 |
| GK ngân sách / Hornicek | GK, 20–30, ≤3M, ≥1.800 phút, right, loại club 1075 | Không | 326 → 47 | 5 |
| No-results / Kane | Attack, Centre-Forward, 18–23, budget=0 EUR, ≥1.200 phút, g90≥0,3, left | Không | 1.059 → 0 | 0 |

Toàn catalogue trước lọc là 4.112. Cột position trước lọc vẫn gồm query; self-exclusion có audit riêng. Tập sau hard giống nhau trên cả bốn engine; tất cả còn rankable trong 5 kịch bản này. Empty checks mang tính vacuous; không diễn giải true trên tập rỗng thành quality.

[summary](../../reports/day8/summary.md) ghi Top 5 weighted với tên/CLB/tuổi/EUR/score và explanation; [top5.csv](../../reports/day8/top5.csv) có 80 dòng cho cả bốn phương pháp. [evaluation.json](../../reports/day8/evaluation.json) có đủ config/weights và output; [scenarios.csv](../../reports/day8/scenarios.csv) 20 dòng, [filter_stages.csv](../../reports/day8/filter_stages.csv) 164 dòng, [rankings.csv](../../reports/day8/rankings.csv) 692 dòng. Dùng bảng trước/sau thay biểu đồ vì chỉ có năm tình huống; không thêm hình trùng thông tin.

## Hạn chế, phản biện và Day 9

- Ngưỡng scenario là kiểm hành vi, chưa tối ưu nhu cầu CLB. Defender/GK chỉ context_profile_only; tuổi/phút không chứng minh kinh nghiệm chuyên môn hay kỹ năng. Không Precision/NDCG khi thiếu labels, không coi filter correctness là chất lượng tuyển trạch.
- Metadata current_club_id/CLB chưa kiểm toán tại cutoff; 24 foot missing vẫn là dữ liệu thiếu. Hard foot có thể loại cầu thủ chỉ vì chưa biết chân; policy fail-closed phải được thể hiện rõ trên UI tương lai.
- Soft foot chỉ ảnh hưởng ties. Ví dụ Kane vẫn có người chân phải đứng trước Moukoko chân trái do cosine cao hơn; người thiếu foot vẫn có thể vào Top 5. Không được gọi đây là mô hình học sở thích.
- Adapter dùng private internals/full eligible ranking; chưa kiểm throughput/concurrency/cloud. Fresh-install/chuyển máy chưa nghiệm thu; source Day 5–8 và docs chưa commit, snapshot data ngoài Git.

1. **Sao không lọc Top 5 cũ?** Sẽ bỏ sót người đủ điều kiện nằm ngoài Top 5 toàn pool. View hard-filtered được đưa vào ranking trước; tests spy xác nhận pool KNN.
2. **5 có nghĩa 5 triệu không?** Chỉ khi khai `budget_value=5, budget_unit=EUR_million`. Field max_budget_eur luôn là EUR gốc, không đoán đơn vị.
3. **Ưu tiên chân trái mà có chân phải có sai không?** Soft chỉ phá hòa khi cosine bằng nhau; hard mới bắt buộc loại nonmatch/missing. Cả mode và match được trả rõ trong response.
4. **Lọc GK bằng goals/90 có được không?** API Day 8 từ chối; dữ liệu này không đo bắt bóng. Defender thresholds nếu yêu cầu chỉ là tấn công, không thay kỹ năng phòng ngự còn thiếu.

**Day 9 dự kiến:** chuẩn hóa explanation có thể truy vết, đầu ra phục vụ so sánh thống nhất đơn vị/cutoff, kiểm ties/đảo dòng/nhóm ít phân biệt. Biểu đồ UI vẫn ở Day 21. Không tự triển khai Day 9, commit/push/deploy; người dùng yêu cầu để commit đến khi chuyển máy.
