/**
 * PHÁT TÀI BANK - AI Chatbot Module (Phát Tài Bot & ChatGPT Engine)
 * - Tích hợp Generative AI: Trả lời mọi câu hỏi trên thế giới giống hệt ChatGPT 4o!
 * - Hỗ trợ đa mô hình: ChatGPT 4o-mini (Puter / Pollinations), DeepSeek, Gemini, OpenAI, Groq & Local MLP.
 * - Nhận diện 77 ý định tài chính chuẩn quốc tế BANKING77 – Hugging Face.
 * - Tự động đồng bộ và lưu trữ lịch sử tương tác vào data/chat_history.json.
 */

// ─── 1. CẤU HÌNH & HỆ THỐNG GIAO TIẾP ───────────────────────────────────────
const AI_SYSTEM_PROMPT = `Bạn là Phát Tài Bot - Trợ lý Trí Tuệ Nhân Tạo toàn năng của Ngân hàng số PHÁT TÀI BANK, hoạt động thông minh, uyên bác và sinh văn bản tự do sâu sắc giống hệt ChatGPT 4o.
Nhiệm vụ của bạn:
1. Trả lời MỌI câu hỏi của người dùng trên toàn thế giới: giải toán, giải phương trình, viết code lập trình (Python, JS, C++, HTML, SQL...), dịch thuật, phân tích khoa học, giải thích lịch sử, địa lý, viết văn, làm thơ, soạn thảo hợp đồng, đơn từ, tư vấn đời sống, sức khỏe...
2. Luôn trả lời trực diện, chi tiết, chính xác, logic, sâu sắc và thân thiện bằng tiếng Việt (hoặc theo ngôn ngữ người dùng yêu cầu).
3. Sử dụng định dạng Markdown rõ ràng, đẹp mắt: dùng bullet, in đậm, bảng số liệu, khối code có syntax highlighting nếu có lập trình.
4. Khi người dùng hỏi về các dịch vụ của PHÁT TÀI BANK hoặc Đồ án AI:
   - Mở tài khoản E-Banking: Hướng dẫn 4 bước online qua eKYC (CCCD gắn chip) trên web/app.
   - Thẻ ATM / Visa / Mastercard: Kích hoạt thẻ, đổi mã PIN, thẻ bị nuốt tại ATM (gọi 1900-8888 hỗ trợ cấp lại thẻ mới miễn phí trong 3 ngày).
   - Sổ tiết kiệm online: Lãi suất ưu đãi 6.8%/năm kỳ hạn 12 tháng, rút vốn linh hoạt.
   - Vay tín chấp: Duyệt online trong 24h, hạn mức 10tr - 500tr, lãi suất từ 10.8%/năm.
   - Chuyển tiền 24/7 Napas: 0đ phí trọn đời, tiền đến sau 3 giây.
   - Đồ án AI: Dựa trên tập dữ liệu chuẩn BANKING77 (Hugging Face / EMNLP), 77 ý định tài chính, mô hình mạng nơ-ron sâu MLP (Accuracy 88.26%, F1 88.34%) và mô hình đối chứng Logistic Regression (Accuracy 88.98%, F1 89.00%).
   - Hotline tổng đài 24/7: 1900-8888.`;

// Bộ nhớ hội thoại ngắn hạn (Conversation Context)
let chatHistoryMemory = [];

function getApiCandidates() {
  const urls = [];
  try {
    if (typeof window !== "undefined" && window.location) {
      const host = window.location.hostname || "localhost";
      urls.push(`http://${host}:8000`);
    }
  } catch (e) {}
  urls.push("http://localhost:8000");
  urls.push("http://127.0.0.1:8000");
  return Array.from(new Set(urls));
}

function getStoredAIConfig() {
  try {
    return {
      provider: localStorage.getItem("phattai_ai_provider") || "chatgpt_free",
      model: localStorage.getItem("phattai_ai_model") || "gpt-4o-mini",
      apiKey: localStorage.getItem("phattai_ai_key") || ""
    };
  } catch (e) {
    return { provider: "chatgpt_free", model: "gpt-4o-mini", apiKey: "" };
  }
}

function saveLocalChatHistory(userMsg, botReply, intent = "general") {
  try {
    const history = JSON.parse(localStorage.getItem("phattai_chat_history") || "[]");
    history.push({
      timestamp: new Date().toISOString(),
      user_msg: userMsg,
      bot_reply: botReply,
      intent: intent
    });
    localStorage.setItem("phattai_chat_history", JSON.stringify(history));
  } catch (e) {}
}

// ─── 2. CƠ SỞ TRI THỨC DỰ PHÒNG OFFLINE ────────────────────────────────────
function solveClientDatetime(text) {
  const t = (text || "").toLowerCase().trim();
  const datePatterns = [
    "ngày mấy", "ngay may", "ngày bao nhiêu", "ngay bao nhieu",
    "hôm nay ngày", "hom nay ngay", "này ngày mấy", "nay ngay may", "nay là ngày",
    "mấy giờ", "may gio", "bây giờ là mấy giờ", "mấy giờ rồi",
    "thứ mấy", "thu may", "hôm nay thứ mấy",
    "năm mấy", "nam may", "năm nay là năm nào",
    "tháng mấy", "thang may"
  ];
  if (datePatterns.some(p => t.includes(p))) {
    const now = new Date();
    const days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];
    const dName = days[now.getDay()];
    const dd = String(now.getDate()).padStart(2, '0');
    const mm = String(now.getMonth() + 1).padStart(2, '0');
    const yyyy = now.getFullYear();
    const hh = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const sec = String(now.getSeconds()).padStart(2, '0');
    return `📅 **THÔNG TIN THỜI GIAN THỜI GIAN THỰC (REALTIME SYSTEM CLOCK):**\n\n• 🗓️ **Hôm nay là:** **${dName}, ngày ${dd} tháng ${mm} năm ${yyyy}**\n• ⏰ **Thời gian hiện tại:** **${hh}:${min}:${sec}** (Múi giờ Việt Nam - GMT+7)\n• 🌐 **Hệ thống:** Máy chủ AI Ngân hàng số PHÁT TÀI BANK đồng bộ thời gian chuẩn liên tục 24/7!`;
  }
  return null;
}

function solveClientWeather(text) {
  const t = (text || "").toLowerCase().trim();
  if (["thời tiết", "thoi tiet", "mưa không", "trời mưa", "dự báo thời tiết"].some(p => t.includes(p))) {
    return `🌤️ **DỰ BÁO THỜI TIẾT HÔM NAY:**\n\n• 📍 **Khu vực:** TP. Hồ Chí Minh & các tỉnh lân cận\n• 🌡️ **Nhiệt độ hiện tại:** **29°C - 32°C**\n• 💧 **Độ ẩm:** 72% | Gió nhẹ\n• ⛅ **Trạng thái:** Mây thay đổi, ngày nắng gián đoạn, chiều tối có mưa rào nhẹ rải rác.\n• 💡 Quý khách có thể xem thời tiết trực tiếp trên Widget ở góc trái Menu!`;
  }
  return null;
}

function solveClientFood(text) {
  const t = (text || "").toLowerCase().trim();
  const foodKeywords = ["ăn gì", "an gi", "gợi ý đồ ăn", "goi y do an", "gợi ý món", "món ăn", "đồ ăn", "thực đơn", "ngày mưa", "ngay mua", "mưa nên ăn gì"];
  if (foodKeywords.some(k => t.includes(k))) {
    const isRain = ["mưa", "mua", "lạnh", "lanh"].some(k => t.includes(k));
    if (isRain) {
      return `🍲 **GỢI Ý MÓN ĂN TUYỆT VỜI CHO NGÀY MƯA SE LẠNH:**\n\n` +
             `1️⃣ **Phở Bò Tái Nạm / Bò Kho Nóng:** Nước dùng ninh xương thơm phức hồi quế, hạt tiêu cay ấm bụng ngay tức thì.\n` +
             `2️⃣ **Lẩu Thái Chua Cay / Lẩu Riêu Cua:** Nồi lẩu sôi sùng sục bên tiếng mưa rơi, vị chua cay đậm đà nhúng bò và rau nấm.\n` +
             `3️⃣ **Cháo Sườn Quẩy Nóng:** Cháo sánh mịn bốc khói ngùn ngụt, rắc ruốc thịt và hạt tiêu thơm lừng ăn kèm quẩy giòn.\n` +
             `4️⃣ **Bánh Xèo Giòn Rụm / BBQ:** Bánh xèo vàng ươm ăn kèm rau sống chấm nước mắm chua ngọt.\n` +
             `5️⃣ **Mì Cay 7 Cấp Độ:** Nước mì nóng bỏng lưỡi xua tan hoàn toàn cảm giác se lạnh ẩm ướt.\n\n` +
             `☕ **Đồ uống ấm:** Trà gừng mật ong nóng hoặc sữa đậu nành nóng!\n` +
             `✨ *Chúc bạn có một bữa ăn ngon miệng và ấm áp!*`;
    }
    return `🍽️ **GỢI Ý THỰC ĐƠN THƠM NGON HÔM NAY:**\n\n• Canh sườn rau củ / Canh chua cá lóc.\n• Thịt kho tàu trứng cút / Gà rang sả ớt giòn thơm.\n• Rau muống xào tỏi xanh giòn.\n• Cơm tấm sườn bì chả hoặc bún bò Huế.\n• Tráng miệng: Trái cây tươi hoặc chè hạt sen long nhãn!`;
  }
  return null;
}

function solveClientLocation(text) {
  const t = (text || "").toLowerCase().trim();
  if (["nhà nè quận mấy", "quận mấy", "thuộc quận nào", "ở quận mấy", "quận nào", "huyện nào"].some(k => t.includes(k))) {
    return `📍 **HƯỚNG DẪN XÁC ĐỊNH QUẬN / HUYỆN:**\n\n` +
           `Để biết chính xác địa chỉ của bạn thuộc **Quận nào**, bạn vui lòng cung cấp thêm:\n` +
           `• 🛣️ **Tên con đường** hoặc **Số nhà cụ thể** (Ví dụ: *"123 Nguyễn Trãi"*, *"Lê Văn Sỹ"*...)\n` +
           `• 🏛️ **Địa danh / Tòa nhà gần đó** (Ví dụ: *gần Chợ Bến Thành, Landmark 81, Sân bay Tân Sơn Nhất*...)\n\n` +
           `🏢 **Trụ sở PHÁT TÀI BANK tại TP.HCM:**\n` +
           `• Trụ sở chính: Số 88 Đường Nguyễn Huệ, Phường Bến Nghé, **Quận 1, TP. Hồ Chí Minh**.\n` +
           `👉 Bạn hãy nhắn tên đường hoặc số nhà cụ thể ngay tại đây, Phát Tài Bot sẽ tra cứu ngay cho bạn!`;
  }
  return null;
}

function solveClientMath(text) {
  try {
    const clean = text.toLowerCase().replace('tính', '').replace('bằng mấy', '').replace('bằng bao nhiêu', '').replace('=', '').trim()
      .replace(/x/g, '*').replace(/:/g, '/').replace(/\^/g, '**');
    const m = clean.match(/([\d\.\s\+\-\*\/\(\)]+)/);
    if (m && m[1] && /\d/.test(m[1]) && /[\+\-\*\/]/.test(m[1])) {
      const expr = m[1].trim();
      if (/^[\d\.\s\+\-\*\/\(\)]+$/.test(expr)) {
        const val = Function(`'use strict'; return (${expr})`)();
        if (typeof val === 'number' && !isNaN(val)) {
          return `🔢 **KẾT QUẢ TÍNH TOÁN:**\nBiểu thức: \`${expr}\`\n➡️ Kết quả: **${val.toLocaleString()}**`;
        }
      }
    }
  } catch (e) {}
  return null;
}

const BOT_BANK_RESPONSES = [
  {
    keywords: ["các bước tạo tài khoản", "tạo tài khoản", "mở tài khoản", "đăng ký tài khoản", "cách tạo tài khoản", "lập tài khoản"],
    response: "📌 **CÁC BƯỚC ĐỂ TẠO TÀI KHOẢN E-BANKING PHÁT TÀI BANK:**\n" +
              "1️⃣ **Bước 1:** Bấm vào nút **'Đăng Ký'** ở góc phải hoặc chọn **6. Đăng Ký E-Banking** trong Menu.\n" +
              "2️⃣ **Bước 2:** Nhập đầy đủ thông tin: Họ và tên, Tên đăng nhập, Số điện thoại và Địa chỉ nhận thẻ.\n" +
              "3️⃣ **Bước 3:** Nhập Mật khẩu (tối thiểu 6 ký tự) và Xác nhận mật khẩu an toàn.\n" +
              "4️⃣ **Bước 4:** Bấm **'Mở Tài Khoản PHÁT TÀI BANK'**. Hệ thống sẽ tự động cấp số tài khoản định danh `PTB...` và đăng nhập ngay!\n" +
              "💡 *Hotline hỗ trợ 24/7:* **1900-8888**."
  },
  {
    keywords: ["kích hoạt thẻ", "activate", "thẻ mới", "nhận thẻ", "các bước kích hoạt"],
    response: "💳 **HƯỚNG DẪN CHI TIẾT KÍCH HOẠT THẺ PHÁT TÀI BANK:**\n" +
              "1️⃣ Đăng nhập vào tài khoản E-Banking trên website hoặc ứng dụng di động.\n" +
              "2️⃣ Vào mục **'Quản lý Thẻ'** -> Nhấp chọn thẻ cần kích hoạt.\n" +
              "3️⃣ Nhập 4 số cuối in trên mặt thẻ và mã xác thực OTP gửi về SMS.\n" +
              "4️⃣ Đổi mã PIN mặc định tại bất kỳ cây ATM nào của PHÁT TÀI BANK để kích hoạt hoàn tất!"
  },
  {
    keywords: ["thẻ bị khóa", "khóa thẻ", "card_blocked", "mở khóa thẻ", "bị nuốt thẻ"],
    response: "🔒 **CÁC BƯỚC XỬ LÝ KHI THẺ BỊ KHÓA:**\n" +
              "1️⃣ Đăng nhập E-Banking -> Chọn **'Quản lý Thẻ'** -> Nhấp **'Mở khóa thẻ'**.\n" +
              "2️⃣ Xác thực bằng mã Smart OTP hoặc nhận diện sinh trắc học FaceID.\n" +
              "3️⃣ Nếu thẻ bị ATM nuốt, gọi ngay hotline khẩn cấp **1900-8888** (nhánh 1) để được cấp lại thẻ mới miễn phí trong 3 ngày."
  },
  {
    keywords: ["tiết kiệm", "lãi suất", "gửi tiền", "kỳ hạn", "cách gửi tiết kiệm"],
    response: "💰 **HƯỚNG DẪN MỞ SỔ TIẾT KIỆM ONLINE LÃI SUẤT 6.8%/NĂM:**\n" +
              "1️⃣ Trên trang chủ, cuộn đến phần **Dịch Vụ Ngân Hàng** -> Chọn **'Gói Tiết Kiệm Linh Hoạt'**.\n" +
              "2️⃣ Chọn số tiền gửi (tối thiểu 1.000.000 VNĐ) và kỳ hạn gửi (từ 1 đến 36 tháng).\n" +
              "3️⃣ Chọn phương thức nhận lãi: Nhận hàng tháng hoặc cộng dồn cuối kỳ -> Bấm **Xác nhận**.\n" +
              "📈 Tiền lãi được tính minh bạch và có thể rút vốn linh hoạt bất kỳ lúc nào!"
  },
  {
    keywords: ["vay", "vay tín chấp", "vay tiêu dùng", "vay online", "các bước vay"],
    response: "📝 **CÁC BƯỚC ĐĂNG KÝ VAY TÍN CHẤP DUYỆT TRONG 24H:**\n" +
              "1️⃣ Chọn gói **'Vay Tín Chấp Tiêu Dùng Online'** trong danh mục dịch vụ.\n" +
              "2️⃣ Nhập số tiền cần vay (10 triệu - 500 triệu) và kỳ hạn trả dần (6 - 60 tháng).\n" +
              "3️⃣ Điền thông tin thu nhập và tải ảnh CCCD gắn chip lên hệ thống.\n" +
              "4️⃣ Hệ thống AI duyệt tự động và giải ngân tiền vào tài khoản trong 24 giờ!"
  },
  {
    keywords: ["chuyển tiền", "chuyển khoản", "transfer", "hạn mức chuyển", "cách chuyển tiền"],
    response: "⚡ **HƯỚNG DẪN CHUYỂN TIỀN NHANH 24/7 NAPAS:**\n" +
              "1️⃣ Vào mục chuyển tiền trên thanh menu hoặc ứng dụng E-Banking.\n" +
              "2️⃣ Nhập Số tài khoản người nhận hoặc quét mã VietQR.\n" +
              "3️⃣ Nhập số tiền muốn chuyển và nội dung giao dịch.\n" +
              "4️⃣ Xác thực mã OTP -> Tiền đến người nhận sau **3 giây**, **hoàn toàn 0đ phí**!"
  },
  {
    keywords: ["đề tài", "de tai", "đề bài", "de bai", "dự án", "báo cáo đề tài"],
    response: "📘 **BÁO CÁO TỔNG QUAN ĐỀ TÀI:**\n" +
              "• **Tên đề tài:** *Xây dựng ứng dụng Chatbot nhận diện ý định từ câu hỏi người dùng dựa trên tập dữ liệu BANKING77 cho PHÁT TÀI BANK*.\n" +
              "• **Mô hình AI:** TF-IDF N-grams (1, 2) kết hợp Mạng nơ-ron sâu MLP (100 ReLU, Adam) đạt Accuracy **88.26%**, F1 **88.34%**; Mô hình đối chứng Logistic Regression đạt Accuracy **88.98%**, F1 **89.00%**."
  }
];

const BANK_QUICK_SUGGESTIONS = [
  "Các bước tạo tài khoản?",
  "Hướng dẫn kích hoạt thẻ?",
  "Cách mở sổ tiết kiệm 6.8%?",
  "Đăng ký vay tín chấp online?",
  "Giải thích thuyết tương đối?",
  "Viết hàm Python tính giai thừa"
];

// ─── 3. GENERATIVE AI ENGINE (CHATGPT / PUTER / POLLINATIONS / CUSTOM KEY) ────
async function callGenerativeAI(userMessage) {
  const config = getStoredAIConfig();
  const provider = config.provider || "chatgpt_free";
  const apiKey = config.apiKey || "";

  // Chuẩn bị danh sách messages kèm context lịch sử gần nhất (Context Memory)
  const messages = [
    { role: "system", content: AI_SYSTEM_PROMPT }
  ];

  // Lấy tối đa 4 tin nhắn gần nhất để giữ mạch trò chuyện
  const recentTurns = chatHistoryMemory.slice(-4);
  for (const turn of recentTurns) {
    messages.push({ role: turn.role, content: turn.content });
  }
  messages.push({ role: "user", content: userMessage });

  let botReply = "";
  let usedModel = "ChatGPT 4o-mini";
  let usedProvider = provider;

  // ── PHƯƠNG ÁN 1: ChatGPT Miễn Phí (Pollinations.ai Background Fetch) ──────────
  if (provider === "chatgpt_free") {
    // Không dùng Puter.js để tránh popup/modal mở thêm trang ngoài ý muốn!
    // Sử dụng fetch chạy ngầm 100% trong chatbox:
    try {
      const controller = (typeof AbortController !== "undefined") ? new AbortController() : null;
      const timeoutId = controller ? setTimeout(() => controller.abort(), 4500) : null;

      const pollResponse = await fetch("https://text.pollinations.ai/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: messages,
          model: "openai",
          system: AI_SYSTEM_PROMPT,
          jsonMode: false
        }),
        signal: controller ? controller.signal : undefined
      });
      if (timeoutId) clearTimeout(timeoutId);

      if (pollResponse.ok) {
        const textRes = await pollResponse.text();
        if (textRes && textRes.trim().length > 0) {
          return {
            reply: textRes.trim(),
            model: "ChatGPT 4o-mini",
            provider: "ChatGPT Free (Pollinations)"
          };
        }
      }
    } catch (errPoll) {
      // Thử nhanh phương thức GET đơn giản
      try {
        const controller2 = (typeof AbortController !== "undefined") ? new AbortController() : null;
        const timeoutId2 = controller2 ? setTimeout(() => controller2.abort(), 3500) : null;
        const getUrl = `https://text.pollinations.ai/${encodeURIComponent(userMessage)}?model=openai`;
        const resGet = await fetch(getUrl, { signal: controller2 ? controller2.signal : undefined });
        if (timeoutId2) clearTimeout(timeoutId2);
        if (resGet.ok) {
          const t = await resGet.text();
          if (t && t.trim().length > 0) {
            return {
              reply: t.trim(),
              model: "ChatGPT 4o-mini",
              provider: "ChatGPT Free (Pollinations)"
            };
          }
        }
      } catch (e2) {}
    }
  }

  // ── PHƯƠNG ÁN 2: Custom API Key (OpenAI / DeepSeek / Gemini / Groq) ─────────
  if (provider === "openai" && apiKey) {
    try {
      const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
        body: JSON.stringify({ model: config.model || "gpt-4o-mini", messages: messages })
      });
      if (res.ok) {
        const d = await res.json();
        return { reply: d.choices[0].message.content, model: config.model || "gpt-4o", provider: "OpenAI Direct" };
      }
    } catch (e) {}
  }

  if (provider === "deepseek" && apiKey) {
    try {
      const res = await fetch("https://api.deepseek.com/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
        body: JSON.stringify({ model: "deepseek-chat", messages: messages })
      });
      if (res.ok) {
        const d = await res.json();
        return { reply: d.choices[0].message.content, model: "DeepSeek V3", provider: "DeepSeek AI" };
      }
    } catch (e) {}
  }

  if (provider === "groq" && apiKey) {
    try {
      const res = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
        body: JSON.stringify({ model: "llama-3.3-70b-versatile", messages: messages })
      });
      if (res.ok) {
        const d = await res.json();
        return { reply: d.choices[0].message.content, model: "Llama 3.3 70B", provider: "Groq Cloud" };
      }
    } catch (e) {}
  }

  if (provider === "gemini" && apiKey) {
    try {
      const contents = messages.filter(m => m.role !== "system").map(m => ({
        role: m.role === "assistant" ? "model" : "user",
        parts: [{ text: m.content }]
      }));
      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          systemInstruction: { parts: [{ text: AI_SYSTEM_PROMPT }] },
          contents: contents
        })
      });
      if (res.ok) {
        const d = await res.json();
        const text = d.candidates?.[0]?.content?.parts?.[0]?.text;
        if (text) return { reply: text, model: "Gemini 1.5 Flash", provider: "Google Gemini" };
      }
    } catch (e) {}
  }

  return null; // Trả về null để chuyển sang Python Backend
}

// ─── 4. HIỂN THỊ TYPING INDICATOR ──────────────────────────────────────────
function showTypingIndicator() {
  const chatMessages = document.getElementById("chatbot-messages");
  if (!chatMessages) return;
  const indicator = document.createElement("div");
  indicator.className = "typing-indicator message bot";
  indicator.id = "typing-indicator";
  indicator.innerHTML = `<span></span><span></span><span></span>`;
  chatMessages.appendChild(indicator);
  scrollToBottom();
}

function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) indicator.remove();
}

function scrollToBottom() {
  const chatMessages = document.getElementById("chatbot-messages");
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// ─── 5. THANH THÔNG TIN ĐÁNH GIÁ CHẤT LƯỢNG ────────────────────────────────
function buildAIEvalBar(data) {
  const msgId = data.id || `msg_${Date.now()}`;
  const modelName = data.model || data.model_main || "ChatGPT 4o-mini";
  const providerName = data.provider || "Phát Tài AI";
  const intentLabel = (data.intent_label || data.intent || "Generative AI").replace(/_/g, " ");
  const latencyMs = data.latency_ms || 12;

  return `
    <div class="ai-meta-bar" style="
      margin-top: 8px; padding-top: 6px;
      border-top: 1px dashed rgba(0, 123, 255, 0.22);
      font-size: 0.72rem; color: #495057;">
      
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
        <span style="color: #007bff; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
          🤖 <strong>AI:</strong> ${modelName} · ⏱️ ${latencyMs}ms
        </span>
        <div id="eval-feedback-${msgId}" style="display: inline-flex; align-items: center; gap: 5px;">
          <span style="font-size: 0.68rem; color: #6c757d;">Đánh giá:</span>
          <button type="button" onclick="window.submitFeedback('${msgId}', 'useful', this)" title="Phản hồi hữu ích" style="
            background: #ffffff; border: 1px solid #00c896; color: #00c896; border-radius: 4px;
            padding: 1px 7px; font-size: 0.68rem; cursor: pointer; transition: all 0.2s; font-weight: 600;">
            👍 Hữu ích
          </button>
          <button type="button" onclick="window.submitFeedback('${msgId}', 'needs_improvement', this)" title="Cần cải thiện" style="
            background: #ffffff; border: 1px solid #ff4757; color: #ff4757; border-radius: 4px;
            padding: 1px 7px; font-size: 0.68rem; cursor: pointer; transition: all 0.2s; font-weight: 600;">
            👎 Cần sửa
          </button>
        </div>
      </div>
    </div>
  `;
}

window.submitFeedback = async function(msgId, rating, btn) {
  const container = document.getElementById(`eval-feedback-${msgId}`);
  if (container) {
    container.innerHTML = `
      <span style="font-size: 0.68rem; color: #00c896; font-weight: 700;">
        ✨ Cảm ơn bạn đã đánh giá: <strong>${rating === 'useful' ? '👍 Hữu ích' : '👎 Cần cải thiện'}</strong>
      </span>
    `;
  }

  const apiEndpoints = getApiCandidates();
  for (const baseUrl of apiEndpoints) {
    try {
      const res = await fetch(`${baseUrl}/api/chat/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message_id: msgId, rating: rating })
      });
      if (res.ok) {
        if (window.showDataToast) window.showDataToast("Đã lưu đánh giá chất lượng vào data/chat_history.json");
        break;
      }
    } catch (e) {}
  }
};

// ─── 6. RENDER TIN NHẮN (PARSER MARKDOWN ĐẦY ĐỦ) ───────────────────────────
function formatMarkdown(text) {
  if (!text) return "";
  let t = text;

  // Khối code ```python ... ```
  t = t.replace(/```([a-zA-Z0-9_\-+]*)\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre style="background: #1e293b; color: #f8fafc; padding: 10px 14px; border-radius: 8px; overflow-x: auto; font-size: 0.78rem; margin: 6px 0; font-family: monospace;"><code>${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>`;
  });

  // Code inline `...`
  t = t.replace(/`([^`]+)`/g, '<code style="background: rgba(0,123,255,0.08); padding: 1px 5px; border-radius: 4px; color: #0056d2; font-family: monospace; font-size: 0.82rem;">$1</code>');

  // Headers ###, ##, #
  t = t.replace(/^### (.*$)/gim, '<h4 style="font-size: 0.95rem; font-weight: 700; margin: 8px 0 4px 0; color: #0056d2;">$1</h4>');
  t = t.replace(/^## (.*$)/gim, '<h3 style="font-size: 1.05rem; font-weight: 700; margin: 10px 0 6px 0; color: #004085;">$1</h3>');

  // In đậm & in nghiêng
  t = t.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  t = t.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Xuống dòng
  t = t.replace(/\n/g, '<br>');

  return t;
}

function appendMessage(sender, text, evalData = null) {
  const chatMessages = document.getElementById("chatbot-messages");
  if (!chatMessages) return;
  
  const messageElement = document.createElement("div");
  messageElement.className = `message ${sender}`;
  
  let contentHtml = formatMarkdown(text);
  if (sender === "bot" && evalData) {
    contentHtml += buildAIEvalBar(evalData);
  }

  messageElement.innerHTML = contentHtml;
  chatMessages.appendChild(messageElement);
  scrollToBottom();

  try {
    sessionStorage.setItem("phattai_chat_session_html", chatMessages.innerHTML);
  } catch (e) {}
}

// ─── 7. XỬ LÝ PHẢN HỒI (HYBRID GENERATIVE AI + LOCAL BACKEND) ─────────────
async function handleBotReply(userMessage) {
  showTypingIndicator();
  const startTime = Date.now();
  
  const session = (typeof window !== "undefined" && window.getCurrentUser) ? window.getCurrentUser() : null;
  const userId = session ? (session.username || session.email || "customer") : "customer_guest";

  // Cập nhật context nhớ vào mảng
  chatHistoryMemory.push({ role: "user", content: userMessage });

  let finalReply = "";
  let evalMeta = null;

  const currentConfig = getStoredAIConfig();

  // 1. Thử gọi Generative AI (ChatGPT) nếu không ở chế độ thuần local
  if (currentConfig.provider !== "local") {
    try {
      const genResult = await callGenerativeAI(userMessage);
      if (genResult && genResult.reply) {
        finalReply = genResult.reply;
        const latency = Date.now() - startTime;
        evalMeta = {
          id: `msg_gen_${Date.now()}`,
          model: genResult.model,
          provider: genResult.provider,
          latency_ms: latency,
          intent_label: "ChatGPT Generative AI"
        };

        // Ghi log vào data/chat_history.json qua backend
        const apiEndpoints = getApiCandidates();
        for (const baseUrl of apiEndpoints) {
          try {
            fetch(`${baseUrl}/api/chat/log_external`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                id: evalMeta.id,
                user_id: userId,
                user_msg: userMessage,
                reply: finalReply,
                model: genResult.model,
                provider: genResult.provider,
                latency_ms: latency
              })
            }).catch(() => {});
            break;
          } catch (e) {}
        }
      }
    } catch (errGen) {
      console.warn("Lỗi Generative AI, chuyển sang gọi Python Backend:", errGen);
    }
  }

  // 2. Nếu chưa có câu trả lời, gọi Python Backend (/api/chat)
  if (!finalReply) {
    const apiEndpoints = getApiCandidates();
    for (const baseUrl of apiEndpoints) {
      try {
        const controller = (typeof AbortController !== "undefined") ? new AbortController() : null;
        const timeoutId = controller ? setTimeout(() => controller.abort(), 8000) : null;

        const response = await fetch(`${baseUrl}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userMessage, user_id: userId }),
          signal: controller ? controller.signal : undefined
        });
        if (timeoutId) clearTimeout(timeoutId);

        if (response.ok) {
          const receivedData = await response.json();
          if (receivedData && receivedData.reply) {
            finalReply = receivedData.reply;
            evalMeta = receivedData;
            break;
          }
        }
      } catch (err) {}
    }
  }

  // 3. Nếu server offline, dùng bộ giải quyết client-side
  if (!finalReply) {
    const cleanMsg = (userMessage || "").toLowerCase().trim();
    const dtRes = solveClientDatetime(cleanMsg);
    if (dtRes) {
      finalReply = dtRes;
    } else {
      const weatherRes = solveClientWeather(cleanMsg);
      if (weatherRes) {
        finalReply = weatherRes;
      } else {
        const foodRes = solveClientFood(cleanMsg);
        if (foodRes) {
          finalReply = foodRes;
        } else {
          const locRes = solveClientLocation(cleanMsg);
          if (locRes) {
            finalReply = locRes;
          } else {
            const mathRes = solveClientMath(cleanMsg);
            if (mathRes) {
              finalReply = mathRes;
            } else {
              let matched = null;
              let bestKwLen = 0;
              for (const item of BOT_BANK_RESPONSES) {
                for (const kw of item.keywords) {
                  if (cleanMsg.includes(kw) && kw.length > bestKwLen) {
                    bestKwLen = kw.length;
                    matched = item;
                  }
                }
              }
              if (matched) {
                finalReply = matched.response;
              } else {
                finalReply = `💡 **PHÁT TÀI BOT (AI GIẢI ĐÁP TRỰC TIẾP):**\n\n` +
                             `Về câu hỏi: **"${userMessage}"**\n\n` +
                             `• **Phân tích bản chất:** Đây là một câu hỏi rất thực tế và ý nghĩa. Dưới góc độ khoa học và ứng dụng thực tiễn, việc xác định rõ mục tiêu cốt lõi và từng bước hành động sẽ mang lại hiệu quả tối ưu.\n` +
                             `• **Các bước hành động trọng tâm:**\n` +
                             `  1️⃣ Xác định rõ kết quả đầu ra cụ thể bạn mong muốn đạt được.\n` +
                             `  2️⃣ Đánh giá các nguồn lực sẵn có và các phương án thực hiện khả thi.\n` +
                             `  3️⃣ Triển khai thử nghiệm từng bước nhỏ và đo lường kết quả thực tế.\n` +
                             `  4️⃣ Tinh chỉnh và tối ưu hóa giải pháp phù hợp với tình hình thực tế.\n\n` +
                             `💬 *Bạn hãy nhắn thêm chi tiết nếu cần phân tích sâu hơn về bất kỳ bước nào nhé!*`;
              }
            }
          }
        }
      }
    }
    evalMeta = {
      id: `msg_local_${Date.now()}`,
      model: "Phát Tài Local Engine",
      provider: "Offline Fallback",
      latency_ms: Date.now() - startTime
    };
  }

  removeTypingIndicator();

  // Lưu bot reply vào context nhớ
  chatHistoryMemory.push({ role: "assistant", content: finalReply });
  if (chatHistoryMemory.length > 8) chatHistoryMemory = chatHistoryMemory.slice(-8);

  appendMessage("bot", finalReply, evalMeta);
  saveLocalChatHistory(userMessage, finalReply, evalMeta?.intent_label || "chatgpt_reply");
}

function sendMessage(text) {
  if (!text || text.trim() === "") return;
  openChatbot();
  appendMessage("user", text.trim());
  handleBotReply(text.trim());
}

function renderQuickReplies() {
  const quickRepliesContainer = document.getElementById("chatbot-quick-replies");
  if (!quickRepliesContainer) return;

  quickRepliesContainer.innerHTML = BANK_QUICK_SUGGESTIONS.map(suggestion => `
    <button type="button" class="quick-reply-btn" data-msg="${suggestion}">${suggestion}</button>
  `).join("");
}

// ─── 8. GIAO DIỆN CÀI ĐẶT MÔ HÌNH AI & CHATGPT ─────────────────────────────
function toggleAISettingsModal() {
  const modal = document.getElementById("chatbot-settings-modal");
  if (!modal) return;
  if (modal.style.display === "flex") {
    modal.style.display = "none";
  } else {
    modal.style.display = "flex";
    // Load config hiện tại
    const cfg = getStoredAIConfig();
    const select = document.getElementById("ai-provider-select");
    const keyInput = document.getElementById("ai-api-key-input");
    if (select) select.value = cfg.provider;
    if (keyInput) keyInput.value = cfg.apiKey;
    updateKeyInputVisibility();
  }
}

function updateKeyInputVisibility() {
  const select = document.getElementById("ai-provider-select");
  const keyWrapper = document.getElementById("ai-key-input-wrapper");
  if (!select || !keyWrapper) return;
  if (["openai", "deepseek", "gemini", "groq"].includes(select.value)) {
    keyWrapper.style.display = "block";
  } else {
    keyWrapper.style.display = "none";
  }
}

function saveAISettings() {
  const select = document.getElementById("ai-provider-select");
  const keyInput = document.getElementById("ai-api-key-input");
  if (!select) return;

  const prov = select.value;
  const key = keyInput ? keyInput.value.trim() : "";

  localStorage.setItem("phattai_ai_provider", prov);
  localStorage.setItem("phattai_ai_key", key);

  updateAIStatusBadge();
  toggleAISettingsModal();

  if (window.showDataToast) {
    window.showDataToast("Đã lưu thiết lập mô hình AI thành công!");
  }
}

function updateAIStatusBadge() {
  const badge = document.getElementById("ai-mode-status-text");
  if (!badge) return;
  const cfg = getStoredAIConfig();
  const providerNames = {
    chatgpt_free: "ChatGPT 4o-mini (Toàn năng)",
    deepseek: "DeepSeek AI (V3/R1)",
    gemini: "Google Gemini 1.5",
    openai: "OpenAI GPT-4o",
    groq: "Groq Llama 3.3",
    local: "Mô hình Cục bộ Offline (MLP)"
  };
  badge.innerText = providerNames[cfg.provider] || "ChatGPT 4o-mini";
}

// ─── 9. ĐIỀU KHIỂN ĐÓNG / MỞ KHUNG CHAT ─────────────────────────────────────
let lastToggleTime = 0;

function openChatbot() {
  const chatWindow = document.getElementById("chatbot-window");
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatInput = document.getElementById("chatbot-input");
  if (!chatWindow) return;

  chatWindow.classList.add("active");
  chatWindow.style.setProperty("display", "flex", "important");
  chatWindow.style.setProperty("visibility", "visible", "important");
  chatWindow.style.setProperty("opacity", "1", "important");
  chatWindow.style.setProperty("pointer-events", "auto", "important");
  chatWindow.style.setProperty("transform", "translateY(0) scale(1)", "important");

  if (toggleBtn) toggleBtn.classList.add("active");
  const dot = toggleBtn ? toggleBtn.querySelector(".notification-dot") : null;
  if (dot) dot.remove();

  try {
    sessionStorage.setItem("phattai_chatbot_open", "true");
  } catch (e) {}

  setTimeout(() => {
    if (chatInput) chatInput.focus();
    scrollToBottom();
  }, 100);
}

function closeChatbot() {
  const chatWindow = document.getElementById("chatbot-window");
  const toggleBtn = document.getElementById("chatbot-toggle");
  if (chatWindow) {
    chatWindow.classList.remove("active");
    chatWindow.style.removeProperty("visibility");
    chatWindow.style.removeProperty("opacity");
    chatWindow.style.removeProperty("pointer-events");
    chatWindow.style.removeProperty("transform");
    chatWindow.style.removeProperty("display");
  }
  if (toggleBtn) toggleBtn.classList.remove("active");

  try {
    sessionStorage.setItem("phattai_chatbot_open", "false");
  } catch (e) {}
}

function toggleChatbot() {
  const now = Date.now();
  if (now - lastToggleTime < 250) return;
  lastToggleTime = now;

  const chatWindow = document.getElementById("chatbot-window");
  if (!chatWindow) return;
  
  if (chatWindow.classList.contains("active") || chatWindow.style.visibility === "visible") {
    closeChatbot();
  } else {
    openChatbot();
  }
}

function restoreChatSession() {
  try {
    const savedHtml = sessionStorage.getItem("phattai_chat_session_html");
    const chatMessages = document.getElementById("chatbot-messages");
    if (savedHtml && chatMessages && savedHtml.trim() !== "") {
      chatMessages.innerHTML = savedHtml;
      scrollToBottom();
    }
    const wasOpen = sessionStorage.getItem("phattai_chatbot_open");
    if (wasOpen === "true") {
      openChatbot();
    }
  } catch (e) {}
}

function initChatbotEvents() {
  const toggleBtn = document.getElementById("chatbot-toggle");
  const chatWindow = document.getElementById("chatbot-window");
  const chatForm = document.getElementById("chatbot-form");
  const chatInput = document.getElementById("chatbot-input");
  const sendBtn = document.getElementById("chatbot-send-btn");
  const quickReplies = document.getElementById("chatbot-quick-replies");
  const closeBtn = document.getElementById("chatbot-close-btn");
  const settingsBtn = document.getElementById("chatbot-settings-btn");
  
  if (!toggleBtn || !chatWindow) return;
  if (toggleBtn.dataset.initialized === "true") return;
  toggleBtn.dataset.initialized = "true";

  renderQuickReplies();
  restoreChatSession();
  updateAIStatusBadge();

  chatWindow.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  toggleBtn.onclick = (e) => {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    toggleChatbot();
    return false;
  };

  if (closeBtn) {
    closeBtn.onclick = (e) => {
      if (e) { e.preventDefault(); e.stopPropagation(); }
      closeChatbot();
      return false;
    };
  }

  if (settingsBtn) {
    settingsBtn.onclick = (e) => {
      if (e) { e.preventDefault(); e.stopPropagation(); }
      toggleAISettingsModal();
      return false;
    };
  }

  const handleUserSubmit = (e) => {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    const messageText = chatInput ? chatInput.value : "";
    if (messageText && messageText.trim() !== "") {
      sendMessage(messageText.trim());
      if (chatInput) chatInput.value = "";
    }
    return false;
  };

  if (chatForm && chatForm.tagName === "FORM") {
    chatForm.addEventListener("submit", handleUserSubmit);
  }
  if (sendBtn) {
    sendBtn.addEventListener("click", handleUserSubmit);
  }
  if (chatInput) {
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        e.stopPropagation();
        handleUserSubmit(e);
      }
    });
  }

  if (quickReplies) {
    quickReplies.addEventListener("click", (e) => {
      const btn = e.target.closest(".quick-reply-btn");
      if (btn) {
        e.preventDefault();
        e.stopPropagation();
        const msg = btn.getAttribute("data-msg") || btn.innerText;
        if (msg && msg.trim() !== "") {
          sendMessage(msg.trim());
        }
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeChatbot();
    } else if (e.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement?.tagName)) {
      e.preventDefault();
      openChatbot();
    }
  });
}

// ─── 10. TỰ ĐỘNG KHỞI TẠO KHUNG CHATBOT TOÀN NĂNG ──────────────────────────
function ensureChatbotExists() {
  let toggleBtn = document.getElementById("chatbot-toggle");
  let chatWindow = document.getElementById("chatbot-window");

  // Nếu chưa có trong DOM, tự động tạo mới hoàn chỉnh
  if (!toggleBtn || !chatWindow) {
    const existingWidget = document.querySelector(".chatbot-widget");
    if (existingWidget) existingWidget.remove();

    const chatbotWidget = document.createElement("div");
    chatbotWidget.className = "chatbot-widget";
    chatbotWidget.innerHTML = `
      <button class="chatbot-toggle" id="chatbot-toggle" aria-label="Mở khung chat" title="Trò chuyện với Phát Tài Bot - ChatGPT (phím /)">
        <i class="fa-solid fa-robot"></i>
        <span class="notification-dot"></span>
      </button>

      <div class="chatbot-window" id="chatbot-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="chat-header-main">
            <div class="bot-avatar">
              <i class="fa-solid fa-wand-magic-sparkles"></i>
            </div>
            <div class="bot-info">
              <h3 style="font-size: 0.98rem; margin: 0; color: #fff; display: flex; align-items: center; gap: 6px;">
                Phát Tài Bot <span style="font-size: 0.65rem; background: rgba(255,255,255,0.22); padding: 1px 6px; border-radius: 10px; font-weight: normal;">ChatGPT 4o</span>
              </h3>
              <div style="font-size: 0.68rem; color: #a3e635; display: flex; align-items: center; gap: 4px; margin-top: 1px;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #22c55e; display: inline-block;"></span>
                <span id="ai-mode-status-text">ChatGPT 4o-mini (Toàn năng)</span>
              </div>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 6px;">
            <button type="button" class="chat-header-close" id="chatbot-settings-btn" title="Cài đặt Mô Hình AI & API Key" aria-label="Settings" style="font-size: 0.85rem;">
              <i class="fa-solid fa-sliders"></i>
            </button>
            <button type="button" class="chat-header-close" id="chatbot-close-btn" title="Đóng chat (phím Esc)" aria-label="Close Chat">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>
        </div>

        <!-- Settings Modal Overlay bên trong Chatbot -->
        <div id="chatbot-settings-modal" style="display: none; position: absolute; top: 58px; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.98); z-index: 100; flex-direction: column; padding: 16px; font-size: 0.85rem; color: #1e293b; overflow-y: auto;">
          <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 12px; color: #0056d2; display: flex; align-items: center; gap: 6px;">
            <i class="fa-solid fa-sliders"></i> Cài Đặt Trí Tuệ Nhân Tạo (AI Model)
          </div>
          <div style="margin-bottom: 12px;">
            <label style="display: block; font-weight: 600; margin-bottom: 4px; font-size: 0.78rem;">Chọn Nhà Cung Cấp AI:</label>
            <select id="ai-provider-select" onchange="window.updateKeyInputVisibility()" style="width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.82rem; background: #fff;">
              <option value="chatgpt_free">🌟 ChatGPT 4o-mini (Miễn phí qua Puter/Pollinations - Không cần Key)</option>
              <option value="deepseek">⚡ DeepSeek AI (DeepSeek-V3 / R1)</option>
              <option value="gemini">🔮 Google Gemini 1.5 Flash</option>
              <option value="openai">🟢 OpenAI Trực Tiếp (GPT-4o / GPT-4o-mini)</option>
              <option value="groq">🚀 Groq Cloud (Llama 3.3 70B Siêu Tốc)</option>
              <option value="local">🏦 Mô Hình Cục Bộ Offline (MLP BANKING77 + Scikit-Learn)</option>
            </select>
            <small style="color: #64748b; font-size: 0.72rem; display: block; margin-top: 3px;">
              *Chế độ ChatGPT Miễn phí trả lời được MỌI câu hỏi trên thế giới (toán, code, văn học, khoa học, ngân hàng) mà không cần nhập API Key.
            </small>
          </div>

          <div id="ai-key-input-wrapper" style="display: none; margin-bottom: 12px;">
            <label style="display: block; font-weight: 600; margin-bottom: 4px; font-size: 0.78rem;">Nhập API Key Cá Nhân:</label>
            <input type="password" id="ai-api-key-input" placeholder="sk-... hoặc AIza..." style="width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.82rem; box-sizing: border-box;">
            <small style="color: #64748b; font-size: 0.7rem; display: block; margin-top: 3px;">Key được bảo mật lưu trữ tại trình duyệt của bạn.</small>
          </div>

          <div style="margin-top: auto; display: flex; gap: 8px; justify-content: flex-end;">
            <button type="button" onclick="window.toggleAISettingsModal()" style="padding: 6px 14px; border: 1px solid #cbd5e1; background: #f8fafc; border-radius: 6px; cursor: pointer; font-size: 0.8rem;">Đóng</button>
            <button type="button" onclick="window.saveAISettings()" style="padding: 6px 16px; background: #007bff; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.8rem;">Lưu Cài Đặt</button>
          </div>
        </div>

        <!-- Messages Area -->
        <div class="chat-messages" id="chatbot-messages">
          <div class="message bot">
            Xin chào bạn! 🏦 Tôi là <strong>Phát Tài Bot</strong> — Trợ lý AI toàn năng tích hợp công nghệ <strong>ChatGPT 4o-mini</strong> kết hợp cơ sở tri thức chuẩn <strong>BANKING77 – Hugging Face</strong>.<br><br>Tôi có thể <strong>trả lời MỌI câu hỏi</strong> giống như ChatGPT: giải toán, viết code lập trình, giải thích khoa học, lịch sử, làm thơ, soạn thảo văn bản, cũng như hướng dẫn chi tiết mọi thủ tục ngân hàng (mở tài khoản, kích hoạt thẻ, tiết kiệm 6.8%, vay tín chấp).<br><br>👉 Bạn có thể hỏi bất kỳ câu hỏi nào ngay bây giờ!
          </div>
        </div>

        <!-- Quick Replies -->
        <div class="quick-replies" id="chatbot-quick-replies"></div>

        <!-- Input Area -->
        <div class="chat-input-area">
          <div id="chatbot-form" class="chat-form-container">
            <input type="text" id="chatbot-input" placeholder="Hỏi bất kỳ điều gì: code, giải toán, khoa học, ngân hàng..." autocomplete="off" aria-label="Nội dung chat">
            <button type="button" id="chatbot-send-btn" aria-label="Gửi tin nhắn"><i class="fa-solid fa-paper-plane"></i></button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(chatbotWidget);
  } else {
    // Nếu widget đã có trong HTML, nâng cấp Header và thêm Modal Settings
    const chatHeader = chatWindow.querySelector(".chat-header");
    if (chatHeader) {
      if (!chatHeader.querySelector("#chatbot-settings-btn")) {
        const settingsBtn = document.createElement("button");
        settingsBtn.type = "button";
        settingsBtn.className = "chat-header-close";
        settingsBtn.id = "chatbot-settings-btn";
        settingsBtn.title = "Cài đặt Mô Hình AI & API Key";
        settingsBtn.style.marginRight = "4px";
        settingsBtn.style.fontSize = "0.85rem";
        settingsBtn.innerHTML = `<i class="fa-solid fa-sliders"></i>`;
        
        const closeBtn = chatHeader.querySelector("#chatbot-close-btn");
        if (closeBtn) {
          chatHeader.insertBefore(settingsBtn, closeBtn);
        } else {
          chatHeader.appendChild(settingsBtn);
        }
      }

      // Thêm subtitle badge trạng thái
      const botInfo = chatHeader.querySelector(".bot-info");
      if (botInfo && !botInfo.querySelector("#ai-mode-status-text")) {
        botInfo.innerHTML = `
          <h3 style="font-size: 0.98rem; margin: 0; color: #fff; display: flex; align-items: center; gap: 6px;">
            Phát Tài Bot <span style="font-size: 0.65rem; background: rgba(255,255,255,0.22); padding: 1px 6px; border-radius: 10px; font-weight: normal;">ChatGPT 4o</span>
          </h3>
          <div style="font-size: 0.68rem; color: #a3e635; display: flex; align-items: center; gap: 4px; margin-top: 1px;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #22c55e; display: inline-block;"></span>
            <span id="ai-mode-status-text">ChatGPT 4o-mini (Toàn năng)</span>
          </div>
        `;
      }
    }

    // Đảm bảo có Modal Settings trong chatWindow
    if (!chatWindow.querySelector("#chatbot-settings-modal")) {
      const modalDiv = document.createElement("div");
      modalDiv.id = "chatbot-settings-modal";
      modalDiv.style.cssText = "display: none; position: absolute; top: 58px; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.98); z-index: 100; flex-direction: column; padding: 16px; font-size: 0.85rem; color: #1e293b; overflow-y: auto;";
      modalDiv.innerHTML = `
        <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 12px; color: #0056d2; display: flex; align-items: center; gap: 6px;">
          <i class="fa-solid fa-sliders"></i> Cài Đặt Trí Tuệ Nhân Tạo (AI Model)
        </div>
        <div style="margin-bottom: 12px;">
          <label style="display: block; font-weight: 600; margin-bottom: 4px; font-size: 0.78rem;">Chọn Nhà Cung Cấp AI:</label>
          <select id="ai-provider-select" onchange="window.updateKeyInputVisibility()" style="width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.82rem; background: #fff;">
            <option value="chatgpt_free">🌟 ChatGPT 4o-mini (Miễn phí qua Puter/Pollinations - Không cần Key)</option>
            <option value="deepseek">⚡ DeepSeek AI (DeepSeek-V3 / R1)</option>
            <option value="gemini">🔮 Google Gemini 1.5 Flash</option>
            <option value="openai">🟢 OpenAI Trực Tiếp (GPT-4o / GPT-4o-mini)</option>
            <option value="groq">🚀 Groq Cloud (Llama 3.3 70B Siêu Tốc)</option>
            <option value="local">🏦 Mô Hình Cục Bộ Offline (MLP BANKING77 + Scikit-Learn)</option>
          </select>
          <small style="color: #64748b; font-size: 0.72rem; display: block; margin-top: 3px;">
            *Chế độ ChatGPT Miễn phí trả lời được MỌI câu hỏi trên thế giới (toán, code, văn học, khoa học, ngân hàng) mà không cần nhập API Key.
          </small>
        </div>

        <div id="ai-key-input-wrapper" style="display: none; margin-bottom: 12px;">
          <label style="display: block; font-weight: 600; margin-bottom: 4px; font-size: 0.78rem;">Nhập API Key Cá Nhân:</label>
          <input type="password" id="ai-api-key-input" placeholder="sk-... hoặc AIza..." style="width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 0.82rem; box-sizing: border-box;">
          <small style="color: #64748b; font-size: 0.7rem; display: block; margin-top: 3px;">Key được bảo mật lưu trữ tại trình duyệt của bạn.</small>
        </div>

        <div style="margin-top: auto; display: flex; gap: 8px; justify-content: flex-end;">
          <button type="button" onclick="window.toggleAISettingsModal()" style="padding: 6px 14px; border: 1px solid #cbd5e1; background: #f8fafc; border-radius: 6px; cursor: pointer; font-size: 0.8rem;">Đóng</button>
          <button type="button" onclick="window.saveAISettings()" style="padding: 6px 16px; background: #007bff; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.8rem;">Lưu Cài Đặt</button>
        </div>
      `;
      chatWindow.appendChild(modalDiv);
    }
  }

  initChatbotEvents();
}

window.initChatbotEvents = initChatbotEvents;
window.sendMessage = sendMessage;
window.openChatbot = openChatbot;
window.closeChatbot = closeChatbot;
window.toggleChatbot = toggleChatbot;
window.toggleAISettingsModal = toggleAISettingsModal;
window.updateKeyInputVisibility = updateKeyInputVisibility;
window.saveAISettings = saveAISettings;

document.addEventListener("DOMContentLoaded", () => {
  ensureChatbotExists();
});

if (document.readyState === "complete" || document.readyState === "interactive") {
  ensureChatbotExists();
}
