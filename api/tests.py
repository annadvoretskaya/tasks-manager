from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from base.models import ApplicationUser, Project, Task, Invite


class AuthenticationTestCase(APITestCase):
    fixtures = ['fixtures/tests/user.json']

    @classmethod
    def setUpTestData(cls):
        super(AuthenticationTestCase, cls).setUpTestData()
        cls.user = ApplicationUser.objects.first()

    def test_user_login(self):
        user = ApplicationUser(username="test", email="test@test.com")
        user.set_password("12qwaszx")
        user.save()

        resp = self.client.post('/api/login/', {'username': 'test', 'password': '12qwaszx'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        token = Token.objects.get(key=resp.data.get('token', None))
        self.assertEqual(token.user, user)

    def test_user_logout(self):
        key = Token.objects.create(user=self.user).key
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(key)}
        resp = self.client.delete('/api/logout/', {}, **headers)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIs(Token.objects.filter(key=key, user=self.user).exists(), False)


class ProjectTestCase(APITestCase):
    fixtures = ['fixtures/tests/user.json', 'fixtures/tests/project.json']

    @classmethod
    def setUpTestData(cls):
        super(ProjectTestCase, cls).setUpTestData()
        cls.user = ApplicationUser.objects.first()
        cls.projects = Project.objects.all()

    def test_project_creation(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Test user project",
            "description": "Lorem ipsum",
            "managers": [2],
            "developers": [3]
        }
        resp = self.client.post('/api/projects/', data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp_json_data = resp.json()
        self.assertTrue(Project.objects.filter(id=resp_json_data.get('id', None)).exists())

    def test_user_projects_list(self):
        self.client.force_authenticate(self.user)
        resp = self.client.get('/api/projects/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        user_projects_count = self.projects.by_user(self.user).count()
        self.assertEqual(user_projects_count, len(resp.json()))


class TaskTestCase(APITestCase):
    fixtures = ['fixtures/tests/user.json', 'fixtures/tests/project.json', 'fixtures/tests/task.json']

    @classmethod
    def setUpTestData(cls):
        super(TaskTestCase, cls).setUpTestData()
        cls.user = ApplicationUser.objects.first()
        cls.project = Project.objects.filter(owner=cls.user).first()

    def test_task_creation(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Test task",
            "description": "Lorem ipsum",
            "due_date": "2017-03-26T22:55:04.752962Z",
            "assigned_to": ''
        }
        request_url = '/api/projects/{project_pk}/tasks/'.format(project_pk=self.project.pk)
        resp = self.client.post(request_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp_json_data = resp.json()
        self.assertTrue(Task.objects.filter(id=resp_json_data.get('id', None)).exists())


class InviteTestCase(APITestCase):
    fixtures = ['fixtures/tests/user.json', 'fixtures/tests/project.json']

    @classmethod
    def setUpTestData(cls):
        super(InviteTestCase, cls).setUpTestData()
        cls.user = ApplicationUser.objects.first()
        cls.project = Project.objects.filter(owner=cls.user).first()

    def test_invite_creation(self):
        self.client.force_authenticate(self.user)
        data = {
            "email": "test@developer.com"
        }
        request_url = '/api/projects/{project_pk}/invites/'.format(project_pk=self.project.pk)
        resp = self.client.post(request_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invite.objects.filter(email="test@developer.com", project=self.project).exists())
