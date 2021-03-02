import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import googleCalendar

def getCalendarData(data):
    try:
        creator = data['creator']
    except Exception as e:
        pass
    try:
        seconds = data['seconds']
        calendarData = googleCalendar.getCalendarData(seconds=seconds)
    except Exception as e:
        calendarData = googleCalendar.getCalendarData()
    return calendarData

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            tmp = self.path.split("?",1)
            self.path = tmp[0]
            data = ""
        except IndexError:
            print("Ошибка в индексировании")

        if len(tmp)>1:
            try:
                data = json.loads(urllib.parse.unquote(tmp[1]))
            except Exception as e:
                data = {}
        if self.path == "/getCalendarData":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            calendarData = getCalendarData(data)
            self.wfile.write(calendarData.encode('utf-8'))
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
