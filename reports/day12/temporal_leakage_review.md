# Day 12 — Temporal leakage và tính hợp lệ của split

**Kết luận hiện hành: chưa có temporal split hợp lệ để đánh giá chất lượng out-of-time.** Không chia ngẫu nhiên các hàng features rồi gọi đó là temporal evaluation. Kiểm raw cutoff đã được chạy lại, nhưng event date khác thời điểm thông tin sẵn có.

Nguồn: [lineage đủ 28 cột](feature_lineage.csv), [audit mới](audit.json), [clean_data](../../src/preprocessing/clean_data.py), [features](../../src/features/build_features.py), [baseline](../../src/recommendation/baseline.py), [weighted](../../src/recommendation/weighted.py), [KNN](../../src/recommendation/knn.py), [service](../../src/recommendation/service.py).

| Nhóm thông tin | Đã kiểm chứng trên snapshot/code | Chưa chứng minh / rủi ro |
|---|---|---|
| games/appearances, counts, minutes, per90 | Season 2025, games ≤2026-06-12; không appearance date lệch/vượt cutoff trong tập join; sums/matches khớp | Không ingestion/publication timestamp hoặc lịch sử revision; dữ liệu nguồn có thể cập nhật sau sự kiện |
| DOB → age | DOB hợp lệ cho 4.112, tái tính công thức và calendar; 1 lỗi xấp xỉ có đề xuất | DOB trong snapshot không có record available-at; độ đúng thực tế chưa kiểm ngoài nguồn; tuổi chưa được sửa |
| position/sub_position/foot/club/name/image/height | Metadata từ snapshot hiện tại, có lookup và missing audit | Không valid_from/to, CLB/vai trò có thể khác tại cutoff; tên lookup “verified” không xử lý temporal leakage |
| valuation/date/freshness/value/log | Latest **positive** value ngày ≤cutoff, freshness 0–365, khớp raw | Publication/revision time không có; market value không fee hoặc label kỹ năng; lựa chọn positive gây selection |
| contributions/reliability | Tính được từ event aggregates, đơn vị/công thức rõ | Không thêm thông tin độc lập; reliability heuristic không phải độ tin cậy thống kê |
| position percentiles | Fit trên toàn candidates, có tie policy | Không được dùng như train-only feature; hiện không vào engine vector. Nếu dùng về sau phải recompute trên reference/train hợp lệ |
| scaler/one-hot/weights | Fit 4.108 reference IDs, loại 4 query; filters không refit; weights giữ nguyên | Query ID holdout không phải chronological holdout, chưa relevance labels; không chọn weights trên test/pilot rồi báo kết quả độc lập |

## Thiết kế temporal evaluation dự kiến, chưa thực hiện Day 13

1. Cần ít nhất snapshot/as-of metadata và event availability tại thời điểm T0, cùng định nghĩa nhiệm vụ/nhãn sau T0 có nguồn. Xác định horizon và population trước xem kết quả; không lấy thông tin T1 để dựng feature T0.
2. Rebuild aggregates/valuation/metadata as-of T0 từ nguồn đủ lịch sử; chỉ fit scaler/category/feature selection trên reference hoặc train T0. Nếu metadata không có lịch sử, loại khỏi phép đánh giá temporal hoặc ghi rõ blocked; không backfill bằng CLB hiện tại rồi coi là đúng.
3. Tách development/pilot queries và final assessment; theo dõi player/query overlap. Pilot chấm cùng 32 người không phải test set độc lập sau hiệu chỉnh rubric/weights.
4. Labels phải độc lập, có cutoff/phạm vi/evidence; chuyển nhượng thực tế cũng không tự động là nhãn kỹ năng hoặc fit. Không đánh giá GK bằng goals, không dùng market value như ground truth.
5. Tách chất lượng retrieval/filter/reproducibility, context relevance và football performance. Với dữ liệu hiện có chỉ đủ kiểm snapshot/contract và chuẩn bị annotation, không đủ khẳng định temporal predictive quality.

Đây là thiết kế và điều kiện cần cho công việc sau; Day 12 không tạo train/test mới, không refit/retune, không gọi Gemini hoặc xây FastAPI/Neon. Sửa tuổi có version sẽ cần tái kiểm feature/scaler/pools/ranking riêng nếu được phép.
