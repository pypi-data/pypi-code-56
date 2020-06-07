from unittest import TestCase
import json
import calculator

class CalcTest(TestCase):
    
    def setUp(self):
        self.a = 5
        self.b = 2
        self.app = calculator.app.test_client()

    def test_add(self):
        res = self.app.get(f'/add/{self.a}/{self.b}')
        expect = { 'result (a+b)': 7 }
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(expect, json.loads(res.data))
    
    def test_subs(self):
        res = self.app.get(f'/subs/{self.a}/{self.b}')
        expect = { 'result (a-b)': 3 }
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(expect, json.loads(res.data))

    def test_multiply(self):
        res = self.app.get(f'/multiply/{self.a}/{self.b}')
        expect = { 'result (a*b)': 10 }
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(expect, json.loads(res.data))

    def test_division(self):
        res = self.app.get(f'/divise/{self.a}/{self.b}')
        expect = { 'result (a/b)': 2.5 }
        self.assertEqual(200, res.status_code)
        self.assertDictEqual(expect, json.loads(res.data))