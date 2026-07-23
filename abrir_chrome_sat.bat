@echo off
title SAT_RPA

taskkill /F /IM chrome.exe >nul 2>&1

timeout /t 2 >nul

if not exist "C:\SAT_RPA\ChromeProfile" mkdir "C:\SAT_RPA\ChromeProfile"

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
--remote-debugging-port=9222 ^
--user-data-dir="C:\SAT_RPA\ChromeProfile"