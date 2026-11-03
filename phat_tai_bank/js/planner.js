/**
 * PHÁT TÀI BANK - Sổ Nhắc Hạn Thanh Toán & Quản Lý Chi Tiêu (CRUD)
 * File: js/planner.js
 *
 * Lưu trữ trực tiếp vào máy chủ API: data/planner.json (Không phụ thuộc LocalStorage)
 */

const PLANNER_API_BASE = "http://localhost:8000";

let plannerItems = [];
let currentStatusFilter = 'all'; // 'all', 'pending', 'completed'
let currentSearchQuery = '';

// Dữ liệu mẫu ban đầu về quản lý chi tiêu ngân hàng
const INITIAL_PLANNER_ITEMS = [
  {
    id: "plan-1",
    name: "Thanh toán hóa đơn điện & nước tháng này",
    qty: "850.000 VNĐ",
    category: "Điện Nước",
    priority: "high",
    completed: false,
    createdAt: Date.now() - 72000 * 2
  },
  {
    id: "plan-2",
    name: "Tất toán dư nợ thẻ tín dụng Visa",
    qty: "3.500.000 VNĐ",
    category: "Thẻ Tín Dụng",
    priority: "high",
    completed: false,
    createdAt: Date.now() - 36000
  },
  {
    id: "plan-3",
    name: "Đóng phí bảo hiểm nhân thọ quý 4",
    qty: "5.000.000 VNĐ",
    category: "Bảo Hiểm",
    priority: "medium",
    completed: true,
    createdAt: Date.now() - 560000
  },
  {
    id: "plan-4",
    name: "Trích tiền gửi tiết kiệm tích lũy định kỳ",
    qty: "2.000.000 VNĐ",
    category: "Tiết Kiệm",
    priority: "low",
    completed: true,
    createdAt: Date.now() - 980000
  }
];

// Nạp dữ liệu sổ chi tiêu trực tiếp từ tệp data/planner.json
async function loadPlannerFromStorage() {
  try {
    const res = await fetch(`${PLANNER_API_BASE}/api/planner`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        plannerItems = data;
        renderPlannerList();
        return;
      }
    }
  } catch (e) {
    console.warn("Chưa kết nối API data/planner.json, sử dụng danh sách khởi tạo:", e);
  }

  plannerItems = [...INITIAL_PLANNER_ITEMS];
  renderPlannerList();
}

function renderPlannerList() {
  const listContainer = document.getElementById("planner-list");
  if (!listContainer) return;
  
  listContainer.innerHTML = "";
  
  let filteredItems = plannerItems.filter(item => {
    if (currentStatusFilter === 'pending') return !item.completed;
    if (currentStatusFilter === 'completed') return item.completed;
    return true;
  });
  
  if (currentSearchQuery.trim() !== "") {
    const query = currentSearchQuery.toLowerCase();
    filteredItems = filteredItems.filter(item => 
      item.name.toLowerCase().includes(query) || 
      item.category.toLowerCase().includes(query)
    );
  }
  
  filteredItems.sort((a, b) => {
    if (a.completed !== b.completed) {
      return a.completed ? 1 : -1;
    }
    const priorityWeight = { high: 3, medium: 2, low: 1 };
    if (priorityWeight[a.priority] !== priorityWeight[b.priority]) {
      return priorityWeight[b.priority] - priorityWeight[a.priority];
    }
    return b.createdAt - a.createdAt;
  });
  
  if (filteredItems.length === 0) {
    listContainer.innerHTML = `
      <div class="empty-state" style="text-align: center; padding: 40px 20px;">
        <i class="fa-solid fa-clipboard-check" style="font-size: 2.2rem; color: var(--text-muted); margin-bottom: 10px; display: block;"></i>
        <p style="font-weight: 600;">Sổ nhắc hạn thanh toán trống.</p>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px;">Thêm các khoản hóa đơn, tiền vay hoặc tiết kiệm để lưu vào data/planner.json!</p>
      </div>
    `;
    return;
  }
  
  filteredItems.forEach(item => {
    const itemElement = document.createElement("div");
    itemElement.className = `planner-item ${item.completed ? 'completed' : ''}`;
    itemElement.setAttribute("data-id", item.id);
    
    const priorityText = item.priority === 'high' ? 'Khẩn cấp' : item.priority === 'medium' ? 'Bình thường' : 'Kỳ sau';
    
    itemElement.innerHTML = `
      <div class="item-left">
        <div class="checkbox-custom ${item.completed ? 'checked' : ''}" onclick="togglePlannerItemStatus('${item.id}')" role="checkbox" aria-checked="${item.completed}">
          <i class="fa-solid fa-check"></i>
        </div>
        <div class="item-details" onclick="togglePlannerItemStatus('${item.id}')">
          <div class="item-name">${item.name}</div>
          <div class="item-meta">
            <span>🏷️ ${item.category}</span>
            <span class="meta-dot"></span>
            <span>💰 Số tiền: <strong>${item.qty}</strong></span>
          </div>
        </div>
      </div>
      <div class="item-right">
        <span class="priority-badge ${item.priority}">${priorityText}</span>
        <div class="item-actions">
          <button class="edit-btn" onclick="openEditPlannerModal('${item.id}')" title="Chỉnh sửa"><i class="fa-solid fa-pen-to-square"></i></button>
          <button class="delete-btn" onclick="deletePlannerItem('${item.id}')" title="Xóa"><i class="fa-solid fa-trash-can"></i></button>
        </div>
      </div>
    `;
    
    listContainer.appendChild(itemElement);
  });
}

// Thêm khoản chi tiêu mới & Lưu thẳng vào data/planner.json
async function addPlannerItem(name, qty, category, priority) {
  const newItem = {
    id: "plan-" + Date.now(),
    name: name,
    qty: qty,
    category: category,
    priority: priority,
    completed: false,
    createdAt: Date.now()
  };
  
  plannerItems.unshift(newItem);
  renderPlannerList();

  try {
    const res = await fetch(`${PLANNER_API_BASE}/api/planner`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newItem)
    });
    if (res.ok) {
      if (window.showDataToast) window.showDataToast("Đã lưu hóa đơn vào data/planner.json");
    }
  } catch (e) {
    console.warn("Lỗi đồng bộ API data/planner.json:", e);
  }
}

// Bật tắt trạng thái hoàn thành & Cập nhật thẳng vào data/planner.json
async function togglePlannerItemStatus(id) {
  const item = plannerItems.find(item => item.id === id);
  if (item) {
    item.completed = !item.completed;
    renderPlannerList();

    try {
      await fetch(`${PLANNER_API_BASE}/api/planner/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed: item.completed })
      });
      if (window.showDataToast) window.showDataToast(`Cập nhật trạng thái vào data/planner.json`);
    } catch (e) {
      console.warn("Lỗi cập nhật API planner:", e);
    }
  }
}

function openEditPlannerModal(id) {
  const item = plannerItems.find(item => item.id === id);
  if (!item) return;
  
  const idEl = document.getElementById("edit-item-id");
  const nameEl = document.getElementById("edit-item-name");
  const qtyEl = document.getElementById("edit-item-qty");
  const catEl = document.getElementById("edit-item-category");
  const priEl = document.getElementById("edit-item-priority");

  if (idEl) idEl.value = item.id;
  if (nameEl) nameEl.value = item.name;
  if (qtyEl) qtyEl.value = item.qty;
  if (catEl) catEl.value = item.category;
  if (priEl) priEl.value = item.priority;
  
  const modal = document.getElementById("edit-modal");
  if (modal) modal.classList.add("active");
}

function closeEditPlannerModal() {
  const modal = document.getElementById("edit-modal");
  if (modal) modal.classList.remove("active");
}

// Sửa khoản chi tiêu & Lưu thẳng vào data/planner.json
async function saveEditPlannerItem() {
  const id = document.getElementById("edit-item-id")?.value;
  const name = document.getElementById("edit-item-name")?.value.trim();
  const qty = document.getElementById("edit-item-qty")?.value.trim();
  const category = document.getElementById("edit-item-category")?.value;
  const priority = document.getElementById("edit-item-priority")?.value;
  
  if (!name || !qty) {
    alert("Vui lòng điền đầy đủ tên khoản thanh toán và số tiền.");
    return;
  }
  
  const item = plannerItems.find(item => item.id === id);
  if (item) {
    item.name = name;
    item.qty = qty;
    item.category = category;
    item.priority = priority;
    
    renderPlannerList();
    closeEditPlannerModal();

    try {
      await fetch(`${PLANNER_API_BASE}/api/planner/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, qty, category, priority })
      });
      if (window.showDataToast) window.showDataToast("Đã cập nhật thay đổi vào data/planner.json");
    } catch (e) {
      console.warn("Lỗi lưu sửa planner:", e);
    }
  }
}

// Xóa khoản chi tiêu & Xóa trực tiếp khỏi data/planner.json
async function deletePlannerItem(id) {
  const itemElement = document.querySelector(`.planner-item[data-id="${id}"]`);
  if (itemElement) {
    itemElement.style.opacity = "0";
    itemElement.style.transform = "translateX(20px)";
    itemElement.style.transition = "all 0.3s ease";
    
    setTimeout(() => {
      plannerItems = plannerItems.filter(item => item.id !== id);
      renderPlannerList();
    }, 300);
  } else {
    plannerItems = plannerItems.filter(item => item.id !== id);
    renderPlannerList();
  }

  try {
    await fetch(`${PLANNER_API_BASE}/api/planner/${id}`, {
      method: "DELETE"
    });
    if (window.showDataToast) window.showDataToast("Đã xóa khỏi data/planner.json");
  } catch (e) {
    console.warn("Lỗi xóa planner:", e);
  }
}

window.loadPlannerFromStorage = loadPlannerFromStorage;
window.addPlannerItem = addPlannerItem;
window.togglePlannerItemStatus = togglePlannerItemStatus;
window.openEditPlannerModal = openEditPlannerModal;
window.closeEditPlannerModal = closeEditPlannerModal;
window.saveEditPlannerItem = saveEditPlannerItem;
window.deletePlannerItem = deletePlannerItem;
window.setPlannerStatusFilter = (filter) => {
  currentStatusFilter = filter;
  renderPlannerList();
};
window.setPlannerSearchQuery = (query) => {
  currentSearchQuery = query;
  renderPlannerList();
};
