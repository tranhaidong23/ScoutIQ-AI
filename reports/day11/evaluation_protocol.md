# Day 11 — Recommendation Evaluation Protocol v1

Ngày kiểm tra: 2026-11-03. **Đã triển khai protocol, audit và công cụ; chưa có đánh giá relevance độc lập.** [evaluation.json](evaluation.json) là kết quả chạy mới; [synthetic_metrics.json](synthetic_metrics.json) chỉ là phép thử toán học SYNTHETIC. Không chọn weights mới hoặc thay ranking Day 5–10.

## Câu hỏi và đơn vị đánh giá

Đánh giá riêng: (1) bộ lọc/contract có đúng không, (2) kết quả có tái lập/ổn định không, (3) hồ sơ có phù hợp nhu cầu được mô tả không. Hai câu đầu không thay thế câu thứ ba. Đơn vị nhãn là **scenario–player–assessor** trên snapshot Transfermarkt 2025/26, cutoff 2026-06-12; không phải chất lượng toàn diện hoặc xác suất ký hợp đồng.

Dataset: 4.112 × 28, SHA-256 `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`. Service/fit IDs/configuration hash/source hashes/môi trường nằm trong evaluation.json. Fit reference 4.108 người, loại 4 query; đây là holdout theo ID để kiểm tra fit, **không phải temporal evaluation**. Không fit lại scaler hoặc tối ưu weights bằng chính bộ tình huống này.

## Tình huống và universe cố định

Nguồn: [SCENARIOS Day 8](../../src/recommendation/run_day8.py), tái dùng nguyên Day 9–10. Đây là bốn demo do dự án xây dựng, **không phải yêu cầu lịch sử của scout/CLB**. Query là hồ sơ tham chiếu, không bắt buộc tự thỏa ràng buộc ứng viên. Query không nằm trong candidate pool.

| Scenario / reference ID | Hard constraints (biên bao gồm) | Soft preference | Ứng viên |
|---|---|---|---:|
| young_low_budget_striker / 132098 | Attack/Centre-Forward; 18–23 tuổi; ≤5.000.000 EUR; ≥1.200 phút; ≥0,3 goals/90; loại CLB 27 | Chân trái chỉ phá hòa score | 22 |
| creative_midfielder / 137576 | Midfield/Attacking Midfield; 20–29; ≤10.000.000 EUR; ≥1.200 phút; ≥0,15 assists/90; chân trái; loại CLB 2282 | Không | 10 |
| experienced_defender / 139208 | Defender/Centre-Back; 28–35; ≤5.000.000 EUR; ≥2.000 phút; chân phải; loại CLB 31 | Không | 94 |
| budget_goalkeeper / 629773 | Goalkeeper; 20–30; ≤3.000.000 EUR; ≥1.800 phút; chân phải; loại CLB 1075 | Không | 47 |

Ngân sách dùng market value EUR để sàng lọc, không phải phí mua/lương/khả năng thương lượng. Không mặc định những hồ sơ vượt threshold có kỹ năng tốt hơn. GK/Defender chỉ được đánh giá **mức phù hợp hồ sơ bối cảnh**, chưa có evidence cho chất lượng phòng ngự/bắt bóng. No-results giữ kiểm thử cũ; không thêm nhãn giả để lấp pool rỗng.

Universe là toàn bộ hard-eligible pool: 173 cặp, 173 ID khác nhau trong bốn tình huống. Bao gồm cả ứng viên không nằm Top 5; nếu tương lai có vector zero vẫn giữ trong universe để phản ánh khả năng bỏ sót retrieval. Đóng băng danh sách ID và dataset hash trước chấm. Không thay universe sau khi xem metric.

## Quy trình annotation và chống vòng lặp tự xác nhận

1. Coordinator đóng băng scenario, rubric v1, K=5, relevant threshold ≥2, dataset/config/hash, candidate universe. Mô tả vai trò bổ sung phải có phiên bản trước khi chấm; không bịa nhu cầu chiến thuật chưa có.
2. Phát [annotation_template.csv](annotation_template.csv), [annotation_evidence.csv](annotation_evidence.csv), mô tả scenario và [rubric](relevance_rubric.md). Template có đủ 173 hàng **unlabeled**, không có tên assessor/điểm/timestamp giả. Evidence packet shuffle seed 11, không có method/rank/similarity; template sắp ID không theo model. Không đưa evaluation.json/Top 5 cho assessor trước khi khóa nhãn. Tên cầu thủ vẫn thấy: danh tiếng có thể gây bias, cần ghi nhận.
3. Dự kiến ít nhất hai người có năng lực phù hợp chấm độc lập; Day 11 **chưa có người được tuyển/chấm**. Ghi assessor ID giả danh, timestamp ISO 8601 có timezone, evidence truy xuất được kèm ngày/nguồn/phạm vi. Không lưu thông tin riêng tư của assessor trong repository công khai.
4. Thiếu bằng chứng quan trọng: giữ grade trống, `label_source=unlabeled`, notes nêu lý do abstain. Không diễn giải trống thành 0. Bổ sung hồ sơ/video/tackles/save metrics sau này cần nguồn và cutoff; không dùng Gemini tạo ground truth.
5. Khóa bản nhãn riêng từng assessor; kiểm đủ IDs, trùng hàng, nguồn, grade 0–3, evidence. `independent_human` là **khai báo provenance cần audit**, không phải chứng nhận tự động. SYNTHETIC nằm riêng, không trộn vào báo cáo relevance thật. Model-generated labels không được nhận như independent human.
6. Bất đồng: giữ nguyên nhãn gốc; dự kiến họp adjudication độc lập, ghi quyết định/nguồn trong phiên bản mới và chọn rõ assessor/adjudicator. Không trung bình nhãn hoặc chọn người chấm cho điểm cao nhất. Công cụ yêu cầu chọn một assessor và một nguồn; không tự gộp.
7. Chỉ sau nhãn đủ và audit nguồn mới tính relevance. Day 12 dự kiến kiểm quy trình/chất lượng annotation, agreement có điều kiện; Day 13 phân tích có giới hạn. Nếu không có labels, giữ trạng thái bị chặn cho relevance, không bịa số để đạt roadmap. Development/test queries và assessor phải tách khi tuning; bộ bốn demo hiện tại không dùng làm test độc lập sau tuning.

## Công thức và quy ước

Triển khai: [metrics.py](../../src/evaluation/metrics.py), [tests](../../tests/test_evaluation_protocol.py). K là số nguyên dương, không giảm K ngầm khi ít ứng viên. Input là thứ tự ID cuối cùng service đã trả, không sort lại bằng grade.

| Metric | Công thức / điều kiện |
|---|---|
| Precision@K | Số ID có grade ≥2 trong Top K / K. Mọi ID đã trả trong Top K phải được chấm; chỗ không trả tính là không thu được relevant. Chưa chấm không coi là 0. Empty ranking chỉ có P=0 khi universe không rỗng đã chấm đủ; còn lại null. |
| Recall@K | Hits / số relevant trong **toàn bộ eligible universe**. Chỉ tính khi mọi candidate có grade; không có relevant → null + lý do. Không gọi recall trên Top 5 đã chấm là recall catalogue. |
| NDCG@K | DCG = Σ(2^grade−1)/log2(rank+1), rank bắt đầu 1. IDCG lấy K grades cao nhất toàn universe; DCG/IDCG. Cần toàn universe có nhãn; IDCG=0 → null. Gain mũ là lựa chọn protocol ưu tiên grade cao, chưa được xác nhận là utility của CLB. |
| Label coverage | Số candidate có grade của assessor/nguồn đã chọn / số hard-eligible candidates. Pool rỗng → null. Không phải chất lượng nhãn. |
| Catalogue coverage | Số ID khác nhau được trả / hợp các hard-eligible pools của bốn demo, tính riêng method. Không dùng 4.112 làm mẫu số rồi gán nghĩa toàn thị trường. |
| Request coverage | Số demo trả ít nhất một người / số demo chạy. Không đo chất lượng hoặc nhu cầu thực. |
| Stability | Overlap@K = giao hai Top K / K cố định; `same_order` kiểm thứ tự ID. Một/both rỗng → null. Cùng shortlist không chứng minh relevance tốt. |

Ties: đánh giá thứ tự sản phẩm thực tế (score round12 → soft foot khi có → ID), không dùng nhãn phá hòa. Do đó không dùng trực tiếp cách trung bình tied scores mặc định của sklearn. Kiểm chứng toán học NDCG dùng `sklearn.metrics.ndcg_score` với **gain 2^grade−1** và score thứ tự không hòa, không nhầm grade tuyến tính với gain mũ. Tham khảo định nghĩa DCG/ideal normalization và hành vi ties trong [tài liệu chính thức sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html).

Duplicate ranked/candidate IDs, unknown/missing candidate IDs trong universe, grade âm/>3/float/bool/NaN/Inf, K sai, timestamp thiếu timezone, evidence rỗng, trộn assessor/provenance → lỗi rõ ràng. Một candidate chưa có nhãn → metric bị chặn tương ứng, không loại candidate đó để làm đẹp kết quả. Schema CSV phải đúng tám cột; `load_annotations` parse ID/grade rõ ràng, giữ trống thành None; gọi validation theo scenario trước đánh giá.

## Chạy lại và báo cáo

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day11 --output-dir reports/day11_recheck
```

POSIX: thay executable bằng `.venv/bin/python`. Output phải chưa tồn tại; runner từ chối ghi đè annotation. Không chạy pipeline thu thập/cleaning để audit, không gọi mạng/API. [audit.py](../../src/evaluation/audit.py) chỉ đọc snapshot; kết quả raw audit không thay thế xác minh nguồn ngoài. Requirements không đổi. Snapshot ngoài Git cần bàn giao riêng/hash match; clone HEAD hiện tại chưa đủ source.

Báo cáo phải gồm dataset/cutoff/hash, query/source, pool IDs, fit IDs/config, K/gain/threshold, provenance/label coverage, metric null/lý do, môi trường, version source, tính đúng filters/parity. Hiện 16 case-method có full response đúng Day 10 và repeat exact; không có nhãn độc lập nên **không macro-average relevance**, không CI/significance/claim chất lượng từ bốn demo. Latency Day 10 chỉ là kết quả lịch sử; Day 11 không đo benchmark mới.
