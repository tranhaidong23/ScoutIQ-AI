# Day 13 — Quyết định correction: DEFERRED

Proposal gốc: [Day12 correction](../day12/correction_proposal.json). **PROPOSED, applied=false, approval=null**, byte/hash gốc được bảo toàn. ID341429 có snapshot age29, calendar age30 theo DOB1996-06-12 và cutoff2026-06-12.

Phép tính calendar đã được kiểm bằng tests Day12, gồm chính sách sinh29/2: kỷ niệm1/3 ở năm không nhuận. Đây là chính sách kỹ thuật đề xuất; chưa có phê duyệt áp dụng hoặc xác minh DOB độc lập bên ngoài snapshot trong Day13. Việc người dùng giao Day13 không tự thay các gate của proposal.

Quyết định: giữ baseline; chưa tạo snapshot sửa tuổi, chưa promote service, chưa đo tác động trên dữ liệu sửa. Không tuyên bố tác động bằng0. Cần bằng chứng DOB có nguồn/thời điểm, review chính sách29/2, cho phép áp dụng rõ ràng, output version mới với parent hashes, kiểm IDs/schema/per90 rồi so filters/scaler/ranking trước quyết định promote. Bảo toàn raw và canonical snapshot.
