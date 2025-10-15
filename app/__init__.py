# app/__init__.py
from flask import Flask

def create_app(env_name='development'):
    """
    應用程式工廠：建立並配置 Flask 實例。
    """
    # 設置模板和靜態檔案路徑
    app = Flask('app', # 使用 'app' 作為應用程式名稱
                instance_relative_config=True, 
                template_folder='../templates')

    # 配置應用程式
    app.config.from_mapping(
        SECRET_KEY='dev_key_secure', 
        TEMPLATES_AUTO_RELOAD=True
    )
    
    # --- 註冊 Blueprints (模組化關鍵) ---
    
    # 1. 註冊 UI 模組
    from .ui import ui_bp as ui_module
    app.register_blueprint(ui_module)
    
    # 2. 註冊 API 模組
    from .api import api_bp as api_module
    app.register_blueprint(api_module, url_prefix='/api')
    
    # 3. 註冊 Auth 模組
    from .auth import auth_bp as auth_module
    app.register_blueprint(auth_module, url_prefix='/auth')

    return app
