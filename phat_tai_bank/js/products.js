/**
 * PHÁT TÀI BANK - Dịch Vụ Ngân Hàng & Giỏ Đăng Ký Trực Tuyến
 * Quản lý danh mục 6 sản phẩm tài chính - ngân hàng, giỏ đăng ký và lưu trữ LocalStorage.
 */

// 1. DANH MỤC DỊCH VỤ NGÂN HÀNG PHÁT TÀI BANK
const PRODUCTS = [
  {
    id: 1,
    name: "Thẻ Thanh Toán Visa Classic",
    category: "card",
    price: 0,
    unit: "Miễn phí phát hành",
    image: "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&q=80&w=400",
    rating: 4.9,
    reviews: 1420,
    tag: "Phổ Biến Nhất",
    desc: "Thẻ thanh toán quốc tế Visa chấp nhận tại 50+ triệu điểm POS toàn cầu, bảo mật chip EMV không chạm, hoàn tiền 0.5% mọi giao dịch."
  },
  {
    id: 2,
    name: "Gói Tiết Kiệm Linh Hoạt",
    category: "savings",
    price: 1000000,
    unit: "Tối thiểu 1 triệu VNĐ",
    image: "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&q=80&w=400",
    rating: 5.0,
    reviews: 980,
    tag: "Lãi Suất 6.8%",
    desc: "Gửi tiết kiệm trực tuyến kỳ hạn linh hoạt 1-36 tháng với lãi suất ưu đãi lên tới 6.8%/năm, rút gốc trước hạn vẫn hưởng lãi không kỳ hạn."
  },
  {
    id: 3,
    name: "Vay Tín Chấp Tiêu Dùng Online",
    category: "loan",
    price: 10000000,
    unit: "Hạn mức tới 500 triệu",
    image: "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&q=80&w=400",
    rating: 4.8,
    reviews: 750,
    tag: "Duyệt 24H",
    desc: "Vay tiêu dùng không cần thế chấp tài sản, giải ngân siêu tốc qua tài khoản trong vòng 24 giờ, lãi suất ưu đãi chỉ từ 0.9%/tháng."
  },
  {
    id: 4,
    name: "Tài Khoản E-Banking Pro Số Đẹp",
    category: "account",
    price: 0,
    unit: "Miễn phí trọn đời",
    image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&q=80&w=400",
    rating: 4.9,
    reviews: 2150,
    tag: "Miễn Phí 24/7",
    desc: "Mở tài khoản số đẹp theo ngày sinh, số điện thoại hoặc phong thủy. Miễn phí chuyển khoản 24/7 Napas, thanh toán hơn 50 loại hóa đơn."
  },
  {
    id: 5,
    name: "Thẻ Tín Dụng Mastercard Gold",
    category: "card",
    price: 180000,
    unit: "Hạn mức tới 200 triệu",
    image: "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&q=80&w=400",
    rating: 4.9,
    reviews: 640,
    tag: "Hạng Vàng",
    desc: "Đặc quyền phòng chờ sân bay hạng thương gia, bảo hiểm du lịch toàn cầu tới 1 tỷ VNĐ, tích điểm đổi quà và trả góp 0% lãi suất."
  },
  {
    id: 6,
    name: "Gói Vay Mua Nhà An Cư",
    category: "loan",
    price: 100000000,
    unit: "Tài trợ tới 85% giá trị",
    image: "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&q=80&w=400",
    rating: 4.7,
    reviews: 320,
    tag: "Lãi Suất 7.5%",
    desc: "Thời hạn vay linh hoạt lên tới 30 năm, ân hạn nợ gốc 24 tháng đầu, giải ngân theo tiến độ hợp đồng mua bán bất động sản."
  }
];

let cart = [];

function formatCurrency(amount) {
  if (amount === 0) return "Miễn phí";
  return amount.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
}

// 2. HIỂN THỊ DANH SÁCH DỊCH VỤ TRÊN CATALOG
function renderProducts(filteredProducts = PRODUCTS) {
  const gridContainer = document.getElementById("products-grid");
  if (!gridContainer) return;
  
  gridContainer.innerHTML = "";
  
  if (filteredProducts.length === 0) {
    gridContainer.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
        <i class="fa-solid fa-building-columns" style="font-size: 2.5rem; color: var(--text-muted); margin-bottom: 15px; display: block;"></i>
        <p style="color: var(--text-muted);">Không tìm thấy dịch vụ tài chính nào phù hợp.</p>
      </div>
    `;
    return;
  }
  
  filteredProducts.forEach(product => {
    const card = document.createElement("article");
    card.className = "product-card animate-fade";
    
    const tagHtml = product.tag ? `<span class="badge badge-success tag" style="background: #007bff; color: #fff;">${product.tag}</span>` : '';
    
    let categoryName = "Thẻ Ngân Hàng";
    if (product.category === "savings") categoryName = "Tiết Kiệm";
    else if (product.category === "loan") categoryName = "Vay Vốn";
    else if (product.category === "account") categoryName = "E-Banking";
    
    card.innerHTML = `
      <div class="product-img" style="position: relative; overflow: hidden; height: 180px;">
        ${tagHtml}
        <img src="${product.image}" alt="${product.name}" loading="lazy" style="width: 100%; height: 100%; object-fit: cover;">
      </div>
      <div class="product-info" style="padding: 16px;">
        <span class="category" style="color: #007bff; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">${categoryName}</span>
        <h3 style="font-size: 1.05rem; margin: 6px 0; font-weight: 700;">${product.name}</h3>
        <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 8px;">${product.desc}</p>
        <div class="rating" style="color: #ffb800; font-size: 0.85rem; margin-bottom: 8px;">
          <i class="fa-solid fa-star"></i> ${product.rating.toFixed(1)}
          <span style="color: var(--text-muted);">(${product.reviews} lượt đăng ký)</span>
        </div>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">Đặc quyền: <strong>${product.unit}</strong></p>
        <div class="price-action" style="display: flex; align-items: center; justify-content: space-between;">
          <span class="price" style="color: #007bff; font-weight: 800; font-size: 1.05rem;">${formatCurrency(product.price)}</span>
          <button class="btn-add-cart" data-id="${product.id}" title="Đăng ký dịch vụ này" aria-label="Đăng ký ${product.name}" style="background: #007bff; color: #fff; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 600; cursor: pointer;">
            <i class="fa-solid fa-plus"></i> Đăng ký
          </button>
        </div>
      </div>
    `;
    
    gridContainer.appendChild(card);
  });
  
  const addButtons = gridContainer.querySelectorAll(".btn-add-cart");
  addButtons.forEach(button => {
    button.addEventListener("click", () => {
      const productId = parseInt(button.getAttribute("data-id"));
      addToCart(productId);
    });
  });
}

// 3. QUẢN LÝ LOGIC GIỎ ĐĂNG KÝ DỊCH VỤ (CART DRAWER)
function ensureCartDrawerExists() {
  if (document.getElementById("cart-drawer")) return;

  const wrapper = document.createElement("div");
  wrapper.id = "cart-drawer-injected-wrapper";
  wrapper.innerHTML = `
    <div class="cart-overlay" id="cart-overlay"></div>
    <aside class="cart-drawer" id="cart-drawer" aria-label="Shopping Cart">
      <div class="cart-header">
        <h2>Giỏ Đăng Ký Dịch Vụ</h2>
        <button class="close-cart-btn" id="cart-close" title="Đóng" aria-label="Close Cart">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      
      <div class="cart-items-list" id="cart-items-container"></div>
      
      <div class="cart-footer">
        <div class="cart-summary-row" style="display: flex; justify-content: space-between; margin-bottom: 12px; font-weight: 700;">
          <span>Tổng phí dịch vụ:</span>
          <span class="total-price" id="cart-total-price" style="color: #007bff;">0đ</span>
        </div>
        <button class="btn btn-primary btn-checkout" id="cart-checkout-btn" style="width: 100%; background: #007bff; color: #fff; padding: 12px; border: none; border-radius: 10px; font-weight: 700; cursor: pointer;">
          <i class="fa-solid fa-circle-check"></i> Xác Nhận Mở Dịch Vụ
        </button>
      </div>
    </aside>
  `;
  document.body.appendChild(wrapper);

  document.getElementById("cart-close")?.addEventListener("click", closeCartDrawer);
  document.getElementById("cart-overlay")?.addEventListener("click", closeCartDrawer);
  document.getElementById("cart-checkout-btn")?.addEventListener("click", () => {
    if (cart.length === 0) {
      if (window.showDataToast) window.showDataToast("⚠️ Giỏ đăng ký dịch vụ đang trống!");
      else alert("Giỏ đăng ký dịch vụ đang trống. Quý khách vui lòng chọn dịch vụ!");
      return;
    }
    saveCartToStorage();
    if (window.showDataToast) window.showDataToast(`🎉 Đã xác nhận đăng ký ${cart.length} dịch vụ — lưu vào data/cart.json`);
    // Hiển thị thông báo nhỏ thay vì alert
    const msg = document.createElement("div");
    msg.style.cssText = `position:fixed;top:80px;left:50%;transform:translateX(-50%);background:#0d1528;color:#00c896;border:1px solid #00c896;padding:14px 28px;border-radius:14px;font-weight:700;z-index:999999;box-shadow:0 8px 24px rgba(0,200,150,0.25);text-align:center;font-size:0.95rem;`;
    msg.innerHTML = `✅ Đăng ký thành công ${cart.length} dịch vụ tài chính!<br><small style="font-weight:400;color:#aaa;">Chuyên viên PHÁT TÀI BANK sẽ liên hệ trong 15 phút để kích hoạt.</small>`;
    document.body.appendChild(msg);
    setTimeout(() => msg.remove(), 4000);
    cart = [];
    saveCartToStorage();
    updateCartUI();
    closeCartDrawer();
  });
}

async function loadCartFromStorage() {
  ensureCartDrawerExists();
  const sessionUser = (window.getCurrentUser) ? window.getCurrentUser() : null;
  const userId = sessionUser ? sessionUser.username : "guest";

  try {
    const res = await fetch(`http://localhost:8000/api/cart?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data)) {
        cart = data;
        updateCartUI();
        return;
      }
    }
  } catch (e) {
    console.warn("Chưa kết nối API data/cart.json:", e);
  }

  cart = [];
  updateCartUI();
}

async function saveCartToStorage() {
  const sessionUser = (window.getCurrentUser) ? window.getCurrentUser() : null;
  const userId = sessionUser ? sessionUser.username : "guest";

  try {
    const res = await fetch("http://localhost:8000/api/cart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, items: cart })
    });
    if (res.ok) {
      if (window.showDataToast) window.showDataToast("Đã lưu giỏ dịch vụ vào data/cart.json");
    }
  } catch (e) {
    console.warn("Lỗi lưu data/cart.json:", e);
  }
}

function addToCart(productOrId, name, price, image) {
  ensureCartDrawerExists();

  let itemToAdd = null;

  if (typeof productOrId === "object" && productOrId !== null) {
    itemToAdd = productOrId;
  } else if (typeof productOrId === "number" && !name) {
    const product = PRODUCTS.find(p => p.id === productOrId);
    if (product) {
      itemToAdd = {
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image
      };
    }
  } else if (productOrId) {
    itemToAdd = {
      id: productOrId,
      name: name || "Dịch vụ ngân hàng",
      price: price || 0,
      image: image || ""
    };
  }

  if (!itemToAdd || !itemToAdd.name) return;

  const existingItem = cart.find(item => item.id === itemToAdd.id || item.name === itemToAdd.name);
  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({
      id: itemToAdd.id,
      name: itemToAdd.name,
      price: itemToAdd.price,
      image: itemToAdd.image,
      quantity: 1
    });
  }
  
  saveCartToStorage();
  updateCartUI();
  
  const badge = document.getElementById("cart-badge");
  if (badge) {
    badge.classList.remove("pulse");
    void badge.offsetWidth;
    badge.classList.add("pulse");
  }
  
  openCartDrawer();
}

function updateCartQty(productId, amount) {
  const item = cart.find(item => item.id === productId || item.id == productId);
  if (!item) return;
  
  item.quantity += amount;
  if (item.quantity <= 0) {
    cart = cart.filter(item => item.id !== productId && item.id != productId);
  }
  
  saveCartToStorage();
  updateCartUI();
}

function removeCartItem(productId) {
  cart = cart.filter(item => item.id !== productId && item.id != productId);
  saveCartToStorage();
  updateCartUI();
}

function getCartTotal() {
  return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
}

function getCartCount() {
  return cart.reduce((count, item) => count + item.quantity, 0);
}

function updateCartUI() {
  ensureCartDrawerExists();
  const cartContainer = document.getElementById("cart-items-container");
  const cartBadge = document.getElementById("cart-badge");
  const cartTotal = document.getElementById("cart-total-price");
  
  if (!cartContainer) return;
  
  const count = getCartCount();
  if (cartBadge) {
    cartBadge.textContent = count;
  }
  
  if (cartTotal) {
    cartTotal.textContent = formatCurrency(getCartTotal());
  }
  
  cartContainer.innerHTML = "";
  
  if (cart.length === 0) {
    cartContainer.innerHTML = `
      <div class="empty-cart" style="text-align: center; padding: 40px 20px;">
        <i class="fa-solid fa-credit-card" style="font-size: 2.5rem; color: var(--text-muted); margin-bottom: 12px; display: block;"></i>
        <p style="font-weight: 600;">Giỏ đăng ký dịch vụ trống.</p>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px;">Quý khách vui lòng chọn gói thẻ, tiết kiệm hoặc vay trực tuyến phù hợp!</p>
      </div>
    `;
    return;
  }
  
  cart.forEach(item => {
    const itemElement = document.createElement("div");
    itemElement.className = "cart-item animate-fade";
    
    itemElement.innerHTML = `
      <img src="${item.image}" alt="${item.name}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;">
      <div class="item-info" style="flex: 1; margin: 0 10px;">
        <h4 style="font-size: 0.88rem; margin: 0 0 4px 0;">${item.name}</h4>
        <span class="price" style="color: #007bff; font-weight: 700; font-size: 0.82rem;">${formatCurrency(item.price)}</span>
      </div>
      <div class="quantity-selector">
        <button class="btn-qty-minus" data-id="${item.id}" aria-label="Giảm"><i class="fa-solid fa-minus"></i></button>
        <span style="font-size: 0.85rem; font-weight: 700;">${item.quantity}</span>
        <button class="btn-qty-plus" data-id="${item.id}" aria-label="Tăng"><i class="fa-solid fa-plus"></i></button>
      </div>
      <button class="remove-item-btn" data-id="${item.id}" title="Hủy" style="background:none; border:none; color:#ff4757; cursor:pointer; margin-left: 8px;"><i class="fa-solid fa-trash-can"></i></button>
    `;
    
    cartContainer.appendChild(itemElement);
  });
  
  cartContainer.querySelectorAll(".btn-qty-minus").forEach(btn => {
    btn.addEventListener("click", () => updateCartQty(btn.getAttribute("data-id"), -1));
  });
  
  cartContainer.querySelectorAll(".btn-qty-plus").forEach(btn => {
    btn.addEventListener("click", () => updateCartQty(btn.getAttribute("data-id"), 1));
  });
  
  cartContainer.querySelectorAll(".remove-item-btn").forEach(btn => {
    btn.addEventListener("click", () => removeCartItem(btn.getAttribute("data-id")));
  });
}

function openCartDrawer() {
  ensureCartDrawerExists();
  const drawer = document.getElementById("cart-drawer");
  const overlay = document.getElementById("cart-overlay");
  if (drawer && overlay) {
    drawer.classList.add("active");
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }
}

function closeCartDrawer() {
  const drawer = document.getElementById("cart-drawer");
  const overlay = document.getElementById("cart-overlay");
  if (drawer && overlay) {
    drawer.classList.remove("active");
    overlay.classList.remove("active");
    document.body.style.overflow = "";
  }
}

// Bắt sự kiện chọn thêm dịch vụ ở các trang phụ
document.addEventListener("click", (e) => {
  const addBtn = e.target.closest(".mini-add-btn");
  if (addBtn) {
    e.preventDefault();
    e.stopPropagation();
    const card = addBtn.closest(".mini-product-card");
    if (card) {
      const name = card.querySelector("h4")?.textContent?.trim() || "Dịch vụ tài chính";
      const img = card.querySelector(".mini-img img")?.getAttribute("src") || "";
      const priceText = card.querySelector(".mini-price")?.textContent || "0";
      const price = parseInt(priceText.replace(/\D/g, ""), 10) || 0;
      
      addToCart({
        id: "serv_" + name.replace(/\s+/g, "_"),
        name: name,
        price: price,
        image: img
      });
    }
  }
});

window.PRODUCTS = PRODUCTS;
window.renderProducts = renderProducts;
window.loadCartFromStorage = loadCartFromStorage;
window.addToCart = addToCart;
window.openCartDrawer = openCartDrawer;
window.closeCartDrawer = closeCartDrawer;
