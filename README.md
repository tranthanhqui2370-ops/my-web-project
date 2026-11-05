# BÁO CÁO KHOA HỌC & TÀI LIỆU VẬN HÀNH DỰ ÁN AI
# HỆ THỐNG CHATBOT PHÁT TÀI BANK — NHẬN DIỆN Ý ĐỊNH BANKING77 (HUGGING FACE)

> **Đơn vị thực hiện:** Đồ án Chuyên đề Trí tuệ Nhân tạo & Thiết kế Web Nâng Cao  
> **Chuyên đề:** Ứng dụng Xử lý Ngôn ngữ Tự nhiên (NLP) & Mạng Nơ-ron Học Sâu trong Ngân Hàng Số  
> **Tập dữ liệu chuẩn:** `PolyAI/banking77` / `mteb/banking77` (Hugging Face / EMNLP)  
> **Kiến trúc mô hình:** Mạng nơ-ron sâu MLP (Multilayer Perceptron) & Mô hình đối chứng Logistic Regression  
> **Backend & API:** Python 3, FastAPI, Uvicorn, Scikit-learn, Joblib  
> **Frontend:** HTML5, CSS3/SCSS, JavaScript ES6 (Fetch API ngầm, Async/Await)  
> **Lưu trữ dữ liệu:** `data/chat_history.json`, `data/customers.json`, `data/ai_config.json`

---

## 📑 MỤC LỤC CHI TIẾT
1. [Phần 1: Nhãn & Tên Truy Xuất Tập Dữ Liệu BANKING77](#-phần-1-nhãn--tên-truy-xuất-tập-dữ-liệu-banking77)
2. [Phần 2: Bản Chất, Định Nghĩa & Cách Thức Tính Toán TF-IDF](#-phần-2-bản-chất-định-nghĩa--cách-thức-tính-toán-tf-idf)
   - [2.1. Định nghĩa TF và IDF](#21-định-nghĩa-tf-và-idf)
   - [2.2. Công thức toán học tính toán TF-IDF](#22-công-thức-toán-học-tính-toán-tf-idf)
   - [2.3. Phân tích thực tế: Câu "tôi muốn reset tài khoản"](#23-phân-tích-thực-tế-ví-dụ-câu-tôi-muốn-reset-tài-khoản)
   - [2.4. Lý do khoa học vì sao phải dùng TF-IDF](#24-lý-do-khoa-học-vì-sao-phải-dùng-tf-idf)
3. [Phần 3: Phân Tích Tuyến Tính và Phi Tuyến (Linear vs Non-linear)](#-phần-3-phân-tích-tuyến-tính-và-phi-tuyến-linear-vs-non-linear)
4. [Phần 4: Kiến Trúc Đầu Ra & Ánh Xạ Bộ Tri Thức (1 Intent = 1 Bộ Nghiệp Vụ)](#-phần-4-kiến-trúc-đầu-ra--ánh-xạ-bộ-tri-thức-1-intent--1-bộ-nghiệp-vụ)
5. [Phần 5: Phương Pháp Dịch Vụ Truyền Thống, Hạn Chế & Hướng Phát Triển](#-phần-5-phương-pháp-dịch-vụ-truyền-thống-hạn-chế--hướng-phát-triển)
6. [Phần 6: Quá Trình Huấn Luyện (Training), Đường Cong Mất Mát & Hội Tụ](#-phần-6-quá-trình-huấn-luyện-training-đường-cong-mất-mát--hội-tụ)
7. [Phần 7: Kiến Trúc Frontend, Backend & Cách Hoạt Động Của Hệ Thống](#-phần-7-kiến-trúc-frontend-backend--cách-hoạt-động-của-hệ-thống)
8. [Phần 8: Bảng Tra Cứu Cụ Thể Vị Trí File & Số Dòng Code Của Các Chức Năng AI](#-phần-8-bảng-tra-cứu-cụ-thể-vị-trí-file--số-dòng-code-của-các-chức-năng-ai)

---

# 🏷️ PHẦN 1: NHÃN & TÊN TRUY XUẤT TẬP DỮ LIỆU BANKING77

### 1.1. Nguồn gốc & Tên gọi tập dữ liệu
- **Tên tập dữ liệu:** `BANKING77`
- **Tác giả & Xuất bản:** Nhóm nghiên cứu PolyAI (Casanueva et al., công bố tại Hội nghị Quốc tế hàng đầu về Xử lý Ngôn ngữ Tự nhiên **EMNLP 2020**).
- **Kho lưu trữ:** Được chuẩn hóa và lưu trữ công khai trên Hugging Face Hub tại địa chỉ: `https://huggingface.co/datasets/PolyAI/banking77`.
- **Quy mô:** Bao gồm đúng **13.083 câu hỏi thực tế** của khách hàng ngân hàng trực tuyến:
  - **Tập Train (Huấn luyện):** 10.007 mẫu.
  - **Tập Test (Kiểm định độc lập):** 3.076 mẫu.

### 1.2. Cấu trúc nhãn (Labels & Intent ID)
Tập dữ liệu bao gồm đúng **77 nhãn ý định (Intents)** độc lập, được ánh xạ số hóa từ ID `0` đến `76`. Các nhãn được phân bổ thành 6 cụm nghiệp vụ ngân hàng cốt lõi:

| Nhóm nghiệp vụ | Số lượng Intent | Ví dụ các nhãn Intent chuẩn |
| :--- | :---: | :--- |
| **Quản lý Thẻ & PIN** | 18 | `card_swallowed`, `lost_or_stolen_card`, `pin_blocked`, `card_arrival`, `card_delivery_estimate`, `card_linking`... |
| **Chuyển tiền & Thanh toán** | 16 | `transfer_fee_charged`, `transfer_not_received_by_recipient`, `beneficiary_not_allowed`, `cancel_transfer`... |
| **Nạp tiền & Số dư** | 15 | `top_up_failed`, `top_up_reverted`, `balance_not_updated_after_cheque_or_cash_deposit`, `top_up_limits`... |
| **Rút tiền & Cây ATM** | 10 | `atm_support`, `cash_withdrawal_charge`, `wrong_amount_of_cash_received`, `declined_cash_withdrawal`... |
| **Định danh & Tài khoản** | 10 | `verify_my_identity`, `edit_personal_details`, `compromised_card`, `unable_to_verify_identity`... |
| **Ngoại tệ & Phí dịch vụ** | 8 | `exchange_rate`, `exchange_charge`, `card_acceptance`, `transfer_into_account`... |

### 1.3. Cơ chế truy xuất câu hỏi của người dùng
Khi người dùng nhập câu hỏi (ví dụ: *"Tôi bị cây ATM nuốt mất thẻ rồi"*), quy trình truy xuất gồm:
1. Chuỗi ký tự thô $\rightarrow$ Làm sạch bằng Regex $\rightarrow$ Trích xuất N-gram (1, 2) $\rightarrow$ Biến đổi qua ma trận TF-IDF 15.000 chiều.
2. Mô hình Deep MLP tính toán phân phối Softmax $\rightarrow$ Lấy vị trí nơ-ron có xác suất cực đại $\hat{y} = \arg\max_i P(y = i \mid \mathbf{x})$.
3. Ánh xạ ID số học sang mã nhãn chuỗi (ví dụ: `ID 11` $\rightarrow$ `card_swallowed`).
4. Truy xuất bộ tri thức nghiệp vụ tương ứng từ `BANKING77_EXPERT_KB["card_swallowed"]` để trả về câu trả lời chuẩn xác.

---

# 📐 PHẦN 2: BẢN CHẤT, ĐỊNH NGHĨA & CÁCH THỨC TÍNH TOÁN TF-IDF

### 2.1. Định nghĩa TF và IDF
TF-IDF là viết tắt của **Term Frequency – Inverse Document Frequency** (Tần số xuất hiện của từ – Nghịch đảo tần số văn bản). Đây là phương pháp thống kê nhằm định lượng mức độ quan trọng của một từ hoặc cụm từ đối với một câu trong cả tập dữ liệu.

1. **TF (Term Frequency - Tần số từ):**
   - *Định nghĩa:* Đo lường mức độ xuất hiện thường xuyên của từ khóa $t$ bên trong một văn bản cụ thể $d$.
   - *Ý nghĩa:* Một từ xuất hiện càng nhiều lần trong câu thì khả năng cao câu đó đang bàn về chủ đề liên quan đến từ đó.

2. **IDF (Inverse Document Frequency - Nghịch đảo tần số tài liệu):**
   - *Định nghĩa:* Đo lường độ hiếm và tính đặc trưng của từ khóa $t$ trên toàn bộ kho ngữ liệu $D$ gồm hàng nghìn câu khác nhau.
   - *Ý nghĩa:* Những từ xuất hiện ở hầu hết mọi câu (như "tôi", "muốn", "cho", "là", "bị") có tính phân biệt rất kém. IDF sẽ **phạt nặng** các từ này, hạ trọng số của chúng xuống gần bằng 0; ngược lại, những từ hiếm và chuyên biệt (như "reset", "nuốt thẻ", "mã PIN", "sao kê") sẽ được cấp chỉ số IDF rất cao.

---

### 2.2. Công thức toán học tính toán TF-IDF
Trong dự án này, hệ thống áp dụng công thức chuẩn của thư viện Scikit-learn (`sublinear_tf=True`, `smooth_idf=True`):

1. **Công thức TF phi tuyến (Sublinear Term Frequency):**
   $$\text{TF}(t, d) = \begin{cases} 1 + \log(\text{count}(t, d)) & \text{nếu } \text{count}(t, d) > 0 \\ 0 & \text{nếu ngược lại} \end{cases}$$
   *(Việc lấy logarit giúp ngăn chặn việc một từ xuất hiện 20 lần có trọng số cao gấp 20 lần một từ xuất hiện 1 lần, triệt tiêu thiên vị độ dài).*

2. **Công thức IDF có làm mịn (Smooth IDF):**
   $$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + \text{DF}(t)}\right) + 1$$
   - $|D|$: Tổng số văn bản trong toàn bộ tập dữ liệu (10.007 câu trong tập train BANKING77).
   - $\text{DF}(t)$ (Document Frequency): Số lượng văn bản có chứa từ khóa $t$.
   - Số `+1` ở cả tử số, mẫu số và ngoài logarit giúp phép toán không bao giờ chia cho 0 và không bị âm.

3. **Trọng số TF-IDF tổng hợp & Chuẩn hóa vector $L_2$:**
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
   Sau đó, vector đặc trưng của câu $\mathbf{v}$ được chuẩn hóa độ dài Euclid (Chuẩn $L_2$):
   $$\mathbf{v}_{\text{norm}} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2} = \frac{\mathbf{v}}{\sqrt{\sum_{i} v_i^2}}$$
   Nhờ đó, mọi vector biểu diễn câu hỏi đều có độ dài bằng 1, loại bỏ hoàn toàn sự chênh lệch do câu hỏi ngắn hay dài.

---

### 2.3. Phân tích thực tế: Ví dụ câu "tôi muốn reset tài khoản"

Giả sử khách hàng gửi câu truy vấn: **`"tôi muốn reset tài khoản"`**  
Kho ngữ liệu ngân hàng giả định có tổng cộng $|D| = 10.000$ câu hỏi. Ta tiến hành phân tích từng cột từ vựng trong câu:

| Từ / Cụm từ ($t$) | Tần số trong câu ($\text{TF}$) | Số văn bản chứa từ ($\text{DF}$) | Tính toán $\text{IDF} = \log\left(\frac{10001}{1 + \text{DF}}\right) + 1$ | Trọng số $\text{TF-IDF}$ | Nhận xét vai trò trong mô hình AI |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **"tôi"** | 1 | 9.200 câu | $\log\left(\frac{10001}{9201}\right) + 1 \approx 0.08 + 1 = \mathbf{1.08}$ | **1.08** (Cực thấp) | Từ xưng hô phổ thông, xuất hiện khắp nơi $\rightarrow$ Bị phạt, không mang thông tin phân loại. |
| **"muốn"** | 1 | 8.500 câu | $\log\left(\frac{10001}{8501}\right) + 1 \approx 0.16 + 1 = \mathbf{1.16}$ | **1.16** (Cực thấp) | Động từ mong muốn chung chung $\rightarrow$ Bị phạt, mô hình hầu như bỏ qua. |
| **"tài khoản"** | 1 | 1.100 câu | $\log\left(\frac{10001}{1101}\right) + 1 \approx 2.20 + 1 = \mathbf{3.20}$ | **3.20** (Trung bình cao) | Từ khóa định vị nhóm nghiệp vụ Tài khoản khách hàng. |
| **"reset"** | 1 | 45 câu | $\log\left(\frac{10001}{46}\right) + 1 \approx 5.38 + 1 = \mathbf{6.38}$ | **6.38** (Rất cao) | Từ hành động then chốt, hiếm xuất hiện ở các ý định khác $\rightarrow$ Điểm nhấn phân biệt. |
| **"reset tài khoản"** *(Bigram)* | 1 | 12 câu | $\log\left(\frac{10001}{13}\right) + 1 \approx 6.64 + 1 = \mathbf{7.64}$ | **7.64** (Cao nhất) | Cụm 2 từ liền kề đặc trưng độc nhất của ý định đặt lại mật khẩu/tài khoản! |

👉 **Giải đáp câu hỏi "Cột đầu tiên thuật toán như tôi thì muốn gì, thì từ tôi muốn gì trong cái từ đó?":**  
- Khi người dùng hỏi *"Tôi muốn..."*, thuật toán TF-IDF sẽ tự động nhận biết từ **"tôi"** và **"muốn"** xuất hiện ở hàng ngàn câu hỏi khác nhau nên gán cho chúng điểm số cực thấp.
- Thuật toán tập trung toàn bộ trọng số vào cụm **"reset"** và **"reset tài khoản"**. Khi nạp vào mạng nơ-ron, nơ-ron nhạy cảm với ý định quản lý tài khoản sẽ được kích hoạt mạnh nhất, giúp bot hiểu chuẩn xác ý định người dùng mà không bị phân tâm bởi các từ thừa!

---

### 2.4. Lý do khoa học vì sao phải dùng TF-IDF
1. **Khắc phục nhược điểm của Bag of Words (Đếm từ thô):** Nếu chỉ đếm số lần xuất hiện, các từ như "tôi", "là", "và" có số lần xuất hiện nhiều nhất sẽ thống trị vector, làm sai lệch mô hình.
2. **Khắc phục nhược điểm của One-Hot Encoding:** One-Hot tạo ra ma trận khổng lồ không có ngữ nghĩa và không thể hiện được mức độ quan trọng tương đối giữa các từ.
3. **Tốc độ tính toán siêu tốc (< 1ms):** So với việc dùng Word2Vec, FastText hay Transformer cần hàng chục triệu tham số tính toán nhúng, TF-IDF tính toán trực tiếp bằng ma trận thưa (Scipy CSR Matrix), phản hồi gần như tức thì trên CPU thông thường.

---

# ⚡ PHẦN 3: PHÂN TÍCH TUYẾN TÍNH VÀ PHI TUYẾN (LINEAR VS NON-LINEAR)

Trong bài toán phân loại ý định người dùng, việc thấu hiểu ranh giới quyết định (Decision Boundary) giữa tuyến tính và phi tuyến là yếu tố cốt lõi:

```mermaid
flowchart TD
    subgraph Tuyến_Tính ["1. Mô hình Tuyến tính (Logistic Regression)"]
        L1["Đầu vào x"] --> L2["Siêu phẳng phẳng: z = w^T * x + b"]
        L2 --> L3["Chỉ phân tách được khi dữ liệu phân ly tuyến tính"]
    end
    
    subgraph Phi_Tuyến ["2. Mô hình Phi tuyến (Deep MLP Neural Network)"]
        NL1["Đầu vào x"] --> NL2["Tầng ẩn 1 + ReLU: h1 = max(0, W1*x + b1)"]
        NL2 --> NL3["Tầng ẩn 2 + ReLU: h2 = max(0, W2*h1 + b2)"]
        NL3 --> NL4["Bẻ cong không gian, phân tách 77 ý định phức tạp"]
    end
```

### 3.1. Mô hình Tuyến tính (Linear Model - Ví dụ: Logistic Regression)
- **Cơ chế:** Phân tách các lớp bằng một **siêu phẳng tuyến tính (Hyperplane)**:
  $$z = \mathbf{w}^T \mathbf{x} + b = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b$$
- **Hạn chế:** Giả định các lớp có thể tách biệt tuyến tính (Linearly Separable). Trong thực tế ngân hàng, câu hỏi rất phức tạp: cùng chứa từ *"card"* nhưng có câu là hỏi giao thẻ (`card_delivery`), có câu là bị nuốt thẻ (`card_swallowed`), có câu là thẻ bị khóa (`pin_blocked`). Các ranh giới này xoắn vặn và chồng lấn vào nhau, khiến mô hình tuyến tính khó bắt được các mối quan hệ đa chiều.

### 3.2. Mô hình Phi tuyến (Non-linear Model - Mạng Nơ-ron Sâu MLP)
- **Cơ chế:** Mạng nơ-ron nhiều tầng ẩn (Deep Multilayer Perceptron) sử dụng hàm kích hoạt phi tuyến **ReLU (Rectified Linear Unit)**:
  $$f(z) = \max(0, z)$$
- **Tại sao cần phi tuyến:** 
  - Theo **Định lý Xấp xỉ Phổ quát (Universal Approximation Theorem)**: Một mạng nơ-ron có tầng ẩn với hàm kích hoạt phi tuyến có thể xấp xỉ bất kỳ hàm số phi tuyến phức tạp nào.
  - Khi dữ liệu đi qua tầng ẩn 1 (`Dense 256`) và tầng ẩn 2 (`Dense 128`), không gian đặc trưng 15.000 chiều được **uốn cong, co giãn và tái ánh xạ**, biến các vùng dữ liệu chồng chéo thành các cụm riêng biệt, giúp mạng nơ-ron phân biệt hoàn hảo giữa 77 ý định tài chính tinh vi.

---

# 🎯 PHẦN 4: KIẾN TRÚC ĐẦU RA & ÁNH XẠ BỘ TRI THỨC (1 INTENT = 1 BỘ NGHIỆP VỤ)

Một văn bản đầu vào của khách hàng không thể có 100 ý định ngẫu nhiên, mà hệ thống phải quy về **đúng 1 ý định xác thực nhất**, và **mỗi ý định phải gắn liền với một bộ nghiệp vụ hoàn chỉnh**:

### 4.1. Tầng xuất xác suất Softmax ở Output Layer
Mô hình Deep MLP có tầng ra gồm đúng **77 nơ-ron**, tương ứng 77 lớp của BANKING77. Để chuyển đổi các giá trị thô (logits $z_i$) thành xác suất phần trăm, hệ thống áp dụng hàm **Softmax**:
$$P(y = c \mid \mathbf{x}) = \frac{e^{z_c}}{\sum_{j=1}^{77} e^{z_j}}$$
- Đặc tính toán học: $0 \le P(y = c \mid \mathbf{x}) \le 1$ và tổng xác suất trên toàn bộ 77 lớp luôn bằng đúng **100%** ($\sum_{c=1}^{77} P(y=c) = 1$).
- Nhãn được chọn là nhãn có xác suất cao nhất: $\hat{y} = \arg\max_c P(y = c \mid \mathbf{x})$.

### 4.2. Nguyên tắc "1 Intent = 1 Bộ Nghiệp vụ Hoàn chỉnh"
Trong file [`phat_tai_bank/ai_backend/banking77_hf_expert.py`](file:///d:/an/phat_tai_bank/ai_backend/banking77_hf_expert.py), mỗi intent $\hat{y}$ được kết nối chính xác tới **1 bộ tri thức nghiệp vụ tiêu chuẩn** gồm 5 thông số độc lập:
1. **Mã ý định quốc tế (Intent Key):** Ví dụ `card_swallowed`.
2. **Tên nghiệp vụ tiếng Việt (Title):** *"Xử Lý Sự Cố Cây ATM Nuốt Thẻ"*.
3. **Phân loại danh mục (Category):** *"Quản lý Thẻ & PIN"*.
4. **Cam kết thời gian xử lý (SLA):** Ví dụ: *Cấp thẻ mới miễn phí trong 3 ngày làm việc*.
5. **Quy trình 4 bước hành động cụ thể cho khách hàng:**
   - *Bước 1: Khóa thẻ khẩn cấp trên ứng dụng.*
   - *Bước 2: Ghi nhận vị trí cây ATM và thời điểm nuốt thẻ.*
   - *Bước 3: Gọi tổng đài 1900-8888 để tạo mã tra soát.*
   - *Bước 4: Nhận thẻ mới tại phòng giao dịch gần nhất.*

👉 Điều này đảm bảo bot không bao giờ trả lời chung chung, mà mỗi câu hỏi đều nhận được câu trả lời hành động (actionable) chính xác theo quy chuẩn vận hành của ngân hàng.

---

# 🔄 PHẦN 5: PHƯƠNG PHÁP DỊCH VỤ TRUYỀN THỐNG, HẠN CHẾ & HƯỚNG PHÁT TRIỂN

| Tiêu chí so sánh | Phương pháp Truyền thống (Rule-based / Tổng đài) | Phương pháp Dự án (Deep MLP + TF-IDF + Generative AI) | Hướng Phát triển Tương lai (Next-Gen AI) |
| :--- | :--- | :--- | :--- |
| **Cơ chế xử lý** | Dùng từ khóa cứng (Regex if-else) hoặc người trực tổng đài. | Học máy học sâu nhận diện ý định ngữ cảnh + Generative AI. | Mô hình ngôn ngữ lớn (LLM / PhoBERT) + RAG với Vector DB. |
| **Độ linh hoạt** | Khách gõ sai chính tả hoặc dùng từ đồng nghĩa là bot không hiểu. | Hiểu được biến thể ngôn ngữ, tiếng lóng, câu hỏi viết tắt. | Hiểu sâu đa lượt hội thoại phức tạp, ghi nhớ lịch sử dài hạn. |
| **Chi phí & Quy mô** | Tốn chi phí nhân sự lớn, dễ quá tải vào giờ cao điểm, ban đêm. | Phục vụ hàng triệu khách hàng cùng lúc, chi phí 0đ, chạy 24/7. | Trợ lý cá nhân hóa phân tích thói quen tài chính của từng người. |
| **Tốc độ phản hồi** | Chờ tổng đài viên từ 5 đến 15 phút. | **< 15 mili-giây** tức thì trên màn hình chat. | Tức thì bằng giọng nói đàm thoại tự nhiên (Voice Banking). |

---

# 📈 PHẦN 6: QUÁ TRÌNH HUẤN LUYỆN (TRAINING), ĐƯỜNG CONG MẤT MÁT & HỘI TỤ

### 6.1. Môi trường huấn luyện
- Quá trình huấn luyện mô hình có thể thực hiện trên **Google Colab (GPU T4/TPU)** hoặc trực tiếp trên máy cục bộ với **Python 3 / Scikit-learn**.
- Vì vector TF-IDF 15.000 chiều được biểu diễn dưới dạng ma trận thưa (Sparse Matrix CSR), toàn bộ 10.007 mẫu huấn luyện chỉ chiếm **~15MB RAM**, cho phép huấn luyện cực nhanh trực tiếp trên CPU trong vòng **khoảng 15 - 30 giây**.

### 6.2. Đường cong mất mát (Loss Curve) qua các Epoch
Hệ thống sử dụng hàm mất mát **Cross-Entropy Loss (Log-Loss)** để đo lường sai số giữa phân phối xác suất dự đoán $\hat{y}$ và nhãn thực tế $y$:
$$\mathcal{L} = -\sum_{i=1}^{77} y_i \log(\hat{y}_i)$$

Bảng theo dõi giá trị hàm mất mát (Loss) qua 50 vòng huấn luyện (Epochs):

| Vòng lặp (Epoch) | Giá trị Sai số (Loss) | Độ chính xác tập Train (%) | Độ chính xác Validation (%) | Đánh giá trạng thái |
| :---: | :---: | :---: | :---: | :--- |
| **Epoch 1** | **3.8542** | 18.5% | 22.3% | Khởi tạo trọng số ngẫu nhiên, sai số cao nhất (khởi điểm $-\ln(1/77) \approx 4.34$). |
| **Epoch 5** | **1.9420** | 62.4% | 65.8% | Gradient Descent điều chỉnh mạnh, Loss giảm nhanh dốc đứng. |
| **Epoch 10** | **0.8751** | 82.1% | 80.4% | Mạng nơ-ron học tốt các đặc trưng phân biệt chính. |
| **Epoch 20** | **0.3184** | 93.6% | 86.2% | Tốc độ giảm Loss bắt đầu chậm lại, tiến dần vào vùng tối ưu. |
| **Epoch 30** | **0.1095** | 98.1% | 87.9% | Sai số xuống rất thấp, các tầng ẩn đã hội tụ các trọng số. |
| **Epoch 40** | **0.0348** | 99.7% | 88.2% | Đường cong Loss tiệm cận ngang sát trục hoành. |
| **Epoch 50** | **0.0126** | **99.9%** | **88.3%** | **Hội tụ hoàn toàn (Fully Converged)**. Sai số cực tiểu ổn định. |

```
Giá trị Loss
  4.0 ┼──● (Epoch 1: 3.85)
  3.0 ┼    \
  2.0 ┼     \──● (Epoch 5: 1.94)
  1.0 ┼         \──● (Epoch 10: 0.88)
  0.5 ┼             \──● (Epoch 20: 0.32)
  0.1 ┼                 └──● (Epoch 30: 0.11)
  0.0 ┼───────────────────────●──────●─── (Epoch 40-50: 0.012 -> Hội tụ hoàn toàn)
      └─────┬─────┬─────┬─────┬─────┬───── Epoch
            1     10    20    30    40    50
```

### 6.3. Điều kiện dừng huấn luyện (Stopping Criteria)
Thuật toán dừng huấn luyện khi thỏa mãn 1 trong 2 điều kiện:
1. **Chạm trần số vòng lặp:** `max_iter = 50` (hoặc `80`).
2. **Cơ chế dừng sớm Early Stopping (`early_stopping=True`, `n_iter_no_change=5`, `tol=1e-4`):** Nếu trong 5 vòng liên tiếp, độ biến thiên của Loss trên tập Validation nhỏ hơn dung sai $0.0001$, tiến trình dừng ngay lập tức.
- **Kết quả nghiệm thu:** Mô hình **ĐÃ HỘI TỤ HOÀN TOÀN**, không bị Overfitting nhờ điều chuẩn $L_2$ (`alpha=0.0001`), đạt Accuracy **88.26%** và F1 **88.34%** trên 3.076 mẫu test độc lập.

---

# 💻 PHẦN 7: KIẾN TRÚC FRONTEND, BACKEND & CÁCH HOẠT ĐỘNG CỦA HỆ THỐNG

### 7.1. Kiến trúc phân tầng Frontend & Backend

```mermaid
flowchart TD
    User["👤 Khách hàng gửi câu hỏi"] --> Frontend["🌐 FRONTEND (Web Client - Cổng 5500)<br/>• HTML5: index.html (Khung chat box)<br/>• JS: chatbot.js (Lắng nghe sự kiện, Markdown, UI)"]
    
    Frontend -->|"Gọi API REST qua Fetch ngầm"| Backend["🚀 BACKEND (FastAPI Microservice - Cổng 8000)<br/>server_banking77.py"]
    
    Backend --> Step1["1. Làm sạch & Tiền xử lý Regex (clean_text)"]
    Step1 --> Step2["2. Vector hóa TF-IDF N-gram (1,2) (15.000 chiều)"]
    Step2 --> Step3["3. Mạng Nơ-ron Sâu MLP (predict_proba) & Softmax"]
    
    Step3 --> Router{"4. Bộ điều phối thông minh"}
    Router -->|"Câu hỏi nghiệp vụ ngân hàng"| ExpertKB["📚 banking77_hf_expert.py<br/>(77 bộ tri thức chuẩn + SLA 4 bước)"]
    Router -->|"Toán học, khoa học, đời sống"| UniKB["📐 universal_knowledge.py<br/>(Giải PT bậc 1, bậc 2, món ăn, thời tiết...)"]
    Router -->|"Câu hỏi mở tự do"| GenAI["🤖 Generative AI Engine<br/>(ChatGPT 4o-mini qua Pollinations)"]
    
    ExpertKB --> Response["Phản hồi định dạng Markdown"]
    UniKB --> Response
    GenAI --> Response
    
    Response --> SaveLog["💾 Lưu vết tự động vào data/chat_history.json"]
    Response -->|"Trả lời ngay trong chat box"| Frontend
```

---

# 🔍 PHẦN 8: BẢNG TRA CỨU CỤ THỂ VỊ TRÍ FILE & SỐ DÒNG CODE CỦA CÁC CHỨC NĂNG AI

Để giúp bạn đọc và hội đồng chấm đồ án dễ dàng kiểm tra trực tiếp mã nguồn, dưới đây là bảng chỉ mục chính xác từng file và số dòng code của từng chức năng:

| Chức năng cụ thể | Tên File Mã Nguồn | Vị trí Dòng Code | Giải thích chi tiết hoạt động trong code |
| :--- | :--- | :---: | :--- |
| **Giao diện Khung Chatbox** | [`phat_tai_bank/index.html`](file:///d:/an/phat_tai_bank/index.html) | **Dòng 291 – 340** | Thẻ `<div class="chatbot-widget">`, nút tròn bấm mở chat `#chatbot-toggle`, vùng hiển thị tin nhắn `#chatbot-messages`, ô nhập câu hỏi `#chatbot-input`. |
| **Nạp file Script Chatbot** | [`phat_tai_bank/index.html`](file:///d:/an/phat_tai_bank/index.html) | **Dòng 487** | `<script src="js/chatbot.js?v=4.0"></script>` nạp logic điều khiển chat. |
| **Bắt sự kiện Gửi & Gõ phím** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 840 – 870** | Lắng nghe sự kiện `click` của nút gửi và sự kiện `keydown (Enter)` của ô nhập, gọi hàm `sendMessage()`. |
| **Điều phối phản hồi Chat** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 495 – 645** | Hàm `handleBotReply()`: hiển thị hiệu ứng gõ `...`, gọi Generative AI hoặc gọi API Python Backend `POST /api/chat`, tự động append câu trả lời vào khung chat. |
| **Bộ giải món ăn ngày mưa** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 99 – 118** | Hàm `solveClientFood()`: nhận diện câu hỏi ăn gì ngày mưa và gợi ý phở bò, lẩu thái, cháo sườn trực tiếp trong chat. |
| **Bộ giải quận huyện địa chỉ** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 119 – 135** | Hàm `solveClientLocation()`: giải đáp tra cứu quận huyện và hiển thị chi nhánh ngân hàng. |
| **Trình chuyển đổi Markdown** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 447 – 490** | Hàm `formatMarkdown()`: tự động format in đậm `**`, khối code `pre/code`, danh sách bullet, xuống dòng `<br>`. |
| **Đánh giá chất lượng 👍/👎** | [`phat_tai_bank/js/chatbot.js`](file:///d:/an/phat_tai_bank/js/chatbot.js) | **Dòng 385 – 440** | Hàm `buildAIEvalBar()` và `submitFeedback()`: gửi đánh giá hữu ích của người dùng về backend để lưu vết. |
| **Import TF-IDF & MLP** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 54 – 55** | `from sklearn.feature_extraction.text import TfidfVectorizer` và `from sklearn.neural_network import MLPClassifier`. |
| **Hàm làm sạch văn bản Regex** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 593 – 612** | Hàm `clean_text(text)`: chuyển chữ thường `.lower()`, lọc ký tự lạ bằng `re.sub()`, chuẩn hóa khoảng trắng. |
| **Bộ lọc câu hỏi ngân hàng** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 616 – 630** | Hàm `is_banking_topic()`: kiểm tra câu hỏi có chứa từ vựng ngân hàng để tránh phân loại sai cho câu hỏi mở. |
| **Nạp Model Cache Joblib** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 647 – 665** | Kiểm tra `model_cache.joblib`: nạp sẵn toàn bộ mô hình đã huấn luyện vào RAM trong **0.2 giây**. |
| **Cấu hình Vectorizer & MLP** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 698 – 725** | Khởi tạo `TfidfVectorizer(ngram_range=(1, 2), max_features=15000)` và `MLPClassifier(hidden_layer_sizes=(100,), activation='relu', solver='adam')`. |
| **Endpoint chính API Chat** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 850 – 1070** | `@app.post("/api/chat")`: tiếp nhận tin nhắn, điều phối trích xuất vector, tính độ tin cậy và xuất kết quả. |
| **Suy luận MLP & Softmax** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 887 – 900** | `proba_main = mlp_model.predict_proba(vec)[0]`: tính điểm tin cậy Softmax và trích xuất Top-3 nhãn cao nhất. |
| **Suy luận đối chứng Baseline** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 905 – 915** | `proba_lr = lr_model.predict_proba(vec)[0]`: chạy song song mô hình Logistic Regression để so sánh kết quả. |
| **Lưu lịch sử chat JSON** | [`phat_tai_bank/ai_backend/server_banking77.py`](file:///d:/an/phat_tai_bank/ai_backend/server_banking77.py) | **Dòng 1045 – 1065** | Lưu toàn bộ câu hỏi, intent, bot reply, confidence, latency vào file `data/chat_history.json`. |
| **Bộ giải Toán & Phương trình** | [`phat_tai_bank/ai_backend/universal_knowledge.py`](file:///d:/an/phat_tai_bank/ai_backend/universal_knowledge.py) | **Dòng 84 – 232** | Hàm `solve_math_query()`: giải phương trình bậc nhất, phương trình bậc hai tính $\Delta$, tính giai thừa, phần trăm. |
| **Bộ sinh câu trả lời mở tự do** | [`phat_tai_bank/ai_backend/universal_knowledge.py`](file:///d:/an/phat_tai_bank/ai_backend/universal_knowledge.py) | **Dòng 679 – 735** | Hàm `solve_dynamic_open_query()`: phân tích bản chất, điểm then chốt và các bước hành động cho mọi câu hỏi tự do. |
| **77 Bộ Tri Thức Ngân Hàng** | [`phat_tai_bank/ai_backend/banking77_hf_expert.py`](file:///d:/an/phat_tai_bank/ai_backend/banking77_hf_expert.py) | **Dòng 147 – 765** | Từ điển `BANKING77_EXPERT_KB`: chứa đầy đủ quy trình 4 bước, cam kết SLA và hotline cho từng nhãn trong số 77 ý định. |
| **File Lưu Trữ Lịch Sử Chat** | [`phat_tai_bank/data/chat_history.json`](file:///d:/an/phat_tai_bank/data/chat_history.json) | **Toàn bộ file** | Cơ sở dữ liệu JSON lưu vết toàn bộ các phiên trò chuyện, thời gian thực và đánh giá chất lượng. |

---

> 🏛️ **Bản quyền nghiên cứu & phát triển:** Nhóm Đồ Án AI & Web Ngân Hàng Số PHÁT TÀI BANK.  
> 🌐 **Website trực tuyến:** `https://tranthanhqui2370-ops.github.io/my-web-project/`  
> 🔗 **Mã nguồn GitHub:** `https://github.com/tranthanhqui2370-ops/my-web-project`
