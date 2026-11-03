/**
 * OrganiCo - Main Application Orchestrator
 * Quản lý khởi tạo ứng dụng, đồng bộ theme sáng/tối, đăng ký các sự kiện DOM
 * và tích hợp các module chức năng.
 */

document.addEventListener("DOMContentLoaded", () => {
  // === 0. QUẢN LÝ MENU BẢNG NHỎ GÓC TRÁI (COMPACT TOP-LEFT DROPDOWN) ===
  const menuToggleBtn = document.getElementById("menu-toggle");
  const menuDropdownPanel = document.getElementById("menu-panel-dropdown");

  if (menuToggleBtn && menuDropdownPanel) {
    menuToggleBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      menuDropdownPanel.classList.toggle("active");
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".menu-dropdown-wrapper")) {
        menuDropdownPanel.classList.remove("active");
      }
    });
  }

  // === 1. QUẢN LÝ THEME SÁNG / TỐI (PERSISTENT THEME SWITCH) ===
  const themeToggleBtn = document.getElementById("theme-toggle");
  const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector("i") : null;
  
  // Khôi phục theme từ LocalStorage
  const savedTheme = localStorage.getItem("organico_theme") || "light";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    if (themeIcon) {
      themeIcon.className = "fa-solid fa-sun"; // Đổi icon sang mặt trời
    }
  } else {
    document.body.classList.remove("dark-mode");
    if (themeIcon) {
      themeIcon.className = "fa-solid fa-moon"; // Đổi icon sang mặt trăng
    }
  }
  
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const isDarkMode = document.body.classList.toggle("dark-mode");
      
      // Cập nhật icon và lưu LocalStorage
      if (isDarkMode) {
        localStorage.setItem("organico_theme", "dark");
        if (themeIcon) themeIcon.className = "fa-solid fa-sun";
      } else {
        localStorage.setItem("organico_theme", "light");
        if (themeIcon) themeIcon.className = "fa-solid fa-moon";
      }
    });
  }

  // === 2. QUẢN LÝ GIỎ HÀNG DRAWER EVENTS ===
  const cartToggleBtn = document.getElementById("cart-toggle");
  const cartCloseBtn = document.getElementById("cart-close");
  const cartOverlay = document.getElementById("cart-overlay");
  const checkoutBtn = document.getElementById("cart-checkout-btn");
  
  if (cartToggleBtn) {
    cartToggleBtn.addEventListener("click", () => {
      openCartDrawer();
    });
  }
  
  if (cartCloseBtn) {
    cartCloseBtn.addEventListener("click", () => {
      closeCartDrawer();
    });
  }
  
  if (cartOverlay) {
    cartOverlay.addEventListener("click", () => {
      closeCartDrawer();
    });
  }
  
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", () => {
      if (cart.length === 0) {
        alert("Giỏ hàng của bạn đang trống. Vui lòng thêm sản phẩm!");
        return;
      }
      
      alert("🎉 Đặt hàng thành công! Đơn hàng của bạn sẽ được nhân viên OrganiCo soạn thảo và giao đến trong vòng 2 giờ. Cảm ơn bạn đã ủng hộ thực phẩm sạch!");
      // Reset giỏ hàng
      cart = [];
      saveCartToStorage();
      updateCartUI();
      closeCartDrawer();
    });
  }

  // Khởi tạo nạp giỏ hàng từ bộ nhớ
  loadCartFromStorage();

  // === 3. KHỞI TẠO CATALOG & BỘ LỌC SẢN PHẨM ===
  // Render danh sách sản phẩm mẫu đầy đủ ban đầu
  renderProducts(PRODUCTS);
  
  // Tìm kiếm sản phẩm (Lọc theo từ khóa)
  const productSearchInput = document.getElementById("product-search");
  if (productSearchInput) {
    productSearchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase().trim();
      const activeFilterBtn = document.querySelector("#category-filters .filter-btn.active");
      const category = activeFilterBtn ? activeFilterBtn.getAttribute("data-category") : "all";
      
      filterCatalog(category, query);

      // Ghi nhận lịch sử tìm kiếm vào search_history.json và LocalStorage
      if (query.length >= 2) {
        clearTimeout(window.searchLogTimeout);
        window.searchLogTimeout = setTimeout(() => {
          const session = window.getCurrentUser ? window.getCurrentUser() : null;
          const username = session ? session.username : "anonymous";
          
          // Lưu LocalStorage
          try {
            const searches = JSON.parse(localStorage.getItem("phattai_search_history") || "[]");
            searches.push({ query: query, timestamp: new Date().toISOString(), user: username });
            localStorage.setItem("phattai_search_history", JSON.stringify(searches));
          } catch (e) {}

          // Lưu vào Backend API -> search_history.json
          fetch("http://localhost:8000/api/search/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: query, user: username, resultsCount: 1 })
          }).catch(() => {});
        }, 800);
      }
    });
  }
  
  // Lọc sản phẩm theo danh mục (Category Tabs)
  const categoryFiltersContainer = document.getElementById("category-filters");
  if (categoryFiltersContainer) {
    categoryFiltersContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;
      
      // Xóa class active ở các nút khác và thêm vào nút vừa click
      categoryFiltersContainer.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const category = btn.getAttribute("data-category");
      const searchQuery = productSearchInput ? productSearchInput.value.toLowerCase().trim() : "";
      
      filterCatalog(category, searchQuery);
    });
  }
  
  // Hàm chung thực hiện lọc catalog và hiển thị
  function filterCatalog(category, query) {
    let result = PRODUCTS;
    
    // Lọc theo danh mục
    if (category !== "all") {
      result = result.filter(product => product.category === category);
    }
    
    // Lọc theo từ khóa tìm kiếm
    if (query !== "") {
      result = result.filter(product => product.name.toLowerCase().includes(query));
    }
    
    renderProducts(result);
  }

  // === 4. KHỞI TẠO MEAL PLANNER & SHOPPING LIST ===
  // Nạp dữ liệu thực đơn từ bộ nhớ
  loadPlannerFromStorage();
  
  // Thêm mới thực phẩm vào danh sách mua sắm
  const plannerForm = document.getElementById("planner-form");
  if (plannerForm) {
    plannerForm.addEventListener("submit", (e) => {
      e.preventDefault();
      
      const nameInput = document.getElementById("planner-item-name");
      const qtyInput = document.getElementById("planner-item-qty");
      const categorySelect = document.getElementById("planner-item-category");
      const prioritySelect = document.getElementById("planner-item-priority");
      
      const name = nameInput.value.trim();
      const qty = qtyInput.value.trim();
      const category = categorySelect.value;
      const priority = prioritySelect.value;
      
      if (name && qty) {
        addPlannerItem(name, qty, category, priority);
        
        // Reset form và focus lại
        plannerForm.reset();
        nameInput.focus();
      }
    });
  }
  
  // Tìm kiếm trong planner
  const plannerSearchInput = document.getElementById("planner-search-input");
  if (plannerSearchInput) {
    plannerSearchInput.addEventListener("input", (e) => {
      const query = e.target.value;
      setPlannerSearchQuery(query);

      // Ghi nhận tìm kiếm vào data/search_history.json
      if (query.trim().length >= 2) {
        clearTimeout(window.plannerSearchLogTimeout);
        window.plannerSearchLogTimeout = setTimeout(() => {
          const session = window.getCurrentUser ? window.getCurrentUser() : null;
          const username = session ? session.username : "anonymous";
          fetch("http://localhost:8000/api/search/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: "Planner: " + query.trim(), user: username, resultsCount: 1 })
          }).catch(() => {});
        }, 800);
      }
    });
  }
  
  // Lọc planner theo trạng thái
  const plannerFiltersContainer = document.querySelector(".planner-filters-status");
  if (plannerFiltersContainer) {
    plannerFiltersContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".status-filter-btn");
      if (!btn) return;
      
      plannerFiltersContainer.querySelectorAll(".status-filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      const status = btn.getAttribute("data-status");
      setPlannerStatusFilter(status);
    });
  }
  
  // Cấu hình sự kiện đóng mở, lưu modal chỉnh sửa
  const editModal = document.getElementById("edit-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalOverlayClose = document.getElementById("modal-overlay-close");
  const editCancelBtn = document.getElementById("edit-cancel-btn");
  const editSaveBtn = document.getElementById("edit-save-btn");
  
  const closeModalFunc = () => {
    closeEditPlannerModal();
  };
  
  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeModalFunc);
  if (modalOverlayClose) modalOverlayClose.addEventListener("click", closeModalFunc);
  if (editCancelBtn) editCancelBtn.addEventListener("click", closeModalFunc);
  
  if (editSaveBtn) {
    editSaveBtn.addEventListener("click", () => {
      saveEditPlannerItem();
    });
  }

  // === 5. KHỞI TẠO FETCH API (WEATHER & HEALTH QUOTES) ===
  loadAllInfoWidgets();

  // === 6. KHỞI TẠO AI CHATBOT EVENTS ===
  initChatbotEvents();

  // === 8. HỆ THỐNG THÔNG BÁO LƯU TRỮ TRỰC TIẾP VÀO DATA/ ===
  window.showDataToast = function(message) {
    let toast = document.getElementById("phattai-data-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "phattai-data-toast";
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 24px;
        background: #0d1528;
        color: #00c896;
        border: 1px solid #00c896;
        padding: 12px 20px;
        border-radius: 50px;
        font-size: 0.88rem;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(0, 200, 150, 0.25);
        z-index: 99999;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        transform: translateY(100px);
        opacity: 0;
        pointer-events: none;
      `;
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<i class="fa-solid fa-database" style="color: #00c896;"></i> <span>${message}</span>`;
    toast.style.transform = "translateY(0)";
    toast.style.opacity = "1";
    
    clearTimeout(window.dataToastTimeout);
    window.dataToastTimeout = setTimeout(() => {
      toast.style.transform = "translateY(100px)";
      toast.style.opacity = "0";
    }, 3200);
  };

  // === 9. TIẾP NHẬN ĐĂNG KÝ 7 CHƯƠNG TRÌNH KHÁM PHÁ & LƯU VÀO data/consultations.json ===
  window.submitConsultation = async function(e, form, progId, progName) {
    if (e && e.preventDefault) e.preventDefault();
    const inputs = form.querySelectorAll("input, select, textarea");
    const fullname = form.querySelector("input[type='text']")?.value || "";
    const phone = form.querySelector("input[type='tel']")?.value || "";
    const pkg = form.querySelector("select")?.value || "";
    const budget = form.querySelector("input[type='number']")?.value || "";

    try {
      const res = await fetch("http://localhost:8000/api/consultations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          program_id: progId,
          program_name: progName,
          fullname: fullname,
          phone: phone,
          interest_pkg: pkg,
          budget: budget
        })
      });
      if (res.ok) {
        if (window.showDataToast) window.showDataToast("Đã lưu đăng ký vào data/consultations.json");
        alert(`🎉 Tiếp nhận thành công! Hồ sơ đăng ký chương trình [${progName}] của Quý khách đã được lưu thẳng vào cơ sở dữ liệu data/consultations.json.`);
        form.reset();
        return;
      }
    } catch (err) {
      console.warn("Lỗi gọi API consultations:", err);
    }

    alert(`🎉 Tiếp nhận thành công! Chuyên viên PHÁT TÀI BANK sẽ liên hệ tư vấn [${progName}] sớm nhất qua SĐT ${phone}.`);
    form.reset();
  };
});
