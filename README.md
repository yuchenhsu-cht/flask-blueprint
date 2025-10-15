# Flask Blueprint Project

## Overview
這個專案展示了如何使用 Flask Blueprint 來建立模組化的網頁應用程式。Blueprint 讓我們可以將大型應用程式分解成多個可管理的組件。

## Features
- 使用 Blueprint 實現模組化應用程式架構
- 清晰的關注點分離
- 易於維護和擴展
- RESTful API 設計
- 完整的錯誤處理機制

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/FlaskBlueprint.git

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
FlaskBlueprint/
├── app/
│   ├── __init__.py         # 應用程式初始化
│   ├── models/            # 資料模型
│   │   └── __init__.py
│   ├── routes/           # API 路由定義
│   │   ├── __init__.py
│   │   ├── auth.py      # 認證相關路由
│   │   └── main.py      # 主要路由
│   ├── services/        # 業務邏輯
│   │   └── __init__.py
│   ├── static/          # 靜態檔案
│   └── templates/       # HTML 模板
├── config/             # 設定檔案
│   ├── __init__.py
│   ├── development.py
│   └── production.py
├── tests/             # 單元測試
├── requirements.txt    # 相依套件
└── run.py             # 啟動程式
```

## Usage
```bash
# Development mode
python run.py

# Production mode
export FLASK_ENV=production
python run.py
```
應用程式將會在 http://localhost:5000 啟動

## License
MIT License