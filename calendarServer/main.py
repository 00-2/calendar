import json
from http.server import BaseHTTPRequestHandler, HTTPServer

html = "<html><body>Hello from the Raspberry Pi</body></html>"

class ServerHandler(BaseHTTPRequestHandler):

    def sendHeaders(self):
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            tmp = self.path.split("?")
            self.path = tmp[0]
            data = ""
        except IndexError:
            print("Ошибка в индексировании")
        if len(tmp)>1:
            data = tmp[1]

        if self.path == "/getCalendarData":
            self.send_response(200)
            self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
