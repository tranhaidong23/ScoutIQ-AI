# Day 9 — Recommendation Explainability & Player Comparison

Hoàn thành phạm vi local ngày 2026-11-02. Không sửa engine/API/scaler/features/ranking/eligibility Day 5–8; không gọi FastAPI/OpenAI, không UI hoặc Day 10. Snapshot Transfermarkt 2025/26, cutoff 2026-06-12, 4.112 cầu thủ × 28 cột. Đây không phải dữ liệu trực tiếp.

## API và đầu vào

```python
import json
import pandas as pd
from pathlib import Path
from src.recommendation.baseline import FEATURE_FILE
from src.recommendation.constraints import AdvancedRecommender
from src.recommendation.run_day8 import SCENARIOS, make_engines
from src.recommendation.explainability import RecommendationExplainer
from src.recommendation.comparison import PlayerComparison

data = pd.read_csv(FEATURE_FILE)
prior = json.loads(Path("reports/day8/evaluation.json").read_text(encoding="utf-8"))
engines = make_engines(data, prior["reference"]["fit_ids"])
_, query, constraints = SCENARIOS[0]
presenter = RecommendationExplainer(AdvancedRecommender(engines["weighted"]))
result = presenter.recommend(query, constraints, top_k=5)
ids = [row["player_id"] for row in result["recommendation"]["results"]]
comparison = PlayerComparison(data).compare([query] + ids[:4], reference_player_id=query)
json.dumps({"explanation": result, "comparison": comparison}, allow_nan=False)
```

Ví dụ chạy từ root với snapshot/prior JSON đúng hashes. Fit 4.108 ID, loại bốn query như runner Day 8; không fit lại theo bộ lọc. Có thể bọc trực tiếp CosineRecommender, WeightedCosineRecommender hoặc KNNRecommender với SearchFilters cũ; AdvancedRecommender cần SearchConstraints. Sai loại request bị từ chối.

`recommend()` gọi engine một lần rồi tạo envelope mới, giữ response nguyên trong `recommendation`. `explain_response(response, query, filters, top_k=5)` dùng khi đã có response: đối chiếu JSON chuẩn hóa với response được tính lại từ cùng engine/request, từ chối sai ID, kiểu ID/rank, tên, score, thứ tự, số lượng, đơn vị, evidence hoặc trạng thái. Đường validation này có thêm một lần retrieval, không fit preprocessing; chưa benchmark overhead. Phải truyền đúng top_k của response, không suy đoán request từ dữ liệu đã nhận.

## Evidence và công thức

- `scoutiq.explanation.v1`: reference, request, fit_audit, cutoff, status/empty_reason; danh sách `{evidence, text}`. Text sinh bằng `render_explanation(evidence)`, không đọc text tự do của response cũ.
- Evidence chứa ID/tên/CLB/vị trí/tuổi/phút/market value EUR/ngày định giá; feature raw thực dùng, đơn vị, trọng số, giá trị reference/candidate và chênh lệch; hard constraint có required/observed/passed; soft preference riêng; missing metadata liệt kê/null. Không impute missing hoặc thêm skill.
- Cosine components là từng tích tọa độ vector đã chuẩn hóa; tổng components của feature đang hoạt động bằng score trong sai số 1e-10. Feature weight=0 không được ghi là đóng góp. Có thể có components âm; đây không phải tỷ lệ kỹ năng hay tác động nhân quả. Khớp categorical raw khác với có trong vocabulary fit; cả hai được ghi rõ.
- `scoutiq.comparison.v1`: 2–5 ID nguyên dương, có thật, không trùng; reference phải thuộc nhóm, mặc định người đầu. Giữ thứ tự do người gọi cung cấp, không tự xếp hạng hoặc kết luận người tốt hơn.
- Signed delta = candidate − reference; absolute delta = abs(signed delta); relative % = 100 × signed delta / abs(reference). Nếu reference=0, relative=null với lý do `zero_reference`; nếu thiếu, delta=null với `missing_value`. NaN/infinity, bool, chuỗi số và phép tính tràn bị từ chối. Relative % giữ dấu, không phải mức cải thiện chất lượng.
- Attack cùng nhóm hoặc Midfield cùng nhóm: so tuổi, phút, EUR, goals/90, assists/90. Defender/GK hoặc nhóm lẫn vị trí: chỉ tuổi/phút/EUR và categorical context; không goals/assists như kỹ năng GK. Market value luôn là bối cảnh/ngân sách, không vào score.
- Validator tái dùng Day 4: schema/ID/missing numeric/range/per90/cutoff; kiểm thêm metadata columns, EUR so market_value_m nếu có. Metadata thiếu được giữ null; chỉ những trường được trình bày có trong missing_fields, không phải audit mọi cột dataset.

## Chạy và kết quả đã kiểm chứng

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day9 --output-dir reports/day9_rerun
```

Directory đầu ra phải mới; runner từ chối ghi đè. Linux/macOS dùng `.venv/bin/python`. Không dependency hoặc API key mới. Runner đọc features + reports/day8/evaluation.json, kiểm snapshot/9 source hashes cũ trước khi tạo outputs; ghi 12 source hashes hiện hành, 2 input hashes, query/config/reference/OS/package versions/Git HEAD. Cần mang cả source/tests chưa commit và dữ liệu ngoài Git sang máy mới.

- Baseline trước thay đổi: 338 passed in 47.81s. Lượt suite mới đầu: 452 passed, 1 failed in 81.33s do pandas 3 từ chối gán inf vào cột int64 trong fixture trước validator. Đổi dtype fixture sang float, giữ nguyên assertion từ chối infinity. Lượt cuối: **453 passed in 59.76s, 0 failed**, exit 0 (338 cũ + 115 mới).
- Tests bao phủ bốn engines × năm scenarios, API cũ, response tampering/NaN/inf/units/rank/ID, hard evidence, components/ablation, 2–5 người/duplicate/unknown IDs, mẫu số 0, missing categorical thật, zero reference vector, không refit/mutate và đảo thứ tự dữ liệu.
- Runner exit 0: **20/20 response khớp nguyên Day 8**, 80 giải thích, 32 nhóm so sánh. Pools 22/10/94/47/0; Top 5/5/5/5/0 cho tiền đạo/tiền vệ/hậu vệ/GK/no-results, giống nhau ở bốn engines. No-results không có giải thích cầu thủ/nhóm so sánh; vẫn có request, status và empty_reason.
- [evaluation.json](../../reports/day9/evaluation.json) giữ đầy đủ response/evidence/text/comparisons; [checks.csv](../../reports/day9/checks.csv) 20 dòng; [top5.csv](../../reports/day9/top5.csv) 80 dòng; [feature_evidence.csv](../../reports/day9/feature_evidence.csv) 260 dòng; [comparisons.csv](../../reports/day9/comparisons.csv) 448 dòng numeric. [Summary](../../reports/day9/summary.md) có Top 5 của năm kịch bản weighted và bảng so sánh; JSON có cả bốn engines/categorical. CSV không thay JSON schema và có ô trống theo loại field.
- Mỗi nonempty case dùng reference + Top 4 (5 người), rồi reference + người thứ 5 (2 người); bao phủ cả Top 5 mà không vượt giới hạn 5 người/nhóm. [Biểu đồ](../../reports/day9/attack_comparison.png) mô tả reference + Top 4 weighted Attack, ba trục đơn vị riêng, không radar điểm tổng hợp; đã xem ảnh kiểm tra nhãn/bố cục.

## Bằng chứng và giới hạn

Barney Stewart weighted similarity với Harry Kane = 0.956331763076 nhưng goals/90 = 0.6293706294 so 1.2661439114: signed delta −0.6367732821, absolute delta 0.6367732821, relative −50.29233062%. Đây là chênh lệch thống kê snapshot, không kết luận khả năng chơi bóng thấp hơn 50%. Tawanda Maswanhise thiếu foot vẫn hợp lệ vì soft preference không phải hard constraint; evidence giữ null.

Module phụ thuộc private catalogue/representation của engine để giữ API cũ; cần regression nếu thay internals. JSON có version nhưng chưa là FastAPI/Pydantic contract, chưa auth/privacy/chat. Không benchmark hiệu năng Day 9, chưa đo mức hữu ích của explanation với scouts. Chưa có relevance labels, temporal/league adjustment hoặc kỹ năng phòng ngự/bắt bóng. Fresh-install/chuyển máy chưa nghiệm thu. Không sửa raw/processed/manifests/dependencies hoặc artefact cũ; không commit/push/deploy.

Day 10 **dự kiến khi được giao**: tích hợp engine thành dịch vụ Python dùng lại cho API, ổn định cấu hình/pipeline filter→ranking→explanation/comparison, regression và tài liệu; chốt phiên bản ứng viên đánh giá, chưa gọi là mô hình tối ưu. Mốc Git chỉ là kế hoạch, phải có quyền riêng.
