from rest_framework.test import APIRequestFactory, APITestCase

# Create your tests here.
# Using the standard RequestFactory API to create a form POST request


class StockTest(APITestCase):
    factory = APIRequestFactory()

    def test_list_all_stocks(self):
        response = self.factory.get('/api/stocks/')

        self.assertEqual(response.status_code, 200)
    def test_list_single_stock(self):
        response = self.factory.get('/api/stocks/1/')

        self.assertEqual(response.status_code, 200)