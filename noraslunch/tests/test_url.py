import uuid
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from noraslunch.views import index, MenuList, CreateMenuView, MenuDetailView, CreateEmployeeMealView, thanks, timeout, \
    UpdateMenuView


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse("noraslunch:index")
        self.assertEquals(resolve(url).func, index)

    def test_thanks_url_resolves(self):
        url = reverse("noraslunch:thanks")
        self.assertEquals(resolve(url).func, thanks)

    def test_timeout_url_resolves(self):
        url = reverse("noraslunch:timeout")
        self.assertEquals(resolve(url).func, timeout)

    def test_menu_list_url_resolves(self):
        url = reverse("noraslunch:menu_list")
        self.assertEquals(resolve(url).func.view_class, MenuList)

    def test_create_menu_url_resolves(self):
        url = reverse("noraslunch:create_menu")
        self.assertEquals(resolve(url).func.view_class, CreateMenuView)

    def test_update_url_resolves(self):
        rnd_uuid = uuid.uuid4()
        url = reverse("noraslunch:update_menu", args=[rnd_uuid])
        self.assertEquals(resolve(url).func.view_class, UpdateMenuView)

    def test_menu_detail_url_resolves(self):
        rnd_uuid = uuid.uuid4()
        url = reverse("noraslunch:menu_detail", args=[rnd_uuid])
        self.assertEquals(resolve(url).func.view_class, MenuDetailView)

    def test_menu_url_resolves(self):
        rnd_uuid = uuid.uuid4()
        url = reverse("noraslunch:menu", args=[rnd_uuid])
        self.assertEquals(resolve(url).func.view_class, CreateEmployeeMealView)







