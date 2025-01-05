# project/middlewares.py

from django.conf import settings

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # เรียกใช้งานการตั้งค่าของ Content Security Policy และ Permissions Policy จากไฟล์ settings
        csp = settings.SECURE_CONTENT_SECURITY_POLICY
        permissions_policy = settings.SECURE_PERMISSIONS_POLICY

        # รับการตอบกลับจากการเรียกใช้งาน middleware ก่อนหน้านี้
        response = self.get_response(request)

        # กำหนด Content-Security-Policy และ Permissions-Policy ใน header ของ response
        response['Content-Security-Policy'] = '; '.join(
            f"{key} {' '.join(value)}" for key, value in csp.items()
        )
        response['Permissions-Policy'] = ', '.join(
            f"{key}=({value})" for key, value in permissions_policy.items()
        )

        return response

