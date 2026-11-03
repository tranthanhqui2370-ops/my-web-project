@echo off
chcp 65001 >nul
title CHIA SẺ WEB RA TOÀN THẾ GIỚI (MẠNG KHÁC, 4G/5G)
echo ======================================================================
echo       TẠO ĐƯỜNG DẪN CÔNG KHAI INTERNET CHO MÁY KHÁC / MẠNG KHÁC
echo ======================================================================
echo.
echo Đang tạo đường hầm kết nối Internet công khai cho cổng 5500...
echo.
echo Khi đường link xuất hiện bên dưới (dạng https://...loca.lt):
echo 👉 Bạn có thể copy link đó gửi cho bất kỳ ai ở mạng khác, dùng 4G/5G
echo    đều mở được web của bạn!
echo.
echo Lưu ý: Giữ cửa sổ này mở để link tiếp tục hoạt động.
echo ======================================================================
echo.
npx --yes localtunnel --port 5500
pause
