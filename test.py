import unittest
import json
import sys, os.path
from apiV1 import *

class TestApiV1(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_24h(self):
        response = self.app.get('/servicio/v1/prediccion/24horas')
        self.assertEqual(response.status_code, 200)

    def test_48h(self):
        response = self.app.get('/servicio/v1/prediccion/48horas')
        self.assertEqual(response.status_code, 200)

    def test_72h(self):
        response = self.app.get('/servicio/v1/prediccion/72horas')
        self.assertEqual(response.status_code, 200)

