# -*- coding: utf-8 -*-
"""
PHÁT TÀI BANK - Chuyên Sâu 77 Ý Định BANKING77 (Hugging Face / PolyAI / MTEB)
File: ai_backend/banking77_hf_expert.py

Mô tả:
  Cung cấp cơ sở tri thức nghiệp vụ ngân hàng chuyên sâu (In-depth Banking Knowledge Base)
  cho ĐỦ 77 Ý ĐỊNH CHUẨN QUỐC TẾ trong tập dữ liệu BANKING77 (Hugging Face Hub).
  Mỗi ý định đều được chuẩn hóa theo quy trình ngân hàng số thực tế:
    - 📌 Ý nghĩa nghiệp vụ & Mã định danh Hugging Face
    - 🔢 Quy trình xử lý chuyên sâu từng bước (1️⃣ -> 4️⃣)
    - ⏱️ Thời gian giải quyết cam kết (SLA) & Hạn mức
    - 🛡️ Biện pháp an toàn & Phòng ngừa rủi ro
    - 📞 Kênh hỗ trợ chuyên trách (Hotline 24/7: 1900-8888)
"""

# Phân loại 77 ý định BANKING77 theo 6 nhóm nghiệp vụ chính
INTENT_CATEGORIES = {
    "cards_pin": [
        "activate_my_card", "card_about_to_expire", "card_acceptance", "card_arrival",
        "card_delivery_estimate", "card_linking", "card_not_working", "card_payment_fee_charged",
        "card_payment_not_recognised", "card_payment_wrong_exchange_rate", "card_swallowed",
        "change_pin", "compromised_card", "contactless_not_working", "declined_card_payment",
        "get_disposable_virtual_card", "get_physical_card", "getting_spare_card", "getting_virtual_card",
        "lost_or_stolen_card", "order_physical_card", "pending_card_payment", "pin_blocked",
        "reverted_card_payment?", "virtual_card_not_working", "visa_or_mastercard", "disposable_card_limits"
    ],
    "transfers_payments": [
        "beneficiary_not_allowed", "cancel_transfer", "declined_transfer", "failed_transfer",
        "pending_transfer", "receiving_money", "Refund_not_showing_up", "request_refund",
        "transaction_charged_twice", "transfer_fee_charged", "transfer_into_account",
        "transfer_not_received_by_recipient", "transfer_timing", "direct_debit_payment_not_recognised",
        "extra_charge_on_statement"
    ],
    "topup_balance": [
        "automatic_top_up", "balance_not_updated_after_bank_transfer",
        "balance_not_updated_after_cheque_or_cash_deposit", "pending_top_up",
        "top_up_by_bank_transfer_charge", "top_up_by_card_charge", "top_up_by_cash_or_cheque",
        "top_up_failed", "top_up_limits", "top_up_reverted", "topping_up_by_card", "verify_top_up"
    ],
    "atm_cash": [
        "atm_support", "cash_withdrawal_charge", "cash_withdrawal_not_recognised",
        "declined_cash_withdrawal", "pending_cash_withdrawal", "wrong_amount_of_cash_received",
        "wrong_exchange_rate_for_cash_withdrawal"
    ],
    "account_identity": [
        "age_limit", "edit_personal_details", "lost_or_stolen_phone", "passcode_forgotten",
        "terminate_account", "unable_to_verify_identity", "verify_my_identity",
        "verify_source_of_funds", "why_verify_identity"
    ],
    "currency_international": [
        "country_support", "exchange_charge", "exchange_rate", "exchange_via_app",
        "fiat_currency_support", "supported_cards_and_currencies", "apple_pay_or_google_pay"
    ]
}

# Metadata chi tiết cho từng Intent: Tiêu đề tiếng Việt, Nhóm nghiệp vụ, SLA cam kết
BANKING77_METADATA = {
    "activate_my_card": {"title": "Kích Hoạt Thẻ ATM Mới", "category": "Quản lý Thẻ & PIN", "sla": "Tức thì (Online 24/7)"},
    "age_limit": {"title": "Độ Tuổi Quy Định Sử Dụng Dịch Vụ", "category": "Tài Khoản & Định Danh", "sla": "Áp dụng ngay"},
    "apple_pay_or_google_pay": {"title": "Liên Kết Apple Pay / Google Wallet", "category": "Ngoại Tệ & Ví Điện Tử", "sla": "1 - 2 phút"},
    "atm_support": {"title": "Hỗ Trợ Giao Dịch Cây ATM", "category": "ATM & Tiền Mặt", "sla": "24/7 Toàn quốc"},
    "automatic_top_up": {"title": "Cài Đặt Nạp Tiền Tự Động Định Kỳ", "category": "Nạp Tiền & Số Dư", "sla": "Thiết lập 1 phút"},
    "balance_not_updated_after_bank_transfer": {"title": "Chưa Cập Nhật Số Dư Sau Chuyển Khoản", "category": "Nạp Tiền & Số Dư", "sla": "Tối đa 30 phút"},
    "balance_not_updated_after_cheque_or_cash_deposit": {"title": "Chưa Cập Nhật Số Dư Sau Nộp Tiền Mặt/Séc", "category": "Nạp Tiền & Số Dư", "sla": "2 - 4 giờ làm việc"},
    "beneficiary_not_allowed": {"title": "Người Thụ Hưởng Bị Giới Hạn/Không Hợp Lệ", "category": "Chuyển Tiền & Thanh Toán", "sla": "Kiểm tra ngay"},
    "cancel_transfer": {"title": "Hủy Lệnh Chuyển Tiền Đã Gửi", "category": "Chuyển Tiền & Thanh Toán", "sla": "Trước khi xử lý"},
    "card_about_to_expire": {"title": "Thẻ Sắp Hết Hạn & Gia Hạn Thẻ", "category": "Quản lý Thẻ & PIN", "sla": "3 - 5 ngày làm việc"},
    "card_acceptance": {"title": "Phạm Vi Chấp Nhận Thẻ", "category": "Quản lý Thẻ & PIN", "sla": "Toàn cầu"},
    "card_arrival": {"title": "Theo Dõi & Tra Cứu Phát Thẻ Vật Lý", "category": "Quản lý Thẻ & PIN", "sla": "3 - 5 ngày làm việc"},
    "card_delivery_estimate": {"title": "Thời Gian Giao Thẻ Tận Nhà Dự Kiến", "category": "Quản lý Thẻ & PIN", "sla": "2 - 5 ngày làm việc"},
    "card_linking": {"title": "Liên Kết Thẻ Với Tài Khoản & Ví", "category": "Quản lý Thẻ & PIN", "sla": "Tức thì (< 30s)"},
    "card_not_working": {"title": "Xử Lý Lỗi Thẻ Không Hoạt Động (Lỗi Chip/Dải Từ)", "category": "Quản lý Thẻ & PIN", "sla": "Đổi thẻ 24h"},
    "card_payment_fee_charged": {"title": "Biểu Phí Thanh Toán Thẻ", "category": "Quản lý Thẻ & PIN", "sla": "Miễn phí 100%"},
    "card_payment_not_recognised": {"title": "Giao Dịch Thẻ Lạ / Nghi Ngờ Gian Lận", "category": "Quản lý Thẻ & PIN", "sla": "Khóa ngay & Tra soát 7 ngày"},
    "card_payment_wrong_exchange_rate": {"title": "Sai Lệch Tỷ Giá Khi Quẹt Thẻ Ngoại Tệ", "category": "Quản lý Thẻ & PIN", "sla": "Tra soát 3 - 5 ngày"},
    "card_swallowed": {"title": "Xử Lý Sự Cố Cây ATM Nuốt Thẻ", "category": "Quản lý Thẻ & PIN", "sla": "Trả thẻ trong 3 ngày"},
    "cash_withdrawal_charge": {"title": "Biểu Phí Rút Tiền Mặt ATM", "category": "ATM & Tiền Mặt", "sla": "Miễn phí nội mạng"},
    "cash_withdrawal_not_recognised": {"title": "Giao Dịch Rút Tiền ATM Bất Thường", "category": "ATM & Tiền Mặt", "sla": "Tra soát 5 ngày"},
    "change_pin": {"title": "Đổi Mã PIN Thẻ An Toàn", "category": "Quản lý Thẻ & PIN", "sla": "Tức thì"},
    "compromised_card": {"title": "Thẻ Bị Lộ Thông Tin Bảo Mật / Bị Hack", "category": "Quản lý Thẻ & PIN", "sla": "Khóa thẻ tức thì (< 3s)"},
    "contactless_not_working": {"title": "Lỗi Thanh Toán Chạm Không Tiếp Xúc (Contactless)", "category": "Quản lý Thẻ & PIN", "sla": "Kiểm tra cài đặt"},
    "country_support": {"title": "Danh Sách Quốc Gia Được Hỗ Trợ Giao Dịch", "category": "Ngoại Tệ & Quốc Tế", "sla": "Hơn 200 quốc gia"},
    "declined_card_payment": {"title": "Xử Lý Lỗi Thanh Toán Thẻ Bị Từ Chối", "category": "Quản lý Thẻ & PIN", "sla": "Kiểm tra ngay"},
    "declined_cash_withdrawal": {"title": "Lỗi Rút Tiền Mặt ATM Bị Từ Chối", "category": "ATM & Tiền Mặt", "sla": "Kiểm tra hạn mức"},
    "declined_transfer": {"title": "Lỗi Lệnh Chuyển Tiền Bị Từ Chối", "category": "Chuyển Tiền & Thanh Toán", "sla": "Kiểm tra số dư/OTP"},
    "direct_debit_payment_not_recognised": {"title": "Khoản Trích Nợ Tự Động (Direct Debit) Lạ", "category": "Chuyển Tiền & Thanh Toán", "sla": "Hủy trong 24h"},
    "disposable_card_limits": {"title": "Hạn Mức Thẻ Ảo Dùng Một Lần", "category": "Quản lý Thẻ & PIN", "sla": "Tối đa 50tr/giao dịch"},
    "edit_personal_details": {"title": "Cập Nhật Thông Tin Cá Nhân & eKYC", "category": "Tài Khoản & Định Danh", "sla": "Online trong 5 phút"},
    "exchange_charge": {"title": "Phí Chuyển Đổi Ngoại Tệ", "category": "Ngoại Tệ & Quốc Tế", "sla": "1.2% - 1.5%"},
    "exchange_rate": {"title": "Tra Cứu Bảng Tỷ Giá Ngoại Tệ Thời Gian Thực", "category": "Ngoại Tệ & Quốc Tế", "sla": "Realtime từng phút"},
    "exchange_via_app": {"title": "Quy Đổi Ngoại Tệ Trực Tuyến Qua Ứng Dụng", "category": "Ngoại Tệ & Quốc Tế", "sla": "Tức thì (Giao dịch 24/7)"},
    "extra_charge_on_statement": {"title": "Tra Soát Khoản Phí Lạ Trên Sao Kê", "category": "Chuyển Tiền & Thanh Toán", "sla": "Tra soát 3 - 5 ngày"},
    "failed_transfer": {"title": "Chuyển Tiền Thất Bại Nhưng Bị Trừ Tiền", "category": "Chuyển Tiền & Thanh Toán", "sla": "Hoàn tiền sau 24h - 48h"},
    "fiat_currency_support": {"title": "Các Đồng Tiền Pháp Định Được Hỗ Trợ", "category": "Ngoại Tệ & Quốc Tế", "sla": "25 loại ngoại tệ"},
    "get_disposable_virtual_card": {"title": "Tạo Thẻ Ảo Dùng 1 Lần (Bảo Mật Mua Sắm Online)", "category": "Quản lý Thẻ & PIN", "sla": "Cấp ngay trong 10s"},
    "get_physical_card": {"title": "Đăng Ký Phát Hành Thẻ Vật Lý Giao Tận Tay", "category": "Quản lý Thẻ & PIN", "sla": "Giao sau 3 - 5 ngày"},
    "getting_spare_card": {"title": "Mở Thẻ Phụ Cho Người Thân", "category": "Quản lý Thẻ & PIN", "sla": "Duyệt online ngay"},
    "getting_virtual_card": {"title": "Mở Thẻ Phi Vật Lý (Virtual Card) Miễn Phí", "category": "Quản lý Thẻ & PIN", "sla": "Sẵn sàng dùng sau 30s"},
    "lost_or_stolen_card": {"title": "Báo Mất Thẻ / Thẻ Bị Đánh Cắp", "category": "Quản lý Thẻ & PIN", "sla": "Khóa khẩn cấp 24/7"},
    "lost_or_stolen_phone": {"title": "Mất Điện Thoại Chứa Ứng Dụng E-Banking & Smart OTP", "category": "Tài Khoản & Định Danh", "sla": "Khóa E-Banking khẩn cấp"},
    "order_physical_card": {"title": "Đặt In & Cá Nhân Hóa Thẻ Vật Lý", "category": "Quản lý Thẻ & PIN", "sla": "In & phát thẻ 3 ngày"},
    "passcode_forgotten": {"title": "Lấy Lại Mật Khẩu Đăng Nhập E-Banking", "category": "Tài Khoản & Định Danh", "sla": "Cấp lại qua OTP 1 phút"},
    "pending_card_payment": {"title": "Giao Dịch Thẻ Đang Chờ Xử Lý (Pending)", "category": "Quản lý Thẻ & PIN", "sla": "Tự động quyết toán 1 - 3 ngày"},
    "pending_cash_withdrawal": {"title": "Lệnh Rút Tiền ATM Đang Chờ Xử Lý", "category": "ATM & Tiền Mặt", "sla": "Quyết toán trong 24h"},
    "pending_top_up": {"title": "Lệnh Nạp Tiền Đang Ở Trạng Thái Chờ", "category": "Nạp Tiền & Số Dư", "sla": "Tối đa 15 phút"},
    "pending_transfer": {"title": "Lệnh Chuyển Khoản Đang Chờ Đối Soát", "category": "Chuyển Tiền & Thanh Toán", "sla": "Tối đa 30 phút"},
    "pin_blocked": {"title": "Mở Khóa Do Nhập Sai Mã PIN 3 Lần", "category": "Quản lý Thẻ & PIN", "sla": "Mở khóa qua eKYC 1 phút"},
    "receiving_money": {"title": "Hướng Dẫn Nhận Tiền Chuyển Khoản / Kiều Hối", "category": "Chuyển Tiền & Thanh Toán", "sla": "Nhận tiền sau 3 giây"},
    "Refund_not_showing_up": {"title": "Khoản Tiền Hoàn Trả (Refund) Chưa Về Tài Khoản", "category": "Chuyển Tiền & Thanh Toán", "sla": "Tra soát 5 - 7 ngày"},
    "request_refund": {"title": "Yêu Cầu Hoàn Tiền Giao Dịch Sai Sót", "category": "Chuyển Tiền & Thanh Toán", "sla": "Tiếp nhận 24h"},
    "reverted_card_payment?": {"title": "Giao Dịch Thanh Toán Thẻ Bị Đảo Lệnh", "category": "Quản lý Thẻ & PIN", "sla": "Hoàn tiền trong 48h"},
    "supported_cards_and_currencies": {"title": "Các Loại Thẻ & Loại Tiền Tệ Được Hỗ Trợ", "category": "Ngoại Tệ & Quốc Tế", "sla": "Xem chi tiết"},
    "terminate_account": {"title": "Quy Trình Tất Toán & Đóng Tài Khoản", "category": "Tài Khoản & Định Danh", "sla": "Xử lý trong ngày"},
    "top_up_by_bank_transfer_charge": {"title": "Phí Nạp Tiền Qua Chuyển Khoản", "category": "Nạp Tiền & Số Dư", "sla": "Miễn phí 100%"},
    "top_up_by_card_charge": {"title": "Phí Nạp Tiền Qua Thẻ Ghi Nợ/Tín Dụng", "category": "Nạp Tiền & Số Dư", "sla": "Miễn phí hoặc theo quy định thẻ"},
    "top_up_by_cash_or_cheque": {"title": "Nạp Tiền Bằng Tiền Mặt/Séc Tại Quầy", "category": "Nạp Tiền & Số Dư", "sla": "Cập nhật sau 15 phút"},
    "top_up_failed": {"title": "Nạp Tiền Thất Bại & Cách Khắc Phục", "category": "Nạp Tiền & Số Dư", "sla": "Xử lý tức thì"},
    "top_up_limits": {"title": "Hạn Mức Nạp Tiền Tối Đa Trong Ngày", "category": "Nạp Tiền & Số Dư", "sla": "Lên tới 500 triệu/ngày"},
    "top_up_reverted": {"title": "Giao Dịch Nạp Tiền Bị Hoàn Lại", "category": "Nạp Tiền & Số Dư", "sla": "Hoàn trả sau 24h"},
    "topping_up_by_card": {"title": "Hướng Dẫn Nạp Tiền Vào Tài Khoản Bằng Thẻ", "category": "Nạp Tiền & Số Dư", "sla": "Hoàn tất sau 10s"},
    "transaction_charged_twice": {"title": "Giao Dịch Bị Trừ Tiền 2 Lần (Double Charge)", "category": "Chuyển Tiền & Thanh Toán", "sla": "Hoàn tiền tự động 24h"},
    "transfer_fee_charged": {"title": "Biểu Phí Chuyển Tiền 24/7", "category": "Chuyển Tiền & Thanh Toán", "sla": "0đ (Miễn phí trọn đời)"},
    "transfer_into_account": {"title": "Chuyển Tiền Vào Tài Khoản PHÁT TÀI BANK", "category": "Chuyển Tiền & Thanh Toán", "sla": "Xử lý tức thì qua VietQR"},
    "transfer_not_received_by_recipient": {"title": "Chuyển Tiền Thành Công Nhưng Người Nhận Chưa Thấy", "category": "Chuyển Tiền & Thanh Toán", "sla": "Tra soát liên ngân hàng 2h"},
    "transfer_timing": {"title": "Thời Gian Xử Lý Lệnh Chuyển Khoản", "category": "Chuyển Tiền & Thanh Toán", "sla": "NAPAS: 3 giây | Thường: 2-4h"},
    "unable_to_verify_identity": {"title": "Lỗi Không Thể Xác Thực eKYC (CCCD mờ/Khuôn mặt)", "category": "Tài Khoản & Định Danh", "sla": "Hỗ trợ quét lại ngay"},
    "verify_my_identity": {"title": "Xác Thực Danh Tính Khách Hàng eKYC Sinh Trắc Học", "category": "Tài Khoản & Định Danh", "sla": "Hoàn tất trong 60 giây"},
    "verify_source_of_funds": {"title": "Chứng Minh Nguồn Gốc Dòng Tiền Hợp Pháp", "category": "Tài Khoản & Định Danh", "sla": "Xét duyệt trong 24h"},
    "verify_top_up": {"title": "Xác Thực Bảo Mật Khi Nạp Tiền Giá Trị Lớn", "category": "Nạp Tiền & Số Dư", "sla": "Xác thực OTP/FaceID 10s"},
    "virtual_card_not_working": {"title": "Lỗi Thẻ Ảo Không Thanh Toán Được", "category": "Quản lý Thẻ & PIN", "sla": "Mở khóa online 1 phút"},
    "visa_or_mastercard": {"title": "Tư Vấn Lựa Chọn Thẻ Quốc Tế Visa & Mastercard", "category": "Quản lý Thẻ & PIN", "sla": "Tư vấn miễn phí"},
    "why_verify_identity": {"title": "Lý Do Bắt Buộc Xác Thực Sinh Trắc Học eKYC", "category": "Tài Khoản & Định Danh", "sla": "Tuân thủ QĐ 2345/NHNN"},
    "wrong_amount_of_cash_received": {"title": "Nhận Sai Số Tiền Khi Rút Tại Cây ATM", "category": "ATM & Tiền Mặt", "sla": "Kiểm quỹ & bồi hoàn 48h"},
    "wrong_exchange_rate_for_cash_withdrawal": {"title": "Sai Lệch Tỷ Giá Khi Rút Tiền Ngoại Tệ Tại ATM", "category": "ATM & Tiền Mặt", "sla": "Tra soát đối chiếu 3 ngày"},
    # Sản phẩm ngân hàng bổ trợ trong hệ sinh thái PHÁT TÀI BANK
    "create_account": {"title": "Quy Trình Mở Tài Khoản E-Banking Mới", "category": "Tài Khoản & Định Danh", "sla": "Mở online 2 phút"},
    "savings_account": {"title": "Gói Tiết Kiệm Tích Lũy Lãi Suất Cao", "category": "Tiết Kiệm & Đầu Tư", "sla": "Mở sổ online 1 phút"},
    "loan_request": {"title": "Đăng Ký Vay Tín Chấp Trực Tuyến Duyệt 24H", "category": "Tín Dụng & Cho Vay", "sla": "Duyệt & giải ngân 24h"},
    "mortgage_domestic": {"title": "Gói Vay Mua Nhà An Cư Ưu Đãi Lãi Suất", "category": "Tín Dụng & Cho Vay", "sla": "Tư vấn trong ngày"},
    "interest_rates": {"title": "Bảng Lãi Suất Tiền Gửi & Vay Vốn Cập Nhật", "category": "Tiết Kiệm & Đầu Tư", "sla": "Cập nhật realtime"}
}

# ==============================================================================
# HỆ CƠ SỞ TRI THỨC NGHIỆP VỤ CHUYÊN SÂU (77 INTENTS HUGGING FACE BANKING77)
# ==============================================================================
BANKING77_EXPERT_KB = {
    # ─────────────────────────────────────────────────────────────────────────
    # 1. QUẢN LÝ THẺ, PIN & BẢO MẬT GIAO DỊCH
    # ─────────────────────────────────────────────────────────────────────────
    "activate_my_card": (
        "💳 **QUY TRÌNH CHUYÊN SÂU: KÍCH HOẠT THẺ ATM / VISA PHÁT TÀI BANK:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `activate_my_card`)*\n\n"
        "1️⃣ **Đăng nhập E-Banking:** Truy cập ứng dụng hoặc website PHÁT TÀI BANK -> Vào mục **'Quản Lý Thẻ'**.\n"
        "2️⃣ **Nhập thông tin thẻ:** Chọn thẻ cần kích hoạt, nhập 4 chữ số cuối in nổi trên mặt thẻ và ngày hết hạn (MM/YY).\n"
        "3️⃣ **Xác thực danh tính:** Nhập mã Smart OTP bảo mật gửi về thiết bị hoặc quét sinh trắc học FaceID.\n"
        "4️⃣ **Đổi mã PIN lần đầu:** Đổi mã PIN 6 số tại mục *'Cài đặt PIN'* hoặc cây ATM gần nhất để kích hoạt thanh toán.\n"
        "⏱️ **Cam kết SLA:** Thẻ kích hoạt tức thì, giao dịch mua sắm và rút tiền được ngay sau 60 giây!\n"
        "📞 *Tổng đài hỗ trợ kích hoạt thẻ khẩn cấp 24/7:* **1900-8888**."
    ),
    "card_about_to_expire": (
        "⏳ **QUY TRÌNH GIA HẠN THẺ SẮP HẾT HẠN (CARD ABOUT TO EXPIRE):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_about_to_expire`)*\n\n"
        "1️⃣ **Thông báo tự động:** Trước 45 ngày khi thẻ hết hạn, hệ thống tự động gửi thông báo qua SMS và App E-Banking.\n"
        "2️⃣ **Xác nhận đổi thẻ miễn phí:** Nhấp vào thông báo -> Chọn *'Gia hạn & Phát thẻ mới'* -> Xác nhận địa chỉ nhận thẻ.\n"
        "3️⃣ **Duy trì giao dịch:** Trong thời gian chờ nhận thẻ mới, thẻ hiện tại vẫn giao dịch bình thường đến hết ngày in trên mặt thẻ.\n"
        "4️⃣ **Nhận thẻ:** Thẻ mới được giao tận nhà sau **3 - 5 ngày làm việc**, hoàn toàn **0đ phí gia hạn**!"
    ),
    "card_acceptance": (
        "🌍 **PHẠM VI VÀ TIÊU CHUẨN CHẤP NHẬN THẺ PHÁT TÀI BANK:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_acceptance`)*\n\n"
        "• **Thẻ Nội Địa Napas:** Chấp nhận 100% tại hơn 20.000 cây ATM và 350.000 máy POS toàn quốc, thanh toán hóa đơn online.\n"
        "• **Thẻ Quốc Tế Visa / Mastercard:** Chấp nhận tại hơn 200 quốc gia và vùng lãnh thổ, thanh toán tại 44 triệu điểm POS và hàng triệu website quốc tế (Amazon, Apple, Shopee, Netflix...).\n"
        "• **Công nghệ bảo mật:** Tích hợp chip EMV chuẩn PCI-DSS, công nghệ xác thực 3D-Secure 2.0 chống gian lận tuyệt đối."
    ),
    "card_arrival": (
        "📦 **TRA CỨU VẬN ĐƠN VÀ THEO DÕI PHÁT THẺ (CARD ARRIVAL):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_arrival`)*\n\n"
        "1️⃣ **Kiểm tra trạng thái vận đơn:** Vào App -> Quản lý Thẻ -> Chọn **'Lịch sử phát thẻ'** để xem mã vận đơn chuyển phát nhanh.\n"
        "2️⃣ **Thời gian phát hành chuẩn:**\n"
        "   - Khu vực nội thành Hà Nội & TP.HCM: **2 - 3 ngày làm việc**.\n"
        "   - Các tỉnh thành khác: **3 - 5 ngày làm việc**.\n"
        "3️⃣ **Trường hợp quá 7 ngày chưa nhận được:** Bấm *'Báo chưa nhận được thẻ'* hoặc gọi **1900-8888**, ngân hàng sẽ phát chuyển phát hỏa tốc lại thẻ mới cho quý khách hoàn toàn miễn phí."
    ),
    "card_delivery_estimate": (
        "🚚 **THỜI GIAN GIAO THẺ ATM TẬN NHÀ DỰ KIẾN (CARD DELIVERY ESTIMATE):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_delivery_estimate`)*\n\n"
        "• **Nội thành Hà Nội & TP. Hồ Chí Minh:** 2 - 3 ngày làm việc (giao dịch viên chuyển phát tận tay).\n"
        "• **Các tỉnh thành và khu vực huyện xã:** 3 - 5 ngày làm việc qua bưu chính an toàn bảo mật cao.\n"
        "• **Dịch vụ phát thẻ hỏa tốc 24H:** Đăng ký nhận thẻ tại phòng giao dịch chỉ sau 24 giờ kể từ khi duyệt hồ sơ online!"
    ),
    "card_linking": (
        "🔗 **HƯỚNG DẪN LIÊN KẾT THẺ VỚI VÍ ĐIỆN TỬ VÀ ỨNG DỤNG MUA SẮM:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_linking`)*\n\n"
        "1️⃣ Mở ứng dụng ví cần liên kết (MoMo, ZaloPay, ShopeePay, Apple Wallet...).\n"
        "2️⃣ Chọn mục **'Liên kết thẻ/tài khoản ngân hàng'** -> Chọn logo **PHÁT TÀI BANK**.\n"
        "3️⃣ Nhập 16 số in trên thẻ, ngày hết hạn và họ tên chủ thẻ.\n"
        "4️⃣ Nhập mã xác thực OTP gửi về SMS chính chủ -> Liên kết thành công tức thì sau **30 giây**!"
    ),
    "card_not_working": (
        "⚠️ **XỬ LÝ SỰ CỐ THẺ ATM / VISA BỊ LỖI KHÔNG HOẠT ĐỘNG (CARD NOT WORKING):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_not_working`)*\n\n"
        "1️⃣ **Kiểm tra trạng thái thẻ trên App:** Đảm bảo thẻ đang ở trạng thái *'Đang hoạt động'* và tính năng *'Thanh toán trực tuyến/quẹt thẻ'* đã được bật.\n"
        "2️⃣ **Kiểm tra chip & dải từ:** Lau nhẹ dải từ và bề mặt chip EMV bằng vải mềm sạch, tránh để thẻ gần nguồn từ tính mạnh.\n"
        "3️⃣ **Đổi thẻ miễn phí:** Nếu chip thẻ bị trầy xước hỏng vật lý, bấm *'Đổi thẻ hỏng'* trên App, ngân hàng sẽ cấp đổi thẻ mới miễn phí trong 48 giờ."
    ),
    "card_payment_fee_charged": (
        "🧾 **QUY ĐỊNH BIỂU PHÍ THANH TOÁN THẺ (CARD PAYMENT FEE CHARGED):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_payment_fee_charged`)*\n\n"
        "• **Thanh toán tại POS & Online nội địa:** **0đ phí** (Hoàn toàn miễn phí 100% cho chủ thẻ).\n"
        "• **Thanh toán tại các trang web nước ngoài:** Chỉ thu phí chuyển đổi ngoại tệ cực ưu đãi từ **1.2% - 1.5%** theo tỷ giá niêm yết.\n"
        "• **Lưu ý:** Nếu quý khách bị điểm chấp nhận thẻ (POS) thu thêm phụ phí quẹt thẻ trái phép, hãy báo ngay Hotline **1900-8888** để ngân hàng xử lý bảo vệ quyền lợi."
    ),
    "card_payment_not_recognised": (
        "🚨 **XỬ LÝ KHẨN CẤP: GIAO DỊCH THẺ KHÔNG XÁC ĐỊNH / NGHI GIAN LẬN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_payment_not_recognised`)*\n\n"
        "1️⃣ **KHÓA THẺ TỨC THÌ:** Mở App E-Banking -> Quản lý Thẻ -> Gạt nút **'Khóa thẻ khẩn cấp'** (hoặc gọi hotline bấm phím 1).\n"
        "2️⃣ **Yêu cầu tra soát online:** Chọn giao dịch lạ -> Bấm **'Yêu cầu tra soát / Khiếu nại giao dịch'**.\n"
        "3️⃣ **Thời gian xử lý:** Ngân hàng phong tỏa tạm thời số tiền tranh chấp và hoàn tất điều tra bảo vệ quyền lợi khách hàng trong **7 - 15 ngày làm việc**.\n"
        "🛡️ *Cam kết:* Bồi hoàn 100% nếu phát hiện gian lận không xuất phát từ lỗi cố ý của chủ thẻ."
    ),
    "card_payment_wrong_exchange_rate": (
        "💱 **TRA SOÁT SAI LỆCH TỶ GIÁ THANH TOÁN NGOẠI TỆ QUA THẺ:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_payment_wrong_exchange_rate`)*\n\n"
        "1️⃣ **Cơ chế tỷ giá:** Giao dịch ngoại tệ được tính theo tỷ giá của tổ chức thẻ quốc tế (Visa/Mastercard) tại thời điểm giao dịch được thanh toán thực tế (thường sau 1-3 ngày làm việc), không phải tại thời điểm tạm khóa tiền.\n"
        "2️⃣ **Tra soát chênh lệch:** Nếu tỷ giá quyết toán vượt quá biên độ công bố của ngân hàng, quý khách chụp màn hình sao kê và gửi yêu cầu tra soát tại App -> Khiếu nại tỷ giá. Thời gian đối chiếu xử lý: **3 - 5 ngày làm việc**."
    ),
    "card_swallowed": (
        "🏧 **XỬ LÝ KHẨN CẤP: THẺ BỊ CÂY ATM NUỐT (CARD SWALLOWED):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `card_swallowed`)*\n\n"
        "1️⃣ **Khóa thẻ tạm thời:** Mở App -> Quản lý thẻ -> Bấm **'Khóa thẻ tạm thời'** để đảm bảo an toàn tuyệt đối.\n"
        "2️⃣ **Báo tổng đài:** Gọi ngay Hotline **1900-8888** (nhánh 1) thông báo vị trí cây ATM và thời điểm nuốt thẻ.\n"
        "3️⃣ **Nhận lại thẻ:**\n"
        "   - Tại ATM thuộc PHÁT TÀI BANK: Nhận lại thẻ tại chi nhánh quản lý cây ATM sau **2 - 3 ngày làm việc** (kèm CCCD).\n"
        "   - Hoặc chọn nhận cấp đổi thẻ mới giao tận nhà miễn phí 100%!"
    ),
    "change_pin": (
        "🔐 **HƯỚNG DẪN CHI TIẾT ĐỔI MÃ PIN THẺ ATM AN TOÀN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `change_pin`)*\n\n"
        "• **Cách 1 — Đổi trực tiếp trên App E-Banking:**\n"
        "  1. Vào Quản lý Thẻ -> Chọn thẻ cần đổi -> Bấm **'Đổi mã PIN'**.\n"
        "  2. Nhập mã PIN mới gồm 6 chữ số -> Nhập lại xác nhận.\n"
        "  3. Xác thực bằng Smart OTP / FaceID -> Hoàn tất tức thì sau 30 giây!\n"
        "• **Cách 2 — Đổi tại cây ATM:** Cho thẻ vào máy -> Nhập PIN hiện tại -> Chọn mục 'Đổi PIN' -> Nhập PIN mới 2 lần.\n"
        "💡 *Lưu ý an toàn:* Không đặt PIN trùng ngày tháng năm sinh hoặc dãy số liên tiếp (123456)."
    ),
    "compromised_card": (
        "🛡️ **CẢNH BÁO BẢO MẬT: THẺ BỊ LỘ THÔNG TIN / CÓ NGUY CƠ BỊ ĐÁNH CẮP:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `compromised_card`)*\n\n"
        "1️⃣ **Bấm KHÓA THẺ NGAY LẬP TỨC** trên ứng dụng để ngăn chặn toàn bộ giao dịch rút tiền và mua sắm.\n"
        "2️⃣ **Báo hủy thẻ cũ:** Bấm nút *'Hủy thẻ do lộ thông tin'* trong phần quản lý thẻ.\n"
        "3️⃣ **Phát hành thẻ mới miễn phí:** Hệ thống sẽ tạo một số thẻ và mã CVV hoàn toàn mới, giao thẻ tận nơi trong 3 ngày.\n"
        "📞 *Liên hệ trung tâm an ninh thẻ PHÁT TÀI BANK khẩn cấp:* **1900-8888**."
    ),
    "contactless_not_working": (
        "📡 **XỬ LÝ LỖI THANH TOÁN CHẠM CONTACTLESS KHÔNG NHẬN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `contactless_not_working`)*\n\n"
        "1️⃣ **Kích hoạt lần đầu:** Thẻ mới cần thực hiện 01 giao dịch cắm chip tại cây ATM hoặc máy POS kèm nhập mã PIN để kích hoạt ăng-ten chạm Contactless.\n"
        "2️⃣ **Kiểm tra cài đặt trên App:** Vào Quản lý Thẻ -> Đảm bảo tính năng *'Thanh toán không tiếp xúc (Contactless)'* đang ở trạng thái BẬT.\n"
        "3️⃣ **Hạn mức chạm:** Giao dịch chạm dưới 1.000.000 VNĐ không cần nhập PIN, trên 1.000.000 VNĐ vui lòng nhập PIN xác nhận."
    ),
    "declined_card_payment": (
        "❌ **NGUYÊN NHÂN VÀ CÁCH XỬ LÝ THANH TOÁN THẺ BỊ TỪ CHỐI:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `declined_card_payment`)*\n\n"
        "1️⃣ **Số dư không đủ:** Kiểm tra lại số dư khả dụng hoặc hạn mức tín dụng còn lại của thẻ.\n"
        "2️⃣ **Chưa mở khóa thanh toán Online/Quốc tế:** Vào App -> Quản lý Thẻ -> Bật *'Thanh toán Internet / Quốc tế'*.\n"
        "3️⃣ **Nhập sai thông tin bảo mật:** Kiểm tra kỹ số thẻ, ngày hết hạn (MM/YY) và 3 số CVV phía sau mặt thẻ.\n"
        "4️⃣ **Vượt hạn mức ngày:** Nâng hạn mức giao dịch trực tiếp trên App trong mục *'Cài đặt hạn mức'*."
    ),
    "disposable_card_limits": (
        "💳 **QUY ĐỊNH HẠN MỨC THẺ ẢO DÙNG 1 LẦN (DISPOSABLE CARD LIMITS):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `disposable_card_limits`)*\n\n"
        "• **Cơ chế:** Thẻ tự động hủy thông tin số thẻ và mã CVV ngay sau khi giao dịch đầu tiên hoàn tất, chống gian lận lộ số thẻ 100%!\n"
        "• **Hạn mức tối đa một giao dịch:** Lên đến **50.000.000 VNĐ / lần**.\n"
        "• **Số lượng thẻ tạo mỗi ngày:** Tối đa tạo 05 thẻ ảo dùng 1 lần trong vòng 24 giờ.\n"
        "• **Phí phát hành:** Hoàn toàn **miễn phí 0đ** trên ứng dụng E-Banking."
    ),
    "get_disposable_virtual_card": (
        "✨ **CÁC BƯỚC TẠO THẺ ẢO DÙNG 1 LẦN AN TOÀN TUYỆT ĐỐI:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `get_disposable_virtual_card`)*\n\n"
        "1️⃣ Mở App PHÁT TÀI BANK -> Vào mục **'Thẻ Của Tôi'** -> Nhấn **'Tạo Thẻ Ảo Dùng 1 Lần'**.\n"
        "2️⃣ Chọn hạn mức tối đa cho lần mua sắm này (ví dụ: 500.000 VNĐ hoặc 5.000.000 VNĐ).\n"
        "3️⃣ Xác thực bằng sinh trắc học FaceID / Smart OTP.\n"
        "4️⃣ Hệ thống cấp ngay số thẻ ảo 16 số kèm CVV để thanh toán online. Sau khi thanh toán xong, thẻ tự hủy để bảo vệ số tiền của bạn!"
    ),
    "get_physical_card": (
        "📮 **HƯỚNG DẪN ĐĂNG KÝ PHÁT HÀNH THẺ VẬT LÝ GIAO TẬN TAY:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `get_physical_card`)*\n\n"
        "1️⃣ Vào mục Dịch Vụ Thẻ trên ứng dụng -> Nhấp **'Phát hành thẻ vật lý'**.\n"
        "2️⃣ Lựa chọn loại thẻ: Thẻ Ghi Nợ Nội Địa Napas hoặc Thẻ Quốc Tế Visa / Mastercard Cashback.\n"
        "3️⃣ Điền địa chỉ nhận thẻ và số điện thoại liên hệ.\n"
        "4️⃣ Nhân viên bưu điện phát thẻ tận tay miễn phí sau **3 - 5 ngày làm việc**!"
    ),
    "getting_spare_card": (
        "👨‍👩‍👧 **HƯỚNG DẪN MỞ THẺ PHỤ CHO NGƯỜI THÂN (SPARE CARD):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `getting_spare_card`)*\n\n"
        "• **Tiện ích:** Chia sẻ hạn mức chi tiêu cho người thân, con cái du học mà không cần mở tài khoản thanh toán mới.\n"
        "• **Cách đăng ký:** Mở App -> Quản lý Thẻ -> Chọn **'Thêm Thẻ Phụ'** -> Nhập họ tên, CCCD người được cấp thẻ phụ -> Cài đặt hạn mức chi tiêu hàng tháng -> Xác nhận."
    ),
    "getting_virtual_card": (
        "⚡ **MỞ THẺ PHI VẬT LÝ (VIRTUAL CARD) SỬ DỤNG NGAY SAU 30 GIÂY:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `getting_virtual_card`)*\n\n"
        "• **Ưu điểm vượt trội:** Không mất thời gian chờ in và phát thẻ, sử dụng được ngay để liên kết ví điện tử, thanh toán hóa đơn, mua sắm online toàn cầu.\n"
        "• **Quy trình 3 bước:** App -> Thẻ của tôi -> Nhấp *'Mở thẻ phi vật lý'* -> Xác thực OTP -> Kích hoạt thẻ ngay tức thì!"
    ),
    "lost_or_stolen_card": (
        "🚨 **QUY TRÌNH XỬ LÝ KHẨN CẤP KHI MẤT THẺ HOẶC BỊ TRỘM THẺ:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `lost_or_stolen_card`)*\n\n"
        "1️⃣ **KHÓA THẺ NGAY LẬP TỨC:** Mở App E-Banking -> Quản lý thẻ -> Bấm **'Khóa thẻ khẩn cấp'**.\n"
        "2️⃣ **Gọi hotline khẩn cấp:** Nếu không có kết nối mạng, gọi ngay **1900-8888** bấm phím 1 để tổng đài viên khóa thẻ tức thì.\n"
        "3️⃣ **Yêu cầu cấp lại:** Đăng ký cấp lại thẻ mới ngay trên App, thẻ mới sẽ được phát về tận nhà quý khách sau 3 ngày làm việc."
    ),
    "order_physical_card": (
        "🎨 **ĐẶT IN THẺ VẬT LÝ VÀ CHỌN THIẾT KẾ ĐỘC BẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `order_physical_card`)*\n\n"
        "1️⃣ Truy cập kho giao diện thẻ PHÁT TÀI BANK trên App E-Banking.\n"
        "2️⃣ Chọn bộ sưu tập thẻ yêu thích: Doanh Nhân Thành Đạt, Kim Long Tài Lộc, hoặc Thẻ Kim Loại Metal Edition.\n"
        "3️⃣ Xác nhận thông tin địa chỉ nhận thẻ -> Nhận thẻ sau 3 ngày làm việc kèm phong bì bảo mật số PIN độc quyền."
    ),
    "pending_card_payment": (
        "🕒 **GIẢI THÍCH TRẠNG THÁI GIAO DỊCH CHỜ XỬ LÝ (PENDING CARD PAYMENT):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `pending_card_payment`)*\n\n"
        "• **Bản chất:** Khi quý khách quẹt thẻ hoặc mua sắm online, ngân hàng sẽ tạm giữ (hold) số tiền tương ứng để chờ bên bán xác nhận đơn hàng.\n"
        "• **Thời gian xử lý:** Đơn hàng thường quyết toán chính thức sau **1 - 3 ngày làm việc**.\n"
        "• **Nếu giao dịch bị hủy:** Số tiền tạm giữ sẽ tự động giải tỏa và hoàn trả về số dư khả dụng của quý khách sau 3 - 7 ngày."
    ),
    "pin_blocked": (
        "🔒 **HƯỚNG DẪN MỞ KHÓA MÃ PIN DO NHẬP SAI QUÁ 3 LẦN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `pin_blocked`)*\n\n"
        "• **Bảo vệ an toàn:** Hệ thống tự động khóa mã PIN khi nhập sai 3 lần liên tiếp để chống kẻ gian dò mã PIN của quý khách.\n"
        "• **Cách mở khóa trực tuyến 100%:**\n"
        "  1. Vào App E-Banking -> Quản lý Thẻ -> Chọn **'Mở khóa PIN'**.\n"
        "  2. Thực hiện xác thực khuôn mặt eKYC LiveFace.\n"
        "  3. Nhập mã PIN mới 6 số -> Thẻ được mở khóa và sử dụng bình thường ngay lập tức!"
    ),
    "reverted_card_payment?": (
        "🔄 **XỬ LÝ GIAO DỊCH THANH TOÁN BỊ ĐẢO LỆNH / HOÀN TIỀN (REVERTED PAYMENT):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `reverted_card_payment?`)*\n\n"
        "• Khi máy POS báo lỗi giao dịch hoặc người bán hủy đơn hàng, hệ thống gửi lệnh đảo hoàn tiền (Reversal).\n"
        "• Số tiền sẽ được cộng ngược lại vào tài khoản của quý khách trong vòng **24h - 48h làm việc** mà không cần làm thủ tục tra soát."
    ),
    "virtual_card_not_working": (
        "📱 **XỬ LÝ LỖI THẺ ẢO KHÔNG THANH TOÁN ĐƯỢC:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `virtual_card_not_working`)*\n\n"
        "1️⃣ Kiểm tra lại mã CVV 3 chữ số trên App (mã CVV thẻ ảo có thể thay đổi định kỳ để tăng cường bảo mật).\n"
        "2️⃣ Đảm bảo tính năng *'Thanh toán trực tuyến (E-commerce)'* đang được bật trong cài đặt thẻ.\n"
        "3️⃣ Kiểm tra số dư tài khoản thanh toán liên kết có đủ để chi trả giao dịch."
    ),
    "visa_or_mastercard": (
        "💳 **TƯ VẤN LỰA CHỌN THẺ QUỐC TẾ: VISA HAY MASTERCARD?**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `visa_or_mastercard`)*\n\n"
        "• **Thẻ Visa PHÁT TÀI BANK:** Thế mạnh chấp nhận cực kỳ phổ biến tại Châu Á, Bắc Mỹ, mạng lưới đối tác giảm giá ẩm thực và du lịch phong phú.\n"
        "• **Thẻ Mastercard PHÁT TÀI BANK:** Tỷ giá quy đổi ngoại tệ tại Châu Âu cực tốt, ưu đãi hoàn tiền tới **5%** cho các chi tiêu mua sắm online và vé máy bay.\n"
        "💡 *Khuyến nghị:* Quý khách có thể mở cùng lúc cả 2 loại thẻ ảo trên App hoàn toàn miễn phí!"
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 2. CHUYỂN TIỀN, THANH TOÁN & TRA SOÁT KHIẾU NẠI
    # ─────────────────────────────────────────────────────────────────────────
    "beneficiary_not_allowed": (
        "⛔ **XỬ LÝ LỖI TÀI KHOẢN NGƯỜI THỤ HƯỞNG BỊ HẠN CHẾ (BENEFICIARY NOT ALLOWED):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `beneficiary_not_allowed`)*\n\n"
        "1️⃣ Tài khoản người nhận đang tạm khóa, bị phong tỏa giao dịch hoặc đã đóng tài khoản tại ngân hàng thụ hưởng.\n"
        "2️⃣ Kiểm tra lại thông tin: Tên ngân hàng nhận, Số tài khoản chính xác hoặc thử chuyển qua hình thức quét mã VietQR để kiểm tra thông tin chủ tài khoản trực tiếp."
    ),
    "cancel_transfer": (
        "🛑 **QUY ĐỊNH HỦY LỆNH CHUYỂN TIỀN ĐÃ GỬI (CANCEL TRANSFER):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `cancel_transfer`)*\n\n"
        "• **Chuyển tiền nhanh Napas 24/7:** Tiền chuyển tới người nhận sau 3 giây nên không thể hủy lệnh chuyển tiền tức thời.\n"
        "• **Chuyển tiền thường / Đặt lịch tương lai:** Quý khách vào mục *'Lịch sử giao dịch'* -> Chọn lệnh chuyển đang chờ xử lý -> Nhấn **'Hủy lệnh chuyển tiền'**.\n"
        "• **Trường hợp chuyển nhầm số tài khoản:** Gọi ngay **1900-8888** để ngân hàng hỗ trợ liên hệ ngân hàng thụ hưởng phong tỏa tra soát thu hồi tiền theo quy định pháp luật."
    ),
    "declined_transfer": (
        "🚫 **NGUYÊN NHÂN LỆNH CHUYỂN TIỀN BỊ TỪ CHỐI (DECLINED TRANSFER):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `declined_transfer`)*\n\n"
        "1️⃣ Số dư khả dụng không đủ (lưu ý số dư tối thiểu duy trì tài khoản là 50.000 VNĐ).\n"
        "2️⃣ Nhập sai mã Smart OTP hoặc hết hạn thời gian nhập mã xác nhận.\n"
        "3️⃣ Giao dịch vượt hạn mức chuyển tiền ngày (chưa bổ sung sinh trắc học eKYC theo quy định NHNN)."
    ),
    "direct_debit_payment_not_recognised": (
        "📑 **TRA SOÁT KHOẢN TRÍCH NỢ TỰ ĐỘNG LẠ (DIRECT DEBIT NOT RECOGNISED):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `direct_debit_payment_not_recognised`)*\n\n"
        "1️⃣ Kiểm tra danh sách dịch vụ đăng ký thanh toán định kỳ: Hóa đơn điện, nước, cước viễn thông, phí phòng tập, gói tài khoản iCloud/Spotify/Netflix.\n"
        "2️⃣ Hủy ủy quyền trích nợ tự động: Vào App -> Thanh toán -> **'Ủy thác thanh toán định kỳ'** -> Chọn dịch vụ và nhấn **'Hủy ủy quyền'**."
    ),
    "extra_charge_on_statement": (
        "🔍 **GIẢI TRÌNH KHOẢN PHÍ LẠ TRÊN SAO KÊ TÀI KHOẢN (EXTRA CHARGE ON STATEMENT):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `extra_charge_on_statement`)*\n\n"
        "• **Các loại phí định kỳ thông thường:** Phí duy trì dịch vụ SMS Banking (nếu đăng ký), phí thường niên thẻ quốc tế.\n"
        "• **Phí chuyển đổi ngoại tệ:** Khi giao dịch tại các nền tảng nước ngoài (Google, Facebook, Grab...).\n"
        "• Nếu khoản phí không rõ nguồn gốc, quý khách bấm nút *'Tra soát khoản phí'* tại chi tiết giao dịch trên App để được hoàn tiền nếu bị tính sai."
    ),
    "failed_transfer": (
        "⚠️ **XỬ LÝ GIAO DỊCH CHUYỂN TIỀN BỊ LỖI THẤT BẠI NHƯNG BỊ TRỪ TIỀN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `failed_transfer`)*\n\n"
        "• **Cơ chế hoàn tiền tự động:** Khi giao dịch liên ngân hàng gặp sự cố đường truyền mạng NAPAS, hệ thống đối soát sẽ tự động hoàn trả tiền về tài khoản trong vòng **24 giờ làm việc**.\n"
        "• **Tra soát nhanh:** Quý khách lưu lại Mã Giao Dịch (FT Code) và gửi tại mục *'Hỗ trợ tra soát'* trên App hoặc gọi **1900-8888**."
    ),
    "pending_transfer": (
        "⏳ **TRẠNG THÁI LỆNH CHUYỂN KHOẢN ĐANG CHỜ XỬ LÝ (PENDING TRANSFER):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `pending_transfer`)*\n\n"
        "• **Chuyển tiền thường ngoài giờ làm việc:** Lệnh chuyển qua kênh liên ngân hàng CITAD thông thường sẽ được hệ thống ngân hàng nhà nước xử lý vào đầu giờ làm việc tiếp theo.\n"
        "• Để tiền tới ngay sau 3 giây 24/7 kể cả ban đêm và ngày nghỉ, quý khách luôn chọn hình thức **'Chuyển Tiền Nhanh 24/7 (NAPAS)'**!"
    ),
    "receiving_money": (
        "📥 **HƯỚNG DẪN CÁCH NHẬN TIỀN CHUYỂN KHOẢN VÀ KIỀU HỐI VỀ TÀI KHOẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `receiving_money`)*\n\n"
        "• **Nhận tiền trong nước:** Cung cấp Số tài khoản PHÁT TÀI BANK (`PTB...`) hoặc gửi **Mã VietQR cá nhân** (lấy tại góc phải App) để người gửi quét mã chuyển tức thì 0đ phí.\n"
        "• **Nhận tiền kiều hối quốc tế:** Cung cấp thông tin tài khoản kèm mã SWIFT Code: `PTBVNVX` của PHÁT TÀI BANK."
    ),
    "Refund_not_showing_up": (
        "⏱️ **KHOẢN TIỀN HOÀN TRẢ (REFUND) TỪ BÊN BÁN CHƯA VỀ TÀI KHOẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `Refund_not_showing_up`)*\n\n"
        "• **Thời gian hoàn tiền tiêu chuẩn từ đối tác thương mại điện tử:**\n"
        "  - Hoàn tiền thẻ nội địa / Tài khoản: **2 - 5 ngày làm việc**.\n"
        "  - Hoàn tiền thẻ quốc tế Visa / Mastercard: **7 - 15 ngày làm việc** (phụ thuộc vào cổng thanh toán quốc tế của đơn vị bán hàng).\n"
        "• Sau thời gian trên chưa nhận được tiền, quý khách cung cấp Biên nhận hoàn tiền (ARN Code) để ngân hàng truy soát tức thì."
    ),
    "request_refund": (
        "📝 **QUY TRÌNH YÊU CẦU HOÀN TIỀN VÀ TRA SOÁT KHIẾU NẠI (REQUEST REFUND):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `request_refund`)*\n\n"
        "1️⃣ Mở App E-Banking -> Lịch sử giao dịch -> Chọn giao dịch cần yêu cầu hoàn tiền.\n"
        "2️⃣ Nhấn chọn **'Khiếu Nại / Yêu Cầu Hoàn Tiền'** -> Chọn lý do (Hủy đơn hàng, máy POS trừ 2 lần, dịch vụ không nhận được).\n"
        "3️⃣ Đính kèm hình ảnh hóa đơn hoặc xác nhận hủy từ người bán -> Gửi yêu cầu.\n"
        "⏱️ Ngân hàng phát hành văn bản tra soát chính thức và bồi hoàn theo quy định trong vòng **5 - 10 ngày làm việc**."
    ),
    "transaction_charged_twice": (
        "⚡ **XỬ LÝ SỰ CỐ GIAO DỊCH BỊ TRỪ TIỀN 2 LẦN (DOUBLE CHARGE):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `transaction_charged_twice`)*\n\n"
        "1️⃣ Kiểm tra lại mã giao dịch trên sao kê: Nếu cùng số tiền và cùng người nhận trong khoảng thời gian vài giây, đây là lỗi trùng lặp do mạng (duplicate debit).\n"
        "2️⃣ Hệ thống quyết toán tự động phát hiện và hoàn trả lại khoản tiền bị trừ trùng trong vòng **24 giờ**.\n"
        "3️⃣ Quý khách cũng có thể ấn *'Báo trùng giao dịch'* trên App để chuyên viên tài chính hoàn tiền ưu tiên ngay trong ngày."
    ),
    "transfer_fee_charged": (
        "💸 **CHÍNH SÁCH BIỂU PHÍ CHUYỂN TIỀN CỦA PHÁT TÀI BANK:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `transfer_fee_charged`)*\n\n"
        "• **MIỄN PHÍ 100% TRỌN ĐỜI:** Toàn bộ giao dịch chuyển tiền nội bộ và chuyển tiền nhanh liên ngân hàng 24/7 NAPAS đều được **MIỄN PHÍ 0Đ**!\n"
        "• Không yêu cầu số dư tối thiểu để được hưởng chính sách 0đ phí chuyển tiền.\n"
        "• Hạn mức chuyển tiền lên tới **500.000.000 VNĐ / ngày** qua Smart OTP an toàn."
    ),
    "transfer_into_account": (
        "🏦 **CÁCH CHUYỂN TIỀN VÀO TÀI KHOẢN PHÁT TÀI BANK TỪ NGÂN HÀNG KHÁC:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `transfer_into_account`)*\n\n"
        "1️⃣ Mở ứng dụng ngân hàng quý khách đang có.\n"
        "2️⃣ Chọn Chuyển Tiền Nhanh 24/7 -> Chọn Ngân hàng thụ hưởng: **PHÁT TÀI BANK (PTB)**.\n"
        "3️⃣ Nhập Số tài khoản nhận (`PTB...`) -> Hệ thống tự động truy vấn hiện đúng tên chủ tài khoản.\n"
        "4️⃣ Nhập số tiền và xác nhận -> Tiền vào tài khoản PHÁT TÀI BANK ngay sau **3 giây**!"
    ),
    "transfer_not_received_by_recipient": (
        "❓ **ĐÃ CHUYỂN TIỀN THÀNH CÔNG NHƯNG NGƯỜI NHẬN CHƯA THẤY TIỀN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `transfer_not_received_by_recipient`)*\n\n"
        "1️⃣ Kiểm tra trạng thái giao dịch trên biên lai: Đã có chữ *'Thành công'* kèm Mã tham chiếu (RRN / Trace Code).\n"
        "2️⃣ Nhờ người nhận kiểm tra trực tiếp mục *'Lịch sử biến động số dư'* trên App ngân hàng nhận (đôi khi tin nhắn SMS biến động số dư của ngân hàng nhận bị nghẽn mạng chậm).\n"
        "3️⃣ Nếu sau 30 phút tài khoản nhận vẫn chưa có tiền, gửi mã giao dịch tới tổng đài **1900-8888** để phát lệnh tra soát liên ngân hàng tức thì."
    ),
    "transfer_timing": (
        "⚡ **THỜI GIAN TIỀN VỀ TÀI KHOẢN (TRANSFER TIMING):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `transfer_timing`)*\n\n"
        "• **Chuyển nhanh NAPAS 24/7 & Quét mã VietQR:** Nhận tiền ngay sau **3 giây**, hoạt động 24/7/365 bất kể ngày nghỉ, lễ tết.\n"
        "• **Chuyển thường liên ngân hàng (CITAD):**\n"
        "  - Chuyển trước 15:30 ngày làm việc: Nhận tiền trong buổi chiều cùng ngày.\n"
        "  - Chuyển sau 15:30 hoặc cuối tuần: Tiền về vào sáng ngày làm việc kế tiếp."
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 3. NẠP TIỀN, RÚT TIỀN & SỐ DƯ TÀI KHOẢN
    # ─────────────────────────────────────────────────────────────────────────
    "automatic_top_up": (
        "🔄 **HƯỚNG DẪN CÀI ĐẶT NẠP TIỀN TỰ ĐỘNG (AUTOMATIC TOP-UP):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `automatic_top_up`)*\n\n"
        "1️⃣ Vào App PHÁT TÀI BANK -> Chọn mục **'Nạp Tiền'** -> Bật tính năng **'Nạp tiền tự động'**.\n"
        "2️⃣ Cài đặt điều kiện kích hoạt: Khi số dư khả dụng thấp hơn mức định trước (ví dụ: < 100.000 VNĐ) hoặc nạp định kỳ vào ngày nhận lương hàng tháng.\n"
        "3️⃣ Chọn nguồn nạp tiền (thẻ liên kết hoặc tài khoản nguồn) -> Xác thực OTP -> Hoàn tất cài đặt an tâm không lo gián đoạn chi tiêu!"
    ),
    "balance_not_updated_after_bank_transfer": (
        "⏳ **SỐ DƯ CHƯA CẬP NHẬT SAU KHI CHUYỂN KHOẢN VÀO TÀI KHOẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `balance_not_updated_after_bank_transfer`)*\n\n"
        "1️⃣ Thực hiện thao tác kéo màn hình xuống để làm mới (Pull to refresh) ứng dụng E-Banking.\n"
        "2️⃣ Kiểm tra mục *'Biến động số dư'* để xác nhận giao dịch ghi nợ/ghi có đã ghi sổ thành công.\n"
        "3️⃣ Trong trường hợp ngân hàng chuyển gửi lệnh thường, thời gian bù trừ liên ngân hàng có thể mất từ 15 - 30 phút. Nếu quá thời gian trên, hãy gửi biên lai chuyển tiền để tổng đài tra soát ngay."
    ),
    "balance_not_updated_after_cheque_or_cash_deposit": (
        "💼 **SỐ DƯ CHƯA CẬP NHẬT SAU KHI NỘP TIỀN MẶT HOẶC SÉC:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `balance_not_updated_after_cheque_or_cash_deposit`)*\n\n"
        "• **Nộp tiền mặt tại máy CRM / ATM thông minh:** Số dư cập nhật ngay sau **60 giây**.\n"
        "• **Nộp tiền tại quầy giao dịch:** Cập nhật số dư tức thì trong buổi giao dịch.\n"
        "• **Thanh toán séc ngân hàng:** Cần thời gian trung tâm bù trừ séc xác thực chữ ký và tài khoản phát hành séc trong vòng **24 - 48 giờ làm việc** theo quy định của Ngân hàng Nhà nước."
    ),
    "pending_top_up": (
        "🕒 **LỆNH NẠP TIỀN ĐANG TRONG TRẠNG THÁI CHỜ XỬ LÝ (PENDING TOP-UP):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `pending_top_up`)*\n\n"
        "• Cổng thanh toán đang chờ xác nhận từ ngân hàng phát hành thẻ nguồn.\n"
        "• Thời gian hoàn tất tối đa: **15 phút**. Quý khách không nên thực hiện thao tác nạp tiền lặp lại nhiều lần để tránh bị trừ tiền 2 lần."
    ),
    "top_up_by_bank_transfer_charge": (
        "🆓 **BIỂU PHÍ NẠP TIỀN VÀO TÀI KHOẢN BẰNG CHUYỂN KHOẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_by_bank_transfer_charge`)*\n\n"
        "• PHÁT TÀI BANK **miễn phí 100% (0đ)** cho tất cả các giao dịch nhận tiền và nạp tiền chuyển khoản từ bất kỳ ngân hàng nào trong nước.\n"
        "• Không thu phụ phí duy trì, không khấu trừ phí giao dịch đối với người nhận."
    ),
    "top_up_by_card_charge": (
        "💳 **QUY ĐỊNH PHÍ NẠP TIỀN VÀO TÀI KHOẢN QUA THẺ LIÊN KẾT:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_by_card_charge`)*\n\n"
        "• **Nạp từ thẻ ghi nợ nội địa (Debit Card):** Hoàn toàn miễn phí 0đ.\n"
        "• **Nạp từ thẻ tín dụng quốc tế (Credit Card):** Áp dụng mức phí xử lý giao dịch ứng tiền theo quy định của tổ chức thẻ quốc tế từ 1.5% - 2.0%."
    ),
    "top_up_by_cash_or_cheque": (
        "🏦 **HƯỚNG DẪN NẠP TIỀN MẶT HOẶC NỘP SÉC VÀO TÀI KHOẢN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_by_cash_or_cheque`)*\n\n"
        "• **Cách 1 — Nộp tại cây ATM đa năng LiveBank / CRM:** Nhét tiền mặt trực tiếp vào khay nạp tiền (tối đa 200 tờ/lần) -> Tiền vào tài khoản ngay tức thì.\n"
        "• **Cách 2 — Nộp tại quầy giao dịch:** Xuất trình CCCD và số tài khoản tại bất kỳ chi nhánh PHÁT TÀI BANK trên toàn quốc."
    ),
    "top_up_failed": (
        "❌ **XỬ LÝ LỖI NẠP TIỀN VÀO TÀI KHOẢN BỊ BÁO THẤT BẠI:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_failed`)*\n\n"
        "1️⃣ Kiểm tra lại số dư tài khoản thẻ nguồn hoặc ví nguồn.\n"
        "2️⃣ Kiểm tra hạn mức giao dịch trực tuyến của thẻ nguồn đã được mở hay chưa.\n"
        "3️⃣ Nếu tài khoản nguồn đã bị trừ tiền nhưng tài khoản PHÁT TÀI BANK chưa cộng tiền: Tiền sẽ được hệ thống hoàn tự động về nguồn trong vòng 24 giờ."
    ),
    "top_up_limits": (
        "📊 **HẠN MỨC NẠP TIỀN TỐI ĐA TRONG NGÀY (TOP-UP LIMITS):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_limits`)*\n\n"
        "• Tài khoản xác thực eKYC cơ bản: Nạp tối đa **100.000.000 VNĐ / ngày**.\n"
        "• Tài khoản đã bổ sung sinh trắc học FaceID: Hạn mức lên đến **500.000.000 VNĐ / ngày**.\n"
        "• Nạp tiền tại quầy giao dịch: Không giới hạn hạn mức nạp tiền mặt."
    ),
    "top_up_reverted": (
        "🔄 **GIAO DỊCH NẠP TIỀN BỊ HOÀN LẠI (TOP-UP REVERTED):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `top_up_reverted`)*\n\n"
        "• Lệnh nạp tiền bị đảo ngược khi ngân hàng đối tác từ chối lệnh quyết toán hoặc kết nối mạng quá giờ (Timeout).\n"
        "• Toàn bộ số tiền nạp được hoàn trả 100% về tài khoản gốc của quý khách mà không phát sinh bất kỳ khoản phí nào."
    ),
    "topping_up_by_card": (
        "📲 **CÁC BƯỚC NẠP TIỀN TỨC THÌ BẰNG THẺ LIÊN KẾT:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `topping_up_by_card`)*\n\n"
        "1️⃣ Mở App PHÁT TÀI BANK -> Nhấn nút **'Nạp Tiền'** tại màn hình chính.\n"
        "2️⃣ Chọn nguồn nạp tiền từ Thẻ ghi nợ liên kết đã lưu.\n"
        "3️⃣ Nhập số tiền muốn nạp (tối thiểu 50.000 VNĐ).\n"
        "4️⃣ Xác thực sinh trắc học FaceID / OTP -> Số dư cộng vào tài khoản sau 5 giây!"
    ),
    "verify_top_up": (
        "🛡️ **QUY TRÌNH XÁC THỰC BẢO MẬT GIAO DỊCH NẠP TIỀN LỚN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `verify_top_up`)*\n\n"
        "• Với các giao dịch nạp tiền trên 10.000.000 VNĐ, hệ thống kích hoạt bảo mật đa tầng yêu cầu quét khuôn mặt sinh trắc học LiveFace và nhập mã xác thực Smart OTP.\n"
        "• Điều này nhằm đảm bảo chính chủ thực hiện và phòng ngừa rủi ro bị kẻ gian thao túng thiết bị."
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 4. GIAO DỊCH CÂY ATM & RÚT TIỀN MẶT
    # ─────────────────────────────────────────────────────────────────────────
    "atm_support": (
        "🏧 **DỊCH VỤ HỖ TRỢ VÀ TÌM KIẾM CÂY ATM GẦN NHẤT:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `atm_support`)*\n\n"
        "• **Tiện ích tại cây ATM:** Rút tiền bằng thẻ hoặc quét mã QR không cần thẻ vật lý, nộp tiền mặt, đổi mã PIN, in sao kê, mở sổ tiết kiệm tại cây ATM.\n"
        "• **Tìm kiếm:** Vào mục *'Mạng lưới chi nhánh & ATM'* trên website hoặc App để xem chỉ đường GPS tới cây ATM gần nhất đang hoạt động."
    ),
    "cash_withdrawal_charge": (
        "💵 **BIỂU PHÍ RÚT TIỀN MẶT TẠI CÂY ATM:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `cash_withdrawal_charge`)*\n\n"
        "• **Tại cây ATM thuộc PHÁT TÀI BANK:** **MIỄN PHÍ 0Đ** cho tất cả chủ thẻ.\n"
        "• **Tại cây ATM ngân hàng khác (Liên minh Napas):** Chỉ 1.100 VNĐ - 3.300 VNĐ / giao dịch theo quy định chuẩn của Napas.\n"
        "• **Rút tiền bằng mã QR không cần thẻ vật lý:** Hoàn toàn miễn phí trên toàn hệ thống."
    ),
    "cash_withdrawal_not_recognised": (
        "🚨 **TRA SOÁT KHẨN CẤP: GIAO DỊCH RÚT TIỀN ATM KHÔNG THỰC HIỆN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `cash_withdrawal_not_recognised`)*\n\n"
        "1️⃣ Báo khóa thẻ ngay trên App để ngăn chặn các giao dịch tiếp theo.\n"
        "2️⃣ Nhấn nút *'Tra soát giao dịch ATM'* -> Ghi rõ thời gian và địa điểm cây ATM xuất hiện giao dịch lạ.\n"
        "3️⃣ Bộ phận an ninh ngân hàng sẽ trích xuất camera giám sát (CCTV) tại cây ATM và đối soát hoàn trả tiền cho khách hàng."
    ),
    "declined_cash_withdrawal": (
        "🚫 **NGUYÊN NHÂN VÀ CÁCH XỬ LÝ LỖI RÚT TIỀN ATM BỊ TỪ CHỐI:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `declined_cash_withdrawal`)*\n\n"
        "1️⃣ **Cây ATM hết tiền hoặc hỏng khay nhả tiền:** Thử rút số tiền nhỏ hơn hoặc di chuyển sang cây ATM lân cận.\n"
        "2️⃣ **Vượt hạn mức rút tiền một lần:** Cây ATM thường chỉ nhả tối đa 5.000.000 VNĐ / lần rút (tối đa 50.000.000 VNĐ / ngày).\n"
        "3️⃣ **Nhập sai mã PIN:** Kiểm tra bàn phím và nhập lại chính xác mã PIN 6 số."
    ),
    "pending_cash_withdrawal": (
        "⏳ **GIAO DỊCH RÚT TIỀN BỊ TRỪ TIỀN NHƯNG CÂY ATM KHÔNG NHẢ TIỀN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `pending_cash_withdrawal`)*\n\n"
        "1️⃣ Đứng chờ trước cửa nhả tiền của ATM thêm 60 giây đề phòng máy nhả tiền trễ.\n"
        "2️⃣ Chụp ảnh màn hình cây ATM báo lỗi và giữ lại biên lai in ra (nếu có).\n"
        "3️⃣ Hệ thống kiểm quỹ ATM sẽ tự động hoàn trả số tiền về tài khoản của quý khách trong vòng **24h - 48h làm việc**."
    ),
    "wrong_amount_of_cash_received": (
        "🔢 **XỬ LÝ SỰ CỐ NHẬN SAI SỐ TIỀN KHI RÚT TẠI CÂY ATM:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `wrong_amount_of_cash_received`)*\n\n"
        "1️⃣ Đếm kỹ lại số tiền vừa rút ngay trước ống kính camera giám sát của cây ATM.\n"
        "2️⃣ Giữ lại hóa đơn biên lai rút tiền do máy in ra.\n"
        "3️⃣ Gọi tổng đài **1900-8888** báo mã cây ATM. Ngân hàng sẽ thực hiện kiểm quỹ đột xuất và đối chiếu hộc tiền để bồi hoàn số tiền thiếu vào tài khoản trong 48 giờ."
    ),
    "wrong_exchange_rate_for_cash_withdrawal": (
        "🌐 **KHIẾU NẠI SAI LỆCH TỶ GIÁ RÚT TIỀN MẶT NGOẠI TỆ Ở NƯỚC NGOÀI:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `wrong_exchange_rate_for_cash_withdrawal`)*\n\n"
        "• Khi rút tiền mặt tại cây ATM nước ngoài bằng thẻ Visa/Mastercard, hãy luôn chọn thanh toán bằng đồng tiền bản địa (Local Currency), không chọn quy đổi động (DCC) tại màn hình ATM để tránh bị đội phí tỷ giá.\n"
        "• Nếu phát hiện tỷ giá bị tính sai quy định, gửi ảnh chụp biên lai ATM tới App để ngân hàng đối soát khiếu nại quốc tế."
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 5. TÀI KHOẢN, MẬT KHẨU & ĐỊNH DANH SINH TRẮC HỌC (eKYC)
    # ─────────────────────────────────────────────────────────────────────────
    "age_limit": (
        "🎂 **QUY ĐỊNH ĐỘ TUỔI MỞ VÀ SỬ DỤNG DỊCH VỤ PHÁT TÀI BANK:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `age_limit`)*\n\n"
        "• **Từ đủ 18 tuổi trở lên:** Có CCCD/Hộ chiếu hợp lệ -> Mở tài khoản E-Banking đầy đủ tính năng, sử dụng mọi dịch vụ chuyển tiền, thẻ tín dụng, gửi tiết kiệm, vay online.\n"
        "• **Từ đủ 15 đến dưới 18 tuổi:** Được mở tài khoản thanh toán và thẻ ghi nợ nội địa theo quy định pháp luật.\n"
        "• **Dưới 15 tuổi:** Mở tài khoản tiết kiệm thông qua người đại diện theo pháp luật (cha mẹ/người giám hộ)."
    ),
    "edit_personal_details": (
        "📝 **CẬP NHẬT THÔNG TIN CÁ NHÂN VÀ ĐỊA CHỈ NHẬN THẺ:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `edit_personal_details`)*\n\n"
        "• **Thay đổi Email, Địa chỉ thường trú:** Thực hiện online 100% tại App -> Cài đặt tài khoản -> Chọn *'Chỉnh sửa thông tin cá nhân'* -> Xác thực khuôn mặt.\n"
        "• **Thay đổi Số điện thoại đăng ký / Số CCCD mới:** Mang CCCD gắn chip đến phòng giao dịch gần nhất để chuyên viên đối chiếu sinh trắc học và cập nhật an toàn."
    ),
    "lost_or_stolen_phone": (
        "📱 **XỬ LÝ KHẨN CẤP KHI MẤT ĐIỆN THOẠI CÀI APP E-BANKING:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `lost_or_stolen_phone`)*\n\n"
        "1️⃣ Gọi ngay đường dây nóng khẩn cấp **1900-8888** yêu cầu **'Khóa quyền truy cập E-Banking & Hủy kích hoạt Smart OTP trên thiết bị cũ'**.\n"
        "2️⃣ Liên hệ nhà mạng viễn thông khóa SIM điện thoại để kẻ gian không thể nhận mã OTP SMS.\n"
        "3️⃣ Khi đổi sang điện thoại mới, đăng nhập lại và thực hiện xác thực khuôn mặt sinh trắc học để kích hoạt thiết bị tin cậy mới."
    ),
    "passcode_forgotten": (
        "🔑 **QUY TRÌNH LẤY LẠI MẬT KHẨU ĐĂNG NHẬP E-BANKING TRỰC TUYẾN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `passcode_forgotten`)*\n\n"
        "1️⃣ Tại màn hình đăng nhập, nhấp vào dòng chữ **'Quên mật khẩu?'**.\n"
        "2️⃣ Nhập Số điện thoại hoặc Tên đăng nhập tài khoản.\n"
        "3️⃣ Quét khuôn mặt xác thực sinh trắc học eKYC và nhập mã OTP gửi về SMS chính chủ.\n"
        "4️⃣ Thiết lập mật khẩu mới (tối thiểu 6 ký tự gồm chữ hoa, chữ thường và số) -> Đăng nhập lại ngay tức thì sau 60 giây!"
    ),
    "terminate_account": (
        "📑 **QUY TRÌNH TẤT TOÁN VÀ ĐÓNG TÀI KHOẢN NGÂN HÀNG:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `terminate_account`)*\n\n"
        "1️⃣ Chuyển toàn bộ số dư khả dụng sang tài khoản ngân hàng khác hoặc rút hết tiền mặt.\n"
        "2️⃣ Thanh toán toàn bộ dư nợ thẻ tín dụng hoặc các khoản phí còn tồn đọng (nếu có).\n"
        "3️⃣ Mang CCCD tới chi nhánh PHÁT TÀI BANK làm thủ tục ký biên bản đóng tài khoản, ngân hàng hoàn tất đóng tài khoản trong 15 phút."
    ),
    "unable_to_verify_identity": (
        "⚠️ **KHẮC PHỤC LỖI KHÔNG THỂ XÁC THỰC DANH TÍNH eKYC:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `unable_to_verify_identity`)*\n\n"
        "• **Lỗi chụp ảnh CCCD:** Đặt CCCD trên mặt phẳng tối màu, chụp đủ 4 góc, không để ánh sáng đèn phản chiếu làm lóa chữ và mã QR.\n"
        "• **Lỗi quét khuôn mặt FaceID:** Giữ điện thoại ngang tầm mắt, không đeo kính râm, không đội mũ, ở nơi có đủ ánh sáng tự nhiên.\n"
        "• Nếu chip NFC trên CCCD không đọc được, hãy đến phòng giao dịch gần nhất để nhân viên quét đầu đọc chuyên dụng trong 2 phút."
    ),
    "verify_my_identity": (
        "🆔 **QUY TRÌNH ĐỊNH DANH SINH TRẮC HỌC (eKYC THEO QUYẾT ĐỊNH 2345/NHNN):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `verify_my_identity`)*\n\n"
        "1️⃣ Vào App PHÁT TÀI BANK -> Cài đặt -> Chọn **'Cập nhật Sinh trắc học / eKYC'**.\n"
        "2️⃣ Chụp ảnh 2 mặt Căn cước công dân gắn chip.\n"
        "3️⃣ Áp mặt lưng điện thoại vào chip trên thẻ CCCD để đọc thông tin thẻ căn cước qua NFC.\n"
        "4️⃣ Quét khuôn mặt trực tiếp theo hướng dẫn -> Hoàn tất nâng hạn mức chuyển tiền lên đến **500 triệu/ngày**!"
    ),
    "verify_source_of_funds": (
        "💼 **QUY TRÌNH XÁC THỰC NGUỒN GỐC DÒNG TIỀN HỢP PHÁP:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `verify_source_of_funds`)*\n\n"
        "• Áp dụng khi phát sinh các giao dịch chuyển tiền giá trị đặc biệt lớn theo quy định phòng chống rửa tiền (AML).\n"
        "• Quý khách có thể tải lên tài liệu chứng minh đơn giản: Hợp đồng lao động, Bảng lương, Hợp đồng mua bán tài sản hoặc Giấy phép kinh doanh trực tiếp trên App."
    ),
    "why_verify_identity": (
        "❓ **TẠI SAO BẮT BUỘC PHẢI XÁC THỰC SINH TRẮC HỌC eKYC?**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `why_verify_identity`)*\n\n"
        "• **Bảo vệ tiền của chính bạn:** Ngăn chặn kẻ gian sử dụng tài khoản rác, tài khoản giả mạo để lừa đảo hoặc chuyển tiền trái phép khi bị mất cắp thông tin.\n"
        "• **Tuân thủ pháp luật:** Theo **Quyết định 2345/QĐ-NHNN**, các giao dịch chuyển tiền trên 10 triệu đồng/lần hoặc tổng trên 20 triệu đồng/ngày bắt buộc phải xác thực bằng khuôn mặt chính chủ trùng khớp với dữ liệu bộ Công An."
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 6. TỶ GIÁ, NGOẠI TỆ & DỊCH VỤ QUỐC TẾ
    # ─────────────────────────────────────────────────────────────────────────
    "country_support": (
        "🌐 **DANH SÁCH QUỐC GIA ĐƯỢC HỖ TRỢ GIAO DỊCH VÀ CHUYỂN TIỀN:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `country_support`)*\n\n"
        "• Thẻ PHÁT TÀI BANK Visa & Mastercard được chấp nhận tại hơn **200 quốc gia và vùng lãnh thổ** trên toàn cầu.\n"
        "• Mạng lưới chuyển tiền quốc tế Swift liên kết với hơn 11.000 định chế tài chính trên toàn thế giới (Mỹ, Anh, Châu Âu, Nhật Bản, Hàn Quốc, Úc, Singapore...)."
    ),
    "exchange_charge": (
        "💹 **BIỂU PHÍ CHUYỂN ĐỔI NGOẠI TỆ CẠNH TRANH NHẤT THỊ TRƯỜNG:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `exchange_charge`)*\n\n"
        "• **Phí quản lý giao dịch ngoại tệ:** Chỉ từ **1.2% - 1.5%** giá trị giao dịch (thấp hơn mức 2.5% - 3.5% của thị trường thông thường).\n"
        "• Miễn hoàn toàn phí chuyển đổi ngoại tệ cho chủ thẻ Hạng Bạch Kim (Platinum) và Kim Loại (Metal Edition) khi chi tiêu tại nước ngoài."
    ),
    "exchange_rate": (
        "📊 **BẢNG TỶ GIÁ NGOẠI TỆ THAM CHIẾU HÔM NAY (CẬP NHẬT REALTIME):**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `exchange_rate`)*\n\n"
        "• **Đô la Mỹ (USD):** Mua vào: **25.120** | Bán ra: **25.380 VND**\n"
        "• **Đồng Euro (EUR):** Mua vào: **27.250** | Bán ra: **27.680 VND**\n"
        "• **Yên Nhật (JPY):** Mua vào: **164.50** | Bán ra: **169.80 VND**\n"
        "• **Bảng Anh (GBP):** Mua vào: **32.100** | Bán ra: **32.750 VND**\n"
        "• **Đô la Úc (AUD):** Mua vào: **16.350** | Bán ra: **16.850 VND**\n"
        "📈 *Tỷ giá biến động theo thời gian thực — Quý khách có thể xem bảng tỷ giá chi tiết từng phút trên App E-Banking.*"
    ),
    "exchange_via_app": (
        "💱 **HƯỚNG DẪN MUA BÁN VÀ QUY ĐỔI NGOẠI TỆ ONLINE TRÊN APP:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `exchange_via_app`)*\n\n"
        "1️⃣ Mở App PHÁT TÀI BANK -> Vào mục **'Đầu Tư & Ngoại Tệ'** -> Chọn **'Quy đổi ngoại tệ'**.\n"
        "2️⃣ Chọn loại ngoại tệ cần mua/bán (USD, EUR, JPY...) và nhập số tiền.\n"
        "3️⃣ Kiểm tra tỷ giá áp dụng ưu đãi -> Chọn tài khoản thanh toán nguồn.\n"
        "4️⃣ Xác thực Smart OTP -> Ngoại tệ được cộng vào ví đa tệ của quý khách ngay lập tức!"
    ),
    "fiat_currency_support": (
        "💵 **DANH MỤC CÁC LOẠI TIỀN TỆ PHÁP ĐỊNH ĐƯỢC HỖ TRỢ:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `fiat_currency_support`)*\n\n"
        "• Hỗ trợ giao dịch và lưu trữ trên 25 đồng tiền phổ biến: **VND, USD, EUR, GBP, JPY, AUD, SGD, CAD, CHF, CNY, KRW, THB, HKD...**\n"
        "• Hỗ trợ mở tài khoản đa tệ giúp khách hàng giữ ngoại tệ để thanh toán học phí du học, công tác hoặc du lịch nước ngoài mà không lo biến động tỷ giá."
    ),
    "supported_cards_and_currencies": (
        "💳 **DANH MỤC THẺ VÀ TIỀN TỆ ĐƯỢC CHẤP NHẬN TẠI PHÁT TÀI BANK:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `supported_cards_and_currencies`)*\n\n"
        "• **Các dòng thẻ:** Thẻ ghi nợ nội địa Napas, Thẻ ghi nợ quốc tế Visa Debit, Thẻ tín dụng hoàn tiền Mastercard Cashback, Thẻ ảo dùng 1 lần Disposable Virtual Card.\n"
        "• **Đơn vị tiền tệ thanh toán:** Chấp nhận thanh toán bằng VND và mọi loại ngoại tệ được quy đổi tự động theo tỷ giá chuẩn quốc tế."
    ),
    "apple_pay_or_google_pay": (
        "📲 **HƯỚNG DẪN TÍCH HỢP APPLE PAY & GOOGLE WALLET:**\n"
        "*(Theo chuẩn nghiệp vụ ý định Hugging Face: `apple_pay_or_google_pay`)*\n\n"
        "1️⃣ Mở ứng dụng **Apple Wallet** (trên iPhone/Apple Watch) hoặc **Google Wallet** (trên điện thoại Android).\n"
        "2️⃣ Nhấn dấu **(+)** -> Chọn **'Thẻ ghi nợ hoặc thẻ tín dụng'**.\n"
        "3️⃣ Đưa thẻ PHÁT TÀI BANK vào khung quét camera hoặc nhập tay số thẻ 16 số.\n"
        "4️⃣ Nhập mã OTP xác thực ngân hàng gửi về SMS -> Thanh toán chạm 1 chạm cực kỳ thời thượng và bảo mật không cần mang theo ví vật lý!"
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # 7. SẢN PHẨM TÀI CHÍNH BỔ TRỢ HỆ SINH THÁI PHÁT TÀI BANK
    # ─────────────────────────────────────────────────────────────────────────
    "create_account": (
        "📌 **CÁC BƯỚC MỞ TÀI KHOẢN E-BANKING PHÁT TÀI BANK ONLINE:**\n"
        "*(Sản phẩm tài chính số tích hợp AI BANKING77)*\n\n"
        "1️⃣ **Bước 1:** Bấm vào nút **'Đăng Ký'** ở góc phải thanh menu hoặc mở khung chat.\n"
        "2️⃣ **Bước 2:** Điền thông tin cá nhân: Họ và tên, Tên đăng nhập (viết liền không dấu), Số điện thoại chính chủ.\n"
        "3️⃣ **Bước 3:** Nhập Mật khẩu an toàn (tối thiểu 6 ký tự) và xác nhận.\n"
        "4️⃣ **Bước 4:** Bấm **'Mở Tài Khoản'** -> Hệ thống cấp số tài khoản định danh `PTB...` miễn phí và đăng nhập ngay!\n"
        "💡 *Hotline hỗ trợ 24/7:* **1900-8888**."
    ),
    "savings_account": (
        "💰 **HƯỚNG DẪN MỞ SỔ TIẾT KIỆM ONLINE LÃI SUẤT TỚI 6.8%/NĂM:**\n"
        "*(Sản phẩm tài chính số tích hợp AI BANKING77)*\n\n"
        "1️⃣ Trên giao diện web, cuộn tới mục Dịch Vụ Ngân Hàng -> Chọn gói **'Tiết Kiệm Linh Hoạt'**.\n"
        "2️⃣ Chọn số tiền gửi (tối thiểu 1.000.000 VNĐ) và kỳ hạn mong muốn (1 đến 36 tháng).\n"
        "3️⃣ Chọn hình thức nhận lãi: Hàng tháng qua tài khoản hoặc cộng dồn lãi cuối kỳ.\n"
        "4️⃣ Bấm **'Xác nhận mở sổ'** -> Sổ tiết kiệm điện tử được sinh ra lập tức và hiển thị biến động lãi suất minh bạch mỗi ngày!"
    ),
    "loan_request": (
        "📝 **CÁC BƯỚC ĐĂNG KÝ VAY TÍN CHẤP TIÊU DÙNG DUYỆT 24H:**\n"
        "*(Sản phẩm tài chính số tích hợp AI BANKING77)*\n\n"
        "1️⃣ Chọn gói **'Vay Tín Chấp Online'** trong danh mục dịch vụ ngân hàng.\n"
        "2️⃣ Nhập khoản tiền muốn vay (từ 10 triệu đến 500 triệu) và kỳ hạn trả dần (6 - 60 tháng).\n"
        "3️⃣ Tải ảnh CCCD gắn chip và thông tin thu nhập theo mẫu đơn giản.\n"
        "4️⃣ Hệ thống AI thẩm định tự động và **giải ngân trực tiếp vào tài khoản trong 24 giờ**!"
    ),
    "mortgage_domestic": (
        "🏠 **GÓI VAY MUA NHÀ AN CƯ LÃI SUẤT ƯU ĐÃI CHỈ TỪ 7.5%/NĂM:**\n"
        "*(Sản phẩm tài chính số tích hợp AI BANKING77)*\n\n"
        "• Tài trợ lên tới **85% giá trị hợp đồng mua bán bất động sản**, thời hạn vay tối đa 30 năm.\n"
        "• Ân hạn trả nợ gốc trong 24 tháng đầu tiên, không bắt buộc mua bảo hiểm nhân thọ đi kèm.\n"
        "📞 Đặt lịch hẹn chuyên viên tín dụng tư vấn tận nơi miễn phí: **1900-8888** (nhánh 3)."
    ),
    "interest_rates": (
        "📊 **BIỂU LÃI SUẤT THAM CHIẾU CẬP NHẬT CỦA PHÁT TÀI BANK:**\n"
        "*(Sản phẩm tài chính số tích hợp AI BANKING77)*\n\n"
        "• Tiết kiệm kỳ hạn 1 tháng: **4.2%/năm**\n"
        "• Tiết kiệm kỳ hạn 6 tháng: **5.5%/năm**\n"
        "• Tiết kiệm kỳ hạn 12 tháng: **6.8%/năm** (Lãi suất ưu đãi nhất thị trường)\n"
        "• Vay tín chấp tiêu dùng: từ **10.8%/năm**\n"
        "• Vay mua nhà cố định 3 năm đầu: từ **7.5%/năm**"
    )
}

# ==============================================================================
# HÀM TRUY XUẤT CHUYÊN SÂU BANKING77 THEO TẬP HUGGING FACE
# ==============================================================================
def get_banking77_expert_reply(intent: str) -> tuple[str, dict]:
    """
    Trả về câu trả lời chuyên sâu kèm metadata chi tiết theo chuẩn BANKING77 Hugging Face
    """
    intent_clean = intent.strip()
    
    # Tìm kiếm chính xác
    if intent_clean in BANKING77_EXPERT_KB:
        meta = BANKING77_METADATA.get(intent_clean, {
            "title": intent_clean.replace('_', ' ').title(),
            "category": "Nghiệp Vụ Ngân Hàng",
            "sla": "24/7"
        })
        return BANKING77_EXPERT_KB[intent_clean], meta
        
    # Thử tìm theo dạng không phân biệt hoa thường hoặc bỏ dấu hỏi
    for k, text in BANKING77_EXPERT_KB.items():
        if k.lower() == intent_clean.lower() or k.rstrip('?').lower() == intent_clean.rstrip('?').lower():
            meta = BANKING77_METADATA.get(k, {
                "title": k.replace('_', ' ').title(),
                "category": "Nghiệp Vụ Ngân Hàng",
                "sla": "24/7"
            })
            return text, meta
            
    # Dự phòng thông minh nếu nhãn chưa có trong danh sách
    intent_display = intent_clean.replace('_', ' ').title()
    fallback_text = (
        f"🏛️ **HƯỚNG DẪN NGHIỆP VỤ CHUYÊN SÂU: {intent_display.upper()}**\n"
        f"*(Nhận diện theo tập dữ liệu Hugging Face: `{intent_clean}`)*\n\n"
        f"1️⃣ **Kiểm tra thông tin trên App:** Quý khách mở ứng dụng E-Banking PHÁT TÀI BANK -> Vào mục cài đặt dịch vụ tương ứng với `{intent_clean}`.\n"
        f"2️⃣ **Xác thực bảo mật:** Sử dụng sinh trắc học FaceID hoặc Smart OTP để thực hiện thao tác an toàn.\n"
        f"3️⃣ **Hỗ trợ trực tiếp:** Nếu cần hỗ trợ khẩn cấp, vui lòng gọi Hotline **1900-8888** (nhánh 1) hoặc tới chi nhánh gần nhất để được phục vụ 24/7."
    )
    meta = {
        "title": intent_display,
        "category": "Nghiệp Vụ Ngân Hàng Tổng Hợp",
        "sla": "24/7"
    }
    return fallback_text, meta
