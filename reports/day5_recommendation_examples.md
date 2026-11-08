# Day 5 — Ví dụ chạy baseline trên dữ liệu thật

Tự sinh bởi `python -B -m src.recommendation.run_day5`. Đây là kiểm tra hành vi, chưa phải đánh giá chất lượng scouting.

Input SHA-256: `425aeb9cf0f7ed13077bf31c6b5326ad02ef010253a45a043c92eabfab4ca6b0`. Cutoff: 2026-06-12. Fit trên 4108 cầu thủ, loại 4 tham chiếu trước khi fit.

## attack_budget_30m

Tham chiếu: **Harry Kane** (ID 132098).

Bộ lọc: `{"position": "Attack", "min_age": 18.0, "max_age": 29.0, "max_budget_eur": 30000000.0, "min_minutes": 1800.0}`.

Ứng viên sau lọc/loại bản thân: 349; trạng thái: `ok`.

| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | 929090 | Franculino | FC Midtjylland | Attack | 21 | 2060 | 22,000,000 | 0.991291 |
| 2 | 424784 | Luis Suárez | Sporting CP | Attack | 28 | 3767 | 30,000,000 | 0.976606 |
| 3 | 333647 | Jonathan Burkardt | Eintracht Frankfurt | Attack | 25 | 1882 | 30,000,000 | 0.946797 |
| 4 | 524590 | Júnior Brumado | FC Midtjylland | Attack | 27 | 1992 | 800,000 | 0.944356 |
| 5 | 315867 | Gianluca Scamacca | Atalanta BC | Attack | 27 | 2016 | 25,000,000 | 0.938443 |

- **Franculino:** goals_per90: 0.9174757281553398 (tham chiếu 1.2661439114391144); assists_per90: 0.1310679611650485 (tham chiếu 0.1660516605166051); sub_position: Centre-Forward (tham chiếu Centre-Forward). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- **Luis Suárez:** goals_per90: 0.8123174940270772 (tham chiếu 1.2661439114391144); assists_per90: 0.2150252190071675 (tham chiếu 0.1660516605166051); sub_position: Centre-Forward (tham chiếu Centre-Forward). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- **Jonathan Burkardt:** goals_per90: 0.7173219978746015 (tham chiếu 1.2661439114391144); assists_per90: 0.0956429330499468 (tham chiếu 0.1660516605166051); sub_position: Centre-Forward (tham chiếu Centre-Forward). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- **Júnior Brumado:** goals_per90: 0.7228915662650602 (tham chiếu 1.2661439114391144); assists_per90: 0.0903614457831325 (tham chiếu 0.1660516605166051); sub_position: Centre-Forward (tham chiếu Centre-Forward). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- **Gianluca Scamacca:** goals_per90: 0.625 (tham chiếu 1.2661439114391144); assists_per90: 0.1339285714285714 (tham chiếu 0.1660516605166051); sub_position: Centre-Forward (tham chiếu Centre-Forward). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.

- Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.
- Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.

## midfield_budget_15m

Tham chiếu: **Hans Vanaken** (ID 137576).

Bộ lọc: `{"position": "Midfield", "min_age": 20.0, "max_age": 30.0, "max_budget_eur": 15000000.0, "min_minutes": 1800.0}`.

Ứng viên sau lọc/loại bản thân: 405; trạng thái: `ok`.

| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | 577455 | Ringo Meerveld | SC Heerenveen | Midfield | 23 | 2689 | 5,000,000 | 0.999739 |
| 2 | 293200 | Nikola Vlašić | Torino FC | Midfield | 28 | 3350 | 10,000,000 | 0.998565 |
| 3 | 507341 | Fabian Rieder | Stade Rennais FC | Midfield | 24 | 2530 | 12,000,000 | 0.994785 |
| 4 | 441216 | Thijs Oosting | PEC Zwolle | Midfield | 26 | 2834 | 900,000 | 0.993635 |
| 5 | 345577 | Carlo Holse | Samsunspor | Midfield | 27 | 2640 | 7,000,000 | 0.986995 |

- **Ringo Meerveld:** goals_per90: 0.2342878393454815 (tham chiếu 0.2290076335877862); assists_per90: 0.1338787653402752 (tham chiếu 0.1335877862595419); sub_position: Attacking Midfield (tham chiếu Attacking Midfield). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.
- **Nikola Vlašić:** goals_per90: 0.2417910447761194 (tham chiếu 0.2290076335877862); assists_per90: 0.1343283582089552 (tham chiếu 0.1335877862595419); sub_position: Attacking Midfield (tham chiếu Attacking Midfield). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.
- **Fabian Rieder:** goals_per90: 0.2134387351778656 (tham chiếu 0.2290076335877862); assists_per90: 0.1422924901185771 (tham chiếu 0.1335877862595419); sub_position: Attacking Midfield (tham chiếu Attacking Midfield). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.
- **Thijs Oosting:** goals_per90: 0.2540578687367678 (tham chiếu 0.2290076335877862); assists_per90: 0.1270289343683839 (tham chiếu 0.1335877862595419); sub_position: Attacking Midfield (tham chiếu Attacking Midfield). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.
- **Carlo Holse:** goals_per90: 0.2727272727272727 (tham chiếu 0.2290076335877862); assists_per90: 0.1363636363636363 (tham chiếu 0.1335877862595419); sub_position: Attacking Midfield (tham chiếu Attacking Midfield). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.

- Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự.
- Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.
- Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.

## defender_context_15m

Tham chiếu: **Virgil van Dijk** (ID 139208).

Bộ lọc: `{"position": "Defender", "min_age": 22.0, "max_age": 32.0, "max_budget_eur": 15000000.0, "min_minutes": 2000.0}`.

Ứng viên sau lọc/loại bản thân: 512; trạng thái: `ok`.

| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | 124502 | Matthias Ginter | SC Freiburg | Defender | 32 | 4606 | 5,000,000 | 0.996192 |
| 2 | 256448 | Gianluca Mancini | Associazione Sportiva Roma | Defender | 30 | 3693 | 15,000,000 | 0.967314 |
| 3 | 243028 | Jan Bednarek | FC Porto | Defender | 30 | 3588 | 11,000,000 | 0.961436 |
| 4 | 328784 | Robin Koch | Eintracht Frankfurt | Defender | 29 | 3755 | 10,000,000 | 0.953971 |
| 5 | 277384 | Martin Valjent | RCD Mallorca | Defender | 30 | 3362 | 3,000,000 | 0.942175 |

- **Matthias Ginter:** age: 32 (tham chiếu 34); minutes_played: 4606 (tham chiếu 4941); sub_position: Centre-Back (tham chiếu Centre-Back); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.
- **Gianluca Mancini:** age: 30 (tham chiếu 34); minutes_played: 3693 (tham chiếu 4941); sub_position: Centre-Back (tham chiếu Centre-Back); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.
- **Jan Bednarek:** age: 30 (tham chiếu 34); minutes_played: 3588 (tham chiếu 4941); sub_position: Centre-Back (tham chiếu Centre-Back); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.
- **Robin Koch:** age: 29 (tham chiếu 34); minutes_played: 3755 (tham chiếu 4941); sub_position: Centre-Back (tham chiếu Centre-Back); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.
- **Martin Valjent:** age: 30 (tham chiếu 34); minutes_played: 3362 (tham chiếu 4941); sub_position: Centre-Back (tham chiếu Centre-Back); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.

- Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự.
- Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.
- Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.

## goalkeeper_context_10m

Tham chiếu: **Lukas Hornicek** (ID 629773).

Bộ lọc: `{"position": "Goalkeeper", "min_age": 20.0, "max_age": 30.0, "max_budget_eur": 10000000.0, "min_minutes": 1800.0}`.

Ứng viên sau lọc/loại bản thân: 107; trạng thái: `ok`.

| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | 426849 | Jari De Busser | Go Ahead Eagles | Goalkeeper | 26 | 4200 | 4,000,000 | 0.982356 |
| 2 | 550829 | Matej Kovar | PSV Eindhoven | Goalkeeper | 26 | 4050 | 8,000,000 | 0.979647 |
| 3 | 361256 | Berke Özer | LOSC Lille | Goalkeeper | 26 | 4035 | 10,000,000 | 0.979264 |
| 4 | 370997 | Dominik Kotarski | FC Copenhagen | Goalkeeper | 26 | 3690 | 5,000,000 | 0.962188 |
| 5 | 463527 | Kjell Scherpen | Union Saint-Gilloise | Goalkeeper | 26 | 3555 | 8,000,000 | 0.949399 |

- **Jari De Busser:** age: 26 (tham chiếu 23); minutes_played: 4200 (tham chiếu 4970); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.
- **Matej Kovar:** age: 26 (tham chiếu 23); minutes_played: 4050 (tham chiếu 4970); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.
- **Berke Özer:** age: 26 (tham chiếu 23); minutes_played: 4035 (tham chiếu 4970); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.
- **Dominik Kotarski:** age: 26 (tham chiếu 23); minutes_played: 3690 (tham chiếu 4970); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.
- **Kjell Scherpen:** age: 26 (tham chiếu 23); minutes_played: 3555 (tham chiếu 4970); foot: right (tham chiếu right). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.

- Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng.
- Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.
- Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.

## empty_budget

Tham chiếu: **Harry Kane** (ID 132098).

Bộ lọc: `{"position": "Attack", "min_age": 18.0, "max_age": 29.0, "max_budget_eur": 0.0, "min_minutes": 1800.0}`.

Ứng viên sau lọc/loại bản thân: 0; trạng thái: `no_candidates`.

| Hạng | ID | Cầu thủ | CLB | Vị trí | Tuổi | Phút | Market value EUR | Cosine |
|---|---|---|---|---|---:|---:|---:|---:|


- Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu.
- Similarity là cosine trong không gian đã chuẩn hóa, không phải xác suất chuyển nhượng hoặc điểm kỹ năng.
- Market value là ước tính lịch sử; CLB là metadata hiện có, chưa xác minh đúng CLB tại cutoff.

