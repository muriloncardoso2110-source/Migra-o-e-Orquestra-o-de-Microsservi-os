"""HTTP APIs used in the migration lab. No external Python dependencies."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from urllib.request import urlopen

PRODUCTS = [
    {"id": 1, "name": "Caderno", "price": 18.9},
    {"id": 2, "name": "Caneta", "price": 4.5},
    {"id": 3, "name": "Mochila", "price": 89.0},
]
CUSTOMERS = [
    {"id": 1, "name": "Ana Lima"},
    {"id": 2, "name": "Bruno Alves"},
]
ORDERS = [
    {"id": 101, "customer_id": 1, "product_id": 1, "quantity": 2},
    {"id": 102, "customer_id": 2, "product_id": 3, "quantity": 1},
]


def get_payload(service, path):
    """Return (status, payload) for a local endpoint."""
    if path == '/health':
        return 200, {'status': 'ok', 'service': service}
    routes = {
        '/api/products': ('catalog', PRODUCTS),
        '/api/customers': ('customers', CUSTOMERS),
        '/api/orders': ('orders', ORDERS),
    }
    if path in routes:
        owner, data = routes[path]
        if service in (owner, 'monolith'):
            return 200, {'items': data, 'count': len(data), 'served_by': service}
    return 404, {'error': 'not_found', 'path': path, 'service': service}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        service = os.environ.get('SERVICE', 'catalog')
        path = urlparse(self.path).path
        status, payload = get_payload(service, path)
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[{os.environ.get("SERVICE", "catalog")}] {self.address_string()} {fmt % args}', flush=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    print(f'API {os.environ.get("SERVICE", "catalog")} na porta {port}', flush=True)
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
