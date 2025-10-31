@echo off
chcp 65001 >nul
title 🦉 NewCoolOwl - Embedding Extractor Setup
echo.
echo ===============================
echo   NewCoolOwl Embedding 環境初始化
echo ===============================
echo.

:: Step 1. 移動到當前資料夾
cd /d %~dp0

:: Step 2. 檢查 Python 是否存在
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未安裝 Python，請先到 python.org 下載安裝！
    pause
    exit /b
)

:: Step 3. 建立虛擬環境 venv
if not exist venv (
    echo [建立虛擬環境] venv...
    python -m venv venv
)

:: Step 4. 啟動 venv
call venv\Scripts\activate

:: Step 5. 升級 pip 並安裝依賴
echo [安裝套件] sentence-transformers, tqdm ...
pip install --upgrade pip
pip install sentence-transformers tqdm

:: Step 6. 檢查主要腳本是否存在
if not exist extract_homophones.py (
    echo [警告] 找不到 extract_homophones.py
    echo 請確認檔案已放在 %cd%
    pause
    exit /b
)

:: Step 7. 執行主程式
echo.
echo ===============================
echo   啟動 Embedding 提取器 ...
echo ===============================
python extract_homophones.py

echo.
echo 完成！
pause
