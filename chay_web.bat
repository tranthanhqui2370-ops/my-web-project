@echo off
chcp 65001 >nul
title KHỞI ĐỘNG PHÁT TÀI BANK & CHATBOT AI
echo ======================================================================
echo          PHÁT TÀI BANK — HỆ THỐNG WEB & CHATBOT AI TOÀN NĂNG
echo ======================================================================
echo.
echo [1/3] Đang khởi động Web Server Frontend (Cổng 5500)...
start "PhatTaiBank - Web Server (5500)" cmd /k "cd /d "%~dp0" && py -m http.server 5500"

echo [2/3] Đang khởi động AI Backend Server (Cổng 8000)...
start "PhatTaiBank - AI Backend (8000)" cmd /k "cd /d "%~dp0phat_tai_bank" && py ai_backend/server_banking77.py"

echo [3/3] Đang mở trình duyệt website...
timeout /t 2 /nobreak >nul
start http://localhost:5500

echo.
echo ======================================================================
echo  KHỞI ĐỘNG THÀNH CÔNG!
echo.
echo  • Truy cập trên máy tính này:
echo    👉 http://localhost:5500
echo.
echo  • Truy cập từ điện thoại / laptop khác (BẮT CHUNG WI-FI):
echo    👉 http://192.168.1.20:5500
echo.
echo  (Vui lòng không tắt 2 cửa sổ màu đen đang chạy ngầm để web hoạt động)
echo ======================================================================
echo.
pause
