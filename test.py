from main import app
import unittest
class FlaskTest(unittest.TestCase):
    def test(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status = response.status_code
        self.assertEqual(status,200)

    if __name__ == "__main__":
        unittest.main()


