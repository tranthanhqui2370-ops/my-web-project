/**
 * PHÁT TÀI BANK - Public Fetch API Integration Module
 * Thực hiện gọi đồng thời Open-Meteo Weather API (thời tiết tại Hội sở TP.HCM)
 * và Advice Slip API kết hợp các khuyến cáo bảo mật tài chính, phòng ngừa gian lận thẻ & OTP.
 */

const LATITUDE = "10.823";
const LONGITUDE = "106.63";
const WEATHER_API_URL = `https://api.open-meteo.com/v1/forecast?latitude=${LATITUDE}&longitude=${LONGITUDE}&current_weather=true`;
const ADVICE_API_URL = "https://api.adviceslip.com/advice";

const WEATHER_CODES = {
  0: { text: "Trời trong xanh", icon: "fa-sun", tip: "Thời tiết thuận lợi cho các giao dịch trực tiếp tại quầy PHÁT TÀI BANK." },
  1: { text: "Ít mây", icon: "fa-cloud-sun", tip: "Thời tiết dịu mát, trải nghiệm mở tài khoản E-Banking số đẹp nhận quà." },
  2: { text: "Nhiều mây", icon: "fa-cloud-sun", tip: "Chuyển tiền nhanh 24/7 Napas tiện lợi ngay tại nhà qua ứng dụng." },
  3: { text: "Trời âm u", icon: "fa-cloud", tip: "Kiểm tra hạn mức chi tiêu định kỳ để quản lý ngân sách hiệu quả." },
  45: { text: "Có sương mù", icon: "fa-smog", tip: "Bảo mật tài khoản: Tuyệt đối không chia sẻ mã OTP cho bất kỳ ai." },
  48: { text: "Sương mù lạnh", icon: "fa-smog", tip: "Kích hoạt xác thực sinh trắc học FaceID trên E-Banking để tăng bảo mật." },
  51: { text: "Mưa phùn nhẹ", icon: "fa-cloud-rain", tip: "Mưa nhẹ: Thanh toán tiền điện nước online không lo trễ hạn." },
  61: { text: "Mưa rào nhẹ", icon: "fa-cloud-rain", tip: "Mở sổ tiết kiệm online lãi suất tới 6.8%/năm nhận lãi ngay hôm nay." },
  80: { text: "Mưa rào rải rác", icon: "fa-cloud-sun-rain", tip: "Hạn chế ra ngoài, quét mã QR thanh toán hóa đơn siêu tốc trên điện thoại." },
  95: { text: "Dông bão", icon: "fa-cloud-bolt", tip: "Cảnh giác với các tin nhắn mạo danh đường link ngân hàng lạ!" },
  default: { text: "Thời tiết ổn định", icon: "fa-cloud-sun", tip: "Bảo vệ tài chính: Đổi mật khẩu E-Banking định kỳ 3 tháng một lần." }
};

const BANK_SECURITY_TIPS = [
  "PHÁT TÀI BANK không bao giờ yêu cầu khách hàng cung cấp mã OTP, mật khẩu hay mã CVV dưới bất kỳ hình thức nào.",
  "Hãy kích hoạt tính năng thông báo biến động số dư tức thì để kiểm soát mọi giao dịch phát sinh.",
  "Sử dụng Thẻ ảo khi mua sắm trên các trang thương mại điện tử để ngăn chặn lộ thông tin thẻ vật lý.",
  "Không đăng nhập tài khoản E-Banking trên các thiết bị công cộng hoặc mạng WiFi không bảo mật.",
  "Định kỳ kiểm tra sao kê tài khoản và báo ngay hotline 1900-8888 nếu phát hiện giao dịch bất thường.",
  "Cài đặt hạn mức giao dịch thẻ theo ngày để giảm thiểu rủi ro khi bị mất thẻ."
];

async function fetchBankingWeather() {
  const weatherTextSpan = document.getElementById("weather-text");
  const weatherIcon = document.querySelector(".weather-widget i");
  if (!weatherTextSpan) return;
  
  try {
    const response = await fetch(WEATHER_API_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    const data = await response.json();
    const temp = Math.round(data.current_weather.temperature);
    const code = data.current_weather.weathercode;
    const weatherInfo = WEATHER_CODES[code] || WEATHER_CODES.default;
    
    if (weatherIcon) weatherIcon.className = `fa-solid ${weatherInfo.icon}`;
    weatherTextSpan.innerHTML = `Chi nhánh TP.HCM: <strong>${temp}°C</strong> - ${weatherInfo.text}. <span style="font-size: 0.8rem; color: var(--text-muted); display: block;">💡 Gợi ý giao dịch: ${weatherInfo.tip}</span>`;
  } catch (error) {
    if (weatherIcon) weatherIcon.className = "fa-solid fa-cloud-sun";
    weatherTextSpan.innerHTML = `Chi nhánh TP.HCM: <strong>29°C</strong> - Nắng nhẹ. <span style="font-size: 0.8rem; color: var(--text-muted); display: block;">💡 Khuyến cáo: Tuyệt đối không chia sẻ mã OTP cho bất kỳ ai!</span>`;
  }
}

async function fetchDailyFinancialAdvice() {
  const quoteTextSpan = document.getElementById("quote-text");
  if (!quoteTextSpan) return;
  
  try {
    const response = await fetch(ADVICE_API_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const englishAdvice = data.slip.advice;
    const randomTip = BANK_SECURITY_TIPS[Math.floor(Math.random() * BANK_SECURITY_TIPS.length)];
    
    quoteTextSpan.innerHTML = `"${englishAdvice}" <span style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-top: 2px;">🛡️ Mẹo bảo mật PHÁT TÀI BANK: ${randomTip}</span>`;
  } catch (error) {
    const randomTip = BANK_SECURITY_TIPS[Math.floor(Math.random() * BANK_SECURITY_TIPS.length)];
    quoteTextSpan.innerHTML = `"Financial security begins with awareness." <span style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-top: 2px;">🛡️ Mẹo bảo mật PHÁT TÀI BANK: ${randomTip}</span>`;
  }
}

async function loadAllInfoWidgets() {
  await Promise.all([
    fetchBankingWeather(),
    fetchDailyFinancialAdvice()
  ]);
}

window.loadAllInfoWidgets = loadAllInfoWidgets;
