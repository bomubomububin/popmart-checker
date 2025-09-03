import time
import json
import requests
import os  # osライブラリをインポート
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 設定項目 ---
URL = "https://www.popmart.com/jp/products/5312/THE-MONSTERS-I-FOUND-YOU-"
CHECK_INTERVAL_SECONDS = 600

# 【変更点】GitHubのSecretsからトークンを読み込む
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')

# --- ここから下は変更不要です ---

def send_line_notification(token, message):
    """LINE Bot経由でメッセージをブロードキャスト送信する関数"""
    if not token:
        print("❌ LINEアクセストークンが設定されていません。")
        return

    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"messages": [{"type": "text", "text": message}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("✅ LINE通知を送信しました！")
    except requests.RequestException as e:
        print(f"❌ LINE通知の送信中にエラーが発生しました: {e}")
        if response is not None:
            print(f"エラー詳細: {response.text}")

def check_stock_with_selenium():
    """Seleniumを使って在庫状況をチェックするメインの関数"""
    print("--- POP MART 在庫チェッカー (GitHub Actionsモード) を起動しました ---")

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
        
        wait = WebDriverWait(driver, 10)

        # ポップアップ処理
        try:
            japan_button_xpath = "//div[contains(@class, 'index_ipInConutry__BoVSZ')]"
            japan_button = wait.until(EC.element_to_be_clickable((By.XPATH, japan_button_xpath)))
            japan_button.click()
            print("👍 地域選択ポップアップの「日本」ボタンをクリックしました。")
            time.sleep(2)
        except Exception:
            print("ℹ️ 地域選択ポップアップは表示されませんでした。")

        try:
            consent_button_xpath = "//div[contains(@class, 'policy_acceptBtn__ZNU71')]"
            consent_button = wait.until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))
            consent_button.click()
            print("👍 プライバシー同意ボタンをクリックしました。")
            time.sleep(3)
        except Exception:
            print("ℹ️ プライバシー同意ポップアップは表示されませんでした。")

        # 在庫チェック
        sold_out_elements = driver.find_elements(By.XPATH, "//*[normalize-space()='再入荷を通知']")
        
        if not sold_out_elements:
            print("🎉 在庫が復活しました！LINEに通知を送信します。")
            send_line_notification(
                LINE_CHANNEL_ACCESS_TOKEN,
                f"在庫が復活しました！\n商品ページを確認してください。\n{URL}"
            )
        else:
            minutes = CHECK_INTERVAL_SECONDS / 60
            print(f"💨 まだ在庫がありません。")
                
    except Exception as e:
        print(f"❌ 不明なエラーが発生しました: {e}")
    finally:
        if driver:
            driver.quit()
            print("🚪 ブラウザを終了しました。")

if __name__ == "__main__":
    check_stock_with_selenium()
