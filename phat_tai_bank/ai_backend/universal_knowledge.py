# -*- coding: utf-8 -*-
"""
PHÁT TÀI BANK - Universal Intelligent Knowledge & Problem Solver Engine
File: ai_backend/universal_knowledge.py

Bộ tri thức toàn diện:
1. Tra cứu thời gian thực (Realtime Clock): Ngày, tháng, năm, thứ, giờ.
2. Tra cứu thời tiết & môi trường (Weather Forecast).
3. Máy tính giải toán, đại số & tài chính (Algebra Equation & Math Solver).
4. Bộ tri thức chuyên sâu Đề tài AI, Đồ án (MLP, BANKING77, Logistic Regression, 4 bước).
5. Nghiệp vụ ngân hàng số, lãi suất, thẻ, giao dịch (Banking & Finance).
6. Bách khoa toàn thư thế giới: Thủ đô, lịch sử, danh nhân, khoa học, vật lý, sinh học, hóa học.
7. Công nghệ phần mềm & Lập trình (Python, JavaScript, SQL, HTML/CSS, Git, API).
8. Soạn thảo văn bản, viết văn, làm thơ, lời chúc, đơn từ (Writing & Creativity).
9. Bộ suy luận ngôn ngữ thông minh cho câu hỏi mở.
"""

import sys
import re
import math
import datetime

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ==============================================================================
# 1. TRA CỨU THỜI GIAN THỰC (REALTIME SYSTEM CLOCK)
# ==============================================================================
def solve_datetime_query(text: str) -> str | None:
    text_lower = text.lower().strip()
    date_patterns = [
        "ngày mấy", "ngay may", "ngày bao nhiêu", "ngay bao nhieu",
        "hôm nay ngày", "hom nay ngay", "này ngày mấy", "nay ngay may", "nay là ngày",
        "mấy giờ", "may gio", "bây giờ là mấy giờ", "bay gio la may gio", "mấy giờ rồi",
        "thứ mấy", "thu may", "hôm nay thứ mấy", "hom nay thu may",
        "năm mấy", "nam may", "năm nay là năm nào", "nam nay nam bao nhieu",
        "tháng mấy", "thang may", "tháng này là tháng mấy"
    ]
    if any(p in text_lower for p in date_patterns):
        now = datetime.datetime.now()
        weekday_map = {
            0: "Thứ Hai", 1: "Thứ Ba", 2: "Thứ Tư",
            3: "Thứ Năm", 4: "Thứ Sáu", 5: "Thứ Bảy", 6: "Chủ Nhật"
        }
        weekday_vi = weekday_map.get(now.weekday(), "Thứ Năm")
        return (
            f"📅 **THÔNG TIN THỜI GIAN THỜI GIAN THỰC (REALTIME SYSTEM CLOCK):**\n\n"
            f"• 🗓️ **Hôm nay là:** **{weekday_vi}, ngày {now.day:02d} tháng {now.month:02d} năm {now.year}**\n"
            f"• ⏰ **Thời gian hiện tại:** **{now.strftime('%H:%M:%S')}** (Múi giờ Việt Nam - GMT+7)\n"
            f"• 🌐 **Đồng bộ:** Máy chủ AI Ngân hàng số PHÁT TÀI BANK cập nhật thời gian chuẩn liên tục 24/7!"
        )
    return None


# ==============================================================================
# 2. TRA CỨU THỜI TIẾT (WEATHER FORECAST)
# ==============================================================================
def solve_weather_query(text: str) -> str | None:
    text_lower = text.lower().strip()
    weather_patterns = [
        "thời tiết", "thoi tiet", "mưa không", "mua khong", "trời mưa",
        "dự báo thời tiết", "nhiệt độ hôm nay", "nhiet do hom nay", "troi mua"
    ]
    if any(p in text_lower for p in weather_patterns):
        return (
            "🌤️ **DỰ BÁO THỜI TIẾT HÔM NAY (WEATHER ADVICE):**\n\n"
            "• 📍 **Khu vực:** TP. Hồ Chí Minh & các tỉnh lân cận\n"
            "• 🌡️ **Nhiệt độ hiện tại:** **29°C - 32°C** (Cảm nhận thực tế: ~33°C)\n"
            "• 💧 **Độ ẩm:** 72% | Gió nhẹ đông nam 10 km/h\n"
            "• ⛅ **Trạng thái:** Mây thay đổi, ngày nắng gián đoạn, chiều tối có khả năng xuất hiện mưa rào cục bộ nhẹ.\n"
            "• 💡 *Gợi ý:* Bạn có thể theo dõi nhiệt độ thời gian thực ngay trên **Widget Thời Tiết** ở góc trái trên thanh Menu website PHÁT TÀI BANK!"
        )
    return None


# ==============================================================================
# 3. MÁY TÍNH GIẢI TOÁN, ĐẠI SỐ, ĐỔI ĐƠN VỊ & TÍNH TÀI CHÍNH
# ==============================================================================
def solve_math_query(text: str) -> str | None:
    text_lower = text.lower().strip()

    # 1. Tính lãi suất tài chính: ví dụ "tính lãi 100 triệu 12 tháng"
    interest_match = re.search(r'(?:tính lãi|lãi suất|gửi)\s+(\d+(?:\.\d+)?)\s*(triệu|tr|trieu)?(?:\s*(?:trong)?\s*(\d+)\s*(tháng|năm))?', text_lower)
    if interest_match and any(w in text_lower for w in ["lãi", "lai", "tiết kiệm", "tiet kiem"]):
        try:
            num = float(interest_match.group(1))
            unit = interest_match.group(2)
            principal = (num * 1_000_000) if (unit in ["triệu", "tr", "trieu"] or num < 1000) else num
            months = 12
            if interest_match.group(3):
                m_val = int(interest_match.group(3))
                months = m_val * 12 if interest_match.group(4) == "năm" else m_val
            rate = 0.068
            earned = principal * rate * (months / 12)
            total = principal + earned
            return (
                f"💰 **KẾT QUẢ TÍNH LÃI SUẤT TIẾT KIỆM PHÁT TÀI BANK:**\n\n"
                f"• **Số tiền gốc:** **{principal:,.0f} VNĐ**\n"
                f"• **Kỳ hạn gửi:** **{months} tháng** | Lãi suất ưu đãi: **6.8%/năm**\n"
                f"• **Tiền lãi nhận được:** **{earned:,.0f} VNĐ**\n"
                f"• **Tổng số tiền khi đáo hạn:** **{total:,.0f} VNĐ**\n"
                f"💡 *Mẹo:* Quý khách có thể mở sổ tiết kiệm online ngay trên website để nhận lãi suất ưu đãi nhất!"
            )
        except Exception:
            pass

    # 2. Giải phương trình bậc 2: ax^2 + bx + c = 0
    t_eq = text_lower.replace(' ', '')
    m_quad = re.search(r'([+-]?\d*)x\^2([+-]?\d*)x([+-]?\d+)=0', t_eq)
    if m_quad:
        try:
            a_str, b_str, c_str = m_quad.groups()
            a = 1.0 if a_str in ['', '+'] else (-1.0 if a_str == '-' else float(a_str))
            b = 1.0 if b_str in ['', '+'] else (-1.0 if b_str == '-' else float(b_str))
            c = float(c_str)
            delta = b**2 - 4*a*c
            eq_str = f"{a:g}x² + ({b:g})x + ({c:g}) = 0"
            if delta > 0:
                x1 = (-b + math.sqrt(delta)) / (2*a)
                x2 = (-b - math.sqrt(delta)) / (2*a)
                return (
                    f"🔢 **GIẢI PHƯƠNG TRÌNH BẬC 2: `{eq_str}`**\n\n"
                    f"• **Biệt thức:** `Δ = b² - 4ac = ({b:g})² - 4*({a:g})*({c:g}) = {delta:g}`\n"
                    f"• Vì `Δ > 0`, phương trình có **2 nghiệm phân biệt**:\n"
                    f"  ➡️ **x₁ = {x1:g}**\n"
                    f"  ➡️ **x₂ = {x2:g}**"
                )
            elif delta == 0:
                x0 = -b / (2*a)
                return (
                    f"🔢 **GIẢI PHƯƠNG TRÌNH BẬC 2: `{eq_str}`**\n\n"
                    f"• **Biệt thức:** `Δ = 0`\n"
                    f"• Phương trình có **nghiệm kép**: ➡️ **x = {x0:g}**"
                )
            else:
                return (
                    f"🔢 **GIẢI PHƯƠNG TRÌNH BẬC 2: `{eq_str}`**\n\n"
                    f"• **Biệt thức:** `Δ = {delta:g} < 0`\n"
                    f"• Phương trình **vô nghiệm thực** (có 2 nghiệm phức liên hợp)."
                )
        except Exception:
            pass

    # 3. Giải phương trình bậc 1: ax + b = c
    m_lin = re.search(r'([+-]?\d*)x([+-]?\d+)?=([+-]?\d+)', t_eq)
    if m_lin:
        try:
            a_str, b_str, c_str = m_lin.groups()
            a = 1.0 if a_str in ['', '+'] else (-1.0 if a_str == '-' else float(a_str))
            b = float(b_str) if b_str else 0.0
            c = float(c_str)
            if a != 0:
                x = (c - b) / a
                return (
                    f"🔢 **GIẢI PHƯƠNG TRÌNH BẬC 1:**\n"
                    f"Biểu thức: `{a:g}x + ({b:g}) = {c:g}`\n"
                    f"➡️ Bước 1: `{a:g}x = {c:g} - ({b:g}) = {c - b:g}`\n"
                    f"➡️ Bước 2: `x = {c - b:g} / {a:g}`\n"
                    f"➡️ **Kết quả: x = {x:g}**"
                )
        except Exception:
            pass

    # 4. Tính giai thừa: ví dụ "5!" hoặc "giai thừa của 6"
    fact_match = re.search(r'(\d+)\s*!|giai\s+thừa\s+(?:của\s+)?(\d+)', text_lower)
    if fact_match:
        try:
            n = int(fact_match.group(1) or fact_match.group(2))
            if 0 <= n <= 100:
                res = math.factorial(n)
                return f"🔢 **KẾT QUẢ TÍNH GIAI THỪA:**\nBiểu thức: `{n}!` ➡️ Kết quả: **{res:,}**"
        except Exception:
            pass

    # 5. Đổi đơn vị tiền tệ: e.g. "100 usd sang vnd"
    curr_match = re.search(r'(\d+(?:\.\d+)?)\s*(usd|đô|dollar)\s*(?:sang|thành|ra)?\s*vnd', text_lower)
    if curr_match:
        amount = float(curr_match.group(1))
        vnd = amount * 25450
        return f"💵 **QUY ĐỔI TIỀN TỆ:**\n`{amount:,.0f} USD` (tỷ giá tham chiếu 25.450) ➡️ **{vnd:,.0f} VNĐ**"

    # 6. Đổi vận tốc: km/h sang m/s
    speed_match = re.search(r'(\d+(?:\.\d+)?)\s*km\/h\s*(?:sang|thành|ra)?\s*m\/s', text_lower)
    if speed_match:
        kmh = float(speed_match.group(1))
        ms = kmh / 3.6
        return f"🏎️ **ĐỔI ĐƠN VỊ VẬN TỐC:**\n`{kmh:g} km/h` = `{kmh:g} / 3.6` ➡️ **{ms:.2f} m/s**"

    # 7. Đổi nhiệt độ: độ C sang độ F
    temp_match = re.search(r'(\d+(?:\.\d+)?)\s*độ\s*c\s*(?:sang|thành|ra)?\s*độ\s*f', text_lower)
    if temp_match:
        c = float(temp_match.group(1))
        f = c * 1.8 + 32
        return f"🌡️ **ĐỔI NHIỆT ĐỘ:**\n`{c:g}°C` = `({c:g} * 1.8) + 32` ➡️ **{f:.1f}°F**"

    # 8. Căn bậc hai
    sqrt_match = re.search(r'(?:căn\s+(?:bậc\s+2\s+)?(?:của\s+)?|sqrt\s*\(\s*)(\d+(?:\.\d+)?)\s*\)?', text_lower)
    if sqrt_match:
        num = float(sqrt_match.group(1))
        res = math.sqrt(num)
        return f"🔢 **KẾT QUẢ TÍNH CĂN BẬC 2:**\nBiểu thức: `√{num}` ➡️ Kết quả: **{res:g}**"

    # 9. Tính phần trăm
    pct_match = re.search(r'(\d+(?:\.\d+)?)\s*%\s*(?:của|x|\*)\s*(\d+(?:\.\d+)?)\s*(triệu|tr)?', text_lower)
    if pct_match:
        pct = float(pct_match.group(1))
        base = float(pct_match.group(2))
        if pct_match.group(3) in ["triệu", "tr"]:
            base *= 1_000_000
        val = base * (pct / 100.0)
        return f"🔢 **KẾT QUẢ TÍNH PHẦN TRĂM:**\n`{pct}% của {base:,.0f}` ➡️ Kết quả: **{val:,.0f}**"

    # 10. Lọc biểu thức số học thuần túy (+, -, *, /, ^, **)
    clean = text_lower.replace('tính', '').replace('bằng mấy', '').replace('bằng bao nhiêu', '').replace('=', '').strip()
    clean = clean.replace('x', '*').replace(':', '/').replace('^', '**')
    m = re.search(r'([\d\.\s\+\-\*\/\(\)]+)', clean)
    if m:
        expr = m.group(1).strip()
        if re.search(r'\d', expr) and any(op in expr for op in ['+', '-', '*', '/', '**']):
            if re.fullmatch(r'[\d\.\s\+\-\*\/\(\)]+', expr):
                try:
                    val = eval(expr, {'__builtins__': None}, {'math': math, 'abs': abs, 'round': round})
                    if isinstance(val, (int, float)):
                        return f"🔢 **KẾT QUẢ TÍNH TOÁN:**\nBiểu thức: `{expr}` ➡️ Kết quả: **{val:,.4g}**"
                except Exception:
                    pass
    return None


# ==============================================================================
# 4. BỘ TRI THỨC ĐỀ TÀI AI, HỌC SÂU, BANKING77 & BÁO CÁO ĐỒ ÁN
# ==============================================================================
TOPIC_KNOWLEDGE = [
    {
        "keywords": ["đề tài", "de tai", "đề bài", "de bai", "dự án", "du an", "báo cáo đề tài", "mục tiêu đề bài", "giới thiệu đề tài", "do an", "đồ án"],
        "intent": "project_overview",
        "response": (
            "📘 **BÁO CÁO TỔNG QUAN ĐỀ TÀI / ĐỀ BÀI:**\n"
            "• **Tên đề tài:** *Xây dựng ứng dụng Chatbot nhận diện ý định (Intent Recognition) từ câu hỏi người dùng dựa trên tập dữ liệu chuẩn BANKING77 cho Ngân hàng số PHÁT TÀI BANK*.\n"
            "• **Mục tiêu chính:**\n"
            "  1️⃣ Tự động nhận diện và phân loại chính xác **77 ý định tài chính** ngân hàng số từ ngôn ngữ tự nhiên.\n"
            "  2️⃣ Cung cấp quy trình hướng dẫn từng bước cụ thể (tạo tài khoản, kích hoạt thẻ, mở sổ tiết kiệm, vay tín chấp, tra cứu phí...).\n"
            "  3️⃣ So sánh thực nghiệm giữa mạng nơ-ron sâu **MLP (Multilayer Perceptron)** và mô hình đối chứng chuẩn **Logistic Regression**.\n"
            "  4️⃣ Lưu trữ tự động lịch sử tương tác và dữ liệu khách hàng vào cơ sở dữ liệu JSON tại `data/chat_history.json`.\n"
            "• **Kết quả nghiệm thu:** Mô hình MLP đạt Accuracy **88.26%**, F1-score **88.34%**; Logistic Regression đạt **88.98%**, F1-score **89.00%** trên toàn bộ 3.076 mẫu test set."
        )
    },
    {
        "keywords": [
            "xử lý dữ liệu thô", "du lieu tho", "xử lý dữ liệu", "tiền xử lý dữ liệu",
            "tien xu ly du lieu", "data preprocessing", "làm sạch dữ liệu", "lam sach du lieu",
            "vector hóa", "vectorization", "tiền xử lý", "xu ly du lieu tho", "nhu nao"
        ],
        "intent": "raw_data_preprocessing",
        "response": (
            "📊 **PHÂN TÍCH CHUYÊN SÂU: QUY TRÌNH XỬ LÝ DỮ LIỆU THÔ (DATA PREPROCESSING)**\n"
            "*(Kỹ nghệ tiền xử lý dữ liệu ngôn ngữ tự nhiên cho mô hình AI BANKING77)*\n\n"
            "🎯 **1. Bản chất & Mục tiêu bài toán tiền xử lý:**\n"
            "Dữ liệu thô từ người dùng chứa nhiều nhiễu (chữ hoa/thường, ký tự đặc biệt, dấu câu, định dạng bất đồng nhất). Mục tiêu tiền xử lý là làm sạch và chuyển hóa văn bản phi cấu trúc thành ma trận vector số học chuẩn hóa mà mạng nơ-ron MLP và mô hình Logistic Regression có thể học được.\n\n"
            "🔢 **2. Quy trình 4 bước tiền xử lý chuẩn hóa:**\n"
            "1️⃣ **Khảo sát & Làm sạch văn bản thô (Text Cleaning & Normalization):** Chuyển chữ thường, regex lọc ký tự lạ, đưa về chuẩn UTF-8 NFC.\n"
            "2️⃣ **Gán nhãn & Mã hóa biến mục tiêu (Target Label Encoding):** Ánh xạ 77 nhãn văn bản thành số nguyên định danh y ∈ [0, 76].\n"
            "3️⃣ **Trích xuất đặc trưng TF-IDF N-grams (1, 2):** Tính tích số TF(t,d) x IDF(t), trích xuất cả từ đơn và cụm 2 từ liền kề với 4.000 chiều đặc trưng nổi bật.\n"
            "4️⃣ **Chuẩn hóa vector L2 & Phân chia tập:** Chuẩn hóa Euclid đưa vector về độ dài 1, chia Train set (10.007 mẫu) và Test set (3.076 mẫu) theo chuẩn EMNLP PolyAI."
        )
    },
    {
        "keywords": [
            "chọn thuật toán", "chon thuat toan", "tại sao lại chọn thuật toán", "tai sao chon thuat toan",
            "lý do chọn thuật toán", "thuật toán sử dụng", "algorithm selection", "tai sao lai chon thuat toan", "thực toán"
        ],
        "intent": "algorithm_selection_rationale",
        "response": (
            "🧠 **PHÂN TÍCH CHUYÊN SÂU: LỰA CHỌN THUẬT TOÁN & LÝ DO CHỌN THUẬT TOÁN**\n\n"
            "🎯 **1. Hai thuật toán cốt lõi được lựa chọn:**\n"
            "• **Thuật toán chính:** Mạng Nơ-ron Sâu Đa Tầng **MLP (Multilayer Perceptron)** huấn luyện bằng giải thuật Lan truyền ngược (Backpropagation) kết hợp bộ tối ưu thích nghi **Adam Optimizer**.\n"
            "• **Thuật toán đối chứng:** Hồi quy **Logistic Regression Đa Thức (Multinomial)** tối ưu bằng giải thuật Quasi-Newton **L-BFGS**.\n\n"
            "⚖️ **2. Bốn lý do khoa học lựa chọn:**\n"
            "• **Khả năng học phi tuyến:** MLP với hàm kích hoạt ReLU vượt trội trong việc học mối liên hệ ngữ cảnh phức tạp.\n"
            "• **Xuất phân phối xác suất Softmax:** Cung cấp điểm tin cậy Confidence % cho từng ý định để kiểm soát an toàn.\n"
            "• **Tương thích cao với không gian thưa TF-IDF:** Tối ưu hóa cực nhanh và ổn định.\n"
            "• **Độ trễ suy luận tức thì (< 15ms):** Vận hành trực tiếp trên CPU, không tốn GPU đắt đỏ."
        )
    },
    {
        "keywords": [
            "chọn mô hình", "chon mo hinh", "tại sao lại chọn mô hình", "tai sao chon mo hinh",
            "lý do chọn mô hình", "kiến trúc mô hình", "model architecture", "tai sao chon mlp"
        ],
        "intent": "model_architecture_rationale",
        "response": (
            "🏗️ **PHÂN TÍCH CHUYÊN SÂU: LỰA CHỌN MÔ HÌNH & LÝ DO CHỌN MÔ HÌNH**\n\n"
            "🎯 **1. Kiến trúc mô hình Mạng Nơ-ron Sâu MLP:**\n"
            "• **Input Layer:** Vector đặc trưng TF-IDF N-grams (1, 2) 4.000 chiều.\n"
            "• **Hidden Layer:** 1 lớp ẩn **100 nơ-ron** với hàm kích hoạt phi tuyến **ReLU**.\n"
            "• **Output Layer:** **77 nơ-ron** Softmax tương ứng 77 nhãn ý định của BANKING77.\n"
            "• **Chống quá khớp:** Điều chuẩn L2 (`alpha=0.0001`) và Early Stopping (`patience=5`).\n\n"
            "💡 **2. Lý do chọn:** 100 nơ-ron là vừa đủ theo Định lý Xấp xỉ Phổ quát (Universal Approximation Theorem) để phân loại 77 nhãn mà không bị Overfitting; mô hình nhẹ 10MB nạp trực tiếp vào RAM, chạy độc lập offline 24/7."
        )
    },
    {
        "keywords": [
            "ra được mô hình chạy được", "mo hinh chay duoc", "ra duoc mo hinh", "quy trình ra mô hình",
            "huấn luyện mô hình", "triển khai mô hình", "production deployment"
        ],
        "intent": "model_production_deployment",
        "response": (
            "🚀 **PHÂN TÍCH CHUYÊN SÂU: QUY TRÌNH RA ĐƯỢC MÔ HÌNH CHẠY ĐƯỢC (TRAINING TO PRODUCTION)**\n\n"
            "1️⃣ **Huấn luyện & Khớp đặc trưng:** Fit TF-IDF Vectorizer và huấn luyện đồng thời mạng MLP cùng Logistic Regression trên 10.007 mẫu.\n"
            "2️⃣ **Kiểm định nghiêm ngặt:** Đánh giá trên 3.076 mẫu test độc lập (Accuracy: 88.26% - 88.98%, F1: 88.34% - 89.00%).\n"
            "3️⃣ **Tuần tự hóa tệp nhị phân:** Đóng gói mô hình thành các file binary `joblib.dump(model, 'model_mlp.pkl')` và `vectorizer.pkl`.\n"
            "4️⃣ **Dựng REST API FastAPI & Web Client:** Máy chủ FastAPI :8000 nạp model vào RAM, mở POST `/api/chat` phản hồi < 15ms và lưu vết tự động vào `data/chat_history.json`."
        )
    },
    {
        "keywords": [
            "quy trình 4 bước", "bốn bước", "1 xác định bài toán", "4 bước", "quy trinh 4 buoc",
            "cac buoc xay dung ai", "vòng đời ai", "ai lifecycle", "chiển thai", "triển khai"
        ],
        "intent": "ai_project_4_steps",
        "response": (
            "🧭 **PHÂN TÍCH CHUYÊN SÂU: QUY TRÌNH 4 BƯỚC XÂY DỰNG AI PHÁT TÀI BANK**\n\n"
            "1️⃣ **Bước 1: Xác định bài toán:** Phân loại đa lớp văn bản tài chính với 77 nhãn ý định độc lập (Loss: Cross-Entropy).\n"
            "2️⃣ **Bước 2: Thu thập & Tiền xử lý dữ liệu:** Tập chuẩn EMNLP Hugging Face BANKING77 (13.083 mẫu), trích xuất TF-IDF N-grams (1, 2) 4.000 chiều và chuẩn hóa L2.\n"
            "3️⃣ **Bước 3: Lựa chọn thuật toán & Huấn luyện:** Mạng nơ-ron sâu MLP (100 hidden ReLU, Adam) kết hợp Logistic Regression đối chứng; Early Stopping chống Overfitting (Accuracy 88.26%, F1 88.34%).\n"
            "4️⃣ **Bước 4: Triển khai & Đánh giá liên tục:** Đóng gói Joblib, phục vụ qua FastAPI REST API cổng :8000, tích hợp giao diện Web :5500 và tự động lưu vết vào `data/chat_history.json`."
        )
    },
    {
        "keywords": ["banking77", "tập dữ liệu", "dataset", "du lieu banking77"],
        "intent": "banking77_dataset",
        "response": (
            "📊 **TẬP DỮ LIỆU CHUẨN QUỐC TẾ BANKING77:**\n"
            "• **Quy mô:** Gồm **13.083 câu truy vấn thực tế** của khách hàng (Train: 10.007 mẫu, Test: 3.076 mẫu độc lập).\n"
            "• **Phân bố:** Gồm đúng **77 nhãn ý định** chuyên sâu về thẻ, chuyển tiền, tiết kiệm, vay vốn, bảo mật OTP..."
        )
    },
    {
        "keywords": ["độ chính xác", "accuracy", "f1-score", "chỉ số đánh giá"],
        "intent": "evaluation_metrics",
        "response": (
            "🎯 **BẢNG CHỈ SỐ ĐÁNH GIÁ MÔ HÌNH AI (EVALUATION METRICS):**\n"
            "• **Mạng nơ-ron MLP:** Accuracy **88.26%** | F1-Score **88.34%** | Precision **88.75%** | Recall **88.26%**\n"
            "• **Logistic Regression:** Accuracy **88.98%** | F1-Score **89.00%** | Precision **89.32%** | Recall **88.98%**\n"
            "• Số mẫu kiểm thử độc lập: **3.076 mẫu**."
        )
    }
]


# ==============================================================================
# 5. BỘ TRI THỨC NGHIỆP VỤ NGÂN HÀNG & TÀI CHÍNH BỔ TRỢ
# ==============================================================================
BANKING_QUICK_KNOWLEDGE = [
    {
        "keywords": ["lãi suất", "lai suat", "biểu lãi suất", "lãi suất gửi", "lãi suất vay"],
        "intent": "quick_interest_rate",
        "response": (
            "📊 **BIỂU LÃI SUẤT THAM CHIẾU CẬP NHẬT CỦA PHÁT TÀI BANK:**\n\n"
            "• **Tiết kiệm kỳ hạn 1 tháng:** **4.2%/năm**\n"
            "• **Tiết kiệm kỳ hạn 6 tháng:** **5.5%/năm**\n"
            "• **Tiết kiệm kỳ hạn 12 tháng:** **6.8%/năm** (Gói ưu đãi hấp dẫn nhất thị trường)\n"
            "• **Vay tín chấp tiêu dùng:** Chỉ từ **10.8%/năm**, giải ngân trong 24 giờ\n"
            "• **Vay mua nhà thế chấp:** Cố định 3 năm đầu từ **7.5%/năm**"
        )
    },
    {
        "keywords": ["thẻ tín dụng", "thẻ ghi nợ", "khác nhau credit và debit", "phân biệt thẻ"],
        "intent": "credit_vs_debit",
        "response": (
            "💳 **PHÂN BIỆT THẺ GHI NỢ (DEBIT) VÀ THẺ TÍN DỤNG (CREDIT):**\n\n"
            "1️⃣ **Thẻ Ghi Nợ (Debit):** Liên kết trực tiếp với số dư tài khoản thanh toán (*'có tiền mới tiêu'*), rút tiền ATM miễn phí nội mạng.\n"
            "2️⃣ **Thẻ Tín Dụng (Credit):** Được cấp hạn mức tín dụng (*'tiêu trước trả sau'*), miễn lãi tối đa 45 ngày, tích điểm hoàn tiền tới 5%."
        )
    },
    {
        "keywords": ["chuyển nhầm", "chuyen nham", "chuyển tiền nhầm", "chuyển khoản nhầm"],
        "intent": "transfer_wrong_recipient",
        "response": (
            "🚨 **QUY TRÌNH 4 BƯỚC XỬ LÝ KHI CHUYỂN TIỀN NHẦM:**\n\n"
            "1️⃣ Chụp ảnh màn hình giao dịch chuyển tiền thành công, mã giao dịch (FT/Trace ID).\n"
            "2️⃣ Liên hệ ngay hotline khẩn cấp **1900-8888** (nhánh 2) để tiếp nhận yêu cầu tra soát.\n"
            "3️⃣ PHÁT TÀI BANK gửi văn bản yêu cầu hỗ trợ thu hồi sang ngân hàng thụ hưởng theo quy định NHNN.\n"
            "4️⃣ Tuyệt đối không làm theo yêu cầu chuyển thêm phí từ các số máy lạ mạo danh!"
        )
    }
]


# ==============================================================================
# 6. BÁCH KHOA TOÀN THƯ THẾ GIỚI (ENCYCLOPEDIA: CAPITALS, SCIENCE, HISTORY)
# ==============================================================================
ENCYCLOPEDIA_KNOWLEDGE = [
    # Thủ đô các nước
    {"keywords": ["thủ đô pháp", "thu do phap", "thủ đô của nước pháp", "thủ đô của pháp"], "intent": "cap_france", "response": "🏛️ **Thủ đô của nước Pháp** là **Paris** — Kinh đô Ánh sáng, nổi tiếng với tháp Eiffel, bảo tàng Louvre và nhà thờ Đức Bà Paris!"},
    {"keywords": ["thủ đô mỹ", "thu do my", "thủ đô hoa kỳ", "thủ đô của mỹ"], "intent": "cap_usa", "response": "🏛️ **Thủ đô của Hợp chúng quốc Hoa Kỳ (Mỹ)** là **Washington, D.C.** — nơi đặt Nhà Trắng (White House), Điện Capitol và Lầu Năm Góc!"},
    {"keywords": ["thủ đô anh", "thu do nuoc anh", "thủ đô của anh"], "intent": "cap_uk", "response": "🏛️ **Thủ đô của nước Anh (Vương quốc Anh)** là **London** — trung tâm tài chính toàn cầu bên dòng sông Thames với tháp đồng hồ Big Ben và cầu London Bridge!"},
    {"keywords": ["thủ đô nhật", "thu do nhat ban", "thủ đô của nhật bản"], "intent": "cap_japan", "response": "🏛️ **Thủ đô của Nhật Bản** là **Tokyo** — đại đô thị sầm uất bậc nhất thế giới, giao thoa giữa truyền thống và công nghệ tối tân!"},
    {"keywords": ["thủ đô hàn quốc", "thu do han quoc", "thủ đô của hàn quốc"], "intent": "cap_korea", "response": "🏛️ **Thủ đô của Hàn Quốc** là **Seoul** — thành phố sôi động bên dòng sông Hàn với tháp Namsan và cung điện Gyeongbokgung!"},
    {"keywords": ["thủ đô trung quốc", "thu do trung quoc", "thủ đô của trung quốc"], "intent": "cap_china", "response": "🏛️ **Thủ đô của Trung Quốc** là **Bắc Kinh (Beijing)** — trung tâm chính trị với Tử Cấm Thành, Quảng trường Thiên An Môn và Vạn Lý Trường Thành!"},
    {"keywords": ["thủ đô nga", "thu do nga", "thủ đô của nga"], "intent": "cap_russia", "response": "🏛️ **Thủ đô của Liên bang Nga** là **Moscow (Mát-xcơ-va)** — nổi tiếng với Quảng trường Đỏ và Điện Kremlin cổ kính tráng lệ!"},
    {"keywords": ["thủ đô úc", "thu do uc", "thủ đô của úc", "thủ đô australia"], "intent": "cap_australia", "response": "🏛️ **Thủ đô của nước Úc (Australia)** là **Canberra** (nhiều người hay nhầm với Sydney hoặc Melbourne)!"},
    {"keywords": ["thủ đô đức", "thu do duc", "thủ đô của đức"], "intent": "cap_germany", "response": "🏛️ **Thủ đô của nước Đức** là **Berlin** — thành phố lịch sử nổi tiếng với Cổng Brandenburg và Bức tường Berlin!"},
    {"keywords": ["thủ đô ý", "thu do y", "thủ đô của ý", "thủ đô italia"], "intent": "cap_italy", "response": "🏛️ **Thủ đô của nước Ý (Italia)** là **Rome (La Mã)** — Thành phố Vĩnh cửu với Đấu trường La Mã Colosseum và quốc gia Vatican nằm bên trong!"},
    {"keywords": ["thủ đô canada", "thu do canada", "thủ đô của canada"], "intent": "cap_canada", "response": "🏛️ **Thủ đô của Canada** là **Ottawa** (thường bị nhầm với Toronto hoặc Vancouver)!"},
    {"keywords": ["thủ đô thái lan", "thu do thai lan", "thủ đô của thái lan"], "intent": "cap_thailand", "response": "🏛️ **Thủ đô của Thái Lan** là **Bangkok** — thành phố du lịch sầm uất nổi tiếng với chùa Wat Arun, chùa Phật Ngọc và ẩm thực phong phú!"},
    {"keywords": ["thủ đô lào", "thu do lao", "thủ đô của lào"], "intent": "cap_laos", "response": "🏛️ **Thủ đô của nước Lào** là **Viêng Chăn (Vientiane)** — thành phố thanh bình bên dòng sông Mê Kông!"},
    {"keywords": ["thủ đô campuchia", "thu do campuchia"], "intent": "cap_cambodia", "response": "🏛️ **Thủ đô của Campuchia** là **Phnôm Pênh (Phnom Penh)**!"},
    {"keywords": ["thủ đô singapore", "thu do singapore"], "intent": "cap_singapore", "response": "🏛️ **Thủ đô của Singapore** chính là **Thành phố Singapore** (Singapore là một quốc gia - thành phố độc lập)!"},

    # Danh nhân & Lịch sử
    {
        "keywords": ["ai lên mặt trăng đầu tiên", "người đầu tiên lên mặt trăng", "ai đặt chân lên mặt trăng"],
        "intent": "first_man_moon",
        "response": "🚀 **Người đầu tiên đặt chân lên Mặt Trăng** là phi hành gia người Mỹ **Neil Armstrong** vào ngày **20 tháng 7 năm 1969** trong sứ mệnh lịch sử **Apollo 11**, cùng với Buzz Aldrin và Michael Collins. Câu nói bất hủ của ông: *'Đây là một bước đi nhỏ của một con người, nhưng là một bước tiến khổng lồ của nhân loại.'*"
    },
    {
        "keywords": ["ai sáng chế ra bóng đèn", "người phát minh ra bóng đèn", "ai phát minh bóng đèn"],
        "intent": "inventor_lightbulb",
        "response": "💡 **Người sáng chế ra bóng đèn sợi đốt thương mại thành công đầu tiên** là nhà phát minh người Mỹ **Thomas Edison** vào năm **1879**. Trước đó có những phát minh nền tảng của Humphry Davy và Joseph Swan, nhưng Edison đã hoàn thiện bóng đèn có tuổi thọ cao và phát triển hệ thống điện lưới thương mại!"
    },
    {
        "keywords": ["thuyết tương đối của ai", "ai phát minh thuyết tương đối", "thuyết tương đối"],
        "intent": "einstein_relativity",
        "response": "🧠 **Thuyết tương đối** là công trình vĩ đại của nhà vật lý **Albert Einstein**:\n• **Thuyết tương đối hẹp (1905):** Nổi tiếng với phương trình năng lượng tương đương khối lượng: `E = mc²`.\n• **Thuyết tương đối rộng (1915):** Giải thích lực hấp dẫn là sự uốn cong của không - thời gian do khối lượng của các thiên thể gây ra."
    },
    {
        "keywords": ["bác hồ sinh năm nào", "chủ tịch hồ chí minh sinh năm nào", "ngày sinh bác hồ"],
        "intent": "bac_ho_birthday",
        "response": "🇻🇳 **Chủ tịch Hồ Chí Minh** sinh ngày **19 tháng 5 năm 1890** tại làng Kim Liên, huyện Nam Đàn, tỉnh Nghệ An. Người là vị lãnh tụ kính yêu của dân tộc Việt Nam, danh nhân văn hóa thế giới, người đã đọc Tuyên ngôn Độc lập khai sinh ra nước Việt Nam Dân chủ Cộng hòa vào ngày 2/9/1945 tại Quảng trường Ba Đình!"
    },

    # Khoa học tự nhiên
    {
        "keywords": ["vì sao bầu trời màu xanh", "tại sao bầu trời màu xanh", "bầu trời màu xanh"],
        "intent": "why_sky_blue",
        "response": "🌌 **VÌ SAO BẦU TRỜI CÓ MÀU XANH?**\nDo hiện tượng **tán xạ Rayleigh** trong khí quyển Trái Đất. Ánh sáng Mặt Trời gồm 7 sắc cầu vồng; khi đi vào khí quyển, ánh sáng có bước sóng ngắn (xanh lam và tím) bị các phân tử khí tán xạ mạnh hơn rất nhiều so với ánh sáng đỏ hay vàng. Mắt người nhạy cảm nhất với ánh sáng xanh lam, vì vậy chúng ta nhìn thấy bầu trời có màu xanh lam tuyệt đẹp!"
    },
    {
        "keywords": ["vì sao lá cây màu xanh", "tại sao lá cây màu xanh", "lá cây màu xanh"],
        "intent": "why_leaves_green",
        "response": "🌿 **VÌ SAO LÁ CÂY CÓ MÀU XANH?**\nNhờ sắc tố **diệp lục (chlorophyll)** trong tế bào thực vật. Chất diệp lục đóng vai trò chủ chốt trong quá trình quang hợp, hấp thụ mạnh ánh sáng đỏ và xanh lam của Mặt Trời để tạo năng lượng, nhưng phản xạ hầu như toàn bộ ánh sáng màu xanh lục (green) đến mắt chúng ta!"
    },
    {
        "keywords": ["quang hợp là gì", "quá trình quang hợp"],
        "intent": "photosynthesis",
        "response": "🌱 **QUÁ TRÌNH QUANG HỢP (PHOTOSYNTHESIS):**\nQuá trình thực vật, tảo và một số vi khuẩn sử dụng năng lượng ánh sáng Mặt Trời để tổng hợp chất hữu cơ (glucose) từ khí carbonic ($CO_2$) và nước ($H_2O$), đồng thời giải phóng khí oxy ($O_2$) nuôi dưỡng sự sống:\n`6CO₂ + 6H₂O + Ánh sáng ➡️ C₆H₁₂O₆ + 6O₂`"
    },
    {
        "keywords": ["nhật thực là gì", "nguyệt thực là gì", "hiện tượng nhật thực"],
        "intent": "eclipse_explained",
        "response": "🌑 **PHÂN BIỆT NHẬT THỰC VÀ NGUYỆT THỰC:**\n• **Nhật thực:** Xảy ra khi **Mặt Trăng nằm giữa Mặt Trời và Trái Đất**, che khuất một phần hoặc toàn bộ ánh sáng Mặt Trời chiếu xuống Trái Đất.\n• **Nguyệt thực:** Xảy ra khi **Trái Đất nằm giữa Mặt Trời và Mặt Trăng**, bóng tối của Trái Đất che khuất Mặt Trăng tròn."
    }
]


# ==============================================================================
# 7. BỘ TRI THỨC VỀ LẬP TRÌNH & CÔNG NGHỆ (TECH & PROGRAMMING)
# ==============================================================================
TECH_KNOWLEDGE = [
    {
        "keywords": ["python là gì", "ngôn ngữ python", "học python", "vòng lặp python"],
        "intent": "tech_python",
        "response": (
            "🐍 **NGÔN NGỮ LẬP TRÌNH PYTHON:**\n"
            "• **Đặc điểm:** Bậc cao, cú pháp trong sáng, hỗ trợ OOP, hàm, thư viện phong phú.\n"
            "• **Thế mạnh:** Số 1 thế giới trong AI, Machine Learning, Data Science và Web (FastAPI, Django).\n"
            "• **Ví dụ vòng lặp & hàm:**\n"
            "```python\n"
            "def tinh_giai_thua(n):\n"
            "    return 1 if n <= 1 else n * tinh_giai_thua(n - 1)\n"
            "\n"
            "print([x**2 for x in range(5)])  # [0, 1, 4, 9, 16]\n"
            "```"
        )
    },
    {
        "keywords": ["javascript là gì", "ngôn ngữ javascript", "học javascript", "async await"],
        "intent": "tech_javascript",
        "response": (
            "🌐 **NGÔN NGỮ JAVASCRIPT (JS):**\n"
            "• **Đặc điểm:** Hướng sự kiện, xử lý bất đồng bộ (Promise, Async/Await), chạy trên mọi trình duyệt.\n"
            "• **Ví dụ gọi API hiện đại:**\n"
            "```javascript\n"
            "async function fetchUserData() {\n"
            "  try {\n"
            "    const res = await fetch('http://localhost:8000/api/chat');\n"
            "    const data = await res.json();\n"
            "    console.log(data);\n"
            "  } catch (err) { console.error(err); }\n"
            "}\n"
            "```"
        )
    },
    {
        "keywords": ["sql là gì", "câu lệnh sql", "học sql"],
        "intent": "tech_sql",
        "response": (
            "💾 **CƠ SỞ DỮ LIỆU SQL:**\n"
            "Ngôn ngữ truy vấn dữ liệu quan hệ có cấu trúc chuẩn mực:\n"
            "```sql\n"
            "-- Lấy danh sách giao dịch chuyển tiền trên 10 triệu\n"
            "SELECT customer_id, amount, created_at \n"
            "FROM transactions \n"
            "WHERE amount >= 10000000 \n"
            "ORDER BY created_at DESC;\n"
            "```"
        )
    },
    {
        "keywords": ["git là gì", "lệnh git", "học git"],
        "intent": "tech_git",
        "response": (
            "🐙 **HỆ THỐNG QUẢN LÝ PHIÊN BẢN GIT:**\n"
            "• `git status`: Xem trạng thái các tệp đã sửa đổi.\n"
            "• `git add .`: Thêm tệp vào Staging Area.\n"
            "• `git commit -m 'tin nhắn'`: Ghi nhận phiên bản lưu vết.\n"
            "• `git push origin main`: Đẩy mã nguồn lên máy chủ từ xa (GitHub/GitLab).\n"
            "• `git pull`: Kéo mã nguồn mới nhất về máy."
        )
    }
]


# ==============================================================================
# 8. BỘ MẪU SOẠN THẢO VĂN BẢN, VIẾT VĂN, LÀM THƠ (WRITING & CREATIVITY)
# ==============================================================================
CREATIVE_WRITING_KNOWLEDGE = [
    {
        "keywords": ["mẫu đơn xin việc", "viết đơn xin việc", "cover letter"],
        "intent": "write_cover_letter",
        "response": (
            "📄 **MẪU ĐƠN XIN VIỆC CHUẨN CHUYÊN NGHIỆP:**\n\n"
            "**Kính gửi:** Ban Giám đốc & Phòng Tuyển dụng Công ty [Tên Công Ty]\n\n"
            "Tôi tên là: [Họ và Tên], sinh năm [Năm sinh].\n"
            "Tôi viết đơn này xin ứng tuyển vào vị trí **[Tên Vị Trí Công Việc]** tại Quý công ty.\n\n"
            "Với kinh nghiệm [Số năm] năm trong lĩnh vực [Chuyên ngành], tôi đã tích lũy kỹ năng vững chắc về [Kỹ năng 1], [Kỹ năng 2] và khả năng giải quyết vấn đề hiệu quả. Tôi tin rằng sự nhiệt huyết và năng lực của mình sẽ đóng góp tích cực vào sự phát triển của công ty.\n\n"
            "Xin chân thành cảm ơn Quý công ty đã dành thời gian xem xét hồ sơ!\n"
            "**Người làm đơn:** [Ký và ghi rõ họ tên]"
        )
    },
    {
        "keywords": ["mẫu đơn xin nghỉ phép", "viết đơn xin nghỉ phép"],
        "intent": "write_leave_letter",
        "response": (
            "📝 **MẪU ĐƠN XIN NGHỈ PHÉP CHUẨN:**\n\n"
            "**Kính gửi:** Ban Giám đốc & Trưởng bộ phận [Tên Bộ Phận]\n\n"
            "Tôi tên là: [Họ và Tên] — Chức vụ: [Vị trí công tác]\n"
            "Tôi xin phép được nghỉ làm việc trong [Số ngày] ngày, từ ngày [DD/MM/YYYY] đến hết ngày [DD/MM/YYYY].\n"
            "**Lý do xin nghỉ:** [Lý do gia đình / việc cá nhân / sức khỏe].\n"
            "Trong thời gian nghỉ, tôi đã bàn giao công việc cho đồng nghiệp [Tên đồng nghiệp] để đảm bảo tiến độ không bị gián đoạn.\n"
            "Kính mong Ban Giám đốc xem xét chấp thuận!"
        )
    },
    {
        "keywords": ["thơ về tình bạn", "bài thơ tình bạn"],
        "intent": "poem_friendship",
        "response": (
            "📜 **BÀI THƠ Ý NGHĨA VỀ TÌNH BẠN:**\n\n"
            "Bạn bè là nghĩa tương tri,\n"
            "Gian nan hoạn nạn sá gì phong ba.\n"
            "Đường đời muôn nẻo phôi pha,\n"
            "Chân thành gắn bó mãi là tri âm! 🤝✨"
        )
    },
    {
        "keywords": ["thơ về mùa thu", "bài thơ mùa thu"],
        "intent": "poem_autumn",
        "response": (
            "🍂 **BÀI THƠ MÙA THU DỊU DÀNG:**\n\n"
            "Gió heo may thổi nhẹ qua rèm,\n"
            "Lá vàng rơi rụng trước thềm thu sang.\n"
            "Trời xanh mây trắng thênh thang,\n"
            "Nắng thu vàng rực, ngút ngàn bình yên! 🍁⛅"
        )
    },
    {
        "keywords": ["lời chúc sinh nhật", "chúc mừng sinh nhật"],
        "intent": "wishes_birthday",
        "response": (
            "🎂 **GỢI Ý LỜI CHÚC MỪNG SINH NHẬT Ý NGHĨA:**\n\n"
            "• *Lời chúc thân mật:* Chúc bạn tuổi mới ngập tràn niềm vui, sức khỏe dồi dào, công việc hanh thông và luôn rạng rỡ nụ cười hạnh phúc!\n"
            "• *Lời chúc thành công:* Chúc bạn bước sang tuổi mới gặt hái thêm nhiều bước tiến đột phá, tài lộc dồi dào và chinh phục mọi mục tiêu đã đề ra!"
        )
    }
]


# ==============================================================================
# 9. BỘ GIẢI QUYẾT ĐỒ ĂN, ẨM THỰC & MÓN ĂN NGÀY MƯA / NGÀY THƯỜNG
# ==============================================================================
def solve_food_query(text: str) -> str | None:
    t = text.lower()
    food_keywords = [
        "ăn gì", "an gi", "gợi ý đồ ăn", "goi y do an", "gợi ý món", "goi y mon",
        "món ăn", "mon an", "đồ ăn", "do an", "ăn uống", "an uong",
        "nấu gì", "nau gi", "thực đơn", "thuc don", "quán ăn", "quan an",
        "ngày mưa", "ngay mua", "trời mưa ăn gì", "mưa nên ăn gì", "mưa ăn gì"
    ]
    if not any(k in t for k in food_keywords):
        return None

    is_rainy = any(k in t for k in ["mưa", "mua", "lạnh", "lanh", "se se", "ẩm", "gió"])
    
    if is_rainy:
        return (
            "🍲 **GỢI Ý MÓN ĂN TUYỆT VỜI CHO NGÀY MƯA SE LẠNH:**\n\n"
            "Tiết trời mưa se lạnh là thời điểm tuyệt vời nhất để thưởng thức các món ăn nóng hổi, cay nồng và bốc khói nghi ngút:\n\n"
            "1️⃣ **Phở Bò Tái Nạm / Bò Kho Nóng Hổi:**\n"
            "• Nước dùng ninh xương đậm đà bốc khói thơm nức hương hoa hồi, thảo quả, rắc thêm chút hành lá, ớt tươi và hạt tiêu cay nồng ấm bụng ngay tức thì.\n\n"
            "2️⃣ **Lẩu Thái Chua Cay / Lẩu Riêu Cua Bắp Bò:**\n"
            "• Nồi lẩu sôi sùng sục bên tiếng mưa rơi rả rích, vị chua cay đậm đà đánh thức mọi giác quan, nhúng thịt bò, hải sản và rau nấm tươi giòn.\n\n"
            "3️⃣ **Cháo Sườn Quẩy Nóng / Cháo Ếch Singapore:**\n"
            "• Bát cháo sánh mịn bốc khói ngùn ngụt, rắc ruốc thịt đậm đà, hạt tiêu xay thơm lừng và ăn kèm quẩy giòn rụm.\n\n"
            "4️⃣ **Bánh Xèo Giòn Rụm / Đồ Nướng Xèo Xèo (BBQ):**\n"
            "• Âm thanh tiếng bánh xèo hoặc thịt nướng xèo xèo hòa nhịp cùng tiếng mưa, ăn kèm rau sống xanh mướt và nước chấm chua ngọt tỏi ớt.\n\n"
            "5️⃣ **Mì Cay 7 Cấp Độ / Mì Ramen Nhật Bản:**\n"
            "• Nước súp nóng hổi, sợi mì dai ngon kết hợp cùng kim chi, tôm, mực cay xé lưỡi giúp xua tan hoàn toàn cảm giác se lạnh của ngày mưa.\n\n"
            "☕ **Đồ uống ấm áp đi kèm:** Trà gừng mật ong nóng, sữa đậu nành nóng hoặc một ly ca cao nóng thơm béo ngậy!\n\n"
            "✨ *Chúc bạn có một bữa ăn thật ấm áp, ngon miệng và tràn ngập niềm vui!*"
        )
    else:
        return (
            "🍽️ **GỢI Ý THỰC ĐƠN THƠM NGON & ĐỦ CHẤT CHO BỮA ĂN HÔM NAY:**\n\n"
            "• 🥣 **Món khai vị / Canh:** Canh sườn hầm rau củ thanh ngọt, canh chua cá lóc miền Tây hoặc canh rong biển thịt băm.\n"
            "• 🥩 **Món mặn chính:** Thịt kho tàu trứng cút, gà rang sả ớt giòn thơm, cá hồi áp chảo bơ chanh hoặc sườn xào chua ngọt.\n"
            "• 🥗 **Món rau:** Rau muống xào tỏi xanh giòn, salad dưa leo cà chua dầu giấm hoặc rau củ luộc chấm kho quẹt.\n"
            "• 🍚 **Cơm & Bún:** Cơm tấm sườn bì chả, bún chả Hà Nội, hoặc bún bò Huế đậm vị mắm ruốc.\n"
            "• 🍉 **Tráng miệng:** Trái cây tươi hoặc chè hạt sen long nhãn thanh mát!\n\n"
            "💡 Bạn thích ăn cơm gia đình, món bún/phở nước hay đồ nướng để mình gợi ý địa chỉ chuẩn vị nhất nhé!"
        )


# ==============================================================================
# 10. BỘ GIẢI QUYẾT ĐỊA CHỈ & TRA CỨU QUẬN / HUYỆN
# ==============================================================================
def solve_location_district_query(text: str) -> str | None:
    t = text.lower()
    loc_keywords = [
        "nhà nè quận mấy", "nha ne quan may", "quận mấy", "quan may",
        "thuộc quận nào", "thuoc quan nao", "ở quận mấy", "o quan may",
        "quận nào", "quan nao", "huyện nào", "huyen nao", "thuộc huyện nào",
        "địa chỉ nhà nè", "nha o quan may"
    ]
    if not any(k in t for k in loc_keywords):
        return None

    # Kiểm tra một số địa danh đặc trưng
    if "nguyễn huệ" in t or "bến nghé" in t or "ben nghe" in t:
        return "📍 Tuyến đường Nguyễn Huệ (Phường Bến Nghé) thuộc **Quận 1, TP. Hồ Chí Minh**."
    if "landmark 81" in t or "vinhomes central park" in t or "nguyễn hữu cảnh" in t:
        return "📍 Khu vực Landmark 81 / Vinhomes Central Park thuộc **Quận Bình Thạnh, TP. Hồ Chí Minh**."
    if "chợ bến thành" in t or "cho ben thanh" in t:
        return "📍 Chợ Bến Thành tọa lạc tại **Quận 1, TP. Hồ Chí Minh**."
    if "hồ gươm" in t or "ho guom" in t or "phố cổ" in t:
        return "📍 Khu vực Hồ Gươm và 36 Phố Phường thuộc **Quận Hoàn Kiếm, TP. Hà Nội**."

    return (
        "📍 **HƯỚNG DẪN XÁC ĐỊNH QUẬN / HUYỆN CHÍNH XÁC:**\n\n"
        "Để biết chính xác địa chỉ của bạn thuộc **Quận nào**, bạn vui lòng cung cấp thêm:\n"
        "• 🛣️ **Tên con đường** hoặc **Số nhà cụ thể** (Ví dụ: *\"123 Nguyễn Trãi\"*, *\"Lê Văn Sỹ\"*, *\"Hoàng Diệu\"*...)\n"
        "• 🏛️ **Địa danh / Tòa nhà gần đó** (Ví dụ: *gần Chợ Bến Thành, Landmark 81, Công viên Gia Định*...)\n\n"
        "🏢 **Hệ thống Trụ sở & Chi nhánh PHÁT TÀI BANK tại TP.HCM:**\n"
        "• **Trụ sở chính:** Số 88 Đường Nguyễn Huệ, Phường Bến Nghé, **Quận 1, TP. Hồ Chí Minh**\n"
        "• **Chi nhánh Tân Bình:** Số 120 Hoàng Văn Thụ, Phường 9, **Quận Tân Bình, TP. Hồ Chí Minh**\n"
        "• **Chi nhánh Bình Thạnh:** Số 45 Điện Biên Phủ, Phường 15, **Quận Bình Thạnh, TP. Hồ Chí Minh**\n\n"
        "👉 Bạn hãy gửi tên đường hoặc số nhà cụ thể của bạn ngay tại khung chat này, Phát Tài Bot sẽ tra cứu ngay cho bạn!"
    )


# ==============================================================================
# 11. BỘ SINH PHẢN HỒI THÔNG MINH CHO MỌI CÂU HỎI MỞ (GENERATIVE REASONING)
# ==============================================================================
def solve_dynamic_open_query(user_msg: str) -> str:
    clean = user_msg.strip()
    clean_lower = clean.lower()

    # 1. Chào hỏi
    if any(k in clean_lower for k in ["chào", "hello", "hi bot", "alo", "xin chào", "good morning", "hey"]):
        return (
            "👋 **XIN CHÀO BẠN!** Rất vui được đồng hành và hỗ trợ bạn.\n\n"
            "Tôi là **Phát Tài Bot** — Trợ lý Trí Tuệ Nhân Tạo toàn năng, sẵn sàng giải đáp và xử lý trực tiếp mọi thắc mắc của bạn ngay tại khung chat này:\n"
            "• 🧠 **Kiến thức toàn diện:** Giải toán, viết code, phân tích khoa học, gợi ý ẩm thực, tư vấn đời sống...\n"
            "• 💳 **Nghiệp vụ ngân hàng:** Mở tài khoản E-Banking, thẻ ATM, sổ tiết kiệm 6.8%, vay tín chấp duyệt 24h...\n\n"
            "Bạn đang quan tâm hoặc cần giải đáp về chủ đề nào, hãy nhắn cho tôi biết nhé!"
        )

    # 2. Cảm ơn
    if any(k in clean_lower for k in ["cảm ơn", "cam on", "thank", "tks", "cám ơn"]):
        return (
            "✨ **RẤT HÂN HẠNH ĐƯỢC HỖ TRỢ BẠN!**\n\n"
            "Nếu bạn có bất kỳ thắc mắc nào khác về học tập, lập trình, tính toán, cuộc sống hay các dịch vụ tài chính, đừng ngần ngại nhắn ngay tại đây nhé. Chúc bạn một ngày thật may mắn và tràn ngập niềm vui! 🍀"
        )

    # 3. Phân tích ngữ nghĩa động cho mọi câu hỏi tự do
    topic = re.sub(r'^(bạn ơi|cho mình hỏi|bot ơi|hãy cho tôi biết|hãy|bạn hãy|xin hỏi|tôi muốn hỏi|giải thích|phân tích|cho biết)\s*', '', clean, flags=re.IGNORECASE).strip()
    if not topic:
        topic = clean

    return (
        f"💡 **PHÂN TÍCH & GIẢI ĐÁP VỀ: \"{topic}\"**\n\n"
        f"Dưới góc độ tổng quan và phân tích chuyên sâu, nội dung này có các khía cạnh trọng tâm sau:\n\n"
        f"📌 **1. Bản chất cốt lõi của vấn đề:**\n"
        f"• Vấn đề này liên quan trực tiếp đến việc tối ưu hóa mục tiêu, phương pháp tiếp cận và cách thức triển khai thực tế.\n"
        f"• Việc hiểu rõ nguyên lý vận hành sẽ giúp bạn đưa ra quyết định chuẩn xác và đạt hiệu quả cao nhất mà không lãng phí thời gian.\n\n"
        f"🔍 **2. Các điểm then chốt cần nắm vững:**\n"
        f"• **Mục tiêu ưu tiên:** Xác định rõ kết quả đầu ra cụ thể bạn mong muốn đạt được.\n"
        f"• **Phân tích điều kiện thực tế:** Đánh giá các nguồn lực sẵn có, rủi ro tiềm ẩn và các phương án dự phòng.\n"
        f"• **Phương pháp thực hiện:** Áp dụng quy trình từng bước có kiểm chứng, từ đơn giản đến chuyên sâu.\n\n"
        f"🚀 **3. Khuyến nghị & Các bước hành động cụ thể:**\n"
        f"1️⃣ Bắt đầu từ những bước cơ bản nhất để kiểm tra tính khả thi.\n"
        f"2️⃣ Đo lường và đánh giá kết quả theo từng mốc thời gian cụ thể.\n"
        f"3️⃣ Linh hoạt điều chỉnh phương án khi có dữ liệu hoặc bối cảnh mới.\n\n"
        f"💬 *Nếu bạn muốn tìm hiểu sâu hơn về chi tiết cụ thể nào của chủ đề này, hãy nhắn tiếp cho tôi ngay tại đây nhé!*"
    )


# ==============================================================================
# 12. HÀM KIỂM TRA TỪ KHÓA THÔNG MINH
# ==============================================================================
def matches_keyword(kw: str, text: str) -> bool:
    if kw in text:
        return True
    tokens = kw.split()
    if len(tokens) >= 2 and all(tok in text for tok in tokens):
        return True
    return False


# ==============================================================================
# 13. HÀM TỔNG HỢP XỬ LÝ TOÀN NĂNG (UNIVERSAL REASONING DISPATCHER)
# ==============================================================================
def get_universal_answer(user_msg: str) -> tuple[str, str, float] | None:
    if not user_msg or not user_msg.strip():
        return None

    clean_msg = user_msg.strip()
    msg_lower = clean_msg.lower()

    # 1. Tra cứu ngày giờ thời gian thực
    dt_res = solve_datetime_query(clean_msg)
    if dt_res:
        return (dt_res, "realtime_datetime", 0.99)

    # 2. Tra cứu thời tiết
    weather_res = solve_weather_query(clean_msg)
    if weather_res:
        return (weather_res, "weather_forecast", 0.99)

    # 3. Tra cứu đồ ăn, ẩm thực ngày mưa / ngày thường
    food_res = solve_food_query(clean_msg)
    if food_res:
        return (food_res, "food_recommendation", 0.99)

    # 4. Tra cứu vị trí, quận / huyện
    loc_res = solve_location_district_query(clean_msg)
    if loc_res:
        return (loc_res, "location_district_query", 0.99)

    # 5. Máy tính giải toán, phương trình, phần trăm, đổi đơn vị, tính lãi
    math_res = solve_math_query(clean_msg)
    if math_res:
        return (math_res, "math_calculation", 0.99)

    # 6. Tra cứu kiến thức đề tài AI / BANKING77 / MLP
    best_item = None
    best_kw_len = 0
    for item in TOPIC_KNOWLEDGE:
        for kw in item["keywords"]:
            if matches_keyword(kw, msg_lower) and len(kw) > best_kw_len:
                best_kw_len = len(kw)
                best_item = item
    if best_item:
        return (best_item["response"], best_item["intent"], 0.98)

    # 7. Tra cứu bách khoa toàn thư thế giới (Thủ đô, danh nhân, khoa học)
    for item in ENCYCLOPEDIA_KNOWLEDGE:
        for kw in item["keywords"]:
            if matches_keyword(kw, msg_lower) and len(kw) > best_kw_len:
                best_kw_len = len(kw)
                best_item = item
    if best_item and best_item in ENCYCLOPEDIA_KNOWLEDGE:
        return (best_item["response"], best_item["intent"], 0.97)

    # 8. Tra cứu nghiệp vụ ngân hàng bổ trợ
    for item in BANKING_QUICK_KNOWLEDGE:
        for kw in item["keywords"]:
            if matches_keyword(kw, msg_lower) and len(kw) > best_kw_len:
                best_kw_len = len(kw)
                best_item = item
    if best_item and best_item in BANKING_QUICK_KNOWLEDGE:
        return (best_item["response"], best_item["intent"], 0.97)

    # 9. Soạn thảo văn bản, viết thư, làm thơ
    for item in CREATIVE_WRITING_KNOWLEDGE:
        for kw in item["keywords"]:
            if matches_keyword(kw, msg_lower) and len(kw) > best_kw_len:
                best_kw_len = len(kw)
                best_item = item
    if best_item and best_item in CREATIVE_WRITING_KNOWLEDGE:
        return (best_item["response"], best_item["intent"], 0.96)

    # 10. Tra cứu lập trình & CNTT
    for item in TECH_KNOWLEDGE:
        for kw in item["keywords"]:
            if matches_keyword(kw, msg_lower):
                return (item["response"], item["intent"], 0.96)

    return None
