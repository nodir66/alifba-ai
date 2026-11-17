@echo off
title Alifba AI - Hujjat va Yangi Alifbo Konverteri
color 0B
echo ========================================================
echo   Alifba AI - Hujjatlar, PDF va Yangi Alifbo Studiyasi
echo   Dastur Yaratuvchisi: Ismoilov Nodir
echo ========================================================
echo.
echo Kutubxonalar tekshirilmoqda...
pip install -r requirements.txt
echo.
echo Dastur ishga tushmoqda...
start http://127.0.0.1:5050
python app.py
pause
