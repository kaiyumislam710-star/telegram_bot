import requests

TOKEN = "7828978717:AAFYSO2XDDI3aAGW1ly7zdL81H-vaCoPr8g"
CHAT_ID = "8304166462"

def send(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Telegram send error: {e}")