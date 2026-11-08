# Day 8 — Advanced Filtering & Search Constraints

Dữ liệu thật: 4.112 người, cutoff 2026-06-12; fit 4.108, loại 4 query.
20 legacy checks và 20 advanced requests đạt; direct/KNN cùng representation khớp full ranking.
Hard filters trước ranking. Soft foot chỉ phá hòa; similarity không phải skill/xác suất.

| Scenario | Position trước lọc | Sau hard | Trả Top K |
|---|---:|---:|---:|
| young_low_budget_striker | 1059 | 22 | 5 |
| creative_midfielder | 1204 | 10 | 5 |
| experienced_defender | 1523 | 94 | 5 |
| budget_goalkeeper | 326 | 47 | 5 |
| no_results | 1059 | 0 | 0 |

## Top 5 weighted (cấu hình giả thuyết Day 6, không khẳng định tối ưu)

### young_low_budget_striker — Harry Kane

Constraints: `{"position": "Attack", "min_age": 18.0, "max_age": 23.0, "max_budget_eur": 5000000.0, "min_minutes": 1200.0, "sub_positions": ["Centre-Forward"], "min_goals_per90": 0.3, "min_assists_per90": null, "preferred_foot": "left", "foot_mode": "soft", "excluded_club_ids": [27], "budget_unit": "EUR", "boundaries": "inclusive", "soft_preference_policy": "equal rounded cosine score only, then player_id", "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}`.

Status: ok; eligible: 22.

| Rank | ID | Tên | CLB | Tuổi | EUR | Score |
|---|---|---|---|---:|---:|---:|
| 1 | 1360186 | Barney Stewart | Falkirk FC | 22 | 1,000,000 | 0.956332 |
| 2 | 818445 | Milan Zonneveld | Sparta Rotterdam | 22 | 450,000 | 0.926601 |
| 3 | 467720 | Youssoufa Moukoko | FC Copenhagen | 21 | 5,000,000 | 0.915929 |
| 4 | 845568 | Marko Milovanović | FC Alverca | 22 | 2,500,000 | 0.890610 |
| 5 | 670987 | Tawanda Maswanhise | Motherwell FC | 23 | 5,000,000 | 0.883390 |

- **Barney Stewart**: goals_per90: 0.6293706293706294 (tham chiếu 1.2661439114391144; w=0.4); assists_per90: 0.1258741258741259 (tham chiếu 0.1660516605166051; w=0.4); sub_position: Centre-Forward (tham chiếu Centre-Forward; w=0.2). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu. Ràng buộc: tuổi=22; market value EUR=1000000.0; phút=1430; vai trò=Centre-Forward; chân=right; club_id=1191. Hiệu suất tấn công: goals/90=0.6293706293706294; assists/90=0.1258741258741259.
- **Milan Zonneveld**: goals_per90: 0.7505686125852918 (tham chiếu 1.2661439114391144; w=0.4); assists_per90: 0.2729340409401061 (tham chiếu 0.1660516605166051; w=0.4); sub_position: Centre-Forward (tham chiếu Centre-Forward; w=0.2). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu. Ràng buộc: tuổi=22; market value EUR=450000.0; phút=1319; vai trò=Centre-Forward; chân=right; club_id=468. Hiệu suất tấn công: goals/90=0.7505686125852918; assists/90=0.2729340409401061.
- **Youssoufa Moukoko**: goals_per90: 0.5674653215636822 (tham chiếu 1.2661439114391144; w=0.4); assists_per90: 0.1134930643127364 (tham chiếu 0.1660516605166051; w=0.4); sub_position: Centre-Forward (tham chiếu Centre-Forward; w=0.2). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu. Ràng buộc: tuổi=21; market value EUR=5000000.0; phút=1586; vai trò=Centre-Forward; chân=left; club_id=190. Hiệu suất tấn công: goals/90=0.5674653215636822; assists/90=0.1134930643127364.
- **Marko Milovanović**: goals_per90: 0.5276872964169381 (tham chiếu 1.2661439114391144; w=0.4); assists_per90: 0.1172638436482084 (tham chiếu 0.1660516605166051; w=0.4); sub_position: Centre-Forward (tham chiếu Centre-Forward; w=0.2). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu. Ràng buộc: tuổi=22; market value EUR=2500000.0; phút=1535; vai trò=Centre-Forward; chân=right; club_id=2521. Hiệu suất tấn công: goals/90=0.5276872964169381; assists/90=0.1172638436482084.
- **Tawanda Maswanhise**: goals_per90: 0.6245434623813002 (tham chiếu 1.2661439114391144; w=0.4); assists_per90: 0.0657414170927684 (tham chiếu 0.1660516605166051; w=0.4); sub_position: Centre-Forward (tham chiếu Centre-Forward; w=0.2). Chỉ mô tả ghi bàn/kiến tạo và vai trò; thiếu xG, pressing và bối cảnh giải đấu. Ràng buộc: tuổi=23; market value EUR=5000000.0; phút=2738; vai trò=Centre-Forward; chân=None; club_id=987. Hiệu suất tấn công: goals/90=0.6245434623813002; assists/90=0.0657414170927684.

### creative_midfielder — Hans Vanaken

Constraints: `{"position": "Midfield", "min_age": 20.0, "max_age": 29.0, "max_budget_eur": 10000000.0, "min_minutes": 1200.0, "sub_positions": ["Attacking Midfield"], "min_goals_per90": null, "min_assists_per90": 0.15, "preferred_foot": "left", "foot_mode": "hard", "excluded_club_ids": [2282], "budget_unit": "EUR", "boundaries": "inclusive", "soft_preference_policy": "equal rounded cosine score only, then player_id", "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}`.

Status: ok; eligible: 10.

| Rank | ID | Tên | CLB | Tuổi | EUR | Score |
|---|---|---|---|---:|---:|---:|
| 1 | 543302 | Jeppe Erenbjerg | Zulte Waregem | 26 | 4,000,000 | 0.922962 |
| 2 | 1175048 | Robin van Cruijsen | FC Volendam | 20 | 1,200,000 | 0.915103 |
| 3 | 652061 | Adam Karabec | AC Sparta Prague | 22 | 7,000,000 | 0.826067 |
| 4 | 896234 | Guillermo Balzi | APO Levadiakos Football Club | 24 | 1,000,000 | 0.700985 |
| 5 | 485672 | Elijah Just | Motherwell FC | 26 | 2,500,000 | 0.671222 |

- **Jeppe Erenbjerg**: goals_per90: 0.4214697406340058 (tham chiếu 0.2290076335877862; w=0.3); assists_per90: 0.1621037463976945 (tham chiếu 0.1335877862595419; w=0.5); sub_position: Attacking Midfield (tham chiếu Attacking Midfield; w=0.2). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự. Ràng buộc: tuổi=26; market value EUR=4000000.0; phút=2776; vai trò=Attacking Midfield; chân=left; club_id=3508. Hiệu suất tấn công: goals/90=0.4214697406340058; assists/90=0.1621037463976945.
- **Robin van Cruijsen**: goals_per90: 0.2535211267605634 (tham chiếu 0.2290076335877862; w=0.3); assists_per90: 0.1901408450704225 (tham chiếu 0.1335877862595419; w=0.5); sub_position: Attacking Midfield (tham chiếu Attacking Midfield; w=0.2). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự. Ràng buộc: tuổi=20; market value EUR=1200000.0; phút=1420; vai trò=Attacking Midfield; chân=left; club_id=724. Hiệu suất tấn công: goals/90=0.2535211267605634; assists/90=0.1901408450704225.
- **Adam Karabec**: goals_per90: 0.1929949964260185 (tham chiếu 0.2290076335877862; w=0.3); assists_per90: 0.1929949964260185 (tham chiếu 0.1335877862595419; w=0.5); sub_position: Attacking Midfield (tham chiếu Attacking Midfield; w=0.2). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự. Ràng buộc: tuổi=22; market value EUR=7000000.0; phút=1399; vai trò=Attacking Midfield; chân=left; club_id=197. Hiệu suất tấn công: goals/90=0.1929949964260185; assists/90=0.1929949964260185.
- **Guillermo Balzi**: goals_per90: 0.3280680437424058 (tham chiếu 0.2290076335877862; w=0.3); assists_per90: 0.3280680437424058 (tham chiếu 0.1335877862595419; w=0.5); sub_position: Attacking Midfield (tham chiếu Attacking Midfield; w=0.2). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự. Ràng buộc: tuổi=24; market value EUR=1000000.0; phút=1646; vai trò=Attacking Midfield; chân=left; club_id=2672. Hiệu suất tấn công: goals/90=0.3280680437424058; assists/90=0.3280680437424058.
- **Elijah Just**: goals_per90: 0.2629382303839733 (tham chiếu 0.2290076335877862; w=0.3); assists_per90: 0.3005008347245409 (tham chiếu 0.1335877862595419; w=0.5); sub_position: Attacking Midfield (tham chiếu Attacking Midfield; w=0.2). Chỉ mô tả đóng góp tấn công; thiếu chuyền bóng, kiểm soát và phòng ngự. Ràng buộc: tuổi=26; market value EUR=2500000.0; phút=2396; vai trò=Attacking Midfield; chân=left; club_id=987. Hiệu suất tấn công: goals/90=0.2629382303839733; assists/90=0.3005008347245409.

### experienced_defender — Virgil van Dijk

Constraints: `{"position": "Defender", "min_age": 28.0, "max_age": 35.0, "max_budget_eur": 5000000.0, "min_minutes": 2000.0, "sub_positions": ["Centre-Back"], "min_goals_per90": null, "min_assists_per90": null, "preferred_foot": "right", "foot_mode": "hard", "excluded_club_ids": [31], "budget_unit": "EUR", "boundaries": "inclusive", "soft_preference_policy": "equal rounded cosine score only, then player_id", "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}`.

Status: ok; eligible: 94.

| Rank | ID | Tên | CLB | Tuổi | EUR | Score |
|---|---|---|---|---:|---:|---:|
| 1 | 236168 | Brandon Mechele | Club Brugge KV | 33 | 2,800,000 | 0.999090 |
| 2 | 124502 | Matthias Ginter | SC Freiburg | 32 | 5,000,000 | 0.995862 |
| 3 | 244221 | Christian Burgess | Union Saint-Gilloise | 34 | 1,800,000 | 0.977334 |
| 4 | 187718 | Clinton Mata | Olympique Lyon | 33 | 2,500,000 | 0.969863 |
| 5 | 173504 | James Tarkowski | Everton FC | 33 | 5,000,000 | 0.960660 |

- **Brandon Mechele**: age: 33 (tham chiếu 34; w=0.2); minutes_played: 4783 (tham chiếu 4941; w=0.2); sub_position: Centre-Back (tham chiếu Centre-Back; w=0.4); foot: right (tham chiếu right; w=0.2). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự. Ràng buộc: tuổi=33; market value EUR=2800000.0; phút=4783; vai trò=Centre-Back; chân=right; club_id=2282.
- **Matthias Ginter**: age: 32 (tham chiếu 34; w=0.2); minutes_played: 4606 (tham chiếu 4941; w=0.2); sub_position: Centre-Back (tham chiếu Centre-Back; w=0.4); foot: right (tham chiếu right; w=0.2). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự. Ràng buộc: tuổi=32; market value EUR=5000000.0; phút=4606; vai trò=Centre-Back; chân=right; club_id=60.
- **Christian Burgess**: age: 34 (tham chiếu 34; w=0.2); minutes_played: 3957 (tham chiếu 4941; w=0.2); sub_position: Centre-Back (tham chiếu Centre-Back; w=0.4); foot: right (tham chiếu right; w=0.2). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự. Ràng buộc: tuổi=34; market value EUR=1800000.0; phút=3957; vai trò=Centre-Back; chân=right; club_id=3948.
- **Clinton Mata**: age: 33 (tham chiếu 34; w=0.2); minutes_played: 3742 (tham chiếu 4941; w=0.2); sub_position: Centre-Back (tham chiếu Centre-Back; w=0.4); foot: right (tham chiếu right; w=0.2). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự. Ràng buộc: tuổi=33; market value EUR=2500000.0; phút=3742; vai trò=Centre-Back; chân=right; club_id=1041.
- **James Tarkowski**: age: 33 (tham chiếu 34; w=0.2); minutes_played: 3630 (tham chiếu 4941; w=0.2); sub_position: Centre-Back (tham chiếu Centre-Back; w=0.4); foot: right (tham chiếu right; w=0.2). Chỉ tương đồng hồ sơ tuổi/thời lượng/vai trò/chân thuận; không đo năng lực phòng ngự. Ràng buộc: tuổi=33; market value EUR=5000000.0; phút=3630; vai trò=Centre-Back; chân=right; club_id=29.

### budget_goalkeeper — Lukas Hornicek

Constraints: `{"position": "Goalkeeper", "min_age": 20.0, "max_age": 30.0, "max_budget_eur": 3000000.0, "min_minutes": 1800.0, "sub_positions": ["Goalkeeper"], "min_goals_per90": null, "min_assists_per90": null, "preferred_foot": "right", "foot_mode": "hard", "excluded_club_ids": [1075], "budget_unit": "EUR", "boundaries": "inclusive", "soft_preference_policy": "equal rounded cosine score only, then player_id", "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}`.

Status: ok; eligible: 47.

| Rank | ID | Tên | CLB | Tuổi | EUR | Score |
|---|---|---|---|---:|---:|---:|
| 1 | 464373 | Elías Ólafsson | FC Midtjylland | 26 | 3,000,000 | 0.863745 |
| 2 | 403564 | Jon McCracken | Dundee FC | 26 | 500,000 | 0.863250 |
| 3 | 338665 | Brent Gabriël | Zulte Waregem | 27 | 1,000,000 | 0.860127 |
| 4 | 337290 | Shamal George | St. Mirren FC | 28 | 300,000 | 0.823090 |
| 5 | 360338 | Marcos Peano | RAAL La Louvière | 27 | 2,000,000 | 0.812324 |

- **Elías Ólafsson**: age: 26 (tham chiếu 23; w=0.25); minutes_played: 3182 (tham chiếu 4970; w=0.25); foot: right (tham chiếu right; w=0.5). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng. Ràng buộc: tuổi=26; market value EUR=3000000.0; phút=3182; vai trò=Goalkeeper; chân=right; club_id=865.
- **Jon McCracken**: age: 26 (tham chiếu 23; w=0.25); minutes_played: 3180 (tham chiếu 4970; w=0.25); foot: right (tham chiếu right; w=0.5). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng. Ràng buộc: tuổi=26; market value EUR=500000.0; phút=3180; vai trò=Goalkeeper; chân=right; club_id=511.
- **Brent Gabriël**: age: 27 (tham chiếu 23; w=0.25); minutes_played: 3240 (tham chiếu 4970; w=0.25); foot: right (tham chiếu right; w=0.5). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng. Ràng buộc: tuổi=27; market value EUR=1000000.0; phút=3240; vai trò=Goalkeeper; chân=right; club_id=3508.
- **Shamal George**: age: 28 (tham chiếu 23; w=0.25); minutes_played: 3218 (tham chiếu 4970; w=0.25); foot: right (tham chiếu right; w=0.5). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng. Ràng buộc: tuổi=28; market value EUR=300000.0; phút=3218; vai trò=Goalkeeper; chân=right; club_id=465.
- **Marcos Peano**: age: 27 (tham chiếu 23; w=0.25); minutes_played: 3060 (tham chiếu 4970; w=0.25); foot: right (tham chiếu right; w=0.5). Chỉ tương đồng hồ sơ tuổi/thời lượng/chân thuận; không đo bắt bóng, không dùng bàn thắng. Ràng buộc: tuổi=27; market value EUR=2000000.0; phút=3060; vai trò=Goalkeeper; chân=right; club_id=3901.

### no_results — Harry Kane

Constraints: `{"position": "Attack", "min_age": 18.0, "max_age": 23.0, "max_budget_eur": 0.0, "min_minutes": 1200.0, "sub_positions": ["Centre-Forward"], "min_goals_per90": 0.3, "min_assists_per90": null, "preferred_foot": "left", "foot_mode": "hard", "excluded_club_ids": [], "budget_unit": "EUR", "boundaries": "inclusive", "soft_preference_policy": "equal rounded cosine score only, then player_id", "missing_policy": "active hard constraint: unknown fails; soft foot: no bonus"}`.

Status: no_candidates; eligible: 0.

| Rank | ID | Tên | CLB | Tuổi | EUR | Score |
|---|---|---|---|---:|---:|---:|


## Giới hạn

Không có nhãn relevance, temporal evaluation hoặc app web. Không đo latency Day 8.
Các ngưỡng là kịch bản kiểm hành vi. Missing metadata/CLB lịch sử và snapshot ngoài Git vẫn cần xử lý.
Day 9 dự kiến chuẩn hóa explanation và dữ liệu so sánh, không bịa chỉ số GK/Defender.
