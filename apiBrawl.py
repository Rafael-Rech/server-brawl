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
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQyMWMwM2Y2LWE4OTItNGU4Zi05ZTY1LTU3ZWZjMDQ0YmJiZSIsImlhdCI6MTcyODkxNDgzMSwic3ViIjoiZGV2ZWxvcGVyL2E4OTRmNmI0LWI0MDUtMDc5OC1hMjAxLTBlYmU2Njc1ZmVlNyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTc5LjE4Ni4yMjQuMjMiXSwidHlwZSI6ImNsaWVudCJ9XX0.D2tiL1rIOH9T5PRTc2SrbdbD4-Sb_zFtJecafS_Zxd1ySaRXe1J-SyAn_a_03kQ6HvbOLeofmO_FjtcPT08Q0A"
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