import datetime
import random
import string
import uuid
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from freezegun import freeze_time
from model_bakery import baker

from noraslunch.models import Menu, Meal, EmployeeMeal


class TestViews(TestCase):

    def setUp(self):
        # General setups
        rnd_string = ''.join(random.choice(string.ascii_letters) for i in range(8))
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        self.some_menu = baker.make(Menu)
        self.some_meal = baker.make(Meal, menu=self.some_menu)
        self.client = Client()
        self.time_out = datetime.time(11)
        self.on_time = datetime.time(10, 59)

        # Menu list url
        self.menu_list_url = reverse("noraslunch:menu_list")

        # Menu Detail urls
        self.menu_detail_url = reverse("noraslunch:menu_detail", args=[self.some_menu.id])
        self.menu_detail_url_rnd_uuid = reverse("noraslunch:menu_detail", args=[uuid.uuid4()])
        self.menu_detail_url_non_uuid = reverse("noraslunch:menu_detail", args=[rnd_string])

        # Create Employee Meal url
        self.menu_url = reverse("noraslunch:menu", args=[self.some_menu.id])
        self.menu_url_rnd_uuid = reverse("noraslunch:menu", args=[uuid.uuid4()])
        self.menu_url_non_uuid = reverse("noraslunch:menu", args=[rnd_string])

        # Create Menu url
        self.create_menu_url = reverse("noraslunch:create_menu")

    # Login view
    def test_login(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    # Menu List View Tests
    """
    Auth / Non Auth request will be tested
    """

    # Non authenticated GET method should redirect to login
    def test_menu_list_not_authenticated_GET(self):
        response = self.client.get(self.menu_list_url)

        # Ensure redirect to login
        self.assertEquals(response.url[0:16], "/accounts/login/")
        self.assertEquals(response.status_code, 302)

    # Authenticated GET method must have 200 status code
    def test_menu_list_authenticated_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.menu_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "noraslunch/menu_list.html")

    # Menu Detail View Test
    """
    Auth / Non auth GET methods will be tested
    Random uuid on url args must show 404 error
    Non uuid on url args must show 404 error
    Template used
    """

    # Non authenticated GET method should redirect to login
    def test_menu_detail_not_authenticated_GET(self):
        response = self.client.get(self.menu_detail_url)

        # Ensure redirect to login
        self.assertEquals(response.url[0:16], "/accounts/login/")
        self.assertEquals(response.status_code, 302)

    # Authenticated GET method must have 200 status code
    def test_menu_detail_authenticated_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.menu_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "noraslunch/menu_detail.html")

    # Random uuid which is not a menu id must show 404 not found error
    def test_menu_detail_rnd_uuid_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.menu_detail_url_rnd_uuid)
        self.assertEquals(response.status_code, 404)

    # Random string which is not a menu id must show 404 not found error
    def test_menu_detail_non_uuid_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.menu_detail_url_non_uuid)
        self.assertEquals(response.status_code, 404)

    # Create Employee Meal View
    """
    Auth / Non auth GET & POST methods will be tested. Both cases must show 200 success with on time request
    Random uuid on url args shows 404 error
    Non uuid on url args show 404 error
    Time out request should not create objects and render timeout template
    """

    # On time non auth GET method should show create employee meal template
    @freeze_time("2020-05-28 10:59:59")
    def test_menu_not_authenticated_GET(self):
        response = self.client.get(self.menu_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "noraslunch/create_employee_meal.html")

    # On time auth GET method should show create employee meal template
    @freeze_time("2020-05-28 10:59:59")
    def test_menu_authenticated_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.menu_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "noraslunch/create_employee_meal.html")

    # On time random uuid which is not a menu id must show 404 not found error
    @freeze_time("2020-05-28 10:59:59")
    def test_menu_rnd_uuid_GET(self):
        response = self.client.get(self.menu_url_rnd_uuid)
        self.assertEquals(response.status_code, 404)

    # Time out random uuid which is not a menu id must show 404 not found error
    @freeze_time("2020-05-28 11:00:00")
    def test_menu_rnd_uuid_GET(self):
        response = self.client.get(self.menu_url_rnd_uuid)
        self.assertEquals(response.status_code, 404)

    # On time random string which is not a menu id must show 404 not found error. Time out test will be skipped
    @freeze_time("2020-05-28 10:59:59")
    def test_menu_non_uuid_GET(self):
        response = self.client.get(self.menu_url_non_uuid)
        self.assertEquals(response.status_code, 404)

    # Time out non auth GET method render timeout.html template
    @freeze_time("2020-05-28 11:00:00")
    def test_menu_not_authenticated_GET_time_out(self):
        response = self.client.get(self.menu_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "noraslunch/timeout.html")

    # On time non auth POST method create object and redirect
    @freeze_time("2020-05-28 10:59:59")
    def test_menu_not_authenticated_POST_on_time_create_employee_meal(self):
        response = self.client.post(self.menu_url, {
            'employee_name': 'John Doe',
            'meal': self.some_meal.id,
            'customization': 'Con todo si no pa que.',
        })
        self.assertGreater(self.some_meal.employeemeal_set.count(), 0)
        self.assertEquals(response.status_code, 302)

    # Time out non auth POST method must not create object and redirect
    @freeze_time("2020-05-28 11:00:00")
    def test_menu_not_authenticated_POST_time_out_create_employee_meal(self):
        response = self.client.post(self.menu_url, {
            'employee_name': 'John Doe',
            'meal': self.some_meal.id,
            'customization': 'Con todo si no pa que.',
        })
        self.assertEquals(response.status_code, 302)

    # Create Menu View
    """
    Auth / Non Auth GET and POST methods
    """

    def test_create_menu_authenticated_GET(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.create_menu_url)
        self.assertEquals(response.status_code, 200)

    def test_create_menu_not_authenticated_GET(self):
        response = self.client.get(self.create_menu_url)

        # Ensure redirect to login
        self.assertEquals(response.url[0:16], "/accounts/login/")
        self.assertEquals(response.status_code, 302)

    def test_create_menu_authenticated_POST(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(self.create_menu_url, {
            # Specific date to avoid get problems later
            'menu_date': '1984-12-08',
            'meal_set-TOTAL_FORMS': ['4'], 'meal_set-INITIAL_FORMS': ['0'],
            'meal_set-MIN_NUM_FORMS': ['0'], 'meal_set-MAX_NUM_FORMS': ['1000'],
            'meal_set-0-description': ['Pastel de choclo, Ensalada y Postre'],
            'meal_set-1-description': ['Arroz con nugget de pollo, Ensalada y Postre'],
            'meal_set-2-description': ['Arroz con hamburguesa, Ensalada y Postre'],
            'meal_set-3-description': ['Ensalada premium de pollo y Postre'],
        })
        menu = Menu.objects.get(menu_date='1984-12-08')
        self.assertEquals(menu.meal_set.count(), 4)
        self.assertEquals(response.status_code, 302)

    def test_create_menu_not_authenticated_POST(self):
        all_menu_objects = Menu.objects.count()
        response = self.client.post(self.create_menu_url, {
            # Specific date to avoid get problems later
            'menu_date': '1984-12-08',
            'meal_set-TOTAL_FORMS': ['4'], 'meal_set-INITIAL_FORMS': ['0'],
            'meal_set-MIN_NUM_FORMS': ['0'], 'meal_set-MAX_NUM_FORMS': ['1000'],
            'meal_set-0-description': ['Pastel de choclo, Ensalada y Postre'],
            'meal_set-1-description': ['Arroz con nugget de pollo, Ensalada y Postre'],
            'meal_set-2-description': ['Arroz con hamburguesa, Ensalada y Postre'],
            'meal_set-3-description': ['Ensalada premium de pollo y Postre'],
        })
        new_all_menu_objects = Menu.objects.count()
        # Ensure non objects was created
        self.assertEquals(all_menu_objects, new_all_menu_objects)

        # Ensure redirect to login
        self.assertEquals(response.url[0:16], "/accounts/login/")
        self.assertEquals(response.status_code, 302)

    # Send menu via slack test
    def test_send_menu_as_slack_message(self):
        response = self.client.get(reverse("noraslunch:send_menu_as_slack_message", args=[self.some_menu.id]))
        self.assertEquals(response.status_code, 302)
