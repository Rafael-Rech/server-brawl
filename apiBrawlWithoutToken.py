from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/events/rotation"):
            self.proxy_request("/v1/events/rotation")
        elif self.path.startswith("/players/"):
            self.proxy_request("/v1/players/")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def proxy_request(self, endpoint):
        api_url = f"https://api.brawlstars.com/v1{self.path}"
        headers = {
            "Authorization": "Bearer token",
        }
        
        response = requests.get(api_url, headers=headers)
        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.content)

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('0.0.0.0', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server on {}".format(server_address))
    httpd.serve_forever()

if __name__ == "__main__":
    run()