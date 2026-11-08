# Day 13 — Nhập pilot và coordinator review

Chưa có người thật chấm. Không tạo danh tính giả hoặc nhãn thay người chấm. Registry chỉ là khai báo; coordinator phải xác minh độc lập ngoài code.

1. Phát bản sao template/evidence/rubric Day12 cùng version cho từng assessor thật, ẩn ranking và nhãn người khác. Không tự gửi lời mời từ công cụ này.
2. Dùng ID giả danh, không email/tên thật; registry theo schema Day12. Điền assessor ID cả ở các hàng pending của bản sao trước khi gộp file. Có thể nộp thiếu hàng; báo cáo ghi rõ missing, không coi là pending hoặc grade0.
3. Mỗi cặp scenario/player/assessor chỉ được có một bản ghi trong toàn bộ lần nhập. Nộp nhiều file có hàng trùng sẽ lỗi, không chọn bản cuối âm thầm. Giữ bản gốc riêng, khóa hash sau khi nhận.
4. Lưu input và output thật ngoài repo. Công cụ không sao chép free text nhưng output vẫn chứa ID giả danh, grades và provenance flags. Người điều phối giữ bảng định danh và bằng chứng review trong kho riêng.
5. Xem coverage theo assessor/scenario và review_queue. Review các mục thiếu bằng chứng, abstain, uncertainty cao, provenance chưa xác nhận và grade bất đồng. Một common item cũng đủ đưa bất đồng vào queue, chưa đủ tính agreement.
6. Adjudication cần người review, ghi ID hàng gốc, hash bản chấm, lý do, nguồn bổ sung, người quyết định và thời điểm trong phiên bản riêng. Không sửa original grade để tăng agreement. Day13 chỉ xuất queue OPEN với adjudicated_grade=null, chưa có importer adjudication.

Từ repo root, chạy mặc định khi chưa có nhãn vào thư mục **chưa tồn tại**:

```powershell
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day13 --output-dir reports/day13_recheck
```

Khi có file thật (thay đường dẫn ví dụ bằng đường dẫn riêng có thật):

```powershell
.\.venv\Scripts\python.exe -B -m src.evaluation.run_day13 --annotations C:\PrivateScoutIQ\assessor_a.csv C:\PrivateScoutIQ\assessor_b.csv --registry C:\PrivateScoutIQ\registry.json --output-dir C:\PrivateScoutIQ\review_run_01
```

Không tự tạo các file mẫu được nhắc trong lệnh. Cần cả --annotations và --registry; path trùng, CSV rỗng, schema sai hoặc snapshot lệch bị từ chối trước khi tạo output. Output có sẵn luôn bị từ chối. Không tự copy registry và ghi chú riêng vào Git.

Agreement chỉ trên các common graded items của hai assessor được khai báo độc lập và đã review, cùng scenario/scope/version. Constant labels có expected disagreement=0 giữ kappa null; missing không điền0. Không gộp GK context với attack-output quality. Độ phủ pilot không đại diện catalogue; ít common items có selection bias.
