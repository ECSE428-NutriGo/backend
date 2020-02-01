from nutrition import controller
from rest_framework.test import APITestCase, APIRequestFactory

class TempTestCase(APITestCase):
    """
    This TestCase is for the GET method on /nutri/test/
    """
    def test_hello_world(self):
        url = '/nutri/test/'
        factory = APIRequestFactory()
        view = controller.Test.as_view()
        request = factory.get(url, content_type='application/json')
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Hello, world!")