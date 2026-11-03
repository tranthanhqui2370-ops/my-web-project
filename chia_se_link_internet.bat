@echo off
chcp 65001 >nul
title CHIA SẺ WEB RA TOÀN THẾ GIỚI (MẠNG KHÁC, 4G/5G)
echo ======================================================================
echo    TẠO ĐƯỜNG DẪN CLOUDFLARE INTERNET CHO MÁY KHÁC / MẠNG KHÁC (4G/5G)
echo ======================================================================
echo.
echo Đang kết nối mạng toàn cầu qua Cloudflare Tunnel...
echo.
echo Khi đường link xuất hiện bên dưới (dạng https://...trycloudflare.com):
echo 👉 Bạn chỉ cần COPY đường link đó gửi cho bạn bè/thầy cô ở bất kỳ đâu
echo    (dùng 4G, 5G hay Wi-Fi khác) đều mở được trang web của bạn ngay!
echo.
echo [LƯU Ý] Giữ cửa sổ này mở để link tiếp tục hoạt động.
echo ======================================================================
echo.
"%~dp0cloudflared.exe" tunnel --url http://localhost:5500
pause
