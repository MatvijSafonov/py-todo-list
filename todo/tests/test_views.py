from django.test import TestCase
from django.urls import reverse

from todo.models import Task

TASK_URL = reverse("todo_list:task-list")
TAG_URL = reverse("todo_list:tag-list")


class PublicTaskTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="New functional",
            content="Add new functional to index page with buttons",
            deadline="2023-04-04 15:00:00",
            status=True,
        )

    def test_login_required(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_valid_task_view(self):
        self.client.login(username="admin", password="admin12345")
        response = self.client.get(reverse("todo_list:task-detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_invalid_task_access(self):
        response = self.client.get(reverse("todo_list:task-detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_deleted_task_access(self):
        self.task.delete()
        response = self.client.get(reverse("todo_list:task-detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)
