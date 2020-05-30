
from django.test import override_settings, TestCase
from model_bakery import baker

from noraslunch.tasks import send_slack


class TestTasks(TestCase):

    @override_settings(
        task_eager_propagates=True,
        task_always_eager=True,
        broker_url='memory://',
        backend='memory'
    )
    def test_send_slack_message(self):
        menu = baker.make('noraslunch.Menu')
        meals = baker.make('noraslunch.Meal', menu=menu, _quantity=4)
        response = send_slack.delay(menu.id)
        self.assertTrue(response.result)
        # Todo: Check for Menu.was_sent = True asynchronously


