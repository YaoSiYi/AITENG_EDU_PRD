"""
公共视图模块
提供基础视图类和通用功能
"""

import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def wrap_response(data, success=True):
    """
    包装响应数据，统一返回格式
    """
    response = {
        'code': 20000 if success else 50000,
        'success': success,
        'data': data if success else None,
        'message': '操作成功' if success else data.get('message', '操作失败')
    }
    return response


def response_wrapper(func):
    """
    装饰器：自动包装视图函数的响应
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # 如果结果已经是 JsonResponse，则直接返回
            if isinstance(result, JsonResponse):
                return result
            
            # 否则包装成统一格式
            if isinstance(result, dict):
                # 如果结果已经是字典格式，认为是成功的响应
                return JsonResponse(wrap_response(result, success=True))
            else:
                # 其他情况作为数据包装
                return JsonResponse(wrap_response({'data': result}, success=True))
        except Exception as e:
            # 如果发生异常，返回错误响应
            error_response = wrap_response({'message': str(e)}, success=False)
            return JsonResponse(error_response, status=500)
    
    return wrapper


class BaseAPIView(View):
    """
    API基础视图类，提供通用功能
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def parse_json_body(self, request):
        """解析JSON请求体"""
        try:
            return json.loads(request.body)
        except (ValueError, json.JSONDecodeError) as e:
            return None

    def validate_required_params(self, data, required_params):
        """验证必要参数"""
        missing_params = [param for param in required_params if not data.get(param)]
        if missing_params:
            return False, missing_params
        return True, []

    def json_response(self, success, message, data=None, status=200, code=None):
        """统一JSON响应格式"""
        response_data = {
            'success': success,
            'message': message,
            'code': code if code is not None else (20000 if success else 40000),
            'data': data if data is not None else {}
        }
        return JsonResponse(response_data, status=status)


class HTTPClient:
    """
    HTTP客户端工具类
    """

    @staticmethod
    def make_request(method, url, headers=None, json_data=None, params=None, timeout=30):
        """发起HTTP请求"""
        try:
            import requests
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=json_data, timeout=timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=json_data, timeout=timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            return {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': None
            }