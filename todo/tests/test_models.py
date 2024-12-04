from django.test import TestCase

from todo.models import Task, Tag


class ModelTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="#bug")
        self.task = Task.objects.create(
            name="New functional",
            content="Add new functional to index page with buttons",
            deadline="2023-04-04 15:00:00",
            status=True,
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "New functional")

    def test_invalid_task_without_name(self):
        with self.assertRaises(ValueError):
            Task.objects.create(content="Missing name", deadline="2023-04-04 15:00:00")

    def test_task_with_long_name(self):
        long_name = "x" * 300
        task = Task.objects.create(name=long_name, content="Test", deadline="2023-04-04 15:00:00")
        self.assertEqual(str(task), long_name[:50] + "...")
