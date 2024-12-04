from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345",
        )
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="worker12345",
            first_name="Test",
            last_name="Worker",
        )
        self.client.force_login(self.admin_user)

    def test_worker_listed(self):
        url = reverse("admin:todo_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.first_name)
        self.assertContains(res, self.worker.last_name)

    def test_invalid_worker_not_listed(self):
        url = reverse("admin:todo_worker_changelist")
        self.worker.delete()
        res = self.client.get(url)
        self.assertNotContains(res, "Test Worker")

    def test_worker_with_empty_name(self):
        self.worker.first_name = ""
        self.worker.last_name = ""
        self.worker.save()
        url = reverse("admin:todo_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, "(No name)")
