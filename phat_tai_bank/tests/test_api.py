"""
PHÁT TÀI BANK - Automated Test Suite
Chạy kiểm thử toàn diện hệ thống REST API & Data Persistence
"""

import unittest
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://localhost:8000"

def make_request(path, method="GET", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))

class TestPhatTaiBankAPI(unittest.TestCase):

    def test_01_root_endpoint(self):
        code, data = make_request("/")
        self.assertEqual(code, 200)
        self.assertEqual(data.get("status"), "online")
        self.assertEqual(data.get("bank"), "PHÁT TÀI BANK")
        self.assertIn("/api/chat", data.get("endpoints", []))

    def test_02_chat_intent_create_account(self):
        payload = {"message": "Các bước tạo tài khoản như thế nào?", "user_id": "test_user_01"}
        code, data = make_request("/api/chat", method="POST", data=payload)
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "create_account")
        self.assertGreaterEqual(data.get("confidence_main", 0), 0.9)
        self.assertIn("data/chat_history.json", data.get("saved_to", ""))
        self.assertIn("CÁC BƯỚC", data.get("reply", ""))

    def test_03_chat_intent_savings(self):
        payload = {"message": "Tôi muốn gửi tiết kiệm lãi suất bao nhiêu?", "user_id": "test_user_02"}
        code, data = make_request("/api/chat", method="POST", data=payload)
        self.assertEqual(code, 200)
        self.assertIn(data.get("intent"), ["savings_account", "interest_rates"])
        self.assertGreaterEqual(data.get("confidence_main", 0), 0.9)

    def test_04_chat_intent_card_blocked(self):
        payload = {"message": "Thẻ bị khóa làm sao mở khóa lại?", "user_id": "test_user_03"}
        code, data = make_request("/api/chat", method="POST", data=payload)
        self.assertEqual(code, 200)
        self.assertEqual(data.get("intent"), "card_blocked")
        self.assertIn("MỞ KHÓA THẺ", data.get("reply", ""))

    def test_05_customer_registration_and_login(self):
        unique_user = f"user_{int(time.time())}"
        reg_payload = {
            "username": unique_user,
            "password": "Password123!",
            "fullname": "Kiểm Thử Viên",
            "phone": "0988776655",
            "address": "TP.HCM"
        }
        code, reg_resp = make_request("/api/customers/register", method="POST", data=reg_payload)
        self.assertEqual(code, 200)
        self.assertEqual(reg_resp.get("status"), "success")
        self.assertTrue(reg_resp["customer"]["accountNumber"].startswith("PTB"))

        # Test login with that user
        login_payload = {"username": unique_user, "password": "Password123!"}
        code, log_resp = make_request("/api/customers/login", method="POST", data=login_payload)
        self.assertEqual(code, 200)
        self.assertEqual(log_resp.get("status"), "success")
        self.assertEqual(log_resp["user"]["username"], unique_user)

    def test_06_planner_crud(self):
        # 1. Create
        item = {
            "name": f"Hóa đơn test tự động {int(time.time())}",
            "qty": "500.000 VNĐ",
            "category": "Điện Nước",
            "priority": "high",
            "completed": False
        }
        code, resp = make_request("/api/planner", method="POST", data=item)
        self.assertEqual(code, 200)
        self.assertEqual(resp.get("status"), "success")
        item_id = resp["item"]["id"]

        # 2. Update
        code, update_resp = make_request(f"/api/planner/{item_id}", method="PUT", data={"completed": True})
        self.assertEqual(code, 200)
        self.assertTrue(update_resp["item"]["completed"])

        # 3. Read
        code, items = make_request("/api/planner")
        self.assertEqual(code, 200)
        ids = [i["id"] for i in items]
        self.assertIn(item_id, ids)

        # 4. Delete
        code, del_resp = make_request(f"/api/planner/{item_id}", method="DELETE")
        self.assertEqual(code, 200)
        self.assertEqual(del_resp.get("status"), "deleted")

    def test_07_cart_sync(self):
        cart_payload = {
            "user_id": "test_cart_user",
            "items": [
                {"id": 1, "name": "Thẻ Thanh Toán Visa Classic", "price": 0, "quantity": 1},
                {"id": 2, "name": "Gói Tiết Kiệm Linh Hoạt", "price": 1000000, "quantity": 2}
            ]
        }
        code, resp = make_request("/api/cart", method="POST", data=cart_payload)
        self.assertEqual(code, 200)
        self.assertEqual(resp.get("status"), "saved")

        # Get cart
        code, cart_items = make_request("/api/cart?user_id=test_cart_user")
        self.assertEqual(code, 200)
        self.assertEqual(len(cart_items), 2)

    def test_08_consultation_registration(self):
        c_payload = {
            "program_id": "CT1",
            "program_name": "Đầu Tư Cổ Phiếu & Quỹ Mở",
            "fullname": "Nguyễn Thị Thử Nghiệm",
            "phone": "0912999888",
            "interest_pkg": "Gói Chuyên Gia",
            "budget": "100000000"
        }
        code, resp = make_request("/api/consultations", method="POST", data=c_payload)
        self.assertEqual(code, 200)
        self.assertEqual(resp.get("status"), "success")
        self.assertIn("data/consultations.json", resp.get("saved_to", ""))

    def test_09_search_log(self):
        s_payload = {"query": "thẻ tín dụng hoàn tiền", "user": "test_search_user", "resultsCount": 1}
        code, resp = make_request("/api/search/log", method="POST", data=s_payload)
        self.assertEqual(code, 200)
        self.assertEqual(resp.get("status"), "logged")

    def test_10_system_stats(self):
        code, stats = make_request("/api/stats")
        self.assertEqual(code, 200)
        self.assertGreater(stats.get("total_chats", 0), 0)
        self.assertGreater(stats.get("total_customers", 0), 0)
        self.assertGreater(stats.get("kb_intents_covered", 0), 40)
        self.assertGreaterEqual(stats["model_mlp"]["accuracy"], 0.88)
        self.assertGreaterEqual(stats["model_lr"]["accuracy"], 0.88)

if __name__ == "__main__":
    unittest.main()
