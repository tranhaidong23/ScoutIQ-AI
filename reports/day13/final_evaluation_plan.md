# Day 13 — Kế hoạch final evaluation và phần bị chặn

**Chưa có final evaluation được nghiệm thu.** Bốn scenario Day8–12 là demo đã dùng trong phát triển; 32 hồ sơ pilot dùng hiệu chỉnh quy trình/rubric, không đổi tên thành test độc lập sau khi xem kết quả. 173 cặp vẫn là universe của các demo, không đại diện tất cả nhu cầu CLB.

| Gate | Điều kiện cần | Hiện tại |
|---|---|---|
| Người chấm | Ít nhất hai assessor thật phù hợp phạm vi, review độc lập và blind protocol | Chưa có |
| Pilot | Nhãn gốc đã khóa, review abstain/uncertainty/bất đồng và rubric ambiguity | 32 pending |
| Final queries | Coordinator chọn nhu cầu/nguồn đại diện, chốt trước khi xem model outputs, lưu version/query hash | Chưa được cung cấp/phê duyệt |
| Dataset/rubric | Chốt snapshot/universe/K/methods/metric policies cùng nguồn evidence | Có baseline và rubric v1; final chưa khóa |
| P@K | Tất cả returned TopK được chấm cho từng assessor; K cố định, không fill missing0 | Chưa có nhãn |
| Recall/NDCG | Full eligible universe có grade, mẫu số relevant/IDCG hợp lệ | Pilot không đủ; không dùng subset làm ideal |
| Temporal | Metadata as-of/publication times, nhãn và split hợp lệ theo thời gian | Chưa có, không thay bằng random split |
| Báo cáo | Report per-scenario/per-assessor, coverage, abstention, undefined cases; không chọn assessor cho điểm cao nhất | Công cụ sẵn sàng, chưa có kết quả thật |

Sau pilot, mọi thay đổi rubric/evidence cần version mới và lưu nguồn quyết định. Khóa final queries trước scoring; tách calibration khỏi final, giữ pipeline/ranking cấu hình đã chọn trước khi xem final labels. Không tự chọn ngưỡng thành công hoặc suy chất lượng từ regression, overlap, coverage hay synthetic fixture. Nếu có đánh giá lại cùng demo, gọi đúng là đánh giá demo, không test độc lập.
