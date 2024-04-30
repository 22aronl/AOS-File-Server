from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

# Define the HTTP request handler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, world!")

# Get the IP address associated with the tap0 interface
def get_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 1))  # Connect to a known external server
        return s.getsockname()[0]

# Get the IP address of the tap0 interface
tap0_ip = get_ip_address()

# Create the HTTP server
server_address = (tap0_ip, 8080)
# server_address = ("192.168.1.1", 8080)  # Change the port as needed
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Start the HTTP server
print(f"Server listening on http://{tap0_ip}:8080")
httpd.serve_forever()