import unittest
from datetime import datetime
from types import SimpleNamespace

from app.tasks import get_new_tasks
from app.conversation import get_new_conversations


class DeltaNotificationTests(unittest.TestCase):
    def test_get_new_tasks_only_returns_new_items(self):
        current = [
            SimpleNamespace(title="Mathe", date=datetime(2026, 8, 10), subject_name="Mathe"),
            SimpleNamespace(title="Deutsch", date=datetime(2026, 8, 11), subject_name="Deutsch"),
        ]
        last = [
            {"title": "Mathe", "date": "2026-08-10 00:00:00", "subject_name": "Mathe"},
        ]

        new_tasks = get_new_tasks(current, last)

        self.assertEqual([task.title for task in new_tasks], ["Deutsch"])

    def test_get_new_conversations_only_returns_new_items(self):
        current = [
            SimpleNamespace(id="msg-1", title="Hallo"),
            SimpleNamespace(id="msg-2", title="Neu"),
        ]
        last = [{"id": "msg-1"}]

        new_conversations = get_new_conversations(current, last)

        self.assertEqual([conversation.id for conversation in new_conversations], ["msg-2"])


if __name__ == "__main__":
    unittest.main()
