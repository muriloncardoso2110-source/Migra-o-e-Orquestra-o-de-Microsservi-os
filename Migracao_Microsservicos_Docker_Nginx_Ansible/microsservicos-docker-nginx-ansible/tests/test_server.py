import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('server', Path(__file__).resolve().parents[1] / 'services' / 'server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

class ApiTests(unittest.TestCase):
    def test_health(self):
        status, result = server.get_payload('catalog', '/health')
        self.assertEqual(status, 200)
        self.assertEqual(result['status'], 'ok')

    def test_isolation(self):
        self.assertEqual(server.get_payload('orders', '/api/products')[0], 404)

    def test_each_api(self):
        for service, route in [('catalog', '/api/products'), ('customers', '/api/customers'), ('orders', '/api/orders')]:
            with self.subTest(service=service):
                status, result = server.get_payload(service, route)
                self.assertEqual(status, 200)
                self.assertGreater(result['count'], 0)

    def test_legacy_serves_all_routes(self):
        for route in ['/api/products', '/api/customers', '/api/orders']:
            self.assertEqual(server.get_payload('monolith', route)[0], 200)

if __name__ == '__main__':
    unittest.main()
