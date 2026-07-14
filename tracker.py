import requests
from bs4 import BeautifulSoup
import os

# Telegram Data
TELEGRAM_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_ID"
SCRAPER_API_KEY = "YOUR_API"


items_to_track = [
    {"name": "camera_osmo", "url": "https://www.amazon.sa/-/en/dp/B0FM3YTRGD/", "file_name": "osmo.txt"},
    
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def check_prices():
    print("\n Checking prices via ScraperAPI ")
    for item in items_to_track:
        try:
            
            payload = {'api_key': SCRAPER_API_KEY, 'url': item["url"]}
            response = requests.get('http://api.scraperapi.com/', params=payload)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            price_element = soup.select_one('span.a-price span.a-price-whole')
            
            if price_element:
                price_text = price_element.text.replace('SAR', '').replace(',', '').strip()
                
                current_price = float(''.join(filter(str.isdigit, price_text.split('.')[0])))
                
                
                last_price = None
                if os.path.exists(item["file_name"]):
                    with open(item["file_name"], "r") as file:
                        last_price = float(file.read().strip())
                
                
                if last_price is None:
                    with open(item["file_name"], "w") as file:
                        file.write(str(current_price))
                    print(f" Initial price saved for {item['name']}: {current_price}")
                
                elif current_price != last_price:
                    msg = f"🔔 تنبيه: تغير في السعر!\nالمنتج: {item['name']}\nالسعر القديم: {last_price} SAR\nالسعر الجديد: {current_price} SAR\nالرابط: {item['url']}"
                    send_telegram_message(msg)
                    print(f" Alert sent for {item['name']}!")
                    
                    with open(item["file_name"], "w") as file:
                        file.write(str(current_price))
                else:
                    print(f" No price change for {item['name']} ({current_price} SAR)")
            else:
                print(f" Could not find price for {item['name']}.")
        except Exception as e:
            print(f" Error checking {item['name']}: {e}")

if __name__ == "__main__":
    check_prices()