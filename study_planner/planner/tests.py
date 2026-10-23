from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Subject, Task


class PlannerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.subject = Subject.objects.create(name='Высшая математика', description='Тестовая дисциплина')
        self.other_subject = Subject.objects.create(name='Базы данных')
        self.task = Task.objects.create(
            title='Лабораторная работа № 6',
            subject=self.subject,
            due_date=date(2026, 11, 1),
            status='new',
        )
        Task.objects.create(
            title='Подготовить конспект',
            subject=self.other_subject,
            due_date=date(2026, 12, 15),
            status='completed',
        )

    def test_subject_crud(self):
        response = self.client.post('/api/subjects/', {
            'name': 'Алгоритмы', 'description': 'Новая дисциплина'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        subject_id = response.data['id']

        response = self.client.patch(f'/api/subjects/{subject_id}/', {'name': 'Алгоритмы и структуры данных'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Алгоритмы и структуры данных')

        response = self.client.delete(f'/api/subjects/{subject_id}/')
        self.assertEqual(response.status_code, 204)

    def test_task_crud(self):
        response = self.client.post('/api/tasks/', {
            'title': 'Практическая работа',
            'subject': self.subject.id,
            'due_date': '2026-11-20',
            'status': 'in_progress',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        task_id = response.data['id']

        response = self.client.patch(f'/api/tasks/{task_id}/', {'status': 'completed'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'completed')

        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, 204)

    def test_server_side_filters_can_be_combined(self):
        response = self.client.get('/api/tasks/', {
            'search': 'лабораторная',
            'status': 'new',
            'subject': self.subject.id,
            'due_before': '2026-11-30',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.task.id)

    def test_invalid_filter_returns_validation_error(self):
        response = self.client.get('/api/tasks/?status=unknown')
        self.assertEqual(response.status_code, 400)

    def test_subject_with_tasks_cannot_be_deleted(self):
        response = self.client.delete(f'/api/subjects/{self.subject.id}/')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Subject.objects.filter(pk=self.subject.id).exists())
