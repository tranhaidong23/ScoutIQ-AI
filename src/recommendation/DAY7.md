# Day 7 — KNN Benchmark & Recommendation Robustness

Thực hiện 2026-11-02. Không thay code, tests, dữ liệu hoặc artefact Day 5–6. Day 7 thêm knn.py, run_day7.py, tests/test_knn_recommendation.py và outputs trong [reports/day7](../../reports/day7/summary.md).

## Implementation và phạm vi

KNNRecommender dùng scikit-learn NearestNeighbors(metric="cosine", algorithm="brute", n_jobs=1). Đây là truy xuất láng giềng chính xác, không classifier/regressor và không model học relevance.

- weights=None: gọi nguyên CosineRecommender để tạo representation Day 5.
- Truyền weights: gọi nguyên WeightedCosineRecommender Day 6; không đổi feature/scaler/reference.
- Attack/Midfield vẫn g90/a90/role; Defender vẫn age/minutes/role/foot, GK age/minutes/foot. Defender/GK context_profile_only.
- Fit scaler/category một lần trên reference đã chọn; filter/search không refit. Constructor/scaler fitting không nằm trong latency đo.
- Mỗi request lọc position/age/EUR/minutes, loại query và zero candidates trước. KNN.fit chỉ lưu các vector đã encode trong pool hợp lệ, không học lại scaling.
- Gọi kneighbors với X=query tường minh và n_neighbors=bằng số ứng viên hợp lệ. Sau đó score=round(1-distance,12), sort score giảm dần rồi player_id tăng dần, cuối cùng cắt K. Lấy tất cả neighbors bảo vệ ties ở ranh giới K và tránh lỗi lấy global Top K rồi mới filter.
- K lớn hơn pool trả tối đa số rankable thực có. Empty trả no_candidates; query vector 0 trả zero_reference_vector; candidate 0 bị loại và đếm. Không tự nới điều kiện.
- Vectors/inputs NaN, infinity, shape sai, query/K sai bị từ chối. Không định nghĩa cosine cho zero vector dù thư viện có thể áp một quy ước khác.
- Score trong [-1,1], distance trong [0,2]. Đối chiếu d=1-cos chỉ trên vector nonzero cùng representation; tolerance 1e-11 bao gồm round12.
- Output giữ evidence/cosine_components và giới hạn Day 5–6, thêm cosine_distance. Không bịa thống kê Defender/GK, không dùng market value hoặc reliability làm điểm kỹ năng.
- Adapter đọc cấu trúc nội bộ representation và dựng response tương đương; regression bảo vệ ranh giới này. Chưa refactor baseline dùng chung vì yêu cầu giữ nguyên baseline.

```python
from src.recommendation.knn import KNNRecommender
from src.recommendation.baseline import SearchFilters
from src.recommendation.weighted import default_weights

engine = KNNRecommender.from_csv(weights=default_weights())
result = engine.recommend(
    132098, SearchFilters("Attack", 18, 29, 30_000_000, 1800), top_k=5
)
```

API ví dụ fit toàn catalogue cho truy xuất mô tả; runner bên dưới dùng explicit fit_ids loại 4 queries như Day 5–6.

## Thí nghiệm và robustness

Snapshot features 4.112×28; SHA-256 425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0; season 2025/26, cutoff 2026-06-12. Fit 4.108 người, query IDs 132098/137576/139208/629773 giữ riêng. Đây không phải temporal evaluation.

Cùng SCENARIOS Day 5: Harry Kane (Attack, 18–29, €30M, >=1.800 phút); Hans Vanaken (Midfield, 20–30, €15M, >=1.800); Virgil van Dijk (Defender, 22–32, €15M, >=2.000); Lukas Hornicek (GK, 20–30, €10M, >=1.800); Attack ngân sách 0. Eligible lần lượt 349/405/512/107/0.

Hai cặp so sánh:

1. Day 5 direct cosine ↔ KNN trên representation Day 5.
2. Day 6 weighted_default direct cosine ↔ KNN trên đúng vector sqrt(w) của Day 6.

Runner kiểm source hashes/snapshot cũ, tái lập Top 5 của cả hai baseline từ JSON lưu trước, xác nhận fit audits giống nhau. 10 cặp full ranking đều khớp ordered IDs và score, đủ filters/unique/exclude-query/components/zero-vector semantics. Lặp lại và đảo catalogue/fit IDs không đổi kết quả; describe không đổi sau search.

K=1/3/5/50/10000 tạo 50 trường hợp; Top K luôn prefix full ranking, không lỗi khi K quá lớn. Unit tests bổ sung tie thật theo foot-only GK có >5 đồng hạng, zero vectors, NaN/invalid, budget/age/minutes biên, 5 cấu hình khác của Day 6 và bất biến market value/GK goals.

- 109 tests cũ trước triển khai: passed in 15.45s.
- Toàn suite sau triển khai: **178 passed in 20.19s, 0 failed** = 109 cũ + 69 mới.
- Max score difference KNN/direct = **0** trên các full rankings thực chạy.
- Max |distance − (1 − tổng cosine_components)| = **4.440892098500626e-16**.
- 8 cặp nonempty overlap@5=1, Spearman full-common ≈1; 2 empty trả null/N/A, không coi là độ ổn định hoàn hảo.
- Không tính Precision@K/NDCG@K vì không có trustworthy relevance labels. Parity là bằng chứng hai cách truy xuất tương đương trên thí nghiệm, không là chất lượng scouting.

## Benchmark

Windows 11, Python 3.13.7, NumPy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1, matplotlib 3.11.2. CPU báo Intel64 Family 6 Model 154 Stepping 4, 12 logical CPUs; không suy tên thương mại từ mã CPU.

- 5 warm-up/method/query, không ghi vào samples; 50 measured/method/query.
- 2 representations × 5 queries × 2 methods × 50 = **1.000 samples**; 100 warm-up calls.
- threadpoolctl giới hạn BLAS/OpenMP về 1 luồng trong block đo; n_jobs KNN=1, threadpool info lưu JSON. Không chạy tests/project jobs đồng thời với benchmark.
- Đồng hồ perf_counter_ns; luân phiên direct→KNN và KNN→direct giữa các repeat; cùng K=5 và pool filtered/nonzero.
- Đo full recommend gồm validation request, filter, retrieval, sort, evidence/explanation; KNN.fit trên filtered encoded vectors được tính trong KNN latency. Không gồm CSV I/O, scaler/category fitting, constructor, assertion hoặc ghi báo cáo.
- Median và p95 từ từng nhóm 50 mẫu; p95 dùng numpy.percentile(method="linear"). Raw timings có repeat và thứ tự gọi.
- So sánh đường chạy ứng dụng, không microbenchmark riêng phép nhân ma trận. Cả hai phương pháp đều trả cùng danh sách/evidence; chi phí adapter và trường distance của KNN cũng nằm trong timing.

Các ô dưới là **median / p95, ms**:

| Query | Day 5 direct | Day 5 KNN | Day 6 direct | Day 6 KNN |
|---|---:|---:|---:|---:|
| Attack | 2.466 / 3.131 | 3.474 / 4.032 | 4.889 / 7.154 | 6.643 / 10.116 |
| Midfield | 4.796 / 6.824 | 6.651 / 9.715 | 4.888 / 6.973 | 6.700 / 9.845 |
| Defender | 5.196 / 7.966 | 6.932 / 10.839 | 5.378 / 7.968 | 7.109 / 10.243 |
| GK | 4.480 / 6.328 | 6.154 / 8.462 | 4.568 / 6.783 | 6.167 / 9.333 |
| Empty | 2.603 / 3.678 | 2.666 / 3.302 | 1.781 / 2.714 | 1.815 / 2.860 |

Median KNN cao hơn direct ở 8/8 query nonempty trong phiên đo. Chưa có bằng chứng tốc độ/quality để thay baseline; giữ direct làm phương án hiện hành, KNN làm đối chứng. Không gọi tỷ lệ này là chi phí riêng thuật toán hoặc kết luận tổng quát mọi dữ liệu.

Giới hạn benchmark: một máy/phiên, background/OS jitter và trạng thái CPU không kiểm soát hoàn toàn, không đo cold start/concurrency/cloud/load hay confidence interval. Empty không gọi kneighbors, nên timing của nó là overhead/no-results path. Chênh latency giữa các query/representation không đủ để kết luận về độ phức tạp riêng từng vị trí.

## Chạy, input và outputs

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day7
```

Runner cần features CSV, reports/day5_recommendation_examples.json và reports/day6/evaluation.json cùng code đúng source hashes. Không ghi đè outputs mặc định, không có --overwrite. Chạy lại ở thư mục mới:

```powershell
.\.venv\Scripts\python.exe -B -m src.recommendation.run_day7 --output-dir reports/day7_rerun --warmup 5 --repeats 50
```

Linux/macOS thay executable bằng .venv/bin/python. threadpoolctl đã là dependency bắc cầu của sklearn trong venv hiện có, không cài package mới. Máy mới cần cài đầy đủ dependencies và kiểm import/tests; không copy venv Windows.

reports/day7/ có:

- evaluation.json: dataset/source/prior report hashes, fit/model audit, query/weights/evidence, parity, môi trường, protocol, timings tổng hợp và Git.
- comparisons.csv: 10 cặp full ranking, checks/overlap/Spearman/score-distance errors.
- robustness.csv: 50 trường hợp K, prefix và parity.
- timings.csv: 1.000 samples thực đo (không phải số liệu mô phỏng).
- benchmark.csv: 20 nhóm median/p95/min/max.
- rankings.csv: 5.492 ranked rows, có distance cho KNN.
- latency.png: median bars và p95 marks; đã xem kiểm bố cục/nhãn.
- summary.md: kết quả tổng hợp tự sinh.

## Q&A và Day 8

**KNN có model tốt hơn không?** Không có bằng chứng đó: cùng representation và cosine thì đây là hai cách truy xuất; kết quả hiện khớp. Không có relevance labels để đánh giá chất lượng.

**Vì sao lấy tất cả neighbors thay vì chỉ K?** Cần xử lý tie ở boundary K theo ID xác định; quy mô hiện tại nhỏ. Đây là lựa chọn chính xác/kiểm chứng, chưa phải tối ưu cho catalogue lớn hoặc ANN.

**KNN.fit có leakage từ candidate không?** Nó chỉ lưu vector đã transform; scaler/categories vẫn fit reference riêng, query không tham gia fit. Không suy ra đã giải quyết temporal leakage/metadata tại cutoff.

**Có thể gọi score cao là cầu thủ giỏi hoặc dễ mua?** Không. Similarity không là skill/probability; market value là ước tính, không phí chuyển nhượng. Defender/GK tiếp tục context-only, không có chỉ số chuyên môn được bịa thêm.

**Day 8 dự kiến:** hoàn thiện bộ lọc vị trí/tuổi/EUR/phút và ngưỡng hiệu suất từ chỉ số thật phù hợp; quy định rõ input/ranges/đơn vị và no-result; kiểm inclusive boundaries, kết hợp filter với ranking, missing và pool consistency. Không thêm bàn thắng như chỉ số kỹ năng GK hoặc dùng giá làm ground truth. Chưa triển khai Day 8, không commit/push/deploy.

