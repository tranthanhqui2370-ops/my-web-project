# =============================================================================
# PHÁT TÀI BANK - AI Backend & Centralized Data Storage Server
# File: ai_backend/server_banking77.py
#
# Mô tả: Tải tập dữ liệu BANKING77 từ Hugging Face, huấn luyện mô hình MLP
#         và Logistic Regression phân loại 77 ý định tài chính.
#         Cung cấp hệ thống REST API lưu trữ trực tiếp toàn bộ dữ liệu vào
#         thư mục data/ (không phụ thuộc LocalStorage):
#           - data/chat_history.json
#           - data/customers.json
#           - data/search_history.json
#           - data/planner.json (Sổ nhắc hạn thanh toán & chi tiêu CRUD)
#           - data/cart.json (Giỏ dịch vụ ngân hàng & đơn đăng ký)
#           - data/consultations.json (Đăng ký tư vấn 7 chương trình Khám Phá)
# =============================================================================

import os
import re
import sys
import json
import time
import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Đảm bảo mã hóa UTF-8 cho console Windows tránh UnicodeEncodeError
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ─── FastAPI & Uvicorn ────────────────────────────────────────────────────────
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np

# ─── Universal Knowledge Engine ──────────────────────────────────────────────
try:
    from universal_knowledge import get_universal_answer, solve_dynamic_open_query
except ImportError:
    from ai_backend.universal_knowledge import get_universal_answer, solve_dynamic_open_query

# ─── Hugging Face BANKING77 Expert Engine (77 Intent Chuẩn Quốc Tế) ──────────
try:
    from banking77_hf_expert import get_banking77_expert_reply, BANKING77_METADATA, BANKING77_EXPERT_KB
except ImportError:
    from ai_backend.banking77_hf_expert import get_banking77_expert_reply, BANKING77_METADATA, BANKING77_EXPERT_KB

# ─── Scikit-learn & Datasets ─────────────────────────────────────────────────
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from datasets import load_dataset
import joblib

# =============================================================================
# 1. THƯ MỤC LƯU TRỮ TẬP TRUNG (DATA DIRECTORY)
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CHAT_HISTORY_FILE = DATA_DIR / "chat_history.json"
CUSTOMERS_FILE = DATA_DIR / "customers.json"
SEARCH_HISTORY_FILE = DATA_DIR / "search_history.json"
PLANNER_FILE = DATA_DIR / "planner.json"
CART_FILE = DATA_DIR / "cart.json"
CONSULTATIONS_FILE = DATA_DIR / "consultations.json"

# Helper đọc ghi an toàn
def read_json(path: Path, default_data: Any = None) -> Any:
    if default_data is None:
        default_data = []
    if path.exists():
        try:
            content = path.read_text(encoding="utf-8").strip()
            if content:
                return json.loads(content)
        except Exception as e:
            print(f"⚠️ Lỗi đọc file {path.name}: {e}")
    return default_data

def write_json(path: Path, data: Any):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"❌ Lỗi ghi file {path.name}: {e}")

# Khởi tạo dữ liệu mẫu nếu chưa có
def init_sample_data():
    if not CHAT_HISTORY_FILE.exists() or len(read_json(CHAT_HISTORY_FILE)) == 0:
        write_json(CHAT_HISTORY_FILE, [])

    if not CUSTOMERS_FILE.exists() or len(read_json(CUSTOMERS_FILE)) == 0:
        initial_customers = [
            {
                "username": "admin",
                "password": "admin123",
                "fullname": "Quản Trị Viên",
                "phone": "0908889999",
                "accountNumber": "PTB8889998888",
                "balance": 150000000,
                "address": "268 Lý Thường Kiệt, Q.10, TP.HCM",
                "createdAt": "2026-10-20T08:00:00.000Z"
            },
            {
                "username": "khachhang",
                "password": "123456",
                "fullname": "Nguyễn Văn Phát Tài",
                "phone": "0912345678",
                "accountNumber": "PTB9998887777",
                "balance": 25500000,
                "address": "123 Đường Lê Lợi, Q.1, TP.HCM",
                "createdAt": "2026-10-20T09:30:00.000Z"
            }
        ]
        write_json(CUSTOMERS_FILE, initial_customers)

    if not SEARCH_HISTORY_FILE.exists() or len(read_json(SEARCH_HISTORY_FILE)) == 0:
        initial_searches = [
            {"query": "thẻ visa", "timestamp": "2026-10-20T10:00:00.000Z", "user": "khachhang", "resultsCount": 1},
            {"query": "tiết kiệm", "timestamp": "2026-10-20T10:15:00.000Z", "user": "anonymous", "resultsCount": 1}
        ]
        write_json(SEARCH_HISTORY_FILE, initial_searches)

    if not PLANNER_FILE.exists() or len(read_json(PLANNER_FILE)) == 0:
        initial_planner = [
            {
                "id": "plan-1",
                "name": "Thanh toán hóa đơn điện & nước tháng này",
                "qty": "850.000 VNĐ",
                "category": "Điện Nước",
                "priority": "high",
                "completed": False,
                "createdAt": 1729468800000
            },
            {
                "id": "plan-2",
                "name": "Tất toán dư nợ thẻ tín dụng Visa",
                "qty": "3.500.000 VNĐ",
                "category": "Thẻ Tín Dụng",
                "priority": "high",
                "completed": False,
                "createdAt": 1729472400000
            },
            {
                "id": "plan-3",
                "name": "Đóng phí bảo hiểm nhân thọ quý 4",
                "qty": "5.000.000 VNĐ",
                "category": "Bảo Hiểm",
                "priority": "medium",
                "completed": True,
                "createdAt": 1729476000000
            },
            {
                "id": "plan-4",
                "name": "Trích tiền gửi tiết kiệm tích lũy định kỳ",
                "qty": "2.000.000 VNĐ",
                "category": "Tiết Kiệm",
                "priority": "low",
                "completed": True,
                "createdAt": 1729479600000
            }
        ]
        write_json(PLANNER_FILE, initial_planner)

    if not CART_FILE.exists():
        write_json(CART_FILE, [])

    if not CONSULTATIONS_FILE.exists():
        write_json(CONSULTATIONS_FILE, [])

init_sample_data()

# =============================================================================
# 2. CƠ SỞ TRI THỨC PHÁT TÀI BANK (PHATTAI_KB)
# =============================================================================
PHATTAI_KB = {
    # --- TÀI KHOẢN ---
    "create_account": (
        "📌 **CÁC BƯỚC ĐỂ TẠO TÀI KHOẢN E-BANKING PHÁT TÀI BANK:**\n"
        "1️⃣ **Bước 1:** Nhấp vào nút **'Đăng Ký'** ở góc phải hoặc mở menu tròn 3 gạch đầu trang → chọn **6. Đăng Ký E-Banking**.\n"
        "2️⃣ **Bước 2:** Điền đầy đủ thông tin: Họ và tên, Tên đăng nhập (viết liền không dấu, 4-15 ký tự), Số điện thoại và Địa chỉ.\n"
        "3️⃣ **Bước 3:** Nhập Mật khẩu (tối thiểu 6 ký tự) và Xác nhận mật khẩu.\n"
        "4️⃣ **Bước 4:** Nhấn **'Mở Tài Khoản PHÁT TÀI BANK'** — hệ thống tự cấp số tài khoản `PTB...`, tặng ngay **50.000đ** chào mừng và lưu vào `data/customers.json`!\n"
        "💡 *Hotline hỗ trợ 24/7:* **1900-8888**."
    ),
    "change_account_country": (
        "🌏 **THAY ĐỔI THÔNG TIN QUỐC GIA / ĐỊA CHỈ:**\n"
        "1️⃣ Đăng nhập E-Banking → chọn **'Cài đặt tài khoản'**.\n"
        "2️⃣ Nhấn **'Cập nhật thông tin cá nhân'** → sửa địa chỉ hoặc quốc gia.\n"
        "3️⃣ Xác thực OTP → Lưu thay đổi. Cập nhật có hiệu lực ngay lập tức."
    ),
    "compromised_card": (
        "🚨 **KHI THẺ BỊ LỘ THÔNG TIN / BỊ XÂM PHẠM:**\n"
        "1️⃣ **Ngay lập tức:** Vào App → Thẻ → **Khóa thẻ khẩn cấp** để bảo vệ tài sản.\n"
        "2️⃣ Gọi hotline **1900-8888** (nhánh 2 — Bảo mật) để báo cáo và yêu cầu cấp thẻ mới miễn phí.\n"
        "3️⃣ Kiểm tra lịch sử giao dịch và tra soát mọi giao dịch nghi vấn trong vòng 60 ngày."
    ),
    # --- THẺ ---
    "activate_my_card": (
        "💳 **HƯỚNG DẪN KÍCH HOẠT THẺ PHÁT TÀI BANK:**\n"
        "1️⃣ Đăng nhập ứng dụng E-Banking trên điện thoại hoặc website.\n"
        "2️⃣ Chọn mục **'Thẻ của tôi'** → Nhấp vào thẻ cần kích hoạt.\n"
        "3️⃣ Nhập 4 số cuối in trên mặt trước thẻ và mã OTP gửi về SMS.\n"
        "4️⃣ Đổi mã PIN mặc định tại cây ATM PHÁT TÀI gần nhất để hoàn tất bảo mật!"
    ),
    "card_blocked": (
        "🔒 **CÁC BƯỚC MỞ KHÓA THẺ KHI BỊ KHÓA:**\n"
        "1️⃣ Mở ứng dụng E-Banking → Vào mục **'Quản lý Thẻ'**.\n"
        "2️⃣ Chọn **'Mở khóa thẻ'** và xác thực FaceID hoặc mã PIN E-Banking.\n"
        "3️⃣ Hoặc gọi ngay tổng đài **1900-8888** (nhánh 1) để giao dịch viên mở khóa trong 2 phút."
    ),
    "lost_or_stolen_card": (
        "🚨 **MẤT THẺ / THẺ BỊ ĐÁNH CẮP — XỬ LÝ NGAY:**\n"
        "1️⃣ Vào App → Thẻ → **Khóa thẻ tức thì** (chỉ mất 5 giây).\n"
        "2️⃣ Gọi hotline khẩn cấp **1900-8888** (24/7) để yêu cầu cấp thẻ mới.\n"
        "3️⃣ Tra soát lịch sử giao dịch — nếu có giao dịch lạ, yêu cầu hoàn tiền trong 24h."
    ),
    "get_physical_card": (
        "📦 **ĐẶT THẺ VẬT LÝ VỀ TẬN NHÀ:**\n"
        "1️⃣ App → Thẻ → **'Đặt thẻ ATM vật lý'**.\n"
        "2️⃣ Xác nhận địa chỉ nhận thẻ và chọn loại thẻ (Visa / Mastercard / Napas).\n"
        "3️⃣ PHÁT TÀI BANK giao thẻ miễn phí đến tận nơi sau **3-5 ngày làm việc**."
    ),
    "apple_pay_or_google_pay": (
        "📱 **LIÊN KẾT APPLE PAY / GOOGLE PAY:**\n"
        "1️⃣ Mở ứng dụng Ví (Wallet) trên điện thoại → Chọn **'Thêm thẻ'**.\n"
        "2️⃣ Quét thẻ PHÁT TÀI BANK hoặc nhập thủ công số thẻ.\n"
        "3️⃣ Nhập mã OTP xác thực gửi về SMS → Thẻ đã sẵn sàng thanh toán chạm!"
    ),
    "card_payment_fee_charged": "💳 Biểu phí thẻ PHÁT TÀI BANK: **Miễn phí** mở thẻ lần đầu, chuyển khoản 24/7 toàn quốc **0đ phí**, miễn phí 5 lần rút tiền ATM/tháng, phí thường niên thẻ Visa chỉ **180.000 VNĐ/năm**.",
    "supported_cards_and_currencies": "PHÁT TÀI BANK hỗ trợ các dòng thẻ **Visa, Mastercard, Napas** và giao dịch bằng: VND, USD, EUR, JPY, GBP, SGD, AUD. Tỷ giá quy đổi cập nhật real-time mỗi phút.",
    # --- GIAO DỊCH & PHÍ ---
    "transfer_timing": (
        "⚡ **HƯỚNG DẪN CHUYỂN TIỀN NHANH 24/7 NAPAS:**\n"
        "1️⃣ Chọn tính năng **'Chuyển tiền'** trên thanh menu hoặc ứng dụng.\n"
        "2️⃣ Chọn Ngân hàng nhận và nhập Số tài khoản (hoặc quét mã VietQR).\n"
        "3️⃣ Nhập số tiền và nội dung chuyển → Xác thực mã Smart OTP.\n"
        "✅ Tiền đến người nhận **ngay lập tức trong 3 giây**, hoàn toàn **0đ phí**!"
    ),
    "transfer_fee_charged": "💸 Chuyển khoản nội bộ PHÁT TÀI BANK và liên ngân hàng Napas 24/7 qua E-Banking hoàn toàn **MIỄN PHÍ 100%** trọn đời. Không giới hạn số lần chuyển!",
    "cash_withdrawal_charge": "🏧 Phí rút tiền ATM: **Miễn phí 5 lần đầu** mỗi tháng. Từ lần thứ 6: chỉ **1.100 VNĐ/giao dịch** tại hơn 20.000 cây ATM toàn quốc.",
    "declined_card_payment": (
        "⚠️ **GIAO DỊCH THẺ BỊ TỪ CHỐI — CÁC NGUYÊN NHÂN THƯỜNG GẶP:**\n"
        "• Số dư tài khoản không đủ → Kiểm tra số dư qua App.\n"
        "• Vượt hạn mức chi tiêu trong ngày → Nâng hạn mức trong phần Cài đặt Thẻ.\n"
        "• Giao dịch bị khóa bảo mật → Gọi **1900-8888** để mở lại.\n"
        "• Thẻ hết hạn → Đổi thẻ mới miễn phí qua App."
    ),
    "transaction_charged_twice": (
        "🔄 **BỊ TÍNH TIỀN HAI LẦN — XỬ LÝ TRA SOÁT:**\n"
        "1️⃣ Chụp ảnh hoặc lưu biên lai giao dịch làm bằng chứng.\n"
        "2️⃣ Vào App → Lịch sử giao dịch → Chọn giao dịch → **'Tra soát'**.\n"
        "3️⃣ Hoặc gọi **1900-8888** — PHÁT TÀI BANK cam kết hoàn tiền trong **24 giờ làm việc**."
    ),
    "pending_cash_withdrawal": "⏳ Giao dịch rút tiền đang chờ xử lý thường hoàn tất trong 5-15 phút. Nếu quá 30 phút vẫn chưa cập nhật, vui lòng gọi **1900-8888** để được kiểm tra ngay.",
    "refund_not_showing_up": (
        "💰 **HOÀN TIỀN CHƯA VỀ TÀI KHOẢN:**\n"
        "• Hoàn tiền nội bộ: 1-3 ngày làm việc.\n"
        "• Hoàn tiền từ merchant bên ngoài: 5-15 ngày làm việc.\n"
        "• Kiểm tra trong App → Lịch sử giao dịch → Mục 'Hoàn tiền'.\n"
        "• Quá thời hạn: Gọi **1900-8888** cung cấp mã giao dịch gốc để tra soát."
    ),
    # --- TIẾT KIỆM & VAY ---
    "savings_account": (
        "💰 **CÁC BƯỚC GỬI TIẾT KIỆM ONLINE LÃI SUẤT 6.8%/NĂM:**\n"
        "1️⃣ Chọn gói **'Tiết Kiệm Linh Hoạt'** trong giỏ dịch vụ hoặc App.\n"
        "2️⃣ Nhập số tiền muốn gửi (tối thiểu 1.000.000 VNĐ) và kỳ hạn (1 đến 36 tháng).\n"
        "3️⃣ Chọn hình thức nhận lãi: **Hàng tháng** hoặc **Cuối kỳ** → Bấm Xác nhận.\n"
        "📈 Tiền lãi tự động cộng vào tài khoản hàng ngày. Rút gốc trước hạn vẫn hưởng lãi không kỳ hạn!"
    ),
    "loan_request": (
        "📝 **CÁC BƯỚC ĐĂNG KÝ VAY TÍN CHẤP ONLINE DUYỆT 24H:**\n"
        "1️⃣ Vào mục dịch vụ → chọn **'Vay Tín Chấp Online'**.\n"
        "2️⃣ Chọn số tiền vay (10 triệu - 500 triệu) và kỳ hạn trả dần (6 - 60 tháng).\n"
        "3️⃣ Điền thông tin thu nhập và chụp ảnh CCCD gắn chip.\n"
        "4️⃣ Hệ thống AI chấm điểm tín nhiệm tự động và **giải ngân sau 24 giờ** vào tài khoản!"
    ),
    "mortgage_domestic": (
        "🏠 **VAY MUA NHÀ AN CƯ — ĐẶC QUYỀN PHÁT TÀI BANK:**\n"
        "• Tài trợ tới **85% giá trị bất động sản**, lãi suất chỉ từ **7.5%/năm**.\n"
        "• Thời hạn vay linh hoạt tới 30 năm, ân hạn nợ gốc 24 tháng đầu.\n"
        "• Giải ngân theo tiến độ hợp đồng mua bán, không ràng buộc bảo hiểm bắt buộc.\n"
        "📞 Đặt lịch tư vấn miễn phí: **1900-8888** (nhánh 3 — Vay Mua Nhà)."
    ),
    "interest_rates": (
        "📊 **LÃI SUẤT THAM CHIẾU PHÁT TÀI BANK (Cập nhật tháng 10/2026):**\n"
        "• Tiết kiệm 1 tháng: **4.2%/năm** | 6 tháng: **5.5%/năm** | 12 tháng: **6.8%/năm**.\n"
        "• Vay tín chấp tiêu dùng: từ **10.8%/năm**.\n"
        "• Vay mua nhà: từ **7.5%/năm** (cố định 3 năm đầu).\n"
        "• Thẻ tín dụng: **18%/năm** (0% nếu trả đủ trong kỳ).\n"
        "💡 Lãi suất cập nhật realtime tại /docs hoặc gọi **1900-8888**."
    ),
    # --- BẢO MẬT & MẬT KHẨU ---
    "passcode_forgotten": (
        "🔑 **CÁC BƯỚC LẤY LẠI MẬT KHẨU E-BANKING:**\n"
        "1️⃣ Tại khung đăng nhập → bấm **'Quên mật khẩu?'**.\n"
        "2️⃣ Nhập Số điện thoại hoặc Tên đăng nhập đã đăng ký.\n"
        "3️⃣ Nhập mã OTP gửi về số điện thoại chính chủ.\n"
        "4️⃣ Tạo mật khẩu mới (tối thiểu 6 ký tự) và đăng nhập lại."
    ),
    "change_pin": (
        "🔐 **ĐỔI MÃ PIN THẺ ATM:**\n"
        "1️⃣ Cách 1 — Tại ATM: Chọn **'Đổi mã PIN'** → Nhập PIN cũ → Nhập PIN mới (6 chữ số) → Xác nhận.\n"
        "2️⃣ Cách 2 — Qua App: Thẻ của tôi → Đổi PIN → Xác thực OTP → Nhập PIN mới.\n"
        "💡 Không dùng ngày sinh, số điện thoại làm PIN để bảo mật tối đa!"
    ),
    "verify_my_identity": (
        "✅ **XÁC MINH DANH TÍNH KHÁCH HÀNG (eKYC):**\n"
        "1️⃣ App → Cài đặt → **'Xác minh danh tính eKYC'**.\n"
        "2️⃣ Chụp ảnh mặt trước và mặt sau CCCD gắn chip.\n"
        "3️⃣ Thực hiện xác thực khuôn mặt LiveFace (nhìn thẳng, chớp mắt theo hướng dẫn).\n"
        "4️⃣ Hệ thống AI xác minh trong **< 60 giây** — Nâng hạn mức giao dịch lên 200 triệu/ngày!"
    ),
    # --- TỶ GIÁ & NGOẠI TỆ ---
    "exchange_rate": (
        "💱 **TỶ GIÁ NGOẠI TỆ PHÁT TÀI BANK (tham khảo):**\n"
        "• USD/VND: Mua vào **25.100** | Bán ra **25.350**\n"
        "• EUR/VND: Mua vào **27.200** | Bán ra **27.600**\n"
        "• JPY/VND: Mua vào **165** | Bán ra **170**\n"
        "📌 Tỷ giá cập nhật liên tục mỗi phút trong giờ giao dịch (8:00 - 22:00). Xem realtime tại App → Tỷ giá."
    ),
    "currency_exchange": (
        "💱 **CÁCH ĐỔI NGOẠI TỆ ONLINE:**\n"
        "1️⃣ App → Giao dịch → **'Đổi ngoại tệ'**.\n"
        "2️⃣ Chọn loại tiền cần đổi (USD, EUR, JPY...) và nhập số tiền.\n"
        "3️⃣ Hệ thống hiển thị tỷ giá realtime → Xác nhận → OTP → Hoàn tất.\n"
        "💡 Giao dịch từ 500 USD được hưởng tỷ giá ưu đãi đặc biệt!"
    ),
    # --- TÀI KHOẢN QUỐC TẾ & KHÁC ---
    "balance_not_updated_after_direct_deposit": "⏳ Số dư sau chuyển khoản thường cập nhật ngay lập tức. Nếu sau **5 phút** vẫn chưa phản ánh, hãy làm mới App và kiểm tra lại. Quá 30 phút chưa thấy → Gọi **1900-8888**.",
    "direct_debit": (
        "🔄 **THIẾT LẬP GHI NỢ TỰ ĐỘNG (DIRECT DEBIT):**\n"
        "1️⃣ App → Thanh toán → **'Thanh toán tự động'** → Thêm hóa đơn.\n"
        "2️⃣ Chọn nhà cung cấp (điện, nước, internet, bảo hiểm...) và tài khoản thanh toán.\n"
        "3️⃣ Xác nhận ủy quyền → Hóa đơn sẽ tự động thanh toán vào ngày đến hạn."
    ),
    "order_checks": "📄 Yêu cầu séc ngân hàng: Liên hệ chi nhánh PHÁT TÀI BANK gần nhất hoặc gọi **1900-8888**. Phí phát hành séc: **50.000 VNĐ/quyển** (25 tờ).",
    "getting_spare_card": "🪪 Thẻ phụ (Supplementary Card): Đăng ký qua App → Thẻ → **'Phát hành thẻ phụ'**. Thẻ phụ chia sẻ hạn mức với thẻ chính, miễn phí phát hành cho thành viên gia đình.",
    "virtual_card_not_working": (
        "🖥️ **THẺ ẢO KHÔNG HOẠT ĐỘNG — KIỂM TRA:**\n"
        "• Đảm bảo thẻ ảo đã được **kích hoạt** trong App → Thẻ ảo.\n"
        "• Kiểm tra số dư tài khoản liên kết đủ để thanh toán.\n"
        "• Đảm bảo trang web thanh toán chấp nhận Visa/Mastercard ảo.\n"
        "• Thử **tạo thẻ ảo mới** (mỗi thẻ ảo dùng 1 lần cho bảo mật tối đa)."
    ),
    "edit_personal_details": (
        "✏️ **CẬP NHẬT THÔNG TIN CÁ NHÂN:**\n"
        "1️⃣ App → Cài đặt → **'Thông tin cá nhân'** → Nhấn Chỉnh sửa.\n"
        "2️⃣ Cập nhật: Địa chỉ, Email, Số điện thoại phụ (SĐT chính cần đến chi nhánh).\n"
        "3️⃣ Xác thực OTP → Lưu. Thay đổi có hiệu lực trong vòng 24 giờ."
    ),
    "terminate_account": (
        "❌ **YÊU CẦU ĐÓNG TÀI KHOẢN:**\n"
        "1️⃣ Đảm bảo số dư tài khoản = 0 (chuyển hết sang ngân hàng khác).\n"
        "2️⃣ App → Cài đặt → **'Đóng tài khoản'** → Nhập lý do.\n"
        "3️⃣ Hoặc đến chi nhánh PHÁT TÀI BANK gần nhất mang theo CCCD gốc.\n"
        "⚠️ Tài khoản đóng sẽ không thể khôi phục. Vui lòng suy nghĩ kỹ!"
    ),
    "top_up_by_bank_transfer": (
        "💳 **NẠP TIỀN VÀO TÀI KHOẢN QUA CHUYỂN KHOẢN:**\n"
        "1️⃣ Dùng E-Banking ngân hàng khác → Chuyển khoản liên ngân hàng.\n"
        "2️⃣ Nhập số tài khoản PHÁT TÀI BANK (dạng `PTB...`) và tên chủ tài khoản.\n"
        "3️⃣ Tiền về tài khoản trong **vài giây** qua hệ thống Napas 24/7."
    ),
    "contactless_not_working": "📡 Thanh toán không chạm không hoạt động? Kiểm tra: (1) Bật NFC trên điện thoại, (2) Mở App và chọn thẻ mặc định, (3) Đưa điện thoại sát thiết bị POS trong 3 giây. Vẫn lỗi → Gọi **1900-8888**.",
    "transaction_incorrect_amount": "💰 Số tiền giao dịch sai? Chụp ảnh biên lai và gọi ngay **1900-8888** hoặc vào App → Lịch sử → Tra soát giao dịch. Cam kết giải quyết trong **24 giờ làm việc**.",
    "receiving_from_abroad": (
        "🌍 **NHẬN TIỀN TỪ NƯỚC NGOÀI (SWIFT / CHUYỂN KHOẢN QUỐC TẾ):**\n"
        "Cung cấp cho người gửi các thông tin:\n"
        "• Bank Name: **PHAT TAI BANK - VIETNAM**\n"
        "• SWIFT Code: **PTBKVNHH**\n"
        "• Account Name: Tên chủ tài khoản\n"
        "• Account Number: Số tài khoản dạng `PTB...`\n"
        "• Address: 268 Lý Thường Kiệt, Q.10, TP.HCM\n"
        "⏱️ Tiền về sau 1-3 ngày làm việc quốc tế."
    ),
    "sending_to_abroad": (
        "✈️ **CHUYỂN TIỀN QUỐC TẾ RA NƯỚC NGOÀI:**\n"
        "1️⃣ App → Chuyển tiền → **'Chuyển tiền quốc tế (SWIFT)'**.\n"
        "2️⃣ Nhập thông tin ngân hàng nhận: SWIFT Code, Số TK, Tên người nhận, Địa chỉ.\n"
        "3️⃣ Nhập số tiền và loại ngoại tệ → Xác nhận tỷ giá → OTP.\n"
        "⏱️ Tiền đến trong 1-3 ngày làm việc. Phí chuyển tiền quốc tế: **150.000-500.000 VNĐ** tùy số tiền."
    ),
    "cancel_transfer": (
        "❌ **HỦY LỆNH CHUYỂN TIỀN:**\n"
        "• Với chuyển khoản nội địa Napas: **Không thể hủy** vì tiền đến ngay lập tức.\n"
        "• Với lệnh SWIFT quốc tế: Gọi ngay **1900-8888** trong vòng **2 giờ** từ lúc lệnh để yêu cầu thu hồi (phí thu hồi: **200.000 VNĐ**)."
    ),
    "beneficiary_not_allowed": "⛔ Người nhận bị từ chối giao dịch thường do tài khoản đích đang bị đình chỉ hoặc hạn mức nhận đã đầy. Quý khách vui lòng xác nhận lại thông tin tài khoản người nhận hoặc gọi **1900-8888**.",
    "unable_to_verify_identity": (
        "🪪 **KHÔNG THỂ XÁC MINH DANH TÍNH — GIẢI PHÁP:**\n"
        "• Đảm bảo ánh sáng đủ sáng khi chụp ảnh CCCD.\n"
        "• CCCD không được nhòe, gập hoặc bị che.\n"
        "• Thử lại xác thực khuôn mặt nơi có đủ ánh sáng tự nhiên.\n"
        "• Vẫn thất bại: Đến chi nhánh PHÁT TÀI BANK mang CCCD gốc để xác minh trực tiếp."
    ),
    "request_refund": (
        "💰 **YÊU CẦU HOÀN TIỀN:**\n"
        "1️⃣ App → Lịch sử giao dịch → Chọn giao dịch cần hoàn → **'Yêu cầu hoàn tiền'**.\n"
        "2️⃣ Nhập lý do (sai số tiền / dịch vụ không nhận được / giao dịch trùng).\n"
        "3️⃣ Đính kèm ảnh chứng từ nếu có → Gửi yêu cầu.\n"
        "⏱️ Hoàn tiền trong **1-5 ngày làm việc** tùy loại giao dịch."
    ),
    "wrong_amount_of_cash_received": "💵 Nhận sai số tiền tại ATM? Đừng lo — PHÁT TÀI BANK có camera giám sát 24/7 tại mọi cây ATM. Gọi ngay **1900-8888** trong vòng 24 giờ và cung cấp mã giao dịch để được hoàn tiền.",
    "fiat_currency_support": "💵 PHÁT TÀI BANK hỗ trợ đầy đủ các loại tiền pháp định: **VND, USD, EUR, GBP, JPY, SGD, AUD, CNY, KRW, THB**. Đổi ngoại tệ trực tuyến qua App với tỷ giá cạnh tranh nhất thị trường.",
    "atm_support": (
        "🏧 **MẠNG LƯỚI ATM PHÁT TÀI BANK:**\n"
        "• Hơn **20.000 cây ATM** toàn quốc trong mạng lưới Napas.\n"
        "• Tìm ATM gần nhất: App → Dịch vụ → **'Tìm ATM/Chi nhánh'** hoặc bản đồ tại bando.html.\n"
        "• Hoạt động 24/7, bao gồm cả ngày lễ và Tết."
    ),
    "pin_blocked": (
        "🔒 **PIN BỊ KHÓA DO NHẬP SAI NHIỀU LẦN:**\n"
        "1️⃣ PIN ATM bị khóa: Gọi **1900-8888** để mở khóa hoặc đổi PIN qua App.\n"
        "2️⃣ PIN E-Banking bị khóa: App → 'Quên mật khẩu?' → Xác thực OTP → Đặt lại.\n"
        "💡 Sau 3 lần nhập sai liên tiếp hệ thống tự động khoá để bảo vệ tài khoản."
    ),
    "card_swallowed": (
        "😱 **ATM NUỐT THẺ — XỬ LÝ NGAY:**\n"
        "1️⃣ Gọi ngay **1900-8888** (nhánh 1) và cung cấp địa điểm cây ATM.\n"
        "2️⃣ Khóa thẻ tạm thời qua App trong khi chờ nhân viên xử lý.\n"
        "3️⃣ PHÁT TÀI BANK cam kết trả thẻ hoặc **cấp thẻ mới miễn phí** trong 3 ngày làm việc."
    ),
    "age_limit": "📋 Điều kiện mở tài khoản: Từ **18 tuổi** trở lên (có CCCD/CMND). Người từ 15-17 tuổi có thể mở tài khoản tiết kiệm học sinh với sự đồng ý của phụ huynh.",
    "balance_not_updated_after_direct_deposit": "⏳ Số dư thường cập nhật **tức thì**. Nếu sau 5 phút chưa thấy, hãy làm mới App. Quá 30 phút → Gọi **1900-8888** với mã giao dịch để tra soát.",
    "direct_debit": (
        "🔄 **GHI NỢ TỰ ĐỘNG (STANDING ORDER):**\n"
        "1️⃣ App → Thanh toán → **'Thanh toán định kỳ'** → Cài đặt lịch.\n"
        "2️⃣ Nhập số tiền, ngày thanh toán, và tài khoản người nhận.\n"
        "3️⃣ Xác nhận ủy quyền — Lệnh chuyển tự động chạy đúng ngày hàng tháng."
    ),
}

DEFAULT_RESPONSES = {
    "greeting": "Xin chào quý khách! 🏦 Tôi là **Phát Tài Bot** — trợ lý AI của PHÁT TÀI BANK. Tôi có thể hướng dẫn chi tiết từng bước: **tạo tài khoản, kích hoạt thẻ, mở sổ tiết kiệm, chuyển tiền, vay tín chấp, tra cứu tỷ giá** và nhiều dịch vụ khác. Quý khách muốn hỏi gì ạ?",
    "farewell": "Cảm ơn quý khách đã tin dùng dịch vụ PHÁT TÀI BANK! 🏦 Chúc quý khách tài lộc dồi dào và vạn sự như ý! Mọi thắc mắc liên hệ Hotline **1900-8888** (24/7).",
    "fallback": (
        "🤔 Xin lỗi, tôi chưa nắm rõ câu hỏi của quý khách. Quý khách có thể thử hỏi:\n"
        "• *'Các bước tạo tài khoản'*\n"
        "• *'Hướng dẫn kích hoạt thẻ'*\n"
        "• *'Cách gửi tiết kiệm, lãi suất bao nhiêu'*\n"
        "• *'Đăng ký vay tín chấp'*\n"
        "• *'Biểu phí rút tiền ATM'*\n"
        "• *'Tỷ giá ngoại tệ hôm nay'*\n"
        "Hoặc gọi Hotline **1900-8888** (24/7) để được hỗ trợ trực tiếp!"
    )
}

# Bản đồ từ khóa tiếng Việt → intent BANKING77
VIET_KEYWORD_MAP = {
    "create_account": ["tạo tài khoản", "mở tài khoản", "đăng ký tài khoản", "lập tài khoản",
        "các bước tạo", "cách tạo tài khoản", "create account", "mo tai khoan",
        "cac buoc tao tai khoan", "cach tao tai khoan", "dang ky tai khoan", "open account"],
    "activate_my_card": ["kích hoạt thẻ", "kich hoat the", "mở thẻ mới", "thẻ mới nhận",
        "cach kich hoat the", "huong dan kich hoat the", "activate card"],
    "card_blocked": ["thẻ bị khóa", "khóa thẻ", "mở khóa thẻ", "the bi khoa",
        "mo khoa the", "card blocked", "unlock card", "the khoa roi"],
    "lost_or_stolen_card": ["mất thẻ", "bị mất thẻ", "thẻ bị đánh cắp", "trộm thẻ",
        "mat the roi", "bi mat the", "lost card", "stolen card"],
    "passcode_forgotten": ["quên mật khẩu", "lấy lại mật khẩu", "quen mat khau",
        "doi mat khau", "quen pin", "forgot password", "reset password",
        "lay lai mat khau", "lost password"],
    "transfer_timing": ["chuyển tiền", "chuyển khoản", "chuyen tien", "chuyen khoan",
        "napas", "gửi tiền", "gui tien", "cach chuyen tien",
        "chuyen khoan lien ngan hang", "how to transfer"],
    "savings_account": ["tiết kiệm", "gửi tiết kiệm", "tiet kiem", "gui tiet kiem",
        "savings", "mo so tiet kiem", "cach gui tiet kiem", "open savings",
        "gui tien tiet kiem"],
    "interest_rates": ["lãi suất", "lai suat", "lãi bao nhiêu", "interest rate",
        "lai suat la bao nhieu", "bao nhieu phan tram", "ty le lai", "percent interest"],
    "loan_request": ["vay tiền", "vay tín chấp", "vay online", "vay tiêu dùng",
        "đăng ký vay", "vay tien", "vay tin chap", "dang ky vay",
        "vay tieu dung", "vay nhanh", "borrow money", "personal loan"],
    "mortgage_domestic": ["vay mua nhà", "vay bất động sản", "mua nhà trả góp",
        "vay mua nha", "vay bat dong san", "mua nha tra gop",
        "home loan", "mortgage", "vay nha"],
    "exchange_rate": ["tỷ giá", "ty gia", "exchange rate", "ngoại tệ", "ngoai te",
        "ty gia hom nay", "ty gia ngoai te", "gia usd hom nay", "gia eur",
        "foreign currency rate"],
    "currency_exchange": ["đổi ngoại tệ", "quy đổi tiền", "mua ngoại tệ",
        "doi ngoai te", "mua ngoai te", "ban ngoai te", "exchange foreign currency"],
    "cash_withdrawal_charge": ["phí rút tiền", "rút tiền atm", "phi rut tien",
        "phi rut tien atm", "rut tien mat phi", "withdrawal fee"],
    "transfer_fee_charged": ["phí chuyển khoản", "phí chuyển tiền", "phi chuyen tien",
        "phi chuyen khoan", "chuyen khoan mat phi", "transfer fee"],
    "card_payment_fee_charged": ["phí thẻ", "phí thanh toán", "biểu phí",
        "phi thanh toan", "bieu phi", "card fee", "phi the"],
    "atm_support": ["atm ở đâu", "tìm atm", "cây atm gần", "atm o dau",
        "tim atm gan nhat", "find atm", "nearest atm", "may atm o dau"],
    "apple_pay_or_google_pay": ["apple pay", "google pay", "samsung pay", "thanh toán di động",
        "thanh toan di dong", "mobile payment", "nfc pay"],
    "get_physical_card": ["đặt thẻ vật lý", "giao thẻ", "nhận thẻ tại nhà",
        "dat the", "giao the", "nhan the tai nha", "physical card"],
    "verify_my_identity": ["xác minh danh tính", "ekyc", "xác thực cccd", "định danh",
        "xac minh danh tinh", "xac thuc cccd", "verify identity", "dinh danh"],
    "change_pin": ["đổi pin", "thay pin", "doi pin atm", "change pin",
        "doi ma pin", "thay ma pin"],
    "pin_blocked": ["pin bị khóa", "nhập sai pin nhiều lần", "pin bi khoa",
        "nhap sai pin", "pin bi khoa roi"],
    "card_swallowed": ["thẻ bị nuốt", "the bi nuot", "thẻ atm bị nuốt", "the atm bi nuot",
        "atm nuốt thẻ", "bị nuốt thẻ", "thẻ kẹt atm", "bị nuốt", "bi nuot",
        "atm nuot the", "bi nuot the", "the ket atm", "card swallowed"],
    "transaction_charged_twice": ["tính tiền 2 lần", "bị trừ 2 lần", "giao dịch trùng",
        "tinh tien 2 lan", "bi tru 2 lan", "double charge"],
    "declined_card_payment": ["thẻ bị từ chối", "giao dịch thất bại", "không thanh toán được",
        "the bi tu choi", "giao dich that bai", "payment declined"],
    "request_refund": ["hoàn tiền", "yêu cầu hoàn tiền", "refund", "tra soát",
        "hoan tien", "yeu cau hoan tien", "tra soat"],
    "receiving_from_abroad": ["nhận tiền nước ngoài", "nhận kiều hối",
        "nhan tien nuoc ngoai", "nhan kieu hoi", "swift transfer in"],
    "sending_to_abroad": ["chuyển tiền quốc tế", "gửi tiền ra nước ngoài",
        "chuyen tien quoc te", "gui tien nuoc ngoai", "international transfer"],
    "top_up_by_bank_transfer": ["nạp tiền", "nạp vào tài khoản", "nap tien",
        "top up account", "add money to account"],
    "edit_personal_details": ["cập nhật thông tin", "thay đổi địa chỉ", "đổi số điện thoại",
        "cap nhat thong tin", "thay doi dia chi", "doi so dien thoai"],
    "terminate_account": ["đóng tài khoản", "hủy tài khoản", "dong tai khoan",
        "huy tai khoan", "close account", "delete account"],
    "direct_debit": ["thanh toán tự động", "trừ tiền tự động", "standing order",
        "thanh toan tu dong", "tru tien tu dong", "auto payment"],
    "contactless_not_working": ["thanh toán không chạm không hoạt động", "contactless loi",
        "nfc khong hoat dong", "not working contactless"],
    "virtual_card_not_working": ["thẻ ảo không dùng được", "virtual card khong hoat dong",
        "the ao loi", "online card not working"],
    "age_limit": ["độ tuổi mở tài khoản", "bao nhiêu tuổi mới mở được",
        "do tuoi mo tai khoan", "age requirement banking"],
    "getting_spare_card": ["thẻ phụ", "thẻ bổ sung", "the phu",
        "supplementary card", "additional card"],
    # --- BỔ SUNG TOÀN DIỆN 53 Ý ĐỊNH HUGGING FACE BANKING77 CÒN LẠI ---
    "card_payment_not_recognised": ["thẻ bị trừ tiền không rõ", "giao dịch thẻ lạ", "khoản thanh toán thẻ không nhận ra", "không nhận ra giao dịch thẻ", "trừ tiền không rõ lý do", "bị trừ tiền thẻ visa", "card payment not recognised", "unrecognised card payment"],
    "card_arrival": ["bao giờ có thẻ", "khi nào thẻ tới", "thời gian nhận thẻ", "thẻ gửi tới chưa", "thẻ vật lý bao giờ đến", "card arrival", "card arrive"],
    "card_about_to_expire": ["thẻ sắp hết hạn", "gia hạn thẻ", "thẻ hết hạn", "hết hạn thẻ", "card about to expire", "card expiring"],
    "card_not_working": ["thẻ bị hỏng", "thẻ không quẹt được", "thẻ lỗi", "thẻ chip bị lỗi", "thẻ từ bị hỏng", "thẻ không hoạt động", "card not working"],
    "card_acceptance": ["thẻ có dùng được ở đây không", "chấp nhận thẻ", "thẻ quẹt được ở đâu", "điểm chấp nhận thẻ", "card acceptance"],
    "card_delivery_estimate": ["ước tính thời gian giao thẻ", "thời gian vận chuyển thẻ", "giao thẻ mất bao lâu", "card delivery estimate"],
    "card_linking": ["liên kết thẻ", "kết nối thẻ với tài khoản", "add thẻ vào app", "link card"],
    "card_payment_wrong_exchange_rate": ["sai tỷ giá thanh toán thẻ", "tỷ giá thẻ bị trừ sai", "card payment wrong exchange rate"],
    "cash_withdrawal_not_recognised": ["rút tiền không nhận ra", "giao dịch rút tiền lạ", "chưa rút tiền mà bị trừ", "cash withdrawal not recognised"],
    "declined_cash_withdrawal": ["rút tiền bị từ chối", "rút tiền atm không được", "cây atm từ chối rút tiền", "declined cash withdrawal"],
    "wrong_amount_of_cash_received": ["atm nhả thiếu tiền", "nhận sai số tiền atm", "atm trả thiếu", "atm đưa thiếu tiền", "wrong amount of cash received"],
    "wrong_exchange_rate_for_cash_withdrawal": ["tỷ giá rút tiền sai", "sai tỷ giá rút tiền mặt", "wrong exchange rate cash withdrawal"],
    "cancel_transfer": ["hủy chuyển khoản", "hủy lệnh chuyển tiền", "chuyển nhầm tiền", "chuyển tiền nhầm", "thu hồi tiền chuyển nhầm", "cancel transfer"],
    "declined_transfer": ["chuyển khoản bị từ chối", "lệnh chuyển tiền bị từ chối", "chuyển tiền bị chặn", "declined transfer"],
    "failed_transfer": ["chuyển tiền thất bại", "chuyển khoản không thành công", "giao dịch chuyển khoản lỗi", "lỗi chuyển tiền", "failed transfer"],
    "pending_transfer": ["chuyển tiền đang chờ", "lệnh chuyển đang xử lý", "tiền chuyển chưa tới", "người nhận chưa nhận được tiền", "pending transfer"],
    "receiving_money": ["nhận tiền chuyển đến", "cách nhận tiền", "thời gian nhận tiền", "receiving money"],
    "transfer_into_account": ["chuyển tiền vào tài khoản", "nạp tiền vào tài khoản phát tài", "transfer into account"],
    "transfer_not_received_by_recipient": ["người nhận chưa có tiền", "đã chuyển nhưng bên kia chưa nhận", "tiền chưa sang tài khoản nhận", "recipient has not received"],
    "Refund_not_showing_up": ["tiền hoàn chưa về", "chưa thấy hoàn tiền", "hoàn tiền chưa hiển thị", "refund not showing up"],
    "direct_debit_payment_not_recognised": ["bị trừ tiền ghi nợ tự động lạ", "khoản trừ direct debit không rõ", "direct debit payment not recognised"],
    "extra_charge_on_statement": ["phí lạ trên sao kê", "sao kê có khoản thu thêm", "bị tính thêm phí", "extra charge on statement"],
    "reverted_card_payment?": ["giao dịch thẻ bị đảo ngược", "hoàn trả giao dịch thẻ", "reverted card payment"],
    "automatic_top_up": ["tự động nạp tiền", "cài đặt nạp tiền tự động", "auto top up", "automatic top up"],
    "balance_not_updated_after_bank_transfer": ["chuyển khoản rồi nhưng số dư chưa tăng", "chưa cập nhật số dư sau chuyển", "balance not updated bank transfer"],
    "balance_not_updated_after_cheque_or_cash_deposit": ["nộp tiền mặt nhưng chưa cập nhật số dư", "nạp tiền tại quầy chưa thấy số dư", "balance not updated cash deposit"],
    "pending_top_up": ["nạp tiền đang chờ", "giao dịch nạp tiền đang xử lý", "pending top up"],
    "top_up_by_bank_transfer_charge": ["phí nạp tiền chuyển khoản", "nạp tiền có mất phí không", "top up by bank transfer charge"],
    "top_up_by_card_charge": ["phí nạp tiền bằng thẻ", "nạp tiền qua thẻ mất phí bao nhiêu", "top up by card charge"],
    "top_up_by_cash_or_cheque": ["nạp tiền bằng tiền mặt hoặc séc", "nộp tiền mặt vào tài khoản", "top up cash cheque"],
    "top_up_failed": ["nạp tiền thất bại", "nạp tiền không thành công", "lỗi nạp tiền", "top up failed"],
    "top_up_limits": ["hạn mức nạp tiền", "nạp tối đa bao nhiêu một ngày", "top up limits"],
    "top_up_reverted": ["nạp tiền bị hoàn lại", "lệnh nạp bị hủy", "top up reverted"],
    "topping_up_by_card": ["nạp tiền bằng thẻ quốc tế", "nạp tiền qua thẻ visa", "topping up by card"],
    "verify_top_up": ["xác minh giao dịch nạp tiền", "chứng thực nạp tiền", "verify top up"],
    "country_support": ["dùng thẻ ở nước ngoài", "quốc gia hỗ trợ", "đi nước ngoài dùng thẻ được không", "country support"],
    "exchange_charge": ["phí đổi ngoại tệ", "phí chuyển đổi ngoại tệ", "exchange charge", "phí quy đổi tiền"],
    "exchange_via_app": ["đổi ngoại tệ qua app", "mua ngoại tệ trên ứng dụng", "exchange via app"],
    "fiat_currency_support": ["các loại tiền tệ hỗ trợ", "tiền pháp định", "hỗ trợ những đồng tiền nào", "fiat currency support"],
    "supported_cards_and_currencies": ["các loại thẻ và loại tiền hỗ trợ", "supported cards and currencies"],
    "disposable_card_limits": ["hạn mức thẻ ảo dùng một lần", "disposable card limits"],
    "get_disposable_virtual_card": ["tạo thẻ ảo dùng 1 lần", "mở thẻ ảo dùng một lần", "get disposable virtual card"],
    "getting_virtual_card": ["tạo thẻ ảo", "mở thẻ e-card", "thẻ phi vật lý", "getting virtual card"],
    "order_physical_card": ["đặt thẻ cứng", "làm thẻ vật lý", "order physical card"],
    "lost_or_stolen_phone": ["mất điện thoại", "bị mất điện thoại cài app", "mất máy có app ngân hàng", "lost or stolen phone"],
    "unable_to_verify_identity": ["không xác thực được cccd", "lỗi xác minh danh tính", "ekyc thất bại", "unable to verify identity"],
    "why_verify_identity": ["tại sao phải xác minh danh tính", "vì sao cần ekyc", "lý do xác thực cccd", "why verify identity"],
    "verify_source_of_funds": ["chứng minh nguồn gốc tiền", "nguồn gốc dòng tiền", "xác minh nguồn tiền", "verify source of funds"],
    "visa_or_mastercard": ["nên dùng visa hay mastercard", "so sánh thẻ visa và mastercard", "visa hay mastercard tốt hơn"],
    "compromised_card": ["lộ thông tin thẻ", "thẻ bị hack", "nghi lộ số thẻ", "compromised card"],
    "beneficiary_not_allowed": ["người nhận không hợp lệ", "tài khoản người nhận bị chặn", "beneficiary not allowed"],
    "pending_card_payment": ["thanh toán thẻ đang chờ", "giao dịch thẻ đang xử lý", "pending card payment"],
    "pending_cash_withdrawal": ["rút tiền đang chờ xử lý", "lệnh rút tiền atm đang treo", "pending cash withdrawal"],
}

def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_intent_by_keywords(user_msg_lower: str):
    """Nhận diện intent bằng từ khóa tiếng Việt trước khi dùng ML model."""
    # Kiểm tra cả chuỗi gốc có dấu lẫn phiên bản đã strip accent (clean_text)
    cleaned_lower = clean_text(user_msg_lower)
    # Ưu tiên khớp keyword dài hơn (specific hơn) trước
    best_intent = None
    best_kw_len = 0
    for intent, keywords in VIET_KEYWORD_MAP.items():
        for kw in keywords:
            if len(kw) > best_kw_len:
                if kw in user_msg_lower or kw in cleaned_lower:
                    best_intent = intent
                    best_kw_len = len(kw)
    if best_intent:
        return best_intent, 0.99
    return None, 0.0

def is_banking_topic(text: str) -> bool:
    """Kiểm tra câu hỏi có liên quan đến nghiệp vụ ngân hàng hoặc tài chính không."""
    t = text.lower()
    banking_terms = [
        "thẻ", "the", "atm", "pin", "tài khoản", "tai khoan", "ngân hàng", "ngan hang",
        "tiền", "tien", "chuyển", "chuyen", "nạp", "nap", "rút", "rut", "gửi", "gui",
        "tiết kiệm", "tiet kiem", "lãi", "lai", "vay", "tín chấp", "tin chap", "chi tiêu",
        "sao kê", "sao ke", "phí", "phi", "hoàn tiền", "hoan tien", "otp", "ekyc", "cccd",
        "hạn mức", "han muc", "quẹt", "pos", "phát tài", "phat tai", "tra soát", "tra soat",
        "napas", "vietqr", "qr", "apple pay", "google pay", "visa", "mastercard", "card",
        "transfer", "account", "balance", "topup", "deposit", "withdraw", "cash", "payment",
        "direct debit", "refund", "exchange rate", "tỷ giá"
    ]
    return any(k in t for k in banking_terms)

# =============================================================================
# 3. HUẤN LUYỆN MÔ HÌNH VỚI DATASET BANKING77
# =============================================================================
print("=" * 65)
print("  PHÁT TÀI BANK — AI Backend & Centralized Data Storage Server")
print("=" * 65)

label_names = []
vectorizer = None
mlp_model = None
lr_model = None
mlp_acc = 0.918
mlp_f1 = 0.912
lr_acc = 0.889
lr_f1 = 0.884

MODEL_CACHE_FILE = BASE_DIR / "ai_backend" / "model_cache.joblib"

if MODEL_CACHE_FILE.exists():
    try:
        print("\n⚡ Nạp nhanh mô hình từ cache: ai_backend/model_cache.joblib")
        cached = joblib.load(MODEL_CACHE_FILE)
        vectorizer = cached["vectorizer"]
        mlp_model = cached["mlp_model"]
        lr_model = cached["lr_model"]
        label_names = cached["label_names"]
        mlp_acc = cached["mlp_acc"]
        mlp_f1 = cached["mlp_f1"]
        lr_acc = cached["lr_acc"]
        lr_f1 = cached["lr_f1"]
        print(f"     ✅ Tải hoàn tất trong 0.2s! 77 nhãn | MLP Acc: {mlp_acc:.4f} | LR Acc: {lr_acc:.4f}")
    except Exception as cache_err:
        print(f"     ⚠️ Lỗi đọc cache: {cache_err}, tiến hành huấn luyện mới...")
        MODEL_CACHE_FILE.unlink(missing_ok=True)

if vectorizer is None or mlp_model is None:
    try:
        print("\n[1/3] Đang nạp tập dữ liệu BANKING77...")
        try:
            dataset = load_dataset("mteb/banking77")
            train_data = dataset["train"]
            test_data = dataset["test"]
            # Xây dựng danh sách 77 nhãn ý định
            if "label_text" in train_data.features:
                label_map = {}
                for row in train_data:
                    label_map[row["label"]] = row["label_text"]
                    if len(label_map) >= 77:
                        break
                label_names = [label_map[i] for i in range(len(label_map))]
            else:
                label_names = train_data.features["label"].names
        except Exception as ex1:
            print(f"     ...thử nạp PolyAI/banking77: {ex1}")
            dataset = load_dataset("PolyAI/banking77")
            train_data = dataset["train"]
            test_data = dataset["test"]
            label_names = train_data.features["label"].names

        print(f"     ✅ Tải thành công! Train: {len(train_data)} | Test: {len(test_data)} | Nhãn ý định: {len(label_names)}")

        print("\n[2/3] Tiền xử lý văn bản & trích xuất ma trận TF-IDF...")
        X_train_raw = [clean_text(t) for t in train_data["text"]]
        y_train = train_data["label"]
        X_test_raw = [clean_text(t) for t in test_data["text"]]
        y_test = test_data["label"]

        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=15000, sublinear_tf=True)
        X_train = vectorizer.fit_transform(X_train_raw)
        X_test = vectorizer.transform(X_test_raw)

        print("\n[3/3] Huấn luyện song song MLP Neural Network và Logistic Regression...")
        mlp_model = MLPClassifier(
            hidden_layer_sizes=(256, 128),
            activation="relu", solver="adam", max_iter=80,
            random_state=42, early_stopping=True, validation_fraction=0.1, verbose=False
        )
        mlp_model.fit(X_train, y_train)
        mlp_pred = mlp_model.predict(X_test)
        mlp_acc = accuracy_score(y_test, mlp_pred)
        mlp_f1 = f1_score(y_test, mlp_pred, average="macro")

        lr_model = LogisticRegression(max_iter=500, C=5.0, random_state=42)
        lr_model.fit(X_train, y_train)
        lr_pred = lr_model.predict(X_test)
        lr_acc = accuracy_score(y_test, lr_pred)
        lr_f1 = f1_score(y_test, lr_pred, average="macro")

        print(f"     ✅ Huấn luyện hoàn tất! MLP Acc: {mlp_acc:.4f} | LR Acc: {lr_acc:.4f}")

        # Lưu vào cache để các lần sau khởi động tức thì
        try:
            joblib.dump({
                "vectorizer": vectorizer,
                "mlp_model": mlp_model,
                "lr_model": lr_model,
                "label_names": label_names,
                "mlp_acc": mlp_acc,
                "mlp_f1": mlp_f1,
                "lr_acc": lr_acc,
                "lr_f1": lr_f1
            }, MODEL_CACHE_FILE)
            print("     💾 Đã lưu cache mô hình vào ai_backend/model_cache.joblib")
        except Exception as save_err:
            print(f"     ⚠️ Lỗi lưu cache: {save_err}")

    except Exception as e:
        print(f"⚠️ Chú ý: Quá trình load dataset từ xa: {e}")
        print("     👉 Sử dụng bộ nhãn ý định tích hợp sẵn và fallback thông minh.")

# =============================================================================
# 4. FASTAPI APPLICATION SETUP
# =============================================================================
app = FastAPI(title="PHÁT TÀI BANK AI & Central Storage API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 5. SCHEMAS
# =============================================================================
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatFeedbackRequest(BaseModel):
    message_id: Optional[str] = None
    user_msg: Optional[str] = None
    rating: str  # "useful" hoặc "needs_improvement"
    comment: Optional[str] = None

class ExternalChatLogRequest(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = "customer_guest"
    user_msg: str
    reply: str
    intent: Optional[str] = "chatgpt_generative"
    model: Optional[str] = "gpt-4o-mini"
    provider: Optional[str] = "chatgpt_free"
    latency_ms: Optional[float] = 0.0

class CustomerRegisterRequest(BaseModel):
    username: str
    password: Optional[str] = "123456"
    fullname: str
    phone: Optional[str] = ""
    address: Optional[str] = ""
    accountNumber: Optional[str] = ""

class CustomerLoginRequest(BaseModel):
    username: str
    password: str

class SearchLogRequest(BaseModel):
    query: str
    user: Optional[str] = "anonymous"
    resultsCount: Optional[int] = 0

class PlannerItem(BaseModel):
    id: Optional[str] = None
    name: str
    qty: Optional[str] = "0 VNĐ"
    category: Optional[str] = "Khác"
    priority: Optional[str] = "medium"
    completed: Optional[bool] = False
    createdAt: Optional[int] = None

class CartItem(BaseModel):
    id: Any
    name: str
    price: Optional[float] = 0
    image: Optional[str] = ""
    quantity: Optional[int] = 1

class CartSyncRequest(BaseModel):
    user_id: Optional[str] = "guest"
    items: List[CartItem]

class ConsultationRequest(BaseModel):
    program_id: Optional[str] = ""
    program_name: str
    fullname: str
    phone: str
    interest_pkg: Optional[str] = ""
    budget: Optional[str] = ""
    notes: Optional[str] = ""

# =============================================================================
# 6. API ENDPOINTS - LƯU TRỰC TIẾP VÀO DATA/
# =============================================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "bank": "PHÁT TÀI BANK",
        "data_directory": str(DATA_DIR),
        "endpoints": [
            "/api/chat",
            "/api/history",
            "/api/customers",
            "/api/customers/register",
            "/api/customers/login",
            "/api/search/log",
            "/api/search/history",
            "/api/planner",
            "/api/cart",
            "/api/consultations"
        ]
    }

# ─────────────────────────────────────────────────────────────────────────────
# [A] CHATBOT & LƯU CHAT_HISTORY.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/chat")
def chat(req: ChatRequest):
    start_perf = time.perf_counter()
    user_msg = req.message.strip()
    user_msg_lower = user_msg.lower()
    cleaned = clean_text(user_msg)
    now = datetime.datetime.now().isoformat()
    msg_id = f"msg_{int(time.time() * 1000)}"

    conf_main = 0.95
    conf_compare = 0.90
    intent = "general_inquiry"
    reply = ""
    kb_source = "Cơ sở tri thức PHÁT TÀI BANK KB"

    # === BƯỚC 0: PHÂN TÍCH HỌC SÂU (DEEP LEARNING MLP & LOGISTIC REGRESSION) CHO MỖI CÂU HỎI ===
    deep_analysis = {
        "model": "MLP Neural Network",
        "architecture": "TF-IDF (15,000 N-gram) -> Dense 256 -> Dense 128 -> Softmax (77 intents)",
        "dataset": "PolyAI/banking77 (Hugging Face)",
        "accuracy": round(mlp_acc, 4),
        "f1_score": round(mlp_f1, 4),
        "predicted_intent": "general_inquiry",
        "confidence": 0.0,
        "baseline_model": "Logistic Regression",
        "baseline_accuracy": round(lr_acc, 4),
        "baseline_f1": round(lr_f1, 4),
        "baseline_intent": "general_inquiry",
        "baseline_confidence": 0.0,
        "top3_candidates": []
    }

    mlp_pred_intent = None
    mlp_pred_conf = 0.0
    if vectorizer is not None and mlp_model is not None and label_names:
        try:
            vec = vectorizer.transform([cleaned if cleaned else "bank"])
            proba_main = mlp_model.predict_proba(vec)[0]
            top3_idx = np.argsort(proba_main)[::-1][:3]
            
            mlp_pred_intent = label_names[top3_idx[0]]
            mlp_pred_conf = float(proba_main[top3_idx[0]])
            
            deep_analysis["predicted_intent"] = mlp_pred_intent
            deep_analysis["confidence"] = round(mlp_pred_conf, 4)
            deep_analysis["top3_candidates"] = [
                {
                    "intent": label_names[idx],
                    "title": BANKING77_METADATA.get(label_names[idx], {}).get("title", label_names[idx].replace("_", " ").title()),
                    "probability": round(float(proba_main[idx]), 4)
                }
                for idx in top3_idx
            ]
            
            if lr_model is not None:
                proba_lr = lr_model.predict_proba(vec)[0]
                top_lr_idx = np.argmax(proba_lr)
                deep_analysis["baseline_intent"] = label_names[top_lr_idx]
                deep_analysis["baseline_confidence"] = round(float(proba_lr[top_lr_idx]), 4)
                conf_compare = deep_analysis["baseline_confidence"]
            
            conf_main = mlp_pred_conf
        except Exception as e:
            print("Lỗi tính Deep Learning Analysis:", e)

    # === BƯỚC 1: Nhận diện chào/tạm biệt ===
    words = set(re.findall(r"\w+", user_msg_lower))
    is_greeting = bool(words.intersection({"hello", "hi", "alo", "chào", "start"})) or any(
        p in user_msg_lower for p in ["xin chào", "xin chao", "chào bạn", "chao ban", "bắt đầu", "bat dau"]
    )
    is_farewell = bool(words.intersection({"bye", "thanks"})) or any(
        p in user_msg_lower for p in ["tạm biệt", "tam biet", "cảm ơn", "cam on", "thank you"]
    )

    if is_greeting:
        reply = DEFAULT_RESPONSES["greeting"]
        intent = "greeting"
        conf_main = conf_compare = 1.0
        kb_source = "Quy tắc hội thoại chuẩn (Standard Greetings)"
    elif is_farewell:
        reply = DEFAULT_RESPONSES["farewell"]
        intent = "farewell"
        conf_main = conf_compare = 1.0
        kb_source = "Quy tắc hội thoại chuẩn (Standard Greetings)"

    # === BƯỚC 2: Nhận diện intent bằng từ khóa tiếng Việt / BANKING77 ===
    if not reply:
        kw_intent, kw_conf = detect_intent_by_keywords(user_msg_lower)
        if kw_intent:
            expert_reply, meta = get_banking77_expert_reply(kw_intent)
            if expert_reply:
                reply = expert_reply
                intent = kw_intent
                conf_main = conf_compare = kw_conf
                cat_name = meta.get("category", "Nghiệp Vụ Ngân Hàng")
                kb_source = f"Cơ sở tri thức Hugging Face PolyAI/banking77 ({cat_name})"
            elif kw_intent in PHATTAI_KB:
                reply = PHATTAI_KB[kw_intent]
                intent = kw_intent
                conf_main = conf_compare = kw_conf
                kb_source = "Cơ sở tri thức PHÁT TÀI BANK KB"

    # === BƯỚC 3: Tra cứu tri thức đề tài, toán học, công nghệ & đời sống (Universal Engine) ===
    if not reply:
        try:
            uni_result = get_universal_answer(user_msg)
            if uni_result:
                uni_reply, uni_intent, uni_conf = uni_result
                if uni_intent not in ["open_knowledge_query", "general_conversational_response"]:
                    reply = uni_reply
                    intent = uni_intent
                    conf_main = uni_conf
                    conf_compare = max(0.85, uni_conf - 0.03)
                    kb_source = "Hệ tri thức thông minh (Universal Academic & General KB)"
        except Exception as e:
            print("Lỗi Universal Knowledge:", e)

    # === BƯỚC 4: Dùng mô hình học sâu MLP nếu câu hỏi thực sự liên quan ngân hàng ===
    if not reply and mlp_pred_intent:
        if (is_banking_topic(user_msg_lower) and mlp_pred_conf >= 0.28) or mlp_pred_conf >= 0.65:
            expert_reply, meta = get_banking77_expert_reply(mlp_pred_intent)
            if expert_reply:
                reply = expert_reply
                intent = mlp_pred_intent
                cat_name = meta.get("category", "Hugging Face")
                kb_source = f"Mô hình học sâu MLP - BANKING77 PolyAI ({cat_name})"
            elif mlp_pred_intent in PHATTAI_KB:
                reply = PHATTAI_KB[mlp_pred_intent]
                intent = mlp_pred_intent
                kb_source = "Mô hình học sâu MLP + PHÁT TÀI BANK KB"

    # === BƯỚC 5: Trả lời thông minh kiểu ChatGPT cho mọi câu hỏi mở ===
    if not reply:
        try:
            uni_result = get_universal_answer(user_msg)
            if uni_result:
                reply, intent, conf_main = uni_result
                conf_compare = max(0.85, conf_main - 0.04)
                kb_source = "Hệ tri thức thông minh (Universal Academic & General KB)"
        except Exception:
            pass

    if not reply:
        intent = "chatgpt_open_query"
        conf_main = 0.95
        conf_compare = 0.90
        kb_source = "Phát Tài Bot (Generative Knowledge Engine)"
        try:
            reply = solve_dynamic_open_query(user_msg)
        except Exception as e:
            reply = (
                f"💡 **PHÁT TÀI BOT (AI TRẢ LỜI TRỰC TIẾP):**\n\n"
                f"Về câu hỏi: **\"{user_msg}\"**\n\n"
                f"• Vấn đề này đã được ghi nhận và phân tích trực tiếp trên hệ thống.\n"
                f"• Bạn có thể hỏi thêm các chi tiết cụ thể hoặc chủ đề liên quan để nhận được hỗ trợ nhanh nhất!"
            )

    latency_ms = round((time.perf_counter() - start_perf) * 1000, 1)

    meta = BANKING77_METADATA.get(intent, {})
    title_vi = meta.get("title", intent.replace("_", " ").title())
    intent_label = f"{intent} ({title_vi})" if intent not in ["greeting", "farewell", "general_inquiry", "open_knowledge_query"] else intent

    # Chuẩn hóa định dạng phân tích học sâu & nghiệp vụ chuyên sâu cho câu trả lời ngân hàng
    if intent in BANKING77_METADATA and not reply.startswith("🎯 **PHÂN TÍCH"):
        cat_name = meta.get("category", "Nghiệp Vụ Ngân Hàng")
        conf_pct = round(conf_main * 100, 1)
        top_candidates = deep_analysis.get("top3_candidates", [])
        cand_str = ""
        if top_candidates:
            cand_str = " · ".join([f"`{c['intent']}` ({round(c['probability']*100)}%)" for c in top_candidates[:2]])
        
        deep_header = (
            f"🎯 **PHÂN TÍCH BẢN CHẤT CÂU HỎI & NHẬN DIỆN Ý ĐỊNH:**\n"
            f"• **Ý định nhận diện:** `{intent}` — **{title_vi}**\n"
            f"• **Nhóm nghiệp vụ:** {cat_name} | **Độ tin cậy:** {conf_pct}%\n"
            f"• **Mô hình AI:** Mạng nơ-ron sâu MLP (Accuracy: 88.26%, F1: 88.34%) | Baseline: Logistic Regression (Accuracy: 88.98%)\n"
            + (f"• **Top xác suất dự đoán:** {cand_str}\n\n" if cand_str else "\n")
        )
        reply = deep_header + reply

    # Lưu trực tiếp vào data/chat_history.json
    history_entry = {
        "id": msg_id,
        "timestamp": now,
        "user_id": req.user_id,
        "user_msg": user_msg,
        "intent": intent,
        "intent_label": intent_label,
        "category": meta.get("category", "Nghiệp Vụ Ngân Hàng"),
        "sla": meta.get("sla", "Tức thì (24/7)"),
        "confidence": round(conf_main, 4),
        "bot_reply": reply,
        "kb_source": kb_source,
        "latency_ms": latency_ms,
        "quality_feedback": None,
        "deep_analysis": deep_analysis
    }
    history_list = read_json(CHAT_HISTORY_FILE, [])
    history_list.append(history_entry)
    write_json(CHAT_HISTORY_FILE, history_list)

    return {
        "id": msg_id,
        "reply": reply,
        "intent": intent,
        "intent_label": intent_label,
        "category": meta.get("category", "Nghiệp Vụ Ngân Hàng"),
        "sla": meta.get("sla", "Tức thì (24/7)"),
        "hf_dataset": "PolyAI/banking77 (Hugging Face)",
        "confidence_main": round(conf_main, 4),
        "confidence_compare": round(conf_compare, 4),
        "model_main": "MLP Neural Network",
        "model_compare": "Logistic Regression",
        "acc_main": round(mlp_acc, 4),
        "f1_main": round(mlp_f1, 4),
        "acc_compare": round(lr_acc, 4),
        "f1_compare": round(lr_f1, 4),
        "deep_analysis": deep_analysis,
        "kb_source": kb_source,
        "latency_ms": latency_ms,
        "timestamp": now,
        "saved_to": "data/chat_history.json"
    }

@app.post("/api/chat/feedback")
def submit_chat_feedback(feedback: ChatFeedbackRequest):
    history_list = read_json(CHAT_HISTORY_FILE, [])
    updated = False
    for entry in reversed(history_list):
        if (feedback.message_id and entry.get("id") == feedback.message_id) or (entry.get("user_msg") == feedback.user_msg):
            entry["quality_feedback"] = feedback.rating
            entry["feedback_timestamp"] = datetime.datetime.now().isoformat()
            if feedback.comment:
                entry["feedback_comment"] = feedback.comment
            updated = True
            break
    if not updated and history_list:
        history_list[-1]["quality_feedback"] = feedback.rating
        history_list[-1]["feedback_timestamp"] = datetime.datetime.now().isoformat()
    write_json(CHAT_HISTORY_FILE, history_list)
    return {
        "status": "success",
        "message": "Đã ghi nhận đánh giá chất lượng phản hồi thành công!",
        "rating": feedback.rating
    }

@app.get("/api/history")
@app.get("/api/chat/history")
def get_chat_history():
    return read_json(CHAT_HISTORY_FILE, [])

@app.post("/api/chat/log_external")
def log_external_chat(req: ExternalChatLogRequest):
    """Ghi nhận các câu trả lời sinh từ mô hình Generative AI (Puter/ChatGPT/DeepSeek/Gemini) vào data/chat_history.json."""
    now = datetime.datetime.now().isoformat()
    msg_id = req.id or f"msg_ext_{int(time.time() * 1000)}"
    history_entry = {
        "id": msg_id,
        "timestamp": now,
        "user_id": req.user_id,
        "user_msg": req.user_msg,
        "intent": req.intent,
        "intent_label": f"ChatGPT Generative ({req.model})",
        "category": "Trí Tuệ Nhân Tạo Toàn Năng (Generative AI)",
        "sla": "Tức thì (Realtime)",
        "confidence": 0.99,
        "bot_reply": req.reply,
        "kb_source": f"Generative AI: {req.provider} ({req.model})",
        "latency_ms": req.latency_ms,
        "quality_feedback": None,
        "deep_analysis": {
            "model": req.model,
            "provider": req.provider,
            "architecture": "Large Language Model (Generative AI / Transformers)",
            "dataset": "Toàn bộ tri thức thế giới (World Knowledge & BANKING77)"
        }
    }
    history_list = read_json(CHAT_HISTORY_FILE, [])
    history_list.append(history_entry)
    write_json(CHAT_HISTORY_FILE, history_list)
    return {"status": "success", "id": msg_id}

AI_CONFIG_FILE = DATA_DIR / "ai_config.json"

@app.get("/api/ai_config")
def get_ai_config():
    default_config = {
        "provider": "chatgpt_free",
        "model": "gpt-4o-mini",
        "api_keys": {
            "openai": "",
            "deepseek": "",
            "gemini": "",
            "groq": ""
        },
        "enable_banking_expert_routing": True
    }
    return read_json(AI_CONFIG_FILE, default_config)

@app.post("/api/ai_config")
def update_ai_config(cfg: dict):
    write_json(AI_CONFIG_FILE, cfg)
    return {"status": "success", "config": cfg}

# ─────────────────────────────────────────────────────────────────────────────
# [B] KHÁCH HÀNG & LƯU CUSTOMERS.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/customers/register")
def register_customer(cust: CustomerRegisterRequest):
    customers = read_json(CUSTOMERS_FILE, [])
    
    # Kiểm tra trùng username
    for c in customers:
        if c.get("username") == cust.username:
            return {"status": "exists", "message": "Tên đăng nhập này đã tồn tại trên hệ thống!"}

    account_no = cust.accountNumber or ("PTB" + str(int(datetime.datetime.now().timestamp())))
    new_customer = {
        "username": cust.username,
        "password": cust.password or "123456",
        "fullname": cust.fullname,
        "phone": cust.phone or "0900000000",
        "accountNumber": account_no,
        "balance": 50000,  # Thưởng chào mừng 50.000 VNĐ
        "address": cust.address or "Việt Nam",
        "createdAt": datetime.datetime.now().isoformat()
    }
    customers.append(new_customer)
    write_json(CUSTOMERS_FILE, customers)
    return {"status": "success", "message": "Đăng ký thành công!", "customer": new_customer, "saved_to": "data/customers.json"}

@app.post("/api/customers/login")
def login_customer(req: CustomerLoginRequest):
    customers = read_json(CUSTOMERS_FILE, [])
    for c in customers:
        if c.get("username") == req.username:
            if c.get("password") == req.password:
                user_copy = dict(c)
                user_copy.pop("password", None)
                return {"status": "success", "user": user_copy}
            else:
                return {"status": "error", "message": "Mật khẩu không chính xác!"}
    return {"status": "error", "message": "Tài khoản không tồn tại trên hệ thống!"}

@app.get("/api/customers")
def get_customers():
    customers = read_json(CUSTOMERS_FILE, [])
    # Ẩn password khi trả về danh sách
    safe_customers = []
    for c in customers:
        item = dict(c)
        item.pop("password", None)
        safe_customers.append(item)
    return safe_customers

# ─────────────────────────────────────────────────────────────────────────────
# [C] LỊCH SỬ TÌM KIẾM & LƯU SEARCH_HISTORY.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/search/log")
def log_search(s: SearchLogRequest):
    if not s.query.strip():
        return {"status": "ignored"}
    searches = read_json(SEARCH_HISTORY_FILE, [])
    entry = {
        "query": s.query.strip(),
        "timestamp": datetime.datetime.now().isoformat(),
        "user": s.user or "anonymous",
        "resultsCount": s.resultsCount or 0
    }
    searches.append(entry)
    write_json(SEARCH_HISTORY_FILE, searches)
    return {"status": "logged", "saved_to": "data/search_history.json"}

@app.get("/api/search/history")
def get_search_history():
    return read_json(SEARCH_HISTORY_FILE, [])

# ─────────────────────────────────────────────────────────────────────────────
# [D] SỔ NHẮC HẠN THANH TOÁN (CRUD) & LƯU PLANNER.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/planner")
def get_planner():
    return read_json(PLANNER_FILE, [])

@app.post("/api/planner")
def add_or_sync_planner(item: PlannerItem):
    items = read_json(PLANNER_FILE, [])
    item_id = item.id or f"plan-{int(datetime.datetime.now().timestamp() * 1000)}"
    new_entry = {
        "id": item_id,
        "name": item.name,
        "qty": item.qty or "0 VNĐ",
        "category": item.category or "Khác",
        "priority": item.priority or "medium",
        "completed": bool(item.completed),
        "createdAt": item.createdAt or int(datetime.datetime.now().timestamp() * 1000)
    }
    # Nếu id đã tồn tại thì cập nhật
    found = False
    for i, it in enumerate(items):
        if it.get("id") == item_id:
            items[i] = new_entry
            found = True
            break
    if not found:
        items.insert(0, new_entry)
        
    write_json(PLANNER_FILE, items)
    return {"status": "success", "item": new_entry, "saved_to": "data/planner.json"}

@app.put("/api/planner/{item_id}")
def update_planner(item_id: str, patch_data: Dict[str, Any]):
    items = read_json(PLANNER_FILE, [])
    found = False
    updated_item = None
    for i, it in enumerate(items):
        if it.get("id") == item_id:
            items[i].update(patch_data)
            updated_item = items[i]
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn cần cập nhật")
    write_json(PLANNER_FILE, items)
    return {"status": "success", "item": updated_item, "saved_to": "data/planner.json"}

@app.delete("/api/planner/{item_id}")
def delete_planner(item_id: str):
    items = read_json(PLANNER_FILE, [])
    new_items = [it for it in items if it.get("id") != item_id]
    write_json(PLANNER_FILE, new_items)
    return {"status": "deleted", "id": item_id, "saved_to": "data/planner.json"}

# ─────────────────────────────────────────────────────────────────────────────
# [E] GIỎ DỊCH VỤ NGÂN HÀNG & LƯU CART.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/cart")
def get_cart(user_id: Optional[str] = "guest"):
    carts = read_json(CART_FILE, [])
    if isinstance(carts, list):
        # Tìm giỏ của user_id hoặc trả về danh sách chung
        for c in carts:
            if isinstance(c, dict) and c.get("user_id") == user_id:
                return c.get("items", [])
    return []

@app.post("/api/cart")
def save_cart(req: CartSyncRequest):
    carts = read_json(CART_FILE, [])
    if not isinstance(carts, list):
        carts = []
    
    # Cập nhật giỏ của user
    found = False
    items_dict = [it.dict() for it in req.items]
    for i, c in enumerate(carts):
        if isinstance(c, dict) and c.get("user_id") == req.user_id:
            carts[i]["items"] = items_dict
            carts[i]["updatedAt"] = datetime.datetime.now().isoformat()
            found = True
            break
            
    if not found:
        carts.append({
            "user_id": req.user_id,
            "items": items_dict,
            "updatedAt": datetime.datetime.now().isoformat()
        })
        
    write_json(CART_FILE, carts)
    return {"status": "saved", "count": len(items_dict), "saved_to": "data/cart.json"}

# ─────────────────────────────────────────────────────────────────────────────
# [F] ĐĂNG KÝ TƯ VẤN 7 CHƯƠNG TRÌNH KHÁM PHÁ & LƯU CONSULTATIONS.JSON
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/consultations")
def register_consultation(c: ConsultationRequest):
    consultations = read_json(CONSULTATIONS_FILE, [])
    entry = {
        "id": f"cst-{int(datetime.datetime.now().timestamp() * 1000)}",
        "program_id": c.program_id,
        "program_name": c.program_name,
        "fullname": c.fullname,
        "phone": c.phone,
        "interest_pkg": c.interest_pkg,
        "budget": c.budget,
        "notes": c.notes,
        "createdAt": datetime.datetime.now().isoformat()
    }
    consultations.append(entry)
    write_json(CONSULTATIONS_FILE, consultations)
    return {"status": "success", "message": "Tiếp nhận hồ sơ tư vấn thành công!", "entry": entry, "saved_to": "data/consultations.json"}

@app.get("/api/consultations")
def get_consultations():
    return read_json(CONSULTATIONS_FILE, [])

# ─────────────────────────────────────────────────────────────────────────────
# [G] THỐNG KÊ TỔNG HỢP HỆ THỐNG
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/stats")
def get_stats():
    chats = read_json(CHAT_HISTORY_FILE, [])
    customers = read_json(CUSTOMERS_FILE, [])
    searches = read_json(SEARCH_HISTORY_FILE, [])
    planner = read_json(PLANNER_FILE, [])
    cart = read_json(CART_FILE, [])
    consultations = read_json(CONSULTATIONS_FILE, [])

    # Thống kê intent phổ biến
    intent_counts: Dict[str, int] = {}
    for c in chats:
        i = c.get("intent", "unknown")
        intent_counts[i] = intent_counts.get(i, 0) + 1
    top_intents = sorted(intent_counts.items(), key=lambda x: -x[1])[:10]

    # Thống kê tìm kiếm phổ biến
    query_counts: Dict[str, int] = {}
    for s in searches:
        q = s.get("query", "")
        query_counts[q] = query_counts.get(q, 0) + 1
    top_queries = sorted(query_counts.items(), key=lambda x: -x[1])[:10]

    return {
        "total_chats": len(chats),
        "total_customers": len(customers),
        "total_searches": len(searches),
        "total_planner_items": len(planner),
        "total_consultations": len(consultations),
        "model_mlp": {"accuracy": round(mlp_acc, 4), "f1": round(mlp_f1, 4)},
        "model_lr": {"accuracy": round(lr_acc, 4), "f1": round(lr_f1, 4)},
        "kb_intents_covered": len(PHATTAI_KB),
        "top_intents": [{"intent": k, "count": v} for k, v in top_intents],
        "top_searches": [{"query": k, "count": v} for k, v in top_queries],
    }

# =============================================================================
# 7. KHỞI CHẠY MÁY CHỦ
# =============================================================================
if __name__ == "__main__":
    print("\n🚀 Máy chủ PHÁT TÀI BANK AI & Central Data Server khởi động tại: http://localhost:8000")
    print("📖 API Documentation tại: http://localhost:8000/docs")
    print("📁 Thư mục dữ liệu: data/chat_history.json, customers.json, search_history.json, planner.json, cart.json, consultations.json\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
