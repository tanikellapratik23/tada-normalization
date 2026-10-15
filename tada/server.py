"""Read-only loopback dashboard and JSON API, with no external assets."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json
from .storage import connect, query
from .core import dumps

def serve(path, port=8080):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed=urlparse(self.path)
            try:
                if parsed.path=='/':data=Path(__file__).with_name('dashboard.html').read_bytes();kind='text/html; charset=utf-8'
                elif parsed.path=='/health':data=b'{"status":"ok"}';kind='application/json'
                elif parsed.path in ('/api/records','/api/stats'):
                    db=connect(path)
                    try:
                        if parsed.path=='/api/records':
                            args={k:v[0] for k,v in parse_qs(parsed.query).items() if k in ('provider','entity','company_id','limit','offset')}
                            for key in ('limit','offset'):
                                if key in args:args[key]=int(args[key])
                            result=query(db,**args)
                        else:
                            rows=[json.loads(x[0]) for x in db.execute('SELECT document FROM records')]
                            result={'total':len(rows),'providers':len({r['source']['provider'] for r in rows}),'diagnostics':sum(len(r['diagnostics']) for r in rows)}
                    finally:db.close()
                    data=dumps(result).encode();kind='application/json'
                else:self.send_error(404);return
                self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store')
                self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
            except (ValueError,TypeError):self.send_error(400,'Invalid query parameters')
        def log_message(self,*args):pass
    print(f'Local explorer: http://127.0.0.1:{port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
