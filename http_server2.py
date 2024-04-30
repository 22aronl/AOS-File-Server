from http.server import BaseHTTPRequestHandler, HTTPServer
from scapy.all import sniff

# Define the tap device you want to sniff packets from
TAP_DEVICE = "dtap0"

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Sniff packets from the tap device
        packets = sniff(iface=TAP_DEVICE, count=10)
        
        # Send captured packets as response
        for packet in packets:
            self.wfile.write(str(packet).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()