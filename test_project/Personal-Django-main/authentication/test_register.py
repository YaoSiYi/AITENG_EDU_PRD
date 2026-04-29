import os
import django
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

class RegisterAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = '/auth/register/'
        
    def test_register_user_success(self):
        """测试成功注册用户"""
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }
        
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['code'], 20000)
        self.assertEqual(response.json()['msg'], '注册成功')
        
        # 检查用户是否创建成功
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # 检查Token是否创建
        user = User.objects.get(username='testuser')
        self.assertTrue(Token.objects.filter(user=user).exists())
        
    def test_register_duplicate_username(self):
        """测试重复用户名注册"""
        # 先创建一个用户
        User.objects.create_user(username='testuser', password='testpassword123')
        
        # 尝试用相同用户名注册
        data = {
            'username': 'testuser',
            'password': 'newpassword123',
            'email': 'new@example.com'
        }
        
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 40000)
        self.assertEqual(response.json()['error'], '用户名已存在')
        
    def test_register_missing_fields(self):
        """测试缺少必填字段"""
        data = {
            'username': 'testuser',
            # 缺少密码字段
            'email': 'test@example.com'
        }
        
        response = self.client.post(self.register_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 40000)
        self.assertEqual(response.json()['error'], '用户名和密码为必填项')


class CurrentUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        
    def test_get_current_user_info(self):
        """测试获取当前用户信息"""
        # 设置认证头
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.get('/auth/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 20000)
        self.assertEqual(response.json()['msg'], 'Success')
        
        data = response.json()['data']
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['is_staff'], False)
        self.assertEqual(data['is_superuser'], False)
        self.assertEqual(data['is_active'], True)
        
    def test_get_current_user_unauthorized(self):
        """测试未认证用户访问当前用户信息"""
        response = self.client.get('/auth/user/')
        self.assertEqual(response.status_code, 401)