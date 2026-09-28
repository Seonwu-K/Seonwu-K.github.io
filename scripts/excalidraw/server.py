import http.server, os, base64, sys
OUT=sys.argv[1]
class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        name=os.path.basename(self.path)
        data=self.rfile.read(int(self.headers['Content-Length'])).decode()
        b=base64.b64decode(data.split(',',1)[1])
        open(os.path.join(OUT,name),'wb').write(b)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass
os.chdir(os.path.dirname(os.path.abspath(__file__)))
http.server.ThreadingHTTPServer(('127.0.0.1',4180),H).serve_forever()
