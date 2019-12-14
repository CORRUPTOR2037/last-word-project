from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

from os import listdir
from os.path import isfile, join
import urllib.parse

mypath = 'records/'
def load_index():
    result = ""
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for file in onlyfiles:
        result += "<a href='./" + file[0:-4].replace(' ', '_') + "'>" + file[0:-4] + "</a>"
    
    return result

def load(filename):
    filename = urllib.parse.unquote(filename).replace("_", " ")
    print(filename)
    with open(filename.replace("_", " ")) as f:
        lines = f.readlines()
        
        result =  '<p><span>Кто:</span>' + lines[0] + '</p>\n'
        result += '<p><span>Когда:</span>' + lines[1] + '</p>\n'
        result += '<p><span>По какой статье:</span>' + lines[2] + '</p>\n'
        result += '<p><span>За что:</span>' + lines[3] + '</p>\n'
        result += '<p><span>Что получил:</span>' + lines[4] + '</p>\n'
        
        result += '<div class="text"><p>' + '</p><p>'.join(lines[6:]) + '</p></div>'
        
        return result
    
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if self.path == '/':
            self.print_page(load_index())
        try:
            self.print_page(load('records' + self.path + '.txt'))
        except Exception as e:
            self.print_page('Ошибка: ' + self.path[1:])
            print(e)

    def do_POST(self):
        pass
    
    def print_page(self, content):
        with open('header.html', 'rb') as f:
            self.wfile.write(f.read())
            
        self.wfile.write(content.encode('utf-8'))
        
        with open('footer.html', 'rb') as f:
            self.wfile.write(f.read())


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    run()
