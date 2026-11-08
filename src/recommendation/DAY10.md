# Day 10 — Unified Recommendation Service

Service Python cục bộ, chưa tạo FastAPI endpoint hoặc gọi OpenAI. Giữ code/API/feature/scaler/weights/eligibility/ranking Day 5–9. Snapshot Transfermarkt 2025/26, cutoff 2026-06-12; market value không là skill/phí chuyển nhượng, similarity không là xác suất.

## Kiến trúc và cấu hình

- [config.py](config.py): ProjectPaths tính root từ vị trí module, nhận root/path khác; ServiceConfig giữ default method/top_k và weights Day 6, validate/copy. Không đường dẫn Windows hoặc secrets được hardcode. Không đưa weights vào request của người tìm kiếm.
- [schemas.py](schemas.py): JSON Schema Draft 2020-12 cho request/response; jsonschema validate structural core, cộng kiểm JSON hữu hạn, native types, cross-field consistency. Extra fields ở request/service envelope bị từ chối; các payload engine cũ có vùng extension để giữ compatibility. Không coi schema là bằng chứng dữ liệu do server tin cậy hoặc auth.
- [service.py](service.py): khởi tạo bốn engine một lần với cùng catalogue/reference. `recommend()` parse/validate → AdvancedRecommender hard filters trước ranking → Top K → RecommendationExplainer → optional PlayerComparison → validate response. Không refit scaler hoặc cache kết quả request; KNN vẫn fit neighbors trên filtered vectors theo Day 7.
- [run_day10.py](run_day10.py): năm scenarios Day 8 × bốn phương pháp, giữ fit IDs Day 9; đối chiếu full response/evidence/comparison, kiểm JSON lặp lại, đo latency riêng, từ chối output-dir tồn tại.

Phương pháp: `cosine`, `weighted_cosine`, `knn_cosine`, `knn_weighted_cosine`. Hai tên weighted map sang engine weighted/knn_weighted của runner cũ; không thay geometry. Mặc định direct cosine như phương án hiện hành, không tự chọn model tốt nhất hoặc tối ưu weights thiếu labels. Server có thể truyền ServiceConfig explicit; cấu hình bị sao chép khi xây service nên thay dict bên ngoài không làm đổi engine.

## Request và cách dùng

```python
import json
from src.recommendation.config import ProjectPaths
from src.recommendation.service import RecommendationService

paths = ProjectPaths()
prior = json.loads((paths.reports / "day9/evaluation.json").read_text(encoding="utf-8"))
service = RecommendationService.from_csv(paths.features, fit_player_ids=prior["reference"]["fit_ids"])
request = {
    "reference_player_id": 132098,
    "method": "weighted_cosine",
    "top_k": 5,
    "include_comparison": True,
    "filters": {
        "position": "Attack", "sub_positions": ["Centre-Forward"],
        "min_age": 18, "max_age": 23, "max_budget_eur": 5000000,
        "min_minutes": 1200, "min_goals_per90": 0.3,
        "preferred_foot": "left", "foot_mode": "soft", "excluded_club_ids": [27]
    }
}
response = service.recommend(request)
encoded_response = service.recommend_json(json.dumps(request))
rows = response["explanation"]["recommendation"]["results"]
explanations = response["explanation"]["explanations"]
groups = response["comparisons"]
```

Chỉ `reference_player_id` và `filters.position` bắt buộc; method/top_k mặc định từ config (cosine/5), include_comparison=false. Filters dùng hợp đồng Day 8: EUR gốc hoặc explicit budget_value+budget_unit EUR/EUR_million, không cả hai; tuổi inclusive, min minutes/per90, exact role/foot và excluded club IDs. Không đoán triệu, không bỏ qua unknown/invalid fields. GK không nhận goals/assists thresholds. Missing active hard constraint không đạt; soft foot chỉ phá hòa score round12 rồi ID.

ID/top_k phải native JSON integer dương, không bool/float/string; top_k lớn trả số có thực, không cap ngầm. Danh sách phải JSON array, không tuple/set; duplicate JSON keys, NaN/Infinity và số overflow bị từ chối. Validation lỗi trả ValueError phía Python; chưa có HTTP status/error middleware. Không ghi payload riêng tư vào lỗi.

Tái lập runner phải truyền đúng fit IDs (4.108, loại bốn query); không truyền fit IDs nghĩa fit toàn catalogue, được audit là `catalogue_snapshot`, không holdout evaluation. Constructor DataFrame dùng Day 4 candidate validator; from_csv kiểm đầy đủ features/percentiles trước dựng service. Biến thể RAM dùng trong tests không thay snapshot thật.

## Response v1

| Trường | Ý nghĩa |
|---|---|
| schema_version | `scoutiq.service.v1` |
| status | ok / no_candidates / zero_reference_vector, giữ engine cũ |
| request | Request được copy và bổ sung defaults; giữ biểu diễn budget ban đầu |
| metadata.method / filters | Method áp dụng và toàn constraints đã chuẩn hóa EUR/policy |
| candidate_count | Ở metadata: số người qua hard filters, loại query, có thể gồm zero vectors |
| rankable_count / returned_count / top_k | Qua hard trừ zero vectors / số trả thực / K yêu cầu. Zero reference có thể trả 0 dù rankable_count>0 |
| metadata.dataset | season/cutoff/source/rows/columns; version=`scoutiq-2025_26:`+content_sha256; csv_sha256 khi load từ CSV |
| metadata.configuration_id | Hash config + fitted audits + dataset content, không phải Git commit hoặc model quality |
| metadata.limitations | Giới hạn theo dataset/vị trí, không skill/probability |
| explanation | Nguyên envelope Day 9, gồm response Day 8 trong recommendation, structured evidence/text/reference/fit_audit/empty_reason |
| comparisons | Rỗng khi không yêu cầu/không có kết quả; có thì reference + mỗi block tối đa 4 candidates, 2–5 người/nhóm, bao phủ toàn Top K |

Response không chứa timestamp hoặc latency của request để JSON deterministic. Thời gian chỉ nằm trong artefact benchmark riêng. JSON serialization `allow_nan=False`, so score/ID/rank/count/method/filters/units/components/text-from-evidence và comparison arithmetic/IDs trước trả kết quả. Schema giữ cơ chế extension cho một số objects legacy; không phải mọi leaf legacy đều có schema riêng. Exported standard JSON Schema coi 5.0 là integer về toán học, nhưng runtime bổ sung type check để từ chối float ID/K. Khi tích hợp framework tương lai phải giữ validation bổ sung này.

Hash content dựa bảng đầy đủ sort ID rồi serialize CSV UTF-8/LF, độc lập thứ tự dòng trên cùng môi trường. csv_sha256 là hash bytes file nguồn, null cho DataFrame trong RAM; cần giữ hash raw này và manifest để chuyển máy. Phiên bản pandas/numeric backend có thể ảnh hưởng canonical serialization/audit hash; chưa hứa bitwise reproduction xuyên môi trường chưa pin. `describe()` trả bản copy dataset/config/audits của bốn engines.

## Chạy và benchmark

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day10 --output-dir reports/day10_rerun --warmup 3 --repeats 20
```

Linux/macOS dùng .venv/bin/python. Runner nhận `--features`, `--prior-day8`, `--prior-day9` nếu cần; output-dir phải mới. Cần source Day 5–10 + snapshot features + JSON Day 8/9 đúng hashes. Không cần tái chạy pipeline dữ liệu hoặc benchmark cũ để chạy Day 10. requirements.txt thêm `jsonschema>=4.18,<5`, bản 4.26.0 đã có sẵn trong .venv; không cài package mới trong phiên. Pydantic chưa được cài, chưa là dependency.

Đo `recommend_json` trọn parse request → validation → filters/ranking → explanations → optional comparisons → validate response → serialize JSON. Tất cả case dùng comparison=true, Top K=5; 3 warm-up + 20 đo/case, 20 cases, 400 measured calls. Luân phiên thứ tự bằng rotation, threadpool limit=1. Không đo CSV I/O/startup/fit/network/HTTP/auth; startup ghi riêng một quan sát, không coi là phân phối. p95 dùng numpy linear; không threshold tốc độ tùy tiện trong tests. Không chạy pytest đồng thời benchmark.

Kết quả thực, môi trường và Top 5: [summary](../../reports/day10/summary.md), [evaluation.json](../../reports/day10/evaluation.json), [benchmark.csv](../../reports/day10/benchmark.csv), [phase review](../../reports/day10/phase_review.md). Các số test/lượt chạy hiện hành ở project_log/HANDOFF; không coi docs kế hoạch là bằng chứng đã chạy.

## Giới hạn và Day 11

Chưa relevance labels/Precision/NDCG, temporal/metadata-at-cutoff audit, league/uncertainty adjustment, hoặc đánh giá explanation bởi scouts. Defender/GK chỉ context; market value không là skill/phí mua. Private adapters Day 8/9, full ranking và bốn engine trong RAM chưa tối ưu bộ nhớ/concurrency. Latency local cùng snapshot không chứng minh cloud SLA, throughput hoặc quality; không so trực tiếp số Day 7 vì phạm vi đo khác.

Ứng viên tích hợp v1 đủ để tiếp tục đánh giá, chưa production release. Day 11 dự kiến protocol/rubric/tình huống có nguồn, rà leakage/split khả thi và metric phù hợp nhãn thực có. FastAPI/DB/auth/privacy/Streamlit/OpenAI/cloud ở roadmap sau. Source/data bàn giao và fresh-install chưa nghiệm thu; không commit/push/deploy, mốc Day 10 chờ người dùng quyết định khi chuyển máy.
