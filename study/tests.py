from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тест CRUD уроков и функционал работы подписки на обновления курса."""

    def setUp(self):
        """Создание тестового пользователя для авторизации."""
        self.user = User.objects.create(email="admin9313@example.com")

        self.course = Course.objects.create(
            name="Test_Course_23",
            description="Test_Course_23",
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            name="Test_Lesson_23",
            description="Test_Lesson_23",
            owner=self.user,
            courses=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_lesson(self):
        """Тест вывод уроков."""

        url = reverse("study:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_create_lesson(self):
        """Тест создания уроков."""
        url = reverse("study:lesson_create")
        data = {
            "name": "Test_Lesson_9",
            "description": "Test_Lesson_39",
            "courses": "1",
            "video": "https://www.youtube.com",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_update_lesson(self):
        """Тест обновления урока."""
        url = reverse("study:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Test2_Lesson_9",
            "description": "Test2_Lesson_39",
        }

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test2_Lesson_9")

    def test_delete_lesson(self):
        """Тест удаления урока."""
        url = reverse("study:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_list_lesson(self):
        """Тест создания уроков."""
        url = reverse("study:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "courses": self.lesson.courses.pk,
                    "id": self.lesson.pk,
                    "price": self.lesson.price,
                    "video": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_create_subscription(self):
        """Тест создание подписки."""
        url = reverse("study:subscription")
        data = {"user_subscription": self.user, "course_subscription": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(
                user_subscription=self.user, course_subscription=self.course.pk
            ).exists()
        )

    def test_remove_subscription(self):
        """Тест удаление подписки."""

        Subscription.objects.create(
            user_subscription=self.user, course_subscription=self.course
        )
        url = reverse("study:subscription")

        data = {"user_subscription": self.user, "course_subscription": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(
                user_subscription=self.user, course_subscription=self.course.pk
            ).exists()
        )
