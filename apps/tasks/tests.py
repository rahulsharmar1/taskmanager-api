from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task

User = get_user_model()

class AuthenticatedAPITestCase(APITestCase):
    pass

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="securepassword123",
        )
        self._authenticate(self.user)

    def _authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
        )

class TaskCreateTests(AuthenticatedAPITestCase):

    def test_create_task_returns_201(self):
        payload = {"title": "Write tests", "status": "todo"}
        response = self.client.post("/api/tasks/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_created_task_belongs_to_requesting_user(self):
        payload = {"title": "My task", "status": "todo"}
        response = self.client.post("/api/tasks/", payload, format="json")
        self.assertEqual(response.data["owner"], self.user.id)
    
    def test_create_task_without_title_returns_400(self):
        response = self.client.post("/api/tasks/", {"status": "todo"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_unauthenticated_create_returns_401(self):
        self.client.credentials()   # remove the token
        response = self.client.post("/api/tasks/", {"title": "Task"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TaskListTests(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        # Create a second user with their own task
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpassword123",
        )
        Task.objects.create(owner=self.user, title="My task", status="todo")
        Task.objects.create(owner=self.other_user, title="Other task", status="done")

    def test_list_returns_only_own_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "My task")

    def test_filter_by_status(self):
        Task.objects.create(owner=self.user, title="Done task", status="done")
        response = self.client.get("/api/tasks/?status=done")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_pagination_returns_envelope(self):
        response = self.client.get("/api/tasks/")
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)


class TaskDetailTests(AuthenticatedAPITestCase):

    def setUp(self):
        super().setUp()
        self.task = Task.objects.create(
            owner=self.user, title="Detail task", status="todo"
        )
        self.other_user = User.objects.create_user(
            username="other", password="pass123"
        )
        self.other_task = Task.objects.create(
            owner=self.other_user, title="Other task", status="todo"
        )

    def test_retrieve_own_task_returns_200(self):
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_users_task_returns_404(self):
        response = self.client.get(f"/api/tasks/{self.other_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_changes_status(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": "done"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "done")

    def test_delete_own_task_returns_204(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_users_task_returns_404(self):
        response = self.client.delete(f"/api/tasks/{self.other_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
