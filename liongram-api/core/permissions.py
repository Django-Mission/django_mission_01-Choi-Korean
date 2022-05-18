from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOnly(BasePermission):
    # 작성자만 접근
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # 관리자
            if request.user.role == '10':
                return True
            elif hasattr(obj, 'profile'):
                return obj.profile.id == request.user.id
            elif obj.__class__ == get_user_model():
                return obj.id == request.user.id
            return False
        else:
            return False