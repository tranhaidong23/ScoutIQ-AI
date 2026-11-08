# Day 11 — Audit findings

Kiểm tra mới 2026-11-03. Nguồn số liệu: [audit_evidence.json](audit_evidence.json), [evaluation.json](evaluation.json); mã audit đọc snapshot tại [audit.py](../../src/evaluation/audit.py). **V** = kiểm trực tiếp code/dữ liệu; **H** = kết quả cũ được đọc lại; **U** = chưa kiểm chứng; **P** = kế hoạch. Không gọi kiểm tra snapshot là xác minh tính đúng ngoài đời của Transfermarkt.

## Pipeline, thời gian và selection

| Thành phần | Bằng chứng / phát hiện | Hệ quả và trạng thái |
|---|---|---|
| Collection | [download_data.py](../../src/collection/download_data.py) tải URL mutable, skip file đã tồn tại; không pin phiên bản upstream. Audit hash 8 file snapshot; không tải lại. | V code/hash; U tái tải đúng snapshot và completeness nguồn. Bàn giao riêng dữ liệu có hash, không dựa vào URL hiện tại để tái tạo y nguyên. |
| Games/appearances | [clean_data.py](../../src/preprocessing/clean_data.py) lọc season 2025, games date ≤ cutoff. 9.515 games được chọn; 155.687 appearances join; 155.684 giữ sau lọc; ngày appearance không vượt cutoff, không lệch ngày game; 0 duplicate player/game sau lọc. | V snapshot. Chênh 3 hàng thuộc tổng điều kiện chất lượng, không tự gán nguyên nhân từng hàng. Event coverage/correctness bên ngoài chưa xác minh. |
| Aggregation | Audit độc lập chỉ đọc raw, tái sum phút/goals/assists và unique games cho 4.112 ID: 0 missing, 0 mismatch, max error 0 cho cả bốn cột. | V; không chạy script ghi đè processed. Không chứng minh mỗi event raw chính xác. |
| Valuations | Chọn latest **positive** value ≤ cutoff, không phải latest bất kể giá trị. 656.301 dòng raw; dates/values của candidates khớp nguồn, 0 sau cutoff/già hơn 365 ngày; 0 latest-any nonpositive trong candidates; 0 conflict giá positive cùng ngày trong phạm vi audit. | V snapshot. Quy tắc positive có thể gây selection bias trên nguồn khác; market value ≠ transfer fee, không skill ground truth. |
| Eligibility | [create_candidates.py](../../src/preprocessing/create_candidates.py), từ 8.322 integrated còn 4.112; tái dựng đủ điều kiện khớp chính xác ID. 4.198 integrated có <900 phút. | V. Ngưỡng phút tạo selection theo cơ hội thi đấu/availability, bỏ dự bị/tài năng mới/chấn thương; không suy rằng người bị loại kém hơn. Chưa chạy sensitivity 450/900/1.350 phút. |
| Tuổi ở boundary | Code tính floor(days/365.2425). Audit so với ngày sinh/lịch thấy **1/4.112 lệch**. Kiểm tra đọc bổ sung: `player_id=341429`, Davinson Sánchez, DOB 1996-06-12, tuổi lưu 29, tuổi theo lịch tại 2026-06-12 là 30. | V lỗi xấp xỉ tuổi; có thể ảnh hưởng age boundary hoặc context similarity. **Không sửa data/eligibility/scaler/ranking trong Day 11.** Cần issue/version dữ liệu và regression riêng khi được giao; chưa đo tác động toàn bộ truy vấn. |
| Metadata lịch sử | `players.current_club_*`, position/sub_position/foot/height từ snapshot hiện tại, không có valid-from/to tại cutoff. `club_name_verified` chỉ lookup khớp bảng clubs. | V cách join; U tính đúng thời điểm. Có rủi ro leakage metadata sau cutoff; không khẳng định đã xảy ra cho mọi hàng hoặc đã loại hết leakage. |

Audit tuổi tái lập bằng `calendar_age = cutoff.year − dob.year − ((dob.month,dob.day) > (cutoff.month,cutoff.day))`; so `features.age` sau join player_id với raw DOB. Count nằm ở `age_calendar_check` của JSON; không thay dữ liệu gốc.

## League/position bias và giới hạn representation

| Position | Integrated | Eligible | Tỷ lệ giữ |
|---|---:|---:|---:|
| Attack | 2.457 | 1.059 | 43,10% |
| Midfield | 2.423 | 1.204 | 49,69% |
| Defender | 2.740 | 1.523 | 55,58% |
| Goalkeeper | 701 | 326 | 46,50% |
| Missing | 1 | 0 | 0% |

V: mức giữ khác nhau theo vị trí, không phải bằng chứng phân biệt nhân quả hoặc quality. Mẫu không đại diện toàn bộ cầu thủ thế giới. Proxy giải dựa **CLB hiện tại**: GB1 393, ES1 376, IT1 371; thiếu 16; toàn bộ phân bố trong audit JSON. Đây không phải xác nhận league cầu thủ thi đấu tại cutoff. Games được chọn còn gồm domestic cup 982, international cup 281, national team 87, other 763, thiếu competition_type 364, bên cạnh domestic league 7.038. Vì vậy aggregate per90 là **hỗn hợp giải/đội tuyển**, chưa hiệu chỉnh strength/style/role/opponent. Không gọi bảng proxy là evaluation từng league đã làm.

| Module | Kiểm tra và bằng chứng | Hạn chế |
|---|---|---|
| [features](../../src/features/build_features.py) | V: validate 4.112×28, duplicate ID=0, per90 nhất quán; global position percentiles tồn tại. | Percentile dùng cả catalogue không được dùng trong similarity; nếu đưa vào train/test tương lai cần fit/reference riêng. Height outlier/metadata thiếu giữ nguyên, không impute kỹ năng. |
| [baseline](../../src/recommendation/baseline.py) | V: Attack/Midfield g90,a90+role; Defender age/minutes+role/foot; GK age/minutes+foot. Scaler fit 4.108 IDs, query holdout; validate finite, zero vectors, deterministic. | Context-only Defender/GK; age/minutes không phải năng lực phòng ngự. Không temporal split, không external validation. |
| [weighted](../../src/recommendation/weighted.py) | V: sqrt(weight), finite/nonnegative, kiểm all-zero; không market/log value/reliability/percentile/club làm skill. | Default là heuristic chưa tối ưu có nhãn. Không đếm raw goals + per90 + contributions đồng thời. g90/a90 vẫn có thể phụ thuộc; không tuyên bố độc lập tuyệt đối. H: [Day 6 correlations](../day6/evaluation.json), chưa tái chạy correlation mới. |
| [KNN](../../src/recommendation/knn.py) | V code + regression: cosine/brute cùng representation, neighbors trên hard pool, score 1−distance, toàn pool rồi phá hòa. | Không tự nhiên tốt hơn direct; H timing Day 7, không benchmark lại Day 11. |
| [constraints](../../src/recommendation/constraints.py) | V: hard trước rank, soft foot chỉ tie; query bị loại; constraints/đơn vị/missing fail rõ ràng. 16 live case-method thỏa pool oracle độc lập. | Tính đúng filter trên age/club metadata lưu trong snapshot chưa bằng tính đúng ngoài đời. |
| [explanation](../../src/recommendation/explainability.py), [comparison](../../src/recommendation/comparison.py) | V: evidence tách text, score/components/units/IDs kiểm consistency, relative zero/missing có null. Full response/comparison của 16 case mới khớp Day 10. | Evidence là giải thích phép tính, không causal attribution, xác suất chuyển nhượng hoặc tổng kết tốt hơn toàn diện. |
| [service](../../src/recommendation/service.py), [schemas](../../src/recommendation/schemas.py) | V: schema/domain checks, immutable fitted state, serialization finite; 16/16 parity/repeat exact. | Python local, chưa FastAPI/Neon/frontend/Gemini. JSON/schema pass không bảo đảm đúng thực tế hay chất lượng scouting. |

## Quyết định và việc còn lại

- Giữ engine/config/cutoff hiện hành để đối chiếu công bằng, không sửa tuổi âm thầm. Ghi rõ lỗi tuổi khi dùng age boundary; kế hoạch sửa có version và tác động cần nhiệm vụ riêng.
- Đóng băng rubric/universe; không dùng similarity/rank hoặc LLM để tạo labels. Bốn demo có selection bias, không đại diện nhu cầu người dùng thực. Chưa có expert labels nên toàn bộ relevance metrics thực bị chặn.
- Day 12 dự kiến kiểm annotation workflow, nhu cầu/nguồn assessor, evidence gaps và split; chỉ đo agreement nếu có nhãn thật. Không giả định công việc này đã diễn ra.
- MVP mới không auth; lịch sử anonymous vẫn cần server-side isolation theo browser session/token khi xây Day 14–23. Neon là PostgreSQL dùng chung hạ tầng, không phải quyền xem lịch sử mọi người. Gemini chỉ chuyển ý định thành schema/giải thích evidence, Python giữ ranking. Đây là quyết định phạm vi của người dùng, **chưa triển khai/kiểm thử**.
