import time
import json
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 設定項目 ---
URL = "https://www.popmart.com/jp/products/5312/THE-MONSTERS-I-FOUND-YOU-"

def send_line_notification(token, message):
    """LINE Bot経由でメッセージをブロードキャスト送信する関数"""
    if not token:
        print("❌ LINEアクセストークンが設定されていません。")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = { "Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    data = {"messages": [{"type": "text", "text": message}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("✅ LINE通知を送信しました！")
    except requests.RequestException as e:
        print(f"❌ LINE通知の送信中にエラーが発生しました: {e}")
        if e.response is not None:
            print(f"エラー詳細: {e.response.text}")

def check_stock_with_selenium():
    """Seleniumを使って在庫状況をチェックするメインの関数"""
    print("--- POP MART 在庫チェッカー (最終調査モード) を起動しました ---")
    
    # --- 【ここから調査コード】 ---
    print("--- 秘密鍵のデバッグ情報 ---")
    retrieved_token = os.environ.get('LINE_TOKEN')

    if not retrieved_token:
        print("❌ Secretsからアクセストークンを読み込めませんでした。")
    else:
        print(f"✅ Secretsからトークンを読み込みました。")
        print(f"トークンの長さ: {len(retrieved_token)} 文字")
        print(f"トークンの最初の5文字: {retrieved_token[:5]}...")
        print(f"トークンの最後の5文字: ...{retrieved_token[-5:]}")
    print("--------------------------\n")
    # --- 【調査コードここまで】 ---

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    
    driver = None
    try:
        print(f"🔄 ブラウザを起動してページをチェックしています...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)
        
        # (ポップアップ処理などは省略して、通知テストをすぐに実行します)
        
        print("🎉 在庫が復活したと仮定して、LINEに通知を送信します。")
        send_line_notification(
            retrieved_token,
            f"これはGitHubからのテスト通知です。\nこの通知が届けば成功です。"
        )
                
    except Exception as e:
        print(f"❌ 不明なエラーが発生しました: {e}")
    finally:
        if driver:
            driver.quit()
            print("🚪 ブラウザを終了しました。")
    
    print("✅ チェック完了。")

if __name__ == "__main__":
    check_stock_with_selenium()
