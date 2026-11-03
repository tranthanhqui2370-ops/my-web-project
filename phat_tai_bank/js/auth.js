/**
 * OrganiCo - Authentication and Member Management Module (Auth)
 * Xử lý đăng nhập, đăng ký, lưu trữ tài khoản người dùng và trạng thái đăng nhập vào LocalStorage.
 */

// 1. KHỞI TẠO DỮ LIỆU TÀI KHOẢN & TRẠNG THÁI
let usersList = [];
let currentUser = null;

// Tài khoản quản trị mặc định ban đầu để thử nghiệm nhanh
const DEFAULT_USERS = [
  {
    username: "admin",
    password: "admin123",
    fullname: "Quản Trị Viên",
    address: "123 Nguyễn Văn Cừ, Q.5, TP.HCM"
  },
  {
    username: "khachhang",
    password: "123456",
    fullname: "Nguyễn Văn A",
    address: "456 Lê Đại Hành, Q.11, TP.HCM"
  }
];

// Khởi chạy nạp dữ liệu từ máy chủ và cơ sở dữ liệu data/customers.json
async function initAuthSystem() {
  ensureAuthModalExists();

  // Nạp danh sách khách hàng trực tiếp từ data/customers.json qua API
  try {
    const res = await fetch("http://localhost:8000/api/customers");
    if (res.ok) {
      const serverUsers = await res.json();
      if (Array.isArray(serverUsers) && serverUsers.length > 0) {
        usersList = serverUsers;
      }
    }
  } catch (e) {
    console.warn("Chưa kết nối API data/customers.json, dùng danh sách mẫu:", e);
    usersList = [...DEFAULT_USERS];
  }

  // Khôi phục phiên đăng nhập hiện tại nếu có
  const storedCurrentUser = sessionStorage.getItem("phattai_current_user") || localStorage.getItem("organico_current_user");
  if (storedCurrentUser) {
    try {
      currentUser = JSON.parse(storedCurrentUser);
    } catch (e) {
      currentUser = null;
    }
  }

  // Render trạng thái trên header ban đầu
  updateAuthHeaderUI();
  
  // Khởi động các sự kiện auth
  bindAuthEvents();
}

function ensureAuthModalExists() {
  if (!document.getElementById("auth-modal")) {
    const modalDiv = document.createElement("div");
    modalDiv.className = "modal";
    modalDiv.id = "auth-modal";
    modalDiv.setAttribute("aria-hidden", "true");
    modalDiv.innerHTML = `
      <div class="modal-overlay" id="auth-modal-overlay"></div>
      <div class="modal-content auth-modal-content">
        <div class="auth-modal-header">
          <div class="auth-tabs">
            <button class="auth-tab active" id="tab-login-btn">Đăng Nhập</button>
            <button class="auth-tab" id="tab-register-btn">Đăng Ký</button>
          </div>
          <button class="close-modal-btn" id="auth-modal-close" title="Đóng" aria-label="Close modal">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
        <div class="modal-body">
          <form id="login-form" class="auth-form active">
            <div class="form-group">
              <label for="login-username">Tên đăng nhập</label>
              <input type="text" id="login-username" placeholder="Nhập tên đăng nhập..." required autocomplete="username">
              <span class="error-msg" id="login-username-error"></span>
            </div>
            <div class="form-group">
              <label for="login-password">Mật khẩu</label>
              <div class="password-input-wrapper">
                <input type="password" id="login-password" placeholder="Nhập mật khẩu..." required autocomplete="current-password">
                <button type="button" class="toggle-password-btn" aria-label="Hiện mật khẩu"><i class="fa-solid fa-eye"></i></button>
              </div>
              <span class="error-msg" id="login-password-error"></span>
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top: 15px; width: 100%;">Đăng Nhập</button>
            <div class="auth-switch-prompt" style="margin-top: 18px; text-align: center; font-size: 0.9rem; color: var(--text-color);">
              Chưa có tài khoản? <a href="#" id="switch-to-register" class="switch-to-reg-btn" style="color: #27ae60; font-weight: 700; text-decoration: underline;">Đăng ký ngay</a>
            </div>
          </form>
          <form id="register-form" class="auth-form">
            <div class="form-group">
              <label for="register-username">Tên đăng nhập</label>
              <input type="text" id="register-username" placeholder="Ví dụ: nguyenvana" required autocomplete="username">
              <span class="error-msg" id="register-username-error"></span>
            </div>
            <div class="form-group">
              <label for="register-address">Địa chỉ giao hàng</label>
              <input type="text" id="register-address" placeholder="Nhập địa chỉ nhận hàng của bạn">
              <span class="error-msg" id="register-address-error"></span>
            </div>
            <div class="form-group">
              <label for="register-fullname">Họ và tên</label>
              <input type="text" id="register-fullname" placeholder="Ví dụ: Nguyễn Văn A" required>
              <span class="error-msg" id="register-fullname-error"></span>
            </div>
            <div class="form-group">
              <label for="register-password">Mật khẩu (tối thiểu 6 ký tự)</label>
              <div class="password-input-wrapper">
                <input type="password" id="register-password" placeholder="Nhập mật khẩu..." required autocomplete="new-password">
                <button type="button" class="toggle-password-btn" aria-label="Hiện mật khẩu"><i class="fa-solid fa-eye"></i></button>
              </div>
              <span class="error-msg" id="register-password-error"></span>
            </div>
            <div class="form-group">
              <label for="register-confirm-password">Xác nhận mật khẩu</label>
              <div class="password-input-wrapper">
                <input type="password" id="register-confirm-password" placeholder="Nhập lại mật khẩu..." required autocomplete="new-password">
                <button type="button" class="toggle-password-btn" aria-label="Hiện mật khẩu"><i class="fa-solid fa-eye"></i></button>
              </div>
              <span class="error-msg" id="register-confirm-password-error"></span>
            </div>
            <button type="submit" class="btn btn-primary" style="margin-top: 15px; width: 100%;">Đăng Ký Tài Khoản</button>
            <div class="auth-switch-prompt" style="margin-top: 18px; text-align: center; font-size: 0.9rem; color: var(--text-color);">
              Đã có tài khoản? <a href="#" id="switch-to-login" class="switch-to-log-btn" style="color: #27ae60; font-weight: 700; text-decoration: underline;">Đăng nhập ngay</a>
            </div>
          </form>
        </div>
      </div>
    `;
    document.body.appendChild(modalDiv);
  }
}

document.addEventListener("click", (e) => {
  const regBtn = e.target.closest("#register-link, .nav-item-register, #switch-to-register, .switch-to-reg-btn");
  if (regBtn) {
    e.preventDefault();
    openAuthModal("register");
  }

  const logBtn = e.target.closest("#switch-to-login, .switch-to-log-btn");
  if (logBtn) {
    e.preventDefault();
    openAuthModal("login");
  }
});


// 2. CẬP NHẬT GIAO DIỆN HEADER (AUTH STATES UI)
function updateAuthHeaderUI() {
  const container = document.getElementById("auth-header-container");
  if (!container) return;

  container.innerHTML = "";

  if (currentUser) {
    // Nếu đã đăng nhập: hiển thị menu dropdown tên người dùng
    const firstChar = currentUser.fullname.charAt(0).toUpperCase();
    const dropdownWrapper = document.createElement("div");
    dropdownWrapper.className = "user-menu-wrapper";
    dropdownWrapper.id = "user-menu-wrapper";
    
    dropdownWrapper.innerHTML = `
      <button class="user-dropdown-btn" id="user-dropdown-btn" aria-haspopup="true" aria-expanded="false" title="Tài khoản cá nhân">
        <span class="avatar-placeholder">${firstChar}</span>
        <span class="fullname-text" style="max-width: 110px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${currentUser.fullname}</span>
        <i class="fa-solid fa-chevron-down"></i>
      </button>
      <div class="user-dropdown-menu" id="user-dropdown-menu">
        <div class="dropdown-header">
          <span>Xin chào,</span>
          <div class="user-name-display">${currentUser.fullname}</div>
        </div>
        <a href="#planner"><i class="fa-solid fa-clipboard-list"></i> Thực đơn của tôi</a>
        <button id="logout-btn" class="logout-btn"><i class="fa-solid fa-right-from-bracket"></i> Đăng Xuất</button>
      </div>
    `;

    container.appendChild(dropdownWrapper);

    // Sự kiện mở/đóng menu thả xuống
    const dropdownBtn = dropdownWrapper.querySelector("#user-dropdown-btn");
    const dropdownMenu = dropdownWrapper.querySelector("#user-dropdown-menu");
    
    if (dropdownBtn && dropdownMenu) {
      dropdownBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const isActive = dropdownMenu.classList.toggle("active");
        dropdownBtn.setAttribute("aria-expanded", isActive ? "true" : "false");
      });
    }

    // Sự kiện Click Đăng xuất
    const logoutBtn = dropdownWrapper.querySelector("#logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        handleLogout();
      });
    }

    // Đóng dropdown khi click ngoài
    document.addEventListener("click", (e) => {
      if (!dropdownWrapper.contains(e.target)) {
        dropdownMenu.classList.remove("active");
        dropdownBtn.setAttribute("aria-expanded", "false");
      }
    });

  } else {
    // Nếu chưa đăng nhập: hiển thị nút "Đăng Nhập"
    const loginBtn = document.createElement("button");
    loginBtn.className = "auth-btn";
    loginBtn.id = "open-login-modal-btn";
    loginBtn.innerHTML = `<i class="fa-solid fa-user"></i> <span>Đăng Nhập</span>`;
    
    loginBtn.addEventListener("click", () => {
      openAuthModal("login");
    });
    
    container.appendChild(loginBtn);
  }
}

// 3. ĐĂNG KÝ CÁC SỰ KIỆN FORM VÀ MODAL
function bindAuthEvents() {
  const modal = document.getElementById("auth-modal");
  const closeBtn = document.getElementById("auth-modal-close");
  const overlay = document.getElementById("auth-modal-overlay");
  
  const tabLogin = document.getElementById("tab-login-btn");
  const tabRegister = document.getElementById("tab-register-btn");
  
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  
  // Tắt mở modal
  const closeModalFunc = () => {
    if (modal) modal.classList.remove("active");
    document.body.style.overflow = "";
    resetFormErrors();
  };
  
  if (closeBtn) closeBtn.addEventListener("click", closeModalFunc);
  if (overlay) overlay.addEventListener("click", closeModalFunc);

  // Chuyển đổi qua lại giữa tab Đăng nhập và Đăng ký
  if (tabLogin && tabRegister && loginForm && registerForm) {
    tabLogin.addEventListener("click", () => {
      tabLogin.classList.add("active");
      tabRegister.classList.remove("active");
      loginForm.classList.add("active");
      registerForm.classList.remove("active");
      resetFormErrors();
    });

    tabRegister.addEventListener("click", () => {
      tabRegister.classList.add("active");
      tabLogin.classList.remove("active");
      registerForm.classList.add("active");
      loginForm.classList.remove("active");
      resetFormErrors();
    });
  }

  // Sự kiện ẩn/hiện mật khẩu (Password Toggles)
  const passwordWrappers = document.querySelectorAll(".password-input-wrapper");
  passwordWrappers.forEach(wrapper => {
    const input = wrapper.querySelector("input");
    const toggleBtn = wrapper.querySelector(".toggle-password-btn");
    if (input && toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const type = input.getAttribute("type") === "password" ? "text" : "password";
        input.setAttribute("type", type);
        const icon = toggleBtn.querySelector("i");
        if (icon) {
          icon.className = type === "password" ? "fa-solid fa-eye" : "fa-solid fa-eye-slash";
        }
      });
    }
  });

  // ==========================================
  // A. SUBMIT FORM ĐĂNG NHẬP (XÁC THỰC TRỰC TIẾP TỪ data/customers.json)
  // ==========================================
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      resetFormErrors();
      
      const usernameInput = document.getElementById("login-username");
      const passwordInput = document.getElementById("login-password");
      
      const username = usernameInput.value.trim().toLowerCase();
      const password = passwordInput.value;
      
      let hasError = false;

      // Validate cơ bản
      if (username === "") {
        showFieldError("login-username", "Tên đăng nhập không được để trống.");
        hasError = true;
      }
      if (password === "") {
        showFieldError("login-password", "Mật khẩu không được để trống.");
        hasError = true;
      }

      if (hasError) return;

      // Gọi API xác thực trực tiếp từ data/customers.json
      try {
        const res = await fetch("http://localhost:8000/api/customers/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });
        if (res.ok) {
          const result = await res.json();
          if (result.status === "success" && result.user) {
            handleLoginSuccess(result.user);
            if (window.showDataToast) window.showDataToast("Đã xác thực từ data/customers.json");
            return;
          } else {
            showFieldError("login-password", result.message || "Tên đăng nhập hoặc mật khẩu không chính xác.");
            return;
          }
        }
      } catch (err) {
        console.warn("Server API offline, kiểm tra dữ liệu nội bộ:", err);
      }

      // Fallback nếu server chưa chạy
      const user = usersList.find(u => u.username === username);
      if (!user) {
        showFieldError("login-username", "Tên đăng nhập không tồn tại.");
        return;
      }

      if (user.password !== password) {
        showFieldError("login-password", "Mật khẩu không chính xác.");
        return;
      }

      handleLoginSuccess(user);
    });
  }

  // ==========================================
  // B. SUBMIT FORM ĐĂNG KÝ (LƯU TRỰC TIẾP VÀO data/customers.json)
  // ==========================================
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      resetFormErrors();
      
      const usernameInput = document.getElementById("register-username");
      const fullnameInput = document.getElementById("register-fullname");
      const passwordInput = document.getElementById("register-password");
      const confirmPasswordInput = document.getElementById("register-confirm-password");
      const addressInput = document.getElementById("register-address");
      
      const username = usernameInput.value.trim().toLowerCase();
      const fullname = fullnameInput.value.trim();
      const password = passwordInput.value;
      const confirmPassword = confirmPasswordInput.value;
      const address = addressInput ? addressInput.value.trim() : "";
      
      let hasError = false;

      // Regex kiểm tra tên đăng nhập (chỉ chữ thường, số, không khoảng trắng, 4-15 ký tự)
      const usernameRegex = /^[a-z0-9_]{4,15}$/;

      if (!usernameRegex.test(username)) {
        showFieldError("register-username", "Tên đăng nhập phải viết liền không dấu, từ 4-15 ký tự (chữ thường, số hoặc dấu gạch dưới).");
        hasError = true;
      }

      if (fullname.length < 2) {
        showFieldError("register-fullname", "Họ và tên tối thiểu 2 ký tự.");
        hasError = true;
      }

      if (address.length < 5) {
        showFieldError("register-address", "Vui lòng nhập địa chỉ cụ thể (tối thiểu 5 ký tự).");
        hasError = true;
      }

      if (password.length < 6) {
        showFieldError("register-password", "Mật khẩu phải tối thiểu từ 6 ký tự.");
        hasError = true;
      }

      if (password !== confirmPassword) {
        showFieldError("register-confirm-password", "Mật khẩu xác nhận không trùng khớp.");
        hasError = true;
      }

      if (hasError) return;

      const accountNumber = "PTB" + Math.floor(1000000000 + Math.random() * 9000000000);
      const newUser = {
        username: username,
        password: password,
        fullname: fullname,
        address: address,
        accountNumber: accountNumber,
        phone: "09" + Math.floor(10000000 + Math.random() * 90000000)
      };

      // Gọi API đăng ký lưu trực tiếp vào tệp data/customers.json
      try {
        const res = await fetch("http://localhost:8000/api/customers/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: username,
            password: password,
            fullname: fullname,
            phone: newUser.phone,
            address: address,
            accountNumber: accountNumber
          })
        });
        if (res.ok) {
          const regResult = await res.json();
          if (regResult.status === "exists") {
            showFieldError("register-username", regResult.message || "Tên đăng nhập đã tồn tại trên hệ thống.");
            return;
          }
        }
      } catch (err) {
        console.warn("Lỗi gọi API đăng ký data/customers.json:", err);
      }

      usersList.push(newUser);
      if (window.showDataToast) window.showDataToast("Đã lưu tài khoản vào data/customers.json");
      else showAuthToast(`🎉 Đăng ký thành công! Số TK: ${accountNumber}`, "success");

      // Auto login sau khi đăng ký
      handleLoginSuccess(newUser);
    });
  }
}

// 4. XỬ LÝ ĐĂNG NHẬP / ĐĂNG XUẤT THÀNH CÔNG
function handleLoginSuccess(user) {
  currentUser = user;
  sessionStorage.setItem("phattai_current_user", JSON.stringify(currentUser));
  localStorage.setItem("organico_current_user", JSON.stringify(currentUser));
  localStorage.setItem("phattai_session", JSON.stringify(currentUser));
  
  // Đóng modal
  const modal = document.getElementById("auth-modal");
  if (modal) modal.classList.remove("active");
  document.body.style.overflow = "";

  // Cập nhật Header
  updateAuthHeaderUI();
  
  // Toast thông báo đăng nhập (không dùng alert)
  if (window.showDataToast) {
    window.showDataToast(`Chào mừng ${user.fullname}! 🏦 Đăng nhập thành công`);
  } else {
    // fallback toast nội bộ
    showAuthToast(`🏦 Chào mừng ${user.fullname}! Đăng nhập E-Banking thành công.`, "success");
  }

  // Cá nhân hóa chatbot
  if (document.getElementById("chatbot-window")) {
    const chatbotMessages = document.getElementById("chatbot-messages");
    const accountNum = user.accountNumber || "PTB88998899";
    const welcomeMsg = `Xin chào Quý khách **${user.fullname}**! 🏦 Đã đăng nhập thành công. Số tài khoản: <code>${accountNum}</code>. Phát Tài Bot có thể hỗ trợ giao dịch, kiểm tra thẻ hay mở sổ tiết kiệm hôm nay?`;
    
    if (chatbotMessages) {
      const messageElement = document.createElement("div");
      messageElement.className = "message bot";
      messageElement.innerHTML = welcomeMsg
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
      chatbotMessages.appendChild(messageElement);
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
  }
}

function handleLogout() {
  if (confirm("Bạn có chắc chắn muốn đăng xuất không?")) {
    currentUser = null;
    localStorage.removeItem("organico_current_user");
    sessionStorage.removeItem("phattai_current_user");
    
    // Khôi phục Header về mặc định
    updateAuthHeaderUI();
    
    if (window.showDataToast) {
      window.showDataToast("Đã đăng xuất thành công. Hẹn gặp lại!");
    } else {
      showAuthToast("Đã đăng xuất tài khoản thành công.", "info");
    }
    
    // Làm mới trang sau 1.5s để reset các thông tin cá nhân
    setTimeout(() => window.location.reload(), 1500);
  }
}

// Toast nội bộ cho auth (dùng khi window.showDataToast chưa sẵn sàng)
function showAuthToast(message, type = "success") {
  const colors = { success: "#00c896", info: "#007bff", error: "#e74c3c" };
  let toast = document.getElementById("auth-toast-internal");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "auth-toast-internal";
    toast.style.cssText = `
      position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(80px);
      background: #0d1528; color: #fff; border-radius: 50px;
      padding: 12px 24px; font-size: 0.88rem; font-weight: 700;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3); z-index: 999999;
      transition: all 0.35s cubic-bezier(0.16,1,0.3,1); opacity: 0;
      display: flex; align-items: center; gap: 10px; min-width: 260px; justify-content: center;
    `;
    document.body.appendChild(toast);
  }
  const color = colors[type] || "#00c896";
  toast.style.borderLeft = `4px solid ${color}`;
  toast.innerHTML = `<span style="color:${color};font-size:1.1em;">●</span> ${message}`;
  toast.style.transform = "translateX(-50%) translateY(0)";
  toast.style.opacity = "1";
  clearTimeout(window._authToastTimer);
  window._authToastTimer = setTimeout(() => {
    toast.style.transform = "translateX(-50%) translateY(80px)";
    toast.style.opacity = "0";
  }, 3000);
}

// 5. CÁC HÀM TIỆN ÍCH HIỂN THỊ LỖI FORM
function openAuthModal(mode = "login") {
  const modal = document.getElementById("auth-modal");
  const tabLogin = document.getElementById("tab-login-btn");
  const tabRegister = document.getElementById("tab-register-btn");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  
  if (!modal) return;
  
  modal.classList.add("active");
  document.body.style.overflow = "hidden"; // khóa cuộn màn hình nền
  
  if (mode === "login") {
    if (tabLogin) tabLogin.click();
  } else {
    if (tabRegister) tabRegister.click();
  }
}

function showFieldError(inputId, errorText) {
  const errorSpan = document.getElementById(`${inputId}-error`);
  const inputElement = document.getElementById(inputId);
  
  if (errorSpan) {
    errorSpan.textContent = errorText;
  }
  if (inputElement) {
    inputElement.style.borderColor = "var(--color-danger)";
  }
}

function resetFormErrors() {
  const errorSpans = document.querySelectorAll(".error-msg");
  errorSpans.forEach(span => span.textContent = "");
  
  const inputs = document.querySelectorAll(".auth-form input");
  inputs.forEach(input => {
    input.style.borderColor = "";
  });
}

// 6. XUẤT RA TOÀN CỤC
window.getCurrentUser = () => currentUser;
window.openAuthModal = openAuthModal;

// Khởi chạy hệ thống Auth khi script được load
document.addEventListener("DOMContentLoaded", () => {
  initAuthSystem();
});