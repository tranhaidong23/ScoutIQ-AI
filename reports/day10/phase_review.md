# ScoutIQ — Phase Review Day 5–10

Kiểm tra ngày 2026-11-02. **Giai đoạn Recommendation Engine hoàn thành trong phạm vi local đã giao; chất lượng tuyển trạch chưa được nghiệm thu.** Đây là tổng hợp bằng chứng Day 5–9 và thực nghiệm mới Day 10, không tuyên bố đã chạy lại mọi benchmark/EDA cũ. Day 11 chưa triển khai; không commit/push/deploy.

## Từng Day và bằng chứng

| Day | Quyết định / đầu ra | Bằng chứng và giới hạn |
|---|---|---|
| 5 | [baseline.py](../../src/recommendation/baseline.py): StandardScaler/reference theo vị trí + one-hot + L2 cosine; tuổi/EUR/phút/vị trí tách khỏi score Attack/Midfield | [5 scenarios](../day5_recommendation_examples.json); 57 tests đạt theo lịch sử; Defender/GK chỉ context. Không dùng giá trị thị trường làm skill |
| 6 | [weighted.py](../../src/recommendation/weighted.py): sqrt(w/max(w)) trước L2, weights không âm; sáu cấu hình gồm ablation | [30 experiments](../day6/evaluation.json); 109 tests theo lịch sử. Mean overlap@5 mặc định .90, bỏ categorical .25 là độ nhạy, không relevance quality; weights là giả thuyết |
| 7 | [knn.py](../../src/recommendation/knn.py): NearestNeighbors cosine/brute trên đúng vector/pool, lấy toàn bộ trước tie/K | [benchmark](../day7/summary.md); 178 tests theo lịch sử, parity với direct. KNN median cao hơn direct ở 8/8 nonempty cases trong phiên Day 7; chưa khẳng định mọi workload |
| 8 | [constraints.py](../../src/recommendation/constraints.py): hard filters trước ranking, soft foot chỉ phá hòa, validation EUR/missing | [evaluation](../day8/evaluation.json); 338 tests theo lịch sử, pools 22/10/94/47/0; API cũ giữ nguyên |
| 9 | [explainability.py](../../src/recommendation/explainability.py), [comparison.py](../../src/recommendation/comparison.py): evidence/text tách, so sánh 2–5 người/unit/delta/zero/missing | [summary](../day9/summary.md); 453 tests theo lịch sử; 80 explanations/32 groups; không overall winner hoặc causal attribution |
| 10 | [service.py](../../src/recommendation/service.py), [schemas.py](../../src/recommendation/schemas.py), [config.py](../../src/recommendation/config.py): thống nhất request → hard constraints → ranking → evidence → optional comparison | [evaluation](evaluation.json), [checks](checks.csv), [tests](../../tests/test_service.py); 549 tests đạt trực tiếp, 20/20 full response/evidence/comparison khớp Day 8–9, JSON deterministic |

Tất cả dùng snapshot Transfermarkt 2025/26, cutoff 2026-06-12; 4.112×28 là cột dataset, không 28 skill features. CSV SHA-256 `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`. Runner Day 10 giữ fit 4.108 IDs, loại queries 132098/137576/139208/629773; không temporal split. Source/artefact Day 5–9 không đổi; đầy đủ source hashes và config/audits ở JSON Day 10.

## Contract và phạm vi tích hợp

Service hỗ trợ cosine/weighted_cosine/knn_cosine/knn_weighted_cosine, mặc định cosine; không lựa chọn weights từ kết quả robustness. API cũ được bọc, không refactor thuật toán. JSON `scoutiq.service.v1` có request defaults, metadata method/normalized filters/candidate_count/rankable_count/returned_count/top_k/dataset/configuration_id/limitations, nguyên envelope Day 9 và comparisons.

[Request schema](request.schema.json) và [response schema](response.schema.json) dùng Draft 2020-12; runtime thêm kiểm native JSON integer, finite numbers/duplicate keys và semantic consistency. Schema là structural core với vùng extension ở legacy objects; chưa Pydantic/HTTP contract. Lỗi là ValueError, không có FastAPI endpoint/error middleware/auth/privacy. Không API key hoặc network.

Optional comparison=true chia reference + mỗi block tối đa 4 candidates, đủ Top K, 2–5 người/nhóm. No-results không tự nới constraints hoặc tạo cầu thủ. Không đổi units/per90/reliability hay dùng market value để skill ranking. `configuration_id` là hash config/fitted audit/data, không là Git commit; csv_sha256 nhận diện bytes nguồn, content hash nhận diện bảng sort ID trên môi trường ghi nhận.

## Nghiệm thu trực tiếp Day 10

- Baseline trước triển khai: **453 passed in 58.18s**, exit 0. Suite mới riêng: **96 passed in 19.35s**. Toàn suite: **549 passed in 62.01s, 0 failed**, exit 0. Không có test thất bại trong các lượt này. Sau suite chỉ sửa đường link phase review của runner để trỏ đúng khi output-dir thay đổi; runner chạy exit 0 với source hash cuối.
- `pip check`: No broken requirements found. Khai báo `jsonschema>=4.18,<5` trực tiếp trong requirements UTF-16; bản 4.26.0 đã có trong .venv, không cài mới. Pydantic chưa cài, không dùng. Môi trường Windows 11/Python 3.13.7, numpy 2.5.4, pandas 3.0.6, sklearn 1.9.1, threadpoolctl 3.7.0.
- 20/20 cases giữ nguyên toàn response Day 8, envelope Day 9 và comparison groups (mạnh hơn chỉ so Top K). 80 kết quả Top 5, pools 22/10/94/47/0, returned 5/5/5/5/0; KNN/direct cùng representation không đổi kết quả. 400 measured calls + 60 warm-up đều serialized JSON giống đối chứng; fitted audits không đổi.
- Từ chối input sai/unknown fields/IDs/budget units/NaN/Inf/duplicate JSON keys; tests kiểm empty/zero vector/large K, defaults/config isolation, permutation, không refit/mutate, response consistency và serialization. Điều này không chứng minh hết leakage hoặc hiệu quả tuyển trạch.

## Latency local

[timings.csv](timings.csv): 400 mẫu; [benchmark.csv](benchmark.csv): 20 nhóm, mỗi nhóm 20 mẫu. 3 warm-up/case, rotation thứ tự 20 cases, threadpool limit=1. Đo recommend_json bao gồm JSON parse/validation, hard filter/ranking, Top K, evidence/text, comparison=true, response validation và JSON serialization. Không CSV I/O/khởi tạo/fit/network/HTTP/auth; không chạy pytest đồng thời. Startup một quan sát **1.423,006 ms**, không có median/p95 startup.

| Scenario | Cosine median/p95 ms | Weighted median/p95 ms | KNN cosine median/p95 ms | KNN weighted median/p95 ms |
|---|---:|---:|---:|---:|
| Tiền đạo trẻ | 85,663 / 150,281 | 90,031 / 145,246 | 85,961 / 135,414 | 95,938 / 122,860 |
| Tiền vệ kiến tạo | 74,381 / 102,959 | 80,826 / 103,740 | 76,931 / 112,387 | 85,739 / 108,948 |
| Hậu vệ kinh nghiệm | 125,829 / 156,275 | 125,921 / 158,670 | 131,079 / 161,772 | 141,391 / 193,290 |
| GK ngân sách | 94,444 / 138,373 | 95,010 / 149,366 | 101,926 / 163,410 | 95,522 / 154,879 |
| No-results | 29,309 / 55,904 | 32,203 / 53,664 | 32,357 / 43,127 | 24,718 / 51,294 |

p95 dùng numpy linear; chỉ 20 mẫu/case, có biến động lớn min/max trong CSV, chưa kiểm soát mọi tác vụ nền/thermal load. Không suy cloud SLA/throughput từ một máy, không so trực tiếp với Day 7 vì phạm vi đo đã thêm schema/comparison/serialization. Không có benchmark toggling comparison hoặc phân rã chi phí nên không quy overhead cho một module cụ thể. Không dùng số tốc độ để chọn model tốt hơn về quality.

## Kết luận giai đoạn và phần còn lại

**Đủ bằng chứng:** ứng viên tích hợp local v1, contract/validation, bốn methods, cùng reference/scaler và filters, explanation/comparison có dữ liệu, deterministic trên snapshot, test hồi quy và báo cáo tái lập. Mặc định direct cosine được giữ; weighted là cấu hình giả thuyết, KNN là đối chứng. Không ghi nhận model tối ưu hoặc production release.

**Chưa xác minh:** relevance labels/expert review, temporal/metadata-at-cutoff audit, league/tactical/uncertainty adjustment, kỹ năng Defender/GK. Dataset ≥900 phút bỏ người ít phút; metadata missing ảnh hưởng hard constraints. Private adapters, full ranking, bốn engine trong RAM và schema legacy extension cần quản lý khi API phát triển. Chưa benchmark concurrent users, large catalogue, memory hoặc cloud. Cần resource limits/auth/privacy trước public endpoint; không tự áp giới hạn làm đổi API cũ trong Day 10.

**Day 11 dự kiến:** thiết lập protocol/rubric và tình huống có nguồn; xác định baseline/metric eligibility, coverage, stability, latency; rà leakage, thiết kế split khả thi theo thời điểm dữ liệu thực. Chỉ Precision@K/NDCG khi có nhãn đáng tin cậy; không market value ground truth. Day 11 chưa triển khai trong phiên này. PostgreSQL/FastAPI/auth/Streamlit/OpenAI/cloud tiếp tục đúng roadmap.

**Bàn giao/Git:** main/HEAD c4d638c2d10c542c897ccf95dedde540814925b1; source/tests/docs Day 5–10 chưa commit. Clone riêng HEAD chưa đủ; cần snapshot 8 file ngoài Git theo manifest, prior JSON/source đúng hashes và kiểm môi trường sạch. Chưa nghiệm thu fresh-install/máy đích. Mốc Day 10 chờ người dùng quyết định khi chuyển máy; không stage/commit/push/deploy/fetch.

## Phản biện

1. **Phase review đạt nghĩa model tốt nhất?** Không. Chỉ chốt ứng viên tích hợp để đánh giá; test parity/stability không thay relevance labels hoặc chuyên gia.
2. **Vì sao thêm JSON Schema khi đã có validation Day 8?** Service có method/ID/K/comparison/config/metadata mới và JSON serialization. Schema kiểm shape/type, Day 8 kiểm domain constraints, cross-field checks bảo vệ response; không tạo lại thuật toán.
3. **p95 dưới 200 ms ở bảng có thể cam kết cloud?** Không. Máy local, 20 mẫu/case, một luồng, không HTTP/auth/DB/concurrency và có outlier. Đã lưu raw timings để đánh giá tiếp, chưa có SLA.
4. **Clone GitHub trên máy mới chạy được ngay?** Chưa. HEAD hiện thiếu công việc Day 5–10; data ngoài Git, dependencies chưa full lock. Cần bàn giao/commit khi được phép rồi nghiệm thu clone sạch với đúng snapshot và môi trường.
