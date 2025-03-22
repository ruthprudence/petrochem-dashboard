from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("network_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        hostname = socket.gethostname()
        try:
            host_ip = socket.gethostbyname(hostname)
        except:
            host_ip = "Could not determine IP"
            
        html = f"""
        <html>
        <head><title>Network Test Server</title></head>
        <body>
            <h1>Network Test Server</h1>
            <p>If you can see this page, your network connectivity is working!</p>
            <h2>Server Information:</h2>
            <ul>
                <li>Hostname: {hostname}</li>
                <li>IP Address: {host_ip}</li>
                <li>Port: 8000</li>
            </ul>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
        logger.info(f"Served request from {self.client_address[0]}")

def run_server(port=8000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPHandler)
    logger.info(f'Starting test server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
    except Exception as e:
        logger.error(f'Server error: {str(e)}')

if __name__ == "__main__":
    run_server()
